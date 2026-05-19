#!/usr/bin/env python3
"""
Apply the canonical S58 registry patch to data/registre.json.

S58 is Emiliano Ilardi, « Ian Curtis is not dead. Dalla Factory Records
ai rave nelle factories », in Amendola & Barone (dir.), Our Vision Touched
the Sky, Rogas, 2021.

S57 remains reserved for Massimo Villani.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "ilardi_ian_curtis_is_not_dead" / "registre_patch_s58.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S58":
        raise SystemExit("Patch file does not contain id S58")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S58":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S58 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
