#!/usr/bin/env python3
"""Tests du prototype CLI M2 d'ajout PERSON."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_person


def write_minimal_repo(root: Path, canonical_person: str | None = None) -> m2_add_person.Paths:
    (root / "data").mkdir(parents=True)
    (root / "registers" / "people").mkdir(parents=True)
    (root / "exports" / "generated").mkdir(parents=True)

    (root / "data" / "registre.json").write_text(
        json.dumps([{"id": "S01"}, {"id": "S02"}], sort_keys=True),
        encoding="utf-8",
    )
    if canonical_person is None:
        canonical_person = ""
    (root / "registers" / "people" / "00_canonical_people.md").write_text(
        canonical_person,
        encoding="utf-8",
    )
    (root / "registers" / "people" / "00_authors_canonical.md").write_text(
        "",
        encoding="utf-8",
    )
    (root / "exports" / "generated" / "people.json").write_text(
        json.dumps([{"id": "PERS-S01-001", "data": {"id": "PERS-S01-001"}}], sort_keys=True),
        encoding="utf-8",
    )

    return m2_add_person.Paths(
        root=root,
        source_registry=root / "data" / "registre.json",
        canonical_people=root / "registers" / "people" / "00_canonical_people.md",
        canonical_authors=root / "registers" / "people" / "00_authors_canonical.md",
        generated_people=root / "exports" / "generated" / "people.json",
    )


def run_case(paths: m2_add_person.Paths, **overrides) -> m2_add_person.CheckResult:
    params = {
        "name": "Test Person",
        "category": "industrie",
        "roles": ["producteur"],
        "sources": ["S01"],
        "paths": paths,
    }
    params.update(overrides)
    return m2_add_person.evaluate_person_addition(**params)


class TestM2AddPerson(unittest.TestCase):
    def test_conform_case_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.candidate["id"], "PERSON-test-person")
        self.assertEqual(result.blockers, [])

    def test_unknown_source_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, sources=["S999"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source inconnue: S999", result.blockers)

    def test_invalid_category_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, category="manager")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn(
            "categorie invalide: manager (categories autorisees: membre, entourage, industrie, "
            "critique_journaliste, auteur_secondaire, influence, theoricien_mobilise)",
            result.blockers,
        )
        self.assertNotIn("schema invalide: Invalid value for categorie: manager", result.blockers)

    def test_identifier_collision_is_blocking(self) -> None:
        existing = """
## PERSON-test-person - Test Person

```yaml
id: PERSON-test-person
type_unite: person
name: Test Person
categorie: industrie
role:
  - producteur
sources:
  - S01
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```
"""
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp), canonical_person=existing)
            result = run_case(paths)

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("identifiant deja utilise: PERSON-test-person", result.blockers)

    def test_author_source_rejects_same_as(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, origin="auteur_source", same_as=["PERS-S01-001"])

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("auteur_source exige same_as vide", result.blockers)

    def test_empty_same_as_explains_missing_write_target(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths)

        self.assertIn(
            "Aucun PERS-* fourni. Aucune cible d'ecriture source/provisoire n'est identifiable. "
            "Validation humaine necessaire avant integration.",
            result.information,
        )

    def test_same_as_explains_probable_write_target(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, same_as=["PERS-S01-001"])

        self.assertEqual(result.decision, "pre-validee")
        self.assertIn(
            "Cible d'ecriture probable : registers/people/*.md puis regeneration controlee de "
            "registers/people/00_canonical_people.md. Pourquoi : PERS-* fourni. "
            "Il manque la confirmation humaine du fichier source/provisoire a modifier.",
            result.information,
        )

    def test_identity_arbitration_produces_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result = run_case(paths, identity_arbitration=True)

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertIn("identite a arbitrer: rattachement ou homonymie a confirmer", result.reserves)

    def test_near_alias_collision_is_reserve_not_blocker(self) -> None:
        existing = """
## PERSON-ian-curtis - Ian Curtis

```yaml
id: PERSON-ian-curtis
type_unite: person
name: Ian Curtis
categorie: membre
role:
  - chanteur
sources:
  - S01
same_as:
  - PERS-S01-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```
"""
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp), canonical_person=existing)
            result = run_case(paths, aliases=["Iain Curtis"])

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn("alias proche d'un nom a arbitrer: Iain Curtis ~ Ian Curtis (PERSON-ian-curtis)", result.reserves)

    def test_help_lists_allowed_categories(self) -> None:
        help_text = m2_add_person.build_parser().format_help()

        self.assertIn("Categories autorisees:", help_text)
        self.assertIn("  - membre", help_text)
        self.assertIn("  - theoricien_mobilise", help_text)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_repo(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_add_person.render_result(result_a), m2_add_person.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
