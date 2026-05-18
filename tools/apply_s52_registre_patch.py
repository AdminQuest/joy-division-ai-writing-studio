#!/usr/bin/env python3
"""
Apply the canonical S52 registry patch to data/registre.json.

S52 is restricted to Andrea Rabbito's chapter
"Control e l’infrangimento del vetro. Oltre la superficie biografica di Ian Curtis"
in Amendola & Barone (dir.), Our Vision Touched the Sky, Rogas, 2021.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "rabbito_control_infrangimento_vetro" / "registre_patch_s52.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S52":
        raise SystemExit("Patch file does not contain id S52")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S52":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S52 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
