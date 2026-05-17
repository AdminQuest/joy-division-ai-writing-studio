#!/usr/bin/env python3
"""
Apply the canonical corrected S40 registry patch to data/registre.json.

S40 is restricted to Fortunato M. Cacciatore's article
"...waiting for something to happen..." in Amendola & Barone (dir.),
Our Vision Touched the Sky: Fenomenologia dei Joy Division, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "cacciatore_waiting_for_something_to_happen" / "registre_patch_s40.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S40":
        raise SystemExit("Patch file does not contain id S40")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S40":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S40 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
