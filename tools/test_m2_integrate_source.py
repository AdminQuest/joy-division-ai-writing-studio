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


def write_campaign_registry(root: Path) -> m2_integrate_source.Paths:
    (root / "data").mkdir(parents=True)
    payload = [
        {
            "id": "S72",
            "auteur": "Simon Reynolds",
            "titre": "Rip It Up and Start Again: Postpunk 1978–1984",
            "annee": "2005/2006",
            "reference_complete": "Reynolds, Simon, Rip It Up and Start Again: Postpunk 1978-1984, 2005/2006.",
        },
        {
            "id": "S74",
            "auteur": "Mick Middles",
            "titre": "From Joy Division to New Order",
            "annee": "1996",
            "reference_complete": "Middles, Mick, From Joy Division to New Order, 1996.",
        },
        {
            "id": "S90",
            "auteur": "Mark Fisher",
            "titre": "Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures",
            "annee": "2014",
            "reference_complete": "Fisher, Mark, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures, 2014.",
            "dossier_source": "sources/fisher_ghosts_of_my_life/",
        },
        {
            "id": "S91",
            "auteur": "Simon Reynolds",
            "titre": "Retromania: Pop Culture's Addiction to Its Own Past",
            "annee": "2011",
            "reference_complete": "Reynolds, Simon, Retromania: Pop Culture's Addiction to Its Own Past, 2011.",
        },
        {
            "id": "S94",
            "auteur": "James Weissinger",
            "titre": "Retromania: Pop Culture's Addiction to Its Own Past (Book Review)",
            "annee": "2012",
            "reference_complete": "Weissinger, James, Retromania: Pop Culture's Addiction to Its Own Past (Book Review), 2012.",
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
        self.assertIn("dossier source probable: sources/known_author_known_source/", result.information)
        self.assertEqual(result.candidate["dossier_source_probable"], "sources/known_author_known_source/")

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

    def test_incomplete_author_is_weak_proximity_not_blocking_duplicate(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_campaign_registry(Path(tmp))
            result = run_case(
                paths,
                title="From Joy Division to New Order",
                author="Middles",
                year="1996",
                reference="MIDDLES, From Joy Division to New Order, 1996.",
            )

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "source proche detectee : metadonnees partielles possibles (S74 - Mick Middles - From Joy Division to New Order (1996))",
            result.reserves,
        )

    def test_abbreviated_title_is_weak_proximity(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_campaign_registry(Path(tmp))
            result = run_case(
                paths,
                title="From Joy Division",
                author="Mick Middles",
                year="1996",
                reference="MIDDLES, Mick, From Joy Division, 1996.",
            )

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "source proche detectee : metadonnees partielles possibles (S74 - Mick Middles - From Joy Division to New Order (1996))",
            result.reserves,
        )

    def test_incomplete_author_and_abbreviated_title_reserve_s74(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_campaign_registry(Path(tmp))
            result = run_case(
                paths,
                title="From Joy Division",
                author="Middles",
                year="1996",
                reference="MIDDLES, From Joy Division, 1996.",
            )

        self.assertEqual(result.decision, "pre-validee avec reserve")
        self.assertEqual(result.blockers, [])
        self.assertIn(
            "source proche detectee : metadonnees partielles possibles (S74 - Mick Middles - From Joy Division to New Order (1996))",
            result.reserves,
        )

    def test_campaign_non_regressions_remain_classified(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_campaign_registry(Path(tmp))
            s90 = run_case(
                paths,
                title="Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures",
                author="Mark Fisher",
                year="2014",
                reference="Fisher, Mark, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures, 2014.",
            )
            s91 = run_case(
                paths,
                title="Retromania: Pop Culture's Addiction to Its Own Past",
                author="Simon Reynolds",
                year="2012",
                reference="Reynolds, Simon, Retromania: Pop Culture's Addiction to Its Own Past, Faber paperback edition, 2012.",
            )
            s72 = run_case(
                paths,
                title="Rip It Up and Start Again: Postpunk 1978–1984",
                author="Simon Reynolds",
                year="2007",
                reference="Reynolds, Simon, Rip It Up and Start Again: Postpunk 1978-1984, edition francaise, 2007.",
            )
            s94 = run_case(
                paths,
                title="Retromania: Pop Culture's Addiction to Its Own Past (Book Review)",
                author="James Weissinger",
                source_type="article",
                year="2012",
                reference="Weissinger, James, Retromania: Pop Culture's Addiction to Its Own Past (Book Review), 2012.",
            )

        self.assertEqual(s90.decision, "non pre-validee")
        self.assertIn("source deja presente de facon certaine: S90 - Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures (2014)", s90.blockers)
        self.assertEqual(s91.decision, "pre-validee avec reserve")
        self.assertIn("source proche detectee : autre edition ou reedition possible (S91 - Retromania: Pop Culture's Addiction to Its Own Past (2011))", s91.reserves)
        self.assertEqual(s72.decision, "pre-validee avec reserve")
        self.assertIn("source proche detectee : autre edition ou reedition possible (S72 - Rip It Up and Start Again: Postpunk 1978–1984 (2005/2006))", s72.reserves)
        self.assertEqual(s94.decision, "non pre-validee")
        self.assertIn("source deja presente de facon certaine: S94 - Retromania: Pop Culture's Addiction to Its Own Past (Book Review) (2012)", s94.blockers)

    def test_output_is_deterministic(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_minimal_registry(Path(tmp))
            result_a = run_case(paths)
            result_b = run_case(paths)

        self.assertEqual(m2_integrate_source.render_result(result_a), m2_integrate_source.render_result(result_b))


if __name__ == "__main__":
    unittest.main()
