#!/usr/bin/env python3
"""
Applique le patch canonique S05 au registre principal.

Usage :
  python3 tools/apply_s05_registre_patch.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRE = REPO_ROOT / "data" / "registre.json"
PATCH = REPO_ROOT / "sources" / "jeffery_tufail_jackson_policing" / "registre_patch_s05.json"


def main() -> None:
    registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))

    if not isinstance(registre, list):
        raise SystemExit("data/registre.json doit contenir une liste JSON")
    if patch.get("id") != "S05":
        raise SystemExit("Le patch ne cible pas S05")

    updated = False
    for i, entry in enumerate(registre):
        if isinstance(entry, dict) and entry.get("id") == "S05":
            merged = dict(entry)
            merged.update(patch)
            registre[i] = merged
            updated = True
            break

    if not updated:
        registre.insert(4, patch)

    REGISTRE.write_text(json.dumps(registre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("S05 registre patch applied")


if __name__ == "__main__":
    main()
