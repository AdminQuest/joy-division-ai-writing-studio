#!/usr/bin/env python3
"""Tests du prototype CLI M2 d'ajout ORG."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_org


def existing_org(
    name: str = "Existing Org",
    aliases: list[str] | None = None,
    wikidata: str | None = None,
) -> dict:
    return {
        "org_id": "ORG-0001",
        "canonical_name": name,
        "aliases": aliases or [],
        "category": "label",
        "country": "GB",
        "status": "unknown",
        "same_as": {"wikidata": wikidata, "musicbrainz": None, "discogs": None},
        "joy_division_relation": {"type": "contextual", "period": None},
        "sources": ["S01"],
        "identity_frozen": True,
        "drift_sentinel": "v1.0",
        "gate": "private",
        "last_verified": "2026-06-01",
    }


def write_minimal_repo(root: Path, org_records: list[dict] | None = None) -> m2_add_org.Paths:
    (root / "data").mkdir(parents=True)
    (root / "registers" / "orgs").mkdir(parents=True)

    (root / "data" / "registre.json").write_text(
        json.dumps([{"id": "S01"}, {"id": "S02"}], sort_keys=True),
        encoding="utf-8",
    )
    (root / "registers" / "orgs" / "orgs.json").write_text(
        json.dumps(org_records or [existing_org()], sort_keys=True),
        encoding="utf-8",
    )

    return m2_add_org.Paths(
        root=root,
        source_registry=root / "data" / "registre.json",
        orgs_json=root / "registers" / "orgs" / "orgs.json",
        schema_json=m2_add_org.REPO_ROOT / "schemas" / "organization_canonical.schema.json",
    )


def run_case(paths: m2_add_org.Paths, **overrides) -> m2_add_org.CheckResult:
    params = {
        "name": "New Org",
        "category": "label",
        "country": "GB",
        "jd_relation": "label_mate",
        "sources": ["S01"],
        "last_verified": "2026-06-01",
        "paths": paths,
    }
    params.update(overrides)
    return m2_add_org.evaluate_org_addition(**params)


class TestM2AddOrg(unittest.TestCase):
    def test_conform_case_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.candidate["org_id"], "ORG-0002")
        self.assertEqual(result.blockers, [])
        self.assertIn("prochain numero disponible detecte: ORG-0002", result.information)

    def test_unknown_source_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, sources=["S999"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source inconnue: S999", result.blockers)

    def test_invalid_category_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, category="publisher")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn(
            "categorie invalide: publisher (categories autorisees: group, label, institution, venue_org, crew, media, other)",
            result.blockers,
        )
        self.assertFalse(any(item.startswith("schema invalide: category:") for item in result.blockers))

    def test_invalid_country_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, country="GBR")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("pays invalide: GBR (format attendu: ISO alpha-2)", result.blockers)
        self.assertFalse(any(item.startswith("schema invalide: country:") for item in result.blockers))

    def test_collision_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp), org_records=[existing_org(name="Factory Records")])
            result = run_case(paths, name="Factory Records")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("collision certaine de nom: Factory Records deja present dans ORG-0001", result.blockers)

    def test_duplicate_wikidata_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp), org_records=[existing_org(wikidata="Q485898")])
            result = run_case(paths, wikidata="Q485898")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("wikidata deja utilise: Q485898 dans ORG-0001", result.blockers)

    def test_near_alias_collision_is_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp), org_records=[existing_org(name="Factory Records")])
            result = run_case(paths, name="Unrelated Org", aliases=["Factory Record"])

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "alias proche d'un nom a arbitrer: Factory Record ~ Factory Records (ORG-0001)",
            result.reserves,
        )

    def test_empty_relation_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, jd_relation="")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("relation Joy Division absente", result.blockers)

    def test_help_lists_allowed_values(self) -> None:
        help_text = m2_add_org.build_parser().format_help()

        self.assertIn("Categories autorisees:", help_text)
        self.assertIn("  - institution", help_text)
        self.assertIn("Statuts autorises:", help_text)
        self.assertIn("Gate autorises:", help_text)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_add_org.render_result(result_a), m2_add_org.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
