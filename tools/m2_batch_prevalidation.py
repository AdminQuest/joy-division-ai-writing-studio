#!/usr/bin/env python3
"""Orchestration batch M2 pour campagnes de pre-validation documentaire."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, Sequence

try:
    from tools import m2_add_image, m2_add_org, m2_add_person, m2_add_place
    from tools.m2_core import (
        BatchItemResult,
        CheckResult,
        PRSummary,
        build_batch_result,
        normalize_text,
        write_batch_summary,
        write_pr_summary,
    )
except ImportError:  # execution directe: python3 tools/m2_batch_prevalidation.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import m2_add_image
    import m2_add_org
    import m2_add_person
    import m2_add_place
    from m2_core import (
        BatchItemResult,
        CheckResult,
        PRSummary,
        build_batch_result,
        normalize_text,
        write_batch_summary,
        write_pr_summary,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class BatchPaths:
    root: Path = REPO_ROOT
    orgs_json_override: Path | None = None
    images_json_override: Path | None = None

    @property
    def output_dir(self) -> Path:
        return self.root / "exports" / "generated"

    @property
    def person_paths(self) -> m2_add_person.Paths:
        return m2_add_person.Paths(
            root=self.root,
            source_registry=self.root / "data" / "registre.json",
            canonical_people=self.root / "registers" / "people" / "00_canonical_people.md",
            canonical_authors=self.root / "registers" / "people" / "00_authors_canonical.md",
            generated_people=self.root / "exports" / "generated" / "people.json",
        )

    @property
    def org_paths(self) -> m2_add_org.Paths:
        return m2_add_org.Paths(
            root=self.root,
            source_registry=self.root / "data" / "registre.json",
            orgs_json=self.orgs_json_override or self.root / "registers" / "orgs" / "orgs.json",
            schema_json=self.root / "schemas" / "organization_canonical.schema.json",
        )

    @property
    def place_paths(self) -> m2_add_place.Paths:
        return m2_add_place.Paths(
            root=self.root,
            source_registry=self.root / "data" / "registre.json",
            places_root=self.root / "registers" / "places",
            schema_yaml=self.root / "schemas" / "places.schema.yaml",
        )

    @property
    def image_paths(self) -> m2_add_image.Paths:
        return m2_add_image.Paths(
            root=self.root,
            source_registry=self.root / "data" / "registre.json",
            images_json=self.images_json_override or self.root / "registers" / "images" / "images.json",
            schema_json=self.root / "schemas" / "image_canonical.schema.json",
            canonical_people=self.root / "registers" / "people" / "00_canonical_people.md",
            canonical_authors=self.root / "registers" / "people" / "00_authors_canonical.md",
            places_root=self.root / "registers" / "places",
        )

    def with_orgs_json(self, path: Path) -> BatchPaths:
        return BatchPaths(root=self.root, orgs_json_override=path, images_json_override=self.images_json_override)

    def with_images_json(self, path: Path) -> BatchPaths:
        return BatchPaths(root=self.root, orgs_json_override=self.orgs_json_override, images_json_override=path)


@dataclass(frozen=True)
class BatchAdapter:
    family: str
    evaluate: Callable[[dict, BatchPaths], CheckResult]
    label: Callable[[CheckResult], str]
    build_pr_summary: Callable[[CheckResult], PRSummary]
    pr_summary_filename: Callable[[CheckResult], str]


def as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "oui"}


def as_int_or_none(value: object) -> int | None:
    if value is None or str(value).strip() == "":
        return None
    return int(str(value).strip())


def evaluate_person_item(item: dict, paths: BatchPaths) -> CheckResult:
    return m2_add_person.evaluate_person_addition(
        name=str(item["name"]),
        category=str(item["category"]),
        roles=as_list(item.get("roles", item.get("role"))),
        sources=as_list(item.get("sources")),
        aliases=as_list(item.get("aliases")),
        same_as=as_list(item.get("same_as")),
        note=item.get("note"),
        origin=item.get("origin"),
        category_arbitration=as_bool(item.get("category_arbitration")),
        identity_arbitration=as_bool(item.get("identity_arbitration")),
        paths=paths.person_paths,
    )


def evaluate_org_item(item: dict, paths: BatchPaths) -> CheckResult:
    return m2_add_org.evaluate_org_addition(
        name=str(item["name"]),
        category=str(item["category"]),
        country=str(item["country"]),
        jd_relation=str(item["jd_relation"]),
        sources=as_list(item.get("sources")),
        last_verified=str(item["last_verified"]),
        aliases=as_list(item.get("aliases")),
        status=str(item.get("status", "unknown")),
        gate=str(item.get("gate", "private")),
        subcategory=item.get("subcategory"),
        city=item.get("city"),
        active_from=item.get("active_from"),
        active_until=item.get("active_until"),
        relation_period=item.get("relation_period"),
        relation_notes=item.get("relation_notes"),
        wikidata=item.get("wikidata"),
        discogs=item.get("discogs"),
        musicbrainz=item.get("musicbrainz"),
        provenance_from_pers=item.get("provenance_from_pers"),
        provenance_from_attribution=as_bool(item.get("provenance_from_attribution")),
        paths=paths.org_paths,
    )


def evaluate_place_item(item: dict, paths: BatchPaths) -> CheckResult:
    return m2_add_place.evaluate_place_addition(
        label=str(item["label"]),
        place_type=str(item["type"]),
        sources=as_list(item.get("sources")),
        aliases=as_list(item.get("aliases")),
        type_detail=item.get("type_detail"),
        usage=item.get("usage"),
        prudence=item.get("prudence"),
        paths=paths.place_paths,
    )


def evaluate_image_item(item: dict, paths: BatchPaths) -> CheckResult:
    return m2_add_image.evaluate_image_addition(
        level=str(item["level"]),
        name=str(item["name"]),
        photographer=str(item["photographer"]),
        sources=as_list(item.get("sources")),
        last_verified=str(item["last_verified"]),
        date=str(item.get("date", "")),
        date_precision=str(item.get("date_precision", "approximate")),
        subjects=as_list(item.get("subjects")),
        session_ref=item.get("session_ref"),
        place=item.get("place"),
        event_ref=item.get("event_ref"),
        context=str(item.get("context", "other")),
        output_count=as_int_or_none(item.get("output_count")),
        usage=as_list(item.get("usage")),
        iconic=as_bool(item.get("iconic")),
        notes=item.get("notes"),
        gate=str(item.get("gate", "private")),
        wikidata=item.get("wikidata"),
        image_id=item.get("image_id"),
        rights_uncertain=as_bool(item.get("rights_uncertain")),
        attribution_uncertain=as_bool(item.get("attribution_uncertain")),
        paths=paths.image_paths,
    )


def person_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['name']} ({candidate['id']})"


def org_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['canonical_name']} ({candidate['org_id']})"


def place_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['label']} ({candidate['id']})"


def image_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['canonical_name']} ({candidate['image_id']})"


def person_pr_summary_filename(result: CheckResult) -> str:
    return f"pr_summary_person_{m2_add_person.slugify(result.candidate['id'])}.md"


def org_pr_summary_filename(result: CheckResult) -> str:
    name_slug = normalize_text(result.candidate["canonical_name"]).replace(" ", "-")
    return f"pr_summary_org_{result.candidate['org_id'].lower()}_{name_slug}.md"


def place_pr_summary_filename(result: CheckResult) -> str:
    return f"pr_summary_place_{m2_add_place.slugify_filename(result.candidate['id'])}.md"


def image_pr_summary_filename(result: CheckResult) -> str:
    name_slug = normalize_text(result.candidate["canonical_name"]).replace(" ", "-")
    return f"pr_summary_image_{result.candidate['image_id'].lower()}_{name_slug}.md"


ADAPTERS = {
    "person": BatchAdapter(
        "PERSON",
        evaluate_person_item,
        person_label,
        m2_add_person.build_person_pr_summary,
        person_pr_summary_filename,
    ),
    "org": BatchAdapter(
        "ORG",
        evaluate_org_item,
        org_label,
        m2_add_org.build_org_pr_summary,
        org_pr_summary_filename,
    ),
    "place": BatchAdapter(
        "PLACE",
        evaluate_place_item,
        place_label,
        m2_add_place.build_place_pr_summary,
        place_pr_summary_filename,
    ),
    "image": BatchAdapter(
        "IMAGE",
        evaluate_image_item,
        image_label,
        m2_add_image.build_image_pr_summary,
        image_pr_summary_filename,
    ),
}


def load_campaign(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Le fichier batch doit contenir un objet JSON.")
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Le champ items doit contenir une liste.")
    return payload


def report_filename(campaign: str) -> str:
    slug = normalize_text(campaign).replace(" ", "-") or "campagne-m2"
    return f"batch_summary_{slug}.md"


def unique_filename(filename: str, *, index: int, used_filenames: set[str]) -> str:
    if filename not in used_filenames:
        used_filenames.add(filename)
        return filename
    path = Path(filename)
    unique = f"{path.stem}_item-{index}{path.suffix}"
    used_filenames.add(unique)
    return unique


def write_item_pr_summary(
    adapter: BatchAdapter,
    result: CheckResult,
    *,
    paths: BatchPaths,
    index: int,
    used_filenames: set[str],
) -> Path:
    filename = unique_filename(adapter.pr_summary_filename(result), index=index, used_filenames=used_filenames)
    return write_pr_summary(adapter.build_pr_summary(result), output_dir=paths.output_dir, filename=filename)


def run_campaign(
    payload: dict,
    *,
    paths: BatchPaths | None = None,
    write_pr_summaries: bool = True,
) -> tuple[Path, int]:
    paths = paths or BatchPaths()
    campaign = str(payload.get("campaign") or payload.get("name") or "campagne-m2")
    item_results: list[BatchItemResult] = []
    base_org_records: list[dict] | None = None
    reserved_org_records: list[dict] = []
    base_image_records: list[dict] | None = None
    reserved_image_records: list[dict] = []
    seen_person_ids: dict[str, str] = {}
    seen_place_ids: dict[str, str] = {}
    used_pr_filenames: set[str] = set()

    with TemporaryDirectory() as tmp:
        orgs_json = Path(tmp) / "orgs.json"
        images_json = Path(tmp) / "images.json"
        for index, item in enumerate(payload.get("items", []), start=1):
            if not isinstance(item, dict):
                result = CheckResult(candidate={"raw": item})
                result.blockers.append("item batch invalide: objet JSON attendu")
                result.finalize()
                item_results.append(BatchItemResult(index, "UNKNOWN", f"item-{index}", result))
                continue

            family_key = str(item.get("family", item.get("type", ""))).strip().lower()
            adapter = ADAPTERS.get(family_key)
            if adapter is None:
                result = CheckResult(candidate=item)
                result.blockers.append(f"famille batch inconnue: {family_key or 'absente'}")
                result.finalize()
                item_results.append(
                    BatchItemResult(index, "UNKNOWN", str(item.get("name", f"item-{index}")), result)
                )
                continue

            adapter_paths = paths
            if family_key == "org":
                if base_org_records is None:
                    base_org_records = m2_add_org.load_org_records(paths.org_paths.orgs_json)
                orgs_json.write_text(
                    json.dumps([*base_org_records, *reserved_org_records], sort_keys=True),
                    encoding="utf-8",
                )
                adapter_paths = paths.with_orgs_json(orgs_json)
            if family_key == "image":
                if base_image_records is None:
                    base_image_records = m2_add_image.load_image_records(paths.image_paths.images_json)
                images_json.write_text(
                    json.dumps([*base_image_records, *reserved_image_records], sort_keys=True),
                    encoding="utf-8",
                )
                adapter_paths = paths.with_images_json(images_json)

            try:
                result = adapter.evaluate(item, adapter_paths)
            except (KeyError, ValueError) as exc:
                result = CheckResult(candidate=item)
                if isinstance(exc, KeyError):
                    result.blockers.append(f"item batch invalide: champ requis absent: {exc.args[0]}")
                else:
                    result.blockers.append(f"item batch invalide: {exc}")
                result.finalize()
                item_results.append(
                    BatchItemResult(index, adapter.family, str(item.get("name", f"item-{index}")), result)
                )
                continue

            if family_key == "org" and result.candidate.get("org_id"):
                reserved_org_records.append(result.candidate)
            if family_key == "image" and result.candidate.get("image_id") and not result.blockers:
                reserved_image_records.append(result.candidate)
            if family_key == "person" and result.candidate.get("id"):
                person_id = str(result.candidate["id"])
                if person_id in seen_person_ids:
                    result.blockers.append(
                        f"collision interne batch PERSON: {person_id} deja propose pour {seen_person_ids[person_id]}"
                    )
                    result.finalize()
                else:
                    seen_person_ids[person_id] = adapter.label(result)
            if family_key == "place" and result.candidate.get("id"):
                place_id = str(result.candidate["id"])
                if place_id in seen_place_ids:
                    result.blockers.append(
                        f"collision interne batch PLACE: {place_id} deja propose pour {seen_place_ids[place_id]}"
                    )
                    result.finalize()
                else:
                    seen_place_ids[place_id] = adapter.label(result)

            pr_summary_path: Path | None = None
            if write_pr_summaries:
                pr_summary_path = write_item_pr_summary(
                    adapter,
                    result,
                    paths=paths,
                    index=index,
                    used_filenames=used_pr_filenames,
                )
            item_results.append(
                BatchItemResult(
                    index=index,
                    family=adapter.family,
                    label=adapter.label(result),
                    result=result,
                    pr_summary_path=str(pr_summary_path.relative_to(paths.root)) if pr_summary_path else None,
                )
            )

    batch = build_batch_result(campaign=campaign, items=item_results)
    report_path = write_batch_summary(batch, output_dir=paths.output_dir, filename=report_filename(campaign))
    return report_path, batch.refused_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute une campagne M2 de pre-validation PERSON/ORG/PLACE/IMAGE et produit un rapport consolide.",
    )
    parser.add_argument("input", help="Fichier JSON de campagne.")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Racine du depot a utiliser. Par defaut: depot courant.")
    parser.add_argument(
        "--no-pr-summaries",
        action="store_true",
        help="Ne genere pas les resumes PR individuels des objets de la campagne.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = BatchPaths(root=Path(args.root).resolve())
    report_path, refused_count = run_campaign(
        load_campaign(Path(args.input)),
        paths=paths,
        write_pr_summaries=not args.no_pr_summaries,
    )
    sys.stdout.write(f"Rapport batch genere : {report_path.relative_to(paths.root)}\n")
    return 1 if refused_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
