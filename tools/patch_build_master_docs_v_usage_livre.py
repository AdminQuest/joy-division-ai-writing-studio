#!/usr/bin/env python3
"""Patch tools/build_master_docs.py to project atoms via usage_livre.

Problem fixed:
- document_maitre generation only used `chapitres` / `chapters`;
- S75 atoms mostly use `usage_livre`, so they appeared in the RAG but not in
  chapter master documents;
- concepts_derives were not counted in recurring concepts.

This patch makes the master documents follow the actual v2 atom schema.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "build_master_docs.py"

OLD_CHAPTER_MATCH = '''def chapter_match(record: Dict[str, Any], chapter_number: int) -> bool:\n    data = record.get("data", {})\n    target = chapter_label(chapter_number)\n    values = as_list(data.get("chapitres")) + as_list(data.get("chapters"))\n    return target in {text(value) for value in values}\n'''

NEW_CHAPTER_MATCH = '''def chapter_match(record: Dict[str, Any], chapter_number: int) -> bool:\n    data = record.get("data", {})\n    target = chapter_label(chapter_number)\n    target_short = f"CH{chapter_number:02d}"\n\n    # The v2 atom schema often uses `usage_livre` rather than `chapitres`\n    # to indicate chapter use. Master docs must therefore project atoms from\n    # all explicit chapter-use fields, not only from legacy chapter fields.\n    values = (\n        as_list(data.get("chapitres"))\n        + as_list(data.get("chapters"))\n        + as_list(data.get("usage_livre"))\n        + as_list(data.get("liens_interchapitres"))\n    )\n\n    normalized = {text(value) for value in values if text(value)}\n    normalized_lower = {value.lower() for value in normalized}\n\n    return (\n        target in normalized\n        or target.lower() in normalized_lower\n        or target_short in normalized\n        or target_short.lower() in normalized_lower\n        or str(chapter_number) in normalized\n    )\n'''

OLD_CONCEPT_VALUES = '''def concept_values(atoms: List[Dict[str, Any]]) -> List[str]:\n    counter: Counter[str] = Counter()\n    for atom in atoms:\n        for concept in as_list(atom.get("data", {}).get("concepts")):\n            item = text(concept)\n            if item:\n                counter[item] += 1\n    return [f"{name} ({count})" for name, count in counter.most_common(MAX_CONCEPTS)]\n'''

NEW_CONCEPT_VALUES = '''def concept_values(atoms: List[Dict[str, Any]]) -> List[str]:\n    counter: Counter[str] = Counter()\n    for atom in atoms:\n        data = atom.get("data", {})\n        values = as_list(data.get("concepts")) + as_list(data.get("concepts_derives"))\n        for concept in values:\n            item = text(concept)\n            if item:\n                counter[item] += 1\n    return [f"{name} ({count})" for name, count in counter.most_common(MAX_CONCEPTS)]\n'''


def main() -> int:
    if not TARGET.exists():
        print(f"File not found: {TARGET}")
        return 1

    content = TARGET.read_text(encoding="utf-8")
    changed = 0

    if OLD_CHAPTER_MATCH in content:
        content = content.replace(OLD_CHAPTER_MATCH, NEW_CHAPTER_MATCH)
        changed += 1
    elif "usage_livre" in content and "target_short" in content:
        print("chapter_match already appears patched.")
    else:
        print("chapter_match block not found; patch not applied.")
        return 2

    if OLD_CONCEPT_VALUES in content:
        content = content.replace(OLD_CONCEPT_VALUES, NEW_CONCEPT_VALUES)
        changed += 1
    elif "concepts_derives" in content:
        print("concept_values already appears patched.")
    else:
        print("concept_values block not found; patch not applied.")
        return 3

    TARGET.write_text(content, encoding="utf-8")
    print(f"Patched build_master_docs.py ({changed} block replacement(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
