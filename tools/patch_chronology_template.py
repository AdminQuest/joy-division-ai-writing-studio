#!/usr/bin/env python3
"""
Mark the chronology register YAML template as a schema block.

The chronology template contains blank lines between top-level keys, so the first
patch_register_templates.py pattern was too narrow.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "registers" / "chronology" / "master_chronology.md"

OLD = "```yaml\nid:\ndate:\nprecision_date:\n\nevent:"
NEW = "```yaml\nschema: chronology_template\nid:\ndate:\nprecision_date:\n\nevent:"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")
    if NEW in text:
        print("Already patched: registers/chronology/master_chronology.md")
        return 0
    if OLD not in text:
        raise SystemExit("Pattern not found in registers/chronology/master_chronology.md")
    TARGET.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("Patched: registers/chronology/master_chronology.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
