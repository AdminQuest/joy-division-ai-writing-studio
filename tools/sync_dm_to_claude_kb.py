#!/usr/bin/env python3
"""Sync private-repo Document Maîtres → consolidated KB file.

Detects which DMs changed since the last sync, generates a single
consolidated Markdown file ready for upload to the Claude project
knowledge base, and records sync state.

Usage:
    python tools/sync_dm_to_claude_kb.py [--force] [--private-repo PATH]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PUBLIC_REPO = SCRIPT_DIR.parent
DEFAULT_PRIVATE_REPO = PUBLIC_REPO.parent / "joy-division-studio-private"
STATE_FILE = SCRIPT_DIR / ".kb_sync_state.json"
OUTPUT_FILE = PUBLIC_REPO / "exports" / "generated" / "DM_consolidated_for_kb.md"
MASTER_DOCS_JSON = "chapters/master_docs.json"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def git_head_sha(repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=repo, check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"last_sync": None, "files": {}}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_master_docs(private_repo: Path) -> list[dict]:
    md_path = private_repo / MASTER_DOCS_JSON
    if not md_path.exists():
        public_md = PUBLIC_REPO / MASTER_DOCS_JSON
        if public_md.exists():
            md_path = public_md
        else:
            sys.exit(f"ERROR: master_docs.json not found in {private_repo} or {PUBLIC_REPO}")
    data = json.loads(md_path.read_text(encoding="utf-8"))
    return data.get("documents", data if isinstance(data, list) else [])


def build_consolidated(private_repo: Path, docs: list[dict], force: bool) -> dict:
    state = load_state()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    commit_sha = git_head_sha(private_repo)

    changed = []
    all_contents = []

    for doc in sorted(docs, key=lambda d: d.get("chapter", 0)):
        rel_path = doc["path"]
        dm_path = private_repo / rel_path
        if not dm_path.exists():
            print(f"  SKIP {rel_path} (file not found)")
            continue

        current_hash = sha256_of_file(dm_path)
        prev = state["files"].get(rel_path, {})
        prev_hash = prev.get("content_sha256", "")

        is_changed = force or (current_hash != prev_hash)

        content = dm_path.read_text(encoding="utf-8")
        chapter_num = doc.get("chapter", "?")
        title = doc.get("title", rel_path)
        all_contents.append(
            f"# Chapitre {chapter_num} — {title}\n\n"
            f"<!-- source: {rel_path} | sha256: {current_hash[:12]} -->\n\n"
            f"{content}\n\n---\n"
        )

        state["files"][rel_path] = {
            "last_synced_commit": commit_sha,
            "last_synced_at": now,
            "content_sha256": current_hash,
            "status": "success",
        }

        if is_changed:
            changed.append(rel_path)
            print(f"  CHANGED {rel_path}")
        else:
            print(f"  OK      {rel_path} (unchanged)")

    header = (
        f"# Documents Maîtres — Joy Division Manuscript\n\n"
        f"Generated: {now}  \n"
        f"Private repo commit: `{commit_sha[:10]}`  \n"
        f"Chapters: {len(all_contents)}  \n"
        f"Changed this run: {len(changed)}\n\n---\n\n"
    )

    consolidated = header + "\n".join(all_contents)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(consolidated, encoding="utf-8")

    state["last_sync"] = now
    save_state(state)

    return {
        "total": len(all_contents),
        "changed": len(changed),
        "changed_files": changed,
        "output": str(OUTPUT_FILE),
        "output_size_kb": round(OUTPUT_FILE.stat().st_size / 1024, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Sync DMs to consolidated KB file")
    parser.add_argument("--force", action="store_true", help="Regenerate even if unchanged")
    parser.add_argument("--private-repo", type=Path, default=None,
                        help=f"Path to private repo (default: {DEFAULT_PRIVATE_REPO})")
    args = parser.parse_args()

    private_repo = args.private_repo or DEFAULT_PRIVATE_REPO
    if not private_repo.exists():
        sys.exit(f"ERROR: Private repo not found at {private_repo}")

    print(f"Private repo: {private_repo}")
    print(f"Output:       {OUTPUT_FILE}")
    print()

    docs = load_master_docs(private_repo)
    result = build_consolidated(private_repo, docs, args.force)

    print()
    print(f"Done. {result['total']} chapters, {result['changed']} changed.")
    print(f"Output: {result['output']} ({result['output_size_kb']} KB)")

    if result["changed"] > 0:
        print("\nUpload DM_consolidated_for_kb.md to the Claude project KB via Console.")
    else:
        print("\nNo changes detected — KB is up to date.")


if __name__ == "__main__":
    main()
