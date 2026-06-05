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


if __name__ == "__main__":
    unittest.main()
