#!/usr/bin/env python3
"""Shared helpers for the documentary build pipeline.

This module is the single source of truth for two things that several tools must
agree on:

1. A *deterministic* build timestamp (:func:`resolved_generated_at`), so that two
   consecutive builds from the same committed inputs produce identical
   ``generated_at`` fields. This is a precondition for the drift sentinel
   (``tools/check_generated_sync.py``) and for the determinism guarantee of
   ``tools/build_all.py``.

2. The canonical list of *generated* artifacts (:func:`iter_generated_files`,
   :data:`GENERATED_*` pathspecs), so the orchestrator, the sentinel and (later)
   CI all stage / compare exactly the same files.

Timestamp resolution order (see :func:`resolved_generated_at`):
  1. ``$SOURCE_DATE_EPOCH`` — set once per run by ``build_all`` and shared across
     passes, guaranteeing byte-identical output within a run.
  2. The HEAD commit date — a deterministic anchor for a given checkout; rebuilding
     the same HEAD yields the same value (no churn between unrelated rebuilds).
  3. Wall-clock ``now()`` — last resort outside a git repository.

Compromise (documented): anchoring on the HEAD commit date means ``generated_at``
tracks the commit graph rather than wall-clock time. Across *different* commits the
value legitimately moves. The drift sentinel therefore compares with the timestamp
field NORMALIZED (:func:`normalize_generated`), so it never raises a false drift on
a pure timestamp change — it only flags substantive divergence. Within a single run
the shared ``SOURCE_DATE_EPOCH`` keeps every pass byte-identical.
"""

from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------- #
# Deterministic build timestamp
# --------------------------------------------------------------------------- #
def head_commit_epoch() -> Optional[int]:
    """Return the HEAD commit's Unix timestamp, or None outside a git repo."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if out.returncode != 0:
        return None
    value = out.stdout.strip()
    return int(value) if value.isdigit() else None


def resolve_source_date_epoch() -> int:
    """Resolve the epoch to freeze for a build run (see module docstring).

    Order: $SOURCE_DATE_EPOCH, then HEAD commit date, then wall-clock now().
    """
    env = os.environ.get("SOURCE_DATE_EPOCH")
    if env and env.strip().isdigit():
        return int(env.strip())
    head = head_commit_epoch()
    if head is not None:
        return head
    return int(datetime.now(tz=timezone.utc).timestamp())


def resolved_generated_at(timespec: str = "seconds") -> str:
    """Return the deterministic ISO-8601 ``generated_at`` value for this build.

    Rendered as naive UTC (no offset suffix) to preserve the historical field
    shape ``YYYY-MM-DDThh:mm:ss`` while remaining fully deterministic.
    """
    epoch = resolve_source_date_epoch()
    return (
        datetime.fromtimestamp(epoch, tz=timezone.utc)
        .replace(tzinfo=None)
        .isoformat(timespec=timespec)
    )


# --------------------------------------------------------------------------- #
# Canonical set of generated artifacts
# --------------------------------------------------------------------------- #
# git pathspecs, grouped for surgical staging in --commit-and-pr (Volet 2).
# NOTE: exports/ is gitignored but its generated files are tracked, so callers
# must use ``git add -f`` for these pathspecs.
GENERATED_REGISTERS_PATHSPECS: List[str] = [
    "registers",
    "exports/generated",
    # master_docs_index.json belongs to the master-docs group, not here. Use the
    # short ":!" exclude form (the long ":(exclude)" form is not honoured by
    # `git add -f` in this environment).
    ":!exports/generated/master_docs_index.json",
]
GENERATED_MASTERDOCS_PATHSPECS: List[str] = [
    "chapters/*/document_maitre.md",
    "chapters/master_docs.json",
    "exports/generated/master_docs_index.json",
]
GENERATED_ALL_PATHSPECS: List[str] = [
    "registers",
    "exports/generated",
    "chapters/*/document_maitre.md",
    "chapters/master_docs.json",
]


def iter_generated_files() -> List[Path]:
    """Return the concrete, existing generated files (for snapshot / compare).

    This is the materialised counterpart of the pathspecs above: every file the
    canonical build produces under registers/, exports/generated/, the chapter
    document_maitre.md files and chapters/master_docs.json.
    """
    files: List[Path] = []

    def _rel(p: Path) -> str:
        # POSIX-relative path: locale-independent, platform-independent sort key.
        return p.relative_to(REPO_ROOT).as_posix()

    for sub in ("registers", "exports/generated"):
        root = REPO_ROOT / sub
        if root.exists():
            files.extend(sorted((p for p in root.rglob("*") if p.is_file()), key=_rel))
    files.extend(sorted((REPO_ROOT / "chapters").glob("*/document_maitre.md"), key=_rel))
    manifest = REPO_ROOT / "chapters" / "master_docs.json"
    if manifest.exists():
        files.append(manifest)
    # De-duplicate while keeping deterministic order.
    seen = set()
    unique: List[Path] = []
    for p in sorted(files):
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def snapshot_generated() -> Dict[Path, bytes]:
    """Capture the raw bytes of every existing generated file (pre-run state).

    Shared by the drift sentinel and the orchestrator's --dry-run path so both
    restore the *exact* pre-run working tree — committed or not — bit for bit.
    """
    return {p: p.read_bytes() for p in iter_generated_files()}


def restore_generated(snapshot: Dict[Path, bytes]) -> int:
    """Restore the working tree to a snapshot taken by :func:`snapshot_generated`.

    Handles the full pre-run state, not just modified content:
      * files in the snapshot are rewritten with their captured bytes;
      * generated files that did NOT exist pre-run (created by an intervening
        build) are removed.
    Returns the number of files touched (rewritten or deleted).
    """
    touched = 0
    for path, data in snapshot.items():
        if not path.exists() or path.read_bytes() != data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            touched += 1
    for path in iter_generated_files():
        if path not in snapshot:  # created after the snapshot ⇒ did not exist pre-run
            try:
                path.unlink()
                touched += 1
            except OSError:
                pass
    return touched


# --------------------------------------------------------------------------- #
# Timestamp normalization (for the drift sentinel)
# --------------------------------------------------------------------------- #
_TS_PATTERNS = [
    # JSON ("generated_at": "...") and YAML (generated_at: "...") forms.
    re.compile(r'(generated_at["\s:=]*")[^"\n]*(")'),
    # diagnostics.md human line: Généré le : `...`
    re.compile(r"(Généré le\s*:\s*`)[^`\n]*(`)"),
]


def normalize_generated(text: str) -> str:
    """Blank out volatile ``generated_at`` timestamps so the sentinel compares
    substantive content only (see module docstring, "Compromise")."""
    for pattern in _TS_PATTERNS:
        text = pattern.sub(r"\1<NORMALIZED>\2", text)
    return text
