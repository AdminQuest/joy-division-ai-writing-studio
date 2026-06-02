#!/usr/bin/env python3
"""Validate the C1 minimal relation graph seed.

This validator intentionally does not generate edges. It checks the checked-in
`exports/generated/edges.json` seed against the schema and against the existing
identifier universe from `exports/generated/index_by_id.json`.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "edge.schema.json"
EDGES_PATH = ROOT / "exports" / "generated" / "edges.json"
INDEX_PATH = ROOT / "exports" / "generated" / "index_by_id.json"

KINDS = {
    "atom",
    "source",
    "quote",
    "legacy_person",
    "legacy_chronology",
    "legacy_concert",
    "person",
    "place",
    "organization",
    "image",
    "event",
    "concert",
    "session",
    "song",
    "concept",
    "motif",
    "myth",
    "relation",
    "chapter",
    "metadata",
    "unknown",
}
RELATION_TYPES = {"same_as", "attributed_to", "documented_by", "indexed_by", "located_at"}
CONFIDENCE = {"high", "medium", "low", "unknown"}
EDGE_ID = re.compile(r"^EDGE-[0-9]{6}$")

KIND_PATTERNS = {
    "atom": re.compile(r"^S\d+-(?:A\d+|\d{3}|PART-[A-Z0-9-]+)$"),
    "source": re.compile(r"^S\d+$"),
    "quote": re.compile(r"^(?:S\d+-Q\d+|S\d+-CIT-\d+|CIT-S\d+-\d+)$"),
    "legacy_person": re.compile(r"^PERS-[A-Za-z0-9-]+(?:#[a-z0-9-]+)?$"),
    "legacy_chronology": re.compile(r"^(?:CHR|CHRON)-[A-Za-z0-9-]+$"),
    "legacy_concert": re.compile(r"^JD-CONCERT-[A-Za-z0-9-]+$"),
    "person": re.compile(r"^PERSON-[A-Za-z0-9-]+$"),
    "place": re.compile(r"^PLACE-[A-Za-z0-9-]+$"),
    "organization": re.compile(r"^ORG-[A-Za-z0-9-]+$"),
    "image": re.compile(r"^IMAGE-[A-Za-z0-9-]+$"),
    "event": re.compile(r"^EVENT-[A-Za-z0-9-]+$"),
    "concert": re.compile(r"^CONCERT-[A-Za-z0-9-]+$"),
    "session": re.compile(r"^SESSION-[A-Za-z0-9-]+$"),
    "song": re.compile(r"^(?:JD-SONG-\d{3}|SONG-[A-Za-z0-9-]+)$"),
    "concept": re.compile(r"^CONCEPT-[A-Za-z0-9_-]+$"),
    "motif": re.compile(r"^MOTIF-[A-Za-z0-9_-]+$"),
    "myth": re.compile(r"^MYTH-[A-Za-z0-9_-]+$"),
    "relation": re.compile(r"^(?:REL|R)-[A-Za-z0-9-]+$"),
}

RELATION_MATRIX = {
    "same_as": {
        ("legacy_person", "person"),
        ("legacy_chronology", "event"),
        ("legacy_chronology", "concert"),
        ("legacy_concert", "concert"),
    },
    "attributed_to": {("quote", "person")},
    "documented_by": {
        ("atom", "source"),
        ("quote", "source"),
        ("event", "source"),
        ("concert", "source"),
        ("person", "source"),
        ("place", "source"),
        ("song", "source"),
    },
    "indexed_by": {
        ("atom", "concept"),
        ("atom", "motif"),
        ("atom", "myth"),
    },
    "located_at": {
        ("atom", "place"),
        ("atom", "unknown"),
        ("event", "place"),
        ("concert", "place"),
        ("session", "place"),
        ("image", "place"),
    },
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_schema(schema: dict[str, Any], bundle: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise SystemExit(
            "Missing required dependency: jsonschema. "
            "Install dependencies with `python3 -m pip install -r requirements.txt`."
        ) from exc

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    messages = []
    for error in sorted(validator.iter_errors(bundle), key=lambda e: list(e.path)):
        path = ".".join(str(part) for part in error.path) or "<root>"
        messages.append(f"schema {path}: {error.message}")
    return messages


def id_matches_kind(kind: str, identifier: str) -> bool:
    pattern = KIND_PATTERNS.get(kind)
    return True if pattern is None else bool(pattern.match(identifier))


def indexed_graph_kind(identifier: str, record: Any) -> Optional[str]:
    if not isinstance(record, dict):
        return None
    raw_kind = record.get("kind")
    if not isinstance(raw_kind, str):
        return None
    if identifier.startswith("PERS-"):
        return "legacy_person"
    if identifier.startswith("JD-CONCERT-"):
        return "legacy_concert"
    if raw_kind == "chronology":
        if identifier.startswith("EVENT-"):
            return "event"
        if identifier.startswith(("CHR-", "CHRON-")):
            return "legacy_chronology"
    return raw_kind


def validate_endpoint(
    edge_label: str,
    role: str,
    kind: Any,
    identifier: Any,
    index: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(kind, str) or not isinstance(identifier, str):
        if not isinstance(identifier, str):
            errors.append(f"{edge_label}: {role}_id must be a string")
        return errors

    record = index.get(identifier)
    if record is None:
        errors.append(f"{edge_label}: {role}_id {identifier!r} is absent from index_by_id.json")
        return errors

    index_kind = indexed_graph_kind(identifier, record)
    if kind != "atom" and not id_matches_kind(kind, identifier):
        errors.append(f"{edge_label}: {role}_id {identifier!r} does not match kind {kind!r}")
    if index_kind != kind:
        errors.append(
            f"{edge_label}: {role}_kind {kind!r} does not match index kind "
            f"{index_kind!r} for {identifier!r}"
        )
    return errors


def validate_edge_semantics(edge: dict[str, Any], index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    edge_id = edge.get("edge_id", "<unknown>")
    edge_label = edge_id if isinstance(edge_id, str) else "<invalid edge_id>"
    source_kind = edge.get("source_kind")
    target_kind = edge.get("target_kind")
    source_id = edge.get("source_id")
    target_id = edge.get("target_id")
    relation_type = edge.get("relation_type")

    if isinstance(edge_id, str) and not EDGE_ID.match(edge_id):
        errors.append(f"{edge_id}: edge_id must match EDGE-000000")
    if isinstance(source_kind, str):
        if source_kind not in KINDS:
            errors.append(f"{edge_label}: unsupported source_kind {source_kind!r}")
    else:
        errors.append(f"{edge_label}: source_kind must be a string")
    if isinstance(target_kind, str):
        if target_kind not in KINDS:
            errors.append(f"{edge_label}: unsupported target_kind {target_kind!r}")
    else:
        errors.append(f"{edge_label}: target_kind must be a string")
    if isinstance(relation_type, str):
        if relation_type not in RELATION_TYPES:
            errors.append(f"{edge_label}: unsupported relation_type {relation_type!r}")
    else:
        errors.append(f"{edge_label}: relation_type must be a string")
    confidence = edge.get("confidence")
    if isinstance(confidence, str):
        if confidence not in CONFIDENCE:
            errors.append(f"{edge_label}: unsupported confidence {confidence!r}")
    else:
        errors.append(f"{edge_label}: confidence must be a string")

    for role, kind, identifier in (
        ("source", source_kind, source_id),
        ("target", target_kind, target_id),
    ):
        errors.extend(validate_endpoint(edge_label, role, kind, identifier, index))

    if isinstance(relation_type, str) and isinstance(source_kind, str) and isinstance(target_kind, str):
        allowed_pairs = RELATION_MATRIX.get(relation_type, set())
        if (source_kind, target_kind) not in allowed_pairs:
            errors.append(
                f"{edge_label}: relation {relation_type!r} does not allow "
                f"{source_kind!r} -> {target_kind!r}"
            )

    if relation_type != "same_as" and source_id == target_id:
        errors.append(f"{edge_label}: reflexive edge is only allowed for same_as")

    evidence_refs = edge.get("evidence_refs")
    if isinstance(evidence_refs, list):
        for ref in evidence_refs:
            if not isinstance(ref, str):
                errors.append(f"{edge_label}: evidence_ref must be a string")
                continue
            if ref not in index:
                errors.append(f"{edge_label}: evidence_ref {ref!r} is absent from index_by_id.json")

    derived_from = edge.get("derived_from")
    if isinstance(derived_from, str) and derived_from != "manual" and not (ROOT / derived_from).exists():
        errors.append(f"{edge_label}: derived_from {derived_from!r} does not exist")
    return errors


def validate_edges_semantics(bundle: Any, index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    edge_ids: set[str] = set()
    normalized_edges: set[tuple[str, str, str]] = set()
    edges = bundle.get("edges", []) if isinstance(bundle, dict) else []
    if not isinstance(edges, list):
        return errors

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            continue
        edge_id = edge.get("edge_id")
        if isinstance(edge_id, str):
            if edge_id in edge_ids:
                errors.append(f"{edge_id}: duplicate edge_id")
            edge_ids.add(edge_id)
        else:
            errors.append(f"edges[{i}]: edge_id must be a string for duplicate checks")

        signature = (edge.get("source_id"), edge.get("relation_type"), edge.get("target_id"))
        if all(isinstance(value, str) for value in signature):
            if signature in normalized_edges:
                label = edge_id if isinstance(edge_id, str) else f"edges[{i}]"
                errors.append(f"{label}: duplicate normalized edge {signature}")
            normalized_edges.add(signature)

        errors.extend(validate_edge_semantics(edge, index))
    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    bundle = load_json(EDGES_PATH)
    index = load_json(INDEX_PATH)
    if not isinstance(index, dict):
        raise SystemExit(f"{INDEX_PATH.relative_to(ROOT)} must contain a JSON object")

    errors = []
    errors.extend(validate_schema(schema, bundle))

    edges = bundle.get("edges", []) if isinstance(bundle, dict) else []
    errors.extend(validate_edges_semantics(bundle, index))

    print("Validation C1 relation edges")
    print("-" * 32)
    print(f"Schema file : {SCHEMA_PATH.relative_to(ROOT)}")
    print(f"Edges file  : {EDGES_PATH.relative_to(ROOT)}")
    print(f"Edges       : {len(edges) if isinstance(edges, list) else 0}")
    print(f"Errors      : {len(errors)}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\nC1 edge graph seed: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
