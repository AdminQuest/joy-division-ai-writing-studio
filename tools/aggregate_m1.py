#!/usr/bin/env python3
"""Minimal M1 aggregation layer.

This script reads existing M1 reports and writes a consolidated status under
reports/m1/. It does not run controls, rebuild exports, fix data, or inspect the
documentary corpus directly.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports" / "m1"
DEFAULT_OUTPUT = REPORT_DIR / "status_m1.md"


@dataclass(frozen=True)
class KnownControl:
    name: str
    report_path: Path
    implemented: bool = True


@dataclass
class ControlStatus:
    name: str
    report: Path
    state: str
    symbol: str
    observations: list[str] = field(default_factory=list)
    summary: dict[str, str] = field(default_factory=dict)


KNOWN_CONTROLS = [
    KnownControl("DM -> atomes", REPORT_DIR / "dm_atoms_traceability.md"),
    KnownControl("DM -> registres", REPORT_DIR / "dm_registers_consistency.md"),
]

KNOWN_AUDITS = [
    (
        "Atomes S35 source vide",
        REPO_ROOT / "docs" / "m1-audit-atomes-source-vide-dm.md",
        "Validé par le rapport DM -> atomes actuel sans écart détecté.",
    ),
    (
        "SONG-S45-SHADOWPLAY-RCA",
        REPO_ROOT / "docs" / "m1-audit-song-s45-shadowplay-rca.md",
        "Validé par le rapport DM -> registres actuel sans identifiant introuvable.",
    ),
]

DOCUMENTARY_DEBT = [
    "DM -> sources",
    "DM -> exports",
    "DM -> génération",
    "DM -> obsolescence",
    "DM -> statut documentaire",
]


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
        raise ValueError("--output doit pointer sous reports/m1/.") from exc
    return resolved_output


def parse_summary_table(markdown: str) -> dict[str, str]:
    summary: dict[str, str] = {}
    in_summary = False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped in {"### Résumé global", "## Résumé global"}:
            in_summary = True
            continue
        if in_summary and stripped.startswith("#") and "Résumé global" not in stripped:
            break
        if not in_summary or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 2 or cells[0] in {"Indicateur", "------------"}:
            continue
        summary[cells[0]] = cells[1]
    return summary


def int_value(summary: dict[str, str], label: str) -> int:
    raw_value = summary.get(label, "0")
    match = re.search(r"-?\d+", raw_value)
    return int(match.group(0)) if match else 0


def status_for_atoms(report_path: Path, summary: dict[str, str]) -> ControlStatus:
    ecarts = int_value(summary, "Écarts détectés")
    non_tracables = int_value(summary, "Documents non traçables")
    partiels = int_value(summary, "Documents partiellement traçables")
    visibles = int_value(summary, "Atomes visibles")
    retrouves = int_value(summary, "Atomes retrouvés")

    observations = [
        f"{retrouves}/{visibles} atomes visibles retrouvés.",
        f"{ecarts} écart détecté dans le rapport agrégé.",
    ]
    if ecarts == 0 and non_tracables == 0 and partiels == 0:
        return ControlStatus("DM -> atomes", report_path, "conforme", "✓", observations, summary)
    if non_tracables > 0:
        return ControlStatus("DM -> atomes", report_path, "non conforme", "✗", observations, summary)
    return ControlStatus("DM -> atomes", report_path, "conforme avec réserve", "⚠", observations, summary)


def status_for_registers(report_path: Path, summary: dict[str, str]) -> ControlStatus:
    missing = int_value(summary, "Identifiants introuvables")
    absent = int_value(summary, "Registres absents")
    counters = int_value(summary, "Compteurs incohérents")
    manifest = int_value(summary, "Manifestes incohérents")
    label_drift = int_value(summary, "Libellés divergents")
    non_covered = int_value(summary, "Familles non couvertes")

    observations = [
        f"{missing} identifiant introuvable.",
        f"{label_drift} libellé divergent.",
        f"{non_covered} famille non couverte.",
    ]
    if missing or absent or counters or manifest:
        return ControlStatus("DM -> registres", report_path, "non conforme", "✗", observations, summary)
    if label_drift or non_covered:
        return ControlStatus("DM -> registres", report_path, "conforme avec réserve", "⚠", observations, summary)
    return ControlStatus("DM -> registres", report_path, "conforme", "✓", observations, summary)


def read_control_status(control: KnownControl) -> ControlStatus:
    if not control.report_path.exists():
        return ControlStatus(
            control.name,
            control.report_path,
            "non exécuté",
            "○",
            [f"Rapport absent : {rel(control.report_path)}."],
        )

    markdown = control.report_path.read_text(encoding="utf-8")
    summary = parse_summary_table(markdown)
    if control.name == "DM -> atomes":
        return status_for_atoms(control.report_path, summary)
    if control.name == "DM -> registres":
        return status_for_registers(control.report_path, summary)
    return ControlStatus(control.name, control.report_path, "inconnu", "?", ["Contrôle non classé."], summary)


def render_report(statuses: list[ControlStatus]) -> str:
    generated_on = date.today().isoformat()
    global_state = "conforme"
    if any(status.state == "non conforme" for status in statuses):
        global_state = "non conforme"
    elif any(status.state in {"conforme avec réserve", "non exécuté", "inconnu"} for status in statuses):
        global_state = "conforme avec réserve"

    lines = [
        "# Status consolidé M1",
        "",
        f"Rapport genere par `python3 tools/aggregate_m1.py` le {generated_on}.",
        "",
        "L'agrégateur lit uniquement les rapports M1 existants. Il ne relance aucun contrôle, ne recalcule aucun diagnostic, ne corrige aucun écart et ne modifie aucun objet documentaire.",
        "",
        "## État général",
        "",
        f"**M1 STATUS** : {global_state}",
        "",
        f"**Date** : {generated_on}",
        "",
        "### Contrôles",
        "",
        "| Contrôle | Statut | Rapport | Observations |",
        "| --- | --- | --- | --- |",
    ]
    for status in statuses:
        observations = "<br>".join(status.observations)
        lines.append(f"| {status.symbol} {status.name} | {status.state} | `{rel(status.report)}` | {observations} |")

    lines.extend([
        "",
        "### Audits validés",
        "",
        "| Audit | Statut | Observation |",
        "| --- | --- | --- |",
    ])
    for label, path, observation in KNOWN_AUDITS:
        symbol = "✓" if path.exists() else "○"
        state = "documenté" if path.exists() else "non documenté"
        lines.append(f"| {symbol} {label} | {state} | {observation if path.exists() else f'Fichier absent : `{rel(path)}`.'} |")

    lines.extend([
        "",
        "## Dette documentaire connue",
        "",
        "| Chantier | Statut |",
        "| --- | --- |",
    ])
    for item in DOCUMENTARY_DEBT:
        lines.append(f"| {item} | non implémenté |")

    lines.extend([
        "",
        "## Maturité",
        "",
        "| Jalon | Statut |",
        "| --- | --- |",
        "| M0 | ✓ terminé |",
        "| M1.1 | ✓ contrôles fondamentaux |",
        "| M1.2 | ✓ agrégation minimale |",
        "| M1.3 | non démarré |",
        "| M2 | non ouvert |",
        "",
        "## Limites",
        "",
        "- Ce status consolide les rapports déjà produits ; il ne prouve pas que les rapports sont fraîchement régénérés.",
        "- Les divergences lexicales et les familles hors MVP restent des réserves documentaires, pas des corrections automatiques.",
        "- L'agrégateur ne remplace pas les audits ciblés lorsque le sens documentaire d'un écart est ambigu.",
        "- Ce fichier n'est pas un tableau de bord M1 et ne définit aucun seuil CI.",
        "",
        "## Conclusion",
        "",
        "L'agrégation minimale M1 est disponible pour consolider les contrôles existants. Elle peut préparer un futur tableau de bord ou une future intégration CI, mais elle ne les implémente pas.",
        "",
    ])
    return "\n".join(lines)


def run(output: Path) -> int:
    statuses = [read_control_status(control) for control in KNOWN_CONTROLS]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(statuses), encoding="utf-8")
    print(f"Rapport: {rel(output)}")
    for status in statuses:
        print(f"{status.symbol} {status.name}: {status.state}")
    return 1 if any(status.state == "non conforme" for status in statuses) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agrégation minimale des rapports M1 existants.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT.relative_to(REPO_ROOT)),
        help="Chemin du status Markdown à écrire (défaut: reports/m1/status_m1.md).",
    )
    args = parser.parse_args(argv)
    try:
        output = resolve_output_path(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
