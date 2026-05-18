#!/usr/bin/env python3
"""
Patch idempotent du registre canonique pour S51.

Objet : fixer la source S51 — Jennifer Malvezzi,
« Dream English Kid 1978-1980. L’immagine lo-fi dei Joy Division nei media popolari inglesi », 2021.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRE = ROOT / "data" / "registre.json"
PATCH = ROOT / "sources" / "malvezzi_dream_english_kid_lo_fi" / "registre_patch_s51.json"


def source_sort_key(entry: dict) -> tuple[int, str]:
    source_id = str(entry.get("id", ""))
    if source_id.startswith("S") and source_id[1:].isdigit():
        return (int(source_id[1:]), source_id)
    return (10_000, source_id)


def main() -> None:
    if not REGISTRE.exists():
        raise FileNotFoundError(f"Registre introuvable : {REGISTRE}")
    if not PATCH.exists():
        raise FileNotFoundError(f"Patch S51 introuvable : {PATCH}")

    registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))

    if patch.get("id") != "S51":
        raise ValueError("Le patch chargé ne porte pas l’identifiant S51.")

    replaced = False
    for index, entry in enumerate(registre):
        if entry.get("id") == "S51":
            registre[index] = patch
            replaced = True
            break

    if not replaced:
        registre.append(patch)

    registre.sort(key=source_sort_key)
    REGISTRE.write_text(
        json.dumps(registre, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    action = "mise à jour" if replaced else "ajoutée"
    print(f"S51 {action} dans data/registre.json")


if __name__ == "__main__":
    main()
