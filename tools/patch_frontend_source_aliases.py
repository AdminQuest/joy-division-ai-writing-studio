#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "apps" / "rag-studio" / "app.js",
    ROOT / "apps" / "rag-studio" / "app_rag2.js",
]

OLD_LINES = [
    "  'S35': 'S41',\n",
    "  'S37': 'S45',\n",
]

for path in FILES:
    text = path.read_text(encoding="utf-8")
    new = text
    for line in OLD_LINES:
        new = new.replace(line, "")
    if new != text:
        path.write_text(new, encoding="utf-8")
        print(f"patched {path}")
    else:
        print(f"no change {path}")
