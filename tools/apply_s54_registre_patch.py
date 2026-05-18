#!/usr/bin/env python3
"""
Apply the canonical S54 registry patch to data/registre.json.

S54 is restricted to Alessandro Gnocchi's chapter
"Interzona. Burroughs e Ballard nei testi di Ian Curtis"
in Amendola & Barone (dir.), Our Vision Touched the Sky, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "gnocchi_interzona_burroughs_ballard" / "registre_patch_s54.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S54":
        raise SystemExit("Patch file does not contain id S54")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S54":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S54 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
