#!/usr/bin/env python3
"""Tests du prototype CLI M2 d'ajout IMAGE."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_image


def person_block(person_id: str = "PERSON-kevin-cummins", name: str = "Kevin Cummins") -> str:
    return f"""
## {person_id} - {name}

```yaml
id: {person_id}
type_unite: person
name: {name}
categorie: industrie
role:
  - photographe
sources:
  - S01
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```
"""


def place_block(place_id: str = "PLACE-HULME", label: str = "Hulme") -> str:
    return f"""
# Lieux de test

```yaml
places:
  - id: {place_id}
    label: "{label}"
    type: quartier
    sources:
      - S01
```
"""


def existing_image(
    *,
    image_id: str = "IMAGE-S-0001",
    level: str = "session",
    name: str = "Existing Image Session",
    session_ref: str | None = None,
) -> dict:
    record = {
        "image_id": image_id,
        "level": level,
        "canonical_name": name,
        "photographer": "PERSON-kevin-cummins",
        "date": "1979-01-06",
        "date_precision": "day",
        "place": "PLACE-HULME",
        "context": "promo",
        "subjects": ["PERSON-ian-curtis"],
        "sources": ["S01"],
        "same_as": {"wikidata": None},
        "identity_frozen": True,
        "drift_sentinel": "v1.0",
        "gate": "public",
        "last_verified": "2026-06-01",
    }
    if level == "session":
        record["session_ref"] = None
    else:
        record["session_ref"] = session_ref or "IMAGE-S-0001"
        record["usage"] = ["consultation documentaire"]
        record["iconic"] = False
    return record


def write_minimal_repo(root: Path, image_records: list[dict] | None = None) -> m2_add_image.Paths:
    (root / "data").mkdir(parents=True)
    (root / "registers" / "images").mkdir(parents=True)
    (root / "registers" / "people").mkdir(parents=True)
    (root / "registers" / "places").mkdir(parents=True)
    (root / "schemas").mkdir(parents=True)
    (root / "exports" / "generated").mkdir(parents=True)

    (root / "data" / "registre.json").write_text(
        json.dumps([{"id": "S01"}, {"id": "S02"}], sort_keys=True),
        encoding="utf-8",
    )
    (root / "registers" / "images" / "images.json").write_text(
        json.dumps(image_records or [existing_image()], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (root / "registers" / "people" / "00_canonical_people.md").write_text(
        person_block() + person_block("PERSON-ian-curtis", "Ian Curtis"),
        encoding="utf-8",
    )
    (root / "registers" / "people" / "00_authors_canonical.md").write_text("", encoding="utf-8")
    (root / "registers" / "places" / "places.md").write_text(place_block(), encoding="utf-8")
    (root / "schemas" / "image_canonical.schema.json").write_text(
        (m2_add_image.REPO_ROOT / "schemas" / "image_canonical.schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    return m2_add_image.Paths(
        root=root,
        source_registry=root / "data" / "registre.json",
        images_json=root / "registers" / "images" / "images.json",
        schema_json=root / "schemas" / "image_canonical.schema.json",
        canonical_people=root / "registers" / "people" / "00_canonical_people.md",
        canonical_authors=root / "registers" / "people" / "00_authors_canonical.md",
        places_root=root / "registers" / "places",
    )


def run_case(paths: m2_add_image.Paths, **overrides) -> m2_add_image.CheckResult:
    params = {
        "level": "session",
        "name": "Prototype Image Session",
        "photographer": "PERSON-kevin-cummins",
        "sources": ["S01"],
        "last_verified": "2026-06-06",
        "date": "1979-02",
        "date_precision": "month",
        "subjects": ["PERSON-ian-curtis"],
        "place": "PLACE-HULME",
        "context": "promo",
        "paths": paths,
    }
    params.update(overrides)
    return m2_add_image.evaluate_image_addition(**params)


class TestM2AddImage(unittest.TestCase):
    def test_conform_session_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.candidate["image_id"], "IMAGE-S-0002")
        self.assertEqual(result.blockers, [])
        self.assertIn("lecture seule: aucune modification du registre IMAGE", result.information)

    def test_approximate_date_and_rights_uncertainty_produce_reserves(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, date="", date_precision="approximate", rights_uncertain=True)

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn("date ou periode approximative a confirmer: IMAGE-S-0002", result.reserves)
        self.assertIn(
            "droits image a arbitrer: ne pas publier ni reproduire sans validation humaine",
            result.reserves,
        )

    def test_image_without_session_ref_is_not_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, level="image")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("session_ref absent pour level=image", result.blockers)

    def test_unknown_source_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, sources=["S999"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source inconnue: S999", result.blockers)

    def test_identifier_collision_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, image_id="IMAGE-S-0001")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("identifiant deja utilise: IMAGE-S-0001", result.blockers)

    def test_near_title_collision_is_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(
                Path(tmp),
                image_records=[existing_image(name="Factory Records Portrait Session")],
            )
            result = run_case(paths, name="Factory Record Portrait Session")

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "image proche a arbitrer: Factory Record Portrait Session ~ "
            "Factory Records Portrait Session (IMAGE-S-0001)",
            result.reserves,
        )

    def test_individual_image_with_existing_session_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(
                paths,
                level="image",
                session_ref="IMAGE-S-0001",
                name="Prototype Individual Image",
                usage=["presse"],
                iconic=True,
            )

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.candidate["image_id"], "IMAGE-I-0001")
        self.assertEqual(result.candidate["session_ref"], "IMAGE-S-0001")

    def test_pr_summary_is_written_as_markdown(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)
            summary_path = m2_add_image.write_image_pr_summary(result, paths)
            markdown = summary_path.read_text(encoding="utf-8")

        self.assertEqual(summary_path.name, "pr_summary_image_image-s-0002_prototype-image-session.md")
        self.assertIn("# Resume de PR M2", markdown)
        self.assertIn("Ajout IMAGE : Prototype Image Session (IMAGE-S-0002)", markdown)
        self.assertIn("Famille documentaire : IMAGE.", markdown)

    def test_help_lists_allowed_values(self) -> None:
        help_text = m2_add_image.build_parser().format_help()

        self.assertIn("Levels autorises:", help_text)
        self.assertIn("  - session", help_text)
        self.assertIn("Contextes autorises:", help_text)
        self.assertIn("Precisions de date autorisees:", help_text)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_add_image.render_result(result_a), m2_add_image.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
