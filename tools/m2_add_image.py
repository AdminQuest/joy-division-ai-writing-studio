#!/usr/bin/env python3
"""CLI M2 pour preparer un ajout IMAGE.

L'outil ne modifie aucun fichier du depot. Il lit le registre canonique des
images, le registre des sources, quelques registres lies et le schema IMAGE,
puis imprime un diagnostic deterministe destine a la revue humaine.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml

try:
    from tools.m2_core import (
        CheckResult,
        build_pr_summary,
        exit_code,
        format_values,
        is_near_text_match,
        load_source_ids,
        normalize_text,
        render_result as render_m2_result,
        split_csv,
        unique_preserving_order,
        write_pr_summary,
    )
except ImportError:  # execution directe: python3 tools/m2_add_image.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from m2_core import (
        CheckResult,
        build_pr_summary,
        exit_code,
        format_values,
        is_near_text_match,
        load_source_ids,
        normalize_text,
        render_result as render_m2_result,
        split_csv,
        unique_preserving_order,
        write_pr_summary,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent
CURRENT_DRIFT_VERSION = "v1.0"

IMAGE_ID_RE = re.compile(r"^IMAGE-(S|I)-[0-9]{4}$")
SESSION_ID_RE = re.compile(r"^IMAGE-S-[0-9]{4}$")
IMAGE_ITEM_ID_RE = re.compile(r"^IMAGE-I-[0-9]{4}$")
PERSON_ID_RE = re.compile(r"^PERSON-[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACE_ID_RE = re.compile(r"^PLACE-[A-Z0-9][A-Z0-9-]*$")
SOURCE_ID_RE = re.compile(r"^S\d+$")
URL_RE = re.compile(r"^https?://")
DATE_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
DATE_YEAR_RE = re.compile(r"^\d{4}$")
LAST_VERIFIED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKIDATA_RE = re.compile(r"^Q\d+$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

VALID_LEVELS = ("session", "image")
VALID_LEVEL_SET = set(VALID_LEVELS)
VALID_CONTEXTS = ("promo", "live", "portrait", "artwork", "rehearsal", "other")
VALID_CONTEXT_SET = set(VALID_CONTEXTS)
VALID_DATE_PRECISIONS = ("day", "month", "year", "approximate")
VALID_DATE_PRECISION_SET = set(VALID_DATE_PRECISIONS)
VALID_GATES = ("public", "private")
VALID_GATE_SET = set(VALID_GATES)


@dataclass(frozen=True)
class Paths:
    root: Path = REPO_ROOT
    source_registry: Path = REPO_ROOT / "data" / "registre.json"
    images_json: Path = REPO_ROOT / "registers" / "images" / "images.json"
    schema_json: Path = REPO_ROOT / "schemas" / "image_canonical.schema.json"
    canonical_people: Path = REPO_ROOT / "registers" / "people" / "00_canonical_people.md"
    canonical_authors: Path = REPO_ROOT / "registers" / "people" / "00_authors_canonical.md"
    places_root: Path = REPO_ROOT / "registers" / "places"


def load_image_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def next_image_id(records: Sequence[dict], level: str) -> str:
    prefix = "IMAGE-S" if level == "session" else "IMAGE-I"
    numbers: list[int] = []
    for rec in records:
        image_id = str(rec.get("image_id", ""))
        if image_id.startswith(f"{prefix}-") and IMAGE_ID_RE.match(image_id):
            numbers.append(int(image_id.split("-")[-1]))
    next_number = max(numbers, default=0) + 1
    return f"{prefix}-{next_number:04d}"


def iter_yaml_records(path: Path, prefix: str) -> list[dict]:
    if not path.exists():
        return []
    records: list[dict] = []
    for block in YAML_BLOCK_RE.findall(path.read_text(encoding="utf-8")):
        data = yaml.safe_load(block)
        if isinstance(data, dict) and str(data.get("id", "")).startswith(prefix):
            records.append(data)
    return records


def load_person_ids(paths: Paths) -> set[str]:
    records = iter_yaml_records(paths.canonical_people, "PERSON-")
    records.extend(iter_yaml_records(paths.canonical_authors, "PERSON-"))
    return {str(rec.get("id")) for rec in records if rec.get("id")}


def iter_place_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def load_place_ids(paths: Paths) -> set[str]:
    ids: set[str] = set()
    for path in iter_place_files(paths.places_root):
        for block in YAML_BLOCK_RE.findall(path.read_text(encoding="utf-8")):
            data = yaml.safe_load(block)
            if not isinstance(data, dict):
                continue
            places = data.get("places")
            if isinstance(places, list):
                ids.update(str(item.get("id")) for item in places if isinstance(item, dict) and item.get("id"))
            elif str(data.get("id", "")).startswith("PLACE-"):
                ids.add(str(data["id"]))
    return ids


def build_candidate(
    *,
    image_id: str,
    level: str,
    name: str,
    photographer: str,
    date: str,
    date_precision: str,
    subjects: Sequence[str],
    sources: Sequence[str],
    session_ref: str | None = None,
    place: str | None = None,
    event_ref: str | None = None,
    context: str = "other",
    output_count: int | None = None,
    usage: Sequence[str] = (),
    iconic: bool = False,
    notes: str | None = None,
    gate: str = "private",
    last_verified: str = "",
    wikidata: str | None = None,
) -> dict:
    candidate = {
        "image_id": image_id,
        "level": level.strip(),
        "canonical_name": name.strip(),
        "photographer": photographer.strip(),
        "date": date.strip(),
        "date_precision": date_precision.strip(),
        "subjects": list(subjects),
        "sources": list(sources),
        "same_as": {"wikidata": wikidata.strip() if wikidata else None},
        "identity_frozen": True,
        "drift_sentinel": CURRENT_DRIFT_VERSION,
        "gate": gate.strip(),
        "last_verified": last_verified.strip(),
    }
    if level == "session":
        candidate["session_ref"] = None
    elif session_ref:
        candidate["session_ref"] = session_ref.strip()
    if place:
        candidate["place"] = place.strip()
    else:
        candidate["place"] = None
    if event_ref:
        candidate["event_ref"] = event_ref.strip()
    candidate["context"] = context.strip()
    if output_count is not None:
        candidate["output_count"] = output_count
    if usage:
        candidate["usage"] = list(usage)
    if iconic:
        candidate["iconic"] = True
    if notes:
        candidate["notes"] = notes.strip()
    return candidate


def _validate_candidate_shape(candidate: dict, schema_path: Path) -> list[str]:
    diagnostics: list[str] = []
    try:
        from jsonschema import Draft202012Validator, FormatChecker

        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(validator.iter_errors(candidate), key=lambda err: list(err.path)):
            path = ".".join(str(part) for part in error.path)
            prefix = f"{path}: " if path else ""
            diagnostics.append(f"{prefix}{error.message}")
    except ImportError:
        diagnostics.append("jsonschema indisponible: validation Draft 2020-12 non executee")
    except FileNotFoundError:
        diagnostics.append(f"schema IMAGE introuvable: {schema_path}")
    return unique_preserving_order(diagnostics)


def add_source_diagnostics_for_image(result: CheckResult, *, sources: Sequence[str], canonical_sources: set[str]) -> None:
    if not sources:
        result.blockers.append("source absente")
        return
    for source in sources:
        if SOURCE_ID_RE.match(source):
            if source not in canonical_sources:
                result.blockers.append(f"source inconnue: {source}")
        elif URL_RE.match(source):
            result.reserves.append(f"source URL non canonique a arbitrer: {source}")
        else:
            result.blockers.append(f"source invalide: {source}")


def validate_date(result: CheckResult, *, image_id: str, date: str, precision: str) -> None:
    if precision == "day" and not DATE_DAY_RE.match(date):
        result.blockers.append(f"date invalide pour precision day: {date or '<vide>'}")
    elif precision == "month" and not DATE_MONTH_RE.match(date):
        result.blockers.append(f"date invalide pour precision month: {date or '<vide>'}")
    elif precision == "year" and not DATE_YEAR_RE.match(date):
        result.blockers.append(f"date invalide pour precision year: {date or '<vide>'}")
    elif precision == "approximate":
        result.reserves.append(f"date ou periode approximative a confirmer: {image_id}")


def evaluate_image_addition(
    *,
    level: str,
    name: str,
    photographer: str,
    sources: Sequence[str],
    last_verified: str,
    date: str = "",
    date_precision: str = "approximate",
    subjects: Sequence[str] = (),
    session_ref: str | None = None,
    place: str | None = None,
    event_ref: str | None = None,
    context: str = "other",
    output_count: int | None = None,
    usage: Sequence[str] = (),
    iconic: bool = False,
    notes: str | None = None,
    gate: str = "private",
    wikidata: str | None = None,
    image_id: str | None = None,
    rights_uncertain: bool = False,
    attribution_uncertain: bool = False,
    paths: Paths | None = None,
) -> CheckResult:
    paths = paths or Paths()
    records = load_image_records(paths.images_json)
    level = level.strip()
    sources = unique_preserving_order(source.strip() for source in sources if source.strip())
    subjects = unique_preserving_order(subject.strip() for subject in subjects if subject.strip())
    usage = unique_preserving_order(item.strip() for item in usage if item.strip())
    image_id = image_id.strip() if image_id else next_image_id(records, level)
    candidate = build_candidate(
        image_id=image_id,
        level=level,
        name=name,
        photographer=photographer,
        date=date,
        date_precision=date_precision,
        subjects=subjects,
        sources=sources,
        session_ref=session_ref,
        place=place,
        event_ref=event_ref,
        context=context,
        output_count=output_count,
        usage=usage,
        iconic=iconic,
        notes=notes,
        gate=gate,
        last_verified=last_verified,
        wikidata=wikidata,
    )
    result = CheckResult(candidate=candidate)

    existing_ids = {str(rec.get("image_id")) for rec in records if rec.get("image_id")}
    existing_names = {
        normalize_text(str(rec.get("canonical_name", ""))): (
            str(rec.get("image_id", "")),
            str(rec.get("canonical_name", "")),
        )
        for rec in records
        if rec.get("canonical_name")
    }
    session_ids = {str(rec.get("image_id")) for rec in records if rec.get("level") == "session"}

    if level not in VALID_LEVEL_SET:
        result.blockers.append(f"level invalide: {level} (valeurs autorisees: {format_values(VALID_LEVELS)})")
    elif level == "session" and not SESSION_ID_RE.match(image_id):
        result.blockers.append(f"identifiant incompatible avec level=session: {image_id}")
    elif level == "image" and not IMAGE_ITEM_ID_RE.match(image_id):
        result.blockers.append(f"identifiant incompatible avec level=image: {image_id}")
    if not IMAGE_ID_RE.match(image_id):
        result.blockers.append(f"identifiant image invalide: {image_id}")
    if image_id in existing_ids:
        result.blockers.append(f"identifiant deja utilise: {image_id}")

    normalized_name = normalize_text(name)
    if normalized_name in existing_names:
        rec_id, _ = existing_names[normalized_name]
        result.blockers.append(f"collision certaine de libelle: {name} deja present dans {rec_id}")
    else:
        for rec_id, rec_name in existing_names.values():
            if is_near_text_match(name, rec_name):
                result.reserves.append(f"image proche a arbitrer: {name} ~ {rec_name} ({rec_id})")

    if level == "image":
        if not session_ref:
            result.blockers.append("session_ref absent pour level=image")
        elif not SESSION_ID_RE.match(session_ref):
            result.blockers.append(f"session_ref invalide: {session_ref}")
        elif session_ref not in session_ids:
            result.blockers.append(f"session_ref introuvable: {session_ref}")

    person_ids = load_person_ids(paths)
    if not photographer.strip():
        result.blockers.append("photographer absent")
    elif not PERSON_ID_RE.match(photographer):
        result.blockers.append(f"photographer invalide: {photographer}")
    elif photographer not in person_ids:
        result.blockers.append(f"photographer PERSON introuvable: {photographer}")
    for subject in subjects:
        if subject.startswith("PERSON-") and subject not in person_ids:
            result.reserves.append(f"sujet PERSON introuvable a arbitrer: {subject}")

    place_ids = load_place_ids(paths)
    if place and place.startswith("PLACE-") and place not in place_ids:
        result.reserves.append(f"lieu PLACE introuvable a arbitrer: {place}")

    canonical_sources = load_source_ids(paths.source_registry)
    add_source_diagnostics_for_image(result, sources=sources, canonical_sources=canonical_sources)

    if date_precision not in VALID_DATE_PRECISION_SET:
        result.blockers.append(
            f"date_precision invalide: {date_precision} (valeurs autorisees: {format_values(VALID_DATE_PRECISIONS)})"
        )
    else:
        validate_date(result, image_id=image_id, date=date.strip(), precision=date_precision)
    if context not in VALID_CONTEXT_SET:
        result.blockers.append(f"context invalide: {context} (valeurs autorisees: {format_values(VALID_CONTEXTS)})")
    if gate not in VALID_GATE_SET:
        result.blockers.append(f"gate invalide: {gate} (valeurs autorisees: {format_values(VALID_GATES)})")
    if not LAST_VERIFIED_RE.match(last_verified):
        result.blockers.append(f"last_verified invalide: {last_verified}")
    if wikidata and not WIKIDATA_RE.match(wikidata):
        result.blockers.append(f"wikidata invalide: {wikidata}")
    if rights_uncertain:
        result.reserves.append("droits image a arbitrer: ne pas publier ni reproduire sans validation humaine")
    if attribution_uncertain:
        result.reserves.append("attribution photographe a arbitrer: ne pas transformer l'hypothese en fait etabli")

    result.information.append(f"prochain identifiant detecte pour {level}: {image_id}")
    result.information.append("cible d'ecriture probable: registers/images/images.json")
    result.information.append("lecture seule: aucune modification du registre IMAGE")

    for diagnostic in _validate_candidate_shape(candidate, paths.schema_json):
        result.blockers.append(f"schema invalide: {diagnostic}")

    result.finalize()
    return result


def dump_candidate_json(candidate: dict) -> str:
    return json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=False)


def render_result(result: CheckResult) -> str:
    return render_m2_result(
        result,
        identifier=result.candidate["image_id"],
        candidate_language="json",
        rendered_candidate=dump_candidate_json(result.candidate),
    )


def build_image_pr_summary(result: CheckResult):
    candidate = result.candidate
    if result.blockers:
        arbitrations = ["Corriger les bloquants avant ouverture de PR."]
    elif result.reserves:
        arbitrations = ["Arbitrer les reserves IMAGE avant integration."]
    else:
        arbitrations = ["Validation humaine finale avant integration."]
    return build_pr_summary(
        result,
        subject=f"Ajout IMAGE : {candidate['canonical_name']} ({candidate['image_id']})",
        scope=[
            "Flux M2 ajout unitaire.",
            "Famille documentaire : IMAGE.",
            "Lecture seule : aucune modification du registre IMAGE effectuee par le prototype.",
            "Entree candidate JSON produite pour revue humaine.",
        ],
        validations=[
            "Pre-validation IMAGE executee localement.",
            "Sources Sxx verifiees contre data/registre.json, URL signalees en reserve.",
            "Schema IMAGE evalue sur l'entree candidate.",
            "Collisions libelle et identifiant evaluees.",
            "Contraintes session/image et session_ref evaluees.",
            "References photographe, sujets PERSON et lieu PLACE inspectees.",
        ],
        human_arbitrations=arbitrations,
        documentary_impact=[
            "Proposition d'objet iconographique IMAGE.",
            "Aucune image canonique et aucun fichier image ne sont crees automatiquement.",
            "Aucun ajout effectif tant que la PR n'est pas relue et validee.",
        ],
        verification_commands=[
            "python3 tools/m2_add_image.py --help",
            "python3 -m unittest tools.test_m2_add_image",
            "python3 tools/validate_images.py",
        ],
    )


def write_image_pr_summary(result: CheckResult, paths: Paths) -> Path:
    name_slug = normalize_text(result.candidate["canonical_name"]).replace(" ", "-")
    filename = f"pr_summary_image_{result.candidate['image_id'].lower()}_{name_slug}.md"
    return write_pr_summary(
        build_image_pr_summary(result),
        output_dir=paths.root / "exports" / "generated",
        filename=filename,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare localement une proposition d'ajout IMAGE sans modifier le depot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Levels autorises:\n"
            + "\n".join(f"  - {level}" for level in VALID_LEVELS)
            + "\n\nContextes autorises:\n"
            + "\n".join(f"  - {context}" for context in VALID_CONTEXTS)
            + "\n\nPrecisions de date autorisees:\n"
            + "\n".join(f"  - {precision}" for precision in VALID_DATE_PRECISIONS)
        ),
    )
    parser.add_argument("--level", required=True, choices=VALID_LEVELS, help="Niveau IMAGE: session ou image.")
    parser.add_argument("--name", required=True, help="Designation canonique de la session ou du cliche.")
    parser.add_argument("--photographer", required=True, help="Identifiant PERSON- du photographe.")
    parser.add_argument("--sources", required=True, help="Sources Sxx separees par des virgules, ou URL a arbitrer.")
    parser.add_argument("--last-verified", required=True, help="Date de verification humaine au format YYYY-MM-DD.")
    parser.add_argument("--date", default="", help="Date ISO complete ou partielle selon --date-precision.")
    parser.add_argument("--date-precision", default="approximate", choices=VALID_DATE_PRECISIONS)
    parser.add_argument("--subjects", help="Sujets PERSON- ou descriptions libres separes par des virgules.")
    parser.add_argument("--session-ref", help="Session IMAGE-S-NNNN parente, obligatoire pour level=image.")
    parser.add_argument("--place", help="Lieu PLACE- ou description libre.")
    parser.add_argument("--event-ref", help="Reference EVENT- si disponible.")
    parser.add_argument("--context", default="other", choices=VALID_CONTEXTS)
    parser.add_argument("--output-count", type=int, help="Nombre de cliches connus pour une session.")
    parser.add_argument("--usage", help="Usages connus separes par des virgules.")
    parser.add_argument("--iconic", action="store_true", help="Marque iconic=true.")
    parser.add_argument("--notes", help="Notes documentaires libres.")
    parser.add_argument("--gate", default="private", choices=VALID_GATES, help="Gate de visibilite. Par defaut: private.")
    parser.add_argument("--wikidata", help="Identifiant Wikidata Q... verifie.")
    parser.add_argument("--image-id", help="Identifiant IMAGE explicite, sinon prochain identifiant disponible.")
    parser.add_argument("--rights-uncertain", action="store_true", help="Ajoute une reserve de droits.")
    parser.add_argument("--attribution-uncertain", action="store_true", help="Ajoute une reserve d'attribution.")
    parser.add_argument(
        "--pr-summary",
        action="store_true",
        help="Ecrit un resume de PR M2 dans exports/generated sans ouvrir de PR GitHub.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = Paths()
    result = evaluate_image_addition(
        level=args.level,
        name=args.name,
        photographer=args.photographer,
        sources=split_csv([args.sources]),
        last_verified=args.last_verified,
        date=args.date,
        date_precision=args.date_precision,
        subjects=split_csv([args.subjects] if args.subjects else None),
        session_ref=args.session_ref,
        place=args.place,
        event_ref=args.event_ref,
        context=args.context,
        output_count=args.output_count,
        usage=split_csv([args.usage] if args.usage else None),
        iconic=args.iconic,
        notes=args.notes,
        gate=args.gate,
        wikidata=args.wikidata,
        image_id=args.image_id,
        rights_uncertain=args.rights_uncertain,
        attribution_uncertain=args.attribution_uncertain,
        paths=paths,
    )
    sys.stdout.write(render_result(result))
    if args.pr_summary:
        path = write_image_pr_summary(result, paths)
        sys.stdout.write(f"Resume PR genere : {path.relative_to(paths.root)}\n")
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
