#!/usr/bin/env python3
"""
Générateur de graphe documentaire.

Produit :
- noeuds ;
- relations ;
- clusters ;
- liens concepts/atomes/mythes/motifs.

Sorties :
exports/generated/documentary_graph.json
exports/generated/documentary_edges.json
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORTS = REPO_ROOT / "exports" / "generated"

ATOMS = EXPORTS / "atoms.json"
GRAPH = EXPORTS / "documentary_graph.json"
EDGES = EXPORTS / "documentary_edges.json"


def load_atoms():
    return json.loads(ATOMS.read_text(encoding="utf-8"))


def build_graph(atoms):
    nodes = []
    edges = []

    for atom in atoms:
        data = atom.get("data", {})

        nodes.append({
            "id": atom.get("id"),
            "type": data.get("type_unite"),
            "importance": data.get("importance", {}),
            "risk": data.get("risque_surinterpretation", {}),
            "chapters": data.get("chapitres", []),
            "concepts": data.get("concepts", []),
            "motifs": data.get("motifs", []),
        })

        relations = data.get("relations", [])

        if isinstance(relations, list):
            for rel in relations:
                if not isinstance(rel, dict):
                    continue

                target = rel.get("cible")
                rel_type = rel.get("type")

                if not target or not rel_type:
                    continue

                edges.append({
                    "source": atom.get("id"),
                    "target": target,
                    "type": rel_type,
                })

    return {
        "nodes": nodes,
        "edges": edges,
    }


def main():
    atoms = load_atoms()
    graph = build_graph(atoms)

    GRAPH.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    EDGES.write_text(
        json.dumps(graph["edges"], ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Graphe documentaire généré")
    print(f"Noeuds : {len(graph['nodes'])}")
    print(f"Relations : {len(graph['edges'])}")


if __name__ == "__main__":
    main()
