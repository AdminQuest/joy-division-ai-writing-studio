#!/usr/bin/env python3
"""
Apply the canonical S21 registry patch to data/registre.json.

S21 is the Manchester Digital Music Archive exhibition page
« City Fun: The Hidden History of Manchester's Favourite Fanzine ».
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "mdmarchive_city_fun_hidden_history" / "registre_patch_s21.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S21":
        raise SystemExit("Patch file does not contain id S21")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S21":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S21 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
