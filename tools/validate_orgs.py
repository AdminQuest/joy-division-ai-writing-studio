#!/usr/bin/env python3
"""Validate the canonical `ORG-` register (etape 10).

Gate-able: exit 0 if errors == 0, else exit 1.

Invariants (severity ERROR unless noted):
  INV1 -- schema: every ORG- satisfies schemas/organization_canonical.schema.json
          (Draft 2020-12); `category` and `status` within closed vocabularies.
  INV2 -- uniqueness: org_id unique across the register.
  INV3 -- identity_frozen: always true for validated entries.
  INV4 -- same_as coherence: wikidata IDs match Q-number pattern; no duplicates
          across entries.
  INV5 -- drift_sentinel: all entries share the current schema version.
  INV6 -- provenance: every entry traces back to pending_org.json or has
          documented provenance.

Usage:
    python3 tools/validate_orgs.py              # gate (INV1..INV6)
    python3 tools/validate_orgs.py --verbose    # detailed output
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORGS_JSON = ROOT / "registers" / "orgs" / "orgs.json"
SCHEMA_JSON = ROOT / "schemas" / "organization_canonical.schema.json"
PENDING_ORG = ROOT / "registers" / "people" / "pending_org.json"

CURRENT_DRIFT_VERSION = "v1.0"

VALID_CATEGORIES = {"group", "label", "institution", "venue_org", "crew", "media", "other"}
VALID_STATUSES = {"active", "dissolved", "dormant", "unknown"}
VALID_GATES = {"public", "private"}
ORG_ID_RE = re.compile(r"^ORG-\d{4}$")
WIKIDATA_RE = re.compile(r"^Q\d+$")
COUNTRY_RE = re.compile(r"^[A-Z]{2}$")
DRIFT_RE = re.compile(r"^v\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_entry(entry: dict, idx: int) -> list[str]:
    errors = []
    oid = entry.get("org_id", f"<entry {idx}>")

    # Required fields
    required = [
        "org_id", "canonical_name", "aliases", "category", "country",
        "status", "same_as", "joy_division_relation", "sources",
        "identity_frozen", "drift_sentinel", "gate", "last_verified"
    ]
    for field in required:
        if field not in entry:
            errors.append(f"[INV1] {oid}: missing required field '{field}'")

    # org_id format
    if "org_id" in entry and not ORG_ID_RE.match(str(entry["org_id"])):
        errors.append(f"[INV1] {oid}: org_id does not match ORG-NNNN pattern")

    # canonical_name non-empty
    if not entry.get("canonical_name"):
        errors.append(f"[INV1] {oid}: canonical_name is empty")

    # category enum
    cat = entry.get("category")
    if cat and cat not in VALID_CATEGORIES:
        errors.append(f"[INV1] {oid}: invalid category '{cat}'")

    # status enum
    status = entry.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(f"[INV1] {oid}: invalid status '{status}'")

    # gate enum
    gate = entry.get("gate")
    if gate and gate not in VALID_GATES:
        errors.append(f"[INV1] {oid}: invalid gate '{gate}'")

    # country format
    country = entry.get("country")
    if country and not COUNTRY_RE.match(str(country)):
        errors.append(f"[INV1] {oid}: country '{country}' is not ISO 3166-1 alpha-2")

    # aliases must be array
    aliases = entry.get("aliases")
    if aliases is not None and not isinstance(aliases, list):
        errors.append(f"[INV1] {oid}: aliases must be an array")

    # sources must be non-empty array
    sources = entry.get("sources")
    if sources is not None:
        if not isinstance(sources, list) or len(sources) < 1:
            errors.append(f"[INV1] {oid}: sources must be a non-empty array")

    # INV3 -- identity_frozen
    if entry.get("identity_frozen") is not True:
        errors.append(f"[INV3] {oid}: identity_frozen must be true")

    # INV4 -- same_as coherence
    same_as = entry.get("same_as", {})
    if isinstance(same_as, dict):
        wikidata = same_as.get("wikidata")
        if wikidata and not WIKIDATA_RE.match(str(wikidata)):
            errors.append(f"[INV4] {oid}: wikidata ID '{wikidata}' does not match Q-number pattern")
    else:
        errors.append(f"[INV1] {oid}: same_as must be an object")

    # joy_division_relation structure
    jdr = entry.get("joy_division_relation")
    if isinstance(jdr, dict):
        if "type" not in jdr:
            errors.append(f"[INV1] {oid}: joy_division_relation.type is required")
    elif jdr is not None:
        errors.append(f"[INV1] {oid}: joy_division_relation must be an object")

    # INV5 -- drift_sentinel
    ds = entry.get("drift_sentinel")
    if ds:
        if not DRIFT_RE.match(str(ds)):
            errors.append(f"[INV5] {oid}: drift_sentinel '{ds}' does not match vN.N pattern")
        elif ds != CURRENT_DRIFT_VERSION:
            errors.append(f"[INV5] {oid}: drift_sentinel '{ds}' != current '{CURRENT_DRIFT_VERSION}'")

    # last_verified format
    lv = entry.get("last_verified")
    if lv and not DATE_RE.match(str(lv)):
        errors.append(f"[INV1] {oid}: last_verified '{lv}' is not YYYY-MM-DD")

    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate canonical ORG- register.")
    ap.add_argument("--verbose", action="store_true", help="Detailed output.")
    args = ap.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    if not ORGS_JSON.exists():
        print(f"ERROR: canonical register absent: {ORGS_JSON}", file=sys.stderr)
        return 1

    try:
        records = load_json(ORGS_JSON)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: cannot parse {ORGS_JSON}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(records, list):
        print("ERROR: orgs.json root must be an array", file=sys.stderr)
        return 1

    # Per-entry validation
    for idx, entry in enumerate(records):
        errors.extend(validate_entry(entry, idx))

    # INV2 -- uniqueness
    seen_ids = {}
    seen_wikidata = {}
    for entry in records:
        oid = entry.get("org_id", "")
        if oid in seen_ids:
            errors.append(f"[INV2] duplicate org_id: {oid}")
        seen_ids[oid] = True

        wikidata = (entry.get("same_as") or {}).get("wikidata")
        if wikidata:
            if wikidata in seen_wikidata:
                errors.append(f"[INV4] duplicate wikidata ID {wikidata}: "
                              f"{seen_wikidata[wikidata]} and {oid}")
            seen_wikidata[wikidata] = oid

    # INV6 -- provenance check against pending_org.json
    if PENDING_ORG.exists():
        try:
            pending = load_json(PENDING_ORG)
            pending_names = {item["name"] for item in pending.get("items", [])}
            for entry in records:
                name = entry.get("canonical_name", "")
                if name not in pending_names:
                    warnings.append(f"[INV6] {entry.get('org_id', '?')}: '{name}' "
                                    f"not found in pending_org.json (may be manually added)")
        except Exception:
            warnings.append("[INV6] could not load pending_org.json for provenance check")

    # Optional: jsonschema validation
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
        schema = load_json(SCHEMA_JSON)
        validator = Draft202012Validator(schema)
        for entry in records:
            for err in validator.iter_errors(entry):
                errors.append(f"[INV1/jsonschema] {entry.get('org_id', '?')}: {err.message}")
    except ImportError:
        if args.verbose:
            print("INFO: jsonschema not installed, skipping Draft 2020-12 validation")

    # Report
    categories = {}
    gates = {"public": 0, "private": 0}
    for entry in records:
        cat = entry.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
        g = entry.get("gate", "unknown")
        if g in gates:
            gates[g] += 1

    print(f"ORG- canoniques : {len(records)}")
    print(f"  categories : {categories}")
    print(f"  gates      : {gates}")
    print(f"  errors     : {len(errors)}")
    print(f"  warnings   : {len(warnings)}")

    if args.verbose or warnings:
        for w in warnings[:50]:
            print(f"  - WARNING {w}")
    if errors:
        for e in errors[:100]:
            print(f"  - ERROR {e}", file=sys.stderr)
        return 1

    print("PASS: all invariants satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
