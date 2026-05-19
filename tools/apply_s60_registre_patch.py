#!/usr/bin/env python3
"""
Apply the canonical S60 registry patch to data/registre.json.

S60 is Raffaele Federici, « Unknown Pleasures: Pulsar di una t-shirt
iconica », in Amendola & Barone (dir.), Our Vision Touched the Sky,
Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "federici_unknown_pleasures_pulsar_tshirt" / "registre_patch_s60.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S60":
        raise SystemExit("Patch file does not contain id S60")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S60":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S60 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
