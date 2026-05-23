#!/usr/bin/env python3
"""
One-command Songbook sync workflow.

This script automates the routine that was previously done by hand:
- optionally initialise the private/synced lyrics workspace;
- extract editorial lyrics notes into the repo;
- rebuild registers, audit, master docs;
- show git status.

It does not commit or push. It prepares the files and tells you what changed.

Private lyrics workspace:
- default: local_data/songbook_lyrics/
- recommended multi-device setup: set SONGBOOK_LYRICS_ROOT to a Google Drive / iCloud / Synology synced folder.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, check: bool = True) -> int:
    print("\n$ " + " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    if check and proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc.returncode


def current_private_root() -> Path:
    return Path(os.environ.get("SONGBOOK_LYRICS_ROOT", ROOT / "local_data" / "songbook_lyrics")).expanduser()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Joy Division Songbook sync workflow.")
    parser.add_argument("--init-private", action="store_true", help="Initialise the private lyrics workspace before extraction.")
    parser.add_argument("--skip-pull", action="store_true", help="Do not run git pull.")
    parser.add_argument("--skip-build", action="store_true", help="Only extract lyrics editorial notes and show git status.")
    parser.add_argument("--diagnostics", action="store_true", help="Run additional diagnostics.")
    args = parser.parse_args()

    print("Songbook sync")
    print(f"Repo: {ROOT}")
    print(f"Private lyrics root: {current_private_root()}")

    if not args.skip_pull:
        run(["git", "pull"])

    if args.init_private:
        run([sys.executable, "tools/init_local_lyrics_workspace.py"])

    run([sys.executable, "tools/extract_local_lyrics_editorial.py"])

    if not args.skip_build:
        run([sys.executable, "tools/build_registers.py", "--strict"])
        run([sys.executable, "tools/audit_song_canon.py"])
        run([sys.executable, "tools/audit_repo.py"])
        run([sys.executable, "tools/build_master_docs.py"])

    if args.diagnostics:
        run(["grep", "-R", "song_lyrics_editorial", "-n", "songs", "data", "rag", "exports"], check=False)
        run(["grep", "-R", "S79", "-n", "sources", "songs", "data", "rag", "exports"], check=False)
        run(["git", "check-ignore", "-v", "local_data/songbook_lyrics/warsaw/full_lyrics.txt"], check=False)

    run(["git", "status"], check=False)


if __name__ == "__main__":
    main()
