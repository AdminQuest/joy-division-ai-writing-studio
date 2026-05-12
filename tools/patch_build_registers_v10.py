#!/usr/bin/env python3
"""
Patch build_registers.py to v0.10.

This finalizes the treatment of unknown YAML blocks by classifying empty schema
examples in register master files as 'template' records.

The parser should then report zero 'unknown' blocks while preserving source,
atom and register semantics.

Run from repository root:

    python3 tools/patch_build_registers_v10.py
    python3 tools/build_registers.py --strict
    python3 tools/audit_repo.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = text.replace(
        "Joy Division AI Writing Studio — Documentary parser v0.9",
        "Joy Division AI Writing Studio — Documentary parser v0.10",
        1,
    )
    text = text.replace(
        "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.",
        "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.\n"
        "v0.10 classifies empty register schema examples as template records.",
        1,
    )

    old = '''    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):\n        return "metadata"\n    return "unknown"\n'''
    new = '''    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):\n        return "metadata"\n    if not record_id and file_rel.startswith("registers/"):\n        return "template"\n    return "unknown"\n'''
    if old not in text:
        raise SystemExit("Patch failed: infer_kind metadata block not found")
    text = text.replace(old, new, 1)

    text = text.replace(
        '''    if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata"}:\n        return diagnostics\n''',
        '''    if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata", "template"}:\n        return diagnostics\n''',
        1,
    )

    text = text.replace(
        '''            if kind not in {"source", "metadata"}:\n''',
        '''            if kind not in {"source", "metadata", "template"}:\n''',
        1,
    )

    text = text.replace(
        '''    metadata = records_by_kind(records, "metadata")\n    sources = build_source_registry(records)\n''',
        '''    metadata = records_by_kind(records, "metadata")\n    templates = records_by_kind(records, "template")\n    sources = build_source_registry(records)\n''',
        1,
    )

    text = text.replace(
        '''    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "sources.json", sources)\n''',
        '''    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "templates.json", [asdict(r) for r in templates])\n    write_json(EXPORT_DIR / "sources.json", sources)\n''',
        1,
    )

    text = text.replace(
        '''    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n''',
        '''    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    write_csv(EXPORT_DIR / "templates.csv", templates, ["id", "name", "role", "sources", "certainty", "date", "event", "type"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n''',
        1,
    )

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.10")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
