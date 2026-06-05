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
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "reports" / "m1"
DEFAULT_OUTPUT = REPORT_DIR / "status_m1.md"
FAILURE_STATES = {"non conforme", "rapport illisible", "non exécuté"}


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


@dataclass(frozen=True)
class KnownAudit:
    label: str
    path: Path
    control_name: str
    validation: str


KNOWN_CONTROLS = [
    KnownControl("DM -> atomes", REPORT_DIR / "dm_atoms_traceability.md"),
    KnownControl("DM -> registres", REPORT_DIR / "dm_registers_consistency.md"),
]

REQUIRED_ATOMS_INDICATORS = [
    "Documents declares dans le manifeste",
    "Documents maîtres sur disque",
    "Documents traçables",
    "Documents partiellement traçables",
    "Documents non traçables",
    "Atomes visibles",
    "Atomes retrouvés",
    "Écarts détectés",
]

REQUIRED_REGISTERS_INDICATORS = [
    "Documents declares dans le manifeste",
    "Documents maîtres sur disque",
    "Documents cohérents",
    "Documents partiellement cohérents",
    "Documents non cohérents",
    "Écarts détectés",
    "Identifiants introuvables",
    "Registres absents",
    "Compteurs incohérents",
    "Familles non couvertes",
    "Relations non résolues",
    "Libellés divergents",
    "Manifestes incohérents",
]

