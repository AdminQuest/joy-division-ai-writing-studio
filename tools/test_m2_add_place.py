#!/usr/bin/env python3
"""Tests du prototype CLI M2 d'ajout PLACE."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_place


def place_block(
    *,
    place_id: str = "PLACE-EXISTING-PLACE",
    label: str = "Existing Place",
    place_type: str = "salle",
) -> str:
    return f"""
# Lieux de test

```yaml
places:
  - id: {place_id}
    label: "{label}"
    type: {place_type}
    sources:
      - S01
```
"""


def write_minimal_repo(root: Path, place_records: str | None = None) -> m2_add_place.Paths:
    (root / "data").mkdir(parents=True)
    (root / "registers" / "places").mkdir(parents=True)
    (root / "schemas").mkdir(parents=True)
    (root / "exports" / "generated").mkdir(parents=True)

    (root / "data" / "registre.json").write_text(
        json.dumps([{"id": "S01"}, {"id": "S02"}], sort_keys=True),
        encoding="utf-8",
    )
    (root / "registers" / "places" / "places.md").write_text(
        place_records if place_records is not None else place_block(),
        encoding="utf-8",
    )
    (root / "schemas" / "places.schema.yaml").write_text(
        (m2_add_place.REPO_ROOT / "schemas" / "places.schema.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    return m2_add_place.Paths(
        root=root,
        source_registry=root / "data" / "registre.json",
        places_root=root / "registers" / "places",
        schema_yaml=root / "schemas" / "places.schema.yaml",
    )


def run_case(paths: m2_add_place.Paths, **overrides) -> m2_add_place.CheckResult:
    params = {
        "label": "Prototype Venue",
        "place_type": "salle",
        "sources": ["S01"],
        "paths": paths,
    }
    params.update(overrides)
    return m2_add_place.evaluate_place_addition(**params)


class TestM2AddPlace(unittest.TestCase):
    def test_conform_case_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.candidate["id"], "PLACE-PROTOTYPE-VENUE")
        self.assertEqual(result.blockers, [])
        self.assertIn("lecture seule: aucune modification du registre PLACE", result.information)

    def test_unknown_source_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, sources=["S999"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source inconnue: S999", result.blockers)

    def test_invalid_source_format_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, sources=["S01-A001"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source invalide: S01-A001", result.blockers)

    def test_invalid_type_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, place_type="venue")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn(
            "type de lieu invalide: venue (types autorises: ville, quartier, habitat, studio, "
            "salle, commerce, education, sante, industrie, science, infrastructure, pouvoir, lieu_memoire)",
            result.blockers,
        )
        self.assertFalse(any(item.startswith("schema invalide: type:") for item in result.blockers))

    def test_identifier_and_label_collision_are_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(
                Path(tmp),
                place_records=place_block(place_id="PLACE-PROTOTYPE-VENUE", label="Prototype Venue"),
            )
            result = run_case(paths)

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("identifiant deja utilise: PLACE-PROTOTYPE-VENUE", result.blockers)
        self.assertIn(
            "collision certaine de label: Prototype Venue deja present dans PLACE-PROTOTYPE-VENUE",
            result.blockers,
        )

    def test_near_alias_collision_is_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(
                Path(tmp),
                place_records=place_block(place_id="PLACE-FACTORY-RECORDS", label="Factory Records"),
            )
            result = run_case(paths, aliases=["Factory Record"])

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "alias proche d'un lieu a arbitrer: Factory Record ~ Factory Records (PLACE-FACTORY-RECORDS)",
            result.reserves,
        )

    def test_pr_summary_is_written_as_markdown(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)
            summary_path = m2_add_place.write_place_pr_summary(result, paths)
            markdown = summary_path.read_text(encoding="utf-8")

        self.assertEqual(summary_path.name, "pr_summary_place_place-prototype-venue.md")
        self.assertIn("# Resume de PR M2", markdown)
        self.assertIn("Ajout PLACE : Prototype Venue (PLACE-PROTOTYPE-VENUE)", markdown)
        self.assertIn("Famille documentaire : PLACE.", markdown)

    def test_help_lists_allowed_types(self) -> None:
        help_text = m2_add_place.build_parser().format_help()

        self.assertIn("Types PLACE autorises:", help_text)
        self.assertIn("  - salle", help_text)
        self.assertIn("  - lieu_memoire", help_text)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_add_place.render_result(result_a), m2_add_place.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
