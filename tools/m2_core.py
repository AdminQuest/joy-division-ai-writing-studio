"""Noyau commun limite pour les prototypes M2.

Ce module porte uniquement les invariants observes dans les prototypes PERSON et
ORG. La logique documentaire propre aux familles reste dans leurs adaptateurs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Pattern, Sequence


NEAR_MATCH_RATIO = 0.88


@dataclass
class CheckResult:
    candidate: dict
    blockers: list[str] = field(default_factory=list)
    reserves: list[str] = field(default_factory=list)
    information: list[str] = field(default_factory=list)

    @property
    def decision(self) -> str:
        if self.blockers:
            return "non pre-validee"
        if self.reserves:
            return "pre-validee avec reserve"
        return "pre-validee"

    def finalize(self) -> None:
        self.blockers = unique_preserving_order(self.blockers)
        self.reserves = unique_preserving_order(self.reserves)
        self.information = unique_preserving_order(self.information)


@dataclass(frozen=True)
class PRSummary:
    subject: str
    scope: list[str]
    validations: list[str]
    blockers: list[str]
    reserves: list[str]
    information: list[str]
    human_arbitrations: list[str]
    documentary_impact: list[str]
    verification_commands: list[str]


@dataclass(frozen=True)
class BatchItemResult:
    index: int
    family: str
    label: str
    result: CheckResult
    pr_summary_path: str | None = None

    @property
    def decision(self) -> str:
        return self.result.decision


@dataclass(frozen=True)
class BatchResult:
    campaign: str
    items: list[BatchItemResult]

    @property
    def object_count(self) -> int:
        return len(self.items)

    @property
    def prevalidated_count(self) -> int:
        return sum(1 for item in self.items if item.decision == "pre-validee")

    @property
    def prevalidated_with_reserve_count(self) -> int:
        return sum(1 for item in self.items if item.decision == "pre-validee avec reserve")

    @property
    def refused_count(self) -> int:
        return sum(1 for item in self.items if item.decision == "non pre-validee")

    @property
    def reserve_count(self) -> int:
        return sum(len(item.result.reserves) for item in self.items)

    @property
    def blocker_count(self) -> int:
        return sum(len(item.result.blockers) for item in self.items)


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = value.encode("ascii", "ignore").decode().lower()
    value = re.sub(r"[^a-z0-9 ]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact_normalized_text(value: str) -> str:
    return normalize_text(value).replace(" ", "")


def split_csv(values: Sequence[str] | None) -> list[str]:
    if not values:
        return []
    items: list[str] = []
    for raw in values:
        for part in raw.split(","):
            item = part.strip()
            if item:
                items.append(item)
    return items


def unique_preserving_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def format_values(values: Sequence[str]) -> str:
    return ", ".join(values)


def is_near_text_match(left: str, right: str) -> bool:
    left_norm = compact_normalized_text(left)
    right_norm = compact_normalized_text(right)
    if not left_norm or not right_norm or left_norm == right_norm:
        return False
    if min(len(left_norm), len(right_norm)) < 6:
        return False
    return SequenceMatcher(None, left_norm, right_norm).ratio() >= NEAR_MATCH_RATIO


def load_source_ids(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return set()
    return {str(item.get("id")) for item in payload if isinstance(item, dict) and item.get("id")}


def add_source_diagnostics(
    result: CheckResult,
    *,
    sources: Sequence[str],
    canonical_sources: set[str],
    format_re: Pattern[str] | None = None,
) -> None:
    for source in sources:
        if format_re is not None and not format_re.match(source):
            result.blockers.append(f"source invalide: {source}")
        elif source not in canonical_sources:
            result.blockers.append(f"source inconnue: {source}")
    if not sources:
        result.blockers.append("source absente")


def render_list(items: Sequence[str]) -> list[str]:
    if not items:
        return ["- aucun"]
    return [f"- {item}" for item in items]


def render_result(
    result: CheckResult,
    *,
    identifier: str,
    candidate_language: str,
    rendered_candidate: str,
) -> str:
    lines = [
        f"Decision : {result.decision}",
        f"Identifiant propose : {identifier}",
        "Bloquants :",
        *render_list(result.blockers),
        "Reserves :",
        *render_list(result.reserves),
        "Informations :",
        *render_list(result.information),
        "Entree candidate :",
        f"```{candidate_language}",
        rendered_candidate,
        "```",
    ]
    return "\n".join(lines) + "\n"


def build_pr_summary(
    result: CheckResult,
    *,
    subject: str,
    scope: Sequence[str],
    validations: Sequence[str],
    human_arbitrations: Sequence[str],
    documentary_impact: Sequence[str],
    verification_commands: Sequence[str],
) -> PRSummary:
    return PRSummary(
        subject=subject,
        scope=unique_preserving_order(item.strip() for item in scope if item.strip()),
        validations=unique_preserving_order(item.strip() for item in validations if item.strip()),
        blockers=list(result.blockers),
        reserves=list(result.reserves),
        information=list(result.information),
        human_arbitrations=unique_preserving_order(item.strip() for item in human_arbitrations if item.strip()),
        documentary_impact=unique_preserving_order(item.strip() for item in documentary_impact if item.strip()),
        verification_commands=unique_preserving_order(item.strip() for item in verification_commands if item.strip()),
    )


def render_pr_summary(summary: PRSummary) -> str:
    lines = [
        "# Resume de PR M2",
        "",
        "## Objet",
        "",
        summary.subject,
        "",
        "## Perimetre",
        "",
        *render_list(summary.scope),
        "",
        "## Validations executees",
        "",
        *render_list(summary.validations),
        "",
        "## Bloquants",
        "",
        *render_list(summary.blockers),
        "",
        "## Reserves",
        "",
        *render_list(summary.reserves),
        "",
        "## Informations",
        "",
        *render_list(summary.information),
        "",
        "## Arbitrages humains",
        "",
        *render_list(summary.human_arbitrations),
        "",
        "## Impact documentaire",
        "",
        *render_list(summary.documentary_impact),
        "",
        "## Commandes de verification",
        "",
        *render_list([f"`{command}`" for command in summary.verification_commands]),
        "",
    ]
    return "\n".join(lines)


def write_pr_summary(summary: PRSummary, *, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(render_pr_summary(summary), encoding="utf-8")
    return path


def build_batch_result(*, campaign: str, items: Sequence[BatchItemResult]) -> BatchResult:
    return BatchResult(
        campaign=campaign.strip() or "campagne-m2",
        items=list(items),
    )


def render_batch_object_line(item: BatchItemResult) -> str:
    parts = [
        f"{item.index}. {item.family} - {item.label}",
        f"decision: {item.decision}",
        f"reserves: {len(item.result.reserves)}",
        f"bloquants: {len(item.result.blockers)}",
    ]
    if item.pr_summary_path:
        parts.append(f"resume PR: `{item.pr_summary_path}`")
    return "- " + " | ".join(parts)


def collect_batch_reserves(batch: BatchResult) -> list[str]:
    lines: list[str] = []
    for item in batch.items:
        for reserve in item.result.reserves:
            lines.append(f"{item.family} - {item.label}: {reserve}")
    return lines


def collect_batch_blockers(batch: BatchResult) -> list[str]:
    lines: list[str] = []
    for item in batch.items:
        for blocker in item.result.blockers:
            lines.append(f"{item.family} - {item.label}: {blocker}")
    return lines


def build_batch_human_arbitrations(batch: BatchResult) -> list[str]:
    if not batch.items:
        return ["Aucun objet a arbitrer dans cette campagne."]
    arbitrations: list[str] = []
    if batch.refused_count:
        arbitrations.append(f"Corriger les bloquants de {batch.refused_count} objet(s) non pre-valide(s).")
    if batch.reserve_count:
        arbitrations.append(f"Arbitrer {batch.reserve_count} reserve(s) avant integration documentaire.")
    if batch.prevalidated_count or batch.prevalidated_with_reserve_count:
        arbitrations.append("Valider humainement les objets pre-valides avant integration.")
    return arbitrations


def render_batch_summary(batch: BatchResult) -> str:
    lines = [
        "# Rapport de campagne M2",
        "",
        "## Synthese",
        "",
        f"Campagne : {batch.campaign}",
        "",
        "Ce rapport consolide les diagnostics M2 d'une campagne documentaire.",
        "Il ne modifie aucun registre et ne remplace pas la revue humaine.",
        "",
        "## Statistiques",
        "",
        f"- objets: {batch.object_count}",
        f"- pre-validations: {batch.prevalidated_count}",
        f"- pre-validations avec reserve: {batch.prevalidated_with_reserve_count}",
        f"- refus: {batch.refused_count}",
        f"- reserves: {batch.reserve_count}",
        f"- bloquants: {batch.blocker_count}",
        "",
        "## Liste des objets",
        "",
        *([render_batch_object_line(item) for item in batch.items] or ["- aucun"]),
        "",
        "## Reserves",
        "",
        *render_list(collect_batch_reserves(batch)),
        "",
        "## Bloquants",
        "",
        *render_list(collect_batch_blockers(batch)),
        "",
        "## Arbitrages humains",
        "",
        *render_list(build_batch_human_arbitrations(batch)),
        "",
    ]
    return "\n".join(lines)


def write_batch_summary(batch: BatchResult, *, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(render_batch_summary(batch), encoding="utf-8")
    return path


def exit_code(result: CheckResult) -> int:
    return 1 if result.blockers else 0
