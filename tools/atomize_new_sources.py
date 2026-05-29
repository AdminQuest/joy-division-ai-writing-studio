#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Atomisation orchestrator for Registre_sources/

This tool orchestrates the *plumbing* around the atomisation of new PDF sources
dropped in the Google Drive folder ``Registre_sources/``. It does NOT perform the
atomisation itself: atomisation is a cognitive task carried out by a Claude agent
(or a human) following ``prompts/atomisation_workflow.md`` of the private repo.

The tool is deliberately split into four explicit, manually-triggered steps so
that a human stays in the loop at every boundary (validation level 2 = branch + PR):

  1. ``--detect``          List the sources currently waiting to be atomised.
  2. ``--prepare SXX``     Pull main, create the work branch, print the atomisation
                           consigne for the agent. (``--all`` to batch every pending
                           source — used mainly for dry-run robustness checks.)
  3. ``--commit-and-pr SXX`` Run build_registers + audit, commit, push, open a PUBLIC
                           pull request towards main.
  4. ``--finalize SXX``    AFTER the PR is merged: move the source PDF on Google Drive
                           to ``Registre_sources/atomized/{YYYY-MM-DD}-{name}.pdf``.

Design notes
------------
* This PR scope is PUBLIC ONLY. The atomisation passes write public material
  (sources/, registers/, rag/, data/, reports/) in this repo. The private volet
  (chapters/, songs/ of joy-division-studio-private) stays manual for now so that
  no lyrics or private notes can leak into a public PR.
* No external dependency: standard library only. PDF reading is the agent's job.
* The Google Drive path is never hardcoded. It is resolved from (in order):
  --registre-path, $REGISTRE_SOURCES_PATH, config.json, then auto-detection under
  ~/Library/CloudStorage/. When no local mount is available (e.g. a cloud agent),
  the tool prints the Drive operation to perform via the Google Drive MCP instead.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRE_JSON = REPO_ROOT / "data" / "registre.json"
SOURCES_DIR = REPO_ROOT / "sources"
DEFAULT_CONFIG = REPO_ROOT / "tools" / "atomisation" / "config.json"

# A source is "pending" when its registre.json status announces the atomisation
# has yet to start. Matched accent- and case-insensitively.
PENDING_STATUS_MARKER = "atomisation a demarrer"

