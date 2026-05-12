#!/usr/bin/env python3
"""
Patch build_registers.py to v0.8.

This patch completes the parser hardening started in v0.7:

1. tolerate legacy YAML blocks with exactly one accidental leading space before a
   top-level key, e.g. ' type_unite: fait';
2. do not count source-level records as documentary usage of a source. Source
   records describe the registry; they must not inflate 'sources_used_in_records'
   or create false 'used_but_missing_from_registre_json' alerts.

Run from the repository root:

    python3 tools/patch_build_registers_v08.py
    python3 tools/build_registers.py
    python3 tools/audit_repo.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_registers.py"

KNOWN_TOPLEVEL_KEYS_LITERAL = '''KNOWN_TOPLEVEL_KEYS = {
    "id", "source_id", "auteur", "titre", "source_titre", "source_label", "source_short_title", "source_year",
    "pages_pdf", "page_pdf", "type_unite", "concepts", "chapitres", "statut", "fiabilite", "citation_directe",
    "citation_originale", "traduction_editoriale_fr", "langue_originale", "importance", "statut_verification",
    "date", "precision_date", "event", "type", "location", "people", "songs", "sources", "certainty", "song",
    "period", "themes", "chapters", "name", "full_name", "role", "notes",
    "role_argumentatif", "niveau_preuve", "stabilite", "risque_surinterpretation", "liens_interchapitres",
    "liens_citations", "motifs", "concepts_derives", "charge_emotionnelle", "nature_discursive",
    "usages_redactionnels", "contradictions", "limites_usage", "legacy_id", "related_places", "related_sources"
}
'''


def replace_exact(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Patch failed: block not found for {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = text.replace(
        "Joy Division AI Writing Studio — Documentary parser v0.7",
        "Joy Division AI Writing Studio — Documentary parser v0.8",
        1,
    )
    text = text.replace(
        "v0.7 fixes YAML normalization, source record classification, and duplicate checks.",
        "v0.7 fixes YAML normalization, source record classification, and duplicate checks.\n"
        "v0.8 tolerates one-space legacy top-level indentation and avoids false source-usage alerts.",
        1,
    )

    if "KNOWN_TOPLEVEL_KEYS" not in text:
        marker = 'YAML_BLOCK_RE = re.compile(r"```yaml\\s*(.*?)\\s*```", re.DOTALL | re.IGNORECASE)\n\n'
        text = text.replace(marker, marker + KNOWN_TOPLEVEL_KEYS_LITERAL + "\n", 1)

    old_normalize_yaml_v07 = '''def normalize_yaml(raw: str) -> str:\n    """Normalize unsafe one-line scalars while preserving YAML indentation.\n\n    Earlier versions de-indented known top-level keys. That broke valid nested\n    objects such as:\n\n        niveau_preuve:\n          statut: corrobore\n          corroboration: moyenne\n\n    The parser must never change indentation. It only quotes plain scalar values\n    containing an internal ': ' sequence, because those are unsafe for PyYAML.\n    """\n    fixed_lines: List[str] = []\n    mapping_line = re.compile(r"^(\\s*)([A-Za-z_][A-Za-z0-9_\\-]*:\\s*)(.+?)\\s*$")\n    for line in raw.splitlines():\n        match = mapping_line.match(line)\n        if not match:\n            fixed_lines.append(line)\n            continue\n        indent, key_prefix, value = match.groups()\n        stripped = value.strip()\n        if not stripped or stripped[0] in {'\\\"', "'", "[", "{", "|", ">"}:\n            fixed_lines.append(line)\n            continue\n        if ": " not in stripped:\n            fixed_lines.append(line)\n            continue\n        escaped = stripped.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')\n        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')\n    return "\\n".join(fixed_lines)\n'''

    old_normalize_yaml_v06 = '''def normalize_yaml(raw: str) -> str:\n    fixed_lines: List[str] = []\n    mapping_line = re.compile(r"^(\\s*)([A-Za-z_][A-Za-z0-9_\\-]*:\\s*)(.+?)\\s*$")\n    for line in raw.splitlines():\n        key_match = re.match(r"^\\s+([A-Za-z_][A-Za-z0-9_\\-]*):", line)\n        if key_match and key_match.group(1) in KNOWN_TOPLEVEL_KEYS:\n            line = line.lstrip()\n        match = mapping_line.match(line)\n        if not match:\n            fixed_lines.append(line)\n            continue\n        indent, key_prefix, value = match.groups()\n        stripped = value.strip()\n        if not stripped or stripped[0] in {'\\\"', "'", "[", "{", "|", ">"}:\n            fixed_lines.append(line)\n            continue\n        if ": " not in stripped:\n            fixed_lines.append(line)\n            continue\n        escaped = stripped.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')\n        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')\n    return "\\n".join(fixed_lines)\n'''

    new_normalize_yaml_v08 = '''def normalize_yaml(raw: str) -> str:\n    """Normalize unsafe one-line scalars while preserving valid YAML nesting.\n\n    The parser accepts a narrow legacy defect: exactly one accidental leading\n    space before a known top-level key, for example ' type_unite: fait'.\n    It does not de-indent valid nested fields, which normally use two spaces.\n    """\n    fixed_lines: List[str] = []\n    mapping_line = re.compile(r"^(\\s*)([A-Za-z_][A-Za-z0-9_\\-]*:\\s*)(.+?)\\s*$")\n    one_space_top_key = re.compile(r"^ ([A-Za-z_][A-Za-z0-9_\\-]*):")\n    for line in raw.splitlines():\n        top_key = one_space_top_key.match(line)\n        if top_key and top_key.group(1) in KNOWN_TOPLEVEL_KEYS:\n            line = line[1:]\n        match = mapping_line.match(line)\n        if not match:\n            fixed_lines.append(line)\n            continue\n        indent, key_prefix, value = match.groups()\n        stripped = value.strip()\n        if not stripped or stripped[0] in {'\\\"', "'", "[", "{", "|", ">"}:\n            fixed_lines.append(line)\n            continue\n        if ": " not in stripped:\n            fixed_lines.append(line)\n            continue\n        escaped = stripped.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')\n        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')\n    return "\\n".join(fixed_lines)\n'''

    if old_normalize_yaml_v07 in text:
        text = text.replace(old_normalize_yaml_v07, new_normalize_yaml_v08, 1)
    elif old_normalize_yaml_v06 in text:
        text = text.replace(old_normalize_yaml_v06, new_normalize_yaml_v08, 1)
    else:
        raise SystemExit("Patch failed: normalize_yaml block not found")

    # Build registry must not count source records as documentary use.
    text = text.replace(
        '''        if data.get("source_id"):\n            ids.append(data["source_id"])\n        if record.kind == "source" and data.get("id"):\n            ids.append(data["id"])\n        if isinstance(data.get("sources"), list):\n''',
        '''        if data.get("source_id"):\n            ids.append(data["source_id"])\n        if isinstance(data.get("sources"), list):\n''',
        1,
    )

    text = text.replace(
        '''        if isinstance(data.get("source_id"), str):\n            used.add(normalize_identifier(data["source_id"]))\n        if record.kind == "source" and isinstance(data.get("id"), str) and re.fullmatch(r"S\\d+", data["id"]):\n            used.add(normalize_identifier(data["id"]))\n        if isinstance(data.get("sources"), list):\n''',
        '''        if isinstance(data.get("source_id"), str):\n            used.add(normalize_identifier(data["source_id"]))\n        if isinstance(data.get("sources"), list):\n''',
        1,
    )

    TARGET.write_text(text, encoding="utf-8")
    print("Patched tools/build_registers.py to v0.8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
