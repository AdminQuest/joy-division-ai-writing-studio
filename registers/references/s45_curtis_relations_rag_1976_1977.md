# S45 — Relations stabilisées et entrées RAG — formation 1976-1977

Ce fichier consolide les relations et l’indexation RAG du passage atomisé dans `sources/curtis_touching_from_a_distance/source_part_1976_1977_formation.md`.

---

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A021-MYTH-006
    source: S45-A021
    type: nuance
    cible: MYTH-006
    justification: >
      L’annonce « Rusty » montre une phase pré-groupe fragile ; elle contredit la
      projection d’un génie immédiatement constitué.

  - id: REL-S45-A022-MYTH-001
    source: S45-A022
    type: nuance
    cible: MYTH-001
    justification: >
      Le second concert des Sex Pistols agit comme confirmation et autorisation,
      non comme origine absolue.

  - id: REL-S45-A022-MOTIF-011
    source: S45-A022
    type: prolonge
    cible: MOTIF-011
    justification: >
      Le concert donne à Curtis une autorisation punk : la scène devient accessible
      sans virtuosité préalable.

  - id: REL-S45-A023-CONCEPT-auto-habilitation-artistique
    source: S45-A023
    type: prolonge
    cible: CONCEPT-auto-habilitation-artistique
    justification: >
      Mont de Marsan est lu par Deborah comme élément d’une stratégie de carrière
      fantasmée, avant toute compétence stabilisée.

  - id: REL-S45-A024-S45-A028
    source: S45-A024
    type: prépare
    cible: S45-A028
    justification: >
      Le concert d’Iggy Pop rend concret le réseau Hook / Mason qui prépare le
      recrutement par affinité.

  - id: REL-S45-A025-CONCEPT-012
    source: S45-A025
    type: prépare
    cible: CONCEPT-012
    justification: >
      Barton Street devient l’espace domestique où le travail d’écriture se matérialise.

  - id: REL-S45-A026-MOTIF-009
    source: S45-A026
    type: prolonge
    cible: MOTIF-009
    justification: >
      L’épisode raciste rapporté et la veste « HATE » renforcent le motif de
      contradiction biographique.

  - id: REL-S45-A026-CONCEPT-004
    source: S45-A026
    type: requiert
    cible: CONCEPT-004
    justification: >
      Le passage exige prudence, recoupement et refus d’un portrait moral totalisant.

  - id: REL-S45-A027-CONCEPT-004
    source: S45-A027
    type: requiert
    cible: CONCEPT-004
    justification: >
      La scène de violence domestique rapportée doit être utilisée sans voyeurisme
      ni causalité rétrospective.

  - id: REL-S45-A028-MOTIF-007
    source: S45-A028
    type: prolonge
    cible: MOTIF-007
    justification: >
      Le recrutement repose sur une logique d’affinité et de sociabilité de groupe.

  - id: REL-S45-A029-S45-A021
    source: S45-A029
    type: prolonge
    cible: S45-A021
    justification: >
      Iain Gray est le premier répondant de la phase « Rusty », puis devient
      dommage collatéral du passage vers Warsaw.

  - id: REL-S45-A030-CONCEPT-012
    source: S45-A030
    type: prolonge
    cible: CONCEPT-012
    justification: >
      La blue room de Barton Street concrétise la domesticité productive comme
      dispositif d’écriture.

  - id: REL-S45-A031-MYTH-003
    source: S45-A031
    type: nuance
    cible: MYTH-003
    justification: >
      Manchester est présenté comme milieu d’auto-habilitation, mais ne doit pas
      redevenir matrice unique et mécanique.

  - id: REL-S45-A032-MYTH-006
    source: S45-A032
    type: nuance
    cible: MYTH-006
    justification: >
      Morley et Deborah Curtis documentent une différence encore inachevée, non
      une esthétique déjà parfaite.

  - id: REL-S45-A033-S45-A034
    source: S45-A033
    type: prépare
    cible: S45-A034
    justification: >
      L’instabilité des batteurs et l’incompatibilité Brotherdale rendent lisible
      l’arrivée de Morris comme seuil de stabilisation.

  - id: REL-S45-A034-MOTIF-006
    source: S45-A034
    type: prolonge
    cible: MOTIF-006
    justification: >
      Stephen Morris est un seuil humain et musical : Warsaw devient enfin une
      formation complète.
