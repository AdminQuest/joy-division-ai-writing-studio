#!/usr/bin/env python3
"""
Apply the canonical S19 registry patch to data/registre.json.

S19 is Pierre Bourdieu, « Les trois états du capital culturel »,
Actes de la recherche en sciences sociales, vol. 30, novembre 1979.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "bourdieu_trois_etats_capital_culturel" / "registre_patch_s19.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S19":
        raise SystemExit("Patch file does not contain id S19")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S19":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S19 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
