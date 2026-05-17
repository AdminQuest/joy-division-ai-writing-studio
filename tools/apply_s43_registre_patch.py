#!/usr/bin/env python3
"""
Apply the canonical S43 registry patch to data/registre.json.

S43 is restricted to Eugenio Capozzi's chapter
"The weight on their shoulders. Ian Curtis e la metamorfosi dei baby boomers"
in Amendola & Barone (dir.), Our Vision Touched the Sky, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "capozzi_weight_on_their_shoulders" / "registre_patch_s43.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S43":
        raise SystemExit("Patch file does not contain id S43")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S43":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S43 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
