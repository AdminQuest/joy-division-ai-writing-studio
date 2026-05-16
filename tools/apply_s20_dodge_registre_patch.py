#!/usr/bin/env python3
"""
Réattribue S20 à Martin Dodge et documente la redirection de l'ancien S20 Reynolds vers S72.

Usage :
  python3 tools/apply_s20_dodge_registre_patch.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRE = REPO_ROOT / "data" / "registre.json"
PATCH = REPO_ROOT / "sources" / "dodge_manchester_geographies" / "registre_patch_s20.json"
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
    if patch.get("id") != "S20":
        raise SystemExit("Le patch ne cible pas S20")

    old_s20 = None
    found = False
    for index, entry in enumerate(registre):
        if isinstance(entry, dict) and entry.get("id") == "S20":
            old_s20 = entry
            registre[index] = patch
            found = True
            break

    if not found:
        registre.append(patch)

    write_json(REGISTRE, registre)

    redirects = read_json(REDIRECTS, [])
    if not isinstance(redirects, list):
        raise SystemExit("data/source_redirects.json doit contenir une liste JSON si le fichier existe")

    redirect_entry = {
        "from": "S20-OLD",
        "from_label": old_s20.get("source_label") if isinstance(old_s20, dict) else "S20 ancien",
        "to": "S72",
        "reason": "Ancien S20 considéré comme doublon de S72 ; S20 réattribué à Martin Dodge, Manchester Geographies, chapitre 3.",
        "date": "2026-05-16"
    }

    redirects = [r for r in redirects if not (isinstance(r, dict) and r.get("from") == "S20-OLD")]
    redirects.append(redirect_entry)
    write_json(REDIRECTS, redirects)

    print("S20 réattribué à Dodge dans data/registre.json")
    print("Redirection S20-OLD -> S72 enregistrée dans data/source_redirects.json")


if __name__ == "__main__":
    main()
