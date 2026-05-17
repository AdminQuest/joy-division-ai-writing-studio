#!/usr/bin/env python3
"""
Apply the canonical S35 registry patch to data/registre.json.

S35 is restricted to Stephen Morris's memoir
Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I
(Constable, 2019).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "morris_record_play_pause" / "registre_patch_s35.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S35":
        raise SystemExit("Patch file does not contain id S35")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S35":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S35 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
