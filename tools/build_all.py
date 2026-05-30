#!/usr/bin/env python3
"""Canonical documentary build pipeline — the single source of truth.

Runs, in order:

  1. ``build_registers.py --strict``   atoms/quotes/... -> registers/ + exports/generated/
  2. ``build_master_docs.py``          exports -> chapters/XX/document_maitre.md,
                                        chapters/master_docs.json,
                                        exports/generated/master_docs_index.json
  3. ``audit_repo.py``                 exports -> exports/generated/audit_repo.{json,md,csv}
  4. ``inject_chapter_source_notes.py``  ONLY with --with-source-notes (OFF by
                                        default, to reproduce the committed legacy
                                        layout: the injected section is out of scope
                                        for the public atomisation pass).

All passes share a single deterministic ``SOURCE_DATE_EPOCH`` (resolved once, from
$SOURCE_DATE_EPOCH or the HEAD commit date), so two consecutive runs from identical
committed inputs are byte-identical — the precondition for the drift sentinel
(``tools/check_generated_sync.py``).

Used by ``tools/atomize_new_sources.py --commit-and-pr`` and by the sentinel; can
also be run standalone.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buildlib import resolve_source_date_epoch  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def run(
    *,
    strict: bool = True,
    with_source_notes: bool = False,
    quiet: bool = False,
) -> int:
    """Run the canonical pipeline. Returns 0 on success, non-zero on first failure.

    Freezes SOURCE_DATE_EPOCH once and shares it across all child passes.
    """
    env = dict(os.environ)
    env.setdefault("SOURCE_DATE_EPOCH", str(resolve_source_date_epoch()))

    steps = [
        [sys.executable, "tools/build_registers.py"] + (["--strict"] if strict else []),
        [sys.executable, "tools/build_master_docs.py"],
        # Regenerate the audit artifacts too, so audit_repo.{json,md,csv} can never
        # drift from the committed atoms (no --fail-on-error: build_all *produces*
        # artifacts; the orchestrator validates separately with --fail-on-error).
        [sys.executable, "tools/audit_repo.py"],
    ]
    if with_source_notes:
        steps.append([sys.executable, "tools/inject_chapter_source_notes.py"])

    for cmd in steps:
        if not quiet:
            print(
                f"build_all $ {' '.join(cmd)}  "
                f"(SOURCE_DATE_EPOCH={env['SOURCE_DATE_EPOCH']})",
                flush=True,
            )
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), env=env)
        if proc.returncode != 0:
            print(
                f"build_all: échec de `{' '.join(cmd)}` (rc={proc.returncode})",
                file=sys.stderr,
            )
            return proc.returncode
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_all.py",
        description="Pipeline canonique : build_registers --strict -> build_master_docs "
        "[-> inject_chapter_source_notes].",
    )
    parser.add_argument(
        "--with-source-notes",
        action="store_true",
        help="Lance aussi inject_chapter_source_notes.py (OFF par défaut).",
    )
    parser.add_argument(
        "--no-strict",
        action="store_true",
        help="N'utilise pas --strict pour build_registers (déconseillé).",
    )
    parser.add_argument("--quiet", action="store_true", help="Sortie minimale.")
    args = parser.parse_args(argv)
    return run(
        strict=not args.no_strict,
        with_source_notes=args.with_source_notes,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    raise SystemExit(main())
