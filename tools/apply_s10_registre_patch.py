#!/usr/bin/env python3
"""
Applique le patch canonique S10 au registre principal.

Usage :
  python3 tools/apply_s10_registre_patch.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRE = REPO_ROOT / "data" / "registre.json"
PATCH = REPO_ROOT / "sources" / "sumner_chapter_and_verse" / "registre_patch_s10.json"
REDIRECTS = REPO_ROOT / "data" / "source_redirects.json"


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    registre = read_json(REGISTRE, [])
    patch = read_json(PATCH, {})

    if not isinstance(registre, list):
        raise SystemExit("data/registre.json doit contenir une liste JSON")
    if patch.get("id") != "S10":
        raise SystemExit("Le patch ne cible pas S10")

    old_s10 = None
    updated = False
    for i, entry in enumerate(registre):
        if isinstance(entry, dict) and entry.get("id") == "S10":
            old_s10 = entry
            merged = dict(entry)
            merged.update(patch)
            registre[i] = merged
            updated = True
            break

    if not updated:
        registre.insert(9, patch)

    write_json(REGISTRE, registre)

    redirects = read_json(REDIRECTS, [])
    if not isinstance(redirects, list):
        redirects = []
    redirects = [r for r in redirects if not (isinstance(r, dict) and r.get("from") == "S10-OLD")]
    if old_s10 and "University of Birmingham" in json.dumps(old_s10, ensure_ascii=False):
        redirects.append({
            "from": "S10-OLD",
            "from_label": old_s10.get("source_label", "S10 ancien"),
            "to": "S10",
            "reason": "Ancienne entrée University of Birmingham eTheses abandonnée comme source active ; S10 réattribué à la source primaire Bernard Sumner, Chapter and Verse.",
            "date": "2026-05-16"
        })
        write_json(REDIRECTS, redirects)

    print("S10 registre patch applied")


if __name__ == "__main__":
    main()
