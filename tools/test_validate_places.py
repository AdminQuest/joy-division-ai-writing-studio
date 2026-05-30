#!/usr/bin/env python3
"""Tests unitaires des invariants same_as du registre des lieux (INV-1..4).

Couvre, pour chaque invariant, un cas PASSANT et un cas en ÉCHEC, plus le cas
réel T.J. Davidson (PLACE-TJ-DAVIDSONS canonique ; PLACE-S83-001 et
PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET en same_as) comme cas passant.

Exécution : python3 -m unittest tools.test_validate_places
        ou : python3 tools/test_validate_places.py
"""
import unittest

from validate_places import check_same_as, VALIDATOR


def rec(pid, same_as=None, lat=None, lng=None, prud=None, prec=None):
    """Construit un (record, rel) minimal au format attendu par check_same_as."""
    d = {"id": pid, "label": pid, "type": "studio"}
    if same_as is not None:
        d["same_as"] = same_as
    if lat is not None:
        d["lat"], d["lng"] = lat, lng
    if prec is not None:
        d["geo_precision"] = prec
    if prud is not None:
        d["prudence_methodologique"] = prud
    return (d, f"registers/places/{pid}.md")


def errors_of(records):
    errors, _warnings, _rep = check_same_as(records)
    return errors


def inv6_warnings(records):
    _e, warnings, _r = check_same_as(records)
    return [w for w in warnings if w.startswith("INV-6")]


def codes(errors):
    return {e.split(" —")[0] for e in errors}


class TestINV1TargetExists(unittest.TestCase):
    def test_pass(self):
        recs = [rec("PLACE-CANON"), rec("PLACE-LEGACY", same_as="PLACE-CANON")]
        self.assertNotIn("INV-1", codes(errors_of(recs)))

    def test_fail(self):
        recs = [rec("PLACE-LEGACY", same_as="PLACE-DOES-NOT-EXIST")]
        self.assertIn("INV-1", codes(errors_of(recs)))


class TestINV2NoCycle(unittest.TestCase):
    def test_pass(self):
        recs = [rec("PLACE-CANON"),
                rec("PLACE-A", same_as="PLACE-CANON"),
                rec("PLACE-B", same_as="PLACE-A")]   # chaîne acyclique A->CANON, B->A
        # B->A->CANON est valide vis-à-vis d'INV-2 (pas de cycle).
        self.assertNotIn("INV-2", codes(errors_of(recs)))

    def test_fail(self):
        recs = [rec("PLACE-A", same_as="PLACE-B"),
                rec("PLACE-B", same_as="PLACE-A")]   # cycle
        self.assertIn("INV-2", codes(errors_of(recs)))


class TestINV3CanonicalIsFixedPoint(unittest.TestCase):
    def test_pass(self):
        recs = [rec("PLACE-CANON"), rec("PLACE-LEGACY", same_as="PLACE-CANON")]
        self.assertNotIn("INV-3", codes(errors_of(recs)))

    def test_fail(self):
        # La cible PLACE-MID porte elle-même un same_as -> n'est pas un point fixe.
        recs = [rec("PLACE-CANON"),
                rec("PLACE-MID", same_as="PLACE-CANON"),
                rec("PLACE-LEGACY", same_as="PLACE-MID")]
        self.assertIn("INV-3", codes(errors_of(recs)))


class TestINV4UniqueConvergence(unittest.TestCase):
    def test_pass(self):
        recs = [rec("PLACE-CANON"), rec("PLACE-LEGACY", same_as="PLACE-CANON")]
        self.assertNotIn("INV-4", codes(errors_of(recs)))

    def test_fail(self):
        # Cas défensif : same_as multi-valué (hors-schéma) divergeant vers deux
        # canoniques distincts -> équivalence d'identité contradictoire.
        recs = [rec("PLACE-CANON-1"), rec("PLACE-CANON-2"),
                rec("PLACE-LEGACY", same_as=["PLACE-CANON-1", "PLACE-CANON-2"])]
        self.assertIn("INV-4", codes(errors_of(recs)))


