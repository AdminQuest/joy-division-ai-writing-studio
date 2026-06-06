#!/usr/bin/env python3
"""Tests du resume de PR commun M2."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools import m2_add_org, m2_add_person, m2_core, m2_integrate_source
from tools.test_m2_add_org import existing_org, write_minimal_repo as write_org_repo
from tools.test_m2_add_person import write_minimal_repo as write_person_repo
from tools.test_m2_integrate_source import write_minimal_registry as write_source_registry


class TestM2PRSummary(unittest.TestCase):
    def test_markdown_renders_prevalidated_without_blockers(self) -> None:
        result = m2_core.CheckResult(candidate={"id": "TEST"})
        result.information.append("information utile")
        result.finalize()

        summary = m2_core.build_pr_summary(
            result,
            subject="Objet test",
            scope=["Perimetre test"],
            validations=["Validation test"],
            human_arbitrations=["Validation humaine finale"],
            documentary_impact=["Impact test"],
            verification_commands=["python3 -m unittest tools.test_m2_pr_summary"],
        )
        markdown = m2_core.render_pr_summary(summary)

        self.assertIn("# Resume de PR M2", markdown)
        self.assertIn("## Bloquants", markdown)
        self.assertIn("- aucun", markdown)
        self.assertIn("`python3 -m unittest tools.test_m2_pr_summary`", markdown)

    def test_markdown_renders_reserve(self) -> None:
        result = m2_core.CheckResult(candidate={"id": "TEST"})
        result.reserves.append("reserve a arbitrer")
        result.finalize()

        summary = m2_core.build_pr_summary(
            result,
            subject="Objet avec reserve",
            scope=["Perimetre test"],
            validations=["Validation test"],
            human_arbitrations=["Arbitrer la reserve"],
            documentary_impact=["Impact test"],
            verification_commands=["python3 -m unittest tools.test_m2_pr_summary"],
        )

        self.assertIn("- reserve a arbitrer", m2_core.render_pr_summary(summary))

    def test_markdown_renders_blocker(self) -> None:
        result = m2_core.CheckResult(candidate={"id": "TEST"})
        result.blockers.append("bloquant a corriger")
        result.finalize()

        summary = m2_core.build_pr_summary(
            result,
            subject="Objet bloque",
            scope=["Perimetre test"],
            validations=["Validation test"],
            human_arbitrations=["Corriger le bloquant"],
            documentary_impact=["Impact test"],
            verification_commands=["python3 -m unittest tools.test_m2_pr_summary"],
        )

        self.assertIn("- bloquant a corriger", m2_core.render_pr_summary(summary))

    def test_person_adapter_writes_pr_summary(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_person_repo(Path(tmp))
            result = m2_add_person.evaluate_person_addition(
                name="Test Person",
                category="industrie",
                roles=["producteur"],
                sources=["S01"],
                paths=paths,
            )
            path = m2_add_person.write_person_pr_summary(result, paths)
            markdown = path.read_text(encoding="utf-8")

        self.assertEqual(path.name, "pr_summary_person_person-test-person.md")
        self.assertIn("Ajout PERSON : Test Person (PERSON-test-person)", markdown)
        self.assertIn("## Reserves", markdown)

    def test_org_adapter_writes_pr_summary_with_reserve(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_org_repo(Path(tmp), org_records=[existing_org(name="Factory Records")])
            result = m2_add_org.evaluate_org_addition(
                name="Unrelated Org",
                category="label",
                country="GB",
                jd_relation="label_mate",
                sources=["S01"],
                last_verified="2026-06-01",
                aliases=["Factory Record"],
                paths=paths,
            )
            path = m2_add_org.write_org_pr_summary(result, paths)
            markdown = path.read_text(encoding="utf-8")

        self.assertEqual(path.name, "pr_summary_org_org-0002_unrelated-org.md")
        self.assertIn("Ajout ORG : Unrelated Org (ORG-0002)", markdown)
        self.assertIn("alias proche d'un nom a arbitrer", markdown)

    def test_source_adapter_writes_pr_summary_with_blocker(self) -> None:
        with TemporaryDirectory() as tmp:
            paths = write_source_registry(Path(tmp))
            result = m2_integrate_source.evaluate_source_integration(
                title="Known Source",
                author="Known Author",
                source_type="livre",
                year="2001",
                reference="Known Author, Known Source, Test Press, 2001.",
                paths=paths,
            )
            path = m2_integrate_source.write_source_pr_summary(result, paths)
            markdown = path.read_text(encoding="utf-8")

        self.assertEqual(path.name, "pr_summary_source_known_author_known_source.md")
        self.assertIn("Integration source longue : Known Source", markdown)
        self.assertIn("source deja presente de facon certaine", markdown)


if __name__ == "__main__":
    unittest.main()
