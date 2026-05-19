#!/usr/bin/env python3
"""
Audit the Joy Division / Warsaw song canon against generated and Markdown song records.

The script is intentionally conservative:
- it reads the canonical titles from registers/songs/00_canonical_joy_division_songs.md;
- it scans Markdown and generated JSON for song-like titles;
- it reports records that map to the canon, records excluded explicitly, and possible off-canon titles.

It does not rewrite source records. Use it before and after a manual cleanup pass.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "registers" / "songs" / "00_canonical_joy_division_songs.md"
SONGS_JSON = ROOT / "exports" / "generated" / "songs.json"
SCAN_DIRS = [ROOT / "registers" / "songs", ROOT / "sources", ROOT / "registers"]


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower().replace("’", "'").replace("‘", "'")
    value = value.replace("…", " ").replace("...", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return value.strip()


def extract_canon() -> tuple[dict[str, str], dict[str, str], list[str]]:
    text = CANON_PATH.read_text(encoding="utf-8")
    aliases: dict[str, str] = {}
    excluded: dict[str, str] = {}
    canonical_order: list[str] = []

    blocks = re.split(r"\n\s*- id:\s+", text)
    for block in blocks[1:]:
        block = "- id: " + block
        song_match = re.search(r"\n\s*song:\s+\"([^\"]+)\"", block)
        if not song_match:
            continue
        song = song_match.group(1).strip()
        is_excluded = "exclude: true" in block
        alias_values = [song]
        aliases_match = re.search(r"\n\s*aliases:\s+\[(.*?)\]", block, re.S)
        if aliases_match:
            alias_values.extend(re.findall(r"\"([^\"]+)\"", aliases_match.group(1)))
        if is_excluded:
            for alias in alias_values:
                excluded[norm(alias)] = song
        else:
            canonical_order.append(song)
            for alias in alias_values:
                aliases[norm(alias)] = song
    return aliases, excluded, canonical_order


def titles_from_generated() -> list[tuple[str, str, str]]:
    if not SONGS_JSON.exists():
        return []
    data = json.loads(SONGS_JSON.read_text(encoding="utf-8"))
    out: list[tuple[str, str, str]] = []
    for item in data:
        d = item.get("data") or {}
        title = d.get("song") or d.get("titre") or d.get("title")
        if title:
            out.append((str(title), item.get("file", ""), item.get("id", "")))
    return out


def titles_from_markdown() -> list[tuple[str, str, str]]:
    patterns = [
        re.compile(r"\n\s*song:\s+\"([^\"]+)\""),
        re.compile(r"\n\s*titre:\s+\"([^\"]+)\""),
        re.compile(r"\n\s*title:\s+\"([^\"]+)\""),
    ]
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path == CANON_PATH:
                continue
            rel = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "type_unite: song" not in text and "type_unite: chanson" not in text and "song:" not in text:
                continue
            for pattern in patterns:
                for match in pattern.finditer(text):
                    title = match.group(1).strip()
                    key = (title, rel)
                    if key not in seen:
                        seen.add(key)
                        out.append((title, rel, "markdown"))
    return out


def main() -> None:
    aliases, excluded, canonical_order = extract_canon()
    records = titles_from_generated() + titles_from_markdown()
    linked: dict[str, int] = {song: 0 for song in canonical_order}
    excluded_hits: list[tuple[str, str, str, str]] = []
    off_canon: list[tuple[str, str, str]] = []

    for title, file, record_id in records:
        key = norm(title)
        if key in aliases:
            linked[aliases[key]] += 1
        elif key in excluded:
            excluded_hits.append((title, excluded[key], file, record_id))
        else:
            off_canon.append((title, file, record_id))

    print(f"Canonical Joy Division/Warsaw titles: {len(canonical_order)}")
    print(f"Song-like records scanned: {len(records)}")
    print(f"Canonical titles with linked records: {sum(1 for v in linked.values() if v)}")
    print(f"Explicitly excluded hits: {len(excluded_hits)}")
    print(f"Possible off-canon titles: {len(off_canon)}")
    print()

    print("Canonical titles without linked records:")
    for song, count in linked.items():
        if count == 0:
            print(f"  - {song}")
    print()

    print("Explicitly excluded hits:")
    for title, canonical_exclusion, file, record_id in excluded_hits[:80]:
        print(f"  - {title} [{record_id}] in {file} -> excluded as {canonical_exclusion}")
    print()

    print("Possible off-canon titles to inspect:")
    for title, file, record_id in off_canon[:160]:
        print(f"  - {title} [{record_id}] in {file}")


if __name__ == "__main__":
    main()
