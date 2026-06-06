#!/usr/bin/env python3
"""Unit checks for the M1 DM -> sources consistency control."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tools import aggregate_m1
from tools import check_dm_sources_consistency as dm_sources


class TestOutputPathGuard(unittest.TestCase):
    def test_default_output_is_allowed(self) -> None:
        resolved = dm_sources.resolve_output_path("reports/m1/dm_sources_consistency.md")
        self.assertEqual(resolved, dm_sources.DEFAULT_REPORT.resolve())

    def test_reports_m1_subpath_is_allowed(self) -> None:
        resolved = dm_sources.resolve_output_path("reports/m1/tmp/sources.md")
        expected = dm_sources.REPO_ROOT / "reports" / "m1" / "tmp" / "sources.md"
        self.assertEqual(resolved, expected.resolve())

    def test_corpus_paths_are_rejected(self) -> None:
        rejected = [
            "chapters/01/document_maitre.md",
            "exports/generated/master_docs_index.json",
            "chapters/master_docs.json",
            "registers/example.json",
            "sources/example.md",
            "data/registre.json",
            "docs/example.md",
            "tools/example.py",
            "reports/m1/../../docs/example.md",
        ]
        for raw_path in rejected:
            with self.subTest(raw_path=raw_path):
                with self.assertRaises(ValueError):
                    dm_sources.resolve_output_path(raw_path)


class TestSourceExtraction(unittest.TestCase):
    def test_extracts_source_ids_without_atom_ids(self) -> None:
        markdown = """
| S01 | S01 — Source canonique | 1 | 0 |
- **S01-A001** — Atome
  Source : S01 — Source canonique
- **S02-PART-TEST** — S02 — Partie de source
"""
        self.assertEqual(dm_sources.extract_visible_source_ids(markdown), {"S01", "S02"})


class TestAuditDocument(unittest.TestCase):
    def test_conform_case_finds_all_visible_sources(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (chapter_dir / "document_maitre.md").write_text(
                "| Sources mobilisées | 1 |\n\n| ID | Source |\n|---|---|\n| S01 | S01 — Source |\n",
                encoding="utf-8",
            )

            with patch.object(dm_sources, "REPO_ROOT", repo_root):
                audit = dm_sources.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "Test"},
                    {"S01"},
                )

        self.assertEqual(audit.status, "cohérent")
        self.assertEqual(audit.visible_sources, {"S01"})
        self.assertEqual(audit.found_sources, {"S01"})
        self.assertEqual(audit.unknown_sources, set())

    def test_unknown_source_fails_control(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (chapter_dir / "document_maitre.md").write_text(
                "| ID | Source |\n|---|---|\n| S99 | S99 — Source absente |\n",
                encoding="utf-8",
            )

            with patch.object(dm_sources, "REPO_ROOT", repo_root):
                audit = dm_sources.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "Test"},
                    {"S01"},
                )

        self.assertEqual(audit.status, "non cohérent")
        self.assertEqual(audit.unknown_sources, {"S99"})
        self.assertEqual(audit.issues[0].kind, "source inconnue")

    def test_orphan_source_is_reported_without_blocking_gap(self) -> None:
        audit = dm_sources.DmAudit(
            path="chapters/01/document_maitre.md",
            status="cohérent",
            visible_sources={"S01"},
            found_sources={"S01"},
        )

        summary = dm_sources.summarize(
            [audit],
            global_issues=[],
            disk_paths={"chapters/01/document_maitre.md"},
            canonical_source_ids={"S01", "S02"},
        )
        report = dm_sources.render_report(
            [audit],
            global_issues=[],
            disk_paths={"chapters/01/document_maitre.md"},
            canonical_source_ids={"S01", "S02"},
        )

        self.assertEqual(summary["sources_orphelines"], 1)
        self.assertEqual(summary["ecarts_detectes"], 0)
        self.assertIn("`S02`", report)
        self.assertIn("information documentaire", report)


class TestEmptyReportDetection(unittest.TestCase):
    def test_empty_sources_report_is_unreadable_for_aggregator(self) -> None:
        status = aggregate_m1.status_for_sources(Path("reports/m1/dm_sources_consistency.md"), {})

        self.assertEqual(status.state, "rapport illisible")
        self.assertEqual(status.symbol, "✗")
        self.assertTrue(any("indicateurs requis absents" in observation for observation in status.observations))


if __name__ == "__main__":
    unittest.main()
