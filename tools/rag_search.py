#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Local RAG search v0.1

Purpose
-------
Minimal local retrieval engine over the generated documentary exports.

It reads:
  - exports/generated/all_records.json

Then builds a lightweight lexical index and returns the most relevant records
for a natural-language query.

This is intentionally dependency-light and local-first.
It does not call any external API.
It does not generate text.
It retrieves structured documentary records so that an LLM can then answer
from grounded material.

Prerequisite
------------
Run the documentary parser first:

    python tools/build_registers.py

Usage
-----

    python tools/rag_search.py "Ian Curtis epilepsy domestic life"
    python tools/rag_search.py "Transmission Mayflower Gretton" --top 8
    python tools/rag_search.py "Hannett Unknown Pleasures live sound" --kind atom
    python tools/rag_search.py "Love Will Tear Us Apart" --json

Design
------
This is not yet a semantic vector database.
It is a first reliable RAG layer:
  - deterministic;
  - transparent;
  - inspectable;
  - compatible with later vector embeddings.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = REPO_ROOT / "exports" / "generated"
ALL_RECORDS_PATH = GENERATED_DIR / "all_records.json"

TOKEN_RE = re.compile(r"[\wÀ-ÿ']+", re.UNICODE)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in",
    "is", "it", "of", "on", "or", "that", "the", "to", "with",
    "au", "aux", "ce", "ces", "dans", "de", "des", "du", "elle", "en", "et",
    "il", "la", "le", "les", "pour", "que", "qui", "sur", "un", "une",
}


def load_records() -> List[Dict[str, Any]]:
    if not ALL_RECORDS_PATH.exists():
        print(
            f"Missing {ALL_RECORDS_PATH.relative_to(REPO_ROOT)}. Run: python tools/build_registers.py",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return json.loads(ALL_RECORDS_PATH.read_text(encoding="utf-8"))


def flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {flatten(val)}" for key, val in value.items())
    return str(value)


def record_text(record: Dict[str, Any]) -> str:
    data = record.get("data", {})
    fields = [
        record.get("id", ""),
        record.get("kind", ""),
        record.get("heading", ""),
        record.get("file", ""),
        flatten(data),
    ]
    return "\n".join(fields)


def tokenize(text: str) -> List[str]:
    tokens = [token.lower() for token in TOKEN_RE.findall(text)]
    return [token for token in tokens if len(token) > 2 and token not in STOPWORDS]


def build_index(records: List[Dict[str, Any]]) -> Tuple[List[Counter], Dict[str, int]]:
    doc_terms: List[Counter] = []
    doc_frequency: Dict[str, int] = defaultdict(int)

    for record in records:
        terms = Counter(tokenize(record_text(record)))
        doc_terms.append(terms)
        for term in terms:
            doc_frequency[term] += 1

    return doc_terms, dict(doc_frequency)


def score_records(
    records: List[Dict[str, Any]],
    query: str,
    kind: str | None = None,
) -> List[Tuple[float, Dict[str, Any]]]:
    query_terms = Counter(tokenize(query))
    if not query_terms:
        return []

    doc_terms, doc_frequency = build_index(records)
    total_docs = len(records)
    results: List[Tuple[float, Dict[str, Any]]] = []

    for record, terms in zip(records, doc_terms):
        if kind and record.get("kind") != kind:
            continue

        score = 0.0
        for term, qtf in query_terms.items():
            tf = terms.get(term, 0)
            if not tf:
                continue
            idf = math.log((1 + total_docs) / (1 + doc_frequency.get(term, 0))) + 1
            score += (1 + math.log(tf)) * idf * qtf

        # Small boosts for exact phrase fragments in the record text.
        lower_text = record_text(record).lower()
        lower_query = query.lower().strip()
        if lower_query and lower_query in lower_text:
            score *= 1.5

        if score > 0:
            results.append((score, record))

    return sorted(results, key=lambda item: item[0], reverse=True)


def concise_record(record: Dict[str, Any]) -> Dict[str, Any]:
    data = record.get("data", {})
    return {
        "id": record.get("id"),
        "kind": record.get("kind"),
        "file": record.get("file"),
        "heading": record.get("heading"),
        "summary_fields": {
            key: data.get(key)
            for key in [
                "source_id", "auteur", "titre", "pages_pdf", "type_unite",
                "concepts", "chapitres", "citation_originale", "traduction_editoriale_fr",
                "song", "themes", "name", "role", "date", "event", "certainty",
            ]
            if key in data
        },
    }


def print_human(results: List[Tuple[float, Dict[str, Any]]], top: int) -> None:
    for rank, (score, record) in enumerate(results[:top], start=1):
        data = record.get("data", {})
        print(f"\n#{rank}  score={score:.2f}  id={record.get('id')}  kind={record.get('kind')}")
        print(f"file: {record.get('file')}")
        if record.get("heading"):
            print(f"heading: {record.get('heading')}")

        for key in [
            "source_id", "auteur", "titre", "pages_pdf", "type_unite",
            "concepts", "chapitres", "citation_originale", "traduction_editoriale_fr",
            "song", "themes", "name", "role", "date", "event", "certainty", "notes",
        ]:
            if key in data:
                value = data[key]
                if isinstance(value, (list, dict)):
                    value = json.dumps(value, ensure_ascii=False)
                print(f"{key}: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the local documentary RAG index.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=10, help="Number of results to return")
    parser.add_argument("--kind", choices=["atom", "quote", "chronology", "song", "person", "unknown"], help="Restrict by record kind")
    parser.add_argument("--json", action="store_true", help="Print JSON results")
    args = parser.parse_args()

    records = load_records()
    results = score_records(records, args.query, args.kind)

    if args.json:
        payload = [
            {"score": score, "record": concise_record(record)}
            for score, record in results[: args.top]
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(results, args.top)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
