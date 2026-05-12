#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Repo audit v0.1

Autonomous documentary audit for the Joy Division AI Writing Studio repository.

This tool does not rebuild the documentary exports. It parses the repository,
reuses the build_registers parser, and writes a human-readable audit report to:

    exports/generated/audit_repo.md

It is intentionally stricter and more synthetic than the RAG exports. Its purpose
is to help the maintainer decide what to fix first:

1. blocking errors;
2. unknown YAML blocks;
3. source registry issues;
4. v2 migration debt;
5. documentary coverage.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import build_registers as br

REPO_ROOT = br.REPO_ROOT
EXPORT_DIR = br.EXPORT_DIR
AUDIT_MD = EXPORT_DIR / "audit_repo.md"
AUDIT_JSON = EXPORT_DIR / "audit_repo.json"
AUDIT_CSV = EXPORT_DIR / "audit_repo_issues.csv"

V2_REQUIRED_ATOM_FIELDS = [
    "role_argumentatif",
    "niveau_preuve",
    "stabilite",
    "importance",
    "risque_surinterpretation",
    "liens_interchapitres",
    "liens_citations",
    "motifs",
    "concepts_derives",
]

V2_STRUCTURED_FIELDS = {
    "niveau_preuve": ["statut", "corroboration", "confiance"],
    "stabilite": ["statut", "risque_revision"],
    "importance": ["niveau"],
    "risque_surinterpretation": ["niveau"],
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(br.make_json_safe(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["level", "category", "file", "record_id", "message", "suggested_action"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: br.flatten_value(row.get(field)) for field in fields})


def source_ids_from_record(record: br.ParsedRecord) -> List[str]:
    data = record.data or {}
    ids: List[str] = []
    if isinstance(data.get("source_id"), str):
        ids.append(br.normalize_identifier(data["source_id"]))
    if isinstance(data.get("sources"), list):
        for source in data["sources"]:
            if isinstance(source, str) and re.match(r"^S\d+$", source):
                ids.append(br.normalize_identifier(source))
    return sorted(set(ids))


def chapter_values(record: br.ParsedRecord) -> List[str]:
    data = record.data or {}
    values: List[str] = []
    for key in ("chapitres", "chapters"):
        raw = data.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw if item)
        elif isinstance(raw, str) and raw.strip():
            values.append(raw.strip())
    return values


def is_v2_complete_atom(record: br.ParsedRecord) -> bool:
    if record.kind != "atom":
        return False
    data = record.data or {}
    for field in V2_REQUIRED_ATOM_FIELDS:
        if field not in data:
            return False
    for field, nested_keys in V2_STRUCTURED_FIELDS.items():
        value = data.get(field)
        if not isinstance(value, dict):
            return False
        for nested_key in nested_keys:
            if nested_key not in value:
                return False
    return True


def classify_issue(diag: br.Diagnostic) -> Tuple[str, str]:
    message = diag.message or ""
    if "Duplicate id" in message:
        return "duplicate_id", "Renommer ou fusionner l’identifiant en doublon."
    if "YAML parse error" in message:
        return "yaml_parse_error", "Corriger la syntaxe YAML du bloc concerné."
    if "Unable to infer documentary kind" in message:
        return "unknown_yaml_block", "Ajouter un champ discriminant ou supprimer le bloc YAML non documentaire."
    if "Missing required field" in message:
        missing = message.replace("Missing required field:", "").strip()
        if missing in V2_REQUIRED_ATOM_FIELDS:
            return "v2_migration_debt", "Reporter dans la migration v2 des atomes ; ne pas traiter comme blocage immédiat."
        return "missing_required_field", "Compléter le champ obligatoire."
    if "Invalid value" in message or "Invalid values" in message:
        return "invalid_controlled_value", "Aligner la valeur avec le schéma contrôlé."
    if "Field must be" in message:
        return "field_type_error", "Corriger le type YAML du champ."
    return "schema_warning", "Examiner le bloc et décider s’il relève d’une correction ou de la dette v2."


def build_audit(records: List[br.ParsedRecord], diagnostics: List[br.Diagnostic]) -> Dict[str, Any]:
    sources = br.build_source_registry(records)
    diagnostics_payload = br.build_diagnostics_payload(records, diagnostics, sources)

    record_counts = Counter(record.kind for record in records)
    source_counts = defaultdict(Counter)
    chapter_counts = Counter()
    file_counts = Counter(record.file for record in records)

    for record in records:
        for source_id in source_ids_from_record(record):
            source_counts[source_id][record.kind] += 1
        for chapter in chapter_values(record):
            chapter_counts[chapter] += 1

    classified_issues: List[Dict[str, Any]] = []
    issue_categories = Counter()
    issue_by_file = Counter()

    for diag in diagnostics:
        category, suggested_action = classify_issue(diag)
        issue_categories[category] += 1
        issue_by_file[diag.file] += 1
        classified_issues.append({
            "level": diag.level,
            "category": category,
            "file": diag.file,
            "record_id": diag.record_id,
            "message": diag.message,
            "suggested_action": suggested_action,
        })

    errors = [issue for issue in classified_issues if issue["level"] == "error"]
    unknowns = [issue for issue in classified_issues if issue["category"] == "unknown_yaml_block"]
    v2_debt = [issue for issue in classified_issues if issue["category"] == "v2_migration_debt"]

    atoms = [record for record in records if record.kind == "atom"]
    v2_complete_atoms = [record for record in atoms if is_v2_complete_atom(record)]

    declared = br.source_ids_from_registry()
    used_ids = set(br.source_ids_from_records(records))
    declared_ids = set(declared.keys())

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "summary": diagnostics_payload["summary"],
        "records_by_kind": dict(sorted(record_counts.items())),
        "records_by_source": {
            source_id: dict(counts)
            for source_id, counts in sorted(source_counts.items())
        },
        "records_by_chapter": dict(sorted(chapter_counts.items())),
        "top_files_by_record_count": file_counts.most_common(30),
        "issue_categories": dict(sorted(issue_categories.items())),
        "top_files_by_issue_count": issue_by_file.most_common(30),
        "blocking_errors": errors,
        "unknown_yaml_blocks": unknowns,
        "v2_migration": {
            "atoms_total": len(atoms),
            "atoms_v2_complete": len(v2_complete_atoms),
            "atoms_v2_incomplete": len(atoms) - len(v2_complete_atoms),
            "v2_missing_field_warnings": len(v2_debt),
        },
        "source_registry": {
            "declared_but_unused": [declared[source_id] for source_id in sorted(declared_ids - used_ids)],
            "used_but_missing_from_registre_json": sorted(used_ids - declared_ids),
            "weak_source_labels": br.weak_source_labels(sources),
            "exported_sources": sources,
        },
        "issues": classified_issues,
    }


