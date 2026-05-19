#!/usr/bin/env python3
"""
Fix known accidental YAML indentation slips in S78 integration files.

Safe and idempotent. Run before build_registers.py when S78 has just been pulled.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "sources" / "nevarez_how_joy_division_came_to_sound_like_manchester" / "source_part_01.md",
    ROOT / "registers" / "s78_nevarez_structuring_registers.md",
    ROOT / "registers" / "s78_nevarez_specialized_registers.md",
]
REPLACEMENTS = {
    "\n titre:": "\ntitre:",
    "\n definition:": "\ndefinition:",
    "\n deconstruction:": "\ndeconstruction:",
}


def main() -> int:
    changed = 0
    for path in TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        fixed = text
        for old, new in REPLACEMENTS.items():
            fixed = fixed.replace(old, new)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            changed += 1
            print(f"fixed: {path.relative_to(ROOT)}")
    print(f"S78 YAML indentation cleanup complete; changed {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
