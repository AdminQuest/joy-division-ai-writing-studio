#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "registers" / "references" / "master_references.md"

BLOCKS = [
    "## S35 — Peter Hook, autobiographie / mémoires, migré vers S41",
    "## S37 — Deborah Curtis, témoignage biographique, migré vers S45",
]


def remove_block(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return text
    rest = text[start + len(heading):]
    next_pos = rest.find("\n## S")
    if next_pos == -1:
        end = len(text)
    else:
        end = start + len(heading) + next_pos + 1
    return text[:start].rstrip() + "\n\n" + text[end:].lstrip()

text = PATH.read_text(encoding="utf-8")
new = text
for heading in BLOCKS:
    new = remove_block(new, heading)

if new != text:
    PATH.write_text(new, encoding="utf-8")
    print("removed S35/S37 legacy blocks from master_references.md")
else:
    print("no S35/S37 legacy blocks found in master_references.md")
