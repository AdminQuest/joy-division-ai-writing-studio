#!/usr/bin/env python3
"""
Apply the canonical S78 registry patch to data/registre.json.

S78 is Leonard Nevarez, « How Joy Division Came to Sound Like Manchester:
Myth and Ways of Listening in the Neoliberal City », Journal of Popular Music
Studies, vol. 25, no. 1, 2013.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "nevarez_how_joy_division_came_to_sound_like_manchester" / "registre_patch_s78.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S78":
        raise SystemExit("Patch file does not contain id S78")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S78":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S78 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
