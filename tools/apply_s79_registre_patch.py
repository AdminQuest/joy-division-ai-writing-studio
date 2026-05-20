#!/usr/bin/env python3
"""
Apply the canonical S79 registry patch to data/registre.json.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "curtis_savage_so_this_is_permanence" / "registre_patch_s79.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S79":
        raise SystemExit("Patch file does not contain id S79")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S79":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S79 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
