#!/usr/bin/env python3
"""
Build chapter master documents and inject per-chapter source notes.

Use this command when source notes exist in chapters/XX/source_notes*.md.
It preserves the rule that chapters/addenda/ is forbidden.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    run([sys.executable, "tools/build_master_docs.py"])
    run([sys.executable, "tools/inject_chapter_source_notes.py"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
