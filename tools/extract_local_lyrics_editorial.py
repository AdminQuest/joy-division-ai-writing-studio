#!/usr/bin/env python3
"""
Extract editorial lyrics notes from local_data/songbook_lyrics/ into versioned Songbook files.

Inputs (not versioned):
- local_data/songbook_lyrics/<slug>/editorial_notes.json
- local_data/songbook_lyrics/<slug>/full_lyrics.txt (not read by default; kept local)

Outputs (versioned):
- songs/<slug>/lyrics_editorial.md
- data/songbook_lyrics_editorial_index.json
- rag/fragments/songbook_lyrics_editorial.jsonl

This script never copies full_lyrics.txt content into the repo.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = ROOT / "local_data" / "songbook_lyrics"
SONGS_ROOT = ROOT / "songs"
DATA_OUT = ROOT / "data" / "songbook_lyrics_editorial_index.json"
RAG_OUT = ROOT / "rag" / "fragments" / "songbook_lyrics_editorial.jsonl"


def scalar(value: str) -> str:
    return json.dumps(value or "", ensure_ascii=False)


def yaml_list(values: Any, indent: int = 2) -> str:
    if not values:
        return "[]"
    if isinstance(values, str):
        values = [values]
    pad = " " * indent
    lines = []
    for item in values:
        if isinstance(item, dict):
            lines.append(f"{pad}- " + next(iter(item.keys())) + ": " + scalar(str(next(iter(item.values())))))
            for key, value in list(item.items())[1:]:
                if isinstance(value, list):
                    if value:
                        lines.append(f"{pad}  {key}:")
                        for sub in value:
                            lines.append(f"{pad}    - {scalar(str(sub))}")
                    else:
                        lines.append(f"{pad}  {key}: []")
                else:
                    lines.append(f"{pad}  {key}: {scalar(str(value))}")
        else:
            lines.append(f"{pad}- {scalar(str(item))}")
    return "\n" + "\n".join(lines)


def load_notes() -> list[dict[str, Any]]:
    if not LOCAL_ROOT.exists():
        return []
    notes = []
    for path in sorted(LOCAL_ROOT.glob("*/editorial_notes.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"WARN: unable to parse {path}: {exc}")
            continue
        item["__local_notes_path"] = path.relative_to(ROOT).as_posix()
        notes.append(item)
    return notes


def render_md(note: dict[str, Any]) -> str:
    today = date.today().isoformat()
    slug = note.get("slug", "")
    title = note.get("canonical_song", slug)
    return f"# {title} — Appareil éditorial des paroles\n\n" \
        f"```yaml\n" \
        f"id: {note.get('id', '')}\n" \
        f"song_id: {note.get('song_id', '')}\n" \
        f"type_unite: song_lyrics_editorial\n" \
        f"canonical_song: {scalar(title)}\n" \
        f"slug: {scalar(slug)}\n" \
        f"canonical_lyrics_source: {scalar(note.get('canonical_lyrics_source', ''))}\n" \
        f"source_page: {scalar(note.get('source_page', ''))}\n" \
        f"full_lyrics_local_path: {scalar(note.get('full_lyrics_local_path', ''))}\n" \
        f"completeness: {scalar(note.get('completeness', 'complete_local_not_versioned'))}\n" \
        f"verification_status: {scalar(note.get('verification_status', 'a_verifier'))}\n" \
        f"last_update: {scalar(today)}\n" \
        f"```\n\n" \
        "## 1. Règle d’usage\n\n" \
        "Les paroles complètes sont conservées localement et ne sont pas reproduites dans le repo. Ce fichier ne contient que des éléments éditoriaux exploitables : courts extraits, motifs, variantes décrites, notes de signification et prudences.\n\n" \
        "## 2. Courts extraits citables\n\n" \
        "```yaml\nshort_excerpts: " + yaml_list(note.get("short_excerpts", [])) + "\n```\n\n" \
        "## 3. Variantes décrites\n\n" \
        "```yaml\nvariants: " + yaml_list(note.get("variants", [])) + "\n```\n\n" \
        "## 4. Motifs et champs lexicaux\n\n" \
        "```yaml\nmotifs: " + yaml_list(note.get("motifs", [])) + "\n```\n\n" \
        "## 5. Notes éditoriales\n\n" \
        "```yaml\neditorial_notes: " + yaml_list(note.get("editorial_notes", [])) + "\n```\n\n" \
        "## 6. Chapitres liés\n\n" \
        "```yaml\nchapters: " + yaml_list(note.get("chapters", [])) + "\n```\n"


def rag_line(note: dict[str, Any]) -> dict[str, Any]:
    title = note.get("canonical_song", "")
    parts = []
    motifs = note.get("motifs") or []
    if motifs:
        parts.append("Motifs : " + ", ".join(str(x) for x in motifs[:8]))
    notes = note.get("editorial_notes") or []
    if notes:
        parts.append("Notes : " + " ; ".join(str(x) for x in notes[:4]))
    variants = note.get("variants") or []
    if variants:
        parts.append("Variantes signalées : " + str(len(variants)))
    return {
        "id": note.get("id", ""),
        "source_id": "LOCAL-LYRICS-EDITORIAL",
        "song_id": note.get("song_id", ""),
        "title": f"{title} — appareil éditorial des paroles",
        "text": " ".join(parts) or "Appareil éditorial créé, à renseigner.",
        "chapters": note.get("chapters", []),
        "tags": ["lyrics", "songbook", title],
        "file": f"songs/{note.get('slug', '')}/lyrics_editorial.md",
    }


def extract(dry_run: bool = False) -> None:
    notes = load_notes()
    index = []
    rag_lines = []
    for note in notes:
        slug = note.get("slug")
        if not slug:
            continue
        target = SONGS_ROOT / slug / "lyrics_editorial.md"
        index.append({
            "id": note.get("id", ""),
            "song_id": note.get("song_id", ""),
            "canonical_song": note.get("canonical_song", ""),
            "slug": slug,
            "lyrics_editorial_file": target.relative_to(ROOT).as_posix(),
            "canonical_lyrics_source": note.get("canonical_lyrics_source", ""),
            "source_page": note.get("source_page", ""),
            "verification_status": note.get("verification_status", "a_verifier"),
            "short_excerpts_count": len(note.get("short_excerpts") or []),
            "variants_count": len(note.get("variants") or []),
            "motifs_count": len(note.get("motifs") or []),
            "local_notes_path": note.get("__local_notes_path", ""),
        })
        rag_lines.append(rag_line(note))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_md(note), encoding="utf-8")
    if not dry_run:
        DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
        DATA_OUT.write_text(json.dumps({
            "type_unite": "songbook_lyrics_editorial_index",
            "version": "1.0",
            "updated_at": date.today().isoformat(),
            "records": index,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        RAG_OUT.parent.mkdir(parents=True, exist_ok=True)
        RAG_OUT.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rag_lines) + ("\n" if rag_lines else ""), encoding="utf-8")
    print(f"Local editorial notes read: {len(notes)}")
    print(f"Versioned editorial files prepared: {len(index)}")
    print(f"Index: {DATA_OUT.relative_to(ROOT)}")
    print(f"RAG fragments: {RAG_OUT.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract versioned editorial notes from local lyrics workspace.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    extract(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