```

---

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A022
    source_id: S45
    atom_id: S45-A022
    title: Le second Lesser Free Trade Hall comme confirmation
    chapters:
      - Chapitre 2
    tags:
      - deborah-curtis
      - sex-pistols
      - lesser-free-trade-hall
      - autorisation-punk
      - mythe-fondateur
      - teleologie
    query_boost:
      - "Deborah Curtis Lesser Free Trade Hall 20 July 1976"
      - "There weren’t as many people there as history would claim"
      - "Sex Pistols confirmation Ian Curtis"
    use_for:
      - nuancer le mythe du concert fondateur
      - montrer le punk comme autorisation
      - cadrer le chapitre 2
    avoid_for:
      - origine absolue de Joy Division
      - preuve d’un génie immédiat

  - id: RAG-S45-A030
    source_id: S45
    atom_id: S45-A030
    title: La blue room de Barton Street comme atelier domestique d’écriture
    chapters:
      - Chapitre 2
      - Chapitre 4
    tags:
      - deborah-curtis
      - barton-street
      - blue-room
      - ecriture
      - domesticite-productive
      - ian-curtis
    query_boost:
      - "Most nights Ian would go into the blue room"
      - "Barton Street blue room Ian Curtis writing"
      - "Deborah Curtis song-writing room"
    use_for:
      - matérialiser l’écriture de Curtis
      - éviter la lecture purement prophétique des textes
      - relier domesticité et processus créatif
    avoid_for:
      - sanctuarisation de Barton Street
      - causalité domestique totale

  - id: RAG-S45-A031
    source_id: S45
    atom_id: S45-A031
    title: Manchester comme nouvelle capitale et scène d’auto-habilitation
    chapters:
      - Chapitre 1
      - Chapitre 2
    tags:
      - manchester
      - anti-londres
      - paul-morley
      - out-there
      - scene-locale
      - auto-habilitation
    query_boost:
      - "Manchester was set to become the new capital"
      - "Paul Morley Out There Manchester scene"
      - "Ranch Bar Stevenson Square Buzzcocks Worst"
    use_for:
      - montrer Manchester comme scène active
      - cadrer l’anti-Londres
      - relier chapitre 1 et chapitre 2
    avoid_for:
      - Manchester comme matrice unique
      - nostalgie de scène non critique

  - id: RAG-S45-A034
    source_id: S45
    atom_id: S45-A034
    title: Stephen Morris comme pièce manquante de Warsaw
    chapters:
      - Chapitre 2
    tags:
      - stephen-morris
      - warsaw
      - recrutement
      - stabilisation
      - batteur
      - famille
    query_boost:
      - "missing piece of the Warsaw jigsaw"
      - "Warsaw became a complete family"
      - "Stephen Morris Jones Music Store Deborah Curtis"
    use_for:
      - démontrer la stabilisation humaine et musicale
      - articuler arrivée de Morris et seuil Joy Division
    avoid_for:
      - récit purement technique du batteur
```

---

## Formulations contrôlées

```yaml
formulations_autorisees:
  - "Le second concert des Sex Pistols confirme à Curtis que la scène devient possible ; il ne constitue pas, à lui seul, l’origine absolue de Joy Division."
  - "Barton Street matérialise l’écriture de Curtis : la chambre bleue est un atelier domestique, non un sanctuaire prophétique."
  - "Manchester se donne alors les rôles nécessaires à sa propre scène : musiciens, fanzines, critiques, photographes et producteurs."
  - "L’arrivée de Stephen Morris stabilise Warsaw humainement autant que musicalement."

formulations_a_proscrire_sans_source_complementaire:
  - "Joy Division naît directement du concert des Sex Pistols."
  - "Curtis sait déjà exactement ce qu’il va devenir en 1976."
  - "Barton Street explique les textes de Curtis."
  - "Manchester est la cause totale du son Joy Division."
  - "Morris apporte seulement une compétence technique."
```
