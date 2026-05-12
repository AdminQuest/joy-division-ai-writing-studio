#!/usr/bin/env python3
"""
Patch build_registers.py to v0.10d without regex.

This replaces infer_kind() using plain string boundaries, avoiding the Python 3.9
regex issue in patch_build_registers_v10c.py.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"

NEW_INFER_KIND = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if record_id.startswith("CONCEPT-"):\n        return "concept"\n    if record_id.startswith("MYTH-"):\n        return "myth"\n    if record_id.startswith("MOTIF-"):\n        return "motif"\n    if record_id.startswith("HIST-"):\n        return "quote_batch"\n    if "RULES" in record_id or "rules" in data:\n        return "rules"\n    if "song" in data:\n        return "song"\n    if data.get("type_unite") == "source" or (re.fullmatch(r"S\\d+", record_id) and data.get("source_label")):\n        return "source"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S") and "-" in record_id:\n        return "atom"\n    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):\n        return "metadata"\n    if not record_id and file_rel.startswith("registers/"):\n        return "template"\n    return "unknown"\n\n'''


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    if start == -1:
        raise SystemExit(f"Patch failed: start marker not found: {start_marker}")
    end = text.find(end_marker, start)
    if end == -1:
        raise SystemExit(f"Patch failed: end marker not found: {end_marker}")
    return text[:start] + replacement + text[end:]


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = text.replace("Documentary parser v0.10c", "Documentary parser v0.10d", 1)
    text = text.replace("Documentary parser v0.10b", "Documentary parser v0.10d", 1)
    text = text.replace("Documentary parser v0.10", "Documentary parser v0.10d", 1)
    text = text.replace("Documentary parser v0.9", "Documentary parser v0.10d", 1)

    if "v0.10d rewrites infer_kind without regex and classifies register templates." not in text:
        insertion = "v0.10d rewrites infer_kind without regex and classifies register templates."
        anchor = "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks."
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + insertion, 1)
        else:
            text = text.replace('"""\n\nfrom __future__', insertion + '\n"""\n\nfrom __future__', 1)

    text = replace_between(text, "def infer_kind(", "def validate_record(", NEW_INFER_KIND)

    # Validation exemption.
    for old in [
        'if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata"}:',
        'if kind in {"schema", "source"}:',
    ]:
        if old in text and "template" not in old:
            new = old[:-2] + ', "template"}:'
            text = text.replace(old, new, 1)

    # Duplicate exemption.
    if 'if kind not in {"source", "metadata"}:' in text:
        text = text.replace(
            'if kind not in {"source", "metadata"}:',
            'if kind not in {"source", "metadata", "template"}:',
            1,
        )

    # Export template records.
    if 'templates = records_by_kind(records, "template")' not in text:
        text = text.replace(
            '    metadata = records_by_kind(records, "metadata")\n    sources = build_source_registry(records)\n',
            '    metadata = records_by_kind(records, "metadata")\n    templates = records_by_kind(records, "template")\n    sources = build_source_registry(records)\n',
            1,
        )

    if 'write_json(EXPORT_DIR / "templates.json"' not in text:
        text = text.replace(
            '    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "sources.json", sources)\n',
            '    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "templates.json", [asdict(r) for r in templates])\n    write_json(EXPORT_DIR / "sources.json", sources)\n',
            1,
        )

    if 'write_csv(EXPORT_DIR / "templates.csv"' not in text:
        text = text.replace(
            '    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n',
            '    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    write_csv(EXPORT_DIR / "templates.csv", templates, ["id", "name", "role", "sources", "certainty", "date", "event", "type"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n',
            1,
        )

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.10d")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
