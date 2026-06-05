#!/usr/bin/env python3
"""Unit checks for the M1 DM -> atoms traceability control."""

from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from tools import check_dm_atoms_traceability as dm_atoms


class TestOutputPathGuard(unittest.TestCase):
    def test_default_output_is_allowed(self) -> None:
        resolved = dm_atoms.resolve_output_path("reports/m1/dm_atoms_traceability.md")
        self.assertEqual(resolved, dm_atoms.DEFAULT_REPORT.resolve())

    def test_reports_m1_subpath_is_allowed(self) -> None:
        resolved = dm_atoms.resolve_output_path("reports/m1/tmp/report.md")
        self.assertEqual(resolved, (dm_atoms.REPO_ROOT / "reports" / "m1" / "tmp" / "report.md").resolve())

    def test_corpus_paths_are_rejected(self) -> None:
        rejected = [
            "chapters/01/document_maitre.md",
            "exports/generated/atoms.json",
            "chapters/master_docs.json",
            "registers/example.json",
            "sources/example.md",
            "data/example.json",
            "docs/example.md",
            "tools/example.py",
            "reports/m1/../../docs/example.md",
        ]
        for raw_path in rejected:
            with self.subTest(raw_path=raw_path):
                with self.assertRaises(ValueError):
                    dm_atoms.resolve_output_path(raw_path)


class TestManifestIndexDiskDrift(unittest.TestCase):
    def test_detects_disk_master_docs_outside_manifest_and_index(self) -> None:
        documents = [
            {"path": "chapters/01/document_maitre.md"},
            {"path": "chapters/99/document_maitre.md"},
        ]
        master_index = {
            "chapters/01/document_maitre.md": {"atoms": 1},
            "chapters/02/document_maitre.md": {"atoms": 1},
        }
        disk_paths = {
            "chapters/01/document_maitre.md",
            "chapters/03/document_maitre.md",
        }

        issues = dm_atoms.detect_manifest_index_disk_drift(documents, master_index, disk_paths)
        observed = {(issue.kind, issue.dm) for issue in issues}

        self.assertIn(("document maître hors manifeste", "chapters/03/document_maitre.md"), observed)
        self.assertIn(("document maître absent de l'index", "chapters/03/document_maitre.md"), observed)
        self.assertIn(("dérive manifeste / index", "chapters/02/document_maitre.md"), observed)


class TestMasterDocPathGuard(unittest.TestCase):
    def test_valid_master_doc_path_is_allowed(self) -> None:
        valid_path, issue = dm_atoms.validate_master_doc_path("chapters/01/document_maitre.md")
        self.assertEqual(valid_path, "chapters/01/document_maitre.md")
        self.assertIsNone(issue)

    def test_invalid_master_doc_paths_are_rejected(self) -> None:
        rejected = [
            "/tmp/document_maitre.md",
            "chapters/01/../document_maitre.md",
            "docs/document_maitre.md",
            "chapters/01/notes.md",
        ]
        for raw_path in rejected:
            with self.subTest(raw_path=raw_path):
                valid_path, issue = dm_atoms.validate_master_doc_path(raw_path)
                self.assertIsNone(valid_path)
                self.assertIsNotNone(issue)

    def test_audit_does_not_read_invalid_manifest_path(self) -> None:
        audit = dm_atoms.audit_document(
            {"path": "/tmp/document_maitre.md", "title": "invalid"},
            atom_ids=set(),
            alias_lookup={},
            master_index={},
        )

        self.assertEqual(audit.status, "non traçable")
        self.assertEqual(audit.visible_atoms, 0)
        self.assertEqual(audit.issues[0].kind, "manifeste incohérent")

    def test_index_rejects_invalid_paths(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            index_path = Path(tmp_dir) / "master_docs_index.json"
            index_path.write_text(
                '{"chapters": [{"path": "chapters/01/notes.md", "atoms": 1}]}',
                encoding="utf-8",
            )

            index, issues = dm_atoms.load_master_index(index_path)

        self.assertEqual(index, {})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "manifeste incohérent")


if __name__ == "__main__":
    unittest.main(verbosity=2)
