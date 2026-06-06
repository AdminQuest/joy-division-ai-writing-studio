#!/usr/bin/env python3
"""Prototype CLI M2 pour preparer un ajout ORG.

L'outil ne modifie aucun fichier du depot. Il lit le registre canonique des
sources et le registre canonique ORG, puis imprime une proposition deterministe.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

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
except ImportError:  # execution directe: python3 tools/m2_add_org.py
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
ORG_ID_RE = re.compile(r"^ORG-\d{4}$")
SOURCE_ID_RE = re.compile(r"^S\d+$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKIDATA_RE = re.compile(r"^Q\d+$")
MUSICBRAINZ_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
VALID_CATEGORIES = ("group", "label", "institution", "venue_org", "crew", "media", "other")
VALID_CATEGORY_SET = set(VALID_CATEGORIES)
VALID_STATUSES = ("active", "dissolved", "dormant", "unknown")
VALID_STATUS_SET = set(VALID_STATUSES)
VALID_GATES = ("public", "private")
VALID_GATE_SET = set(VALID_GATES)
CURRENT_DRIFT_VERSION = "v1.0"


@dataclass(frozen=True)
class Paths:
    root: Path = REPO_ROOT
    source_registry: Path = REPO_ROOT / "data" / "registre.json"
    orgs_json: Path = REPO_ROOT / "registers" / "orgs" / "orgs.json"
    schema_json: Path = REPO_ROOT / "schemas" / "organization_canonical.schema.json"


def load_org_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def next_org_id(records: Sequence[dict]) -> str:
    numbers: list[int] = []
    for rec in records:
        org_id = str(rec.get("org_id", ""))
        if ORG_ID_RE.match(org_id):
            numbers.append(int(org_id.split("-")[1]))
    next_number = max(numbers, default=0) + 1
    return f"ORG-{next_number:04d}"


def build_candidate(
    *,
    org_id: str,
    name: str,
    category: str,
    country: str,
    jd_relation: str,
    sources: Sequence[str],
    last_verified: str,
    aliases: Sequence[str] = (),
    status: str = "unknown",
    gate: str = "private",
    subcategory: str | None = None,
    city: str | None = None,
    active_from: str | None = None,
    active_until: str | None = None,
    relation_period: str | None = None,
    relation_notes: str | None = None,
    wikidata: str | None = None,
    discogs: str | None = None,
    musicbrainz: str | None = None,
    provenance_from_pers: str | None = None,
    provenance_from_attribution: bool = False,
) -> dict:
    candidate = {
        "org_id": org_id,
        "canonical_name": name.strip(),
        "aliases": list(aliases),
        "category": category.strip(),
        "country": country.strip(),
        "status": status.strip(),
        "same_as": {
            "wikidata": wikidata.strip() if wikidata else None,
            "musicbrainz": musicbrainz.strip() if musicbrainz else None,
            "discogs": discogs.strip() if discogs else None,
        },
        "joy_division_relation": {
            "type": jd_relation.strip(),
            "period": relation_period.strip() if relation_period else None,
        },
        "sources": list(sources),
        "identity_frozen": True,
        "drift_sentinel": CURRENT_DRIFT_VERSION,
        "gate": gate.strip(),
        "last_verified": last_verified.strip(),
    }
    if relation_notes:
        candidate["joy_division_relation"]["notes"] = relation_notes.strip()
    if subcategory:
        candidate["subcategory"] = subcategory.strip()
    if city:
        candidate["city"] = city.strip()
    if active_from:
        candidate["active_from"] = active_from.strip()
    if active_until:
        value = active_until.strip()
        candidate["active_until"] = None if value.lower() == "null" else value
    provenance: dict[str, object] = {}
    if provenance_from_pers:
        provenance["from_pers"] = provenance_from_pers.strip()
    if provenance_from_attribution:
        provenance["from_attribution"] = True
    if provenance:
        candidate["provenance"] = provenance
    return candidate


def _validate_candidate_shape(candidate: dict, schema_path: Path) -> list[str]:
    diagnostics: list[str] = []
    required = (
        "org_id",
        "canonical_name",
        "aliases",
        "category",
        "country",
        "status",
        "same_as",
        "joy_division_relation",
        "sources",
        "identity_frozen",
        "drift_sentinel",
        "gate",
        "last_verified",
    )
    for key in required:
        if key not in candidate:
            diagnostics.append(f"Missing required field: {key}")

    org_id = str(candidate.get("org_id", ""))
    if not ORG_ID_RE.match(org_id):
        diagnostics.append(f"Invalid value for org_id: {org_id}")
    if not str(candidate.get("canonical_name", "")).strip():
        diagnostics.append("Field must be non-empty: canonical_name")
    if not isinstance(candidate.get("aliases"), list):
        diagnostics.append("Field must be a list: aliases")
    if candidate.get("category") not in VALID_CATEGORY_SET:
        diagnostics.append(f"Invalid value for category: {candidate.get('category')}")
    if candidate.get("status") not in VALID_STATUS_SET:
        diagnostics.append(f"Invalid value for status: {candidate.get('status')}")
    if candidate.get("gate") not in VALID_GATE_SET:
        diagnostics.append(f"Invalid value for gate: {candidate.get('gate')}")
    country = str(candidate.get("country", ""))
    if not COUNTRY_RE.match(country):
        diagnostics.append(f"Invalid value for country: {country}")
    sources = candidate.get("sources")
    if not isinstance(sources, list) or not sources:
        diagnostics.append("Field must be a non-empty list: sources")
    same_as = candidate.get("same_as")
    if not isinstance(same_as, dict):
        diagnostics.append("Field must be an object/dict: same_as")
    else:
        wikidata = same_as.get("wikidata")
        musicbrainz = same_as.get("musicbrainz")
        if wikidata and not WIKIDATA_RE.match(str(wikidata)):
            diagnostics.append(f"Invalid value for same_as.wikidata: {wikidata}")
        if musicbrainz and not MUSICBRAINZ_RE.match(str(musicbrainz)):
            diagnostics.append(f"Invalid value for same_as.musicbrainz: {musicbrainz}")
    relation = candidate.get("joy_division_relation")
    if not isinstance(relation, dict):
        diagnostics.append("Field must be an object/dict: joy_division_relation")
    elif not str(relation.get("type", "")).strip():
        diagnostics.append("Field must be non-empty: joy_division_relation.type")
    if candidate.get("identity_frozen") is not True:
        diagnostics.append("Invalid value for identity_frozen: expected true")
    drift_sentinel = str(candidate.get("drift_sentinel", ""))
    if drift_sentinel != CURRENT_DRIFT_VERSION:
        diagnostics.append(f"Invalid value for drift_sentinel: {drift_sentinel}")
    last_verified = str(candidate.get("last_verified", ""))
    if not DATE_RE.match(last_verified):
        diagnostics.append(f"Invalid value for last_verified: {last_verified}")

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

    return unique_preserving_order(diagnostics)


def evaluate_org_addition(
    *,
    name: str,
    category: str,
    country: str,
    jd_relation: str,
    sources: Sequence[str],
    last_verified: str,
    aliases: Sequence[str] = (),
    status: str = "unknown",
    gate: str = "private",
    subcategory: str | None = None,
    city: str | None = None,
    active_from: str | None = None,
    active_until: str | None = None,
    relation_period: str | None = None,
    relation_notes: str | None = None,
    wikidata: str | None = None,
    discogs: str | None = None,
    musicbrainz: str | None = None,
    provenance_from_pers: str | None = None,
    provenance_from_attribution: bool = False,
    paths: Paths | None = None,
) -> CheckResult:
    paths = paths or Paths()
    sources = unique_preserving_order(source.strip() for source in sources if source.strip())
    aliases = unique_preserving_order(alias.strip() for alias in aliases if alias.strip())
    records = load_org_records(paths.orgs_json)
    org_id = next_org_id(records)
    candidate = build_candidate(
        org_id=org_id,
        name=name,
        category=category,
        country=country,
        jd_relation=jd_relation,
        sources=sources,
        last_verified=last_verified,
        aliases=aliases,
        status=status,
        gate=gate,
        subcategory=subcategory,
        city=city,
        active_from=active_from,
        active_until=active_until,
        relation_period=relation_period,
        relation_notes=relation_notes,
        wikidata=wikidata,
        discogs=discogs,
        musicbrainz=musicbrainz,
        provenance_from_pers=provenance_from_pers,
        provenance_from_attribution=provenance_from_attribution,
    )
    result = CheckResult(candidate=candidate)

    existing_ids = {str(rec.get("org_id")) for rec in records if rec.get("org_id")}
    if org_id in existing_ids:
        result.blockers.append(f"identifiant deja utilise: {org_id}")
    if not ORG_ID_RE.match(org_id):
        result.blockers.append(f"identifiant invalide: {org_id}")
    result.information.append(f"prochain numero disponible detecte: {org_id}")
    result.information.append("cible d'ecriture probable: registers/orgs/orgs.json")
    result.information.append("lecture seule: aucune modification du registre ORG")

    existing_names = {
        normalize_text(str(rec.get("canonical_name", ""))): (
            str(rec.get("org_id", "")),
            str(rec.get("canonical_name", "")),
        )
        for rec in records
        if rec.get("canonical_name")
    }
    existing_aliases: dict[str, tuple[str, str]] = {}
    for rec in records:
        rec_id = str(rec.get("org_id", ""))
        for alias in rec.get("aliases") or []:
            existing_aliases[normalize_text(str(alias))] = (rec_id, str(alias))

    normalized_name = normalize_text(name)
    if normalized_name in existing_names:
        rec_id, _ = existing_names[normalized_name]
        result.blockers.append(f"collision certaine de nom: {name} deja present dans {rec_id}")
    if normalized_name in existing_aliases:
        rec_id, _ = existing_aliases[normalized_name]
        result.blockers.append(f"collision avec un alias existant: {name} dans {rec_id}")

    if normalized_name not in existing_names and normalized_name not in existing_aliases:
        for rec_id, rec_name in existing_names.values():
            if is_near_text_match(name, rec_name):
                result.reserves.append(f"organisation proche a arbitrer: {name} ~ {rec_name} ({rec_id})")
        for rec_id, alias in existing_aliases.values():
            if is_near_text_match(name, alias):
                result.reserves.append(f"nom proche d'un alias a arbitrer: {name} ~ {alias} ({rec_id})")

    for alias in aliases:
        normalized_alias = normalize_text(alias)
        if normalized_alias in existing_names:
            rec_id, rec_name = existing_names[normalized_alias]
            result.blockers.append(f"alias deja present comme nom canonique: {alias} dans {rec_id} ({rec_name})")
        if normalized_alias in existing_aliases:
            rec_id, _ = existing_aliases[normalized_alias]
            result.blockers.append(f"alias deja present: {alias} dans {rec_id}")
        if normalized_alias not in existing_names and normalized_alias not in existing_aliases:
            for rec_id, rec_name in existing_names.values():
                if is_near_text_match(alias, rec_name):
                    result.reserves.append(f"alias proche d'un nom a arbitrer: {alias} ~ {rec_name} ({rec_id})")
            for rec_id, existing_alias in existing_aliases.values():
                if is_near_text_match(alias, existing_alias):
                    result.reserves.append(
                        f"alias proche d'un alias existant a arbitrer: {alias} ~ {existing_alias} ({rec_id})"
                    )

    existing_wikidata = {}
    for rec in records:
        rec_id = str(rec.get("org_id", ""))
        same_as = rec.get("same_as") or {}
        if not isinstance(same_as, dict):
            continue
        existing = same_as.get("wikidata")
        if existing:
            existing_wikidata[str(existing)] = rec_id
    if wikidata and wikidata in existing_wikidata:
        result.blockers.append(f"wikidata deja utilise: {wikidata} dans {existing_wikidata[wikidata]}")

    canonical_sources = load_source_ids(paths.source_registry)
    add_source_diagnostics(result, sources=sources, canonical_sources=canonical_sources, format_re=SOURCE_ID_RE)

    category_is_valid = category in VALID_CATEGORY_SET
    country_is_valid = bool(country) and bool(COUNTRY_RE.match(country))
    status_is_valid = status in VALID_STATUS_SET
    gate_is_valid = gate in VALID_GATE_SET
    if not category_is_valid:
        result.blockers.append(f"categorie invalide: {category} (categories autorisees: {format_values(VALID_CATEGORIES)})")
    if country and not country_is_valid:
        result.blockers.append(f"pays invalide: {country} (format attendu: ISO alpha-2)")
    if not status_is_valid:
        result.blockers.append(f"statut invalide: {status} (statuts autorises: {format_values(VALID_STATUSES)})")
    if not gate_is_valid:
        result.blockers.append(f"gate invalide: {gate} (valeurs autorisees: {format_values(VALID_GATES)})")
    if not jd_relation.strip():
        result.blockers.append("relation Joy Division absente")
    if not last_verified.strip():
        result.blockers.append("last_verified absent")

    for diagnostic in _validate_candidate_shape(candidate, paths.schema_json):
        if not category_is_valid and (
            diagnostic == f"Invalid value for category: {category}" or diagnostic.startswith("category: ")
        ):
            continue
        if country and not country_is_valid and (
            diagnostic == f"Invalid value for country: {country}" or diagnostic.startswith("country: ")
        ):
            continue
        if not status_is_valid and (
            diagnostic == f"Invalid value for status: {status}" or diagnostic.startswith("status: ")
        ):
            continue
        if not gate_is_valid and (
            diagnostic == f"Invalid value for gate: {gate}" or diagnostic.startswith("gate: ")
        ):
            continue
        result.blockers.append(f"schema invalide: {diagnostic}")

    result.finalize()
    return result


def dump_candidate_json(candidate: dict) -> str:
    return json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=False)


def render_result(result: CheckResult) -> str:
    return render_m2_result(
        result,
        identifier=result.candidate["org_id"],
        candidate_language="json",
        rendered_candidate=dump_candidate_json(result.candidate),
    )


def build_org_pr_summary(result: CheckResult):
    candidate = result.candidate
    if result.blockers:
        arbitrations = ["Corriger les bloquants avant ouverture de PR."]
    elif result.reserves:
        arbitrations = ["Arbitrer les reserves ORG avant integration."]
    else:
        arbitrations = ["Validation humaine finale avant integration."]
    return build_pr_summary(
        result,
        subject=f"Ajout ORG : {candidate['canonical_name']} ({candidate['org_id']})",
        scope=[
            "Flux M2 ajout unitaire.",
            "Famille documentaire : ORG.",
            "Lecture seule : aucune modification du registre ORG effectuee par le prototype.",
            "Entree candidate JSON produite pour revue humaine.",
        ],
        validations=[
            "Pre-validation ORG executee localement.",
            "Sources Sxx verifiees contre data/registre.json.",
            "Schema ORG evalue sur l'entree candidate.",
            "Collisions nom, alias, identifiant et Wikidata evaluees.",
        ],
        human_arbitrations=arbitrations,
        documentary_impact=[
            "Proposition d'organisation canonique ORG.",
            "Aucun ajout effectif tant que la PR n'est pas relue et validee.",
        ],
        verification_commands=[
            "python3 tools/m2_add_org.py --help",
            "python3 -m unittest tools.test_m2_add_org",
            "python3 tools/validate_orgs.py",
        ],
    )


def write_org_pr_summary(result: CheckResult, paths: Paths) -> Path:
    name_slug = normalize_text(result.candidate["canonical_name"]).replace(" ", "-")
    filename = f"pr_summary_org_{result.candidate['org_id'].lower()}_{name_slug}.md"
    return write_pr_summary(
        build_org_pr_summary(result),
        output_dir=paths.root / "exports" / "generated",
        filename=filename,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare localement une proposition d'ajout ORG sans modifier le depot.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Categories autorisees:\n"
            + "\n".join(f"  - {category}" for category in VALID_CATEGORIES)
            + "\n\nStatuts autorises:\n"
            + "\n".join(f"  - {status}" for status in VALID_STATUSES)
            + "\n\nGate autorises:\n"
            + "\n".join(f"  - {gate}" for gate in VALID_GATES)
        ),
    )
    parser.add_argument("--name", required=True, help="Nom canonique de l'organisation.")
    parser.add_argument("--category", required=True, help="Categorie ORG canonique. Voir la liste ci-dessous.")
    parser.add_argument("--country", required=True, help="Code pays ISO alpha-2, par exemple GB.")
    parser.add_argument("--jd-relation", required=True, help="Type de relation documentee avec Joy Division.")
    parser.add_argument("--sources", required=True, help="Sources Sxx separees par des virgules, par exemple S41,S74.")
    parser.add_argument(
        "--last-verified",
        required=True,
        help="Date explicite de verification humaine au format YYYY-MM-DD. Aucune date dynamique n'est generee.",
    )
    parser.add_argument("--aliases", help="Alias separes par des virgules.")
    parser.add_argument("--status", default="unknown", help="Statut ORG. Par defaut: unknown.")
    parser.add_argument("--gate", default="private", help="Gate de visibilite. Par defaut: private.")
    parser.add_argument("--subcategory", help="Sous-categorie libre.")
    parser.add_argument("--city", help="Ville principale.")
    parser.add_argument("--active-from", help="Debut d'activite documente.")
    parser.add_argument("--active-until", help="Fin d'activite documentee, ou null.")
    parser.add_argument("--relation-period", help="Periode de relation avec Joy Division, ou null.")
    parser.add_argument("--relation-notes", help="Notes courtes sur la relation documentee.")
    parser.add_argument("--wikidata", help="Identifiant Wikidata Q... verifie.")
    parser.add_argument("--discogs", help="URL ou identifiant Discogs verifie.")
    parser.add_argument("--musicbrainz", help="UUID MusicBrainz verifie.")
    parser.add_argument("--provenance-from-pers", help="Identifiant PERS-* d'origine si hand-off documente.")
    parser.add_argument("--provenance-from-attribution", action="store_true", help="Marque provenance.from_attribution=true.")
    parser.add_argument(
        "--pr-summary",
        action="store_true",
        help="Ecrit un resume de PR M2 dans exports/generated sans ouvrir de PR GitHub.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = Paths()
    result = evaluate_org_addition(
        name=args.name,
        category=args.category,
        country=args.country,
        jd_relation=args.jd_relation,
        sources=split_csv([args.sources]),
        last_verified=args.last_verified,
        aliases=split_csv([args.aliases] if args.aliases else None),
        status=args.status,
        gate=args.gate,
        subcategory=args.subcategory,
        city=args.city,
        active_from=args.active_from,
        active_until=args.active_until,
        relation_period=args.relation_period,
        relation_notes=args.relation_notes,
        wikidata=args.wikidata,
        discogs=args.discogs,
        musicbrainz=args.musicbrainz,
        provenance_from_pers=args.provenance_from_pers,
        provenance_from_attribution=args.provenance_from_attribution,
        paths=paths,
    )
    sys.stdout.write(render_result(result))
    if args.pr_summary:
        path = write_org_pr_summary(result, paths)
        sys.stdout.write(f"Resume PR genere : {path.relative_to(paths.root)}\n")
    return exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
