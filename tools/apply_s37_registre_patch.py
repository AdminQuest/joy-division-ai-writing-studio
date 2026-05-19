#!/usr/bin/env python3
"""
Apply the canonical S37 registry patch to data/registre.json.

S37 is Paul Morley, Joy Division: Piece by Piece: Writing About Joy
Division 1977–2007, Plexus, 2008.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "morley_piece_by_piece" / "registre_patch_s37.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S37":
        raise SystemExit("Patch file does not contain id S37")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S37":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S37 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
