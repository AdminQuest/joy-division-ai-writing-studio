#!/usr/bin/env python3
"""Unit checks for the M1 DM -> atoms traceability control."""

from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

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


class TestDiskScanGuard(unittest.TestCase):
    def test_scan_rejects_disk_only_symlinked_master_doc(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (repo_root / "chapters" / "master_docs.json").write_text("not a master document", encoding="utf-8")
            (chapter_dir / "document_maitre.md").symlink_to(repo_root / "chapters" / "master_docs.json")

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_atoms.scan_disk_master_docs()

        self.assertEqual(disk_paths, set())
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertIn("présent sur disque mais refusé", issues[0].detail)

    def test_scan_rejects_disk_only_symlinked_chapter_directory(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapters_dir = repo_root / "chapters"
            real_chapter_dir = chapters_dir / "02"
            real_chapter_dir.mkdir(parents=True)
            (real_chapter_dir / "document_maitre.md").write_text("| Atomes | 0 |\n", encoding="utf-8")
            (chapters_dir / "99").symlink_to(real_chapter_dir, target_is_directory=True)

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_atoms.scan_disk_master_docs()

        self.assertEqual(disk_paths, {"chapters/02/document_maitre.md"})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertEqual(issues[0].dm, "chapters/99/document_maitre.md")

    def test_scan_rejects_disk_only_symlink_to_another_chapter(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapters_dir = repo_root / "chapters"
            target_chapter_dir = chapters_dir / "02"
            symlink_chapter_dir = chapters_dir / "99"
            target_chapter_dir.mkdir(parents=True)
            symlink_chapter_dir.mkdir()
            (target_chapter_dir / "document_maitre.md").write_text("| Atomes | 0 |\n", encoding="utf-8")
            (symlink_chapter_dir / "document_maitre.md").symlink_to(target_chapter_dir / "document_maitre.md")

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_atoms.scan_disk_master_docs()

        self.assertEqual(disk_paths, {"chapters/02/document_maitre.md"})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertEqual(issues[0].dm, "chapters/99/document_maitre.md")

    def test_scan_rejects_disk_only_symlink_to_master_docs_manifest(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "99"
            chapter_dir.mkdir(parents=True)
            (repo_root / "chapters" / "master_docs.json").write_text("not a master document", encoding="utf-8")
            (chapter_dir / "document_maitre.md").symlink_to(repo_root / "chapters" / "master_docs.json")

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_atoms.scan_disk_master_docs()

        self.assertEqual(disk_paths, set())
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertEqual(issues[0].dm, "chapters/99/document_maitre.md")


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

    def test_audit_refuses_symlinked_master_doc_before_reading(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (repo_root / "chapters" / "master_docs.json").write_text("not a master document", encoding="utf-8")
            (chapter_dir / "document_maitre.md").symlink_to(repo_root / "chapters" / "master_docs.json")

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                audit = dm_atoms.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "symlink"},
                    atom_ids=set(),
                    alias_lookup={},
                    master_index={"chapters/01/document_maitre.md": {"atoms": 1}},
                )

        self.assertEqual(audit.status, "non traçable")
        self.assertEqual(audit.visible_atoms, 0)
        self.assertEqual(audit.issues[0].kind, "document maître invalide")
        self.assertIn("composant symlinké", audit.issues[0].detail)

    def test_audit_refuses_symlinked_chapter_directory_before_reading(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapters_dir = repo_root / "chapters"
            real_chapter_dir = chapters_dir / "02"
            real_chapter_dir.mkdir(parents=True)
            (real_chapter_dir / "document_maitre.md").write_text("| Atomes | 0 |\n", encoding="utf-8")
            (chapters_dir / "99").symlink_to(real_chapter_dir, target_is_directory=True)

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                audit = dm_atoms.audit_document(
                    {"path": "chapters/99/document_maitre.md", "title": "symlinked chapter"},
                    atom_ids=set(),
                    alias_lookup={},
                    master_index={"chapters/99/document_maitre.md": {"atoms": 0}},
                )

        self.assertEqual(audit.status, "non traçable")
        self.assertEqual(audit.visible_atoms, 0)
        self.assertEqual(audit.issues[0].kind, "document maître invalide")
        self.assertIn("composant symlinké", audit.issues[0].detail)

    def test_audit_refuses_symlinked_chapter_to_chapters_root_before_reading(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapters_dir = repo_root / "chapters"
            chapters_dir.mkdir(parents=True)
            (chapters_dir / "document_maitre.md").write_text("| Atomes | 0 |\n", encoding="utf-8")
            (chapters_dir / "99").symlink_to(chapters_dir, target_is_directory=True)

            with patch.object(dm_atoms, "REPO_ROOT", repo_root):
                audit = dm_atoms.audit_document(
                    {"path": "chapters/99/document_maitre.md", "title": "symlinked chapter root"},
                    atom_ids=set(),
                    alias_lookup={},
                    master_index={"chapters/99/document_maitre.md": {"atoms": 0}},
                )

        self.assertEqual(audit.status, "non traçable")
        self.assertEqual(audit.visible_atoms, 0)
        self.assertEqual(audit.issues[0].kind, "document maître invalide")
        self.assertIn("composant symlinké", audit.issues[0].detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)
