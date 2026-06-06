#!/usr/bin/env python3
"""CLI M2 pour preparer un ajout PLACE.

L'outil ne modifie aucun fichier du depot. Il lit le registre canonique des
sources, les registres PLACE existants et le schema des lieux, puis imprime un
diagnostic deterministe destine a une revue humaine.
"""

from __future__ import annotations

import argparse
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
        format_values,
        is_near_text_match,
        load_source_ids,
        normalize_text,
        render_result as render_m2_result,
        split_csv,
        unique_preserving_order,
        write_pr_summary,
    )
except ImportError:  # execution directe: python3 tools/m2_add_place.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from m2_core import (
        CheckResult,
        add_source_diagnostics,
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
PLACE_ID_RE = re.compile(r"^PLACE-[A-Z0-9][A-Z0-9-]*$")
SOURCE_ID_RE = re.compile(r"^S\d+$")
YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)
DEFAULT_PLACE_TYPES = (
    "ville",
    "quartier",
    "habitat",
    "studio",
    "salle",
    "commerce",
    "education",
    "sante",
    "industrie",
    "science",
    "infrastructure",
    "pouvoir",
    "lieu_memoire",
)


@dataclass(frozen=True)
class Paths:
    root: Path = REPO_ROOT
    source_registry: Path = REPO_ROOT / "data" / "registre.json"
    places_root: Path = REPO_ROOT / "registers" / "places"
    schema_yaml: Path = REPO_ROOT / "schemas" / "places.schema.yaml"


def slugify_place(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = value.encode("ascii", "ignore").decode().upper()
    value = re.sub(r"[^A-Z0-9]+", "-", value).strip("-")
    return re.sub(r"-+", "-", value)


def slugify_filename(value: str) -> str:
    slug = normalize_text(value).replace(" ", "-")
    return slug or "place"


def iter_place_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def iter_place_records(path: Path) -> list[dict]:
    records: list[dict] = []
    if not path.exists():
        return records
    for block in YAML_BLOCK_RE.findall(path.read_text(encoding="utf-8")):
        data = yaml.safe_load(block)
        if isinstance(data, dict):
            places = data.get("places")
            if isinstance(places, list):
                records.extend(
                    item
                    for item in places
                    if isinstance(item, dict) and str(item.get("id", "")).startswith("PLACE-")
                )
            elif str(data.get("id", "")).startswith("PLACE-"):
                records.append(data)
    return records


def load_place_records(paths: Paths) -> list[dict]:
    records: list[dict] = []
    for path in iter_place_files(paths.places_root):
        records.extend(iter_place_records(path))
    return records


def load_place_types(schema_path: Path) -> tuple[str, ...]:
    if not schema_path.exists():
        return DEFAULT_PLACE_TYPES
    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        return DEFAULT_PLACE_TYPES
    properties = schema.get("properties") or {}
    type_schema = properties.get("type") or {}
    enum = type_schema.get("enum")
    if not isinstance(enum, list):
        return DEFAULT_PLACE_TYPES
    values = tuple(str(item) for item in enum if str(item))
    return values or DEFAULT_PLACE_TYPES


def build_candidate(
    *,
    label: str,
    place_type: str,
    sources: Sequence[str],
    type_detail: str | None = None,
    usage: str | None = None,
    prudence: str | None = None,
) -> dict:
    candidate = {
        "id": f"PLACE-{slugify_place(label)}",
        "label": label.strip(),
        "type": place_type.strip(),
        "sources": list(sources),
    }
    if type_detail:
        candidate["type_detail"] = type_detail.strip()
    if usage:
        candidate["usage"] = usage.strip()
    if prudence:
        candidate["prudence"] = prudence.strip()
    return candidate


def _validate_candidate_shape(candidate: dict, schema_path: Path) -> list[str]:
    diagnostics: list[str] = []
    required = ("id", "label", "type")
    for key in required:
        if key not in candidate:
            diagnostics.append(f"Missing required field: {key}")

    place_id = str(candidate.get("id", ""))
    if not PLACE_ID_RE.match(place_id):
        diagnostics.append(f"Invalid value for id: {place_id}")
    if not str(candidate.get("label", "")).strip():
        diagnostics.append("Field must be non-empty: label")
    if not isinstance(candidate.get("sources"), list) or not candidate.get("sources"):
        diagnostics.append("Field must be a non-empty list: sources")

    try:
        from jsonschema import Draft202012Validator

        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(candidate), key=lambda err: list(err.path)):
            path = ".".join(str(part) for part in error.path)
            prefix = f"{path}: " if path else ""
            diagnostics.append(f"{prefix}{error.message}")
    except ImportError:
        diagnostics.append("jsonschema indisponible: validation Draft 2020-12 non executee")
    except FileNotFoundError:
        diagnostics.append(f"schema PLACE introuvable: {schema_path}")

    return unique_preserving_order(diagnostics)


