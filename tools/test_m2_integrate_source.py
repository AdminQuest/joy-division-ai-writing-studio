#!/usr/bin/env python3
"""Tests du prototype CLI M2 d'integration de source longue."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_integrate_source


def write_minimal_registry(root: Path) -> m2_integrate_source.Paths:
    (root / "data").mkdir(parents=True)
    payload = [
        {
            "id": "S01",
            "auteur": "Known Author",
            "titre": "Known Source",
            "annee": "2001",
            "reference_complete": "Known Author, Known Source, Test Press, 2001.",
            "dossier_source": "sources/known_author_known_source/",
        },
        {
            "id": "S02",
            "auteur": "Near Author",
            "titre": "Near Source",
            "annee": "2019",
            "reference_complete": "Near Author, Near Source, First Edition, 2019.",
        },
        {
            "id": "S03",
            "auteur": "URL Author",
            "titre": "URL Source",
            "annee": "2020",
            "reference_complete": "URL Author, URL Source, Web Archive, 2020.",
            "url": "https://example.test/source",
        },
        {
            "id": "S04",
            "auteur": "Alan J. Kidd",
            "titre": "Manchester: A History",
            "annee": "2006",
            "reference_complete": "Kidd, Alan J. Manchester: A History. Lancaster / Clitheroe: Carnegie Publishing, 2006.",
        },
    ]
    (root / "data" / "registre.json").write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return m2_integrate_source.Paths(root=root, source_registry=root / "data" / "registre.json")


def run_case(paths: m2_integrate_source.Paths, **overrides) -> m2_integrate_source.CheckResult:
    params = {
        "title": "New Source",
        "author": "New Author",
        "source_type": "livre",
        "year": "2026",
        "reference": "New Author, New Source, Test Press, 2026.",
        "paths": paths,
    }
    params.update(overrides)
    return m2_integrate_source.evaluate_source_integration(**params)


class TestM2IntegrateSource(unittest.TestCase):
    def test_conform_case_is_prevalidated(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(paths)

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.blockers, [])
        self.assertEqual(result.reserves, [])
        self.assertIn("nouveau Sxx probablement requis: S05", result.information)
        self.assertEqual(result.candidate["dossier_source_probable"], "sources/new_author_new_source/")

    def test_existing_source_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(
                paths,
                title="Known Source",
                author="Known Author",
                year="2001",
                reference="Known Author, Known Source, Test Press, 2001.",
            )

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source deja presente de facon certaine: S01 - Known Source (2001)", result.blockers)
        self.assertIn("Sxx existant: S01", result.information)

    def test_near_source_is_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(
                paths,
                title="Near Source",
                author="Near Author",
                year="2024",
                reference="Near Author, Near Source, Revised Edition, 2024.",
            )

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "source proche detectee : autre edition ou reedition possible (S02 - Near Source (2019))",
            result.reserves,
        )

    def test_invalid_type_is_blocking(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(paths, source_type="blog")

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn(
            "type documentaire inconnu: blog (types autorises: livre, article, interview, fanzine, archive, memoire, these, dossier documentaire)",
            result.blockers,
        )

    def test_blank_url_does_not_match_first_registry_entry(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(paths, url="   ")

        self.assertEqual(result.decision, "pre-validee")
        self.assertEqual(result.blockers, [])
        self.assertIn("nouveau Sxx probablement requis: S05", result.information)
        self.assertNotIn("url", result.candidate["metadata"])

    def test_canonical_url_field_is_blocking_duplicate(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(
                paths,
                title="Different Title",
                author="Different Author",
                year="2026",
                reference="Different Author, Different Title, Test Press, 2026.",
                url="https://example.test/source",
            )

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source deja presente de facon certaine: S03 - URL Source (2020)", result.blockers)
        self.assertIn("Sxx existant: S03", result.information)

    def test_author_surname_first_form_matches_existing_source(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result = run_case(
                paths,
                title="Manchester: A History",
                author="Kidd, Alan J.",
                year="2006",
                reference="Kidd, Alan J. Manchester: A History. Lancaster / Clitheroe: Carnegie Publishing, 2006.",
            )

        self.assertEqual(result.decision, "non pre-validee")
        self.assertIn("source deja presente de facon certaine: S04 - Manchester: A History (2006)", result.blockers)
        self.assertIn("Sxx existant: S04", result.information)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_integrate_source.render_result(result_a), m2_integrate_source.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