# Private repo workflow that the agent must follow to atomise.
WORKFLOW_REF = "joy-division-studio-private:prompts/atomisation_workflow.md"


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
class Log:
    """Minimal leveled logger with an explicit dry-run prefix."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run

    def _emit(self, level: str, msg: str) -> None:
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{level:5} | {msg}", flush=True)

    def info(self, msg: str) -> None:
        self._emit("INFO", msg)

    def step(self, msg: str) -> None:
        self._emit("STEP", msg)

    def warn(self, msg: str) -> None:
        self._emit("WARN", msg)

    def error(self, msg: str) -> None:
        self._emit("ERROR", msg)

    def action(self, msg: str) -> None:
        """An action that mutates state (skipped in dry-run)."""
        verb = "WOULD" if self.dry_run else "DO"
        self._emit(verb, msg)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)
    )


def normalize(text: str) -> str:
    return strip_accents(str(text)).lower().strip()


def slugify(text: str) -> str:
    text = strip_accents(str(text)).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")


def load_config(path: Optional[Path]) -> Dict[str, Any]:
    cfg_path = path or DEFAULT_CONFIG
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARN  | could not read config {cfg_path}: {exc}", file=sys.stderr)
    return {}


def load_registre() -> List[Dict[str, Any]]:
    if not REGISTRE_JSON.exists():
        raise FileNotFoundError(f"registre introuvable: {REGISTRE_JSON}")
    return json.loads(REGISTRE_JSON.read_text(encoding="utf-8"))


def source_is_atomized(source_id: str) -> bool:
    """True if at least one atom file already references this source_id in sources/.

    More robust than guessing the sources/<auteur>/ directory name, which is not
    stored in registre.json for every entry.
    """
    needle = f"source_id: {source_id}"
    if not SOURCES_DIR.exists():
        return False
    for md in SOURCES_DIR.rglob("*.md"):
        try:
            if needle in md.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def is_pending(entry: Dict[str, Any]) -> bool:
    status = normalize(entry.get("statut", ""))
    if PENDING_STATUS_MARKER not in status:
        return False
    return not source_is_atomized(entry["id"])


def detect_pending(registre: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [e for e in registre if is_pending(e)]


def find_entry(registre: List[Dict[str, Any]], source_id: str) -> Optional[Dict[str, Any]]:
    for e in registre:
        if e.get("id") == source_id:
            return e
    return None


def branch_name(entry: Dict[str, Any], today: str) -> str:
    sid = entry["id"]
    short = entry.get("source_short_title") or entry.get("titre") or sid
    return f"claude/atomize-{today}-{slugify(sid + '-' + short)}"


# --------------------------------------------------------------------------- #
# Google Drive resolution (filesystem mount OR MCP fallback)
# --------------------------------------------------------------------------- #
def resolve_registre_path(
    args: argparse.Namespace, config: Dict[str, Any], log: Log
) -> Optional[Path]:
    """Resolve the local Registre_sources/ path. Returns None in MCP/cloud mode."""
    # 1. explicit CLI flag
    candidates: List[Optional[str]] = [getattr(args, "registre_path", None)]
    # 2. environment variable
    candidates.append(os.environ.get("REGISTRE_SOURCES_PATH"))
    # 3. config file
    candidates.append(config.get("registre_sources_path"))
    for cand in candidates:
        if cand:
            p = Path(os.path.expanduser(cand))
            if p.exists():
                return p
            log.warn(f"chemin Registre_sources configuré mais introuvable: {p}")
    # 4. auto-detection under ~/Library/CloudStorage (macOS Google Drive Desktop)
    cloud = Path(os.path.expanduser("~/Library/CloudStorage"))
    if cloud.exists():
        for match in cloud.glob("GoogleDrive-*/**/Registre_sources"):
            if match.is_dir():
                log.info(f"Registre_sources auto-détecté: {match}")
                return match
    return None


def find_drive_folder(registre_path: Path, source_id: str) -> Optional[Path]:
    matches = sorted(registre_path.glob(f"{source_id}_*"))
    return matches[0] if matches else None


def find_pdfs(folder: Path) -> List[Path]:
    return sorted(folder.glob("*.pdf"))


# --------------------------------------------------------------------------- #
# Git / PR plumbing
# --------------------------------------------------------------------------- #
def run_cmd(cmd: List[str], log: Log, *, dry: bool, check: bool = True) -> int:
    log.action("$ " + " ".join(cmd))
    if dry:
        return 0
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if check and proc.returncode != 0:
        raise RuntimeError(f"commande échouée ({proc.returncode}): {' '.join(cmd)}")
    return proc.returncode


def git_current_branch() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return out.stdout.strip()


def gh_available() -> bool:
    return shutil.which("gh") is not None


# --------------------------------------------------------------------------- #
# Atomisation consigne (printed for the agent)
# --------------------------------------------------------------------------- #
def print_consigne(
    entry: Dict[str, Any], branch: str, pdf_hint: str, log: Log
) -> None:
    sid = entry["id"]
    label = entry.get("source_label", sid)
    sep = "=" * 78
    print()
    print(sep)
    print(f"  CONSIGNE D'ATOMISATION — {label}")
    print(sep)
    print(
        f"""
Branche de travail : {branch}
PDF source         : {pdf_hint}
Workflow à suivre  : {WORKFLOW_REF}

