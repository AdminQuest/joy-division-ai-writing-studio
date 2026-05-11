#!/usr/bin/env python3
"""
Historiographical diagnostics generator

Produit un rapport de diagnostic documentaire avancé :

- atomes incomplets ;
- atomes fragiles ;
- risques de surinterprétation ;
- mythes ;
- controverses ;
- densité théorique ;
- motifs dominants.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORTS = REPO_ROOT / "exports" / "generated"
OUTPUT = EXPORTS / "historiographical_diagnostics.json"


def load_atoms():
    atoms_path = EXPORTS / "atoms.json"

    if not atoms_path.exists():
        raise SystemExit(
            "atoms.json introuvable. Lancer d’abord build_registers.py"
        )

    return json.loads(atoms_path.read_text(encoding="utf-8"))


def atom_data(atom):
    return atom.get("data", {})


def build_report(atoms):
    incomplete = []
    fragile = []
    myths = []
    controversies = []
    high_risk = []
    theoretical = []

    motif_counter = Counter()
    concept_counter = Counter()

    for atom in atoms:
        data = atom_data(atom)

        required = [
            "role_argumentatif",
            "niveau_preuve",
            "stabilite",
            "importance",
            "risque_surinterpretation",
            "motifs",
            "concepts_derives",
        ]

        missing = [field for field in required if field not in data]

        if missing:
            incomplete.append({
                "id": atom.get("id"),
                "missing": missing,
                "file": atom.get("file")
            })

        atom_type = data.get("type_unite")

        if atom_type == "mythe":
            myths.append(atom.get("id"))

        if atom_type == "controverse":
            controversies.append(atom.get("id"))

        niveau_preuve = data.get("niveau_preuve", {})

        if isinstance(niveau_preuve, dict):
            if niveau_preuve.get("statut") in ["fragile", "hypothese", "contesté"]:
                fragile.append(atom.get("id"))

        risque = data.get("risque_surinterpretation", {})

        if isinstance(risque, dict):
            if risque.get("niveau") in ["eleve", "critique"]:
                high_risk.append(atom.get("id"))

        nature = data.get("nature_discursive", [])

        if isinstance(nature, list):
            if "theorique" in nature:
                theoretical.append(atom.get("id"))

        motifs = data.get("motifs", [])

        if isinstance(motifs, list):
            motif_counter.update(motifs)

        concepts = data.get("concepts_derives", [])

        if isinstance(concepts, list):
            concept_counter.update(concepts)

    return {
        "summary": {
            "total_atoms": len(atoms),
            "incomplete_atoms": len(incomplete),
            "fragile_atoms": len(fragile),
            "myth_atoms": len(myths),
            "controversy_atoms": len(controversies),
            "high_risk_atoms": len(high_risk),
            "theoretical_atoms": len(theoretical),
        },
        "incomplete_atoms": incomplete,
        "fragile_atoms": fragile,
        "myth_atoms": myths,
        "controversy_atoms": controversies,
        "high_risk_atoms": high_risk,
        "theoretical_atoms": theoretical,
        "top_motifs": motif_counter.most_common(30),
        "top_derived_concepts": concept_counter.most_common(30),
    }


def main():
    atoms = load_atoms()
    report = build_report(atoms)

    OUTPUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Diagnostic historiographique généré")
    print(f"Sortie : {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
