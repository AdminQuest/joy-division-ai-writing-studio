#!/usr/bin/env python3
"""
Step 6 — Seed external evidence files for priority Songbook dossiers.

This script does not scrape the web. It prepares the evidence containers that will receive
checked external data from joydiv.org, Discogs, official booklets, BBC/Peel references,
lyrics books and personal bootleg catalogues.

Inputs:
- data/songbook_priority_seed_v1.json
- data/songbook_external_sources_registry.json

Outputs:
- songs/<slug>/external_evidence.md for each priority song
- data/songbook_external_evidence_index.json
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "songbook_priority_seed_v1.json"
REGISTRY_PATH = ROOT / "data" / "songbook_external_sources_registry.json"
OUT_INDEX = ROOT / "data" / "songbook_external_evidence_index.json"


def scalar(value: str) -> str:
    return json.dumps(value or "", ensure_ascii=False)


def yaml_list(values: list[str], indent: int = 2) -> str:
    if not values:
        return "[]"
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}- {scalar(v)}" for v in values)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_external_evidence(song: dict[str, Any], registry: dict[str, Any]) -> str:
    today = date.today().isoformat()
    external_ids = [src["external_source_id"] for src in registry.get("external_sources", [])]
    preferred = song.get("external_sources_to_verify", [])
    return f"# {song['song']} — Preuves externes à intégrer\n\n" \
        f"```yaml\n" \
        f"id: {song['id']}-EXTERNAL-EVIDENCE\n" \
        f"song_id: {song['id']}\n" \
        f"type_unite: song_external_evidence_file\n" \
        f"canonical_song: {scalar(song['song'])}\n" \
        f"slug: {scalar(song['slug'])}\n" \
        f"status: \"external evidence container created ; no external facts consolidated yet\"\n" \
        f"last_update: {scalar(today)}\n" \
        f"registry: \"data/songbook_external_sources_registry.json\"\n" \
        f"schema: \"schemas/song_external_evidence.schema.yaml\"\n" \
        f"```\n\n" \
        "## 1. Sources externes à vérifier pour ce titre\n\n" \
        "```yaml\npreferred_external_sources: " + yaml_list(preferred) + "\n```\n\n" \
        "## 2. Sources externes disponibles dans le registre\n\n" \
        "```yaml\nregistered_external_sources: " + yaml_list(external_ids) + "\n```\n\n" \
        "## 3. Preuves externes collectées\n\n" \
        "```yaml\nexternal_evidence: []\n```\n\n" \
        "## 4. Données en attente par type\n\n" \
        "```yaml\npending_external_tasks:\n" \
        "  lyrics: \"source imprimée ou officielle à vérifier ; ne pas importer automatiquement depuis internet\"\n" \
        "  sessions: \"vérifier joydiv.org, livrets officiels, BBC/Peel et sources discographiques\"\n" \
        "  releases: \"vérifier Discogs puis recouper avec livrets officiels\"\n" \
        "  live_occurrences: \"vérifier joydiv.org et setlists spécialisées avant consolidation\"\n" \
        "  bootlegs: \"rattacher à la collection personnelle, à Discogs et à un concert si possible\"\n" \
        "```\n\n" \
        "## 5. Prudence\n\n" \
        "Aucune donnée externe n’est consolidée dans ce fichier tant qu’elle n’a pas reçu un `evidence_id`, une source, une date de consultation, un type de preuve et un statut de vérification.\n"


def seed(force: bool = False) -> None:
    seed_data = load_json(SEED_PATH)
    registry = load_json(REGISTRY_PATH)
    rows = []
    created = 0
    skipped = 0
    for song in seed_data.get("priority_songs", []):
        path = ROOT / "songs" / song["slug"] / "external_evidence.md"
        if path.exists() and not force:
            skipped += 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render_external_evidence(song, registry), encoding="utf-8")
            created += 1
        rows.append({
            "song_id": song["id"],
            "song": song["song"],
            "slug": song["slug"],
            "priority": song["priority"],
            "external_evidence_file": f"songs/{song['slug']}/external_evidence.md",
            "preferred_external_sources": song.get("external_sources_to_verify", []),
        })
    OUT_INDEX.write_text(json.dumps({
        "type_unite": "songbook_external_evidence_index",
        "version": "1.0",
        "updated_at": date.today().isoformat(),
        "registry": "data/songbook_external_sources_registry.json",
        "schema": "schemas/song_external_evidence.schema.yaml",
        "priority_songs": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"External evidence files created/refreshed: {created}")
    print(f"Existing files skipped: {skipped}")
    print(f"Index written: {OUT_INDEX.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed external evidence containers for priority Songbook dossiers.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing external_evidence.md files.")
    args = parser.parse_args()
    seed(force=args.force)


if __name__ == "__main__":
    main()
