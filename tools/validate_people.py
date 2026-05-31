#!/usr/bin/env python3
"""Validate the canonical `PERSON-` register (étape 9).

Porte gate-able : exit 0 si errors == 0, sinon exit 1.

Deux strates coexistent :
  - identité canonique  PERSON-<slug>  (registers/people/00_canonical_people.md)
  - couche provisoire    PERS-*         (registers/people/*.md), réconciliée par
    `same_as` (porté côté canonique) vers son PERSON-.

Invariants (sévérité ERROR sauf mention) :
  INV1 — schéma : tout PERSON- satisfait schemas/person_canonical.schema.json
         (Draft 2020-12) ; `categorie` ∈ vocabulaire fermé.
  INV2 — same_as : toute cible `same_as` résout vers un id PERS-* existant de la
         couche provisoire (people.json) ; un PERSON- est un point fixe (pas de
         same_as vers un autre PERSON-).
  INV3 — partition : chaque PERS-* de people.json est rabattu sur AU PLUS un
         PERSON- (pas de double rattachement) ; couverture exhaustive — tout
         PERS-* est soit dans un `same_as`, soit dans un hand-off (pending_org /
         pending_concept), soit une entrée mixte éclatée déclarée.
  INV4 — unicité : id PERSON- unique ; slug unique.
  INV5 — cas sensibles : PERS-S76-003 (Kevin Curtis) n'est PAS rabattu sur
         PERSON-ian-curtis (jamais fusionné).
  + cohérence SSOT : le registre committé == sortie déterministe du générateur
    (`build_people_canon.py`). Vérifié par --check-drift.

Usage :
    python3 tools/validate_people.py                 # gate (INV1..INV5)
    python3 tools/validate_people.py --check-drift   # gate + sentinelle SSOT
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_against_schema  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CANON_MD = ROOT / "registers" / "people" / "00_canonical_people.md"
PENDING_ORG = ROOT / "registers" / "people" / "pending_org.json"
PENDING_CONCEPT = ROOT / "registers" / "people" / "pending_concept.json"
PEOPLE_JSON = ROOT / "exports" / "generated" / "people.json"
SCHEMA_JSON = ROOT / "schemas" / "person_canonical.schema.json"
GENERATOR = ROOT / "tools" / "build_people_canon.py"

YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

KEVIN_CURTIS_ID = "PERS-S76-003"
IAN_CURTIS_PERSON = "PERSON-ian-curtis"


def iter_canon_blocks():
    for block in YAML_BLOCK.findall(CANON_MD.read_text(encoding="utf-8")):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            yield {"__parse_error__": str(exc)}
            continue
        if isinstance(data, dict):
            yield data


def load_provisional_ids() -> set:
    raw = json.loads(PEOPLE_JSON.read_text(encoding="utf-8"))
    ids = set()
    for rec in raw:
        pid = rec.get("data", {}).get("id", rec.get("id"))
        if pid and str(pid).startswith("PERS-") and not str(pid).startswith("PERSON-"):
            ids.add(pid)
    return ids


def load_handoff_ids() -> set:
    ids = set()
    for path in (PENDING_ORG, PENDING_CONCEPT):
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload.get("items", []):
            fp = item.get("from_pers", "")
            base = fp.split("#")[0]
            if base.startswith("PERS-"):
                ids.add(base)
    return ids


def _maybe_jsonschema_check(records, errors):
    """If jsonschema is available, validate against the Draft 2020-12 contract.

    Optional dependency: absence is not an error (the field-level checks of
    schema_validation already gate the required fields and `categorie`).
    """
    try:
        import jsonschema  # noqa: F401
    except Exception:
        return
    from jsonschema import Draft202012Validator
    schema = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for r in records:
        for err in validator.iter_errors(r):
            errors.append(f"[INV1/jsonschema] {r.get('id','?')}: {err.message}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate canonical PERSON- register.")
    ap.add_argument("--check-drift", action="store_true",
                    help="Sentinelle SSOT : échoue si le registre committé diverge "
                         "de la sortie déterministe du générateur.")
    args = ap.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    if not CANON_MD.exists():
        print(f"ERROR: registre canonique absent : {CANON_MD}", file=sys.stderr)
        return 1

    records = []
    for data in iter_canon_blocks():
        if "__parse_error__" in data:
            errors.append(f"[INV1] YAML parse error: {data['__parse_error__']}")
            continue
        records.append(data)

    # INV4 — unicité id + slug
    seen_ids, seen_slugs = {}, {}
    for r in records:
        pid = r.get("id", "")
        if pid in seen_ids:
            errors.append(f"[INV4] id PERSON- dupliqué : {pid}")
        seen_ids[pid] = True
        slug = pid[len("PERSON-"):] if pid.startswith("PERSON-") else pid
        if slug in seen_slugs:
            errors.append(f"[INV4] slug dupliqué : {slug}")
        seen_slugs[slug] = True

    # INV1 — schéma (champs requis + vocabulaire fermé) via schema_validation
    for r in records:
        for msg in validate_against_schema("person", r):
            errors.append(f"[INV1] {r.get('id','?')}: {msg}")
    _maybe_jsonschema_check(records, errors)

    # INV2/INV3 — same_as : résolution + couverture + non-duplication
    provisional = load_provisional_ids()
    handoff = load_handoff_ids()
    rattaches: dict[str, str] = {}
    for r in records:
        pid = r.get("id", "")
        for sa in r.get("same_as", []) or []:
            base = sa.split("#")[0]
            if sa.startswith("PERSON-"):
                errors.append(f"[INV2] {pid}: same_as pointe vers un PERSON- ({sa}) — interdit (point fixe).")
                continue
            if base not in provisional:
                errors.append(f"[INV2] {pid}: same_as {sa} ne résout vers aucun PERS-* de people.json.")
            if base in rattaches and rattaches[base] != pid:
                errors.append(f"[INV3] {base} rabattu sur deux PERSON- : {rattaches[base]} et {pid}.")
            rattaches[base] = pid

    # INV3 — couverture exhaustive de la couche provisoire
    accounted = set(rattaches) | handoff | {"PERS-S76-052", "PERS-S76-064"}
    uncovered = sorted(provisional - accounted)
    for pid in uncovered:
        errors.append(f"[INV3] PERS-* non couvert (ni same_as, ni hand-off, ni éclatement) : {pid}")
    phantom = sorted(set(rattaches) - provisional)
    for pid in phantom:
        errors.append(f"[INV3] same_as fantôme (absent de people.json) : {pid}")

    # INV5 — cas sensible Kevin Curtis
    if rattaches.get(KEVIN_CURTIS_ID) == IAN_CURTIS_PERSON:
        errors.append(f"[INV5] {KEVIN_CURTIS_ID} (Kevin Curtis) rabattu sur {IAN_CURTIS_PERSON} — INTERDIT.")

    # Sentinelle SSOT
    if args.check_drift:
        proc = subprocess.run([sys.executable, str(GENERATOR), "--to-stdout"],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            errors.append(f"[SSOT] le générateur a échoué : {proc.stderr.strip()[:300]}")
        elif proc.stdout != CANON_MD.read_text(encoding="utf-8"):
            errors.append("[SSOT] DRIFT : 00_canonical_people.md diffère de la sortie "
                          "déterministe de build_people_canon.py. Régénérer puis committer.")

    # Rapport
    print(f"PERSON- canoniques : {len(records)}")
    print(f"PERS-* provisoires : {len(provisional)} | rabattus : {len(rattaches)} | "
          f"hand-off : {len(handoff)} | mixtes éclatés : 2")
    print(f"errors   : {len(errors)}")
    print(f"warnings : {len(warnings)}")
    if warnings:
        for w in warnings[:50]:
            print(f"  - WARNING {w}")
    if errors:
        for e in errors[:100]:
            print(f"  - ERROR {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