PÉRIMÈTRE DE CETTE PASSE — PUBLIC UNIQUEMENT
  Écrire seulement dans le repo PUBLIC (joy-division-ai-writing-studio) :
    - sources/<auteur_court>/        (source.md, atomes, citations_exactes.md)
    - registers/                     (atoms, quotes, chronology, concepts,
                                      motifs, myths, references, relations,
                                      people, songs, places, organizations)
    - data/registre.json             (mettre à jour le statut de {sid})
    - rag/context, rag/fragments, exports/generated
    - reports/{sid.lower()}_*_atomization_report.md

  NE PAS écrire dans le repo privé (chapters/, songs/) pendant cette passe :
  le volet privé reste manuel pour éviter toute fuite de paroles/notes en PR
  publique.

SURCHARGES PAR RAPPORT AU WORKFLOW 347 LIGNES
  - Ne PAS committer sur main : rester sur la branche {branch}.
  - Ne PAS faire `git push` vers main. Le commit + push + PR sont gérés
    ensuite par `atomize_new_sources.py --commit-and-pr {sid}`.
  - Jamais de paroles complètes. Pour une chanson : éléments analytiques,
    contextuels, historiographiques et éditoriaux uniquement.

RAPPELS QUALITÉ
  - Atomes v2 sélectifs (nœuds critiques), pas d'atomisation mécanique.
  - Relations stabilisées, concepts à label sémantique stable.
  - Citations courtes, pages PDF + pages livre, guillemets français.

À la fin de la passe d'atomisation, lance :
  python3 tools/atomize_new_sources.py --commit-and-pr {sid}
