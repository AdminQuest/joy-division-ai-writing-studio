#!/usr/bin/env python3
"""Unit checks for the minimal M1 aggregation layer."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools import aggregate_m1


class TestStrictIndicatorParsing(unittest.TestCase):
    def test_absent_indicator_is_not_zero(self) -> None:
        self.assertIsNone(aggregate_m1.int_value({}, "Écarts détectés"))

    def test_non_numeric_indicator_is_not_zero(self) -> None:
        self.assertIsNone(aggregate_m1.int_value({"Écarts détectés": "aucun"}, "Écarts détectés"))


class TestUnreadableReportStatus(unittest.TestCase):
    def test_atoms_report_without_summary_is_not_conform(self) -> None:
        status = aggregate_m1.status_for_atoms(Path("reports/m1/dm_atoms_traceability.md"), {})

        self.assertEqual(status.state, "rapport illisible")
        self.assertEqual(status.symbol, "✗")
        self.assertTrue(any("indicateurs requis absents" in observation for observation in status.observations))

    def test_registers_report_missing_required_indicator_is_not_conform(self) -> None:
        summary = {
            label: "0"
            for label in aggregate_m1.REQUIRED_REGISTERS_INDICATORS
            if label != "Identifiants introuvables"
        }

        status = aggregate_m1.status_for_registers(Path("reports/m1/dm_registers_consistency.md"), summary)

        self.assertEqual(status.state, "rapport illisible")
        self.assertTrue(any("Identifiants introuvables" in observation for observation in status.observations))

    def test_registers_report_with_non_numeric_required_indicator_is_not_conform(self) -> None:
        summary = {label: "0" for label in aggregate_m1.REQUIRED_REGISTERS_INDICATORS}
        summary["Compteurs incohérents"] = "non disponible"

        status = aggregate_m1.status_for_registers(Path("reports/m1/dm_registers_consistency.md"), summary)

        self.assertEqual(status.state, "rapport illisible")
        self.assertTrue(any("Compteurs incohérents" in observation for observation in status.observations))

    def test_render_report_surfaces_unreadable_status(self) -> None:
        status = aggregate_m1.status_for_atoms(Path("reports/m1/dm_atoms_traceability.md"), {})
        report = aggregate_m1.render_report([status])

        self.assertIn("**M1 STATUS** : non conforme", report)
        self.assertIn("rapport illisible", report)
        self.assertIn("Statut impossible à consolider", report)


class TestAtomsStrictStatus(unittest.TestCase):
    def valid_atoms_summary(self) -> dict[str, str]:
        return {
            "Documents declares dans le manifeste": "14",
            "Documents maîtres sur disque": "14",
            "Documents traçables": "14",
            "Documents partiellement traçables": "0",
            "Documents non traçables": "0",
            "Atomes visibles": "2477",
            "Atomes retrouvés": "2477",
            "Écarts détectés": "0",
        }

    def test_atoms_report_with_positive_gap_is_non_conform(self) -> None:
        summary = self.valid_atoms_summary()
        summary["Écarts détectés"] = "1"

        status = aggregate_m1.status_for_atoms(Path("reports/m1/dm_atoms_traceability.md"), summary)

        self.assertEqual(status.state, "non conforme")
        self.assertTrue(any("écart de traçabilité" in observation for observation in status.observations))

    def test_atoms_report_with_partial_document_is_non_conform(self) -> None:
        summary = self.valid_atoms_summary()
        summary["Documents partiellement traçables"] = "1"

        status = aggregate_m1.status_for_atoms(Path("reports/m1/dm_atoms_traceability.md"), summary)

        self.assertEqual(status.state, "non conforme")

    def test_atoms_report_with_missing_visible_atom_is_non_conform(self) -> None:
        summary = self.valid_atoms_summary()
        summary["Atomes retrouvés"] = "2476"

        status = aggregate_m1.status_for_atoms(Path("reports/m1/dm_atoms_traceability.md"), summary)

        self.assertEqual(status.state, "non conforme")


class TestRegistersStrictStatus(unittest.TestCase):
    def valid_registers_summary(self) -> dict[str, str]:
        return {
            "Documents declares dans le manifeste": "14",
            "Documents maîtres sur disque": "14",
            "Documents cohérents": "14",
            "Documents partiellement cohérents": "0",
            "Documents non cohérents": "0",
            "Écarts détectés": "0",
            "Identifiants introuvables": "0",
            "Registres absents": "0",
            "Compteurs incohérents": "0",
            "Familles non couvertes": "0",
            "Relations non résolues": "0",
            "Libellés divergents": "0",
            "Manifestes incohérents": "0",
        }

    def test_registers_report_with_unexplained_gap_is_non_conform(self) -> None:
        summary = self.valid_registers_summary()
        summary["Écarts détectés"] = "1"

        status = aggregate_m1.status_for_registers(Path("reports/m1/dm_registers_consistency.md"), summary)

        self.assertEqual(status.state, "non conforme")
        self.assertTrue(any("ne sont pas expliqués" in observation for observation in status.observations))

    def test_registers_report_with_non_coherent_document_is_non_conform(self) -> None:
        summary = self.valid_registers_summary()
        summary["Documents non cohérents"] = "1"

        status = aggregate_m1.status_for_registers(Path("reports/m1/dm_registers_consistency.md"), summary)

        self.assertEqual(status.state, "non conforme")
        self.assertTrue(any("Documents non cohérents=1" in observation for observation in status.observations))

    def test_registers_report_with_only_label_or_mvp_reserve_remains_reserve(self) -> None:
        summary = self.valid_registers_summary()
        summary["Libellés divergents"] = "2"
        summary["Familles non couvertes"] = "3"
        summary["Écarts détectés"] = "5"

        status = aggregate_m1.status_for_registers(Path("reports/m1/dm_registers_consistency.md"), summary)

        self.assertEqual(status.state, "conforme avec réserve")


class TestAuditValidationStatus(unittest.TestCase):
    def test_existing_audit_is_not_validated_when_control_is_non_conform(self) -> None:
        audit = aggregate_m1.KnownAudit(
            label="Atomes S35 source vide",
            path=Path(__file__),
            control_name="DM -> atomes",
            validation="atoms_conforme",
        )
        control = aggregate_m1.ControlStatus(
            "DM -> atomes",
            Path("reports/m1/dm_atoms_traceability.md"),
            "non conforme",
            "✗",
        )

        symbol, state, observation = aggregate_m1.audit_validation_status(audit, {"DM -> atomes": control})

        self.assertEqual(symbol, "⚠")
        self.assertEqual(state, "documenté — non validé par le contrôle associé")
        self.assertIn("non conforme", observation)

    def test_s35_audit_is_validated_when_atoms_control_is_conform(self) -> None:
        audit = aggregate_m1.KnownAudit(
            label="Atomes S35 source vide",
            path=Path(__file__),
            control_name="DM -> atomes",
            validation="atoms_conforme",
        )
        control = aggregate_m1.ControlStatus(
            "DM -> atomes",
            Path("reports/m1/dm_atoms_traceability.md"),
            "conforme",
            "✓",
        )

        symbol, state, _ = aggregate_m1.audit_validation_status(audit, {"DM -> atomes": control})

        self.assertEqual(symbol, "✓")
        self.assertEqual(state, "validé")

    def test_shadowplay_audit_is_validated_with_register_reserve_and_no_missing_id(self) -> None:
        audit = aggregate_m1.KnownAudit(
            label="SONG-S45-SHADOWPLAY-RCA",
            path=Path(__file__),
            control_name="DM -> registres",
            validation="registers_no_missing_ids",
        )
        control = aggregate_m1.ControlStatus(
            "DM -> registres",
            Path("reports/m1/dm_registers_consistency.md"),
            "conforme avec réserve",
            "⚠",
            summary={"Identifiants introuvables": "0"},
        )

        symbol, state, observation = aggregate_m1.audit_validation_status(audit, {"DM -> registres": control})

        self.assertEqual(symbol, "✓")
        self.assertEqual(state, "validé avec réserve")
        self.assertIn("Identifiants introuvables=0", observation)

    def test_shadowplay_audit_is_not_validated_with_missing_id(self) -> None:
        audit = aggregate_m1.KnownAudit(
            label="SONG-S45-SHADOWPLAY-RCA",
            path=Path(__file__),
            control_name="DM -> registres",
            validation="registers_no_missing_ids",
        )
        control = aggregate_m1.ControlStatus(
            "DM -> registres",
            Path("reports/m1/dm_registers_consistency.md"),
            "non conforme",
            "✗",
            summary={"Identifiants introuvables": "1"},
        )

        symbol, state, _ = aggregate_m1.audit_validation_status(audit, {"DM -> registres": control})

        self.assertEqual(symbol, "⚠")
        self.assertEqual(state, "documenté — non validé par le contrôle associé")


if __name__ == "__main__":
    unittest.main()
