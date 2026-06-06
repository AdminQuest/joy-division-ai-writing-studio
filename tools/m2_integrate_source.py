#!/usr/bin/env python3
"""Prototype CLI M2 pour preparer l'integration d'une source longue.

L'outil est volontairement en lecture seule. Il lit `data/registre.json`,
diagnostique la source candidate et imprime une proposition preparatoire sans
creer de source canonique, dossier source, atome, citation, relation, branche ou
Pull Request.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from tools.m2_core import CheckResult, exit_code, is_near_text_match, normalize_text, render_list
except ImportError:  # execution directe: python3 tools/m2_integrate_source.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from m2_core import CheckResult, exit_code, is_near_text_match, normalize_text, render_list


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ID_RE = re.compile(r"^S(\d+)$")
VALID_TYPES = (
    "livre",
    "article",
    "interview",
    "fanzine",
    "archive",
    "memoire",
    "these",
    "dossier documentaire",
)
TYPE_ALIASES = {"dossier_documentaire": "dossier documentaire"}


@dataclass(frozen=True)
class Paths:
    root: Path = REPO_ROOT
    source_registry: Path = REPO_ROOT / "data" / "registre.json"


def slugify_source(author: str, title: str) -> str:
    value = f"{author} {title}"
    value = unicodedata.normalize("NFD", value or "")
    value = value.encode("ascii", "ignore").decode().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    value = re.sub(r"_+", "_", value)
    return value[:80].rstrip("_") or "source_candidate"


def canonical_type(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", (value or "").strip().lower().replace("-", "_"))
    return TYPE_ALIASES.get(cleaned, cleaned)


def format_valid_types() -> str:
    return ", ".join(VALID_TYPES)


def load_registry(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def next_source_id(records: Sequence[dict]) -> str:
    numbers: list[int] = []
    for rec in records:
        match = SOURCE_ID_RE.match(str(rec.get("id", "")))
        if match:
            numbers.append(int(match.group(1)))
    next_number = max(numbers, default=0) + 1
    return f"S{next_number:02d}" if next_number < 100 else f"S{next_number}"


def same_text(left: object, right: str) -> bool:
    return normalize_text(str(left or "")) == normalize_text(right)


def same_author(left: object, right: str) -> bool:
    left_norm = normalize_text(str(left or ""))
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return False
    left_tokens = sorted(left_norm.split())
    right_tokens = sorted(right_norm.split())
    return left_norm == right_norm or left_norm in right_norm or right_norm in left_norm or left_tokens == right_tokens


def short_source(rec: dict) -> str:
    source_id = str(rec.get("id", "source inconnue"))
    title = str(rec.get("titre") or rec.get("source_label") or "titre inconnu")
    year = str(rec.get("annee") or "annee inconnue")
    return f"{source_id} - {title} ({year})"


def find_existing_source(records: Sequence[dict], *, title: str, author: str, year: str, reference: str, url: str | None) -> dict | None:
    clean_url = (url or "").strip()
    for rec in records:
        title_equal = same_text(rec.get("titre"), title)
        author_equal = same_author(rec.get("auteur"), author)
        year_equal = same_text(rec.get("annee"), year)
        reference_equal = bool(reference.strip()) and same_text(rec.get("reference_complete"), reference)
        url_equal = bool(clean_url) and (
            same_text(rec.get("url"), clean_url)
            or same_text(rec.get("source_url"), clean_url)
            or same_text(rec.get("source_drive"), clean_url)
            or clean_url in str(rec.get("reference_complete") or "")
        )
        if (title_equal and author_equal and year_equal) or reference_equal or url_equal:
            return rec
    return None


def find_near_sources(records: Sequence[dict], *, title: str, author: str, year: str, reference: str) -> list[str]:
    reserves: list[str] = []
    for rec in records:
        rec_title = str(rec.get("titre") or "")
        rec_author = str(rec.get("auteur") or "")
        rec_year = str(rec.get("annee") or "")
        rec_reference = str(rec.get("reference_complete") or "")
        rec_label = short_source(rec)

        title_equal = same_text(rec_title, title)
        author_equal = same_author(rec_author, author)
        year_equal = same_text(rec_year, year)

        if title_equal and author_equal and not year_equal:
            reserves.append(f"source proche detectee : autre edition ou reedition possible ({rec_label})")
            continue

        if title_equal and not author_equal:
            reserves.append(f"source proche detectee : variante de titre ({rec_label})")
            continue

        if author_equal and is_near_text_match(title, rec_title):
            reserves.append(f"source proche detectee : titre proche ({rec_label})")
            continue

        if reference and rec_reference and is_near_text_match(reference, rec_reference):
            reserves.append(f"source proche detectee : reference proche ({rec_label})")

    return reserves


def build_candidate(
    *,
    title: str,
    author: str,
    source_type: str,
    year: str,
    reference: str,
    url: str | None,
    edition: str | None,
    publication: str | None,
    pages_useful: str | None,
    section_useful: str | None,
    existing_source: dict | None,
    probable_source_id: str,
    dossier_slug: str,
) -> dict:
    if existing_source:
        source_status = "source deja presente"
        source_id = str(existing_source.get("id", ""))
        dossier_source = str(existing_source.get("dossier_source") or f"sources/{dossier_slug}/")
    else:
        source_status = "nouvelle source probable"
        source_id = f"{probable_source_id} (probable, non attribue)"
        dossier_source = f"sources/{dossier_slug}/"

    metadata = {
        "titre": title.strip(),
        "auteur": author.strip(),
        "annee": year.strip(),
        "reference_complete": reference.strip(),
    }
    optional = {
        "url": url,
        "edition": edition,
        "publication": publication,
        "pages_utiles": pages_useful,
        "section_utile": section_useful,
    }
    for key, value in optional.items():
        if value and value.strip():
            metadata[key] = value.strip()

    return {
        "type_documentaire": source_type,
        "source_probable": source_status,
        "sxx": source_id,
        "dossier_source_probable": dossier_source,
        "fichiers_potentiellement_concernes": [
            "data/registre.json",
            dossier_source,
        ],
        "metadata": metadata,
    }


def evaluate_source_integration(
    *,
    title: str,
    author: str,
    source_type: str,
    year: str,
    reference: str,
    url: str | None = None,
    edition: str | None = None,
    publication: str | None = None,
    pages_useful: str | None = None,
    section_useful: str | None = None,
    paths: Paths | None = None,
) -> CheckResult:
    paths = paths or Paths()
    records = load_registry(paths.source_registry)
    normalized_type = canonical_type(source_type)
    dossier_slug = slugify_source(author, title)
    probable_source_id = next_source_id(records)
    existing_source = find_existing_source(
        records,
        title=title,
        author=author,
        year=year,
        reference=reference,
        url=url,
    )
    candidate = build_candidate(
        title=title,
        author=author,
        source_type=normalized_type,
        year=year,
        reference=reference,
        url=url,
        edition=edition,
        publication=publication,
        pages_useful=pages_useful,
        section_useful=section_useful,
        existing_source=existing_source,
        probable_source_id=probable_source_id,
        dossier_slug=dossier_slug,
    )
    result = CheckResult(candidate=candidate)

    if not title.strip():
        result.blockers.append("titre absent")
    if not author.strip():
        result.blockers.append("auteur absent")
    if not year.strip():
        result.blockers.append("annee absente")
    if normalized_type not in VALID_TYPES:
        result.blockers.append(f"type documentaire inconnu: {source_type} (types autorises: {format_valid_types()})")

    if existing_source:
        result.blockers.append(f"source deja presente de facon certaine: {short_source(existing_source)}")
    else:
        result.reserves.extend(find_near_sources(records, title=title, author=author, year=year, reference=reference))

    if not reference.strip():
        result.reserves.append("reference complete absente ou vide: qualification bibliographique a completer")
    if edition:
        result.information.append(f"edition fournie: {edition.strip()}")
    if publication:
        result.information.append(f"publication associee: {publication.strip()}")
    if pages_useful:
        result.information.append(f"pages utiles signalees: {pages_useful.strip()}")
    if section_useful:
        result.information.append(f"section utile signalee: {section_useful.strip()}")

    if existing_source:
        result.information.append(f"Sxx existant: {existing_source.get('id')}")
    else:
        result.information.append(f"nouveau Sxx probablement requis: {probable_source_id}")
    result.information.append(f"dossier source probable: {candidate['dossier_source_probable']}")
    result.information.append("lecture seule: aucun fichier cree ou modifie")

    result.finalize()
    return result


def render_metadata(metadata: dict) -> list[str]:
    return [f"  {key}: {value}" for key, value in metadata.items()]


def render_result(result: CheckResult) -> str:
    candidate = result.candidate
    lines = [
        f"Decision : {result.decision}",
        "Bloquants :",
        *render_list(result.blockers),
        "Reserves :",
        *render_list(result.reserves),
        "Informations :",
        *render_list(result.information),
        "Proposition :",
        f"- type documentaire : {candidate['type_documentaire']}",
        f"- source probable : {candidate['source_probable']}",
        f"- Sxx : {candidate['sxx']}",
        f"- dossier source probable : {candidate['dossier_source_probable']}",
        "- fichiers potentiellement concernes :",
        *[f"  - {path}" for path in candidate["fichiers_potentiellement_concernes"]],
        "- metadonnees candidates :",
        *render_metadata(candidate["metadata"]),
    ]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare localement un diagnostic d'integration de source longue sans modifier le depot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Types autorises:\n" + "\n".join(f"  - {source_type}" for source_type in VALID_TYPES),
    )
    parser.add_argument("--title", required=True, help="Titre de la source candidate.")
    parser.add_argument("--author", required=True, help="Auteur, autrice ou responsable documentaire.")
    parser.add_argument("--type", required=True, help="Type documentaire M2.3. Voir la liste ci-dessous.")
    parser.add_argument("--year", required=True, help="Annee ou date principale de la source.")
    parser.add_argument("--reference", required=True, help="Reference bibliographique complete ou description equivalente.")
    parser.add_argument("--url", help="URL utile si elle fait partie de l'identification.")
    parser.add_argument("--edition", help="Edition, version ou tirage consulte.")
    parser.add_argument("--publication", help="Publication, revue, fanzine ou support parent.")
    parser.add_argument("--pages-useful", help="Pages utiles ou pagination traitee.")
    parser.add_argument("--section-useful", help="Section, chapitre ou partie utile.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = evaluate_source_integration(
        title=args.title,
        author=args.author,
        source_type=args.type,
        year=args.year,
        reference=args.reference,
        url=args.url,
        edition=args.edition,
        publication=args.publication,
        pages_useful=args.pages_useful,
        section_useful=args.section_useful,
    )
    sys.stdout.write(render_result(result))
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
