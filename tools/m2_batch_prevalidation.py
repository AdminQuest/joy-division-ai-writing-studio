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
    from tools import m2_add_org, m2_add_person
    from tools.m2_core import (
        BatchItemResult,
        CheckResult,
        build_batch_result,
        normalize_text,
        write_batch_summary,
    )
except ImportError:  # execution directe: python3 tools/m2_batch_prevalidation.py
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import m2_add_org
    import m2_add_person
    from m2_core import (
        BatchItemResult,
        CheckResult,
        build_batch_result,
        normalize_text,
        write_batch_summary,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class BatchPaths:
    root: Path = REPO_ROOT
    orgs_json_override: Path | None = None

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

    def with_orgs_json(self, path: Path) -> BatchPaths:
        return BatchPaths(root=self.root, orgs_json_override=path)


@dataclass(frozen=True)
class BatchAdapter:
    family: str
    evaluate: Callable[[dict, BatchPaths], CheckResult]
    label: Callable[[CheckResult], str]
    write_pr_summary: Callable[[CheckResult, BatchPaths], Path]


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


def person_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['name']} ({candidate['id']})"


def org_label(result: CheckResult) -> str:
    candidate = result.candidate
    return f"{candidate['canonical_name']} ({candidate['org_id']})"


def write_person_pr_summary(result: CheckResult, paths: BatchPaths) -> Path:
    return m2_add_person.write_person_pr_summary(result, paths.person_paths)


def write_org_pr_summary(result: CheckResult, paths: BatchPaths) -> Path:
    return m2_add_org.write_org_pr_summary(result, paths.org_paths)


ADAPTERS = {
    "person": BatchAdapter("PERSON", evaluate_person_item, person_label, write_person_pr_summary),
    "org": BatchAdapter("ORG", evaluate_org_item, org_label, write_org_pr_summary),
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

    with TemporaryDirectory() as tmp:
        orgs_json = Path(tmp) / "orgs.json"
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

            try:
                result = adapter.evaluate(item, adapter_paths)
            except KeyError as exc:
                result = CheckResult(candidate=item)
                result.blockers.append(f"item batch invalide: champ requis absent: {exc.args[0]}")
                result.finalize()
                item_results.append(
                    BatchItemResult(index, adapter.family, str(item.get("name", f"item-{index}")), result)
                )
                continue

            if family_key == "org" and result.candidate.get("org_id"):
                reserved_org_records.append(result.candidate)

            pr_summary_path: Path | None = None
            if write_pr_summaries:
                pr_summary_path = adapter.write_pr_summary(result, adapter_paths)
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
        description="Execute une campagne M2 de pre-validation PERSON/ORG et produit un rapport consolide.",
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
