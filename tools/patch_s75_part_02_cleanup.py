#!/usr/bin/env python3
"""Cleanup patch for S75 part 2 atomization.

Fixes two YAML indentation typos and canonicalizes the candidate
`CONCEPT-mass-produced-secret` target to CONCEPT-007.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "sources" / "ott_unknown_pleasures" / "source_part_02.md"

REPLACEMENTS = {
    "type_unite: archive\n titre: Granada TV": "type_unite: archive\ntitre: Granada TV",
    "type_unite: concept\n titre: Unknown Pleasures": "type_unite: concept\ntitre: Unknown Pleasures",
    "type: prépare\n    cible: CONCEPT-mass-produced-secret\n    note: \"Concept candidat à créer si plusieurs atomes traitent la diffusion comme secret communautaire.\"": "type: prolonge\n    cible: CONCEPT-007\n    note: \"Prolonge le concept de secret produit en masse pour penser la diffusion initiale d'Unknown Pleasures.\"",
}


def main() -> int:
    if not TARGET.exists():
        print(f"File not found: {TARGET}")
        return 1
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            changed += 1
        else:
            print(f"Pattern not found or already patched: {old[:80]!r}")
    TARGET.write_text(text, encoding="utf-8")
    print(f"S75 part 2 cleanup applied: {changed} replacement(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
