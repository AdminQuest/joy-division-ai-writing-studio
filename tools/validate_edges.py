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
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "edge.schema.json"
EDGES_PATH = ROOT / "exports" / "generated" / "edges.json"
INDEX_PATH = ROOT / "exports" / "generated" / "index_by_id.json"

REQUIRED_ROOT = {"schema_version", "generated_from", "edges"}
REQUIRED_EDGE = {
    "edge_id",
    "source_kind",
    "source_id",
    "target_kind",
    "target_id",
    "relation_type",
    "evidence_refs",
    "confidence",
    "derived_from",
}
ALLOWED_EDGE = REQUIRED_EDGE | {"qualifiers", "status"}
KINDS = {
    "atom",
    "source",
    "quote",
    "legacy_person",
    "legacy_chronology",
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
RELATION_TYPES = {"same_as", "attributed_to", "documented_by", "located_at"}
CONFIDENCE = {"high", "medium", "low", "unknown"}
EDGE_ID = re.compile(r"^EDGE-[0-9]{6}$")

KIND_PATTERNS = {
    "atom": re.compile(r"^S\d+-(?:A\d+|\d{3}|PART-[A-Z0-9-]+)$"),
    "source": re.compile(r"^S\d+$"),
    "quote": re.compile(r"^(?:S\d+-Q\d+|S\d+-CIT-\d+|CIT-S\d+-\d+)$"),
    "legacy_person": re.compile(r"^PERS-[A-Za-z0-9-]+(?:#[a-z0-9-]+)?$"),
    "legacy_chronology": re.compile(r"^(?:CHR|CHRON)-[A-Za-z0-9-]+$"),
    "person": re.compile(r"^PERSON-[A-Za-z0-9-]+$"),
    "place": re.compile(r"^PLACE-[A-Za-z0-9-]+$"),
    "organization": re.compile(r"^ORG-[A-Za-z0-9-]+$"),
    "image": re.compile(r"^IMAGE-[A-Za-z0-9-]+$"),
    "event": re.compile(r"^EVENT-[A-Za-z0-9-]+$"),
    "concert": re.compile(r"^(?:CONCERT|JD-CONCERT)-[A-Za-z0-9-]+$"),
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
    "located_at": {
        ("atom", "place"),
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


def validate_with_jsonschema(schema: dict[str, Any], bundle: dict[str, Any]) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return []
    validator = Draft202012Validator(schema)
    messages = []
    for error in sorted(validator.iter_errors(bundle), key=lambda e: list(e.path)):
        path = ".".join(str(part) for part in error.path) or "<root>"
        messages.append(f"schema {path}: {error.message}")
    return messages


def schema_fallback(bundle: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(bundle, dict):
        return ["schema <root>: root must be an object"]
    extra_root = set(bundle) - REQUIRED_ROOT
    missing_root = REQUIRED_ROOT - set(bundle)
    if extra_root:
        errors.append(f"schema <root>: unexpected keys {sorted(extra_root)}")
    if missing_root:
        errors.append(f"schema <root>: missing keys {sorted(missing_root)}")
    if bundle.get("schema_version") != "1.0.0":
        errors.append("schema schema_version: expected '1.0.0'")
    generated_from = bundle.get("generated_from")
    if not isinstance(generated_from, list) or not generated_from or not all(isinstance(v, str) and v for v in generated_from):
        errors.append("schema generated_from: expected non-empty list of strings")
    edges = bundle.get("edges")
    if not isinstance(edges, list):
        errors.append("schema edges: expected list")
        return errors
    if len(edges) > 9:
        errors.append("schema edges: expected fewer than 10 edges")
    for i, edge in enumerate(edges):
        loc = f"edges[{i}]"
        if not isinstance(edge, dict):
            errors.append(f"schema {loc}: expected object")
            continue
        missing = REQUIRED_EDGE - set(edge)
        extra = set(edge) - ALLOWED_EDGE
        if missing:
            errors.append(f"schema {loc}: missing keys {sorted(missing)}")
        if extra:
            errors.append(f"schema {loc}: unexpected keys {sorted(extra)}")
        for key in ("edge_id", "source_kind", "source_id", "target_kind", "target_id", "relation_type", "confidence", "derived_from"):
            if key in edge and not isinstance(edge[key], str):
                errors.append(f"schema {loc}.{key}: expected string")
        evidence = edge.get("evidence_refs")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(v, str) and v for v in evidence):
            errors.append(f"schema {loc}.evidence_refs: expected non-empty list of strings")
        if isinstance(evidence, list) and len(set(evidence)) != len(evidence):
            errors.append(f"schema {loc}.evidence_refs: duplicate values")
    return errors


def id_matches_kind(kind: str, identifier: str) -> bool:
    pattern = KIND_PATTERNS.get(kind)
    return True if pattern is None else bool(pattern.match(identifier))


def validate_edge_semantics(edge: dict[str, Any], index_ids: set[str]) -> list[str]:
    errors: list[str] = []
    edge_id = edge.get("edge_id", "<unknown>")
    source_kind = edge.get("source_kind")
    target_kind = edge.get("target_kind")
    source_id = edge.get("source_id")
    target_id = edge.get("target_id")
    relation_type = edge.get("relation_type")

    if isinstance(edge_id, str) and not EDGE_ID.match(edge_id):
        errors.append(f"{edge_id}: edge_id must match EDGE-000000")
    if source_kind not in KINDS:
        errors.append(f"{edge_id}: unsupported source_kind {source_kind!r}")
    if target_kind not in KINDS:
        errors.append(f"{edge_id}: unsupported target_kind {target_kind!r}")
    if relation_type not in RELATION_TYPES:
        errors.append(f"{edge_id}: unsupported relation_type {relation_type!r}")
    if edge.get("confidence") not in CONFIDENCE:
        errors.append(f"{edge_id}: unsupported confidence {edge.get('confidence')!r}")

    for role, kind, identifier in (
        ("source", source_kind, source_id),
        ("target", target_kind, target_id),
    ):
        if not isinstance(kind, str) or not isinstance(identifier, str):
            continue
        if not id_matches_kind(kind, identifier):
            errors.append(f"{edge_id}: {role}_id {identifier!r} does not match kind {kind!r}")
        if identifier not in index_ids:
            errors.append(f"{edge_id}: {role}_id {identifier!r} is absent from index_by_id.json")

    if isinstance(relation_type, str) and isinstance(source_kind, str) and isinstance(target_kind, str):
        allowed_pairs = RELATION_MATRIX.get(relation_type, set())
        if (source_kind, target_kind) not in allowed_pairs:
            errors.append(
                f"{edge_id}: relation {relation_type!r} does not allow "
                f"{source_kind!r} -> {target_kind!r}"
            )

    if relation_type != "same_as" and source_id == target_id:
        errors.append(f"{edge_id}: reflexive edge is only allowed for same_as")

    for ref in edge.get("evidence_refs", []):
        if ref not in index_ids:
            errors.append(f"{edge_id}: evidence_ref {ref!r} is absent from index_by_id.json")

    derived_from = edge.get("derived_from")
    if isinstance(derived_from, str) and derived_from != "manual" and not (ROOT / derived_from).exists():
        errors.append(f"{edge_id}: derived_from {derived_from!r} does not exist")
    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    bundle = load_json(EDGES_PATH)
    index = load_json(INDEX_PATH)
    index_ids = set(index)

    errors = []
    errors.extend(validate_with_jsonschema(schema, bundle))
    errors.extend(schema_fallback(bundle))

    edge_ids: set[str] = set()
    normalized_edges: set[tuple[str, str, str]] = set()
    edges = bundle.get("edges", []) if isinstance(bundle, dict) else []
    if isinstance(edges, list):
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            edge_id = edge.get("edge_id")
            if edge_id in edge_ids:
                errors.append(f"{edge_id}: duplicate edge_id")
            edge_ids.add(edge_id)
            signature = (edge.get("source_id"), edge.get("relation_type"), edge.get("target_id"))
            if signature in normalized_edges:
                errors.append(f"{edge_id}: duplicate normalized edge {signature}")
            normalized_edges.add(signature)
            errors.extend(validate_edge_semantics(edge, index_ids))

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
