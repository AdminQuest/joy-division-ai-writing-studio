#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Documentary parser v0.1

Purpose
-------
This script scans the repository Markdown files, extracts fenced YAML blocks,
classifies them by documentary type, validates basic IDs, and generates machine-readable
exports for future register synchronization and RAG indexing.

It does NOT rewrite the Markdown registers yet.
It creates derived files under `exports/generated/`.

Current outputs
---------------
- exports/generated/atoms.json
- exports/generated/quotes.json
- exports/generated/chronology.json
- exports/generated/songs.json
- exports/generated/people.json
- exports/generated/all_records.json
- exports/generated/index_by_id.json
- exports/generated/diagnostics.json
- exports/generated/atoms.csv
- exports/generated/quotes.csv
- exports/generated/chronology.csv
- exports/generated/songs.csv
- exports/generated/people.csv

Usage
-----
From repository root:

    python tools/build_registers.py

Optional:

    python tools/build_registers.py --strict

Dependencies
------------
Requires PyYAML:

    pip install pyyaml

Design principles
-----------------
- Markdown remains the human-readable source.
- YAML blocks are the machine-readable layer.
- Exports are generated artifacts, not primary sources.
- The parser is deliberately conservative: it reports anomalies instead of silently fixing them.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: PyYAML. Install it with: pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "exports" / "generated"

SCAN_DIRS = [
    REPO_ROOT / "sources",
    REPO_ROOT / "registers",
]

YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)

ID_PREFIX_KIND = {
    "S": "atom_or_quote",
    "CHR": "chronology",
    "PERS": "person",
}


@dataclass
class ParsedRecord:
    kind: str
    id: str
    file: str
    heading: Optional[str]
    data: Dict[str, Any]


@dataclass
class Diagnostic:
    level: str
    file: str
    message: str
    record_id: Optional[str] = None


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def iter_markdown_files() -> Iterable[Path]:
    for directory in SCAN_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*.md"):
            if "exports/generated" in rel(path):
                continue
            yield path


def nearest_heading(text: str, pos: int) -> Optional[str]:
    before = text[:pos]
    headings = re.findall(r"^(#{1,6})\s+(.+?)\s*$", before, flags=re.MULTILINE)
    if not headings:
        return None
    return headings[-1][1].strip()


def extract_yaml_blocks(path: Path) -> List[Tuple[Dict[str, Any], Optional[str], str]]:
    text = path.read_text(encoding="utf-8")
    blocks: List[Tuple[Dict[str, Any], Optional[str], str]] = []
    for match in YAML_BLOCK_RE.finditer(text):
        raw = match.group(1).strip()
        heading = nearest_heading(text, match.start())
        if not raw:
            continue
        try:
            loaded = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            blocks.append(({"__parse_error__": str(exc), "__raw__": raw}, heading, raw))
            continue
        if isinstance(loaded, dict):
            blocks.append((loaded, heading, raw))
        else:
            blocks.append(({"__non_mapping__": loaded, "__raw__": raw}, heading, raw))
    return blocks


def infer_kind(data: Dict[str, Any], file_path: Path) -> str:
    file_rel = rel(file_path)

    if "schema" in data:
        return "schema"

    if data.get("id", "").startswith("CHR-"):
        return "chronology"

    if data.get("id", "").startswith("PERS-"):
        return "person"

    if "song" in data:
        return "song"

    record_id = str(data.get("id", ""))
    if "-Q" in record_id or "citations_exactes" in file_rel:
        return "quote"

    if record_id.startswith("S"):
        return "atom"

    return "unknown"


def validate_record(kind: str, data: Dict[str, Any], file_path: Path) -> List[Diagnostic]:
    diagnostics: List[Diagnostic] = []
    file_rel = rel(file_path)
    record_id = str(data.get("id", "")) if data.get("id") is not None else None

    if "__parse_error__" in data:
        return [Diagnostic("error", file_rel, f"YAML parse error: {data['__parse_error__']}", None)]

    if "__non_mapping__" in data:
        return [Diagnostic("warning", file_rel, "YAML block is not a mapping/object", None)]

    if kind not in {"schema", "song"} and not data.get("id"):
        diagnostics.append(Diagnostic("warning", file_rel, "Missing id", None))

    if kind == "atom":
        required = ["id", "source_id", "type_unite"]
        for key in required:
            if key not in data:
                diagnostics.append(Diagnostic("warning", file_rel, f"Atom missing required key: {key}", record_id))

    if kind == "quote":
        required = ["id", "source_id", "citation_originale", "langue_originale"]
        for key in required:
            if key not in data:
                diagnostics.append(Diagnostic("warning", file_rel, f"Quote missing required key: {key}", record_id))

    if kind == "chronology":
        required = ["id", "date", "event", "type", "sources", "certainty"]
        for key in required:
            if key not in data:
                diagnostics.append(Diagnostic("warning", file_rel, f"Chronology event missing required key: {key}", record_id))

    if kind == "person":
        required = ["id", "name", "role", "sources"]
        for key in required:
            if key not in data:
                diagnostics.append(Diagnostic("warning", file_rel, f"Person missing required key: {key}", record_id))

    if kind == "song":
        required = ["song", "themes", "sources", "chapters"]
        for key in required:
            if key not in data:
                diagnostics.append(Diagnostic("warning", file_rel, f"Song missing required key: {key}", str(data.get("song"))))

    return diagnostics


