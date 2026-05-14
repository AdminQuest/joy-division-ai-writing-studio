# S41 — Relations stabilisées et entrées RAG — Lesser Free Trade Hall, basse, scène punk et recrutement de Curtis

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A014-CONCEPT-048
    source: S41-A014
    type: prolonge
    cible: CONCEPT-048
    justification: >
      Le concert des Sex Pistols agit comme catalyseur d’une décision déjà préparée par la classe, la presse et les premières écoutes.

  - id: REL-S41-A015-CONCEPT-049
    source: S41-A015
    type: prolonge
    cible: CONCEPT-049
    justification: >
      L’achat de la basse naît d’une règle punk et d’un hasard matériel plutôt que d’un projet de virtuosité.

  - id: REL-S41-A016-CONCEPT-049
    source: S41-A016
    type: prolonge
    cible: CONCEPT-049
    justification: >
      Le jeu mélodique de Hook est relu par lui comme conséquence d’un apprentissage imparfait.

  - id: REL-S41-A017-CONCEPT-046
    source: S41-A017
    type: prolonge
    cible: CONCEPT-046
    justification: >
      Le punk devient permission sociale par la visibilité corporelle et la provocation de rue.

  - id: REL-S41-A018-CONCEPT-050
    source: S41-A018
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Le deuxième concert des Pistols montre que l’effet punk passe par lieux, groupes, rivalités et supports.

  - id: REL-S41-A019-CONCEPT-051
    source: S41-A019
    type: prolonge
    cible: CONCEPT-051
    justification: >
      Curtis apparaît comme jeune punk ordinaire et intense, avant sa cristallisation mythique.

  - id: REL-S41-A020-S41-A019
    source: S41-A020
    type: prolonge
    cible: S41-A019
    justification: >
      Le semblable aperçu à l’Electric Circus devient chanteur par convergence de besoins de groupe.

  - id: REL-S41-A021-CONCEPT-050
    source: S41-A021
    type: nuance
    cible: CONCEPT-050
    justification: >
      La violence du dernier concert Pistols révèle aussi la limite interne de l’écosystème punk.

  - id: REL-S41-A022-CONCEPT-050
    source: S41-A022
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Terry Mason rend visible l’infrastructure amicale, technique et logistique autour du groupe.

  - id: REL-S41-A023-CONCEPT-020
    source: S41-A023
    type: prolonge
    cible: CONCEPT-020
    justification: >
      Hook distingue ses propres paroles fonctionnelles de l’intensité perçue des textes de Curtis.

  - id: REL-S41-A024-CONCEPT-052
    source: S41-A024
    type: prolonge
    cible: CONCEPT-052
    justification: >
      Hook propose une lecture rétrospective de Curtis comme être aux personas multiples.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A014
    source_id: S41
    atom_id: S41-A014
    title: "Lesser Free Trade Hall : conversion punk"
    chapters:
      - Chapitre 2
      - Chapitre 6
      - Chapitre 14
    tags:
      - lesser-free-trade-hall
      - sex-pistols
      - johnny-rotten
      - malcolm-mclaren
      - punk-epiphany
    query_boost:
      - "I could do that"
      - "I fucking need to do that"
      - "Lesser Free Trade Hall Peter Hook Sex Pistols conversion"
    use_for:
      - catalyseur punk
      - origine non absolue
      - permission sociale
    avoid_for:
      - origine unique du post-punk mancunien

  - id: RAG-S41-A015
    source_id: S41
    atom_id: S41-A015
    title: "Achat de la première basse chez Mazel"
    chapters:
      - Chapitre 2
      - Chapitre 3
    tags:
      - peter-hook
      - bass
      - mazel
      - gibson-eb0-copy
      - black-bin-liner
    query_boost:
      - "Is that a bass guitar"
      - "Mazel Gibson EB-0 copy black bin liner"
    use_for:
      - origine instrumentale de Hook
      - hasard matériel
    avoid_for:
      - vocation instrumentale précoce

  - id: RAG-S41-A016
    source_id: S41
    atom_id: S41-A016
    title: "Apprendre faux : trois doigts et Tippex"
    chapters:
      - Chapitre 3
    tags:
      - bass-style
      - three-fingers
      - tippex
      - palmer-hughes
      - melodic-bass
    query_boost:
      - "it came through learning badly"
      - "three-fingered bass player Tippex stickers"
    use_for:
      - genèse du style de basse
      - erreur productive
    avoid_for:
      - causalité unique du son

  - id: RAG-S41-A019
    source_id: S41
    atom_id: S41-A019
    title: "Curtis avec Hate sur son manteau"
    chapters:
      - Chapitre 2
      - Chapitre 6
      - Chapitre 14
    tags:
      - ian-curtis
      - hate-coat
      - electric-circus
      - pre-myth
      - punk
    query_boost:
      - "He was just a kid with Hate on his coat"
      - "Ian Curtis Hate coat Electric Circus Peter Hook"
    use_for:
      - Curtis pré-mythique
      - rencontre fondatrice
    avoid_for:
      - prophétie psychologique

  - id: RAG-S41-A020
    source_id: S41
    atom_id: S41-A020
    title: "Recruter Curtis comme chanteur"
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - ian-curtis
      - recruitment
      - singer
      - ashworth-valley
      - warsaw
    query_boost:
      - "Well, come in with us, then. You can sing for us"
      - "Ian Curtis joins Warsaw Ashworth Valley"
    use_for:
      - recrutement de Curtis
      - convergence des groupes
    avoid_for:
      - version unique non croisée

  - id: RAG-S41-A023
    source_id: S41
    atom_id: S41-A023
    title: "Premières répétitions, WEM PA et paroles de Curtis"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 6
    tags:
      - rehearsals
      - wem-pa
      - lyrics
      - ian-curtis
      - early-songs
    query_boost:
      - "he wasn’t playing at being in a band"
      - "WEM PA Big Alex rehearsal rooms Ian Curtis lyrics"
    use_for:
      - processus créatif initial
      - paroles de Curtis
      - précarité des répétitions
    avoid_for:
      - mythification pure de Curtis

  - id: RAG-S41-A024
    source_id: S41
    atom_id: S41-A024
    title: "Trop d’Ians : plasticité relationnelle de Curtis"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - ian-curtis
      - personas
      - people-pleaser
      - marriage
      - band-life
    query_boost:
      - "There were just too many Ians to cope with"
      - "Ian Curtis people pleaser three personas Hook"
    use_for:
      - plasticité relationnelle
      - prudence psychologique
    avoid_for:
      - diagnostic rétrospectif
```
