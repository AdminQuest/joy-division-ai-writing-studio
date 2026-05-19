#!/usr/bin/env python3
"""
Apply the canonical S55 registry patch to data/registre.json.

S55 is Vincenzo Romania, « A guide to come: i Joy Division come universo
simbolico. Una ricerca sulle recensioni musicali », in Amendola & Barone
(dir.), Our Vision Touched the Sky, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "romania_a_guide_to_come_universo_simbolico" / "registre_patch_s55.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S55":
        raise SystemExit("Patch file does not contain id S55")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S55":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S55 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
