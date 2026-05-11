#!/usr/bin/env python3
"""
Prompt context builder

Construit automatiquement un contexte historiographique
pour les prompts IA à partir :

- des diagnostics ;
- des motifs ;
- des risques ;
- des couches narratives ;
- des concepts.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORTS = REPO_ROOT / "exports" / "generated"

DIAGNOSTICS = EXPORTS / "historiographical_diagnostics.json"
OUTPUT = EXPORTS / "prompt_context.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_context(diag):
    context = {
        "global_constraints": [],
        "warnings": [],
        "recommended_focus": [],
    }

    if diag["summary"]["high_risk_atoms"] > 0:
        context["warnings"].append(
            "Limiter les surinterprétations et les téléologies."
        )

    if diag["summary"]["theoretical_atoms"] > 20:
        context["warnings"].append(
            "Réduire la densité théorique et revenir au terrain matériel."
        )

    top_motifs = diag.get("top_motifs", [])[:5]

    for motif, count in top_motifs:
        context["recommended_focus"].append({
            "motif": motif,
            "count": count,
        })

    context["global_constraints"] = [
        "Distinguer fait, mémoire et mythe.",
        "Éviter la prophétisation rétrospective.",
        "Préserver la matérialité des pratiques musicales.",
        "Limiter les abstractions théoriques.",
    ]

    return context


def main():
    diag = load_json(DIAGNOSTICS)
    context = build_context(diag)

    OUTPUT.write_text(
        json.dumps(context, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Contexte historiographique généré")
    print(f"Sortie : {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
