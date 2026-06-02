#!/usr/bin/env python3
"""Generate the C1 edge graph.

C1 lot 2A generates all stable and currently validatable same_as edges from the
canonical identifier index. C1 lot 2B-1 adds deterministic quote -> person
attributed_to edges. C1 lot 2B-2 adds deterministic quote -> source documented_by
edges. C1 lot 3A adds a reduced set of deterministic atom -> source
documented_by edges when the atom brings new graph connectivity. C1 lot 4A
adds deterministic atom -> concept indexed_by edges for atoms already present in
the graph. C1 lot 4B adds deterministic atom -> motif indexed_by edges for
atoms already present in the graph. C1 lot 4C adds deterministic atom -> myth
indexed_by edges for atoms already present in the graph.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "exports" / "generated" / "index_by_id.json"
ATTRIBUTION_PATH = ROOT / "exports" / "generated" / "attribution_edges.json"
ATOMS_PATH = ROOT / "exports" / "generated" / "atoms.json"
QUOTES_PATH = ROOT / "exports" / "generated" / "quotes.json"
EDGES_PATH = ROOT / "exports" / "generated" / "edges.json"
CHAPTERS_PATH = ROOT / "chapters"
ATOM_REF_PATTERN = re.compile(r"(?<![A-Z0-9_-])S\d+(?:-A\d+|-\d{3}|-PART-[A-Z0-9_-]+)(?![A-Z0-9_-])")

ALLOWED_SAME_AS = {
    ("legacy_person", "person"),
    ("legacy_chronology", "event"),
    ("legacy_chronology", "concert"),
    # Kept after review arbitration: JD-CONCERT-* is a legacy concert endpoint,
    # while CONCERT-* is the canonical concert endpoint.
    ("legacy_concert", "concert"),
}

CONCEPTUAL_SIGNAL_FIELDS = {
    "concepts",
    "concepts_derives",
    "motifs",
    "mythes",
    "myths",
    "related_concepts",
    "related_motifs",
    "related_myths",
}

CITATION_SIGNAL_FIELDS = {
    "citation",
    "citation_directe",
    "citation_courte",
    "citation_originale",
    "passage",
    "passage_atomise",
    "texte",
    "liens_citations",
    "related_quotes",
    "citation_ids",
    "quotes",
}

FORMAL_SIGNAL_FIELDS = {
    "relations",
    "related_atoms",
    "atomes_lies",
    "liens_interchapitres",
    "related_sources",
}

ENTITY_SIGNAL_FIELDS = {
    "related_people",
    "associated_people",
    "personnes",
    "personne",
    "locuteurs",
    "related_places",
    "lieux",
    "lieu",
    "location",
    "related_events",
    "evenements",
    "events",
    "related_songs",
    "song_id",
    "canonical_song",
    "related_organizations",
    "related_organisations",
    "organisations",
    "orgs",
    "studio",
    "label",
}

ATOM_QUOTE_REF_FIELDS = {
    "related_quotes",
    "liens_citations",
    "citation_ids",
    "quotes",
}

CONCEPT_ATOM_FIELDS = {
    "related_atoms",
    "atoms",
    "atomes",
    "atomes_lies",
    "atomes_associes",
}

ATOM_CONCEPT_REF_FIELDS = {
    "concepts",
    "concepts_derives",
    "related_concepts",
}

MOTIF_ATOM_FIELDS = {
    "related_atoms",
    "atoms",
    "atomes",
    "atomes_lies",
    "atomes_associes",
}

ATOM_MOTIF_REF_FIELDS = {
    "motifs",
    "related_motifs",
    "motifs_associes",
}

MYTH_ATOM_FIELDS = {
    "related_atoms",
    "atoms",
    "atomes",
    "atomes_lies",
    "atomes_associes",
}

ATOM_MYTH_REF_FIELDS = {
    "mythes",
    "myths",
    "related_myths",
    "mythes_associes",
}


def load_index() -> dict[str, Any]:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def load_attribution_edges() -> dict[str, Any]:
    return json.loads(ATTRIBUTION_PATH.read_text(encoding="utf-8"))


def load_atoms() -> list[dict[str, Any]]:
    return json.loads(ATOMS_PATH.read_text(encoding="utf-8"))


def load_quotes() -> list[dict[str, Any]]:
    return json.loads(QUOTES_PATH.read_text(encoding="utf-8"))


def graph_kind(identifier: str, index: dict[str, Any]) -> Optional[str]:
    record = index.get(identifier, {})
    raw_kind = record.get("kind") if isinstance(record, dict) else None
    if identifier.startswith("PERS-"):
        return "legacy_person"
    if identifier.startswith("JD-CONCERT-"):
        return "legacy_concert"
    if raw_kind == "chronology":
        if identifier.startswith("EVENT-"):
            return "event"
        if identifier.startswith(("CHR-", "CHRON-")):
            return "legacy_chronology"
    return raw_kind if isinstance(raw_kind, str) else None


def non_empty(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().lower() not in {"aucune", "none", "null"}
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def has_any_field(data: dict[str, Any], fields: set[str]) -> bool:
    return any(non_empty(data.get(field)) for field in fields)


def collect_atom_refs(value: Any, atom_ids: set[str]) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, str):
        if value in atom_ids:
            refs.add(value)
        for match in ATOM_REF_PATTERN.finditer(value):
            ref = match.group(0)
            if ref in atom_ids:
                refs.add(ref)
    elif isinstance(value, list):
        for item in value:
            refs.update(collect_atom_refs(item, atom_ids))
    elif isinstance(value, dict):
        for item in value.values():
            refs.update(collect_atom_refs(item, atom_ids))
    return refs


def collect_known_refs(value: Any, known_ids: set[str]) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, str):
        if value in known_ids:
            refs.add(value)
    elif isinstance(value, list):
        for item in value:
            refs.update(collect_known_refs(item, known_ids))
    elif isinstance(value, dict):
        for item in value.values():
            refs.update(collect_known_refs(item, known_ids))
    return refs


def indexed_atom_ids(index: dict[str, Any]) -> set[str]:
    return {
        identifier
        for identifier, record in index.items()
        if isinstance(identifier, str) and graph_kind(identifier, index) == "atom"
    }


def text_contains_identifier(text: str, identifier: str) -> bool:
    start = 0
    while True:
        index = text.find(identifier, start)
        if index == -1:
            return False
        before = text[index - 1] if index > 0 else ""
        after_index = index + len(identifier)
        after = text[after_index] if after_index < len(text) else ""
        if before not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" and after not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-":
            return True
        start = index + len(identifier)


def document_master_atom_ids(atom_ids: set[str]) -> set[str]:
    refs: set[str] = set()
    for path in sorted(CHAPTERS_PATH.glob("*/document_maitre.md")):
        text = path.read_text(encoding="utf-8")
        for atom_id in atom_ids:
            if text_contains_identifier(text, atom_id):
                refs.add(atom_id)
    return refs


def quote_refs_by_atom(quotes: list[dict[str, Any]], atom_ids: set[str]) -> dict[str, set[str]]:
    refs: dict[str, set[str]] = {}
    for quote in quotes:
        quote_id = quote.get("id")
        if not isinstance(quote_id, str):
            continue
        data = quote.get("data", {})
        if not isinstance(data, dict):
            continue
        for atom_id in collect_atom_refs(data, atom_ids):
            refs.setdefault(atom_id, set()).add(quote_id)
    return refs


def atom_declared_quote_refs_by_atom(atoms: list[dict[str, Any]], quote_ids: set[str]) -> dict[str, set[str]]:
    refs: dict[str, set[str]] = {}
    for atom in atoms:
        atom_id = atom.get("id")
        if not isinstance(atom_id, str):
            continue
        data = atom.get("data", {})
        if not isinstance(data, dict):
            continue
        for field in ATOM_QUOTE_REF_FIELDS:
            for quote_id in collect_known_refs(data.get(field), quote_ids):
                refs.setdefault(atom_id, set()).add(quote_id)
    return refs


def relational_score(atom: dict[str, Any], master_atom_ids: set[str], cited_atom_ids: set[str]) -> int:
    atom_id = atom.get("id")
    data = atom.get("data", {})
    if not isinstance(atom_id, str) or not isinstance(data, dict):
        return 0

    signals = [
        atom_id in master_atom_ids,
        has_any_field(data, CONCEPTUAL_SIGNAL_FIELDS),
        atom_id in cited_atom_ids or has_any_field(data, CITATION_SIGNAL_FIELDS),
        has_any_field(data, FORMAL_SIGNAL_FIELDS),
        has_any_field(data, ENTITY_SIGNAL_FIELDS),
    ]
    return sum(1 for signal in signals if signal)


def iter_same_as_edges(index: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    for declared_target_id, record in index.items():
        if not isinstance(record, dict):
            continue
        data = record.get("data", {})
        if not isinstance(data, dict):
            continue

        aliases = data.get("same_as")
        if isinstance(aliases, str):
            aliases = [aliases]
        if not isinstance(aliases, list):
            continue

        target_kind = graph_kind(declared_target_id, index)
        for alias in aliases:
            if not isinstance(alias, str):
                exclusions["non_string_same_as"] += 1
                continue
            if alias not in index:
                exclusions["missing_endpoint"] += 1
                continue

            alias_kind = graph_kind(alias, index)
            if (alias_kind, target_kind) in ALLOWED_SAME_AS:
                source_kind, source_id = alias_kind, alias
                final_target_kind, final_target_id = target_kind, declared_target_id
            elif (target_kind, alias_kind) in ALLOWED_SAME_AS:
                source_kind, source_id = target_kind, declared_target_id
                final_target_kind, final_target_id = alias_kind, alias
            else:
                exclusions[f"unsupported_{target_kind}_to_{alias_kind}"] += 1
                continue

            signature = (source_id, "same_as", final_target_id)
            if signature in seen:
                exclusions["duplicate_signature"] += 1
                continue
            seen.add(signature)

            edges.append(
                {
                    "source_kind": source_kind,
                    "source_id": source_id,
                    "target_kind": final_target_kind,
                    "target_id": final_target_id,
                    "relation_type": "same_as",
                    "evidence_refs": [source_id],
                    "confidence": "high",
                    "derived_from": record.get("file") or "exports/generated/index_by_id.json",
                }
            )

    edges.sort(
        key=lambda edge: (
            edge["relation_type"],
            edge["source_kind"],
            edge["source_id"],
            edge["target_kind"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def iter_attributed_to_edges(index: dict[str, Any], attribution: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    rows = attribution.get("edges", [])
    if not isinstance(rows, list):
        exclusions["invalid_attribution_edges"] += 1
        return edges, exclusions

    for row in rows:
        if not isinstance(row, dict):
            exclusions["invalid_attribution_row"] += 1
            continue
        source_id = row.get("citation")

        links = row.get("liens") or []
        if not isinstance(links, list):
            exclusions["invalid_attribution_links"] += 1
            continue

        for link in links:
            if not isinstance(link, dict):
                exclusions["invalid_attribution_link"] += 1
                continue
            predicate = link.get("predicat")
            if predicate != "attribuee_a":
                exclusions[f"skipped_{predicate}"] += 1
                continue

            link_flags = link.get("flags") or []
            if not isinstance(link_flags, list):
                link_flags = []
            flags = sorted({flag for flag in link_flags if isinstance(flag, str)})
            if flags:
                exclusions[f"flagged_{'_'.join(flags)}"] += 1
                continue

            target_id = link.get("cible")
            if not isinstance(source_id, str) or source_id not in index:
                exclusions["missing_quote_endpoint"] += 1
                continue
            if not isinstance(target_id, str) or target_id not in index:
                exclusions["missing_person_endpoint"] += 1
                continue

            source_kind = graph_kind(source_id, index)
            target_kind = graph_kind(target_id, index)
            if source_kind != "quote":
                exclusions[f"unsupported_source_kind_{source_kind}"] += 1
                continue
            if target_kind != "person":
                exclusions[f"unsupported_target_kind_{target_kind}"] += 1
                continue

            signature = (source_id, "attributed_to", target_id)
            if signature in seen:
                exclusions["duplicate_signature"] += 1
                continue
            seen.add(signature)

            edges.append(
                {
                    "source_kind": "quote",
                    "source_id": source_id,
                    "target_kind": "person",
                    "target_id": target_id,
                    "relation_type": "attributed_to",
                    "evidence_refs": [source_id],
                    "confidence": "high",
                    "derived_from": "exports/generated/attribution_edges.json",
                }
            )

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def quote_source_id(quote_id: str, data: dict[str, Any]) -> Optional[str]:
    declared_source_id = data.get("source_id")
    if isinstance(declared_source_id, str):
        return declared_source_id

    match = re.search(r"S\d+", quote_id)
    return match.group(0) if match else None


def iter_quote_source_edges(index: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    for quote_id, record in index.items():
        if graph_kind(quote_id, index) != "quote":
            continue
        if not isinstance(record, dict):
            exclusions["invalid_quote_record"] += 1
            continue

        data = record.get("data", {})
        if not isinstance(data, dict):
            data = {}

        source_id = quote_source_id(quote_id, data)
        if not isinstance(source_id, str) or source_id not in index:
            exclusions["missing_source_endpoint"] += 1
            continue
        if graph_kind(source_id, index) != "source":
            exclusions[f"unsupported_source_kind_{graph_kind(source_id, index)}"] += 1
            continue

        signature = (quote_id, "documented_by", source_id)
        if signature in seen:
            exclusions["duplicate_signature"] += 1
            continue
        seen.add(signature)

        edges.append(
            {
                "source_kind": "quote",
                "source_id": quote_id,
                "target_kind": "source",
                "target_id": source_id,
                "relation_type": "documented_by",
                "evidence_refs": [quote_id],
                "confidence": "high",
                "derived_from": "exports/generated/index_by_id.json",
            }
        )

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def iter_atom_source_edges(
    index: dict[str, Any],
    atoms: list[dict[str, Any]],
    quotes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    atom_ids = indexed_atom_ids(index)
    master_atom_ids = document_master_atom_ids(atom_ids)
    quote_refs = quote_refs_by_atom(quotes, atom_ids)
    quote_ids = {quote.get("id") for quote in quotes if isinstance(quote.get("id"), str)}
    for atom_id, quote_ids_for_atom in atom_declared_quote_refs_by_atom(atoms, quote_ids).items():
        if atom_id in atom_ids:
            quote_refs.setdefault(atom_id, set()).update(quote_ids_for_atom)
    cited_atom_ids = set(quote_refs)
    quotes_by_id = {quote.get("id"): quote for quote in quotes if isinstance(quote.get("id"), str)}

    for atom in atoms:
        if not isinstance(atom, dict):
            exclusions["invalid_atom_record"] += 1
            continue
        atom_id = atom.get("id")
        if not isinstance(atom_id, str):
            exclusions["invalid_atom_id"] += 1
            continue

        data = atom.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_atom_data"] += 1
            continue

        source_id = data.get("source_id")
        if not isinstance(source_id, str) or source_id not in index:
            exclusions["missing_source_endpoint"] += 1
            continue
        if graph_kind(source_id, index) != "source":
            exclusions[f"unsupported_source_kind_{graph_kind(source_id, index)}"] += 1
            continue
        if graph_kind(atom_id, index) != "atom":
            exclusions[f"unsupported_atom_kind_{graph_kind(atom_id, index)}"] += 1
            continue

        score = relational_score(atom, master_atom_ids, cited_atom_ids)
        if score < 3:
            exclusions[f"score_{score}"] += 1
            continue

        already_documented_by_quote = False
        for quote_id in quote_refs.get(atom_id, set()):
            quote = quotes_by_id.get(quote_id, {})
            quote_data = quote.get("data", {}) if isinstance(quote, dict) else {}
            quote_source_id = quote_data.get("source_id") if isinstance(quote_data, dict) else None
            if quote_source_id == source_id and graph_kind(source_id, index) == "source":
                already_documented_by_quote = True
                break
        if already_documented_by_quote:
            exclusions["already_documented_by_quote_source"] += 1
            continue

        signature = (atom_id, "documented_by", source_id)
        if signature in seen:
            exclusions["duplicate_signature"] += 1
            continue
        seen.add(signature)

        edges.append(
            {
                "source_kind": "atom",
                "source_id": atom_id,
                "target_kind": "source",
                "target_id": source_id,
                "relation_type": "documented_by",
                "evidence_refs": [atom_id],
                "confidence": "high",
                "derived_from": "exports/generated/atoms.json",
            }
        )

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def graph_atom_ids(edges: list[dict[str, Any]]) -> set[str]:
    atom_ids: set[str] = set()
    for edge in edges:
        if edge.get("source_kind") == "atom" and isinstance(edge.get("source_id"), str):
            atom_ids.add(edge["source_id"])
        if edge.get("target_kind") == "atom" and isinstance(edge.get("target_id"), str):
            atom_ids.add(edge["target_id"])
    return atom_ids


def iter_atom_concept_edges(
    index: dict[str, Any],
    atoms: list[dict[str, Any]],
    existing_atom_ids: set[str],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    atom_ids = indexed_atom_ids(index)
    concept_ids = {
        identifier
        for identifier, record in index.items()
        if isinstance(identifier, str) and graph_kind(identifier, index) == "concept"
    }

    def add_candidate(atom_id: str, concept_id: str, derived_from: str) -> None:
        if atom_id not in atom_ids:
            exclusions["missing_atom_endpoint"] += 1
            return
        if atom_id not in existing_atom_ids:
            exclusions["atom_not_in_graph"] += 1
            return
        if concept_id not in concept_ids:
            exclusions["missing_concept_endpoint"] += 1
            return

        signature = (atom_id, "indexed_by", concept_id)
        if signature in seen:
            exclusions["duplicate_signature"] += 1
            return
        seen.add(signature)

        edges.append(
            {
                "source_kind": "atom",
                "source_id": atom_id,
                "target_kind": "concept",
                "target_id": concept_id,
                "relation_type": "indexed_by",
                "evidence_refs": [atom_id],
                "confidence": "high",
                "derived_from": derived_from,
            }
        )

    for concept_id, record in index.items():
        if graph_kind(concept_id, index) != "concept":
            continue
        if not isinstance(record, dict):
            exclusions["invalid_concept_record"] += 1
            continue
        data = record.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_concept_data"] += 1
            continue

        derived_from = record.get("file")
        if not isinstance(derived_from, str) or not derived_from:
            derived_from = "exports/generated/index_by_id.json"

        for field in CONCEPT_ATOM_FIELDS:
            for atom_id in collect_known_refs(data.get(field), atom_ids):
                add_candidate(atom_id, concept_id, derived_from)
        for atom_id in collect_known_refs(data.get("relations"), atom_ids):
            add_candidate(atom_id, concept_id, derived_from)

    for atom in atoms:
        if not isinstance(atom, dict):
            exclusions["invalid_atom_record"] += 1
            continue
        atom_id = atom.get("id")
        if not isinstance(atom_id, str):
            exclusions["invalid_atom_id"] += 1
            continue
        data = atom.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_atom_data"] += 1
            continue

        for field in ATOM_CONCEPT_REF_FIELDS:
            for concept_id in collect_known_refs(data.get(field), concept_ids):
                add_candidate(atom_id, concept_id, "exports/generated/atoms.json")

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def iter_atom_motif_edges(
    index: dict[str, Any],
    atoms: list[dict[str, Any]],
    existing_atom_ids: set[str],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    atom_ids = indexed_atom_ids(index)
    motif_ids = {
        identifier
        for identifier, record in index.items()
        if isinstance(identifier, str) and graph_kind(identifier, index) == "motif"
    }

    def add_candidate(atom_id: str, motif_id: str, derived_from: str) -> None:
        if atom_id not in atom_ids:
            exclusions["missing_atom_endpoint"] += 1
            return
        if atom_id not in existing_atom_ids:
            exclusions["atom_not_in_graph"] += 1
            return
        if motif_id not in motif_ids:
            exclusions["missing_motif_endpoint"] += 1
            return

        signature = (atom_id, "indexed_by", motif_id)
        if signature in seen:
            exclusions["duplicate_signature"] += 1
            return
        seen.add(signature)

        edges.append(
            {
                "source_kind": "atom",
                "source_id": atom_id,
                "target_kind": "motif",
                "target_id": motif_id,
                "relation_type": "indexed_by",
                "evidence_refs": [atom_id],
                "confidence": "high",
                "derived_from": derived_from,
            }
        )

    for motif_id, record in index.items():
        if graph_kind(motif_id, index) != "motif":
            continue
        if not isinstance(record, dict):
            exclusions["invalid_motif_record"] += 1
            continue
        data = record.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_motif_data"] += 1
            continue

        derived_from = record.get("file")
        if not isinstance(derived_from, str) or not derived_from:
            derived_from = "exports/generated/index_by_id.json"

        for field in MOTIF_ATOM_FIELDS:
            for atom_id in collect_known_refs(data.get(field), atom_ids):
                add_candidate(atom_id, motif_id, derived_from)
        for atom_id in collect_known_refs(data.get("relations"), atom_ids):
            add_candidate(atom_id, motif_id, derived_from)

    for atom in atoms:
        if not isinstance(atom, dict):
            exclusions["invalid_atom_record"] += 1
            continue
        atom_id = atom.get("id")
        if not isinstance(atom_id, str):
            exclusions["invalid_atom_id"] += 1
            continue
        data = atom.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_atom_data"] += 1
            continue

        for field in ATOM_MOTIF_REF_FIELDS:
            for motif_id in collect_known_refs(data.get(field), motif_ids):
                add_candidate(atom_id, motif_id, "exports/generated/atoms.json")

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def iter_atom_myth_edges(
    index: dict[str, Any],
    atoms: list[dict[str, Any]],
    existing_atom_ids: set[str],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    edges: list[dict[str, Any]] = []
    exclusions: Counter[str] = Counter()
    seen: set[tuple[str, str, str]] = set()

    atom_ids = indexed_atom_ids(index)
    myth_ids = {
        identifier
        for identifier, record in index.items()
        if isinstance(identifier, str) and graph_kind(identifier, index) == "myth"
    }

    def add_candidate(atom_id: str, myth_id: str, derived_from: str) -> None:
        if atom_id not in atom_ids:
            exclusions["missing_atom_endpoint"] += 1
            return
        if atom_id not in existing_atom_ids:
            exclusions["atom_not_in_graph"] += 1
            return
        if myth_id not in myth_ids:
            exclusions["missing_myth_endpoint"] += 1
            return

        signature = (atom_id, "indexed_by", myth_id)
        if signature in seen:
            exclusions["duplicate_signature"] += 1
            return
        seen.add(signature)

        edges.append(
            {
                "source_kind": "atom",
                "source_id": atom_id,
                "target_kind": "myth",
                "target_id": myth_id,
                "relation_type": "indexed_by",
                "evidence_refs": [atom_id],
                "confidence": "high",
                "derived_from": derived_from,
            }
        )

    for myth_id, record in index.items():
        if graph_kind(myth_id, index) != "myth":
            continue
        if not isinstance(record, dict):
            exclusions["invalid_myth_record"] += 1
            continue
        data = record.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_myth_data"] += 1
            continue

        derived_from = record.get("file")
        if not isinstance(derived_from, str) or not derived_from:
            derived_from = "exports/generated/index_by_id.json"

        for field in MYTH_ATOM_FIELDS:
            for atom_id in collect_known_refs(data.get(field), atom_ids):
                add_candidate(atom_id, myth_id, derived_from)
        for atom_id in collect_known_refs(data.get("relations"), atom_ids):
            add_candidate(atom_id, myth_id, derived_from)

    for atom in atoms:
        if not isinstance(atom, dict):
            exclusions["invalid_atom_record"] += 1
            continue
        atom_id = atom.get("id")
        if not isinstance(atom_id, str):
            exclusions["invalid_atom_id"] += 1
            continue
        data = atom.get("data", {})
        if not isinstance(data, dict):
            exclusions["invalid_atom_data"] += 1
            continue

        for field in ATOM_MYTH_REF_FIELDS:
            for myth_id in collect_known_refs(data.get(field), myth_ids):
                add_candidate(atom_id, myth_id, "exports/generated/atoms.json")

    edges.sort(
        key=lambda edge: (
            edge["source_id"],
            edge["target_id"],
            edge["derived_from"],
        )
    )
    return edges, exclusions


def write_edges(edges: list[dict[str, Any]]) -> None:
    ordered_edges = []
    for i, edge in enumerate(edges, start=1):
        ordered_edges.append(
            {
                "edge_id": f"EDGE-{i:06d}",
                "source_kind": edge["source_kind"],
                "source_id": edge["source_id"],
                "target_kind": edge["target_kind"],
                "target_id": edge["target_id"],
                "relation_type": edge["relation_type"],
                "evidence_refs": edge["evidence_refs"],
                "confidence": edge["confidence"],
                "derived_from": edge["derived_from"],
            }
        )

    bundle = {
        "schema_version": "1.0.0",
        "generated_from": [
            "exports/generated/index_by_id.json",
            "exports/generated/attribution_edges.json",
            "exports/generated/atoms.json",
            "exports/generated/quotes.json",
            "chapters/*/document_maitre.md",
        ],
        "edges": ordered_edges,
    }
    EDGES_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic C1 edges.")
    parser.add_argument("--quiet", action="store_true", help="Do not print generation statistics.")
    args = parser.parse_args(argv)

    index = load_index()
    attribution = load_attribution_edges()
    atoms = load_atoms()
    quotes = load_quotes()
    same_as_edges, same_as_exclusions = iter_same_as_edges(index)
    attributed_to_edges, attributed_to_exclusions = iter_attributed_to_edges(index, attribution)
    quote_source_edges, quote_source_exclusions = iter_quote_source_edges(index)
    atom_source_edges, atom_source_exclusions = iter_atom_source_edges(index, atoms, quotes)
    base_edges = [*same_as_edges, *attributed_to_edges, *quote_source_edges, *atom_source_edges]
    atom_concept_edges, atom_concept_exclusions = iter_atom_concept_edges(
        index,
        atoms,
        graph_atom_ids(base_edges),
    )
    concept_graph_edges = [*base_edges, *atom_concept_edges]
    atom_motif_edges, atom_motif_exclusions = iter_atom_motif_edges(
        index,
        atoms,
        graph_atom_ids(concept_graph_edges),
    )
    semantic_graph_edges = [*concept_graph_edges, *atom_motif_edges]
    atom_myth_edges, atom_myth_exclusions = iter_atom_myth_edges(
        index,
        atoms,
        graph_atom_ids(semantic_graph_edges),
    )
    edges = [*semantic_graph_edges, *atom_myth_edges]
    write_edges(edges)

    if not args.quiet:
        by_pair = Counter((edge["source_kind"], edge["target_kind"]) for edge in edges)
        print(f"edges={len(edges)}")
        for (source_kind, target_kind), count in sorted(by_pair.items()):
            print(f"{source_kind}->{target_kind}={count}")
        for key, count in sorted(same_as_exclusions.items()):
            print(f"excluded.same_as.{key}={count}")
        for key, count in sorted(attributed_to_exclusions.items()):
            print(f"excluded.attributed_to.{key}={count}")
        for key, count in sorted(quote_source_exclusions.items()):
            print(f"excluded.documented_by.{key}={count}")
        for key, count in sorted(atom_source_exclusions.items()):
            print(f"excluded.atom_documented_by.{key}={count}")
        for key, count in sorted(atom_concept_exclusions.items()):
            print(f"excluded.atom_indexed_by.{key}={count}")
        for key, count in sorted(atom_motif_exclusions.items()):
            print(f"excluded.atom_motif_indexed_by.{key}={count}")
        for key, count in sorted(atom_myth_exclusions.items()):
            print(f"excluded.atom_myth_indexed_by.{key}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
