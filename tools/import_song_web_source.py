#!/usr/bin/env python3
"""Import a song-oriented external web source into the Songbook workflow.

Supports either direct URL fetch or a locally saved HTML page.
"""

from __future__ import annotations

import argparse
import html as html_lib
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

HEADINGS = {
    "credits": ["credit", "credits", "written", "written by", "composition", "composer"],
    "versions": ["version", "versions", "recording", "recordings", "session", "sessions", "studio", "peel", "bbc"],
    "releases": ["release", "releases", "released", "appears", "album", "single", "compilation"],
    "live_occurrences": ["live", "concert", "concerts", "performed", "gig", "gigs", "setlist"],
    "bootlegs": ["bootleg", "bootlegs", "unofficial", "tape", "tapes"],
    "bibliography": ["source", "sources", "references", "bibliography", "links"],
    "notes": ["note", "notes", "comment", "comments", "information"],
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def fetch(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode("utf-8", errors="ignore")


def read_html(args) -> tuple[str, str]:
    if args.html_file:
        path = Path(args.html_file).expanduser()
        return path.read_text(encoding="utf-8", errors="ignore"), path.as_posix()
    return fetch(args.url), args.url


def text_from_html(raw: str) -> str:
    text = raw
    text = re.sub(r"(?is)<script.*?</script>", "\n", text)
    text = re.sub(r"(?is)<style.*?</style>", "\n", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</(p|div|li|tr|td|th|h1|h2|h3|h4|table|blockquote)>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def split_lines(text: str) -> list[str]:
    return [line.strip(" -\t") for line in text.splitlines() if line.strip(" -\t")]


def classify_line(line: str) -> str | None:
    lower = line.lower().strip(":")
    for field, keys in HEADINGS.items():
        if any(lower == k or lower.startswith(k + ":") or lower.startswith(k + " ") for k in keys):
            return field
    return None


def parse_external_fields(raw_html: str, title: str) -> dict:
    text = text_from_html(raw_html)
    lines = split_lines(text)
    fields = {
        "title": title,
        "aliases": [],
        "credits": [],
        "versions": [],
        "releases": [],
        "live_occurrences": [],
        "bootlegs": [],
        "bibliography": [],
        "notes": [],
        "raw_text_preview": lines[:80],
    }

    current = "notes"
    for line in lines:
        if len(line) > 500:
            continue
        field = classify_line(line)
        if field:
            current = field
            remainder = re.sub(r"^[^:]{1,40}:\s*", "", line).strip()
            if remainder and remainder.lower() != line.lower():
                fields[current].append(remainder)
            continue
        lower = line.lower()
        if any(k in lower for k in ["peel", "bbc", "session", "recorded", "studio", "version"]):
            fields["versions"].append(line)
        elif any(k in lower for k in ["factory", "album", "single", "released", "lp", "ep", "cassette", "cd"]):
            fields["releases"].append(line)
        elif any(k in lower for k in ["live", "concert", "gig", "performance", "setlist"]):
            fields["live_occurrences"].append(line)
        elif any(k in lower for k in ["bootleg", "unofficial", "audience tape", "soundboard"]):
            fields["bootlegs"].append(line)
        elif any(k in lower for k in ["written by", "lyrics", "music", "published", "copyright"]):
            fields["credits"].append(line)
        elif current in fields and current != "raw_text_preview":
            fields[current].append(line)

    for key in ["credits", "versions", "releases", "live_occurrences", "bootlegs", "bibliography", "notes"]:
        seen = []
        for item in fields[key]:
            if item and item not in seen:
                seen.append(item)
        fields[key] = seen[:80]
    fields["notes"].append("Parsed heuristically from saved or fetched HTML. Check before relying on any field.")
    return fields


def write_local_capture(song_slug: str, url: str, raw_html: str) -> Path:
    folder = RAW_ROOT / song_slug
    folder.mkdir(parents=True, exist_ok=True)
    host = slugify(urlparse(url).netloc or "local-html")
    target = folder / f"{host}.html"
    target.write_text(raw_html, encoding="utf-8")
    return target


def build_metadata(song_slug: str, song_id: str, song_title: str, url: str, source_name: str, capture_path: Path, raw_html: str) -> dict:
    fields = parse_external_fields(raw_html, song_title)
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
        "extracted_fields": fields,
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
    parser.add_argument("--html-file", default="", help="Optional local saved HTML file")
    parser.add_argument("--source-name", required=True)
    args = parser.parse_args()

    raw_html, origin = read_html(args)
    capture = write_local_capture(args.song, args.url or origin, raw_html)
    metadata = build_metadata(args.song, args.song_id or "", args.title or args.song, args.url or origin, args.source_name, capture, raw_html)
    versioned = write_versioned_metadata(args.song, metadata)

    print(f"HTML origin: {origin}")
    print(f"Local capture: {capture}")
    print(f"Versioned metadata: {versioned}")
    print("Extracted counts:")
    for key, value in metadata["extracted_fields"].items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)}")


if __name__ == "__main__":
    main()