def parse_repository() -> Tuple[List[ParsedRecord], List[Diagnostic]]:
    records: List[ParsedRecord] = []
    diagnostics: List[Diagnostic] = []
    seen_ids: Dict[str, str] = {}

    for path in iter_markdown_files():
        for data, heading, _raw in extract_yaml_blocks(path):
            kind = infer_kind(data, path)
            diagnostics.extend(validate_record(kind, data, path))

            if kind == "schema":
                continue

            record_id = str(data.get("id") or data.get("song") or "")
            if not record_id:
                record_id = f"NO_ID::{rel(path)}::{len(records) + 1}"

            if record_id in seen_ids:
                diagnostics.append(
                    Diagnostic(
                        "error",
                        rel(path),
                        f"Duplicate id also found in {seen_ids[record_id]}",
                        record_id,
                    )
                )
            else:
                seen_ids[record_id] = rel(path)

            records.append(
                ParsedRecord(
                    kind=kind,
                    id=record_id,
                    file=rel(path),
                    heading=heading,
                    data=data,
                )
            )

    return records, diagnostics


def records_by_kind(records: List[ParsedRecord], kind: str) -> List[ParsedRecord]:
    return [record for record in records if record.kind == kind]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False), encoding="utf-8")


def flatten_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def write_csv(path: Path, records: List[ParsedRecord], preferred_fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["kind", "id", "file", "heading"] + preferred_fields

    # Include any additional top-level keys found in the records.
    extra_keys = []
    for record in records:
        for key in record.data.keys():
            if key not in preferred_fields and key not in {"id"} and key not in extra_keys:
                extra_keys.append(key)
    fields += extra_keys

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = {
                "kind": record.kind,
                "id": record.id,
                "file": record.file,
                "heading": record.heading or "",
            }
            for key in fields:
                if key in row:
                    continue
                row[key] = flatten_value(record.data.get(key))
            writer.writerow(row)


def build_exports(records: List[ParsedRecord], diagnostics: List[Diagnostic]) -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    atoms = records_by_kind(records, "atom")
    quotes = records_by_kind(records, "quote")
    chronology = records_by_kind(records, "chronology")
    songs = records_by_kind(records, "song")
    people = records_by_kind(records, "person")

    all_payload = [asdict(record) for record in records]
    index_by_id = {record.id: asdict(record) for record in records}

    write_json(EXPORT_DIR / "atoms.json", [asdict(r) for r in atoms])
    write_json(EXPORT_DIR / "quotes.json", [asdict(r) for r in quotes])
    write_json(EXPORT_DIR / "chronology.json", [asdict(r) for r in chronology])
    write_json(EXPORT_DIR / "songs.json", [asdict(r) for r in songs])
    write_json(EXPORT_DIR / "people.json", [asdict(r) for r in people])
    write_json(EXPORT_DIR / "all_records.json", all_payload)
    write_json(EXPORT_DIR / "index_by_id.json", index_by_id)
    write_json(EXPORT_DIR / "diagnostics.json", [asdict(d) for d in diagnostics])

    write_csv(EXPORT_DIR / "atoms.csv", atoms, ["source_id", "auteur", "titre", "pages_pdf", "type_unite", "concepts", "chapitres", "statut", "fiabilite"])
    write_csv(EXPORT_DIR / "quotes.csv", quotes, ["source_id", "citation_originale", "traduction_editoriale_fr", "page_pdf", "langue_originale", "importance"])
    write_csv(EXPORT_DIR / "chronology.csv", chronology, ["date", "precision_date", "event", "type", "location", "people", "songs", "sources", "certainty"])
    write_csv(EXPORT_DIR / "songs.csv", songs, ["song", "period", "themes", "sources", "chapters", "certainty"])
    write_csv(EXPORT_DIR / "people.csv", people, ["name", "full_name", "role", "sources", "chapters", "certainty"])


def print_summary(records: List[ParsedRecord], diagnostics: List[Diagnostic]) -> None:
    counts: Dict[str, int] = {}
    for record in records:
        counts[record.kind] = counts.get(record.kind, 0) + 1

    print("Documentary parser summary")
    print("---------------------------")
    for kind in sorted(counts):
        print(f"{kind:12s}: {counts[kind]}")

    errors = [d for d in diagnostics if d.level == "error"]
    warnings = [d for d in diagnostics if d.level == "warning"]
    print(f"errors      : {len(errors)}")
    print(f"warnings    : {len(warnings)}")
    print(f"exports     : {rel(EXPORT_DIR)}")

    if diagnostics:
        print("\nDiagnostics:")
        for diag in diagnostics[:50]:
            suffix = f" [{diag.record_id}]" if diag.record_id else ""
            print(f"- {diag.level.upper()} {diag.file}{suffix}: {diag.message}")
        if len(diagnostics) > 50:
            print(f"... {len(diagnostics) - 50} additional diagnostics written to diagnostics.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build documentary exports from Markdown/YAML records.")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if errors are found.")
    args = parser.parse_args()

    records, diagnostics = parse_repository()
    build_exports(records, diagnostics)
    print_summary(records, diagnostics)

    if args.strict and any(d.level == "error" for d in diagnostics):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
