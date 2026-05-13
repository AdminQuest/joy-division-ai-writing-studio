#!/usr/bin/env python3
"""Stabilise les relations des atomes S75 — Chris Ott.

Ce script applique uniquement les corrections relationnelles à :

    sources/ott_unknown_pleasures/source_part_01.md

Il ne modifie pas les registres. Il remplace les cibles libres ou provisoires
par les identifiants canoniques disponibles quand ils existent, et conserve
les relations internes S75 structurantes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "sources" / "ott_unknown_pleasures" / "source_part_01.md"

REPLACEMENTS = {
    # S75-A001 — pas de cible canonique pertinente existante pour l'héritage / culte sombre.
    """relations:\n  - type: prolonge\n    cible: MOTIF-heritage\n  - type: nuance\n    cible: MYTH-culte_sombre""": """relations:\n  - type: signale_candidat\n    cible: MOTIF-postérité\n    note: \"Cible non encore canonisée ; motif à créer si la postérité devient un axe transversal.\"\n  - type: signale_candidat\n    cible: CONCEPT-réception-posthume\n    note: \"Cible non encore canonisée ; concept à créer si plusieurs sources confirment cet axe.\""" ,

    # S75-A002 — rattachement aux mythes existants + candidat conceptuel.
    """relations:\n  - type: nuance\n    cible: MYTH-joy_division_mystique\n  - type: prolonge\n    cible: CONCEPT-prudence_historiographique""": """relations:\n  - type: nuance\n    cible: MYTH-002\n    note: \"Évite de transformer Curtis en figure prophétique par mystification rétrospective.\"\n  - type: nuance\n    cible: MYTH-003\n    note: \"Évite de transformer Manchester en matrice explicative totale.\"\n  - type: nuance\n    cible: MYTH-004\n    note: \"Évite de réduire le son Joy Division à une mystique Hannett isolée.\"\n  - type: signale_candidat\n    cible: CONCEPT-prudence-historiographique\n    note: \"Concept à créer : méthode de contrôle des dérives mythographiques.\""" ,

    # S75-A003 — mythe Curtis stabilisé.
    """relations:\n  - type: nuance\n    cible: MYTH-curtis_prophete_de_sa_mort\n  - type: prolonge\n    cible: S45""": """relations:\n  - type: nuance\n    cible: MYTH-002\n    note: \"Évite de lire la trajectoire de Curtis comme destin prophétique entièrement annoncé.\"\n  - type: prolonge\n    cible: S45\n    note: \"Relation vers la source Deborah Curtis ; à remplacer ultérieurement par un atome S45 précis si disponible.\""" ,

    # S75-A004 — Free Trade Hall, Manchester, géographie émotionnelle.
    """relations:\n  - type: nuance\n    cible: MYTH-lesser_free_trade_hall_origine_absolue\n  - type: prolonge\n    cible: CONCEPT-geographie_emotionnelle""": """relations:\n  - type: nuance\n    cible: MYTH-001\n    note: \"Présente le punk comme autorisation et possibilité, non comme origine unique.\"\n  - type: nuance\n    cible: MYTH-003\n    note: \"Évite de transformer Manchester en cause totale du son.\"\n  - type: prolonge\n    cible: CONCEPT-003\n    note: \"Relie la différence Manchester/Londres à une géographie émotionnelle du groupe.\""" ,

    # S75-A005 — Free Trade Hall stabilisé.
    """relations:\n  - type: nuance\n    cible: MYTH-lesser_free_trade_hall_origine_absolue\n  - type: corrobore\n    cible: S74-A004""": """relations:\n  - type: nuance\n    cible: MYTH-001\n    note: \"Distingue le concert du 4 juin 1976, son inflation mémorielle, et le choc du 20 juillet pour Curtis.\"\n  - type: corrobore\n    cible: S74-A004\n    note: \"Recoupe l’analyse du concert des Sex Pistols comme moment originel mancunien, sans en faire une origine absolue.\""" ,

    # S75-A006 — Stiff Kittens : candidat mythe.
    """relations:\n  - type: nuance\n    cible: MYTH-stiff_kittens_origine\n  - type: prolonge\n    cible: S75-A017""": """relations:\n  - type: prépare\n    cible: S75-A017\n    note: \"Prépare la question de la nomination avant le passage Warsaw → Joy Division.\"\n  - type: signale_candidat\n    cible: MYTH-Stiff-Kittens-origine-constituée\n    note: \"Mythe mineur à créer seulement si d’autres sources confirment sa récurrence.\""" ,

    # S75-A007 — reconnaissance immédiate : candidat mythe.
    """relations:\n  - type: prolonge\n    cible: S75-A006\n  - type: nuance\n    cible: MYTH-reconnaissance_immediate""": """relations:\n  - type: prolonge\n    cible: S75-A006\n    note: \"Prolonge la question de la reconnaissance faible et encore indécise de Warsaw.\"\n  - type: signale_candidat\n    cible: MYTH-reconnaissance-immédiate\n    note: \"Mythe à créer seulement si la reconnaissance précoce de Warsaw devient un motif récurrent.\""" ,

    # S75-A008 — bootleg : candidat motif.
    """relations:\n  - type: prolonge\n    cible: MOTIF-bootleg\n  - type: corrobore\n    cible: S68""": """relations:\n  - type: signale_candidat\n    cible: MOTIF-culture-bootleg\n    note: \"Motif à créer pour le chapitre 8 et les archives sonores non officielles.\"\n  - type: corrobore\n    cible: S68\n    note: \"Relation provisoire vers Marco Broll ; à remplacer par un atome S68 précis si disponible.\""" ,

    # S75-A009 — génie immédiat + contrainte productive.
    """relations:\n  - type: prolonge\n    cible: S75-A008\n  - type: nuance\n    cible: MYTH-genie_immediat""": """relations:\n  - type: prolonge\n    cible: S75-A008\n    note: \"Transforme l’objet bootleg en preuve sonore imparfaite de la genèse.\"\n  - type: signale_candidat\n    cible: MYTH-génie-immédiat\n    note: \"Mythe à créer : Joy Division ne surgit pas immédiatement comme forme achevée.\"\n  - type: signale_candidat\n    cible: CONCEPT-contrainte-productive\n    note: \"Concept à créer : la limite technique et matérielle produit une forme.\""" ,

    # S75-A010 — Curtis poète déjà accompli → mythe Curtis existant + candidat plus fin.
    """relations:\n  - type: nuance\n    cible: MYTH-curtis_poete_deja_accompli\n  - type: corrobore\n    cible: S45""": """relations:\n  - type: nuance\n    cible: MYTH-002\n    note: \"Évite de transformer les premiers textes de Curtis en prophétie déjà accomplie.\"\n  - type: signale_candidat\n    cible: MYTH-Curtis-poète-déjà-accompli\n    note: \"Mythe plus précis à créer si la maturation inachevée des premiers textes devient un axe récurrent.\"\n  - type: corrobore\n    cible: S45\n    note: \"Relation vers Deborah Curtis ; à remplacer par un atome S45 précis si disponible.\""" ,

    # S75-A011 — Gretton / stabilisation.
    """relations:\n  - type: prolonge\n    cible: S75-A009\n  - type: annonce\n    cible: CONCEPT-gretton_management""": """relations:\n  - type: prolonge\n    cible: S75-A009\n    note: \"Prolonge la genèse non héroïque par une stabilisation humaine négative.\"\n  - type: prépare\n    cible: S75-A015\n    note: \"Prépare la stabilisation formelle permise par Stephen Morris.\"\n  - type: signale_candidat\n    cible: CONCEPT-stabilisation-négative\n    note: \"Concept à créer si l'éviction ou la contrainte humaine devient une catégorie d'analyse.\""" ,

    # S75-A012 — poésie de l'aliénation + isolement + mythe Curtis.
    """relations:\n  - type: nuance\n    cible: S75-A010\n  - type: prépare\n    cible: CONCEPT-poesie_de_l_alienation""": """relations:\n  - type: nuance\n    cible: S75-A010\n    note: \"Nuance la brutalité primitive de « Gutz » par une scène de maturation inachevée.\"\n  - type: nuance\n    cible: MYTH-002\n    note: \"Évite de lire l'écriture de Curtis comme prophétie déjà constituée.\"\n  - type: prolonge\n    cible: MOTIF-003\n    note: \"Active le motif d'isolement dans la scène de la pièce bleue.\"\n  - type: signale_candidat\n    cible: CONCEPT-poésie-de-l-aliénation\n    note: \"Concept à créer si l'analyse des paroles de Curtis est stabilisée transversalement.\""" ,

    # S75-A013 — choc / imagerie nazie.
    """relations:\n  - type: prolonge\n    cible: S75-A018\n  - type: nuance\n    cible: MYTH-nazi_imagery_simple_fascination""": """relations:\n  - type: prépare\n    cible: S75-A016\n    note: \"Prépare l'ambiguïté Hess par l'arrière-plan shock art / Throbbing Gristle.\"\n  - type: prépare\n    cible: S75-A018\n    note: \"Prépare la lecture de l'imagerie litigieuse de *An Ideal for Living*.\"\n  - type: signale_candidat\n    cible: MYTH-imagerie-nazie-comme-fascination-fasciste\n    note: \"Mythe à créer pour éviter l'alternative simpliste fascination / innocence.\"\n  - type: signale_candidat\n    cible: CONCEPT-esthétique-du-choc\n    note: \"Concept à créer si l'influence industrial / shock art devient transversale.\""" ,

    # S75-A014 — Sumner / Lower Broughton.
    """relations:\n  - type: nuance\n    cible: MYTH-curtis_centre_unique\n  - type: prolonge\n    cible: CONCEPT-geographie_emotionnelle""": """relations:\n  - type: nuance\n    cible: MYTH-002\n    note: \"Rééquilibre le récit en rappelant l’expérience sociale de Sumner.\"\n  - type: nuance\n    cible: MYTH-003\n    note: \"Inscrit Salford et Lower Broughton dans le récit sans déterminisme urbain mécanique.\"\n  - type: prolonge\n    cible: CONCEPT-003\n    note: \"Alimente la géographie émotionnelle par la trajectoire de Sumner.\"\n  - type: prolonge\n    cible: CONCEPT-002\n    note: \"Rattache Lower Broughton au déclin urbain et industriel.\"\n  - type: prolonge\n    cible: MOTIF-002\n    note: \"Active le motif de ruine ou d’effondrement industriel.\""" ,

    # S75-A015 — architecture sonore candidate.
    """relations:\n  - type: prolonge\n    cible: S75-A011\n  - type: prépare\n    cible: CONCEPT-architecture_sonore""": """relations:\n  - type: prolonge\n    cible: S75-A011\n    note: \"Prolonge la stabilisation humaine par la stabilisation rythmique.\"\n  - type: prépare\n    cible: S75-A020\n    note: \"Prépare le seuil formel de « No Love Lost ».\"\n  - type: signale_candidat\n    cible: CONCEPT-architecture-sonore\n    note: \"Concept à créer : organisation formelle du son Joy Division.\""" ,

    # S75-A016 — Hess / Electric Circus.
    """relations:\n  - type: prolonge\n    cible: S75-A013\n  - type: annonce\n    cible: S75-A018""": """relations:\n  - type: prolonge\n    cible: S75-A013\n    note: \"Prolonge l'arrière-plan shock art dans une ambiguïté scénique documentée.\"\n  - type: annonce\n    cible: S75-A018\n    note: \"Annonce la cristallisation de l'ambiguïté dans *An Ideal for Living*.\"\n  - type: signale_candidat\n    cible: MYTH-imagerie-nazie-comme-fascination-fasciste\n    note: \"Mythe à créer pour encadrer les lectures réductrices de l'imagerie WWII.\""" ,

    # S75-A017 — Warsaw / Joy Division.
    """relations:\n  - type: nuance\n    cible: S75-A006\n  - type: corrobore\n    cible: MYTH-warsaw_cover_up\n  - type: prolonge\n    cible: S75-A018""": """relations:\n  - type: prolonge\n    cible: S75-A006\n    note: \"Prolonge la question de la nomination, de Stiff Kittens à Warsaw puis Joy Division.\"\n  - type: annonce\n    cible: S75-A018\n    note: \"Annonce la controverse visuelle et éthique de *An Ideal for Living*.\"\n  - type: signale_candidat\n    cible: MYTH-Warsaw-cover-up\n    note: \"Mythe optionnel à créer seulement si la thèse d'une justification a posteriori apparaît dans plusieurs sources.\""" ,

    # S75-A018 — An Ideal For Living.
    """relations:\n  - type: prolonge\n    cible: S75-A016\n  - type: prolonge\n    cible: S75-A017\n  - type: nuance\n    cible: MYTH-fascination_fasciste""": """relations:\n  - type: prolonge\n    cible: S75-A016\n    note: \"Prolonge l’ambiguïté Hess / Electric Circus dans l’objet *An Ideal for Living*.\"\n  - type: prolonge\n    cible: S75-A017\n    note: \"Relie le choix du nom Joy Division à l’imagerie litigieuse de l’EP.\"\n  - type: corrobore\n    cible: S74-A024\n    note: \"Recoupe l’atome S74 sur *An Ideal for Living* comme objet visuel litigieux.\"\n  - type: signale_candidat\n    cible: MYTH-imagerie-nazie-comme-fascination-fasciste\n    note: \"Mythe à créer pour éviter à la fois l'excuse romantique et la condamnation non contextualisée.\""" ,

    # S75-A019 — matérialité / contrainte productive.
    """relations:\n  - type: prolonge\n    cible: S75-A018\n  - type: illustre\n    cible: CONCEPT-contrainte_produit_la_forme""": """relations:\n  - type: prolonge\n    cible: S75-A018\n    note: \"Déplace la controverse visuelle vers la matérialité discographique de l’EP.\"\n  - type: illustre\n    cible: S75-A009\n    note: \"Illustre par le pressage et le remastering la contrainte déjà observable dans les démos.\"\n  - type: signale_candidat\n    cible: CONCEPT-contrainte-productive\n    note: \"Concept à créer : la contrainte matérielle produit ou révèle la forme.\"\n  - type: signale_candidat\n    cible: CONCEPT-matérialité-discographique\n    note: \"Concept à créer si les supports, pressages et éditions deviennent un axe transversal.\""" ,

    # S75-A020 — No Love Lost.
    """relations:\n  - type: prolonge\n    cible: S75-A015\n  - type: nuance\n    cible: S75-A019\n  - type: annonce\n    cible: CONCEPT-architecture_sonore""": """relations:\n  - type: prolonge\n    cible: S75-A015\n    note: \"Fait de la précision de Morris une condition du seuil « No Love Lost ».\"\n  - type: nuance\n    cible: S75-A019\n    note: \"Le mauvais support discographique masque partiellement un seuil musical déjà présent.\"\n  - type: signale_candidat\n    cible: CONCEPT-architecture-sonore\n    note: \"Concept à créer pour formaliser le passage du punk à l'organisation sonore Joy Division.\"\n  - type: signale_registre\n    cible: SONG-No-Love-Lost\n    note: \"Créer une entrée chanson si le registre des chansons doit exploiter ce seuil.\""" ,
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
            text = text.replace(old, new, 1)
            changed += 1
        else:
            missing.append(old.splitlines()[0:3])

    TARGET.write_text(text, encoding="utf-8")

    print(f"S75 relation stabilization applied: {changed} replacement(s).")
    if missing:
        print(f"WARNING: {len(missing)} expected block(s) not found.")
        for block in missing:
            print("---")
            print("\n".join(block))
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
