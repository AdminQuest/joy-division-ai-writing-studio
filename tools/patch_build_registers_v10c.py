#!/usr/bin/env python3
"""
Robustly patch build_registers.py to v0.10c by rewriting infer_kind().

This avoids fragile string matching around the final return "unknown".
It replaces the whole infer_kind function between:

    def infer_kind(...)

and:

    def validate_record(...)

Then it ensures template records are exported and not validated as unknowns.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"

NEW_INFER_KIND = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if record_id.startswith("CONCEPT-"):\n        return "concept"\n    if record_id.startswith("MYTH-"):\n        return "myth"\n    if record_id.startswith("MOTIF-"):\n        return "motif"\n    if record_id.startswith("HIST-"):\n        return "quote_batch"\n    if "RULES" in record_id or "rules" in data:\n        return "rules"\n    if "song" in data:\n        return "song"\n    if data.get("type_unite") == "source" or (re.fullmatch(r"S\\d+", record_id) and data.get("source_label")):\n        return "source"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S") and "-" in record_id:\n        return "atom"\n    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):\n        return "metadata"\n    if not record_id and file_rel.startswith("registers/"):\n        return "template"\n    return "unknown"\n\n'''


def replace_function(text: str, name: str, replacement: str, next_name: str) -> str:
    pattern = re.compile(
        rf"def {name}\\(.*?\\n(?=def {next_name}\\()",
        flags=re.DOTALL,
    )
    new_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Patch failed: could not replace function {name}")
    return new_text


def ensure_replace(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = re.sub(r"Documentary parser v0\\.\d+(?:b|c)?", "Documentary parser v0.10c", text, count=1)
    if "v0.10c rewrites infer_kind to classify register templates." not in text:
        text = text.replace(
            "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.",
            "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.\n"
            "v0.10c rewrites infer_kind to classify register templates.",
            1,
        )

    text = replace_function(text, "infer_kind", NEW_INFER_KIND, "validate_record")

    text = ensure_replace(
        text,
        'if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata"}:',
        'if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata", "template"}:',
    )
    text = ensure_replace(
        text,
        'if kind in {"schema", "source"}:',
        'if kind in {"schema", "source", "template"}:',
    )

    text = ensure_replace(
        text,
        'if kind not in {"source", "metadata"}:',
        'if kind not in {"source", "metadata", "template"}:',
    )

    if 'templates = records_by_kind(records, "template")' not in text:
        text = ensure_replace(
            text,
            '    metadata = records_by_kind(records, "metadata")\n    sources = build_source_registry(records)\n',
            '    metadata = records_by_kind(records, "metadata")\n    templates = records_by_kind(records, "template")\n    sources = build_source_registry(records)\n',
        )

    if 'write_json(EXPORT_DIR / "templates.json"' not in text:
        text = ensure_replace(
            text,
            '    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "sources.json", sources)\n',
            '    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "templates.json", [asdict(r) for r in templates])\n    write_json(EXPORT_DIR / "sources.json", sources)\n',
        )

    if 'write_csv(EXPORT_DIR / "templates.csv"' not in text:
        text = ensure_replace(
            text,
            '    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n',
            '    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    write_csv(EXPORT_DIR / "templates.csv", templates, ["id", "name", "role", "sources", "certainty", "date", "event", "type"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n',
        )

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.10c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
