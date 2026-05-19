#!/usr/bin/env python3
"""
Patch README workflow rules after removing chapters/addenda/.

This script is idempotent. It keeps README as the normative document:
- chapters/addenda/ is forbidden;
- chapter source notes must live directly in chapters/XX/;
- master docs must be built with source-note injection.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

MARKER = "### 2.2. Injection des notes de chapitre dans les documents maîtres"
BLOCK = """\n### 2.2. Injection des notes de chapitre dans les documents maîtres\n\nLes fichiers `chapters/XX/source_notes*.md` sont lus après la génération des documents maîtres. Ils sont injectés dans une section dédiée des `chapters/XX/document_maitre.md`.\n\nCommande recommandée après `build_registers.py` et `audit_repo.py` :\n\n```bash\npython3 tools/build_master_docs.py\npython3 tools/inject_chapter_source_notes.py\n```\n\nCommande équivalente en un seul appel :\n\n```bash\npython3 tools/build_master_docs_with_notes.py\n```\n\nIl est interdit de recréer `chapters/addenda/`. Toute note transversale doit être dispatchée dans les dossiers `chapters/XX/` concernés.\n"""

OLD_CMD = """python3 tools/build_master_docs.py"""
NEW_CMD = """python3 tools/build_master_docs.py\npython3 tools/inject_chapter_source_notes.py"""


def main() -> int:
    text = README.read_text(encoding="utf-8")

    if MARKER not in text:
        anchor = "---\n\n## 3. Règle impérative pour toute atomisation"
        if anchor not in text:
            raise SystemExit("README anchor not found")
        text = text.replace(anchor, BLOCK + "\n---\n\n## 3. Règle impérative pour toute atomisation", 1)

    # Update the first standalone build_master_docs command in the local mandatory chain if it has not already been expanded.
    if "python3 tools/inject_chapter_source_notes.py" not in text.split("## 12. Publication des exports", 1)[0]:
        text = text.replace(OLD_CMD, NEW_CMD, 1)

    README.write_text(text, encoding="utf-8")
    print("README patched: no chapters/addenda/ workflow and source-note injection documented.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
