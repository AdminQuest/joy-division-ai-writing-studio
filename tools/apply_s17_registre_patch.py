#!/usr/bin/env python3
"""
Apply the canonical S17 registry patch to data/registre.json.

S17 is the Wikipedia page « Rowche Rumble », used only as a tertiary
orientation source for The Fall's 1979 single.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "wikipedia_rowche_rumble" / "registre_patch_s17.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S17":
        raise SystemExit("Patch file does not contain id S17")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S17":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("S17 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
