#!/usr/bin/env python3
"""
Generate empty Joy Division / Warsaw song dossier folders from the canonical song register.

Step 3 of the Songbook workflow.

The script is intentionally non-destructive by default:
- it reads registers/songs/00_canonical_joy_division_songs.md;
- it creates songs/<slug>/ folders;
- it creates 7 standard files per song when they do not already exist;
- it writes data/song_dossiers_index.json;
- use --force only to refresh already existing generated skeleton files.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "registers" / "songs" / "00_canonical_joy_division_songs.md"
TEMPLATE_DIR = ROOT / "templates"
SONGS_DIR = ROOT / "songs"
DATA_DIR = ROOT / "data"
INDEX_PATH = DATA_DIR / "song_dossiers_index.json"

TEMPLATES = {
    "song.md": "song_dossier_template.md",
    "lyrics.md": "song_lyrics_template.md",
    "sessions.md": "song_sessions_template.md",
    "live_occurrences.md": "song_live_occurrences_template.md",
    "releases.md": "song_releases_template.md",
    "bootlegs.md": "song_bootlegs_template.md",
    "source_notes.md": "song_source_notes_template.md",
}


def yaml_inline_list(value: Any) -> str:
    if not value:
        return "[]"
    if isinstance(value, list):
        return "[" + ", ".join(json.dumps(str(v), ensure_ascii=False) for v in value) + "]"
    return "[" + json.dumps(str(value), ensure_ascii=False) + "]"


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
    # Use a conservative line-based parser for the simple canonical YAML blocks.
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


def render_template(template_name: str, song: dict[str, Any]) -> str:
    template_path = TEMPLATE_DIR / template_name
    content = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{SONG_ID}}": str(song["id"]),
        "{{SONG_TITLE}}": str(song["song"]),
        "{{SONG_SLUG}}": str(song["slug"]),
        "{{SONG_CATEGORY}}": str(song.get("category", "")),
        "{{SONG_PERIOD}}": str(song.get("period", "")),
        "{{SONG_STATUS}}": str(song.get("status", "")),
        "{{SONG_ALBUMS_YAML}}": yaml_inline_list(song.get("albums", [])),
        "{{SONG_ALIASES_YAML}}": yaml_inline_list(song.get("aliases", [])),
        "{{SONG_VARIANTS_YAML}}": yaml_inline_list(song.get("include_variants", [])),
        "{{GENERATED_DATE}}": date.today().isoformat(),
    }
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def write_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def generate(force: bool = False) -> None:
    songs = parse_canon()
    if not songs:
        raise SystemExit(f"No canonical songs found in {CANON_PATH}")

    created = 0
    skipped = 0
    index: list[dict[str, Any]] = []

    for song in songs:
        slug = str(song["slug"])
        song_dir = SONGS_DIR / slug
        song_dir.mkdir(parents=True, exist_ok=True)
        files = []
        for file_name, template_name in TEMPLATES.items():
            target = song_dir / file_name
            content = render_template(template_name, song)
            if write_file(target, content, force):
                created += 1
            else:
                skipped += 1
            files.append(target.relative_to(ROOT).as_posix())
        index.append({
            "id": song["id"],
            "song": song["song"],
            "slug": slug,
            "category": song.get("category", ""),
            "period": song.get("period", ""),
            "status": song.get("status", ""),
            "albums": song.get("albums", []),
            "aliases": song.get("aliases", []),
            "include_variants": song.get("include_variants", []),
            "folder": f"songs/{slug}/",
            "files": files,
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Canonical songs: {len(songs)}")
    print(f"Skeleton files created/refreshed: {created}")
    print(f"Existing files skipped: {skipped}")
    print(f"Index written: {INDEX_PATH.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Joy Division / Warsaw song dossier skeletons.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated skeleton files.")
    args = parser.parse_args()
    generate(force=args.force)


if __name__ == "__main__":
    main()
