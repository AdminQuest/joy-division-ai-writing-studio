#!/usr/bin/env python3
"""
Apply the canonical S39 registry patch to data/registre.json.

This script replaces the existing S39 entry, preserving the order of the registry.
It is intentionally source-specific, following the repository pattern already used
for canonical source corrections.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "bauman_liquid_modernity" / "registre_patch_s39.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S39":
        raise SystemExit("Patch file does not contain id S39")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S39":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S39 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
