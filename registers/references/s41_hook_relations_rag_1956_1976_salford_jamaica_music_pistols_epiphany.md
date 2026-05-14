# S41 — Relations stabilisées et entrées RAG — Salford, Jamaïque, premières écoutes et épiphanie Sex Pistols

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A007-CONCEPT-044
    source: S41-A007
    type: prolonge
    cible: CONCEPT-044
    justification: >
      Hook construit Salford comme texture visuelle et affective de l’enfance : brun, smog, logement ouvrier et violence familiale.

  - id: REL-S41-A008-CONCEPT-045
    source: S41-A008
    type: prolonge
    cible: CONCEPT-045
    justification: >
      La Jamaïque constitue une mobilité ouvrière contrariée : confort, couleur, instabilité puis retour perdant à Salford.

  - id: REL-S41-A009-ORIGINE-HOOK-SUMNER
    source: S41-A009
    type: prépare
    cible: RELATION-HOOK-SUMNER
    justification: >
      La rencontre scolaire précède la formation musicale et installe une alliance sociale antérieure au punk.

  - id: REL-S41-A010-CONCEPT-044
    source: S41-A010
    type: prolonge
    cible: CONCEPT-044
    justification: >
      Le vol et la scally attitude prolongent Salford comme matrice pratique, pas seulement décorative.

  - id: REL-S41-A011-CONCEPT-047
    source: S41-A011
    type: prolonge
    cible: CONCEPT-047
    justification: >
      Le Lesser Free Trade Hall est désacralisé par une mémoire antérieure d’ivresse ouvrière.

  - id: REL-S41-A012-REGISTRE-INFLUENCES-MUSICALES
    source: S41-A012
    type: alimente
    cible: REGISTRE-INFLUENCES-MUSICALES
    justification: >
      Cockney Rebel et « Sebastian » apparaissent comme gateway musical avant la rupture punk.

  - id: REL-S41-A013-CONCEPT-046
    source: S41-A013
    type: prolonge
    cible: CONCEPT-046
    justification: >
      Les Sex Pistols rendent la musique praticable parce qu’ils paraissent socialement semblables à Hook.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A007
    source_id: S41
    atom_id: S41-A007
    title: "Salford brun et smoggy"
    chapters:
      - Chapitre 2
      - Chapitre 13
    tags:
      - salford
      - childhood
      - smog
      - working-class
      - control
    query_boost:
      - "dark and smoggy and brown wet cardboard box"
      - "Peter Hook Salford childhood Control black and white"
    use_for:
      - géographie émotionnelle
      - mémoire ouvrière
      - origine sociale de Hook
    avoid_for:
      - déterminisme sonore direct

  - id: RAG-S41-A008
    source_id: S41
    atom_id: S41-A008
    title: "Jamaïque en couleur et retour perdant à Salford"
    chapters:
      - Chapitre 2
      - Chapitre 13
    tags:
      - jamaica
      - salford
      - colour
      - return
      - mobility
    query_boost:
      - "Well in Jamaica it was definitely in colour"
      - "Peter Hook Jamaica Salford return 1966"
    use_for:
      - contraste biographique
      - mobilité ouvrière contrariée
    avoid_for:
      - influence musicale directe non prouvée

  - id: RAG-S41-A010
    source_id: S41
    atom_id: S41-A010
    title: "Vol, classe et scally attitude"
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - theft
      - salford
      - scally
      - working-class
      - backstage
    query_boost:
      - "You never had anything so you took it"
      - "Joy Division arty intellectual image working class thieves"
    use_for:
      - décalage image arty / pratiques de classe
      - sociologie du groupe
    avoid_for:
      - romantisation de la délinquance

  - id: RAG-S41-A012
    source_id: S41
    atom_id: S41-A012
    title: "Sebastian comme gateway musical"
    chapters:
      - Chapitre 2
      - Chapitre 11
    tags:
      - cockney-rebel
      - sebastian
      - radio-luxembourg
      - steve-harley
      - pop
    query_boost:
      - "They became my gateway to music"
      - "Sebastian Cockney Rebel Peter Hook Radio Luxembourg Rhyl"
    use_for:
      - influences musicales pré-punk
      - rituel d’écoute
    avoid_for:
      - influence formelle unique

  - id: RAG-S41-A013
    source_id: S41
    atom_id: S41-A013
    title: "Sex Pistols comme permission de classe"
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - sex-pistols
      - melody-maker
      - newquay
      - working-class
      - punk
    query_boost:
      - "they looked like working-class tossers too"
      - "I have got to see this lot"
      - "Sex Pistols possibility working class Peter Hook"
    use_for:
      - révélation punk
      - classe et permission d’agir
    avoid_for:
      - réduction du punk à la seule classe
```
