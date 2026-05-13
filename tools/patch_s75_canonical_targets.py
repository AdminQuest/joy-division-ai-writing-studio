#!/usr/bin/env python3
"""Remplace dans S75 les cibles candidates désormais canonisées.

À exécuter après :

    python3 tools/patch_s75_relations.py

Ce script ne modifie pas les registres. Il transforme les relations de type
`signale_candidat` vers les nouveaux identifiants canoniques créés dans :

    registers/concepts/master_concepts.md
    registers/motifs/master_motifs.md
    registers/myths/master_myths.md

Cibles stabilisées :

    CONCEPT-004 — prudence historiographique
    CONCEPT-005 — contrainte productive
    CONCEPT-006 — architecture sonore
    MOTIF-004   — culture bootleg
    MOTIF-005   — provocation
    MOTIF-006   — seuil
    MYTH-006    — Le génie immédiat de Joy Division
    MYTH-007    — L’imagerie nazie comme fascination fasciste
    MYTH-008    — Stiff Kittens comme origine constituée
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "sources" / "ott_unknown_pleasures" / "source_part_01.md"

REPLACEMENTS = {
    # CONCEPT-004 — prudence historiographique
    """  - type: signale_candidat
    cible: CONCEPT-prudence-historiographique
    note: "Concept à créer : méthode de contrôle des dérives mythographiques.""": """  - type: prolonge
    cible: CONCEPT-004
    note: "Prolonge le concept de prudence historiographique comme méthode de contrôle des dérives mythographiques.""",

    # CONCEPT-005 — contrainte productive
    """  - type: signale_candidat
    cible: CONCEPT-contrainte-productive
    note: "Concept à créer : la limite technique et matérielle produit une forme.""": """  - type: illustre
    cible: CONCEPT-005
    note: "Illustre la contrainte productive : la limite technique et matérielle produit ou révèle une forme.""",

    """  - type: signale_candidat
    cible: CONCEPT-contrainte-productive
    note: "Concept à créer : la contrainte matérielle produit ou révèle la forme.""": """  - type: illustre
    cible: CONCEPT-005
    note: "Illustre la contrainte productive : la contrainte matérielle produit ou révèle la forme.""",

    # CONCEPT-006 — architecture sonore
    """  - type: signale_candidat
    cible: CONCEPT-architecture-sonore
    note: "Concept à créer : organisation formelle du son Joy Division.""": """  - type: prépare
    cible: CONCEPT-006
    note: "Prépare le concept d’architecture sonore comme organisation formelle du son Joy Division.""",

    """  - type: signale_candidat
    cible: CONCEPT-architecture-sonore
    note: "Concept à créer pour formaliser le passage du punk à l'organisation sonore Joy Division.""": """  - type: annonce
    cible: CONCEPT-006
    note: "Annonce l’architecture sonore comme formalisation du passage du punk à Joy Division.""",

    # MOTIF-004 — culture bootleg
    """  - type: signale_candidat
    cible: MOTIF-culture-bootleg
    note: "Motif à créer pour le chapitre 8 et les archives sonores non officielles.""": """  - type: prolonge
    cible: MOTIF-004
    note: "Prolonge le motif de culture bootleg, utile au chapitre 8 et aux archives sonores non officielles.""",

    # MYTH-006 — génie immédiat
    """  - type: signale_candidat
    cible: MYTH-génie-immédiat
    note: "Mythe à créer : Joy Division ne surgit pas immédiatement comme forme achevée.""": """  - type: nuance
    cible: MYTH-006
    note: "Nuance le mythe du génie immédiat : Joy Division ne surgit pas comme forme achevée.""",

    # MYTH-007 — imagerie nazie comme fascination fasciste
    """  - type: signale_candidat
    cible: MYTH-imagerie-nazie-comme-fascination-fasciste
    note: "Mythe à créer pour éviter l'alternative simpliste fascination / innocence.""": """  - type: nuance
    cible: MYTH-007
    note: "Nuance le mythe de l’imagerie nazie comme fascination fasciste simple, sans basculer dans l’excuse inverse.""",

    """  - type: signale_candidat
    cible: MYTH-imagerie-nazie-comme-fascination-fasciste
    note: "Mythe à créer pour encadrer les lectures réductrices de l'imagerie WWII.""": """  - type: nuance
    cible: MYTH-007
    note: "Encadre les lectures réductrices de l’imagerie WWII par le mythe canonique MYTH-007.""",

    """  - type: signale_candidat
    cible: MYTH-imagerie-nazie-comme-fascination-fasciste
    note: "Mythe à créer pour éviter à la fois l'excuse romantique et la condamnation non contextualisée.""": """  - type: nuance
    cible: MYTH-007
    note: "Nuance le mythe de l’imagerie nazie comme fascination fasciste, en évitant l’excuse romantique comme la condamnation non contextualisée.""",

    # MYTH-008 — Stiff Kittens
    """  - type: signale_candidat
    cible: MYTH-Stiff-Kittens-origine-constituée
    note: "Mythe mineur à créer seulement si d’autres sources confirment sa récurrence.""": """  - type: nuance
    cible: MYTH-008
    note: "Nuance le micro-mythe de Stiff Kittens comme origine constituée.""",
}

# Remplacements légers : candidats devenus motifs canoniques mais qui ne figurent pas
# nécessairement comme relations explicites dans tous les atomes S75.
OPTIONAL_INLINE = {
    "cible: MOTIF-culture-bootleg": "cible: MOTIF-004",
    "cible: CONCEPT-prudence-historiographique": "cible: CONCEPT-004",
    "cible: CONCEPT-contrainte-productive": "cible: CONCEPT-005",
    "cible: CONCEPT-architecture-sonore": "cible: CONCEPT-006",
    "cible: MYTH-génie-immédiat": "cible: MYTH-006",
    "cible: MYTH-imagerie-nazie-comme-fascination-fasciste": "cible: MYTH-007",
    "cible: MYTH-Stiff-Kittens-origine-constituée": "cible: MYTH-008",
}


def main() -> int:
    if not TARGET.exists():
        print(f"File not found: {TARGET}")
        return 1

    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    missing = []

    for old, new in REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            changed += 1
        else:
            missing.append(old.splitlines()[0:3])

    inline_changed = 0
    for old, new in OPTIONAL_INLINE.items():
        if old in text:
            text = text.replace(old, new)
            inline_changed += 1

    TARGET.write_text(text, encoding="utf-8")

    print(f"S75 canonical target patch applied: {changed} block replacement(s), {inline_changed} inline replacement type(s).")
    if missing:
        print(f"NOTE: {len(missing)} expected block(s) not found. This is acceptable if the first S75 patch was not yet applied or if the block was already canonicalized.")
        for block in missing:
            print("---")
            print("\n".join(block))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
