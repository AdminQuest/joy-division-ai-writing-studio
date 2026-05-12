#!/usr/bin/env python3
"""
Mark empty register YAML templates as schema blocks.

The remaining unknown YAML blocks are not documentary records. They are empty
schema examples in:

- registers/people/master_people.md
- registers/chronology/master_chronology.md

Adding a top-level 'schema:' key makes build_registers.py classify them as
schema blocks and skip them from documentary records.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATCHES = [
    (
        ROOT / "registers" / "people" / "master_people.md",
        "```yaml\nid:\nname:\nfull_name:\nrole:",
        "```yaml\nschema: person_template\nid:\nname:\nfull_name:\nrole:",
    ),
    (
        ROOT / "registers" / "chronology" / "master_chronology.md",
        "```yaml\nid:\ndate:\nprecision_date:\nevent:",
        "```yaml\nschema: chronology_template\nid:\ndate:\nprecision_date:\nevent:",
    ),
]


def main() -> int:
    changed = 0
    for path, old, new in PATCHES:
        text = path.read_text(encoding="utf-8")
        if new in text:
            print(f"Already patched: {path.relative_to(ROOT)}")
            continue
        if old not in text:
            raise SystemExit(f"Pattern not found in {path.relative_to(ROOT)}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"Patched: {path.relative_to(ROOT)}")
        changed += 1
    print(f"Register templates patched: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
