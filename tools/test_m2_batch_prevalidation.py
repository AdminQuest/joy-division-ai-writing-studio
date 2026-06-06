#!/usr/bin/env python3
"""Tests de l'orchestration batch M2."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_image, m2_add_org, m2_add_place, m2_batch_prevalidation
from tools.test_m2_add_image import existing_image, person_block as image_person_block, place_block as image_place_block
from tools.test_m2_add_org import existing_org
from tools.test_m2_add_place import place_block
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
    (root / "registers" / "people" / "00_canonical_people.md").write_text(
        image_person_block() + image_person_block("PERSON-ian-curtis", "Ian Curtis"),
        encoding="utf-8",
    )
    (root / "registers" / "places").mkdir(parents=True, exist_ok=True)
    (root / "registers" / "places" / "places.md").write_text(
        place_block() + image_place_block(),
        encoding="utf-8",
    )
    (root / "schemas" / "places.schema.yaml").write_text(
        (m2_add_place.REPO_ROOT / "schemas" / "places.schema.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / "registers" / "images").mkdir(parents=True, exist_ok=True)
    (root / "registers" / "images" / "images.json").write_text(
        json.dumps([existing_image()], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (root / "schemas" / "image_canonical.schema.json").write_text(
        (m2_add_image.REPO_ROOT / "schemas" / "image_canonical.schema.json").read_text(encoding="utf-8"),
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

    def test_mixed_campaign_supports_person_org_and_place(self) -> None:
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
                        {
                            "family": "place",
                            "label": "Mixed Venue",
                            "type": "salle",
                            "sources": ["S01"],
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            person_pr = Path(tmp) / "exports" / "generated" / "pr_summary_person_person-mixed-person.md"
            org_pr = Path(tmp) / "exports" / "generated" / "pr_summary_org_org-0002_mixed-org.md"
            place_pr = Path(tmp) / "exports" / "generated" / "pr_summary_place_place-mixed-venue.md"
            person_pr_exists = person_pr.exists()
            org_pr_exists = org_pr.exists()
            place_pr_exists = place_pr.exists()

        self.assertEqual(refused_count, 0)
        self.assertTrue(person_pr_exists)
        self.assertTrue(org_pr_exists)
        self.assertTrue(place_pr_exists)
        self.assertIn("- objets: 3", markdown)
        self.assertIn("- pre-validations: 2", markdown)
        self.assertIn("- pre-validations avec reserve: 1", markdown)
        self.assertIn("PERSON - Mixed Person (PERSON-mixed-person)", markdown)
        self.assertIn("ORG - Mixed Org (ORG-0002)", markdown)
        self.assertIn("PLACE - Mixed Venue (PLACE-MIXED-VENUE)", markdown)

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

    def test_duplicate_place_candidate_is_blocking_and_keeps_unique_summaries(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "duplicate-place",
                    "items": [
                        {
                            "family": "place",
                            "label": "Duplicate Place",
                            "type": "salle",
                            "sources": ["S01"],
                        },
                        {
                            "family": "place",
                            "label": "Duplicate Place",
                            "type": "salle",
                            "sources": ["S01"],
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            first_pr = Path(tmp) / "exports" / "generated" / "pr_summary_place_place-duplicate-place.md"
            second_pr = (
                Path(tmp)
                / "exports"
                / "generated"
                / "pr_summary_place_place-duplicate-place_item-2.md"
            )
            first_pr_exists = first_pr.exists()
            second_pr_exists = second_pr.exists()

        self.assertEqual(refused_count, 1)
        self.assertTrue(first_pr_exists)
        self.assertTrue(second_pr_exists)
        self.assertIn("- refus: 1", markdown)
        self.assertIn("collision interne batch PLACE: PLACE-DUPLICATE-PLACE", markdown)

    def test_image_items_are_reserved_across_batch_items(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_batch_repo(Path(tmp))
            report_path, refused_count = m2_batch_prevalidation.run_campaign(
                {
                    "campaign": "two-images",
                    "items": [
                        {
                            "family": "image",
                            "level": "session",
                            "name": "First Batch Image Session",
                            "photographer": "PERSON-kevin-cummins",
                            "date": "1979-02",
                            "date_precision": "month",
                            "context": "promo",
                            "subjects": ["PERSON-ian-curtis"],
                            "place": "PLACE-HULME",
                            "sources": ["S01"],
                            "last_verified": "2026-06-06",
                        },
                        {
                            "family": "image",
                            "level": "session",
                            "name": "Second Batch Image Session",
                            "photographer": "PERSON-kevin-cummins",
                            "date": "1979-03",
                            "date_precision": "month",
                            "context": "promo",
                            "subjects": ["PERSON-ian-curtis"],
                            "place": "PLACE-HULME",
                            "sources": ["S01"],
                            "last_verified": "2026-06-06",
                        },
                    ],
                },
                paths=paths,
            )
            markdown = report_path.read_text(encoding="utf-8")
            first_pr = (
                Path(tmp)
                / "exports"
                / "generated"
                / "pr_summary_image_image-s-0002_first-batch-image-session.md"
            )
            second_pr = (
                Path(tmp)
                / "exports"
                / "generated"
                / "pr_summary_image_image-s-0003_second-batch-image-session.md"
            )
            first_pr_exists = first_pr.exists()
            second_pr_exists = second_pr.exists()

        self.assertEqual(refused_count, 0)
        self.assertTrue(first_pr_exists)
        self.assertTrue(second_pr_exists)
        self.assertIn("IMAGE - First Batch Image Session (IMAGE-S-0002)", markdown)
        self.assertIn("IMAGE - Second Batch Image Session (IMAGE-S-0003)", markdown)


if __name__ == "__main__":
    unittest.main()
