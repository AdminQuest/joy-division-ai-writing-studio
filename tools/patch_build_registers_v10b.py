#!/usr/bin/env python3
"""
Robust patch build_registers.py to v0.10b.

The first v0.10 patch expected an exact infer_kind() block and can fail if the
local parser has already been changed by earlier patches. This version applies
small, robust replacements:

- insert template classification immediately before return "unknown";
- exempt template records from schema diagnostics and duplicate checks;
- add templates.json / templates.csv exports if the build_exports() function has
  the v0.9 export blocks.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    # Version banner, tolerant of v0.9/v0.10 leftovers.
    text = text.replace("Documentary parser v0.9", "Documentary parser v0.10b", 1)
    text = text.replace("Documentary parser v0.10", "Documentary parser v0.10b", 1)
    if "v0.10b classifies empty register schema examples as template records." not in text:
        text = text.replace(
            "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.",
            "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.\n"
            "v0.10b classifies empty register schema examples as template records.",
            1,
        )

    # Insert template classification before the first return unknown in infer_kind.
    template_rule = '    if not record_id and file_rel.startswith("registers/"):\n        return "template"\n'
    if template_rule not in text:
        marker = '    return "unknown"\n\ndef validate_record'
        if marker not in text:
            raise SystemExit('Patch failed: could not find infer_kind return "unknown" marker')
        text = text.replace(marker, template_rule + '    return "unknown"\n\ndef validate_record', 1)

    # Exempt template from validation diagnostics.
    text = text.replace(
        'if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata"}:',
        'if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata", "template"}:',
        1,
    )

    # If still v0.6-style, replace schema-only exemption.
    text = text.replace(
        'if kind in {"schema", "source"}:',
        'if kind in {"schema", "source", "template"}:',
        1,
    )

    # Exempt template from duplicate checks.
    text = text.replace(
        'if kind not in {"source", "metadata"}:',
        'if kind not in {"source", "metadata", "template"}:',
        1,
    )

    # Add template collection in build_exports.
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
    print("Patched tools/build_registers.py to v0.10b")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
