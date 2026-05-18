#!/usr/bin/env python3
"""
Patch idempotent du registre canonique pour S49.

Objet : fixer la source S49 — Manolo Farci, « Here are the Young Men, the weight
on their shoulders. La danza esistenziale di Ian Curtis », 2021.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRE = ROOT / "data" / "registre.json"
PATCH = ROOT / "sources" / "farci_danza_esistenziale_ian_curtis" / "registre_patch_s49.json"


def source_sort_key(entry: dict) -> tuple[int, str]:
    source_id = str(entry.get("id", ""))
    if source_id.startswith("S") and source_id[1:].isdigit():
        return (int(source_id[1:]), source_id)
    return (10_000, source_id)


def main() -> None:
    if not REGISTRE.exists():
        raise FileNotFoundError(f"Registre introuvable : {REGISTRE}")
    if not PATCH.exists():
        raise FileNotFoundError(f"Patch S49 introuvable : {PATCH}")

    registre = json.loads(REGISTRE.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))

    if patch.get("id") != "S49":
        raise ValueError("Le patch chargé ne porte pas l’identifiant S49.")

    replaced = False
    for index, entry in enumerate(registre):
        if entry.get("id") == "S49":
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
    print(f"S49 {action} dans data/registre.json")


if __name__ == "__main__":
    main()
