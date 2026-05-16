#!/usr/bin/env python3
"""
Applique le patch canonique S12 au registre principal.

Usage :
  python3 tools/apply_s12_registre_patch.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRE = REPO_ROOT / "data" / "registre.json"
PATCH = REPO_ROOT / "sources" / "press_aids_anderton_1986" / "registre_patch_s12.json"


def main() -> None:
    registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))

    if not isinstance(registre, list):
        raise SystemExit("data/registre.json doit contenir une liste JSON")
    if patch.get("id") != "S12":
        raise SystemExit("Le patch ne cible pas S12")

    updated = False
    for i, entry in enumerate(registre):
        if isinstance(entry, dict) and entry.get("id") == "S12":
            merged = dict(entry)
            merged.update(patch)
            registre[i] = merged
            updated = True
            break

    if not updated:
        registre.insert(11, patch)

    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("S12 registre patch applied")


if __name__ == "__main__":
    main()