KNOWN_AUDITS = [
    KnownAudit(
        label="Atomes S35 source vide",
        path=REPO_ROOT / "docs" / "m1-audit-atomes-source-vide-dm.md",
        control_name="DM -> atomes",
        validation="atoms_conforme",
    ),
    KnownAudit(
        label="SONG-S45-SHADOWPLAY-RCA",
        path=REPO_ROOT / "docs" / "m1-audit-song-s45-shadowplay-rca.md",
        control_name="DM -> registres",
        validation="registers_no_missing_ids",
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


def int_value(summary: dict[str, str], label: str) -> int | None:
    raw_value = summary.get(label)
    if raw_value is None:
        return None
    match = re.search(r"-?\d+", raw_value)
    if not match:
        return None
    return int(match.group(0))


def invalid_summary_status(control_name: str, report_path: Path, missing: list[str], invalid: list[str]) -> ControlStatus:
    observations = [
        "Statut impossible à consolider : indicateurs requis absents ou non parsables.",
    ]
    if missing:
        observations.append("Indicateurs absents : " + ", ".join(f"`{label}`" for label in missing) + ".")
    if invalid:
        observations.append("Indicateurs non parsables : " + ", ".join(f"`{label}`" for label in invalid) + ".")
    return ControlStatus(control_name, report_path, "rapport illisible", "✗", observations)


def validate_required_indicators(
    control_name: str,
    report_path: Path,
    summary: dict[str, str],
    required: list[str],
) -> ControlStatus | None:
    missing = [label for label in required if label not in summary]
    invalid = [label for label in required if label in summary and int_value(summary, label) is None]
    if missing or invalid:
        return invalid_summary_status(control_name, report_path, missing, invalid)
    return None


def status_for_atoms(report_path: Path, summary: dict[str, str]) -> ControlStatus:
    invalid_status = validate_required_indicators("DM -> atomes", report_path, summary, REQUIRED_ATOMS_INDICATORS)
    if invalid_status is not None:
        return invalid_status

    ecarts = int_value(summary, "Écarts détectés")
    non_tracables = int_value(summary, "Documents non traçables")
    partiels = int_value(summary, "Documents partiellement traçables")
    visibles = int_value(summary, "Atomes visibles")
    retrouves = int_value(summary, "Atomes retrouvés")
    assert ecarts is not None
    assert non_tracables is not None
    assert partiels is not None
    assert visibles is not None
    assert retrouves is not None

    observations = [
        f"{retrouves}/{visibles} atomes visibles retrouvés.",
        f"{ecarts} écart détecté dans le rapport agrégé.",
    ]
    if ecarts == 0 and non_tracables == 0 and partiels == 0 and visibles == retrouves:
        return ControlStatus("DM -> atomes", report_path, "conforme", "✓", observations, summary)
    return ControlStatus(
        "DM -> atomes",
        report_path,
        "non conforme",
        "✗",
        observations + [
            "Le rapport source signale un écart de traçabilité ; le statut ne peut pas être consolidé comme conforme.",
        ],
        summary,
    )


def status_for_registers(report_path: Path, summary: dict[str, str]) -> ControlStatus:
    invalid_status = validate_required_indicators(
        "DM -> registres",
        report_path,
        summary,
        REQUIRED_REGISTERS_INDICATORS,
    )
    if invalid_status is not None:
        return invalid_status

    missing = int_value(summary, "Identifiants introuvables")
    absent = int_value(summary, "Registres absents")
    counters = int_value(summary, "Compteurs incohérents")
    non_coherents = int_value(summary, "Documents non cohérents")
    ecarts = int_value(summary, "Écarts détectés")
    manifest = int_value(summary, "Manifestes incohérents")
    relations = int_value(summary, "Relations non résolues")
    label_drift = int_value(summary, "Libellés divergents")
    non_covered = int_value(summary, "Familles non couvertes")
    assert missing is not None
    assert absent is not None
    assert counters is not None
    assert non_coherents is not None
    assert ecarts is not None
    assert manifest is not None
    assert relations is not None
    assert label_drift is not None
    assert non_covered is not None

    observations = [
        f"{ecarts} écart(s) détecté(s).",
        f"{non_coherents} document(s) non cohérent(s).",
        f"{missing} identifiant introuvable.",
        f"{label_drift} libellé divergent.",
        f"{non_covered} famille non couverte.",
    ]
    blocking_values = {
        "Documents non cohérents": non_coherents,
        "Identifiants introuvables": missing,
        "Registres absents": absent,
        "Compteurs incohérents": counters,
        "Manifestes incohérents": manifest,
        "Relations non résolues": relations,
    }
    reserve_values = {
        "Libellés divergents": label_drift,
        "Familles non couvertes": non_covered,
    }
    blocking = {
        label: value
        for label, value in blocking_values.items()
        if value > 0
    }
    blocking_total = sum(blocking_values.values())
    reserve_total = sum(reserve_values.values())
    unexplained_gaps = ecarts - blocking_total - reserve_total
    if blocking:
        blocking_summary = ", ".join(f"{label}={value}" for label, value in blocking.items())
        return ControlStatus(
            "DM -> registres",
            report_path,
            "non conforme",
            "✗",
            observations + [
                f"Le rapport source signale des écarts bloquants : {blocking_summary}.",
            ],
            summary,
        )
    if unexplained_gaps > 0:
        return ControlStatus(
            "DM -> registres",
            report_path,
            "non conforme",
            "✗",
            observations + [
                f"{unexplained_gaps} écart(s) ne sont pas expliqués par les compteurs connus.",
            ],
            summary,
        )
    if reserve_total > 0:
        return ControlStatus(
            "DM -> registres",
            report_path,
            "conforme avec réserve",
            "⚠",
            observations + [
                "Les écarts restants relèvent des libellés divergents ou des familles hors MVP.",
            ],
            summary,
        )
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


def audit_validation_status(audit: KnownAudit, status_by_name: dict[str, ControlStatus]) -> tuple[str, str, str]:
    if not audit.path.exists():
        return "○", "non documenté", f"Fichier absent : `{rel(audit.path)}`."

    control_status = status_by_name.get(audit.control_name)
    if control_status is None:
        return (
            "⚠",
            "documenté — validation à confirmer",
            f"Audit présent ; contrôle associé `{audit.control_name}` absent du status consolidé.",
        )

    if audit.validation == "atoms_conforme":
        if control_status.state == "conforme":
            return "✓", "validé", "Validation confirmée par le contrôle `DM -> atomes` conforme."
        return (
            "⚠",
            "documenté — non validé par le contrôle associé",
            f"Audit présent ; contrôle `DM -> atomes` actuellement `{control_status.state}`.",
        )

    if audit.validation == "registers_no_missing_ids":
        missing = int_value(control_status.summary, "Identifiants introuvables")
        if control_status.state in {"conforme", "conforme avec réserve"} and missing == 0:
            state = "validé avec réserve" if control_status.state == "conforme avec réserve" else "validé"
            return (
                "✓",
                state,
                "Validation confirmée par `Identifiants introuvables=0` dans le contrôle `DM -> registres`.",
            )
        return (
            "⚠",
            "documenté — non validé par le contrôle associé",
            f"Audit présent ; contrôle `DM -> registres` actuellement `{control_status.state}`.",
        )

    return (
        "⚠",
        "documenté — validation à confirmer",
        f"Audit présent ; règle de validation `{audit.validation}` non reconnue.",
    )


def render_report(statuses: list[ControlStatus]) -> str:
    status_by_name = {status.name: status for status in statuses}
    global_state = "conforme"
    if any(status.state in FAILURE_STATES for status in statuses):
        global_state = "non conforme"
    elif any(status.state in {"conforme avec réserve", "non exécuté", "inconnu"} for status in statuses):
        global_state = "conforme avec réserve"

    lines = [
        "# Status consolidé M1",
        "",
        "Rapport genere par `python3 tools/aggregate_m1.py` à partir des rapports M1 versionnés.",
        "",
        "L'agrégateur lit uniquement les rapports M1 existants. Il ne relance aucun contrôle, ne recalcule aucun diagnostic, ne corrige aucun écart et ne modifie aucun objet documentaire.",
        "",
        "## État général",
        "",
        f"**M1 STATUS** : {global_state}",
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
        "### Audits M1",
        "",
        "| Audit | Contrôle associé | Statut | Observation |",
        "| --- | --- | --- | --- |",
    ])
    for audit in KNOWN_AUDITS:
        symbol, state, observation = audit_validation_status(audit, status_by_name)
        lines.append(f"| {symbol} {audit.label} | {audit.control_name} | {state} | {observation} |")

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
    return 1 if any(status.state in FAILURE_STATES for status in statuses) else 0


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
