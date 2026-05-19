#!/usr/bin/env python3
"""
Apply the canonical S08 registry patch to data/registre.json.

S08 is restricted to Internationale situationniste, n° 2, décembre 1958,
for the passages on psychogeography and dérive: Khatib, « Essai de description
psychogéographique des Halles », and Debord, « Théorie de la dérive ».
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "internationale_situationniste_2_psychogeographie_derive" / "registre_patch_s08.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S08":
        raise SystemExit("Patch file does not contain id S08")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S08":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S08 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
