#!/usr/bin/env python3
"""Drift sentinel — fail loudly if generated artifacts are out of sync.

Verifies that the generated artifacts in the working tree (registers/,
exports/generated/, chapters/XX/document_maitre.md, chapters/master_docs.json)
are EXACTLY what a fresh deterministic rebuild (``build_all``) produces from the
current sources. If anything diverges — a generated file edited by hand, or an
atom changed without a rebuild — the sentinel exits non-zero and lists the
offending files, so no stale documentary artifact can pass.

Model (matches the agreed design: build → rebuild → diff):
  1. Snapshot the *current* working-tree generated files (normalized hashes).
  2. Run ``build_all`` (deterministic; overwrites the generated files).
  3. Compare the rebuilt files against the snapshot.
  4. Any substantive difference ⇒ drift ⇒ exit non-zero, files listed.

The timestamp field is normalized out before comparison (see
``buildlib.normalize_generated``): the sentinel flags *substantive* drift only,
never a pure ``generated_at`` change. This keeps it robust across commits and in
CI (Volet D).

Note on side effects: step 2 regenerates the artifacts in place. When the tree is
already in sync (the normal case, e.g. right after ``build_all`` in
``--commit-and-pr``) this is a deterministic no-op and the tree is left untouched.
When drift IS detected, the rebuild leaves the artifacts *corrected* in the
working tree — the intended remedy — so the caller can review and stage them. The
sentinel never touches sources or committed history.

Exit codes:
  0  in sync (no substantive drift)
  1  drift detected (offending files listed on stderr)
  2  the rebuild itself failed
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_all  # noqa: E402
from buildlib import REPO_ROOT, iter_generated_files, normalize_generated  # noqa: E402


def _digest(path: Path) -> str:
    """Normalized content digest: timestamps blanked for text, raw bytes otherwise."""
    data = path.read_bytes()
    try:
        text = normalize_generated(data.decode("utf-8"))
        payload = text.encode("utf-8")
    except UnicodeDecodeError:
        payload = data
    return hashlib.sha256(payload).hexdigest()


def _digests(files) -> dict:
    return {p: _digest(p) for p in files}


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

    # 1. Snapshot the current working-tree generated artifacts.
    before = _digests(iter_generated_files())

    # 2. Deterministic rebuild from the current sources.
    rc = build_all.run(with_source_notes=args.with_source_notes, quiet=True)
    if rc != 0:
        print("SENTINELLE : le rebuild de contrôle (build_all) a échoué.", file=sys.stderr)
        return 2

    # 3. Compare the rebuilt artifacts against the snapshot.
    after = _digests(iter_generated_files())
    all_paths = sorted(set(before) | set(after))
    diffs = [p for p in all_paths if before.get(p) != after.get(p)]

    if diffs:
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

    if not args.quiet:
        print(f"Sentinelle OK : {len(all_paths)} artefact(s) générés en phase.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
