#!/usr/bin/env python3
"""
Migration tool — Atomes v2

Injecte automatiquement les champs minimaux requis
par le schéma d’atomisation enrichie v2.

Objectif :
- rendre compatibles les anciens atomes ;
- éviter les warnings structurels ;
- préparer les enrichissements historiographiques.

Le script n’écrase pas les champs déjà existants.
"""

from __future__ import annotations

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [REPO_ROOT / "sources", REPO_ROOT / "registers"]

DEFAULT_BLOCK = """
role_argumentatif:
  - documentation générale

niveau_preuve:
  statut: corrobore
  corroboration: moyenne
  confiance: moyenne

stabilite:
  statut: assez_stable
  risque_revision: moyen

importance:
  niveau: moyenne

risque_surinterpretation:
  niveau: moyen

liens_interchapitres:
  - Chapitre 1

liens_citations: []

motifs: []

concepts_derives: []
""".strip()

YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)

REQUIRED_FIELDS = [
    "role_argumentatif",
    "niveau_preuve",
    "stabilite",
    "importance",
    "risque_surinterpretation",
    "liens_interchapitres",
    "liens_citations",
    "motifs",
    "concepts_derives",
]


def iter_markdown_files():
    for directory in SCAN_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*.md"):
            yield path


def needs_migration(block: str) -> bool:
    return any(field not in block for field in REQUIRED_FIELDS)


def migrate_yaml_block(block: str) -> str:
    if not needs_migration(block):
        return block

    migrated = block.rstrip() + "\n\n"

    for line in DEFAULT_BLOCK.splitlines():
        field_name = line.split(":")[0].strip()

        if field_name and field_name in REQUIRED_FIELDS:
            if field_name in migrated:
                continue

        migrated += line + "\n"

    return migrated.rstrip()


def migrate_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    modified = False

    def replacer(match):
        nonlocal modified

        block = match.group(1)

        if not needs_migration(block):
            return match.group(0)

        modified = True
        migrated = migrate_yaml_block(block)

        return f"```yaml\n{migrated}\n```"

    updated = YAML_BLOCK_RE.sub(replacer, text)

    if modified:
        path.write_text(updated, encoding="utf-8")

    return modified


def main():
    migrated_files = []

    for path in iter_markdown_files():
        if migrate_file(path):
            migrated_files.append(path)

    print("Migration v2 terminée")
    print(f"Fichiers modifiés : {len(migrated_files)}")

    for path in migrated_files[:50]:
        print(f"- {path.relative_to(REPO_ROOT)}")

    if len(migrated_files) > 50:
        print(f"... {len(migrated_files) - 50} fichiers supplémentaires")


if __name__ == "__main__":
    main()
