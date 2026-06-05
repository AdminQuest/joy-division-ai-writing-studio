#!/usr/bin/env python3
"""M1 P0 control: document master -> atoms traceability.

This control is intentionally read-only for the documentary corpus. It reads the
master-doc manifest, generated exports, and master documents, then writes a
regenerable report under reports/m1/. It does not rebuild, fix, or mutate any
documentary source, register, export, manifest, or master document.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports" / "m1"
DEFAULT_REPORT = REPORT_DIR / "dm_atoms_traceability.md"
MANIFEST_PATH = REPO_ROOT / "chapters" / "master_docs.json"
ATOMS_EXPORT = REPO_ROOT / "exports" / "generated" / "atoms.json"
MASTER_DOCS_INDEX = REPO_ROOT / "exports" / "generated" / "master_docs_index.json"

# Atom ids in the corpus currently use both S35-A086 and legacy S45-001 forms.
ATOM_ID_RE = re.compile(r"(?<!-)\bS\d{2,3}-(?:A)?\d{3}\b")
DASHBOARD_ATOMS_RE = re.compile(r"^\|\s*Atomes\s*\|\s*(\d+)\s*\|", re.MULTILINE)


@dataclass
class Issue:
    kind: str
    dm: str
    detail: str


@dataclass
class DmAudit:
    path: str
    title: str = ""
    status: str = "non traçable"
    visible_atoms: int = 0
    found_atoms: int = 0
    alias_resolved_atoms: int = 0
    expected_atoms: int | None = None
    dashboard_atoms: int | None = None
    missing_atom_ids: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_output_path(raw_output: str) -> Path:
    output = Path(raw_output)
    if not output.is_absolute():
        output = REPO_ROOT / output

    resolved_output = output.resolve()
    resolved_report_dir = REPORT_DIR.resolve()
    try:
        resolved_output.relative_to(resolved_report_dir)
    except ValueError as exc:
        raise ValueError(
            "--output doit pointer sous reports/m1/. "
            "Le controle refuse d'ecrire dans le corpus, les exports, les registres, "
            "les sources, la documentation ou les outils."
        ) from exc

    return resolved_output


def validate_master_doc_path(raw_path: object) -> tuple[str | None, Issue | None]:
    raw_display = str(raw_path)
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None, Issue("manifeste incohérent", raw_display, "Chemin de document maitre absent ou non textuel.")

    candidate = Path(raw_path)
    if candidate.is_absolute():
        return None, Issue("manifeste incohérent", raw_path, "Chemin de document maitre absolu refuse.")
    if any(part == ".." for part in candidate.parts):
        return None, Issue("manifeste incohérent", raw_path, "Chemin de document maitre contenant '..' refuse.")

    parts = candidate.parts
    if len(parts) != 3 or parts[0] != "chapters" or parts[2] != "document_maitre.md" or parts[1] in {"", ".", ".."}:
        return None, Issue(
            "manifeste incohérent",
            raw_path,
            "Chemin de document maitre invalide: attendu chapters/*/document_maitre.md.",
        )

    resolved = (REPO_ROOT / candidate).resolve()
    chapters_root = (REPO_ROOT / "chapters").resolve()
    try:
        resolved.relative_to(chapters_root)
    except ValueError:
        return None, Issue("manifeste incohérent", raw_path, "Chemin de document maitre resolu hors chapters/ refuse.")

    return candidate.as_posix(), None


def validate_master_doc_filesystem_path(doc_path: str) -> Issue | None:
    candidate = Path(doc_path)
    chapter = candidate.parts[1]
    chapter_dir = REPO_ROOT / "chapters" / chapter
    full_path = chapter_dir / "document_maitre.md"
    expected_resolved = REPO_ROOT / "chapters" / chapter / "document_maitre.md"

    if chapter_dir.is_symlink() or full_path.is_symlink():
        return Issue(
            "document maître invalide",
            doc_path,
            "Chemin de document maître refusé : composant symlinké ou cible résolue non conforme.",
        )

    if full_path.resolve(strict=False) != expected_resolved:
        return Issue(
            "document maître invalide",
            doc_path,
            "Chemin de document maître refusé : composant symlinké ou cible résolue non conforme.",
        )

    return None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def escape_md(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", r"\|").replace("\n", " ")


def load_manifest(path: Path) -> tuple[list[dict[str, Any]], list[Issue]]:
    payload = load_json(path)
    documents = payload.get("documents") if isinstance(payload, dict) else None
    issues: list[Issue] = []
    if not isinstance(documents, list):
        issues.append(Issue("manifeste incohérent", rel(path), "Champ documents absent ou invalide."))
        return [], issues

    seen_paths: set[str] = set()
    seen_chapters: set[int] = set()
    for doc in documents:
        doc_path = str(doc.get("path", "<chemin absent>"))
        chapter = doc.get("chapter")
        if doc_path in seen_paths:
            issues.append(Issue("manifeste incohérent", doc_path, "Chemin duplique dans le manifeste."))
        seen_paths.add(doc_path)
        if isinstance(chapter, int):
            if chapter in seen_chapters:
                issues.append(Issue("manifeste incohérent", doc_path, f"Chapitre duplique dans le manifeste: {chapter}."))
            seen_chapters.add(chapter)
        else:
            issues.append(Issue("manifeste incohérent", doc_path, "Chapitre absent ou non numerique."))
    return documents, issues


def load_atom_ids(path: Path) -> set[str]:
    payload = load_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"{rel(path)} doit contenir une liste JSON.")
    atom_ids: set[str] = set()
    for item in payload:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        data_id = item.get("data", {}).get("id") if isinstance(item.get("data"), dict) else None
        for raw_id in (item_id, data_id):
            if isinstance(raw_id, str) and ATOM_ID_RE.fullmatch(raw_id):
                atom_ids.add(raw_id)
    return atom_ids


def atom_aliases(atom_id: str) -> set[str]:
    match = re.fullmatch(r"(S\d{2,3})-A(\d{3})", atom_id)
    if match:
        return {f"{match.group(1)}-{match.group(2)}"}
    match = re.fullmatch(r"(S\d{2,3})-(\d{3})", atom_id)
    if match:
        return {f"{match.group(1)}-A{match.group(2)}"}
    return set()


def build_alias_lookup(atom_ids: set[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for atom_id in atom_ids:
        for alias in atom_aliases(atom_id):
            aliases.setdefault(alias, atom_id)
    return aliases


def load_master_index(path: Path) -> tuple[dict[str, dict[str, Any]], list[Issue]]:
    payload = load_json(path)
    chapters = payload.get("chapters") if isinstance(payload, dict) else None
    issues: list[Issue] = []
    if not isinstance(chapters, list):
        issues.append(Issue("manifeste incohérent", rel(path), "Champ chapters absent ou invalide."))
        return {}, issues

    index: dict[str, dict[str, Any]] = {}
    for chapter in chapters:
        if not isinstance(chapter, dict):
            continue
        path_value = chapter.get("path")
        if not isinstance(path_value, str):
            issues.append(Issue("manifeste incohérent", rel(path), "Entree d'index sans chemin."))
            continue
        valid_path, path_issue = validate_master_doc_path(path_value)
        if path_issue is not None:
            issues.append(path_issue)
            continue
        assert valid_path is not None
        if valid_path in index:
            issues.append(Issue("manifeste incohérent", path_value, "Chemin duplique dans master_docs_index."))
        index[valid_path] = chapter
    return index, issues


def scan_disk_master_docs() -> set[str]:
    return {
        rel(path)
        for path in sorted((REPO_ROOT / "chapters").glob("*/document_maitre.md"))
        if path.is_file()
    }


def extract_visible_atom_ids(markdown: str) -> set[str]:
    return set(ATOM_ID_RE.findall(markdown))


def extract_dashboard_atoms(markdown: str) -> int | None:
    match = DASHBOARD_ATOMS_RE.search(markdown)
    if not match:
        return None
    return int(match.group(1))


def audit_document(
    doc: dict[str, Any],
    atom_ids: set[str],
    alias_lookup: dict[str, str],
    master_index: dict[str, dict[str, Any]],
) -> DmAudit:
    raw_doc_path = doc.get("path", "")
    doc_path = str(raw_doc_path)
    title = str(doc.get("title", ""))
    audit = DmAudit(path=doc_path, title=title)

    valid_path, path_issue = validate_master_doc_path(raw_doc_path)
    if path_issue is not None:
        audit.issues.append(path_issue)
        return audit
    assert valid_path is not None
    doc_path = valid_path
    audit.path = doc_path

    full_path = REPO_ROOT / doc_path
    filesystem_issue = validate_master_doc_filesystem_path(doc_path)
    if filesystem_issue is not None:
        audit.issues.append(filesystem_issue)
        return audit

    index_entry = master_index.get(doc_path)
    if index_entry is None:
        audit.issues.append(Issue("document maître absent de l'index", doc_path, "Document present dans le manifeste mais absent de exports/generated/master_docs_index.json."))
    else:
        expected = index_entry.get("atoms")
        if isinstance(expected, int):
            audit.expected_atoms = expected
        else:
            audit.issues.append(Issue("incohérence de volumétrie", doc_path, "Volumetrie atoms absente ou invalide dans master_docs_index."))

    if not full_path.exists():
        audit.issues.append(Issue("document maître absent sur disque", doc_path, "Fichier declare dans le manifeste mais absent du depot."))
        return audit

    markdown = full_path.read_text(encoding="utf-8")
    visible_ids = extract_visible_atom_ids(markdown)
    audit.visible_atoms = len(visible_ids)
    audit.dashboard_atoms = extract_dashboard_atoms(markdown)

    if audit.dashboard_atoms is None:
        audit.issues.append(Issue("incohérence de volumétrie", doc_path, "Volumetrie Atomes absente du tableau de bord du document maitre."))
    elif audit.expected_atoms is not None and audit.dashboard_atoms != audit.expected_atoms:
        audit.issues.append(
            Issue(
                "incohérence de volumétrie",
                doc_path,
                f"Tableau de bord Atomes={audit.dashboard_atoms}, master_docs_index atoms={audit.expected_atoms}.",
            )
        )

    audit.missing_atom_ids = sorted(
        atom_id for atom_id in visible_ids
        if atom_id not in atom_ids and atom_id not in alias_lookup
    )
    audit.alias_resolved_atoms = sum(
        1 for atom_id in visible_ids
        if atom_id not in atom_ids and atom_id in alias_lookup
    )
    audit.found_atoms = audit.visible_atoms - len(audit.missing_atom_ids)
    for atom_id in audit.missing_atom_ids:
        audit.issues.append(Issue("atome introuvable", doc_path, f"{atom_id} est visible dans le DM mais absent de exports/generated/atoms.json."))

    if audit.expected_atoms and audit.visible_atoms == 0:
        audit.issues.append(Issue("atome manquant", doc_path, "Aucun identifiant atomique visible alors que l'index declare des atomes."))

    if audit.issues:
        blocking_kinds = {"document maître absent sur disque", "document maître invalide", "manifeste incohérent"}
        if any(issue.kind in blocking_kinds for issue in audit.issues):
            audit.status = "non traçable"
        else:
            audit.status = "partiellement traçable"
    else:
        audit.status = "traçable"
    return audit


def detect_manifest_index_disk_drift(
    documents: list[dict[str, Any]],
    master_index: dict[str, dict[str, Any]],
    disk_paths: set[str],
) -> list[Issue]:
    manifest_paths = {
        valid_path
        for doc in documents
        for valid_path, issue in [validate_master_doc_path(doc.get("path", ""))]
        if issue is None and valid_path is not None
    }
    index_paths = set(master_index)
    issues: list[Issue] = []

    for path in sorted(disk_paths - manifest_paths):
        issues.append(Issue("document maître hors manifeste", path, "Document maitre present sur disque mais absent de chapters/master_docs.json."))
    for path in sorted((disk_paths - index_paths) - manifest_paths):
        issues.append(Issue("document maître absent de l'index", path, "Document maitre present sur disque mais absent de exports/generated/master_docs_index.json."))
    for path in sorted(index_paths - manifest_paths):
        issues.append(Issue("dérive manifeste / index", path, "Document present dans master_docs_index mais absent du manifeste."))
    return issues


def summarize(audits: list[DmAudit], global_issues: list[Issue], disk_paths: set[str]) -> dict[str, int]:
    all_issues = global_issues + [issue for audit in audits for issue in audit.issues]
    return {
        "documents_manifestes": len(audits),
        "documents_sur_disque": len(disk_paths),
        "documents_tracables": sum(1 for audit in audits if audit.status == "traçable"),
        "documents_partiellement_tracables": sum(1 for audit in audits if audit.status == "partiellement traçable"),
        "documents_non_tracables": sum(1 for audit in audits if audit.status == "non traçable"),
        "atomes_visibles": sum(audit.visible_atoms for audit in audits),
        "atomes_retrouves": sum(audit.found_atoms for audit in audits),
        "identifiants_resolus_par_alias": sum(audit.alias_resolved_atoms for audit in audits),
        "ecarts_detectes": len(all_issues),
        "atomes_introuvables": sum(1 for issue in all_issues if issue.kind == "atome introuvable"),
        "incoherences_volumetrie": sum(1 for issue in all_issues if issue.kind == "incohérence de volumétrie"),
        "documents_absents_sur_disque": sum(1 for issue in all_issues if issue.kind == "document maître absent sur disque"),
        "documents_invalides": sum(1 for issue in all_issues if issue.kind == "document maître invalide"),
        "documents_hors_manifeste": sum(1 for issue in all_issues if issue.kind == "document maître hors manifeste"),
        "documents_absents_index": sum(1 for issue in all_issues if issue.kind == "document maître absent de l'index"),
        "derives_manifest_index": sum(1 for issue in all_issues if issue.kind == "dérive manifeste / index"),
        "manifestes_incoherents": sum(1 for issue in all_issues if issue.kind == "manifeste incohérent"),
    }


def render_report(audits: list[DmAudit], global_issues: list[Issue], disk_paths: set[str]) -> str:
    summary = summarize(audits, global_issues, disk_paths)
    lines: list[str] = [
        "# Controle M1 - DM vers atomes",
        "",
        "Rapport genere par `python3 tools/check_dm_atoms_traceability.py`.",
        "",
        "Ce controle est strictement en lecture sur les documents maitres, exports, registres, atomes et manifeste. Il produit des constats et ne corrige aucun ecart.",
        "",
        "Limite MVP : le controle verifie les identifiants atomiques explicitement visibles et les volumetries principales. Il ne realise pas de tracabilite passage par passage.",
        "",
        "### Résumé global",
        "",
        "| Indicateur | Valeur |",
        "|------------|---------|",
    ]

    labels = [
        ("Documents declares dans le manifeste", "documents_manifestes"),
        ("Documents maîtres sur disque", "documents_sur_disque"),
        ("Documents traçables", "documents_tracables"),
        ("Documents partiellement traçables", "documents_partiellement_tracables"),
        ("Documents non traçables", "documents_non_tracables"),
        ("Atomes visibles", "atomes_visibles"),
        ("Atomes retrouvés", "atomes_retrouves"),
        ("Identifiants résolus par alias", "identifiants_resolus_par_alias"),
        ("Écarts détectés", "ecarts_detectes"),
        ("Atomes introuvables", "atomes_introuvables"),
        ("Incohérences de volumétrie", "incoherences_volumetrie"),
        ("Documents maîtres absents sur disque", "documents_absents_sur_disque"),
        ("Documents maîtres invalides", "documents_invalides"),
        ("Documents maîtres hors manifeste", "documents_hors_manifeste"),
        ("Documents maîtres absents de l'index", "documents_absents_index"),
        ("Dérives manifeste / index", "derives_manifest_index"),
        ("Manifestes incohérents", "manifestes_incoherents"),
    ]
    for label, key in labels:
        lines.append(f"| {label} | {summary[key]} |")

    lines.extend([
        "",
        "### Audit par document maître",
        "",
        "| DM | Statut | Atomes visibles | Atomes retrouvés | Écarts |",
        "|----|----|----|----|----|",
    ])
    for audit in audits:
        issue_summary = "Aucun"
        if audit.issues:
            issue_counts: dict[str, int] = {}
            for issue in audit.issues:
                issue_counts[issue.kind] = issue_counts.get(issue.kind, 0) + 1
            issue_summary = ", ".join(f"{kind}: {count}" for kind, count in sorted(issue_counts.items()))
        lines.append(
            f"| `{escape_md(audit.path)}` | {escape_md(audit.status)} | "
            f"{audit.visible_atoms} | {audit.found_atoms} | {escape_md(issue_summary)} |"
        )

    lines.extend([
        "",
        "### Écarts détectés",
        "",
    ])
    all_issues = global_issues + [issue for audit in audits for issue in audit.issues]
    if not all_issues:
        lines.append("Aucun écart détecté dans le perimetre MVP.")
    else:
        for issue in all_issues:
            lines.append(f"- **{escape_md(issue.kind)}** — `{escape_md(issue.dm)}` : {escape_md(issue.detail)}")

    lines.extend([
        "",
        "### Limites observees",
        "",
        "- Les documents maitres exposent des atomes visibles, mais pas une table complete passage -> atome.",
        "- Le controle compare la volumetrie `Atomes` du tableau de bord avec `exports/generated/master_docs_index.json`, pas le nombre d'atomes visibles avec le nombre total d'atomes rattaches.",
        "- Les variantes historiques `Sxx-000` et `Sxx-A000` sont resolues comme alias lorsqu'une forme correspond a un atome exporte.",
        "- Certains atomes peuvent etre rattaches au document maitre sans etre affiches dans les sections visibles, ce qui n'est pas traite comme un ecart par le MVP.",
        "- Les sources, registres, citations et exports autres que `atoms.json` et `master_docs_index.json` restent hors perimetre.",
        "",
        "### Faux positifs possibles",
        "",
        "- Un atome non affiche peut etre volontairement omis par selection redactionnelle.",
        "- Un identifiant visible dans une section de relations peut etre verifie comme atome existant sans prouver qu'il soutient un passage precis.",
        "- Une volumetrie correcte ne prouve pas la derivabilite fine du contenu redactionnel.",
        "- Une absence d'ecart dans ce rapport ne vaut pas validation DM -> sources, DM -> registres ou DM -> exports.",
        "",
    ])
    return "\n".join(lines)


def run(output: Path) -> int:
    documents, manifest_issues = load_manifest(MANIFEST_PATH)
    atom_ids = load_atom_ids(ATOMS_EXPORT)
    alias_lookup = build_alias_lookup(atom_ids)
    master_index, index_issues = load_master_index(MASTER_DOCS_INDEX)
    disk_paths = scan_disk_master_docs()
    global_issues = manifest_issues + index_issues + detect_manifest_index_disk_drift(documents, master_index, disk_paths)
    audits = [audit_document(doc, atom_ids, alias_lookup, master_index) for doc in documents]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(audits, global_issues, disk_paths), encoding="utf-8")

    summary = summarize(audits, global_issues, disk_paths)
    print(f"Rapport: {rel(output)}")
    print(
        "DM traçables: {documents_tracables}/{documents_manifestes}; "
        "écarts: {ecarts_detectes}; atomes visibles: {atomes_visibles}; "
        "atomes retrouvés: {atomes_retrouves}".format(**summary)
    )
    return 1 if summary["ecarts_detectes"] else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Controle M1 P0 non destructif de tracabilite DM -> atomes."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT.relative_to(REPO_ROOT)),
        help="Chemin du rapport Markdown a ecrire (defaut: reports/m1/dm_atoms_traceability.md).",
    )
    args = parser.parse_args(argv)
    try:
        output = resolve_output_path(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
