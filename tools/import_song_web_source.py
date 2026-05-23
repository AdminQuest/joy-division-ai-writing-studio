#!/usr/bin/env python3
"""
Import a song-oriented external web source into the Songbook workflow.

This tool is designed for pages such as:
- joydivision.epizy.com/joyd/<song>.html
- joydiv.org references
- Discogs releases

It stores raw captures locally and creates versioned metadata/evidence files.

Example:
  python3 tools/import_song_web_source.py \
    --song warsaw \
    --url https://joydivision.epizy.com/joyd/warsaw.html \
    --source-name "Joy Division songs pages"
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOT = Path(os.environ.get("SONGBOOK_LYRICS_ROOT", ROOT / "local_data" / "songbook_lyrics")).expanduser()
RAW_ROOT = PRIVATE_ROOT.parent / "web_captures"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def fetch(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode("utf-8", errors="ignore")


def write_local_capture(song_slug: str, url: str, html: str) -> Path:
    folder = RAW_ROOT / song_slug
    folder.mkdir(parents=True, exist_ok=True)
    host = slugify(urlparse(url).netloc)
    target = folder / f"{host}.html"
    target.write_text(html, encoding="utf-8")
    return target


def build_metadata(song_slug: str, song_id: str, song_title: str, url: str, source_name: str, capture_path: Path) -> dict:
    return {
        "web_source_id": f"WEB-{slugify(source_name)}-{song_slug}".upper(),
        "song_id": song_id,
        "canonical_song": song_title,
        "slug": song_slug,
        "url": url,
        "source_name": source_name,
        "consulted_at": date.today().isoformat(),
        "captured_html_local_path": str(capture_path),
        "target_song_folder": f"songs/{song_slug}/",
        "extracted_fields": {
            "title": song_title,
            "aliases": [],
            "credits": [],
            "versions": [],
            "releases": [],
            "live_occurrences": [],
            "bootlegs": [],
            "bibliography": [],
            "notes": [
                "Raw HTML captured locally.",
                "Metadata extraction to be completed manually or by parser improvements."
            ]
        },
        "private_lyrics_action": "compare_with_private_lyrics",
        "verification_status": "to_check",
        "trust_level": "B"
    }


def write_versioned_metadata(song_slug: str, metadata: dict):
    target = ROOT / "songs" / song_slug / "web_sources.json"
    existing = []
    if target.exists():
        try:
            existing = json.loads(target.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    existing = [x for x in existing if x.get("web_source_id") != metadata["web_source_id"]]
    existing.append(metadata)
    target.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def main():
    parser = argparse.ArgumentParser(description="Import an external song web source into the Songbook workflow.")
    parser.add_argument("--song", required=True, help="Song slug, e.g. warsaw")
    parser.add_argument("--song-id", default="", help="Canonical JD-SONG-XXX id")
    parser.add_argument("--title", default="", help="Canonical song title")
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-name", required=True)
    args = parser.parse_args()

    html = fetch(args.url)
    capture = write_local_capture(args.song, args.url, html)

    metadata = build_metadata(
        args.song,
        args.song_id or "",
        args.title or args.song,
        args.url,
        args.source_name,
        capture,
    )

    versioned = write_versioned_metadata(args.song, metadata)

    print(f"Local capture: {capture}")
    print(f"Versioned metadata: {versioned}")


if __name__ == "__main__":
    main()
