#!/usr/bin/env python3
"""
Patch build_registers.py to v0.9.

This patch treats the remaining 'unknown' records as explicit documentary kinds
instead of parser failures:

- concept      CONCEPT-*
- myth         MYTH-*
- motif        MOTIF-*
- quote_batch  HIST-*
- rules        *RULES*
- metadata     README / coverage / chapters / source metadata blocks without id

It also creates dedicated JSON/CSV exports for concept, myth, motif, rules,
metadata and source records.

Run from repository root:

    python3 tools/patch_build_registers_v09.py
    python3 tools/build_registers.py
    python3 tools/audit_repo.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Patch failed: block not found for {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = text.replace(
        "Joy Division AI Writing Studio — Documentary parser v0.8",
        "Joy Division AI Writing Studio — Documentary parser v0.9",
        1,
    )
    text = text.replace(
        "v0.8 tolerates one-space legacy top-level indentation and avoids false source-usage alerts.",
        "v0.8 tolerates one-space legacy top-level indentation and avoids false source-usage alerts.\n"
        "v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.",
        1,
    )

    old_infer_kind_v08 = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if "song" in data:\n        return "song"\n    if data.get("type_unite") == "source" or (re.fullmatch(r"S\\d+", record_id) and data.get("source_label")):\n        return "source"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S") and "-" in record_id:\n        return "atom"\n    return "unknown"\n'''

    old_infer_kind_v06 = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if "song" in data:\n        return "song"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S"):\n        return "atom"\n    return "unknown"\n'''

    new_infer_kind_v09 = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if record_id.startswith("CONCEPT-"):\n        return "concept"\n    if record_id.startswith("MYTH-"):\n        return "myth"\n    if record_id.startswith("MOTIF-"):\n        return "motif"\n    if record_id.startswith("HIST-"):\n        return "quote_batch"\n    if "RULES" in record_id or "rules" in data:\n        return "rules"\n    if "song" in data:\n        return "song"\n    if data.get("type_unite") == "source" or (re.fullmatch(r"S\\d+", record_id) and data.get("source_label")):\n        return "source"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S") and "-" in record_id:\n        return "atom"\n    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):\n        return "metadata"\n    return "unknown"\n'''

    if old_infer_kind_v08 in text:
        text = text.replace(old_infer_kind_v08, new_infer_kind_v09, 1)
    elif old_infer_kind_v06 in text:
        text = text.replace(old_infer_kind_v06, new_infer_kind_v09, 1)
    else:
        raise SystemExit("Patch failed: infer_kind block not found")

    text = text.replace(
        '''    if kind in {"schema", "source"}:\n        return diagnostics\n''',
        '''    if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata"}:\n        return diagnostics\n''',
        1,
    )

    text = text.replace(
        '''            if kind != "source":\n                if record_id in seen_ids:\n                    diagnostics.append(Diagnostic("error", rel(path), f"Duplicate id also found in {seen_ids[record_id]}", record_id))\n                else:\n                    seen_ids[record_id] = rel(path)\n            records.append(ParsedRecord(kind=kind, id=record_id, file=rel(path), heading=heading, data=data))\n''',
        '''            if kind not in {"source", "metadata"}:\n                if record_id in seen_ids:\n                    diagnostics.append(Diagnostic("error", rel(path), f"Duplicate id also found in {seen_ids[record_id]}", record_id))\n                else:\n                    seen_ids[record_id] = rel(path)\n            records.append(ParsedRecord(kind=kind, id=record_id, file=rel(path), heading=heading, data=data))\n''',
        1,
    )

    # Add generated collections for new kinds.
    text = text.replace(
        '''    songs = records_by_kind(records, "song")\n    people = records_by_kind(records, "person")\n    sources = build_source_registry(records)\n''',
        '''    songs = records_by_kind(records, "song")\n    people = records_by_kind(records, "person")\n    source_records = records_by_kind(records, "source")\n    concepts = records_by_kind(records, "concept")\n    myths = records_by_kind(records, "myth")\n    motifs = records_by_kind(records, "motif")\n    quote_batches = records_by_kind(records, "quote_batch")\n    rules = records_by_kind(records, "rules")\n    metadata = records_by_kind(records, "metadata")\n    sources = build_source_registry(records)\n''',
        1,
    )

    text = text.replace(
        '''    write_json(EXPORT_DIR / "people.json", [asdict(r) for r in people])\n    write_json(EXPORT_DIR / "sources.json", sources)\n''',
        '''    write_json(EXPORT_DIR / "people.json", [asdict(r) for r in people])\n    write_json(EXPORT_DIR / "source_records.json", [asdict(r) for r in source_records])\n    write_json(EXPORT_DIR / "concepts.json", [asdict(r) for r in concepts])\n    write_json(EXPORT_DIR / "myths.json", [asdict(r) for r in myths])\n    write_json(EXPORT_DIR / "motifs.json", [asdict(r) for r in motifs])\n    write_json(EXPORT_DIR / "quote_batches.json", [asdict(r) for r in quote_batches])\n    write_json(EXPORT_DIR / "rules.json", [asdict(r) for r in rules])\n    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])\n    write_json(EXPORT_DIR / "sources.json", sources)\n''',
        1,
    )

    text = text.replace(
        '''    write_csv(EXPORT_DIR / "people.csv", people, ["name", "full_name", "role", "sources", "chapters", "certainty"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n''',
        '''    write_csv(EXPORT_DIR / "people.csv", people, ["name", "full_name", "role", "sources", "chapters", "certainty"])\n    write_csv(EXPORT_DIR / "source_records.csv", source_records, ["source_id", "source_label", "auteur", "titre", "source_year", "nature", "status", "priority"])\n    write_csv(EXPORT_DIR / "concepts.csv", concepts, ["id", "nom", "name", "definition", "filiation", "niveau_consensus", "chapitres", "sources"])\n    write_csv(EXPORT_DIR / "myths.csv", myths, ["id", "mythe", "name", "niveau_risque", "correction", "chapitres", "sources"])\n    write_csv(EXPORT_DIR / "motifs.csv", motifs, ["id", "motif", "name", "definition", "chapitres", "sources"])\n    write_csv(EXPORT_DIR / "quote_batches.csv", quote_batches, ["id", "lot", "source_file", "rows_imported", "chapitres", "statut_consolidation"])\n    write_csv(EXPORT_DIR / "rules.csv", rules, ["id", "statut_consolidation", "rules"])\n    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])\n    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]\n''',
        1,
    )

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.9")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
