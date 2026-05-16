#!/usr/bin/env python3
"""
Applique le patch canonique S09 au registre principal.

Usage :
  python3 tools/apply_s09_registre_patch.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRE = REPO_ROOT / "data" / "registre.json"
PATCH = REPO_ROOT / "sources" / "cummins_joy_division_visual_corpus" / "registre_patch_s09.json"


def main() -> None:
    registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))

    if not isinstance(registre, list):
        raise SystemExit("data/registre.json doit contenir une liste JSON")
    if patch.get("id") != "S09":
        raise SystemExit("Le patch ne cible pas S09")

    updated = False
    for i, entry in enumerate(registre):
        if isinstance(entry, dict) and entry.get("id") == "S09":
            merged = dict(entry)
            merged.update(patch)
            registre[i] = merged
            updated = True
            break

    if not updated:
        registre.insert(8, patch)

    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("S09 registre patch applied")


if __name__ == "__main__":
    main()
