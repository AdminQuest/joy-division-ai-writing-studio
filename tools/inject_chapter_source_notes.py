#!/usr/bin/env python3
"""
Inject per-chapter source notes into generated chapter master documents.

This script intentionally reads ONLY files located directly in chapters/XX/.
It never reads chapters/addenda/, which is a deprecated and forbidden path.

Run after tools/build_master_docs.py.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = REPO_ROOT / "chapters"
START = "## 15. Notes de sources réinjectées"
END = "## 16. Lacunes et prochaines vérifications"
LEGACY_LACUNES = "## 15. Lacunes et prochaines vérifications"
FORBIDDEN_ADDENDA = CHAPTERS_DIR / "addenda"


def chapter_sort_key(path: Path) -> tuple[str, str]:
    return (path.parent.name, path.name)


def read_notes(chapter_dir: Path) -> str:
    note_files = sorted(chapter_dir.glob("source_notes*.md"), key=chapter_sort_key)
    if not note_files:
        return ""

    chunks: list[str] = []
    for path in note_files:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        chunks.append(f"### {path.name}\n\n{text}")
    return "\n\n".join(chunks).strip()


def strip_existing_notes(content: str) -> str:
    if START in content and END in content:
        before, rest = content.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + END + after
    return content


def inject_notes(path: Path, notes: str) -> bool:
    content = path.read_text(encoding="utf-8")
    content = strip_existing_notes(content)

    if LEGACY_LACUNES not in content and END not in content:
        return False

    if END not in content:
        content = content.replace(LEGACY_LACUNES, END, 1)

    if not notes:
        path.write_text(content, encoding="utf-8")
        return False

    block = (
        f"{START}\n\n"
        "Ces notes proviennent de fichiers `source_notes*.md` placés directement dans le dossier du chapitre. "
        "Elles remplacent l’ancien mécanisme interdit `chapters/addenda/`.\n\n"
        f"{notes}\n\n"
    )
    content = content.replace(END, block + END, 1)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if FORBIDDEN_ADDENDA.exists():
        files = [p for p in FORBIDDEN_ADDENDA.rglob("*") if p.is_file()]
        if files:
            raise SystemExit(
                "Forbidden chapters/addenda/ files found. Move their content into chapters/XX/source_notes*.md, "
                "then delete them before injecting source notes."
            )

    changed = 0
    for chapter_dir in sorted(CHAPTERS_DIR.glob("[0-9][0-9]")):
        doc = chapter_dir / "document_maitre.md"
        if not doc.exists():
            continue
        if inject_notes(doc, read_notes(chapter_dir)):
            changed += 1

    print(f"Injected chapter source notes into {changed} document_maitre.md file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
