#!/usr/bin/env python3
"""
Step 5 — Enrich priority Songbook dossiers from internal atomized records.

This script is deliberately repo-native and source-first:
- it reads data/songbook_priority_seed_v1.json;
- it reads registers/songs/00_canonical_joy_division_songs.md for aliases;
- it reads exports/generated/songs.json when available;
- it optionally scans Markdown registers/songs/*.md and registers/*.md for song records;
- it updates songs/<slug>/source_notes.md for the priority dossiers;
- it writes data/songbook_internal_sources_index.json.

It does not fetch the internet. External sources remain only verification targets.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "registers" / "songs" / "00_canonical_joy_division_songs.md"
SEED_PATH = ROOT / "data" / "songbook_priority_seed_v1.json"
SONGS_JSON = ROOT / "exports" / "generated" / "songs.json"
OUT_INDEX = ROOT / "data" / "songbook_internal_sources_index.json"


def norm(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.lower().replace("’", "'").replace("‘", "'")
    value = value.replace("…", " ").replace("...", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return value.strip()


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


def parse_canon_aliases() -> dict[str, dict[str, Any]]:
    text = CANON_PATH.read_text(encoding="utf-8")
    aliases: dict[str, dict[str, Any]] = {}
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
                add_aliases(current, aliases)
            break
        m_id = re.match(r"\s*- id:\s*(\S+)", line)
        if m_id:
            if current:
                add_aliases(current, aliases)
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
    return aliases


def add_aliases(song: dict[str, Any], aliases: dict[str, dict[str, Any]]) -> None:
    if song.get("canonical_song") is not True or song.get("exclude") is True:
        return
    values = [song.get("song", ""), *song.get("aliases", [])]
    for alias in values:
        key = norm(str(alias))
        if key:
            aliases[key] = song


def load_generated_song_records() -> list[dict[str, Any]]:
    if not SONGS_JSON.exists():
        return []
    try:
        data = json.loads(SONGS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return []
    out: list[dict[str, Any]] = []
    for item in data:
        d = item.get("data") or {}
        title = d.get("song") or d.get("titre") or d.get("title")
        if not title:
            continue
        out.append({
            "record_id": item.get("id") or d.get("id") or "",
            "file": item.get("file") or d.get("__file") or "",
            "heading": item.get("heading") or "",
            "source_id": d.get("source_id") or first(d.get("sources")),
            "source_label": d.get("source_label") or "",
            "song": str(title),
            "usage": d.get("usage") or d.get("notes") or d.get("resume") or "",
            "chapters": d.get("chapters") or d.get("chapitres") or [],
            "related_atoms": d.get("related_atoms") or d.get("atomes_lies") or [],
            "related_quotes": d.get("related_quotes") or d.get("citations_liees") or [],
            "themes": d.get("themes") or d.get("motifs") or d.get("related_motifs") or [],
            "keywords": d.get("keywords") or [],
        })
    return out


def first(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return ""


def read_seed() -> dict[str, Any]:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def match_records(records: list[dict[str, Any]], aliases: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    matched: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    for record in records:
        song = aliases.get(norm(record.get("song", "")))
        if not song:
            continue
        key = (song["id"], record.get("record_id", ""), record.get("file", ""))
        if key in seen:
            continue
        seen.add(key)
        matched[song["id"]].append(record)
    return matched


def yaml_scalar(value: str) -> str:
    return json.dumps(value or "", ensure_ascii=False)


def yaml_list(values: Any, indent: int = 2) -> str:
    if not values:
        return "[]"
    if isinstance(values, str):
        values = [values]
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}- {yaml_scalar(str(v))}" for v in values)


def render_source_notes(song: dict[str, Any], records: list[dict[str, Any]]) -> str:
    today = date.today().isoformat()
    source_ids = sorted({r.get("source_id", "") for r in records if r.get("source_id")})
    related_atoms = sorted({a for r in records for a in ensure_list(r.get("related_atoms"))})
    related_quotes = sorted({q for r in records for q in ensure_list(r.get("related_quotes"))})
    files = sorted({r.get("file", "") for r in records if r.get("file")})

    internal_sources_rows = []
    for sid in source_ids:
        label = next((r.get("source_label") for r in records if r.get("source_id") == sid and r.get("source_label")), sid)
        count = sum(1 for r in records if r.get("source_id") == sid)
        internal_sources_rows.append({"source_id": sid, "source_label": label or sid, "matched_song_records": count})

    record_rows = []
    for r in records:
        record_rows.append({
            "record_id": r.get("record_id", ""),
            "source_id": r.get("source_id", ""),
            "song_title_in_record": r.get("song", ""),
            "file": r.get("file", ""),
            "heading": r.get("heading", ""),
            "chapters": ensure_list(r.get("chapters")),
            "usage": r.get("usage", ""),
            "themes": ensure_list(r.get("themes")),
            "keywords": ensure_list(r.get("keywords")),
        })

    return f"# {song['song']} — Sources, atomes et vérifications\n\n" \
        f"```yaml\n" \
        f"id: {song['id']}-SOURCE-NOTES\n" \
        f"song_id: {song['id']}\n" \
        f"type_unite: song_source_notes\n" \
        f"canonical_song: {yaml_scalar(song['song'])}\n" \
        f"slug: {yaml_scalar(song['slug'])}\n" \
        f"verification_status: \"enrichi automatiquement depuis exports/generated/songs.json ; à vérifier source par source\"\n" \
        f"last_update: {yaml_scalar(today)}\n" \
        f"matched_records: {len(records)}\n" \
        f"````\n".replace("````", "```") + \
        "\n## 1. Sources internes atomisées\n\n" + \
        "```yaml\ninternal_sources:\n" + render_yaml_objects(internal_sources_rows) + "\n```\n\n" + \
        "## 2. Mentions internes rattachées\n\n" + \
        "```yaml\nmatched_song_records:\n" + render_yaml_objects(record_rows) + "\n```\n\n" + \
        "## 3. Atomes liés\n\n" + \
        "```yaml\nrelated_atoms: " + yaml_list(related_atoms) + "\n```\n\n" + \
        "## 4. Citations liées\n\n" + \
        "```yaml\nrelated_quotes: " + yaml_list(related_quotes) + "\n```\n\n" + \
        "## 5. Fichiers internes repérés\n\n" + \
        "```yaml\nmatched_files: " + yaml_list(files) + "\n```\n\n" + \
        "## 6. Sources externes à intégrer\n\n" + \
        "```yaml\nexternal_sources: " + yaml_list(song.get("external_sources_to_verify", [])) + "\n```\n\n" + \
        "## 7. Contradictions et arbitrages\n\n" + \
        "```yaml\nsource_conflicts: []\narbitrages:\n  - \"Étape 5 : rattachement automatique effectué sur titres canoniques et alias ; chaque donnée reste à vérifier avant usage définitif.\"\n```\n"


def ensure_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def render_yaml_objects(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return " []"
    lines: list[str] = []
    for row in rows:
        lines.append("  - " + next(iter(row.keys())) + ": " + yaml_scalar(str(next(iter(row.values())))))
        for key, value in list(row.items())[1:]:
            if isinstance(value, list):
                if value:
                    lines.append(f"    {key}:")
                    for item in value:
                        lines.append(f"      - {yaml_scalar(str(item))}")
                else:
                    lines.append(f"    {key}: []")
            else:
                lines.append(f"    {key}: {yaml_scalar(str(value))}")
    return "\n" + "\n".join(lines)


def render_index(seed: dict[str, Any], matched: dict[str, list[dict[str, Any]]]) -> str:
    rows = []
    for song in seed["priority_songs"]:
        rows.append({
            "priority": song["priority"],
            "song_id": song["id"],
            "song": song["song"],
            "slug": song["slug"],
            "matched_records": len(matched.get(song["id"], [])),
            "source_notes": f"songs/{song['slug']}/source_notes.md",
            "priority_notes": f"songs/{song['slug']}/priority_notes.md",
        })
    return json.dumps({
        "type_unite": "songbook_internal_sources_index",
        "version": "1.0",
        "updated_at": date.today().isoformat(),
        "input_seed": "data/songbook_priority_seed_v1.json",
        "input_generated_songs": "exports/generated/songs.json",
        "priority_songs": rows,
    }, ensure_ascii=False, indent=2) + "\n"


def enrich(dry_run: bool = False) -> None:
    seed = read_seed()
    aliases = parse_canon_aliases()
    records = load_generated_song_records()
    matched = match_records(records, aliases)
    updated = 0
    for song in seed["priority_songs"]:
        song_records = matched.get(song["id"], [])
        enriched_song = {**song}
        target = ROOT / "songs" / song["slug"] / "source_notes.md"
        content = render_source_notes(enriched_song, song_records)
        if not dry_run:
            target.write_text(content, encoding="utf-8")
        updated += 1
    if not dry_run:
        OUT_INDEX.write_text(render_index(seed, matched), encoding="utf-8")
    print(f"Priority dossiers processed: {updated}")
    print(f"Generated song records scanned: {len(records)}")
    print(f"Priority dossiers with matches: {sum(1 for s in seed['priority_songs'] if matched.get(s['id']))}")
    print(f"Index: {OUT_INDEX.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich priority Songbook dossiers from generated internal song records.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    enrich(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
