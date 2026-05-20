#!/usr/bin/env python3
"""
Initialise a local, non-versioned lyrics workspace for the Songbook.

It creates local_data/songbook_lyrics/<slug>/full_lyrics.txt and editorial_notes.json
for every canonical Joy Division / Warsaw song.

The local_data/ directory is ignored by Git. Do not force-add it.
"""

from __future__ import annotations

import ast
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "registers" / "songs" / "00_canonical_joy_division_songs.md"
LOCAL_ROOT = ROOT / "local_data" / "songbook_lyrics"


def parse_inline_list(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    return [x.strip().strip('"\'') for x in raw.strip("[]").split(",") if x.strip()]


def parse_canon() -> list[dict[str, Any]]:
    text = CANON_PATH.read_text(encoding="utf-8")
    songs: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_songs = False
    for line in text.splitlines():
        if line.strip() == "songs:":
            in_songs = True
            continue
        if not in_songs:
            continue
        if line.startswith("```"):
            if current:
                songs.append(current)
            break
        m_id = re.match(r"\s*- id:\s*(\S+)", line)
        if m_id:
            if current:
                songs.append(current)
            current = {"id": m_id.group(1).strip()}
            continue
        if current is None:
            continue
        m = re.match(r"\s*([a-zA-Z_]+):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith('"') and value.endswith('"'):
            current[key] = value[1:-1]
        elif value in {"true", "false"}:
            current[key] = value == "true"
        elif value.startswith("["):
            current[key] = parse_inline_list(value)
        else:
            current[key] = value
    return [s for s in songs if s.get("canonical_song") is True and s.get("exclude") is not True]


def editorial_template(song: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"{song['id']}-LYRICS-EDITORIAL",
        "song_id": song["id"],
        "canonical_song": song["song"],
        "slug": song["slug"],
        "type_unite": "song_lyrics_editorial",
        "canonical_lyrics_source": "",
        "source_page": "",
        "full_lyrics_local_path": f"local_data/songbook_lyrics/{song['slug']}/full_lyrics.txt",
        "completeness": "complete_local_not_versioned",
        "verification_status": "a_verifier",
        "short_excerpts": [],
        "variants": [],
        "motifs": [],
        "editorial_notes": [],
        "chapters": [],
        "last_update": date.today().isoformat(),
        "instructions": [
            "Conserver les paroles complètes uniquement dans full_lyrics.txt.",
            "Ne mettre ici que des courts extraits, variantes décrites, motifs et notes éditoriales.",
            "Renseigner source, page et statut de vérification avant extraction vers le repo."
        ],
    }


def main() -> None:
    songs = parse_canon()
    created = 0
    skipped = 0
    for song in songs:
        folder = LOCAL_ROOT / song["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        lyrics_path = folder / "full_lyrics.txt"
        notes_path = folder / "editorial_notes.json"
        if not lyrics_path.exists():
            lyrics_path.write_text(
                f"# {song['song']}\n\n"
                "Colle ici les paroles complètes pour usage local uniquement.\n"
                "Ce fichier est dans local_data/ et ne doit jamais être versionné.\n",
                encoding="utf-8",
            )
            created += 1
        else:
            skipped += 1
        if not notes_path.exists():
            notes_path.write_text(json.dumps(editorial_template(song), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            created += 1
        else:
            skipped += 1
    print(f"Canonical songs: {len(songs)}")
    print(f"Local files created: {created}")
    print(f"Existing files skipped: {skipped}")
    print(f"Workspace: {LOCAL_ROOT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
