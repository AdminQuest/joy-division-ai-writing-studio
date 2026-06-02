#!/usr/bin/env python3
"""Generate the C1 edge graph.

C1 lot 2A intentionally generates all stable and currently validatable same_as
edges from the canonical identifier index. The retained perimeter includes the
arbitrated JD-CONCERT-* -> CONCERT-* reconciliation as legacy_concert -> concert
so that the concert identity closure is not lost. Quote/source/person,
atom/source, places, and interpretive relations remain out of scope.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "exports" / "generated" / "index_by_id.json"
EDGES_PATH = ROOT / "exports" / "generated" / "edges.json"

ALLOWED_SAME_AS = {
    ("legacy_person", "person"),
    ("legacy_chronology", "event"),
    ("legacy_chronology", "concert"),
    # Kept after review arbitration: JD-CONCERT-* is a legacy concert endpoint,
    # while CONCERT-* is the canonical concert endpoint.
    ("legacy_concert", "concert"),
}


def load_index() -> dict[str, Any]:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


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
        "generated_from": ["exports/generated/index_by_id.json"],
        "edges": ordered_edges,
    }
    EDGES_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic C1 same_as edges.")
    parser.add_argument("--quiet", action="store_true", help="Do not print generation statistics.")
    args = parser.parse_args(argv)

    index = load_index()
    edges, exclusions = iter_same_as_edges(index)
    write_edges(edges)

    if not args.quiet:
        by_pair = Counter((edge["source_kind"], edge["target_kind"]) for edge in edges)
        print(f"edges={len(edges)}")
        for (source_kind, target_kind), count in sorted(by_pair.items()):
            print(f"{source_kind}->{target_kind}={count}")
        for key, count in sorted(exclusions.items()):
            print(f"excluded.{key}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
