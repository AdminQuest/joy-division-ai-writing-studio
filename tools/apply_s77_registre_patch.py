#!/usr/bin/env python3
"""
Apply the canonical S77 registry patch to data/registre.json.

S77 is Matthew Worley, « ‘While the world was dying, did you wonder why?’:
Punk, Politics and British (fan)zines, 1976–84 », History Workshop Journal,
vol. 79, no. 1, 2015.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "registre.json"
PATCH_PATH = ROOT / "sources" / "worley_punk_politics_british_fanzines" / "registre_patch_s77.json"


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    patch = json.loads(PATCH_PATH.read_text(encoding="utf-8"))

    if patch.get("id") != "S77":
        raise SystemExit("Patch file does not contain id S77")

    replaced = False
    for index, entry in enumerate(registry):
        if entry.get("id") == "S77":
            registry[index] = patch
            replaced = True
            break

    if not replaced:
        registry.append(patch)

    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("S77 registry entry applied to data/registre.json")


if __name__ == "__main__":
    main()
