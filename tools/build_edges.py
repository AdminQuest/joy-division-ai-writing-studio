#!/usr/bin/env python3
"""Generate the C1 edge graph.

C1 lot 2A generates all stable and currently validatable same_as edges from the
canonical identifier index. C1 lot 2B-1 adds only deterministic quote -> person
attributed_to edges. Quote -> source, atom/source, places, and interpretive
relations remain out of scope.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "exports" / "generated" / "index_by_id.json"
ATTRIBUTION_PATH = ROOT / "exports" / "generated" / "attribution_edges.json"
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


def load_attribution_edges() -> dict[str, Any]:
    return json.loads(ATTRIBUTION_PATH.read_text(encoding="utf-8"))


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
        row_flags = row.get("flags") or []
        if not isinstance(row_flags, list):
            row_flags = []

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
            flags = sorted({flag for flag in [*row_flags, *link_flags] if isinstance(flag, str)})
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
    same_as_edges, same_as_exclusions = iter_same_as_edges(index)
    attributed_to_edges, attributed_to_exclusions = iter_attributed_to_edges(index, attribution)
    edges = [*same_as_edges, *attributed_to_edges]
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
