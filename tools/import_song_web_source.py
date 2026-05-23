#!/usr/bin/env python3
"""Import a song-oriented external web source into the Songbook workflow.

Supports direct URL fetch or locally saved HTML pages. The parser includes a
specific section parser for Joy Division song pages, whose useful structure is:
Track history / Lyrics / Other information / Covers.
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
SECTION_ALIASES = {
    "track history": "track_history",
    "lyrics": "lyrics_source",
    "other information": "other_information",
    "covers": "covers",
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
    text = re.sub(r"(?i)</(p|div|li|tr|td|th|h1|h2|h3|h4|table|blockquote|pre)>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html_lib.unescape(text).replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def split_lines(text: str) -> list[str]:
    return [line.strip(" -\t") for line in text.splitlines() if line.strip(" -\t")]


def sectionize(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {v: [] for v in SECTION_ALIASES.values()}
    sections["unclassified"] = []
    current = "unclassified"
    for line in lines:
        key = line.lower().strip().strip(":")
        if key in SECTION_ALIASES:
            current = SECTION_ALIASES[key]
            continue
        sections.setdefault(current, []).append(line)
    return sections


def parse_track_history(lines: list[str]) -> tuple[list[dict], list[dict], list[dict]]:
    sessions, releases, live = [], [], []
    for line in lines:
        lower = line.lower()
        item = {"description": line, "verification_status": "to_check"}
        if "recorded" in lower:
            sessions.append(item)
        if "released" in lower or "substance" in lower or "heart and soul" in lower or "warsaw" in lower or "ideal for living" in lower:
            releases.append(item)
        if "live" in lower or "warehouse" in lower or "preston" in lower:
            live.append(item)
    return sessions, releases, live


def parse_lyrics_variants(lines: list[str]) -> tuple[list[dict], list[str], list[str]]:
    variants, short_excerpts, notes = [], [], []
    current_note = None
    buffer = []
    for line in lines:
        if line.startswith("[") and line.endswith("]"):
            text = line.strip("[]")
            variants.append({"variant_type": "lyrics_note", "description": text, "verification_status": "to_check"})
            current_note = text
            buffer = []
            continue
        if line.startswith("["):
            current_note = line.strip("[").strip()
            buffer = []
            continue
        if current_note:
            if line.endswith("]"):
                buffer.append(line.strip("]").strip())
                variants.append({"variant_type": "lyrics_variant", "description": current_note, "text": " / ".join(buffer), "verification_status": "to_check"})
                current_note = None
                buffer = []
            else:
                buffer.append(line)
        if re.search(r"\b3[-, ]?1[-, ]?G\b", line, re.I) or "350125" in line or "3-5-0-1-2-5" in line:
            short_excerpts.append(line)
    if current_note and buffer:
        variants.append({"variant_type": "lyrics_variant", "description": current_note, "text": " / ".join(buffer), "verification_status": "to_check"})
    notes.append("Lyrics block includes at least one original-version note and several variant readings. Compare with S79 before canonical use.")
    return variants, list(dict.fromkeys(short_excerpts))[:10], notes


def parse_other_information(lines: list[str]) -> list[str]:
    return lines[:40]


def parse_covers(lines: list[str]) -> list[dict]:
    covers = []
    current_artist = None
    for line in lines:
        if not line:
            continue
        # Many saved pages flatten table cells. Treat lines with catalogue/year info as release lines.
        has_release_hint = bool(re.search(r"\b(19|20)\d{2}\b|\(|\bSub Pop\b|\bMerge\b|\bCleopatra\b|\bWestworld\b|\bFidel\b|\bbootleg\b|\bdownload\b", line, re.I))
        if has_release_hint and current_artist:
            covers.append({"artist": current_artist, "release": line, "verification_status": "to_check"})
            current_artist = None
        elif has_release_hint:
            covers.append({"artist": "", "release": line, "verification_status": "to_check"})
        else:
            if current_artist:
                current_artist = current_artist + " " + line
            else:
                current_artist = line
    if current_artist:
        covers.append({"artist": current_artist, "release": "", "verification_status": "to_check"})
    return covers


def parse_external_fields(raw_html: str, title: str) -> dict:
    text = text_from_html(raw_html)
    lines = split_lines(text)
    sections = sectionize(lines)
    sessions, releases, live = parse_track_history(sections.get("track_history", []))
    variants, excerpts, lyrics_notes = parse_lyrics_variants(sections.get("lyrics_source", []))
    other = parse_other_information(sections.get("other_information", []))
    covers = parse_covers(sections.get("covers", []))

    notes = [
        "Parsed from explicit Joy Division song-page sections: Track history, Lyrics, Other information, Covers.",
        "Check all web-derived data before treating it as verified evidence.",
    ]
    notes.extend(other)
    notes.extend(lyrics_notes)

    return {
        "title": title,
        "aliases": [],
        "credits": [],
        "track_history": sections.get("track_history", []),
        "versions": sessions,
        "releases": releases,
        "live_occurrences": live,
        "bootlegs": [],
        "covers": covers,
        "lyrics_variants": variants,
        "short_excerpts": [{"excerpt": x, "usage": "web-source lyric marker or variant line", "verification_status": "to_check"} for x in excerpts],
        "other_information": other,
        "bibliography": [],
        "notes": notes,
        "raw_text_preview": lines[:80],
    }


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
