#!/usr/bin/env python3
"""M1 P0 control: document master -> registers consistency.

This control is intentionally read-only for the documentary corpus. It reads the
master-doc manifest, generated register exports, the master-doc index, and
master documents, then writes a regenerable report under reports/m1/. It does
not rebuild, fix, or mutate any documentary source, register, export, manifest,
or master document.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports" / "m1"
DEFAULT_REPORT = REPORT_DIR / "dm_registers_consistency.md"
MANIFEST_PATH = REPO_ROOT / "chapters" / "master_docs.json"
MASTER_DOCS_INDEX = REPO_ROOT / "exports" / "generated" / "master_docs_index.json"

P0_FAMILIES = ("people", "songs", "chronology", "quotes", "concerts", "sessions")
EXPORT_PATHS = {
    "people": REPO_ROOT / "exports" / "generated" / "people.json",
    "songs": REPO_ROOT / "exports" / "generated" / "songs.json",
    "chronology": REPO_ROOT / "exports" / "generated" / "chronology.json",
    "quotes": REPO_ROOT / "exports" / "generated" / "quotes.json",
    "concerts": REPO_ROOT / "exports" / "generated" / "concerts.json",
    "sessions": REPO_ROOT / "exports" / "generated" / "sessions.json",
}
INDEX_COUNTERS = {
    "people": "people",
    "songs": "songs",
    "chronology": "chronology",
    "quotes": "quotes",
}
DASHBOARD_LABELS = {
    "people": "Personnes",
    "songs": "Chansons",
    "chronology": "Événements chronologiques",
    "quotes": "Citations",
}

REGISTER_ID_PATTERNS = [
    ("concerts", re.compile(r"\b(?:JD-)?CONCERT-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("sessions", re.compile(r"\b(?:JD-)?SESSION-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("people", re.compile(r"\b(?:PERSON|PERS)-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("chronology", re.compile(r"\b(?:CHR|EVENT)-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("quotes", re.compile(r"\b(?:CIT-S\d{2,3}-\d{3}|S\d{2,3}-Q\d{3})\b")),
    ("songs", re.compile(r"\bSONG-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
]
NON_MVP_PATTERNS = [
    ("concepts", re.compile(r"\bCONCEPT-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("motifs", re.compile(r"\bMOTIF-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("myths", re.compile(r"\bMYTH-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("places", re.compile(r"\bPLACE-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("relations", re.compile(r"\bREL-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
    ("organizations", re.compile(r"\b(?:ORG|ORGANIZATION)-[A-Za-z0-9][A-Za-z0-9_-]*\b")),
]


@dataclass
class Issue:
    kind: str
    dm: str
    detail: str
    family: str = ""
    severity: str = "informationnel"


@dataclass
class RegisterRecord:
    id: str
    label: str = ""
    aliases: set[str] = field(default_factory=set)


@dataclass
class VisibleRef:
    id: str
    label: str = ""


@dataclass
class DmAudit:
    path: str
    title: str = ""
    status: str = "non cohérent"
    visible_counts: dict[str, int] = field(default_factory=dict)
    found_counts: dict[str, int] = field(default_factory=dict)
    dashboard_counts: dict[str, int | None] = field(default_factory=dict)
    expected_counts: dict[str, int | None] = field(default_factory=dict)
    non_mvp_counts: dict[str, int] = field(default_factory=dict)
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


def normalize_label(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("«", "").replace("»", "").replace('"', "").replace("'", "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


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
        valid_path, path_issue = validate_master_doc_path_lexical(path_value)
        if path_issue is not None:
            issues.append(path_issue)
            continue
        assert valid_path is not None
        filesystem_issue = validate_master_doc_filesystem_path(valid_path)
        if filesystem_issue is not None:
            issues.append(filesystem_issue)
            continue
        if valid_path in index:
            issues.append(Issue("manifeste incohérent", path_value, "Chemin duplique dans master_docs_index."))
        index[valid_path] = chapter
    return index, issues


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
            issues.append(Issue("document maître invalide", valid_path, "Document maître présent sur disque mais refusé : composant symlinké ou cible résolue non conforme."))
            continue
        if path.is_file():
            disk_paths.add(valid_path)
    return disk_paths, issues


def record_label(data: dict[str, Any], family: str) -> str:
    candidates_by_family = {
        "people": ("name", "nom", "full_name", "label"),
        "songs": ("song", "title", "titre", "name", "label"),
        "chronology": ("event", "label", "title"),
        "quotes": ("texte", "citation_originale", "label"),
        "concerts": ("label", "lieu", "heading"),
        "sessions": ("label", "titre", "name"),
    }
    for key in candidates_by_family[family]:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def record_aliases(data: dict[str, Any]) -> set[str]:
    aliases: set[str] = set()
    for key in ("alt_names", "same_as", "aliases"):
        value = data.get(key)
        if isinstance(value, str):
            aliases.add(value)
        elif isinstance(value, list):
            aliases.update(item for item in value if isinstance(item, str))
    return aliases


def load_register_export(family: str, path: Path) -> tuple[dict[str, RegisterRecord], list[Issue]]:
    issues: list[Issue] = []
    if not path.exists():
        return {}, [Issue("registre absent", rel(path), "Export de registre absent.", family=family, severity="bloquant")]

    payload = load_json(path)
    if not isinstance(payload, list):
        return {}, [Issue("registre absent", rel(path), "Export de registre invalide: liste JSON attendue.", family=family, severity="bloquant")]

    records: dict[str, RegisterRecord] = {}
    for item in payload:
        if not isinstance(item, dict):
            continue
        data = item.get("data") if isinstance(item.get("data"), dict) else {}
        candidates = [item, data]
        ids: set[str] = set()
        label = ""
        aliases: set[str] = set()
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            value = candidate.get("id")
            if isinstance(value, str) and value.strip():
                ids.add(value.strip())
            same_as = candidate.get("same_as")
            if isinstance(same_as, str) and same_as.strip():
                ids.add(same_as.strip())
            if not label:
                label = record_label(candidate, family)
            aliases.update(record_aliases(candidate))
        for item_id in ids:
            records[item_id] = RegisterRecord(id=item_id, label=label, aliases=aliases)
    return records, issues


def load_register_exports() -> tuple[dict[str, dict[str, RegisterRecord]], list[Issue]]:
    exports: dict[str, dict[str, RegisterRecord]] = {}
    issues: list[Issue] = []
    for family, path in EXPORT_PATHS.items():
        records, export_issues = load_register_export(family, path)
        exports[family] = records
        issues.extend(export_issues)
    return exports, issues


def classify_register_id(register_id: str) -> str | None:
    for family, pattern in REGISTER_ID_PATTERNS:
        if pattern.fullmatch(register_id):
            return family
    return None


def table_label_for_id(line: str, register_id: str) -> str:
    stripped = line.strip()
    if not stripped.startswith("|") or "|" not in stripped[1:]:
        return ""
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if len(cells) >= 2 and cells[0] == register_id:
        return cells[1]
    return ""


def bullet_label_for_id(line: str, register_id: str) -> str:
    stripped = line.strip()
    if not stripped.startswith("-"):
        return ""
    text = stripped.lstrip("-").strip()
    text = text.replace("**", "")
    if not text.startswith(register_id):
        return ""
    parts = [part.strip() for part in text.split("—")]
    if len(parts) >= 2:
        return parts[1]
    return ""


def visible_label_for_id(line: str, register_id: str) -> str:
    return table_label_for_id(line, register_id) or bullet_label_for_id(line, register_id)


def extract_visible_register_refs(markdown: str) -> tuple[dict[str, dict[str, VisibleRef]], dict[str, set[str]]]:
    refs: dict[str, dict[str, VisibleRef]] = {family: {} for family in P0_FAMILIES}
    non_mvp: dict[str, set[str]] = {}
    for line in markdown.splitlines():
        for family, pattern in REGISTER_ID_PATTERNS:
            for match in pattern.finditer(line):
                register_id = match.group(0)
                refs[family].setdefault(register_id, VisibleRef(id=register_id, label=visible_label_for_id(line, register_id)))
        for family, pattern in NON_MVP_PATTERNS:
            for match in pattern.finditer(line):
                non_mvp.setdefault(family, set()).add(match.group(0))
    return refs, non_mvp


def extract_dashboard_counts(markdown: str) -> dict[str, int | None]:
    counts: dict[str, int | None] = {family: None for family in INDEX_COUNTERS}
    for family, label in DASHBOARD_LABELS.items():
        escaped_label = re.escape(label)
        match = re.search(rf"^\|\s*{escaped_label}\s*\|\s*(\d+)\s*\|", markdown, re.MULTILINE)
        if match:
            counts[family] = int(match.group(1))
    return counts


def label_diverges(visible_label: str, record: RegisterRecord, family: str) -> bool:
    if family not in {"people", "songs", "chronology", "sessions"}:
        return False
    if not visible_label or not record.label:
        return False
    visible = normalize_label(visible_label)
    canonical = normalize_label(record.label)
    if not visible or not canonical or visible == canonical:
        return False
    aliases = {normalize_label(alias) for alias in record.aliases}
    return visible not in aliases


def audit_document(
    doc: dict[str, Any],
    register_exports: dict[str, dict[str, RegisterRecord]],
    master_index: dict[str, dict[str, Any]],
) -> DmAudit:
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

    index_entry = master_index.get(doc_path)
    if index_entry is None:
        audit.issues.append(Issue("document maître absent de l'index", doc_path, "Document present dans le manifeste mais absent de exports/generated/master_docs_index.json.", severity="bloquant"))
    else:
        for family, index_key in INDEX_COUNTERS.items():
            expected = index_entry.get(index_key)
            audit.expected_counts[family] = expected if isinstance(expected, int) else None
            if expected is None:
                audit.issues.append(Issue("compteur incohérent", doc_path, f"Compteur {index_key} absent dans master_docs_index.", family=family, severity="mineur"))
            elif not isinstance(expected, int):
                audit.issues.append(Issue("compteur incohérent", doc_path, f"Compteur {index_key} invalide dans master_docs_index.", family=family, severity="majeur"))

    if not full_path.exists():
        audit.issues.append(Issue("document maître absent sur disque", doc_path, "Fichier declare dans le manifeste mais absent du depot.", severity="bloquant"))
        return audit

    markdown = full_path.read_text(encoding="utf-8")
    visible_refs, non_mvp = extract_visible_register_refs(markdown)
    audit.dashboard_counts = extract_dashboard_counts(markdown)
    audit.non_mvp_counts = {family: len(ids) for family, ids in non_mvp.items()}

    for family in P0_FAMILIES:
        records = register_exports.get(family, {})
        refs = visible_refs.get(family, {})
        audit.visible_counts[family] = len(refs)
        found = 0
        for register_id, visible_ref in sorted(refs.items()):
            record = records.get(register_id)
            if record is None:
                audit.issues.append(Issue("identifiant introuvable", doc_path, f"{register_id} est visible dans le DM mais absent de {rel(EXPORT_PATHS[family])}.", family=family, severity="majeur"))
                continue
            found += 1
            if label_diverges(visible_ref.label, record, family):
                audit.issues.append(Issue("libellé divergent", doc_path, f"{register_id}: libelle visible `{visible_ref.label}` ; libelle exporte `{record.label}`.", family=family, severity="mineur"))
        audit.found_counts[family] = found

    for family, index_key in INDEX_COUNTERS.items():
        dashboard_value = audit.dashboard_counts.get(family)
        expected_value = audit.expected_counts.get(family)
        if dashboard_value is None:
            audit.issues.append(Issue("compteur incohérent", doc_path, f"Compteur {DASHBOARD_LABELS[family]} absent du tableau de bord du document maitre.", family=family, severity="mineur"))
        elif expected_value is not None and dashboard_value != expected_value:
            audit.issues.append(Issue("compteur incohérent", doc_path, f"Tableau de bord {DASHBOARD_LABELS[family]}={dashboard_value}, master_docs_index {index_key}={expected_value}.", family=family, severity="majeur"))

    for family, count in sorted(audit.non_mvp_counts.items()):
        if count:
            audit.issues.append(Issue("famille non couverte", doc_path, f"{count} identifiant(s) visibles pour la famille `{family}` hors MVP.", family=family, severity="informationnel"))

    blocking_kinds = {"document maître absent sur disque", "document maître invalide", "manifeste incohérent", "registre absent"}
    consistency_issues = [issue for issue in audit.issues if issue.kind != "famille non couverte"]
    if any(issue.kind in blocking_kinds or issue.severity == "bloquant" for issue in consistency_issues):
        audit.status = "non cohérent"
    elif consistency_issues:
        audit.status = "partiellement cohérent"
    else:
        audit.status = "cohérent"
    return audit


def detect_manifest_index_disk_drift(
    documents: list[dict[str, Any]],
    master_index: dict[str, dict[str, Any]],
    disk_paths: set[str],
) -> list[Issue]:
    manifest_paths = {
        valid_path
        for doc in documents
        for valid_path, issue in [validate_master_doc_path_lexical(doc.get("path", ""))]
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
    summary = {
        "documents_manifestes": len(audits),
        "documents_sur_disque": len(disk_paths),
        "documents_coherents": sum(1 for audit in audits if audit.status == "cohérent"),
        "documents_partiellement_coherents": sum(1 for audit in audits if audit.status == "partiellement cohérent"),
        "documents_non_coherents": sum(1 for audit in audits if audit.status == "non cohérent"),
        "ecarts_detectes": len(all_issues),
        "identifiants_introuvables": sum(1 for issue in all_issues if issue.kind == "identifiant introuvable"),
        "registres_absents": sum(1 for issue in all_issues if issue.kind == "registre absent"),
        "compteurs_incoherents": sum(1 for issue in all_issues if issue.kind == "compteur incohérent"),
        "familles_non_couvertes": sum(1 for issue in all_issues if issue.kind == "famille non couverte"),
        "relations_non_resolues": sum(1 for issue in all_issues if issue.kind == "relation non résolue"),
        "libelles_divergents": sum(1 for issue in all_issues if issue.kind == "libellé divergent"),
        "manifestes_incoherents": sum(1 for issue in all_issues if issue.kind == "manifeste incohérent"),
    }
    for family in P0_FAMILIES:
        summary[f"{family}_visibles"] = sum(audit.visible_counts.get(family, 0) for audit in audits)
        summary[f"{family}_retrouves"] = sum(audit.found_counts.get(family, 0) for audit in audits)
    return summary


def render_family_counts(audit: DmAudit) -> str:
    chunks = []
    for family in P0_FAMILIES:
        visible = audit.visible_counts.get(family, 0)
        found = audit.found_counts.get(family, 0)
        chunks.append(f"{family}: {found}/{visible}")
    return ", ".join(chunks)


def render_issue_summary(audit: DmAudit) -> str:
    blocking_counts: dict[str, int] = {}
    for issue in audit.issues:
        if issue.kind == "famille non couverte":
            continue
        blocking_counts[issue.kind] = blocking_counts.get(issue.kind, 0) + 1
    if not blocking_counts:
        return "Aucun écart MVP"
    return ", ".join(f"{kind}: {count}" for kind, count in sorted(blocking_counts.items()))


def render_report(audits: list[DmAudit], global_issues: list[Issue], disk_paths: set[str]) -> str:
    summary = summarize(audits, global_issues, disk_paths)
    lines: list[str] = [
        "# Controle M1 - DM vers registres",
        "",
        "## Objet",
        "",
        "Rapport genere par `python3 tools/check_dm_registers_consistency.py`.",
        "",
        "Ce controle est strictement en lecture sur les documents maitres, registres, exports et manifeste. Il produit des constats et ne corrige aucun ecart.",
        "",
        "## Périmètre",
        "",
        "Perimetre MVP couvert : personnes, chansons, chronologie, citations, concerts et sessions.",
        "",
        "Le controle verifie les identifiants de registres explicitement visibles dans `chapters/*/document_maitre.md`, leur presence dans les exports P0 disponibles, et les principales volumetries exposees par `exports/generated/master_docs_index.json`.",
        "",
        "Hors perimetre MVP : registres P1, relations transversales completes, sources, exports hors registres P0, tracabilite passage par passage, correction des registres ou des documents maitres.",
        "",
        "## Résumé global",
        "",
        "| Indicateur | Valeur |",
        "|------------|---------|",
    ]
    labels = [
        ("Documents declares dans le manifeste", "documents_manifestes"),
        ("Documents maîtres sur disque", "documents_sur_disque"),
        ("Documents cohérents", "documents_coherents"),
        ("Documents partiellement cohérents", "documents_partiellement_coherents"),
        ("Documents non cohérents", "documents_non_coherents"),
        ("Écarts détectés", "ecarts_detectes"),
        ("Identifiants introuvables", "identifiants_introuvables"),
        ("Registres absents", "registres_absents"),
        ("Compteurs incohérents", "compteurs_incoherents"),
        ("Familles non couvertes", "familles_non_couvertes"),
        ("Relations non résolues", "relations_non_resolues"),
        ("Libellés divergents", "libelles_divergents"),
        ("Manifestes incohérents", "manifestes_incoherents"),
    ]
    for label, key in labels:
        lines.append(f"| {label} | {summary[key]} |")
    for family in P0_FAMILIES:
        lines.append(f"| {family} visibles / retrouvés | {summary[f'{family}_retrouves']} / {summary[f'{family}_visibles']} |")

    lines.extend([
        "",
        "## Audit par document maître",
        "",
        "| DM | Statut | Registres P0 retrouvés | Écarts MVP | Familles hors MVP |",
        "|----|--------|------------------------|------------|-------------------|",
    ])
    for audit in audits:
        non_mvp = "Aucune"
        if audit.non_mvp_counts:
            non_mvp = ", ".join(f"{family}: {count}" for family, count in sorted(audit.non_mvp_counts.items()) if count)
        lines.append(
            f"| `{escape_md(audit.path)}` | {escape_md(audit.status)} | "
            f"{escape_md(render_family_counts(audit))} | {escape_md(render_issue_summary(audit))} | {escape_md(non_mvp)} |"
        )

    lines.extend([
        "",
        "## Écarts détectés",
        "",
    ])
    all_issues = global_issues + [issue for audit in audits for issue in audit.issues]
    if not all_issues:
        lines.append("Aucun écart détecté dans le perimetre MVP.")
    else:
        for issue in all_issues:
            family = f" — famille `{escape_md(issue.family)}`" if issue.family else ""
            lines.append(f"- **{escape_md(issue.kind)}**{family} — `{escape_md(issue.dm)}` : {escape_md(issue.detail)}")

    lines.extend([
        "",
        "## Limites observées",
        "",
        "- Le controle ne couvre que les familles P0 : personnes, chansons, chronologie, citations, concerts et sessions.",
        "- Les familles P1 visibles, comme concepts, motifs, mythes, lieux, organisations et relations, sont signalees comme hors MVP et ne sont pas resolues.",
        "- Les relations transversales ne sont pas controlees dans cette version.",
        "- La comparaison de libelles reste volontairement prudente et ne s'applique que lorsque le libelle visible et le libelle exporte sont objectivement disponibles.",
        "- Le controle ne verifie pas la tracabilite passage par passage.",
        "- Une volumetrie coherente ne prouve pas la coherence fine de tous les passages redactionnels.",
        "",
        "## Faux positifs possibles",
        "",
        "- Un libelle abrege ou typographiquement adapte dans un document maitre peut differer du libelle exporte sans signaler une erreur documentaire.",
        "- Une famille hors MVP peut etre volontairement visible dans un document maitre sans etre controlee par cette premiere version.",
        "- Un identifiant absent d'un export P0 peut relever d'un registre specialise non encore consolide plutot que d'une erreur du document maitre.",
        "- Les compteurs peuvent rester coherents alors que certains objets visibles sont des selections redactionnelles.",
        "",
        "## Conclusion",
        "",
    ])
    if summary["identifiants_introuvables"] or summary["compteurs_incoherents"] or summary["libelles_divergents"] or summary["registres_absents"]:
        lines.append("Le controle DM -> registres est partiellement concluant dans le perimetre MVP : des ecarts doivent etre relus avant toute correction separee.")
    else:
        lines.append("Le controle DM -> registres est concluant dans le perimetre MVP : les identifiants P0 visibles sont retrouves dans les exports disponibles et les volumetries principales sont coherentes.")
    lines.append("")
    lines.append("Ce rapport ne vaut pas validation des registres P1, des sources, des exports complets ou de la coherence passage par passage.")
    lines.append("")
    return "\n".join(lines)


def run(output: Path) -> int:
    documents, manifest_issues = load_manifest(MANIFEST_PATH)
    register_exports, export_issues = load_register_exports()
    master_index, index_issues = load_master_index(MASTER_DOCS_INDEX)
    disk_paths, disk_issues = scan_disk_master_docs()
    global_issues = manifest_issues + export_issues + index_issues + disk_issues + detect_manifest_index_disk_drift(documents, master_index, disk_paths)
    audits = [audit_document(doc, register_exports, master_index) for doc in documents]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(audits, global_issues, disk_paths), encoding="utf-8")

    summary = summarize(audits, global_issues, disk_paths)
    print(f"Rapport: {rel(output)}")
    print(
        "DM cohérents: {documents_coherents}/{documents_manifestes}; "
        "écarts: {ecarts_detectes}; identifiants introuvables: {identifiants_introuvables}; "
        "compteurs incohérents: {compteurs_incoherents}".format(**summary)
    )
    return 1 if any(issue.severity in {"bloquant", "majeur"} for issue in global_issues + [issue for audit in audits for issue in audit.issues if issue.kind != "famille non couverte"]) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Controle M1 P0 non destructif de coherence DM -> registres."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT.relative_to(REPO_ROOT)),
        help="Chemin du rapport Markdown a ecrire (defaut: reports/m1/dm_registers_consistency.md).",
    )
    args = parser.parse_args(argv)
    try:
        output = resolve_output_path(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
