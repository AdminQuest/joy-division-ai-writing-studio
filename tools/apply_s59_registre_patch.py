#!/usr/bin/env python3
"""
Apply the canonical S59 registry patch to data/registre.json.

S59 is Francesca Ferrara, « Joy Division: una poetica della distanza »,
in Amendola & Barone (dir.), Our Vision Touched the Sky, Rogas, 2021.

The user initially requested S57 for this source, but S57 is already fixed
for Massimo Villani. This script therefore preserves canonical stability and
applies Ferrara as S59.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "ferrara_poetica_della_distanza" / "registre_patch_s59.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S59":
        raise SystemExit("Patch file does not contain id S59")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S59":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S59 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
