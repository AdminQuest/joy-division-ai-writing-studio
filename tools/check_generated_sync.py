#!/usr/bin/env python3
"""Drift sentinel — fail loudly if generated artifacts are out of sync.

Verifies that the generated artifacts in the working tree (registers/,
exports/generated/, chapters/XX/document_maitre.md, chapters/master_docs.json)
are EXACTLY what a fresh deterministic rebuild (``build_all``) produces from the
current sources. If anything diverges — a generated file edited by hand, or an
atom changed without a rebuild — the sentinel exits non-zero and lists the
offending files, so no stale documentary artifact can pass.

Model (matches the agreed design: build → rebuild → diff):
  1. Snapshot the *current* working-tree generated files (raw bytes + normalized hash).
  2. Run ``build_all`` (deterministic; overwrites the generated files).
  3. Compare the rebuilt files against the snapshot on the NORMALIZED content.
  4. Any substantive difference ⇒ drift ⇒ exit non-zero, files listed.

The timestamp field is normalized out before comparison (see
``buildlib.normalize_generated``): the sentinel flags *substantive* drift only,
never a pure ``generated_at`` change. This keeps it robust across commits and in
CI (Volet D).

Cleanliness contract (two distinct paths — do not confuse them):
* ON SUCCESS (no substantive drift): the only thing the control rebuild can have
  changed is the ``generated_at`` timestamp. Those timestamp-only changes are
  restored from the pre-rebuild snapshot before returning 0, so the sentinel is a
  TRUE no-op by restoration (not by luck): ``git status`` is exactly what it was
  before the run.
* ON FAILURE (real drift): the rebuilt — i.e. corrected — artifacts are left in
  the working tree on purpose, as the remedy; the caller reviews and stages them.

The sentinel never touches sources or committed history.

Exit codes:
  0  in sync (no substantive drift); working tree left untouched
  1  drift detected (offending files listed on stderr; corrected artifacts left in tree)
  2  the rebuild itself failed
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_all  # noqa: E402
from buildlib import (  # noqa: E402
    REPO_ROOT,
    iter_generated_files,
    normalize_generated,
    restore_generated,
    snapshot_generated,
)


def _normalized_hash(data: bytes) -> str:
    """Hash of the normalized content (timestamps blanked for text; raw otherwise)."""
    try:
        payload = normalize_generated(data.decode("utf-8")).encode("utf-8")
    except UnicodeDecodeError:
        payload = data
    return hashlib.sha256(payload).hexdigest()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_generated_sync.py",
        description="Sentinelle anti-drift : échoue si les artefacts générés ne "
        "correspondent pas à un rebuild déterministe.",
    )
    parser.add_argument(
        "--with-source-notes",
        action="store_true",
        help="Rejoue inject_chapter_source_notes.py dans le rebuild de contrôle.",
    )
    parser.add_argument("--quiet", action="store_true", help="Sortie minimale.")
    args = parser.parse_args(argv)

    # 1. Snapshot the current working-tree generated artifacts (raw bytes).
    before = snapshot_generated()

    # 2. Deterministic rebuild from the current sources.
    rc = build_all.run(with_source_notes=args.with_source_notes, quiet=True)
    if rc != 0:
        print("SENTINELLE : le rebuild de contrôle (build_all) a échoué.", file=sys.stderr)
        return 2

    # 3. Compare the rebuilt artifacts against the snapshot on NORMALIZED content.
    after = {p: p.read_bytes() for p in iter_generated_files()}
    all_paths = sorted(set(before) | set(after))
    diffs = [
        p for p in all_paths
        if _normalized_hash(before.get(p, b"")) != _normalized_hash(after.get(p, b""))
    ]

    if diffs:
        # FAILURE: leave the rebuilt (corrected) artifacts in place as the remedy.
        print(
            "\n"
            "================================================================\n"
            "  SENTINELLE ANTI-DRIFT : ÉCHEC — artefacts générés périmés\n"
            "================================================================\n"
            "Un rebuild déterministe (build_all) produit un résultat différent\n"
            "de l'arbre de travail. Cause probable : un fichier généré a été\n"
            "édité à la main, ou un atome a changé sans régénération.\n"
            f"\n{len(diffs)} fichier(s) divergent(s) :",
            file=sys.stderr,
        )
        for p in diffs:
            try:
                rel = p.relative_to(REPO_ROOT)
            except ValueError:
                rel = p
            print(f"  - {rel}", file=sys.stderr)
        print(
            "\nLes artefacts ont été régénérés (corrigés) dans l'arbre de travail.\n"
            "Vérifie et ajoute le résultat, puis recommence.\n",
            file=sys.stderr,
        )
        return 1

    # SUCCESS: the only changes the control rebuild can have made are timestamp-only.
    # Restore the exact pre-run state from the snapshot so the run is a true no-op.
    restored = restore_generated(before)

    if not args.quiet:
        suffix = f" (arbre restauré : {restored} fichier(s) horodatage seul)" if restored else ""
        print(f"Sentinelle OK : {len(all_paths)} artefact(s) générés en phase{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
