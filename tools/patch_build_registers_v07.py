#!/usr/bin/env python3
"""
Patch build_registers.py to v0.7.

This is a targeted maintenance patch for the documentary parser.
It fixes three issues revealed by audit_repo.py:

1. nested YAML fields are wrongly de-indented by normalize_yaml();
2. source-level YAML blocks such as id: S69 are treated as atoms;
3. duplicate checks should not report source records as duplicate atoms.

Run once from the repository root:

    python3 tools/patch_build_registers_v07.py
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
        "Joy Division AI Writing Studio — Documentary parser v0.6",
        "Joy Division AI Writing Studio — Documentary parser v0.7",
        1,
    )
    text = text.replace(
        "v0.6 produces a permanent, structured diagnostic report even when no error is found.",
        "v0.6 produces a permanent, structured diagnostic report even when no error is found.\n"
        "v0.7 fixes YAML normalization, source record classification, and duplicate checks.",
        1,
    )

    old_normalize_yaml = '''def normalize_yaml(raw: str) -> str:\n    fixed_lines: List[str] = []\n    mapping_line = re.compile(r"^(\\s*)([A-Za-z_][A-Za-z0-9_\\-]*:\\s*)(.+?)\\s*$")\n    for line in raw.splitlines():\n        key_match = re.match(r"^\\s+([A-Za-z_][A-Za-z0-9_\\-]*):", line)\n        if key_match and key_match.group(1) in KNOWN_TOPLEVEL_KEYS:\n            line = line.lstrip()\n        match = mapping_line.match(line)\n        if not match:\n            fixed_lines.append(line)\n            continue\n        indent, key_prefix, value = match.groups()\n        stripped = value.strip()\n        if not stripped or stripped[0] in {'\\\"', "'", "[", "{", "|", ">"}:\n            fixed_lines.append(line)\n            continue\n        if ": " not in stripped:\n            fixed_lines.append(line)\n            continue\n        escaped = stripped.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')\n        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')\n    return "\\n".join(fixed_lines)\n'''

    new_normalize_yaml = '''def normalize_yaml(raw: str) -> str:\n    """Normalize unsafe one-line scalars while preserving YAML indentation.\n\n    Earlier versions de-indented known top-level keys. That broke valid nested\n    objects such as:\n\n        niveau_preuve:\n          statut: corrobore\n          corroboration: moyenne\n\n    The parser must never change indentation. It only quotes plain scalar values\n    containing an internal ': ' sequence, because those are unsafe for PyYAML.\n    """\n    fixed_lines: List[str] = []\n    mapping_line = re.compile(r"^(\\s*)([A-Za-z_][A-Za-z0-9_\\-]*:\\s*)(.+?)\\s*$")\n    for line in raw.splitlines():\n        match = mapping_line.match(line)\n        if not match:\n            fixed_lines.append(line)\n            continue\n        indent, key_prefix, value = match.groups()\n        stripped = value.strip()\n        if not stripped or stripped[0] in {'\\\"', "'", "[", "{", "|", ">"}:\n            fixed_lines.append(line)\n            continue\n        if ": " not in stripped:\n            fixed_lines.append(line)\n            continue\n        escaped = stripped.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')\n        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')\n    return "\\n".join(fixed_lines)\n'''

    text = replace_exact(text, old_normalize_yaml, new_normalize_yaml, "normalize_yaml")

    old_infer_kind = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if "song" in data:\n        return "song"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S"):\n        return "atom"\n    return "unknown"\n'''

    new_infer_kind = '''def infer_kind(data: Dict[str, Any], file_path: Path) -> str:\n    file_rel = rel(file_path)\n    if "schema" in data:\n        return "schema"\n    record_id = str(data.get("id", ""))\n    if record_id.startswith("CHR-"):\n        return "chronology"\n    if record_id.startswith("PERS-"):\n        return "person"\n    if "song" in data:\n        return "song"\n    if data.get("type_unite") == "source" or (re.fullmatch(r"S\\d+", record_id) and data.get("source_label")):\n        return "source"\n    if "-Q" in record_id or "citations_exactes" in file_rel:\n        return "quote"\n    if record_id.startswith("S") and "-" in record_id:\n        return "atom"\n    return "unknown"\n'''

    text = replace_exact(text, old_infer_kind, new_infer_kind, "infer_kind")

    text = text.replace(
        '''    if kind == "schema":\n        return diagnostics\n''',
        '''    if kind in {"schema", "source"}:\n        return diagnostics\n''',
        1,
    )

    text = text.replace(
        '''            if record_id in seen_ids:\n                diagnostics.append(Diagnostic("error", rel(path), f"Duplicate id also found in {seen_ids[record_id]}", record_id))\n            else:\n                seen_ids[record_id] = rel(path)\n            records.append(ParsedRecord(kind=kind, id=record_id, file=rel(path), heading=heading, data=data))\n''',
        '''            if kind != "source":\n                if record_id in seen_ids:\n                    diagnostics.append(Diagnostic("error", rel(path), f"Duplicate id also found in {seen_ids[record_id]}", record_id))\n                else:\n                    seen_ids[record_id] = rel(path)\n            records.append(ParsedRecord(kind=kind, id=record_id, file=rel(path), heading=heading, data=data))\n''',
        1,
    )

    text = text.replace(
        '''        if data.get("source_id"):\n            ids.append(data["source_id"])\n        if isinstance(data.get("sources"), list):\n''',
        '''        if data.get("source_id"):\n            ids.append(data["source_id"])\n        if record.kind == "source" and data.get("id"):\n            ids.append(data["id"])\n        if isinstance(data.get("sources"), list):\n''',
        1,
    )

    text = text.replace(
        '''        if isinstance(data.get("source_id"), str):\n            used.add(normalize_identifier(data["source_id"]))\n        if isinstance(data.get("sources"), list):\n''',
        '''        if isinstance(data.get("source_id"), str):\n            used.add(normalize_identifier(data["source_id"]))\n        if record.kind == "source" and isinstance(data.get("id"), str) and re.fullmatch(r"S\\d+", data["id"]):\n            used.add(normalize_identifier(data["id"]))\n        if isinstance(data.get("sources"), list):\n''',
        1,
    )

    text = text.replace(
        '''    errors = [d for d in diagnostics if d.level == "error"]\n    warnings = [d for d in diagnostics if d.level == "warning"]\n    print(f"errors      : {len(errors)}")\n    print(f"warnings    : {len(warnings)}")\n    print(f"exports     : {rel(EXPORT_DIR)}")\n    if diagnostics:\n        print("\\nDiagnostics:")\n        for diag in diagnostics[:50]:\n''',
        '''    errors = [d for d in diagnostics if d.level == "error"]\n    warnings = [d for d in diagnostics if d.level == "warning"]\n    unknowns = [d for d in diagnostics if d.message == "Unable to infer documentary kind"]\n    print(f"errors      : {len(errors)}")\n    print(f"warnings    : {len(warnings)}")\n    print(f"unknown     : {len(unknowns)}")\n    print(f"exports     : {rel(EXPORT_DIR)}")\n    if diagnostics:\n        ordered = errors + [d for d in diagnostics if d.level != "error"]\n        print("\\nDiagnostics:")\n        for diag in ordered[:50]:\n''',
        1,
    )

    text = text.replace("for diag in diagnostics[:50]:", "for diag in ordered[:50]:", 1)

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
