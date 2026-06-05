#!/usr/bin/env python3
"""Unit checks for the M1 DM -> registers consistency control."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tools import check_dm_registers_consistency as dm_registers


class TestOutputPathGuard(unittest.TestCase):
    def test_default_output_is_allowed(self) -> None:
        resolved = dm_registers.resolve_output_path("reports/m1/dm_registers_consistency.md")
        self.assertEqual(resolved, dm_registers.DEFAULT_REPORT.resolve())

    def test_reports_m1_subpath_is_allowed(self) -> None:
        resolved = dm_registers.resolve_output_path("reports/m1/tmp/registers.md")
        expected = dm_registers.REPO_ROOT / "reports" / "m1" / "tmp" / "registers.md"
        self.assertEqual(resolved, expected.resolve())

    def test_corpus_paths_are_rejected(self) -> None:
        rejected = [
            "chapters/01/document_maitre.md",
            "exports/generated/people.json",
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
                    dm_registers.resolve_output_path(raw_path)


class TestMasterDocPathGuard(unittest.TestCase):
    def test_valid_master_doc_path_is_allowed(self) -> None:
        valid_path, issue = dm_registers.validate_master_doc_path_lexical("chapters/01/document_maitre.md")
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
                valid_path, issue = dm_registers.validate_master_doc_path_lexical(raw_path)
                self.assertIsNone(valid_path)
                self.assertIsNotNone(issue)

    def test_audit_refuses_symlinked_master_doc_before_reading(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            target = repo_root / "chapters" / "master_docs.json"
            target.write_text("not a master document", encoding="utf-8")
            (chapter_dir / "document_maitre.md").symlink_to(target)

            with patch.object(dm_registers, "REPO_ROOT", repo_root):
                audit = dm_registers.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "Test"},
                    register_exports={family: {} for family in dm_registers.P0_FAMILIES},
                    master_index={},
                )

        self.assertEqual(audit.status, "non cohérent")
        self.assertEqual(audit.issues[0].kind, "document maître invalide")


class TestDiskScanGuard(unittest.TestCase):
    def test_scan_rejects_disk_only_symlinked_master_doc(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "99"
            chapter_dir.mkdir(parents=True)
            target = repo_root / "chapters" / "master_docs.json"
            target.write_text("not a master document", encoding="utf-8")
            (chapter_dir / "document_maitre.md").symlink_to(target)

            with patch.object(dm_registers, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_registers.scan_disk_master_docs()

        self.assertEqual(disk_paths, set())
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertIn("présent sur disque mais refusé", issues[0].detail)

    def test_scan_rejects_disk_only_symlinked_chapter_directory(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapters_dir = repo_root / "chapters"
            real_chapter = chapters_dir / "02"
            real_chapter.mkdir(parents=True)
            (real_chapter / "document_maitre.md").write_text("# DM\n", encoding="utf-8")
            (chapters_dir / "99").symlink_to(real_chapter, target_is_directory=True)

            with patch.object(dm_registers, "REPO_ROOT", repo_root):
                disk_paths, issues = dm_registers.scan_disk_master_docs()

        self.assertEqual(disk_paths, {"chapters/02/document_maitre.md"})
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].kind, "document maître invalide")
        self.assertEqual(issues[0].dm, "chapters/99/document_maitre.md")


class TestRegisterExtraction(unittest.TestCase):
    def test_extracts_p0_refs_and_non_mvp_families(self) -> None:
        markdown = """
| PERS-001 | Ian Curtis |
| SONG-S34-001 | Shadowplay |
| CHR-1977-001 | Concert |
| CIT-S86-001 | Citation |
| JD-CONCERT-1977-001 | Live |
| JD-SESSION-1979-001 | Studio |
- REL-S42-001 — relation hors MVP
- CONCEPT-001 — concept hors MVP
"""
        refs, non_mvp = dm_registers.extract_visible_register_refs(markdown)

        self.assertIn("PERS-001", refs["people"])
        self.assertIn("SONG-S34-001", refs["songs"])
        self.assertIn("CHR-1977-001", refs["chronology"])
        self.assertIn("CIT-S86-001", refs["quotes"])
        self.assertIn("JD-CONCERT-1977-001", refs["concerts"])
        self.assertIn("JD-SESSION-1979-001", refs["sessions"])
        self.assertIn("REL-S42-001", non_mvp["relations"])
        self.assertIn("CONCEPT-001", non_mvp["concepts"])

    def test_extracts_dashboard_counts(self) -> None:
        markdown = """
| Indicateur | Valeur |
| Personnes | 12 |
| Chansons | 8 |
| Événements chronologiques | 4 |
| Citations | 5 |
"""
        counts = dm_registers.extract_dashboard_counts(markdown)

        self.assertEqual(counts["people"], 12)
        self.assertEqual(counts["songs"], 8)
        self.assertEqual(counts["chronology"], 4)
        self.assertEqual(counts["quotes"], 5)


class TestAuditDocument(unittest.TestCase):
    def test_audit_marks_document_coherent_when_ids_and_counts_match(self) -> None:
        markdown = """
| Personnes | 1 |
| Chansons | 1 |
| Événements chronologiques | 1 |
| Citations | 1 |
| PERS-001 | Ian Curtis |
| SONG-S34-001 | Shadowplay |
| CHR-1977-001 | Concert |
| CIT-S86-001 | Citation |
"""
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (chapter_dir / "document_maitre.md").write_text(markdown, encoding="utf-8")

            register_exports = {family: {} for family in dm_registers.P0_FAMILIES}
            register_exports["people"]["PERS-001"] = dm_registers.RegisterRecord("PERS-001", "Ian Curtis")
            register_exports["songs"]["SONG-S34-001"] = dm_registers.RegisterRecord("SONG-S34-001", "Shadowplay")
            register_exports["chronology"]["CHR-1977-001"] = dm_registers.RegisterRecord("CHR-1977-001", "Concert")
            register_exports["quotes"]["CIT-S86-001"] = dm_registers.RegisterRecord("CIT-S86-001", "Citation")

            with patch.object(dm_registers, "REPO_ROOT", repo_root):
                audit = dm_registers.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "Test"},
                    register_exports=register_exports,
                    master_index={
                        "chapters/01/document_maitre.md": {
                            "people": 1,
                            "songs": 1,
                            "chronology": 1,
                            "quotes": 1,
                        }
                    },
                )

        self.assertEqual(audit.status, "cohérent")
        self.assertEqual(audit.issues, [])

    def test_audit_reports_unknown_p0_identifier(self) -> None:
        markdown = """
| Personnes | 0 |
| Chansons | 1 |
| Événements chronologiques | 0 |
| Citations | 0 |
| SONG-UNKNOWN | Unknown |
"""
        with TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            chapter_dir = repo_root / "chapters" / "01"
            chapter_dir.mkdir(parents=True)
            (chapter_dir / "document_maitre.md").write_text(markdown, encoding="utf-8")

            with patch.object(dm_registers, "REPO_ROOT", repo_root):
                audit = dm_registers.audit_document(
                    {"path": "chapters/01/document_maitre.md", "title": "Test"},
                    register_exports={family: {} for family in dm_registers.P0_FAMILIES},
                    master_index={
                        "chapters/01/document_maitre.md": {
                            "people": 0,
                            "songs": 1,
                            "chronology": 0,
                            "quotes": 0,
                        }
                    },
                )

        self.assertEqual(audit.status, "partiellement cohérent")
        self.assertEqual(audit.issues[0].kind, "identifiant introuvable")


if __name__ == "__main__":
    unittest.main()