class TestRealTJDavidson(unittest.TestCase):
    def test_passing_case(self):
        recs = [
            rec("PLACE-TJ-DAVIDSONS", lat=53.474, lng=-2.249),
            rec("PLACE-S83-001", same_as="PLACE-TJ-DAVIDSONS"),
            rec("PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET", same_as="PLACE-TJ-DAVIDSONS"),
        ]
        errors, _w, repmap = check_same_as(recs)
        self.assertEqual(errors, [], f"attendu aucune erreur, obtenu : {errors}")
        # Les deux legacy résolvent vers le canonique unique.
        self.assertEqual(repmap["PLACE-S83-001"], "PLACE-TJ-DAVIDSONS")
        self.assertEqual(repmap["PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET"], "PLACE-TJ-DAVIDSONS")
        self.assertEqual(repmap["PLACE-TJ-DAVIDSONS"], "PLACE-TJ-DAVIDSONS")  # point fixe


class TestRegionPrecision(unittest.TestCase):
    """B.1 — le palier grossier `region` est accepté par le schéma."""

    def _errs(self, prec):
        return list(VALIDATOR.iter_errors(
            {"id": "PLACE-X", "label": "X", "type": "ville",
             "lat": 53.5, "lng": -2.3, "geo_precision": prec}))

    def test_region_valid(self):
        self.assertEqual(self._errs("region"), [])

    def test_approximative_rejected(self):
        # « approximative » a été retiré de l'énum (granularité ≠ confiance).
        self.assertTrue(self._errs("approximative"))


class TestINV6CoordCollision(unittest.TestCase):
    def test_two_coarse_no_warning(self):
        # B.4 : chevauchement de centroïdes entre zones grossières → toléré.
        recs = [rec("PLACE-A", lat=53.5, lng=-2.3, prec="region"),
                rec("PLACE-B", lat=53.5, lng=-2.3, prec="ville")]
        self.assertEqual(inv6_warnings(recs), [])

    def test_two_precise_no_justification_warns(self):
        recs = [rec("PLACE-A", lat=53.5, lng=-2.3, prec="exacte"),
                rec("PLACE-B", lat=53.5, lng=-2.3, prec="rue")]
        self.assertTrue(inv6_warnings(recs))

    def test_precise_with_justification_no_warning(self):
        # Cas réel Free Trade Hall / Lesser Free Trade Hall (même bâtiment).
        recs = [rec("PLACE-FREE-TRADE-HALL", lat=53.4779, lng=-2.247, prec="exacte"),
                rec("PLACE-LESSER-FREE-TRADE-HALL", lat=53.4779, lng=-2.247,
                    prec="exacte", prud="Petite salle au sein du Free Trade Hall.")]
        self.assertEqual(inv6_warnings(recs), [])

    def test_mixed_precise_coarse_warns(self):
        recs = [rec("PLACE-A", lat=53.5, lng=-2.3, prec="exacte"),
                rec("PLACE-B", lat=53.5, lng=-2.3, prec="ville")]
        self.assertTrue(inv6_warnings(recs))


class TestManchesterNonRegression(unittest.TestCase):
    """MANCHESTER-CITY réconcilié vers MANCHESTER → un seul canonique au
    centroïde, donc aucune collision INV-6 (décision lot B)."""

    def test_reconciled_no_inv6(self):
        recs = [
            rec("PLACE-MANCHESTER", lat=53.4808, lng=-2.2426, prec="ville"),
            rec("PLACE-MANCHESTER-CITY", same_as="PLACE-MANCHESTER"),
            rec("PLACE-GREATER-MANCHESTER", lat=53.59, lng=-2.30, prec="region"),
        ]
        errors, warnings, rep = check_same_as(recs)
        self.assertEqual(errors, [])
        self.assertEqual(rep["PLACE-MANCHESTER-CITY"], "PLACE-MANCHESTER")
        self.assertEqual([w for w in warnings if w.startswith("INV-6")], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
