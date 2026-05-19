#!/usr/bin/env python3
"""
Apply the canonical S07 registry patch to data/registre.json.

S07 is Friedrich Engels, The Condition of the Working Class in England,
first published in Leipzig in 1845, using the provided English working PDF.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "engels_condition_working_class_england" / "registre_patch_s07.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S07":
        raise SystemExit("Patch file does not contain id S07")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S07":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S07 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