def section_table(rows: Iterable[Tuple[Any, Any]], left: str, right: str) -> List[str]:
    output = [f"| {left} | {right} |", "|---|---:|"]
    for key, value in rows:
        output.append(f"| {key} | {value} |")
    return output


def write_markdown(path: Path, audit: Dict[str, Any], max_items: int = 40) -> None:
    summary = audit["summary"]
    lines: List[str] = [
        "# Audit du repo documentaire",
        "",
        f"Généré le : `{audit['generated_at']}`",
        "",
        "## 1. Verdict",
        "",
    ]

    errors = audit["blocking_errors"]
    unknowns = audit["unknown_yaml_blocks"]
    weak_labels = audit["source_registry"]["weak_source_labels"]
    missing_sources = audit["source_registry"]["used_but_missing_from_registre_json"]

    if errors:
        lines.append(f"Le repo n’est pas strict-compliant : {len(errors)} erreur(s) bloquante(s) subsistent.")
    elif missing_sources:
        lines.append("Le repo présente des sources utilisées mais absentes du registre canonique.")
    elif unknowns:
        lines.append(f"Le repo est techniquement exploitable, mais {len(unknowns)} bloc(s) YAML ne sont pas classés.")
    else:
        lines.append("Le repo ne présente pas d’erreur bloquante ni de bloc YAML inconnu.")

    if audit["v2_migration"]["atoms_v2_incomplete"]:
        lines.append(
            f"La dette principale reste la migration v2 : {audit['v2_migration']['atoms_v2_incomplete']} atome(s) incomplet(s) sur {audit['v2_migration']['atoms_total']}."
        )

    lines += [
        "",
        "## 2. Synthèse chiffrée",
        "",
        f"- Enregistrements : {summary.get('records_total', 0)}",
        f"- Erreurs : {summary.get('errors', 0)}",
        f"- Avertissements : {summary.get('warnings', 0)}",
        f"- Sources déclarées : {summary.get('sources_declared_in_registre_json', 0)}",
        f"- Sources utilisées : {summary.get('sources_used_in_records', 0)}",
        f"- Sources exportées : {summary.get('sources_exported', 0)}",
        f"- Sources utilisées absentes du registre : {summary.get('used_but_missing_from_registre_json', 0)}",
        f"- Libellés faibles : {summary.get('weak_source_labels', 0)}",
        "",
        "## 3. Enregistrements par type",
        "",
    ]
    lines += section_table(sorted(audit["records_by_kind"].items()), "Type", "Nombre")

    lines += ["", "## 4. Catégories de problèmes", ""]
    lines += section_table(sorted(audit["issue_categories"].items()), "Catégorie", "Nombre")

    lines += ["", "## 5. Erreurs bloquantes", ""]
    if errors:
        for issue in errors[:max_items]:
            record = f" [{issue['record_id']}]" if issue.get("record_id") else ""
            lines.append(f"- **{issue['category']}** — `{issue['file']}`{record} : {issue['message']} → {issue['suggested_action']}")
        if len(errors) > max_items:
            lines.append(f"- … {len(errors) - max_items} erreur(s) supplémentaire(s) dans `audit_repo.json`.")
    else:
        lines.append("Aucune.")

    lines += ["", "## 6. Blocs YAML non classés", ""]
    if unknowns:
        for issue in unknowns[:max_items]:
            record = f" [{issue['record_id']}]" if issue.get("record_id") else ""
            lines.append(f"- `{issue['file']}`{record} : {issue['message']}")
        if len(unknowns) > max_items:
            lines.append(f"- … {len(unknowns) - max_items} bloc(s) supplémentaire(s) dans `audit_repo.json`.")
    else:
        lines.append("Aucun.")

    lines += ["", "## 7. Registre des sources", ""]
    missing = audit["source_registry"]["used_but_missing_from_registre_json"]
    unused = audit["source_registry"]["declared_but_unused"]
    if missing:
        lines.append("Sources utilisées mais absentes de `data/registre.json` :")
        lines.extend(f"- {source_id}" for source_id in missing)
    else:
        lines.append("Aucune source utilisée n’est absente de `data/registre.json`.")
    lines.append("")
    if unused:
        lines.append("Sources déclarées mais non utilisées :")
        for source in unused:
            lines.append(f"- {source.get('source_label', source.get('source_id'))} — {source.get('statut', '')}")
    else:
        lines.append("Aucune source déclarée n’est inutilisée.")
    lines.append("")
    if weak_labels:
        lines.append("Libellés faibles :")
        for source in weak_labels:
            lines.append(f"- {source.get('source_id')} : {source.get('source_label')}")
    else:
        lines.append("Aucun libellé faible.")

    lines += ["", "## 8. Migration v2", ""]
    migration = audit["v2_migration"]
    lines.extend([
        f"- Atomes : {migration['atoms_total']}",
        f"- Atomes v2 complets : {migration['atoms_v2_complete']}",
        f"- Atomes v2 incomplets : {migration['atoms_v2_incomplete']}",
        f"- Avertissements de champs v2 manquants : {migration['v2_missing_field_warnings']}",
        "",
        "Cette dette ne doit pas être corrigée mécaniquement sans stratégie d’enrichissement documentaire. Elle relève d’une migration progressive des sources déjà atomisées.",
    ])

    lines += ["", "## 9. Fichiers les plus chargés en problèmes", ""]
    lines += section_table(audit["top_files_by_issue_count"][:20], "Fichier", "Problèmes")

    lines += ["", "## 10. Commandes utiles", "", "```bash", "python3 tools/build_registers.py", "python3 tools/audit_repo.py", "python3 tools/audit_repo.py --fail-on-error", "```", ""]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the Joy Division documentary repository.")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit with code 1 if blocking errors are found.")
    parser.add_argument("--max-items", type=int, default=40, help="Maximum detailed issues shown in the Markdown report per section.")
    args = parser.parse_args()

    records, diagnostics = br.parse_repository()
    audit = build_audit(records, diagnostics)

    write_json(AUDIT_JSON, audit)
    write_markdown(AUDIT_MD, audit, max_items=args.max_items)
    write_csv(AUDIT_CSV, audit["issues"])

    summary = audit["summary"]
    print("Repo audit summary")
    print("------------------")
    print(f"records     : {summary.get('records_total', 0)}")
    print(f"errors      : {summary.get('errors', 0)}")
    print(f"warnings    : {summary.get('warnings', 0)}")
    print(f"unknown     : {audit['records_by_kind'].get('unknown', 0)}")
    print(f"audit md    : {br.rel(AUDIT_MD)}")
    print(f"audit json  : {br.rel(AUDIT_JSON)}")
    print(f"audit csv   : {br.rel(AUDIT_CSV)}")

    if args.fail_on_error and audit["blocking_errors"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