"""
    )
    print(sep)
    print()


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_detect(registre: List[Dict[str, Any]], log: Log) -> int:
    pending = detect_pending(registre)
    if not pending:
        log.info("Aucune source en attente d'atomisation.")
        return 0
    log.info(f"{len(pending)} source(s) en attente d'atomisation :")
    for e in pending:
        print(f"    - {e['id']:5} {e.get('source_label', '')}")
    return 0


def prepare_one(
    entry: Dict[str, Any],
    registre_path: Optional[Path],
    today: str,
    log: Log,
    dry: bool,
) -> bool:
    sid = entry["id"]
    branch = branch_name(entry, today)
    log.step(f"=== PREPARE {sid} — {entry.get('source_label','')} ===")

    if source_is_atomized(sid):
        log.warn(f"{sid} semble déjà atomisé (source_id présent dans sources/). Skip.")
        return False

    # Locate the PDF (informational; the agent reads it via Drive MCP or local mount)
    if registre_path is not None:
        folder = find_drive_folder(registre_path, sid)
        if folder is None:
            log.warn(f"Aucun dossier {sid}_* dans {registre_path}.")
            pdf_hint = f"(dossier {sid}_* introuvable sous {registre_path})"
        else:
            pdfs = find_pdfs(folder)
            if pdfs:
                pdf_hint = "  ;  ".join(str(p) for p in pdfs)
                log.info(f"PDF localisé : {pdf_hint}")
            else:
                pdf_hint = f"(aucun .pdf dans {folder})"
                log.warn(pdf_hint)
    else:
        pdf_hint = (
            f"Registre_sources/{sid}_*/  (montage local absent — lire via MCP Drive : "
            f"search_files parentId du dossier {sid}_*, puis read_file_content)"
        )
        log.info("Mode MCP/cloud : pas de montage Drive local, lecture PDF via MCP.")

    # Git: refresh main and create the work branch
    run_cmd(["git", "fetch", "origin", "main"], log, dry=dry, check=False)
    run_cmd(["git", "checkout", "main"], log, dry=dry, check=False)
    run_cmd(["git", "pull", "origin", "main"], log, dry=dry, check=False)
    run_cmd(["git", "checkout", "-b", branch], log, dry=dry, check=False)

    print_consigne(entry, branch, pdf_hint, log)
    return True


def cmd_prepare(
    registre: List[Dict[str, Any]],
    source_id: Optional[str],
    do_all: bool,
    registre_path: Optional[Path],
    today: str,
    log: Log,
    dry: bool,
) -> int:
    if do_all:
        targets = detect_pending(registre)
        if not targets:
            log.info("Aucune source en attente — rien à préparer.")
            return 0
        log.info(f"Préparation par lot de {len(targets)} source(s) : "
                 + ", ".join(e["id"] for e in targets))
        ok = True
        for e in targets:
            try:
                prepare_one(e, registre_path, today, log, dry)
            except Exception as exc:  # noqa: BLE001 — isolate per-source failures
                log.error(f"Échec préparation {e['id']}: {exc}")
                ok = False
                continue
        return 0 if ok else 1

    if not source_id:
        log.error("--prepare exige un SXX, ou --all.")
        return 2
    entry = find_entry(registre, source_id)
    if entry is None:
        log.error(f"Source {source_id} absente de data/registre.json.")
        return 2
    try:
        prepare_one(entry, registre_path, today, log, dry)
    except Exception as exc:  # noqa: BLE001
        log.error(f"Échec préparation {source_id}: {exc}")
        return 1
    return 0


def cmd_commit_and_pr(
    registre: List[Dict[str, Any]],
    source_id: str,
    today: str,
    log: Log,
    dry: bool,
) -> int:
    entry = find_entry(registre, source_id)
    if entry is None:
        log.error(f"Source {source_id} absente de data/registre.json.")
        return 2
    short = entry.get("source_short_title", source_id)
    branch = git_current_branch()
    log.step(f"=== COMMIT & PR {source_id} (branche {branch}) ===")

    if branch in ("main", "master"):
        log.error("Refus : on est sur main. Place-toi sur la branche claude/atomize-…")
        return 1
    if not source_is_atomized(source_id) and not dry:
        log.error(
            f"Aucun atome {source_id} détecté dans sources/. "
            "Lance d'abord l'atomisation (voir --prepare). Abandon."
        )
        return 1

    # Validation pipeline
    log.step("Validation : build_registers --strict")
    run_cmd([sys.executable, "tools/build_registers.py", "--strict"], log, dry=dry)
    log.step("Validation : audit_repo --fail-on-error")
    run_cmd([sys.executable, "tools/audit_repo.py", "--fail-on-error"], log, dry=dry)

    # Stage public material only
    log.step("Staging (public uniquement)")
    run_cmd(
        ["git", "add", "data/registre.json", "sources/", "registers/", "rag/",
         "reports/", "apps/"],
        log, dry=dry, check=False,
    )
    run_cmd(["git", "add", "-f", "exports/generated"], log, dry=dry, check=False)

    commit_msg = f"feat({source_id}): atomisation — {short}"
    run_cmd(["git", "commit", "-m", commit_msg], log, dry=dry, check=False)
    run_cmd(["git", "push", "-u", "origin", branch], log, dry=dry, check=False)

    # Pull request
    pr_title = f"feat({source_id}): atomisation — {short}"
    pr_body = (
        f"Atomisation de **{entry.get('source_label', source_id)}** "
        f"(passe PUBLIQUE).\n\n"
        f"- Volet privé (chapters/, songs/) : NON inclus (traité manuellement).\n"
        f"- `build_registers --strict` et `audit_repo --fail-on-error` : OK.\n"
        f"- Après fusion : `python3 tools/atomize_new_sources.py "
        f"--finalize {source_id}` pour archiver le PDF sur Drive.\n"
    )
    if gh_available():
        log.step("Ouverture de la PR via gh")
        run_cmd(
            ["gh", "pr", "create", "--base", "main", "--head", branch,
             "--title", pr_title, "--body", pr_body],
            log, dry=dry, check=False,
        )
    else:
        log.warn("`gh` indisponible : créer la PR manuellement / via MCP GitHub.")
        print()
        print("  PR à créer :")
        print(f"    base   : main")
        print(f"    head   : {branch}")
        print(f"    titre  : {pr_title}")
        print(f"    corps  :\n{pr_body}")
    return 0


def cmd_finalize(
    registre: List[Dict[str, Any]],
    source_id: str,
    registre_path: Optional[Path],
    today: str,
    log: Log,
    dry: bool,
) -> int:
    entry = find_entry(registre, source_id)
    if entry is None:
        log.error(f"Source {source_id} absente de data/registre.json.")
        return 2
    log.step(f"=== FINALIZE {source_id} : archivage du PDF sur Drive ===")

    if registre_path is None:
        log.warn("Montage Drive local absent — opération à réaliser via MCP Drive :")
        print(
            f"""
  Via le MCP Google Drive (mode cloud / agent) :
    1. search_files : parentId du dossier {source_id}_* dans Registre_sources/
    2. pour chaque PDF trouvé :
         - créer (si besoin) le sous-dossier Registre_sources/atomized/
         - copy_file vers atomized/ en renommant : {today}-<nom-original>.pdf
         - supprimer l'original (ou déplacer via update parents)