def evaluate_place_addition(
    *,
    label: str,
    place_type: str,
    sources: Sequence[str],
    aliases: Sequence[str] = (),
    type_detail: str | None = None,
    usage: str | None = None,
    prudence: str | None = None,
    paths: Paths | None = None,
) -> CheckResult:
    paths = paths or Paths()
    sources = unique_preserving_order(source.strip() for source in sources if source.strip())
    aliases = unique_preserving_order(alias.strip() for alias in aliases if alias.strip())
    candidate = build_candidate(
        label=label,
        place_type=place_type,
        sources=sources,
        type_detail=type_detail,
        usage=usage,
        prudence=prudence,
    )
    result = CheckResult(candidate=candidate)

    records = load_place_records(paths)
    existing_ids = {str(rec.get("id")) for rec in records if rec.get("id")}
    existing_labels = {
        normalize_text(str(rec.get("label", ""))): (str(rec.get("id", "")), str(rec.get("label", "")))
        for rec in records
        if rec.get("label")
    }

    candidate_id = candidate["id"]
    if not PLACE_ID_RE.match(candidate_id):
        result.blockers.append(f"identifiant invalide: {candidate_id}")
    if candidate_id in existing_ids:
        result.blockers.append(f"identifiant deja utilise: {candidate_id}")

    normalized_label = normalize_text(label)
    if normalized_label in existing_labels:
        rec_id, _ = existing_labels[normalized_label]
        result.blockers.append(f"collision certaine de label: {label} deja present dans {rec_id}")
    else:
        for rec_id, rec_label in existing_labels.values():
            if is_near_text_match(label, rec_label):
                result.reserves.append(f"lieu proche a arbitrer: {label} ~ {rec_label} ({rec_id})")

    for alias in aliases:
        normalized_alias = normalize_text(alias)
        if normalized_alias in existing_labels:
            rec_id, rec_label = existing_labels[normalized_alias]
            result.blockers.append(
                f"alias deja present comme label canonique: {alias} dans {rec_id} ({rec_label})"
            )
        else:
            for rec_id, rec_label in existing_labels.values():
                if is_near_text_match(alias, rec_label):
                    result.reserves.append(f"alias proche d'un lieu a arbitrer: {alias} ~ {rec_label} ({rec_id})")

    canonical_sources = load_source_ids(paths.source_registry)
    add_source_diagnostics(result, sources=sources, canonical_sources=canonical_sources, format_re=SOURCE_ID_RE)

    place_types = load_place_types(paths.schema_yaml)
    type_is_valid = place_type in set(place_types)
    if not type_is_valid:
        result.blockers.append(f"type de lieu invalide: {place_type} (types autorises: {format_values(place_types)})")

    for diagnostic in _validate_candidate_shape(candidate, paths.schema_yaml):
        if not type_is_valid and (
            diagnostic == f"{place_type!r} is not one of {list(place_types)!r}"
            or diagnostic.startswith("type: ")
        ):
            continue
        result.blockers.append(f"schema invalide: {diagnostic}")

    if aliases:
        result.information.append(
            "alias fournis pour diagnostic uniquement: le schema PLACE ne les integre pas automatiquement"
        )
    result.information.append("cible d'ecriture probable: registers/places/*.md")
    result.information.append("lecture seule: aucune modification du registre PLACE")

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


def build_place_pr_summary(result: CheckResult):
    candidate = result.candidate
    if result.blockers:
        arbitrations = ["Corriger les bloquants avant ouverture de PR."]
    elif result.reserves:
        arbitrations = ["Arbitrer les reserves PLACE avant integration."]
    else:
        arbitrations = ["Validation humaine finale avant integration."]
    return build_pr_summary(
        result,
        subject=f"Ajout PLACE : {candidate['label']} ({candidate['id']})",
        scope=[
            "Flux M2 ajout unitaire.",
            "Famille documentaire : PLACE.",
            "Lecture seule : aucune modification du registre PLACE effectuee par le prototype.",
            "Entree candidate YAML produite pour revue humaine.",
        ],
        validations=[
            "Pre-validation PLACE executee localement.",
            "Sources Sxx verifiees contre data/registre.json.",
            "Schema PLACE evalue sur l'entree candidate.",
            "Collisions label, alias de saisie et identifiant evaluees.",
            "Proximite documentaire avec les lieux existants evaluee.",
        ],
        human_arbitrations=arbitrations,
        documentary_impact=[
            "Proposition de lieu documentaire PLACE.",
            "Aucun ajout effectif tant que la PR n'est pas relue et validee.",
        ],
        verification_commands=[
            "python3 tools/m2_add_place.py --help",
            "python3 -m unittest tools.test_m2_add_place",
            "python3 tools/validate_places.py",
        ],
    )


def write_place_pr_summary(result: CheckResult, paths: Paths) -> Path:
    filename = f"pr_summary_place_{slugify_filename(result.candidate['id'])}.md"
    return write_pr_summary(
        build_place_pr_summary(result),
        output_dir=paths.root / "exports" / "generated",
        filename=filename,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare localement une proposition d'ajout PLACE sans modifier le depot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Types PLACE autorises:\n" + "\n".join(f"  - {place_type}" for place_type in DEFAULT_PLACE_TYPES),
    )
    parser.add_argument("--label", required=True, help="Label canonique du lieu.")
    parser.add_argument(
        "--type",
        required=True,
        dest="place_type",
        help="Type PLACE canonique. Voir la liste ci-dessous.",
    )
    parser.add_argument("--sources", required=True, help="Sources Sxx separees par des virgules, par exemple S41,S74.")
    parser.add_argument("--aliases", help="Alias de saisie separes par des virgules, utilises pour le diagnostic.")
    parser.add_argument("--type-detail", help="Precision libre du type de lieu.")
    parser.add_argument("--usage", help="Usage documentaire attendu du lieu.")
    parser.add_argument("--prudence", help="Note de prudence documentaire.")
    parser.add_argument(
        "--pr-summary",
        action="store_true",
        help="Ecrit un resume de PR M2 dans exports/generated sans ouvrir de PR GitHub.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = Paths()
    result = evaluate_place_addition(
        label=args.label,
        place_type=args.place_type,
        sources=split_csv([args.sources]),
        aliases=split_csv([args.aliases] if args.aliases else None),
        type_detail=args.type_detail,
        usage=args.usage,
        prudence=args.prudence,
        paths=paths,
    )
    sys.stdout.write(render_result(result))
    if args.pr_summary:
        path = write_place_pr_summary(result, paths)
        sys.stdout.write(f"Resume PR genere : {path.relative_to(paths.root)}\n")
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
