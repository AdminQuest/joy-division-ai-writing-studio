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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buildlib import (  # noqa: E402
    GENERATED_ALL_PATHSPECS,
    GENERATED_MASTERDOCS_PATHSPECS,
    GENERATED_REGISTERS_PATHSPECS,
    normalize_generated,
    restore_generated,
    snapshot_generated,
)

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


def count_atoms(source_id: str) -> int:
    """Count actual atoms (``id: SXX-Axxx``) authored for this source in sources/.

    This is the real signal that an atomisation pass produced content: a bare
    source.md with ``source_id: SXX`` but no atoms is *partial* and must not be
    committed. Matches lines like ``id: S90-A001`` (with optional indentation).
    """
    pattern = re.compile(rf"^\s*id:\s*{re.escape(source_id)}-A\d+", re.MULTILINE)
    if not SOURCES_DIR.exists():
        return 0
    total = 0
    for md in SOURCES_DIR.rglob("*.md"):
        try:
            total += len(pattern.findall(md.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return total


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


def git_branch_exists(branch: str) -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


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
    reuse_branch: bool = False,
) -> bool:
    sid = entry["id"]
    branch = branch_name(entry, today)
    log.step(f"=== PREPARE {sid} — {entry.get('source_label','')} ===")

    if source_is_atomized(sid):
        log.warn(f"{sid} semble déjà atomisé (source_id présent dans sources/). Skip.")
        return False

    # Idempotence: never silently clobber or strand the user on main. Check the
    # work branch BEFORE any git mutation.
    branch_exists = git_branch_exists(branch)
    if branch_exists and not reuse_branch:
        log.error(
            f"La branche {branch} existe déjà. Échec propre (aucune mutation). "
            f"Reprends le travail dessus avec `git checkout {branch}`, "
            f"relance avec --reuse-branch, ou supprime-la (git branch -D {branch})."
        )
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

    # Git: refresh main and create (or reuse) the work branch
    if branch_exists and reuse_branch:
        log.warn(f"--reuse-branch : reprise sur la branche existante {branch}.")
        run_cmd(["git", "checkout", branch], log, dry=dry, check=False)
    else:
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
    reuse_branch: bool = False,
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
                if not prepare_one(e, registre_path, today, log, dry, reuse_branch):
                    ok = False
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
        ok = prepare_one(entry, registre_path, today, log, dry, reuse_branch)
    except Exception as exc:  # noqa: BLE001
        log.error(f"Échec préparation {source_id}: {exc}")
        return 1
    return 0 if ok else 1


def _git(args: List[str], capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args, cwd=str(REPO_ROOT), capture_output=capture, text=True
    )


def commit_groups(source_id: str, short: str) -> List[Dict[str, Any]]:
    """Logical commit groups for --commit-and-pr, in order.

    Axis = *édité-humain | généré* (NOT drift|feature): with the anti-drift
    sentinel in place, a pass never carries pre-existing drift to resorb, so the
    only meaningful split is hand-authored inputs vs build_all-generated artifacts.
    A group whose diff is empty is skipped (no empty commits).
    """
    sid_lower = source_id.lower()
    return [
        {
            "key": "human",
            "label": "édité-humain (sources, registre, rapport)",
            "message": f"feat({source_id}): atomisation — {short}",
            # rag/ and apps/ are agent/human-authored, not build_all outputs.
            "pathspecs": [
                "data/registre.json",
                "sources",
                "rag",
                "apps",
                f"reports/{sid_lower}_*",
            ],
        },
        {
            "key": "registers",
            "label": "généré : registres + exports",
            "message": f"chore(registers): régénération registres + exports — {source_id}",
            "pathspecs": list(GENERATED_REGISTERS_PATHSPECS),
        },
        {
            "key": "masterdocs",
            "label": "généré : documents maîtres",
            "message": f"rebuild(master-docs): régénération depuis atomes — {source_id}",
            "pathspecs": list(GENERATED_MASTERDOCS_PATHSPECS),
        },
    ]


def _raw_changed_files(pathspecs: List[str]) -> List[str]:
    """Files within pathspecs that differ from HEAD (raw bytes). Uses the index
    as scratch space (stage, read names, reset); it does NOT commit."""
    _git(["reset", "-q"])
    _git(["add", "-f", "--"] + pathspecs)
    out = _git(["diff", "--cached", "--name-only"], capture=True)
    _git(["reset", "-q"])
    return [line for line in out.stdout.splitlines() if line.strip()]


def _is_timestamp_only_change(path: str) -> bool:
    """True if the only difference between HEAD and the worktree for *path* is the
    generated_at timestamp. Reuses buildlib.normalize_generated (single source of
    truth, shared with the sentinel)."""
    head = _git(["show", f"HEAD:{path}"], capture=True)
    if head.returncode != 0:
        return False  # new file → a real change
    work_path = REPO_ROOT / path
    try:
        work = work_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False  # binary / unreadable → never treat as pure-timestamp
    return normalize_generated(head.stdout) == normalize_generated(work)


def group_changed_files(pathspecs: List[str]) -> List[str]:
    """Files within pathspecs whose NORMALIZED diff vs HEAD is non-empty.

    A file where only ``generated_at`` changed is excluded: committing it would be
    pure timestamp churn. This is the automation of the manual revert done on
    PR #20, and it shares its normalization with the drift sentinel."""
    return [f for f in _raw_changed_files(pathspecs) if not _is_timestamp_only_change(f)]


def revert_timestamp_only_churn(log: Log, dry: bool) -> List[str]:
    """Restore (git checkout HEAD) every generated file whose only change is the
    timestamp, so the worktree carries no pure-churn artifact before staging.

    Returns the reverted paths. Substantive changes are left untouched."""
    reverted = [
        f for f in _raw_changed_files(GENERATED_ALL_PATHSPECS)
        if _is_timestamp_only_change(f)
    ]
    if reverted:
        log.action(
            f"git checkout HEAD -- ({len(reverted)} fichier(s) horodatage seul)"
        )
        if not dry:
            _git(["checkout", "HEAD", "--"] + reverted)
    return reverted


def stage_and_commit_group(group: Dict[str, Any], log: Log, dry: bool) -> List[str]:
    """Stage one group and commit iff its normalized diff is non-empty. Returns
    the staged files (timestamp-only churn already excluded)."""
    files = group_changed_files(group["pathspecs"])
    if not files:
        log.info(f"Groupe « {group['label']} » : aucun changement, commit ignoré.")
        return []
    log.action(
        f"git add + commit -m {group['message']!r}  ({len(files)} fichier(s))"
    )
    if not dry:
        # Stage exactly the substantively-changed files (churn already reverted).
        _git(["add", "-f", "--"] + files)
        _git(["commit", "-m", group["message"]])
    return files


def build_pr_body(
    entry: Dict[str, Any], source_id: str, groups: List[Dict[str, Any]]
) -> str:
    """PR body mirroring PR #20: a Commits breakdown + a determinism Garanties block,
    with a LINK to the arbitration report rather than a synthesis of its table."""
    sid_lower = source_id.lower()
    lines = [
        f"Atomisation de **{entry.get('source_label', source_id)}** (passe PUBLIQUE).",
        "",
        "## Commits",
        "",
    ]
    for g in groups:
        if g.get("files"):
            lines.append(
                f"- `{g['message']}` — {len(g['files'])} fichier(s) ({g['label']})"
            )
    lines += [
        "",
        "## Garanties",
        "",
        "- Pipeline canonique `tools/build_all.py` "
        "(`build_registers --strict` → `build_master_docs`).",
        "- Sentinelle anti-drift `tools/check_generated_sync.py` : "
        "rebuild à blanc → **0 divergence** (horodatage gelé via `SOURCE_DATE_EPOCH`).",
        "- `audit_repo --fail-on-error` : OK.",
        "- Volet privé (chapters/songs du repo privé) : NON inclus (traité manuellement).",
        "- Découpage **édité-humain | généré** (pas drift|feature) : "
        "aucune dette de drift à résorber.",
        "",
        f"Détail de l'arbitrage éventuel : voir `reports/{sid_lower}_*.md`.",
        "",
        f"Après fusion : `python3 tools/atomize_new_sources.py --finalize {source_id}` "
        "pour archiver le PDF sur Drive.",
    ]
    return "\n".join(lines)


def cmd_commit_and_pr(
    registre: List[Dict[str, Any]],
    source_id: str,
    today: str,
    log: Log,
    dry: bool,
    single_commit: bool = False,
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

    # Completeness gate: require real atoms (SXX-Axxx), not just a bare source.md.
    # This catches a *partial* pass (source.md present but no atoms written).
    n_atoms = count_atoms(source_id)
    log.info(f"{n_atoms} atome(s) {source_id}-Axxx détecté(s) dans sources/.")
    if n_atoms == 0 and not dry:
        log.error(
            f"Aucun atome {source_id}-Axxx dans sources/ : atomisation absente ou "
            "partielle. Termine la passe (voir --prepare) avant de committer. Abandon."
        )
        return 1

    # --dry-run is READ-ONLY: snapshot the exact PRE-RUN bytes of every generated
    # artifact (committed or not) so we can restore them verbatim after computing the
    # plan. Restoring from this snapshot — not `git checkout HEAD` — preserves any
    # uncommitted generated changes the user already had in their tree.
    pre_run_snapshot = snapshot_generated() if dry else None

    def _restore_if_dry() -> None:
        if dry:
            n = restore_generated(pre_run_snapshot)
            log.info(f"DRY-RUN : arbre restauré à l'état pré-run ({n} fichier(s)).")

    # Canonical build: regenerate registers + exports + master docs deterministically,
    # so no stale document_maitre can drift away from the committed atoms (Volet 1).
    # The build runs for real even in --dry-run (the plan is computed from its output);
    # _restore_if_dry() then puts the tree back exactly as it was before the command.
    try:
        log.step("Build canonique : build_all (build_registers --strict → build_master_docs)")
        run_cmd([sys.executable, "tools/build_all.py"], log, dry=False)
        log.step("Validation : audit_repo --fail-on-error")
        run_cmd([sys.executable, "tools/audit_repo.py", "--fail-on-error"], log, dry=False)
    except RuntimeError as exc:
        log.error(f"Build/validation échoué — rien n'est commité ni poussé : {exc}")
        log.error("Corrige les erreurs signalées ci-dessus, puis relance --commit-and-pr.")
        _restore_if_dry()
        return 1

    # Drift sentinel: a fresh deterministic rebuild must produce ZERO difference.
    # Runs BEFORE any commit — failure means nothing is staged, committed or pushed.
    log.step("Sentinelle anti-drift : check_generated_sync (rebuild à blanc → 0 diff)")
    rc = run_cmd([sys.executable, "tools/check_generated_sync.py"], log, dry=False,
                 check=False)
    if rc != 0:
        log.error(
            "Sentinelle anti-drift : ÉCHEC. Des artefacts générés sont périmés "
            "vis-à-vis des sources. Régénère (`python3 tools/build_all.py`), "
            "ajoute le résultat, puis relance --commit-and-pr. Rien n'est commité."
        )
        _restore_if_dry()
        return 1

    # Build the commit plan (édité-humain | généré), skipping empty groups.
    groups = commit_groups(source_id, short)
    if single_commit:
        merged_pathspecs: List[str] = []
        for g in groups:
            merged_pathspecs.extend(g["pathspecs"])
        groups = [{
            "key": "single",
            "label": "passe complète (commit unique)",
            "message": f"feat({source_id}): atomisation — {short}",
            "pathspecs": merged_pathspecs,
        }]
    for g in groups:
        g["files"] = group_changed_files(g["pathspecs"])
    planned = [g for g in groups if g["files"]]

    if dry:
        # The plan is computed above; restore the pre-run state so the build leaves no
        # trace (committed or uncommitted generated changes are preserved verbatim).
        _restore_if_dry()
        log.step("DRY-RUN : plan de commits (aucun commit, aucun push, arbre restauré)")
        if not planned:
            log.info("Aucun changement à committer.")
        for g in planned:
            print()
            print(f"  • {g['message']}")
            print(f"    groupe : {g['label']}  ({len(g['files'])} fichier(s))")
            for f in g["files"]:
                print(f"        {f}")
        print()
        print("  --- corps de PR qui serait généré ---")
        print(build_pr_body(entry, source_id, planned))
        return 0

    if not planned:
        log.warn("Aucun changement à committer — ni commit ni PR.")
        return 0

    # Revert pure-timestamp churn on generated artifacts so the worktree carries
    # only substantive changes before staging (same normalization as the sentinel).
    reverted = revert_timestamp_only_churn(log, dry=dry)
    if reverted:
        log.info(f"{len(reverted)} artefact(s) à horodatage seul réinitialisé(s).")

    # Commit each non-empty group in order.
    log.step("Commits scindés (édité-humain | généré)")
    for g in planned:
        stage_and_commit_group(g, log, dry=dry)

    run_cmd(["git", "push", "-u", "origin", branch], log, dry=dry, check=False)

    # Pull request
    pr_title = f"feat({source_id}): atomisation — {short}"
    pr_body = build_pr_body(entry, source_id, planned)
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
    p.add_argument("--reuse-branch", action="store_true", dest="reuse_branch",
                   help="Avec --prepare : reprend une branche de travail existante "
                        "au lieu d'échouer (par défaut : échec propre, pas d'écrasement).")
    p.add_argument("--single-commit", action="store_true", dest="single_commit",
                   help="Avec --commit-and-pr : un seul commit au lieu du découpage "
                        "édité-humain | généré (pour les passes triviales).")
    p.add_argument("--dry-run", action="store_true",
                   help="Simule sans rien écrire, déplacer ni pousser (read-only : "
                        "l'arbre est restauré après). Avec --commit-and-pr : imprime "
                        "le plan de commits + le corps de PR sans rien committer.")
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
                           args.dry_run, args.reuse_branch)
    if args.commit_and_pr:
        return cmd_commit_and_pr(registre, args.commit_and_pr, today, log,
                                 args.dry_run, args.single_commit)
    if args.finalize:
        return cmd_finalize(registre, args.finalize, registre_path, today, log,
                            args.dry_run)
    return 2


if __name__ == "__main__":
    sys.exit(main())
