#!/usr/bin/env python3
"""Validate the canonical `IMAGE-` register (etape 11).

Gate-able: exit 0 if errors == 0, else exit 1.

Invariants (severity ERROR unless noted):
  INV1 -- uniqueness: image_id unique across the register.
  INV2 -- session_ref: every level="image" entry has a session_ref
          pointing to an existing level="session" entry in the same file.
  INV3 -- photographer: photographer field references a PERSON- identifier.
  INV4 -- date format: date respects ISO 8601 when date_precision is
          "day" (YYYY-MM-DD) or "month" (YYYY-MM).
  INV5 -- identity_frozen: always true for validated entries.
  INV6 -- gate: must be "public" or "private".

Usage:
    python3 tools/validate_images.py              # gate (INV1..INV6)
    python3 tools/validate_images.py --verbose    # detailed output
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_JSON = ROOT / "registers" / "images" / "images.json"
SCHEMA_JSON = ROOT / "schemas" / "image_canonical.schema.json"

CURRENT_DRIFT_VERSION = "v1.0"

VALID_LEVELS = {"session", "image", "image_reference"}
VALID_CONTEXTS = {"promo", "live", "portrait", "artwork", "rehearsal", "other"}
VALID_PRECISIONS = {"day", "month", "year", "approximate", "unknown"}
VALID_GATES = {"public", "private"}
VALID_STATUSES = {"canonical", "reference_only"}
VALID_RIGHTS_STATUSES = {"known", "unknown", "restricted"}

IMAGE_ID_RE = re.compile(r"^(IMAGE-(S|I)-[0-9]{4}|IMAGE-FB-[0-9]+)$")
SESSION_ID_RE = re.compile(r"^IMAGE-S-[0-9]{4}$")
IMAGE_LEVEL_ID_RE = {
    "session": re.compile(r"^IMAGE-S-[0-9]{4}$"),
    "image": re.compile(r"^IMAGE-I-[0-9]{4}$"),
    "image_reference": re.compile(r"^IMAGE-FB-[0-9]+$"),
}
PERSON_RE = re.compile(r"^PERSON-[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
DATE_YEAR_RE = re.compile(r"^\d{4}$")
DRIFT_RE = re.compile(r"^v\d+\.\d+$")
LAST_VERIFIED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_entry(entry: dict, idx: int, session_ids: set[str]) -> list[str]:
    errors = []
    iid = entry.get("image_id", f"<entry {idx}>")

    required = [
        "image_id", "level", "canonical_name", "photographer",
        "date", "date_precision", "subjects", "sources",
        "same_as", "identity_frozen", "drift_sentinel", "gate", "last_verified"
    ]
    for field in required:
        if field not in entry:
            errors.append(f"[INV1] {iid}: missing required field '{field}'")

    if "image_id" in entry and not IMAGE_ID_RE.match(str(entry["image_id"])):
        errors.append(f"[INV1] {iid}: image_id does not match IMAGE-(S|I)-NNNN or IMAGE-FB-NNNN pattern")

    level = entry.get("level")
    if level and level not in VALID_LEVELS:
        errors.append(f"[INV1] {iid}: invalid level '{level}'")
    elif level:
        expected_id_re = IMAGE_LEVEL_ID_RE[level]
        if "image_id" in entry and not expected_id_re.match(str(entry["image_id"])):
            errors.append(f"[INV1] {iid}: level='{level}' has incompatible image_id '{entry['image_id']}'")

    if not entry.get("canonical_name"):
        errors.append(f"[INV1] {iid}: canonical_name is empty")

    context = entry.get("context")
    if context and context not in VALID_CONTEXTS:
        errors.append(f"[INV1] {iid}: invalid context '{context}'")

    precision = entry.get("date_precision")
    if precision and precision not in VALID_PRECISIONS:
        errors.append(f"[INV1] {iid}: invalid date_precision '{precision}'")

    gate = entry.get("gate")
    if gate and gate not in VALID_GATES:
        errors.append(f"[INV6] {iid}: invalid gate '{gate}'")

    status = entry.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(f"[INV1] {iid}: invalid status '{status}'")

    rights_status = entry.get("rights_status")
    if rights_status and rights_status not in VALID_RIGHTS_STATUSES:
        errors.append(f"[INV1] {iid}: invalid rights_status '{rights_status}'")

    if level == "image_reference":
        if not str(entry.get("image_id", "")).startswith("IMAGE-FB-"):
            errors.append(f"[INV1] {iid}: level='image_reference' expects an IMAGE-FB-* identifier")
        if entry.get("status") != "reference_only":
            errors.append(f"[INV1] {iid}: level='image_reference' expects status='reference_only'")
        if not entry.get("source_url"):
            errors.append(f"[INV1] {iid}: level='image_reference' expects source_url")
        if entry.get("local_file") is not None:
            errors.append(f"[INV1] {iid}: level='image_reference' must not define a local_file")

    # INV2 -- session_ref validity
    if level == "image":
        sr = entry.get("session_ref")
        if not sr:
            errors.append(f"[INV2] {iid}: level='image' but session_ref is missing or null")
        elif not SESSION_ID_RE.match(str(sr)):
            errors.append(f"[INV2] {iid}: session_ref '{sr}' does not match IMAGE-S-NNNN pattern")
        elif sr not in session_ids:
            errors.append(f"[INV2] {iid}: session_ref '{sr}' not found among session entries")

    # INV3 -- photographer PERSON- cross-check
    photographer = entry.get("photographer")
    if photographer and not PERSON_RE.match(str(photographer)):
        errors.append(f"[INV3] {iid}: photographer '{photographer}' does not match PERSON- pattern")

    # INV4 -- date format vs precision
    date = entry.get("date")
    if date and precision:
        if precision == "day" and not DATE_DAY_RE.match(str(date)):
            errors.append(f"[INV4] {iid}: date '{date}' does not match YYYY-MM-DD for precision 'day'")
        elif precision == "month" and not DATE_MONTH_RE.match(str(date)):
            errors.append(f"[INV4] {iid}: date '{date}' does not match YYYY-MM for precision 'month'")
        elif precision == "year" and not DATE_YEAR_RE.match(str(date)):
            errors.append(f"[INV4] {iid}: date '{date}' does not match YYYY for precision 'year'")

    # INV5 -- identity_frozen
    if entry.get("identity_frozen") is not True:
        errors.append(f"[INV5] {iid}: identity_frozen must be true")

    # same_as coherence
    same_as = entry.get("same_as", {})
    if isinstance(same_as, dict):
        wikidata = same_as.get("wikidata")
        if wikidata and not re.match(r"^Q\d+$", str(wikidata)):
            errors.append(f"[INV1] {iid}: wikidata ID '{wikidata}' does not match Q-number pattern")
    elif same_as is not None:
        errors.append(f"[INV1] {iid}: same_as must be an object")

    # sources non-empty
    sources = entry.get("sources")
    if sources is not None:
        if not isinstance(sources, list) or len(sources) < 1:
            errors.append(f"[INV1] {iid}: sources must be a non-empty array")

    # drift_sentinel
    ds = entry.get("drift_sentinel")
    if ds:
        if not DRIFT_RE.match(str(ds)):
            errors.append(f"[INV1] {iid}: drift_sentinel '{ds}' does not match vN.N pattern")
        elif ds != CURRENT_DRIFT_VERSION:
            errors.append(f"[INV1] {iid}: drift_sentinel '{ds}' != current '{CURRENT_DRIFT_VERSION}'")

    # last_verified format
    lv = entry.get("last_verified")
    if lv and not LAST_VERIFIED_RE.match(str(lv)):
        errors.append(f"[INV1] {iid}: last_verified '{lv}' is not YYYY-MM-DD")

    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate canonical IMAGE- register.")
    ap.add_argument("--verbose", action="store_true", help="Detailed output.")
    args = ap.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    if not IMAGES_JSON.exists():
        print(f"ERROR: canonical register absent: {IMAGES_JSON}", file=sys.stderr)
        return 1

    try:
        records = load_json(IMAGES_JSON)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: cannot parse {IMAGES_JSON}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(records, list):
        print("ERROR: images.json root must be an array", file=sys.stderr)
        return 1

    session_ids = {
        e.get("image_id") for e in records if e.get("level") == "session"
    }

    for idx, entry in enumerate(records):
        errors.extend(validate_entry(entry, idx, session_ids))

    # INV1 -- uniqueness
    seen_ids: dict[str, bool] = {}
    for entry in records:
        iid = entry.get("image_id", "")
        if iid in seen_ids:
            errors.append(f"[INV1] duplicate image_id: {iid}")
        seen_ids[iid] = True

    # Optional: jsonschema validation with FormatChecker
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        schema = load_json(SCHEMA_JSON)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for entry in records:
            for err in validator.iter_errors(entry):
                errors.append(f"[INV1/jsonschema] {entry.get('image_id', '?')}: {err.message}")
    except ImportError:
        if args.verbose:
            print("INFO: jsonschema not installed, skipping Draft 2020-12 validation")

    # Report
    sessions = [e for e in records if e.get("level") == "session"]
    images = [e for e in records if e.get("level") == "image"]
    references = [e for e in records if e.get("level") == "image_reference"]
    gates = {"public": 0, "private": 0}
    for entry in records:
        g = entry.get("gate", "unknown")
        if g in gates:
            gates[g] += 1

    print(f"IMAGE- canoniques : {len(records)} ({len(sessions)} sessions, {len(images)} images, {len(references)} references)")
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
