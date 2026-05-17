#!/usr/bin/env python3
"""
Apply the canonical S48 registry patch to data/registre.json.

S48 is restricted to Alfredo De Sia's chapter
"Il segno, la grafica, la visione"
in Amendola & Barone (dir.), Our Vision Touched the Sky, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "desia_segno_grafica_visione" / "registre_patch_s48.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S48":
        raise SystemExit("Patch file does not contain id S48")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S48":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S48 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
