#!/usr/bin/env python3
"""Prototype CLI M2 pour preparer un ajout PERSON.

L'outil ne modifie aucun fichier du depot. Il lit le registre canonique des
sources, les registres PERSON canoniques et les artefacts people disponibles,
puis imprime une proposition deterministe.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml

try:
    from tools.m2_core import (
        CheckResult,
        add_source_diagnostics,
        build_pr_summary,
        exit_code,
        is_near_text_match,
        load_source_ids,
        normalize_text,
        render_result as render_m2_result,
        split_csv,
        unique_preserving_order,
        write_pr_summary,
    )
    from tools.schema_validation import validate_against_schema
except ImportError:  # execution directe: python3 tools/m2_add_person.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from m2_core import (
        CheckResult,
        add_source_diagnostics,
        build_pr_summary,
        exit_code,
        is_near_text_match,
        load_source_ids,
        normalize_text,
        render_result as render_m2_result,
        split_csv,
        unique_preserving_order,
        write_pr_summary,
    )
    from schema_validation import validate_against_schema


REPO_ROOT = Path(__file__).resolve().parent.parent
PERSON_ID_RE = re.compile(r"^PERSON-[a-z0-9]+(?:-[a-z0-9]+)*$")
PERS_ID_RE = re.compile(r"^PERS-[A-Za-z0-9-]+(?:#[a-z0-9-]+)?$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

VALID_CATEGORIES = (
    "membre",
    "entourage",
    "industrie",
    "critique_journaliste",
    "auteur_secondaire",
    "influence",
    "theoricien_mobilise",
)
VALID_CATEGORY_SET = set(VALID_CATEGORIES)


@dataclass(frozen=True)
class Paths:
    root: Path = REPO_ROOT
    source_registry: Path = REPO_ROOT / "data" / "registre.json"
    canonical_people: Path = REPO_ROOT / "registers" / "people" / "00_canonical_people.md"
    canonical_authors: Path = REPO_ROOT / "registers" / "people" / "00_authors_canonical.md"
    generated_people: Path = REPO_ROOT / "exports" / "generated" / "people.json"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = value.encode("ascii", "ignore").decode().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return re.sub(r"-+", "-", value)


def format_valid_categories() -> str:
    return ", ".join(VALID_CATEGORIES)


def iter_yaml_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records: list[dict] = []
    for block in YAML_BLOCK_RE.findall(path.read_text(encoding="utf-8")):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and str(data.get("id", "")).startswith("PERSON-"):
            records.append(data)
    return records


def load_person_records(paths: Paths) -> list[dict]:
    return iter_yaml_records(paths.canonical_people) + iter_yaml_records(paths.canonical_authors)


def load_provisional_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return set()
    ids: set[str] = set()
    for rec in payload:
        if not isinstance(rec, dict):
            continue
        pid = rec.get("data", {}).get("id", rec.get("id"))
        if pid and str(pid).startswith("PERS-") and not str(pid).startswith("PERSON-"):
            ids.add(str(pid))
    return ids


def build_same_as_index(records: Iterable[dict]) -> dict[str, str]:
    index: dict[str, str] = {}
    for rec in records:
        person_id = str(rec.get("id", ""))
        same_as = rec.get("same_as") or []
        if not isinstance(same_as, list):
            continue
        for raw in same_as:
            base = str(raw).split("#")[0]
            if base.startswith("PERS-"):
                index[base] = person_id
    return index


def infer_write_target(candidate: dict) -> str:
    same_as = candidate.get("same_as") or []
    if candidate.get("origine") == "auteur_source":
        return (
            "Cible d'ecriture probable : pipeline d'attribution vers "
            "registers/people/00_authors_canonical.md. Pourquoi : origine auteur_source. "
            "Il manque la validation humaine du pipeline d'attribution avant integration."
        )
    if same_as:
        return (
            "Cible d'ecriture probable : registers/people/*.md puis regeneration controlee de "
            "registers/people/00_canonical_people.md. Pourquoi : PERS-* fourni. "
            "Il manque la confirmation humaine du fichier source/provisoire a modifier."
        )
    return (
        "Aucun PERS-* fourni. Aucune cible d'ecriture source/provisoire n'est identifiable. "
        "Validation humaine necessaire avant integration."
    )


def build_candidate(
    *,
    name: str,
    category: str,
    roles: Sequence[str],
    sources: Sequence[str],
    aliases: Sequence[str] = (),
    same_as: Sequence[str] = (),
    note: str | None = None,
    origin: str | None = None,
    category_arbitration: bool = False,
    identity_arbitration: bool = False,
) -> dict:
    candidate = {
        "id": f"PERSON-{slugify(name)}",
        "type_unite": "person",
        "name": name.strip(),
        "categorie": category,
        "role": list(roles),
        "sources": list(sources),
        "same_as": list(same_as),
        "alt_names": list(aliases),
        "categorie_a_arbitrer": bool(category_arbitration),
        "a_arbitrer": bool(identity_arbitration),
    }
    if note:
        candidate["note"] = note.strip()
    if origin:
        candidate["origine"] = origin.strip()
    return candidate


def _validate_candidate_shape(candidate: dict) -> list[str]:
    diagnostics = list(validate_against_schema("person", candidate))

    required = {
        "id",
        "type_unite",
        "name",
        "categorie",
        "role",
        "sources",
        "same_as",
        "alt_names",
        "categorie_a_arbitrer",
        "a_arbitrer",
    }
    for key in sorted(required - set(candidate)):
        diagnostics.append(f"Missing required field: {key}")

    if candidate.get("type_unite") != "person":
        diagnostics.append("Invalid value for type_unite: expected person")
    if not isinstance(candidate.get("role"), list) or not candidate.get("role"):
        diagnostics.append("Field must be a non-empty list: role")
    if not isinstance(candidate.get("sources"), list) or not candidate.get("sources"):
        diagnostics.append("Field must be a non-empty list: sources")
    if not isinstance(candidate.get("same_as"), list):
        diagnostics.append("Field must be a list: same_as")
    if not isinstance(candidate.get("alt_names"), list):
        diagnostics.append("Field must be a list: alt_names")
    if not isinstance(candidate.get("categorie_a_arbitrer"), bool):
        diagnostics.append("Field must be a boolean: categorie_a_arbitrer")
    if not isinstance(candidate.get("a_arbitrer"), bool):
        diagnostics.append("Field must be a boolean: a_arbitrer")
    if candidate.get("origine") and candidate.get("origine") != "auteur_source":
        diagnostics.append(f"Invalid value for origine: {candidate.get('origine')}")

    return unique_preserving_order(diagnostics)


def evaluate_person_addition(
    *,
    name: str,
    category: str,
    roles: Sequence[str],
    sources: Sequence[str],
    aliases: Sequence[str] = (),
    same_as: Sequence[str] = (),
    note: str | None = None,
    origin: str | None = None,
    category_arbitration: bool = False,
    identity_arbitration: bool = False,
    paths: Paths | None = None,
) -> CheckResult:
    paths = paths or Paths()
    roles = unique_preserving_order(role.strip() for role in roles if role.strip())
    sources = unique_preserving_order(source.strip() for source in sources if source.strip())
    aliases = unique_preserving_order(alias.strip() for alias in aliases if alias.strip())
    same_as = unique_preserving_order(item.strip() for item in same_as if item.strip())

    candidate = build_candidate(
        name=name,
        category=category,
        roles=roles,
        sources=sources,
        aliases=aliases,
        same_as=same_as,
        note=note,
        origin=origin,
        category_arbitration=category_arbitration,
        identity_arbitration=identity_arbitration,
    )
    result = CheckResult(candidate=candidate)

    canonical_records = load_person_records(paths)
    existing_ids = {str(rec.get("id")) for rec in canonical_records if rec.get("id")}
    existing_names = {
        normalize_text(str(rec.get("name", ""))): str(rec.get("id", ""))
        for rec in canonical_records
        if rec.get("name")
    }
    existing_name_labels = {
        normalize_text(str(rec.get("name", ""))): (str(rec.get("id", "")), str(rec.get("name", "")))
        for rec in canonical_records
        if rec.get("name")
    }
    existing_aliases: dict[str, str] = {}
    existing_alias_labels: dict[str, tuple[str, str]] = {}
    for rec in canonical_records:
        rec_id = str(rec.get("id", ""))
        for alias in rec.get("alt_names") or []:
            existing_aliases[normalize_text(str(alias))] = rec_id
            existing_alias_labels[normalize_text(str(alias))] = (rec_id, str(alias))

    candidate_id = candidate["id"]
    if not PERSON_ID_RE.match(candidate_id):
        result.blockers.append(f"identifiant invalide: {candidate_id}")
    if candidate_id in existing_ids:
        result.blockers.append(f"identifiant deja utilise: {candidate_id}")

    normalized_name = normalize_text(name)
    if normalized_name in existing_names:
        result.blockers.append(f"collision certaine de nom: {name} deja present dans {existing_names[normalized_name]}")
    if normalized_name in existing_aliases:
        result.blockers.append(f"collision avec un alias existant: {name} dans {existing_aliases[normalized_name]}")

    if normalized_name not in existing_names and normalized_name not in existing_aliases:
        for rec_id, rec_name in existing_name_labels.values():
            if is_near_text_match(name, rec_name):
                result.reserves.append(f"nom proche a arbitrer: {name} ~ {rec_name} ({rec_id})")
        for rec_id, alias in existing_alias_labels.values():
            if is_near_text_match(name, alias):
                result.reserves.append(f"nom proche d'un alias a arbitrer: {name} ~ {alias} ({rec_id})")

    for alias in aliases:
        normalized_alias = normalize_text(alias)
        if normalized_alias in existing_names:
            result.blockers.append(f"alias deja present comme nom canonique: {alias} dans {existing_names[normalized_alias]}")
        if normalized_alias in existing_aliases:
            result.blockers.append(f"alias deja present: {alias} dans {existing_aliases[normalized_alias]}")
        if normalized_alias not in existing_names and normalized_alias not in existing_aliases:
            for rec_id, rec_name in existing_name_labels.values():
                if is_near_text_match(alias, rec_name):
                    result.reserves.append(f"alias proche d'un nom a arbitrer: {alias} ~ {rec_name} ({rec_id})")
            for rec_id, existing_alias in existing_alias_labels.values():
                if is_near_text_match(alias, existing_alias):
                    result.reserves.append(
                        f"alias proche d'un alias existant a arbitrer: {alias} ~ {existing_alias} ({rec_id})"
                    )

    canonical_sources = load_source_ids(paths.source_registry)
    add_source_diagnostics(result, sources=sources, canonical_sources=canonical_sources)

    category_is_valid = category in VALID_CATEGORY_SET
    if not category_is_valid:
        result.blockers.append(f"categorie invalide: {category} (categories autorisees: {format_valid_categories()})")
    if not roles:
        result.blockers.append("role absent")

    provisional_ids = load_provisional_ids(paths.generated_people)
    same_as_index = build_same_as_index(canonical_records)
    for item in same_as:
        base = item.split("#")[0]
        if item.startswith("PERSON-"):
            result.blockers.append(f"same_as interdit vers PERSON: {item}")
        elif not PERS_ID_RE.match(item):
            result.blockers.append(f"same_as invalide: {item}")
        elif base not in provisional_ids:
            result.blockers.append(f"same_as PERS introuvable: {item}")
        elif base in same_as_index:
            result.blockers.append(f"same_as deja rattache: {base} -> {same_as_index[base]}")

    if origin == "auteur_source" and same_as:
        result.blockers.append("auteur_source exige same_as vide")

    for diagnostic in _validate_candidate_shape(candidate):
        if not category_is_valid and diagnostic == f"Invalid value for categorie: {category}":
            continue
        result.blockers.append(f"schema invalide: {diagnostic}")

    if category_arbitration:
        result.reserves.append("categorie a arbitrer: double appartenance documentaire a confirmer")
    if identity_arbitration:
        result.reserves.append("identite a arbitrer: rattachement ou homonymie a confirmer")

    if not same_as and origin != "auteur_source":
        result.information.append(infer_write_target(candidate))
    if same_as and origin != "auteur_source":
        result.information.append(infer_write_target(candidate))
    if origin == "auteur_source":
        result.information.append(infer_write_target(candidate))
        result.information.append("auteur-source: verifier le pipeline d'attribution avant integration")

    result.finalize()
    return result


def dump_candidate_yaml(candidate: dict) -> str:
    return yaml.safe_dump(candidate, sort_keys=False, allow_unicode=True).strip()


def render_result(result: CheckResult) -> str:
    return render_m2_result(
        result,
        identifier=result.candidate["id"],
        candidate_language="yaml",
        rendered_candidate=dump_candidate_yaml(result.candidate),
    )


def build_person_pr_summary(result: CheckResult):
    candidate = result.candidate
    if result.blockers:
        arbitrations = ["Corriger les bloquants avant ouverture de PR."]
    elif result.reserves:
        arbitrations = ["Arbitrer les reserves PERSON avant integration."]
    else:
        arbitrations = ["Validation humaine finale avant integration."]
    return build_pr_summary(
        result,
        subject=f"Ajout PERSON : {candidate['name']} ({candidate['id']})",
        scope=[
            "Flux M2 ajout unitaire.",
            "Famille documentaire : PERSON.",
            "Lecture seule : aucune modification de registre effectuee par le prototype.",
            "Entree candidate YAML produite pour revue humaine.",
        ],
        validations=[
            "Pre-validation PERSON executee localement.",
            "Sources Sxx verifiees contre data/registre.json.",
            "Schema PERSON evalue sur l'entree candidate.",
            "Collisions nom, alias, identifiant et same_as evaluees.",
        ],
        human_arbitrations=arbitrations,
        documentary_impact=[
            "Proposition d'identite canonique PERSON.",
            "Aucun ajout effectif tant que la PR n'est pas relue et validee.",
        ],
        verification_commands=[
            "python3 tools/m2_add_person.py --help",
            "python3 -m unittest tools.test_m2_add_person",
            "python3 tools/validate_people.py",
        ],
    )


def write_person_pr_summary(result: CheckResult, paths: Paths) -> Path:
    filename = f"pr_summary_person_{slugify(result.candidate['id'])}.md"
    return write_pr_summary(
        build_person_pr_summary(result),
        output_dir=paths.root / "exports" / "generated",
        filename=filename,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare localement une proposition d'ajout PERSON sans modifier le depot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Categories autorisees:\n" + "\n".join(f"  - {category}" for category in VALID_CATEGORIES),
    )
    parser.add_argument("--name", required=True, help="Nom canonique de la personne.")
    parser.add_argument("--category", required=True, help="Categorie PERSON canonique. Voir la liste ci-dessous.")
    parser.add_argument(
        "--role",
        required=True,
        action="append",
        help="Role documentaire. Peut etre repete ou contenir une liste separee par des virgules.",
    )
    parser.add_argument(
        "--sources",
        required=True,
        help="Sources Sxx separees par des virgules, par exemple S41,S74.",
    )
    parser.add_argument("--aliases", help="Alias separes par des virgules.")
    parser.add_argument("--same-as", help="Identifiants PERS-* separes par des virgules.")
    parser.add_argument("--note", help="Note de prudence ou de canonicalisation.")
    parser.add_argument("--origin", choices=["auteur_source"], help="Origine optionnelle supportee par le schema.")
    parser.add_argument("--category-arbitration", action="store_true", help="Marque categorie_a_arbitrer=true.")
    parser.add_argument("--identity-arbitration", action="store_true", help="Marque a_arbitrer=true.")
    parser.add_argument(
        "--pr-summary",
        action="store_true",
        help="Ecrit un resume de PR M2 dans exports/generated sans ouvrir de PR GitHub.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = Paths()
    result = evaluate_person_addition(
        name=args.name,
        category=args.category,
        roles=split_csv(args.role),
        sources=split_csv([args.sources]),
        aliases=split_csv([args.aliases] if args.aliases else None),
        same_as=split_csv([args.same_as] if args.same_as else None),
        note=args.note,
        origin=args.origin,
        category_arbitration=args.category_arbitration,
        identity_arbitration=args.identity_arbitration,
        paths=paths,
    )
    sys.stdout.write(render_result(result))
    if args.pr_summary:
        path = write_person_pr_summary(result, paths)
        sys.stdout.write(f"Resume PR genere : {path.relative_to(paths.root)}\n")
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
