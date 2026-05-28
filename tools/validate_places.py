#!/usr/bin/env python3
"""Validate the places register against schemas/places.schema.yaml.

Replicates the runtime pipeline of apps/lib/dynamic-registers.js:
  1. parse every YAML block under registers/**.md
  2. keep place records (places: container items + standalone PLACE-* blocks)
  3. drop document-header parasites (type_unite present and != "place")
  4. validate each source record against the JSON Schema (Draft 2020-12,
     FormatChecker active)
  5. report the distinct count after id-deduplication (what the UI displays)

Usage: python3 tools/validate_places.py
Exit code 1 if any record is invalid.
"""
import glob
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "schemas" / "places.schema.yaml").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def is_place(record: dict, path: str) -> bool:
    return str(record.get("id", "")).startswith("PLACE-") or "/places/" in path.replace("\\", "/")


def is_parasite(record: dict) -> bool:
    tu = record.get("type_unite")
    return tu is not None and tu != "place"


def collect_records():
    records = []
    for path in sorted(glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True)):
        rel = path.replace(str(ROOT) + "/", "")
        for block in YAML_BLOCK.findall(Path(path).read_text(encoding="utf-8")):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                continue
            if not isinstance(data, dict):
                continue
            items = data["places"] if isinstance(data.get("places"), list) else (
                [data] if str(data.get("id", "")).startswith("PLACE-") else []
            )
            for item in items:
                if isinstance(item, dict) and is_place(item, rel) and not is_parasite(item):
                    records.append((item, rel))
    return records


def main() -> int:
    records = collect_records()
    invalid = []
    for record, rel in records:
        errors = sorted(VALIDATOR.iter_errors(record), key=str)
        if errors:
            invalid.append((record.get("id"), rel, [e.message for e in errors]))

    distinct_ids = {r.get("id") for r, _ in records}

    print(f"Source place records (parasites excluded) : {len(records)}")
    print(f"Distinct places after id-deduplication     : {len(distinct_ids)}")
    print(f"Valid against schema                        : {len(records) - len(invalid)}/{len(records)}")

    if invalid:
        print(f"\nINVALID ({len(invalid)}):")
        for pid, rel, msgs in invalid:
            print(f"  {pid}  ({rel})")
            for m in msgs:
                print(f"       - {m}")
        return 1

    print("\nAll place records are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
