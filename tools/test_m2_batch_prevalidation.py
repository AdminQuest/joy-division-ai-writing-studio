#!/usr/bin/env python3
"""Tests de l'orchestration batch M2."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_org, m2_batch_prevalidation
from tools.test_m2_add_org import existing_org
from tools.test_m2_add_person import write_minimal_repo as write_person_repo


def write_batch_repo(root: Path, *, org_records: list[dict] | None = None) -> m2_batch_prevalidation.BatchPaths:
    write_person_repo(root)
    (root / "registers" / "orgs").mkdir(parents=True, exist_ok=True)
    (root / "registers" / "orgs" / "orgs.json").write_text(
        json.dumps(org_records or [existing_org()], sort_keys=True),
        encoding="utf-8",
    )
    (root / "schemas").mkdir(parents=True, exist_ok=True)
    (root / "schemas" / "organization_canonical.schema.json").write_text(
        (m2_add_org.REPO_ROOT / "schemas" / "organization_canonical.schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return m2_batch_prevalidation.BatchPaths(root=root)


class TestM2BatchPrevalidation(unittest.TestCase):
    def test_empty_campaign_renders_zero_statistics(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {"campaign": "empty", "items": []},
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")

        self.assertEqual(refused_count, 0)
        self.assertIn("- objets: 0", markdown)
        self.assertIn("- pre-validations: 0", markdown)
        self.assertIn("- aucun", markdown)

    def test_success_campaign_writes_report_and_pr_summary(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "success",
                    "items": [
                        {
                            "family": "person",
                            "name": "Batch Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S01"],
                        }
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            pr_path = Path(tmp) / "exports" / "generated" / "pr_summary_person_person-batch-person.md"
            pr_exists = pr_path.exists()

        self.assertEqual(refused_count, 0)
        self.assertTrue(pr_exists)
        self.assertIn("- pre-validations: 1", markdown)
        self.assertIn("PERSON - Batch Person (PERSON-batch-person)", markdown)

    def test_campaign_with_reserve_counts_reserves(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "reserve",
                    "items": [
                        {
                            "family": "person",
                            "name": "Reserved Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S01"],
                            "identity_arbitration": True,
                        }
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")

        self.assertEqual(refused_count, 0)
        self.assertIn("- pre-validations avec reserve: 1", markdown)
        self.assertIn("- reserves: 1", markdown)
        self.assertIn("identite a arbitrer: rattachement ou homonymie a confirmer", markdown)

    def test_campaign_with_refusal_counts_blockers(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "refus",
                    "items": [
                        {
                            "family": "person",
                            "name": "Blocked Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S999"],
                        }
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")

        self.assertEqual(refused_count, 1)
        self.assertIn("- refus: 1", markdown)
        self.assertIn("- bloquants: 1", markdown)
        self.assertIn("source inconnue: S999", markdown)

    def test_mixed_campaign_supports_person_and_org(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp), org_records=[existing_org(name="Factory Records")])
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "mixed",
                    "items": [
                        {
                            "family": "person",
                            "name": "Mixed Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S01"],
                        },
                        {
                            "family": "org",
                            "name": "Mixed Org",
                            "category": "label",
                            "country": "GB",
                            "jd_relation": "label_mate",
                            "sources": ["S01"],
                            "last_verified": "2026-06-01",
                            "aliases": ["Factory Record"],
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            person_pr = Path(tmp) / "exports" / "generated" / "pr_summary_person_person-mixed-person.md"
            org_pr = Path(tmp) / "exports" / "generated" / "pr_summary_org_org-0002_mixed-org.md"
            person_pr_exists = person_pr.exists()
            org_pr_exists = org_pr.exists()

        self.assertEqual(refused_count, 0)
        self.assertTrue(person_pr_exists)
        self.assertTrue(org_pr_exists)
        self.assertIn("- objets: 2", markdown)
        self.assertIn("- pre-validations: 1", markdown)
        self.assertIn("- pre-validations avec reserve: 1", markdown)
        self.assertIn("PERSON - Mixed Person (PERSON-mixed-person)", markdown)
        self.assertIn("ORG - Mixed Org (ORG-0002)", markdown)

    def test_org_ids_are_reserved_across_batch_items(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp), org_records=[existing_org(name="Factory Records")])
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "two-orgs",
                    "items": [
                        {
                            "family": "org",
                            "name": "First Batch Org",
                            "category": "label",
                            "country": "GB",
                            "jd_relation": "label_mate",
                            "sources": ["S01"],
                            "last_verified": "2026-06-01",
                        },
                        {
                            "family": "org",
                            "name": "Second Batch Org",
                            "category": "label",
                            "country": "GB",
                            "jd_relation": "label_mate",
                            "sources": ["S01"],
                            "last_verified": "2026-06-01",
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            first_pr = Path(tmp) / "exports" / "generated" / "pr_summary_org_org-0002_first-batch-org.md"
            second_pr = Path(tmp) / "exports" / "generated" / "pr_summary_org_org-0003_second-batch-org.md"
            first_pr_exists = first_pr.exists()
            second_pr_exists = second_pr.exists()

        self.assertEqual(refused_count, 0)
        self.assertTrue(first_pr_exists)
        self.assertTrue(second_pr_exists)
        self.assertIn("ORG - First Batch Org (ORG-0002)", markdown)
        self.assertIn("ORG - Second Batch Org (ORG-0003)", markdown)

    def test_duplicate_person_candidate_is_blocking_and_keeps_unique_summaries(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "duplicate-person",
                    "items": [
                        {
                            "family": "person",
                            "name": "Duplicate Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S01"],
                        },
                        {
                            "family": "person",
                            "name": "Duplicate Person",
                            "category": "industrie",
                            "roles": ["producteur"],
                            "sources": ["S01"],
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            first_pr = Path(tmp) / "exports" / "generated" / "pr_summary_person_person-duplicate-person.md"
            second_pr = (
                Path(tmp)
                / "exports"
                / "generated"
                / "pr_summary_person_person-duplicate-person_item-2.md"
            )
            first_pr_exists = first_pr.exists()
            second_pr_exists = second_pr.exists()

        self.assertEqual(refused_count, 1)
        self.assertTrue(first_pr_exists)
        self.assertTrue(second_pr_exists)
        self.assertIn("- refus: 1", markdown)
        self.assertIn("collision interne batch PERSON: PERSON-duplicate-person", markdown)


if __name__ == "__main__":
    unittest.main()
