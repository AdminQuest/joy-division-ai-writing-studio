#!/usr/bin/env python3
"""M1 P0 control: document master -> canonical sources consistency.

This control is intentionally read-only for the documentary corpus. It reads the
master-doc manifest, the canonical source register, and master documents, then
writes a regenerable report under reports/m1/. It does not rebuild, fix, or
mutate any documentary source, register, export, manifest, or master document.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports" / "m1"
DEFAULT_REPORT = REPORT_DIR / "dm_sources_consistency.md"
MANIFEST_PATH = REPO_ROOT / "chapters" / "master_docs.json"
SOURCES_REGISTER = REPO_ROOT / "data" / "registre.json"

SOURCE_ID_RE = re.compile(r"(?<![A-Z0-9-])S\d{2,3}(?![-A-Z0-9])")
CANONICAL_SOURCE_ID_RE = re.compile(r"S\d{2,3}")


@dataclass
class Issue:
    kind: str
    dm: str
    detail: str
    severity: str = "majeur"


@dataclass
class DmAudit:
    path: str
    title: str = ""
    status: str = "non cohérent"
    visible_sources: set[str] = field(default_factory=set)
    found_sources: set[str] = field(default_factory=set)
    unknown_sources: set[str] = field(default_factory=set)
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


def validate_master_doc_path_lexical(raw_path: object) -> tuple[str | None, Issue | None]:
    raw_display = str(raw_path)
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None, Issue("manifeste incohérent", raw_display, "Chemin de document maitre absent ou non textuel.", severity="bloquant")

    candidate = Path(raw_path)
    if candidate.is_absolute():
        return None, Issue("manifeste incohérent", raw_path, "Chemin de document maitre absolu refuse.", severity="bloquant")
    if any(part == ".." for part in candidate.parts):
        return None, Issue("manifeste incohérent", raw_path, "Chemin de document maitre contenant '..' refuse.", severity="bloquant")

    parts = candidate.parts
    if len(parts) != 3 or parts[0] != "chapters" or parts[2] != "document_maitre.md" or parts[1] in {"", ".", ".."}:
        return None, Issue(
            "manifeste incohérent",
            raw_path,
            "Chemin de document maitre invalide: attendu chapters/*/document_maitre.md.",
            severity="bloquant",
        )

    return candidate.as_posix(), None


def validate_master_doc_filesystem_path(doc_path: str) -> Issue | None:
    candidate = Path(doc_path)
    chapter = candidate.parts[1]
    chapter_dir = REPO_ROOT / "chapters" / chapter
    full_path = chapter_dir / "document_maitre.md"
    expected_resolved = (REPO_ROOT / "chapters").resolve(strict=False) / chapter / "document_maitre.md"

    if chapter_dir.is_symlink() or full_path.is_symlink():
        return Issue(
            "document maître invalide",
            doc_path,
            "Chemin de document maître refusé : composant symlinké ou cible résolue non conforme.",
            severity="bloquant",
        )

    if full_path.resolve(strict=False) != expected_resolved:
        return Issue(
            "document maître invalide",
            doc_path,
            "Chemin de document maître refusé : composant symlinké ou cible résolue non conforme.",
            severity="bloquant",
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
        issues.append(Issue("manifeste incohérent", rel(path), "Champ documents absent ou invalide.", severity="bloquant"))
        return [], issues

    seen_paths: set[str] = set()
    seen_chapters: set[int] = set()
    for doc in documents:
        doc_path = str(doc.get("path", "<chemin absent>"))
        chapter = doc.get("chapter")
        if doc_path in seen_paths:
            issues.append(Issue("manifeste incohérent", doc_path, "Chemin duplique dans le manifeste.", severity="bloquant"))
        seen_paths.add(doc_path)
        if isinstance(chapter, int):
            if chapter in seen_chapters:
                issues.append(Issue("manifeste incohérent", doc_path, f"Chapitre duplique dans le manifeste: {chapter}.", severity="bloquant"))
            seen_chapters.add(chapter)
        else:
            issues.append(Issue("manifeste incohérent", doc_path, "Chapitre absent ou non numerique.", severity="bloquant"))
    return documents, issues


def load_canonical_source_ids(path: Path) -> tuple[set[str], list[Issue]]:
    payload = load_json(path)
    if not isinstance(payload, list):
        return set(), [Issue("registre source invalide", rel(path), "Liste JSON attendue dans data/registre.json.", severity="bloquant")]

    source_ids: set[str] = set()
    issues: list[Issue] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            continue
        source_id = item.get("id")
        if not isinstance(source_id, str):
            continue
        source_id = source_id.strip()
        if CANONICAL_SOURCE_ID_RE.fullmatch(source_id):
            if source_id in source_ids:
                issues.append(Issue("registre source incohérent", rel(path), f"Identifiant source duplique: {source_id}.", severity="bloquant"))
            source_ids.add(source_id)
        elif source_id.startswith("S"):
            issues.append(Issue("registre source incohérent", rel(path), f"Identifiant source non canonique a l'index {index}: {source_id}.", severity="bloquant"))
    return source_ids, issues


def scan_disk_master_docs() -> tuple[set[str], list[Issue]]:
    disk_paths: set[str] = set()
    issues: list[Issue] = []
    for path in sorted((REPO_ROOT / "chapters").glob("*/document_maitre.md")):
        doc_path = rel(path)
        valid_path, path_issue = validate_master_doc_path_lexical(doc_path)
        if path_issue is not None:
            issues.append(path_issue)
            continue
        assert valid_path is not None
        filesystem_issue = validate_master_doc_filesystem_path(valid_path)
        if filesystem_issue is not None:
            issues.append(Issue("document maître invalide", valid_path, "Document maître présent sur disque mais refusé : composant symlinké ou cible résolue non conforme.", severity="bloquant"))
            continue
        if path.is_file():
            disk_paths.add(valid_path)
    return disk_paths, issues


def extract_visible_source_ids(markdown: str) -> set[str]:
    return set(SOURCE_ID_RE.findall(markdown))


def audit_document(doc: dict[str, Any], canonical_source_ids: set[str]) -> DmAudit:
    raw_doc_path = doc.get("path", "")
    doc_path = str(raw_doc_path)
    title = str(doc.get("title", ""))
    audit = DmAudit(path=doc_path, title=title)

    valid_path, path_issue = validate_master_doc_path_lexical(raw_doc_path)
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

    if not full_path.exists():
        audit.issues.append(Issue("document maître absent sur disque", doc_path, "Fichier declare dans le manifeste mais absent du depot.", severity="bloquant"))
        return audit

    markdown = full_path.read_text(encoding="utf-8")
    audit.visible_sources = extract_visible_source_ids(markdown)
    audit.found_sources = audit.visible_sources & canonical_source_ids
    audit.unknown_sources = audit.visible_sources - canonical_source_ids

    for source_id in sorted(audit.unknown_sources):
        audit.issues.append(
            Issue(
                "source inconnue",
                doc_path,
                f"{source_id} est visible dans le DM mais absent du registre canonique data/registre.json.",
                severity="majeur",
            )
        )

    audit.status = "non cohérent" if audit.issues else "cohérent"
    return audit


def detect_manifest_disk_drift(documents: list[dict[str, Any]], disk_paths: set[str]) -> list[Issue]:
    manifest_paths = {
        valid_path
        for doc in documents
        for valid_path, issue in [validate_master_doc_path_lexical(doc.get("path", ""))]
        if issue is None and valid_path is not None
    }
    issues: list[Issue] = []
    for path in sorted(disk_paths - manifest_paths):
        issues.append(Issue("document maître hors manifeste", path, "Document maitre present sur disque mais absent de chapters/master_docs.json.", severity="bloquant"))
    return issues


def orphan_source_ids(canonical_source_ids: set[str], audits: list[DmAudit]) -> set[str]:
    mobilized = set().union(*(audit.visible_sources for audit in audits)) if audits else set()
    return canonical_source_ids - mobilized


def summarize(
    audits: list[DmAudit],
    global_issues: list[Issue],
    disk_paths: set[str],
    canonical_source_ids: set[str],
) -> dict[str, int]:
    all_issues = global_issues + [issue for audit in audits for issue in audit.issues]
    orphans = orphan_source_ids(canonical_source_ids, audits)
    unknown = sum(len(audit.unknown_sources) for audit in audits)
    return {
        "documents_declares": len(audits),
        "documents_presents": len(disk_paths),
        "documents_coherents": sum(1 for audit in audits if audit.status == "cohérent"),
        "documents_non_coherents": sum(1 for audit in audits if audit.status == "non cohérent"),
        "sources_canoniques": len(canonical_source_ids),
        "sources_visibles": sum(len(audit.visible_sources) for audit in audits),
        "sources_retrouvees": sum(len(audit.found_sources) for audit in audits),
        "sources_inconnues": unknown,
        "sources_mentionnees_non_declarees": unknown,
        "sources_orphelines": len(orphans),
        "ecarts_detectes": len(all_issues),
        "manifestes_incoherents": sum(1 for issue in all_issues if issue.kind == "manifeste incohérent"),
        "documents_absents_sur_disque": sum(1 for issue in all_issues if issue.kind == "document maître absent sur disque"),
        "documents_invalides": sum(1 for issue in all_issues if issue.kind == "document maître invalide"),
        "documents_hors_manifeste": sum(1 for issue in all_issues if issue.kind == "document maître hors manifeste"),
        "registres_sources_incoherents": sum(1 for issue in all_issues if issue.kind in {"registre source invalide", "registre source incohérent"}),
    }


def render_issue_summary(audit: DmAudit) -> str:
    if not audit.issues:
        return "Aucun écart"
    counts: dict[str, int] = {}
    for issue in audit.issues:
        counts[issue.kind] = counts.get(issue.kind, 0) + 1
    return ", ".join(f"{kind}: {count}" for kind, count in sorted(counts.items()))


def render_report(
    audits: list[DmAudit],
    global_issues: list[Issue],
    disk_paths: set[str],
    canonical_source_ids: set[str],
) -> str:
    summary = summarize(audits, global_issues, disk_paths, canonical_source_ids)
    orphans = sorted(orphan_source_ids(canonical_source_ids, audits))
    all_issues = global_issues + [issue for audit in audits for issue in audit.issues]

    lines: list[str] = [
        "# Controle M1 - DM vers sources",
        "",
        "## Objet",
        "",
        "Rapport genere par `python3 tools/check_dm_sources_consistency.py`.",
        "",
        "Ce controle est strictement en lecture sur les documents maitres, le manifeste et le registre canonique `data/registre.json`. Il produit des constats et ne corrige aucun ecart.",
        "",
        "## Périmètre",
        "",
        "Perimetre M1.3 couvert : existence des identifiants de sources `Sxx` ou `Sxxx` explicitement visibles dans les documents maitres et presence de ces identifiants dans `data/registre.json`.",
        "",
        "Dans ce rapport, une source mentionnee mais non declaree designe une reference visible qui n'est pas declaree dans le registre canonique.",
        "",
        "Hors perimetre : citations, atomes, relations, granularite section, granularite paragraphe, validite historiographique, qualite de source et usage correct de la source.",
        "",
        "## Résumé global",
        "",
        "| Indicateur | Valeur |",
        "|------------|---------|",
    ]
    labels = [
        ("Documents maîtres déclarés", "documents_declares"),
        ("Documents maîtres présents", "documents_presents"),
        ("Documents maîtres cohérents", "documents_coherents"),
        ("Documents maîtres non cohérents", "documents_non_coherents"),
        ("Sources canoniques", "sources_canoniques"),
        ("Sources visibles", "sources_visibles"),
        ("Sources retrouvées", "sources_retrouvees"),
        ("Sources inconnues", "sources_inconnues"),
        ("Sources mentionnées mais non déclarées", "sources_mentionnees_non_declarees"),
        ("Sources orphelines", "sources_orphelines"),
        ("Écarts détectés", "ecarts_detectes"),
        ("Manifestes incohérents", "manifestes_incoherents"),
        ("Documents maîtres absents sur disque", "documents_absents_sur_disque"),
        ("Documents maîtres invalides", "documents_invalides"),
        ("Documents maîtres hors manifeste", "documents_hors_manifeste"),
        ("Registres sources incohérents", "registres_sources_incoherents"),
    ]
    for label, key in labels:
        lines.append(f"| {label} | {summary[key]} |")

    lines.extend([
        "",
        "## Audit par document maître",
        "",
        "| DM | Statut | Sources visibles | Sources retrouvées | Sources inconnues | Écarts |",
        "|----|--------|------------------|--------------------|-------------------|--------|",
    ])
    for audit in audits:
        unknown = ", ".join(sorted(audit.unknown_sources)) if audit.unknown_sources else "Aucune"
        lines.append(
            f"| `{escape_md(audit.path)}` | {escape_md(audit.status)} | "
            f"{len(audit.visible_sources)} | {len(audit.found_sources)} | {escape_md(unknown)} | {escape_md(render_issue_summary(audit))} |"
        )

    lines.extend([
        "",
        "## Sources inconnues",
        "",
    ])
    unknown_rows = [
        (audit.path, source_id)
        for audit in audits
        for source_id in sorted(audit.unknown_sources)
    ]
    if not unknown_rows:
        lines.append("Aucune source inconnue détectée.")
    else:
        for doc_path, source_id in unknown_rows:
            lines.append(f"- `{escape_md(source_id)}` — `{escape_md(doc_path)}` : absent de `data/registre.json`.")

    lines.extend([
        "",
        "## Sources orphelines",
        "",
    ])
    if not orphans:
        lines.append("Aucune source canonique orpheline détectée.")
    else:
        for source_id in orphans:
            lines.append(f"- `{escape_md(source_id)}` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.")

    lines.extend([
        "",
        "## Écarts détectés",
        "",
    ])
    if not all_issues:
        lines.append("Aucun écart détecté dans le perimetre M1.3.")
    else:
        for issue in all_issues:
            lines.append(f"- **{escape_md(issue.kind)}** — `{escape_md(issue.dm)}` : {escape_md(issue.detail)}")

    lines.extend([
        "",
        "## Conclusion",
        "",
    ])
    if summary["sources_inconnues"] == 0 and summary["ecarts_detectes"] == 0:
        lines.append("Le controle DM -> sources est conforme : les sources visibles dans les documents maitres existent dans le registre canonique.")
    else:
        lines.append("Le controle DM -> sources est non conforme : au moins une source visible est absente du registre canonique ou un ecart bloquant a ete detecte.")
    lines.append("")
    lines.append("Les sources orphelines sont listees comme information documentaire ; elles ne constituent pas un ecart bloquant dans le controle de niveau 1.")
    lines.append("")
    return "\n".join(lines)


def run(output: Path) -> int:
    documents, manifest_issues = load_manifest(MANIFEST_PATH)
    canonical_source_ids, register_issues = load_canonical_source_ids(SOURCES_REGISTER)
    disk_paths, disk_issues = scan_disk_master_docs()
    global_issues = manifest_issues + register_issues + disk_issues + detect_manifest_disk_drift(documents, disk_paths)
    audits = [audit_document(doc, canonical_source_ids) for doc in documents]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(audits, global_issues, disk_paths, canonical_source_ids), encoding="utf-8")

    summary = summarize(audits, global_issues, disk_paths, canonical_source_ids)
    print(f"Rapport: {rel(output)}")
    print(
        "DM cohérents: {documents_coherents}/{documents_declares}; "
        "écarts: {ecarts_detectes}; sources visibles: {sources_visibles}; "
        "sources retrouvées: {sources_retrouvees}; sources inconnues: {sources_inconnues}; "
        "sources orphelines: {sources_orphelines}".format(**summary)
    )
    return 1 if summary["sources_inconnues"] > 0 or summary["ecarts_detectes"] > 0 else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Controle M1 P0 non destructif de coherence DM -> sources."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT.relative_to(REPO_ROOT)),
        help="Chemin du rapport Markdown a ecrire (defaut: reports/m1/dm_sources_consistency.md).",
    )
    args = parser.parse_args(argv)
    try:
        output = resolve_output_path(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