"""
        )
        return 0

    folder = find_drive_folder(registre_path, source_id)
    if folder is None:
        log.error(f"Dossier {source_id}_* introuvable sous {registre_path}.")
        return 1
    pdfs = find_pdfs(folder)
    if not pdfs:
        log.warn(f"Aucun PDF à archiver dans {folder}.")
        return 0

    atomized_dir = registre_path / "atomized"
    log.action(f"mkdir -p {atomized_dir}")
    if not dry:
        atomized_dir.mkdir(exist_ok=True)

    for pdf in pdfs:
        dest = atomized_dir / f"{today}-{pdf.name}"
        log.action(f"move {pdf}  ->  {dest}")
        if not dry:
            shutil.move(str(pdf), str(dest))
    log.info(f"{len(pdfs)} PDF archivé(s) pour {source_id}.")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="atomize_new_sources.py",
        description="Orchestrateur d'atomisation des PDF de Registre_sources/ "
                    "(public uniquement, validation par PR).",
    )
    actions = p.add_mutually_exclusive_group(required=True)
    actions.add_argument("--detect", action="store_true",
                         help="Liste les sources en attente d'atomisation.")
    actions.add_argument("--prepare", nargs="?", const="", metavar="SXX",
                         help="Crée la branche et affiche la consigne d'atomisation. "
                              "Combiner avec --all pour traiter tout le lot.")
    actions.add_argument("--commit-and-pr", metavar="SXX", dest="commit_and_pr",
                         help="build_registers + audit, commit, push, ouvre la PR.")
    actions.add_argument("--finalize", metavar="SXX",
                         help="Après fusion : déplace le PDF vers atomized/.")

    p.add_argument("--all", action="store_true",
                   help="Avec --prepare : traite toutes les sources en attente.")
    p.add_argument("--dry-run", action="store_true",
                   help="Simule sans rien écrire, déplacer ni pousser.")
    p.add_argument("--registre-path", metavar="PATH",
                   help="Chemin local du dossier Registre_sources/ (sinon "
                        "$REGISTRE_SOURCES_PATH, config.json, ou auto-détection).")
    p.add_argument("--config", metavar="PATH", type=Path,
                   help=f"Fichier de config (défaut: {DEFAULT_CONFIG}).")
    p.add_argument("--date", metavar="YYYY-MM-DD",
                   help="Force la date (utile pour des tests reproductibles).")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    log = Log(dry_run=args.dry_run)
    today = args.date or date.today().isoformat()
    config = load_config(args.config)

    try:
        registre = load_registre()
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        log.error(str(exc))
        return 2

    if args.detect:
        return cmd_detect(registre, log)

    # Drive path is only required for prepare (informational) and finalize.
    registre_path = resolve_registre_path(args, config, log)

    if args.prepare is not None:
        sid = args.prepare or None
        return cmd_prepare(registre, sid, args.all, registre_path, today, log,
                           args.dry_run)
    if args.commit_and_pr:
        return cmd_commit_and_pr(registre, args.commit_and_pr, today, log,
                                 args.dry_run)
    if args.finalize:
        return cmd_finalize(registre, args.finalize, registre_path, today, log,
                            args.dry_run)
    return 2


if __name__ == "__main__":
    sys.exit(main())
