# S41 — Relations stabilisées et entrées RAG — Peel, Factory vs Genetic, Eden Studios

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A104-CONCEPT-090
    source: S41-A104
    type: prolonge
    cible: CONCEPT-090
    justification: >
      La charge de Hook comme chauffeur et porteur révèle le travail logistique invisible qui soutient les concerts.

  - id: REL-S41-A105-CONCEPT-091
    source: S41-A105
    type: prolonge
    cible: CONCEPT-091
    justification: >
      Le groupe connaît l’épilepsie de Curtis mais ne ralentit pas, Hook parlant explicitement d’une stratégie d’évitement collectif.

  - id: REL-S41-A106-CONCEPT-091
    source: S41-A106
    type: prolonge
    cible: CONCEPT-091
    justification: >
      Le management à plein temps de Gretton multiplie les opportunités et accélère le calendrier dans un contexte médical fragile.

  - id: REL-S41-A107-CONCEPT-092
    source: S41-A107
    type: prolonge
    cible: CONCEPT-092
    justification: >
      La Peel Session agit comme validation radiophonique alternative, distincte d’un succès commercial classique.

  - id: REL-S41-A108-CONCEPT-093
    source: S41-A108
    type: prolonge
    cible: CONCEPT-093
    justification: >
      Les références Kraftwerk et Velvet Underground sont métabolisées dans des morceaux qui finissent par sonner comme Joy Division.

  - id: REL-S41-A109-CONCEPT-094
    source: S41-A109
    type: prolonge
    cible: CONCEPT-094
    justification: >
      Curtis transforme les fragments de jam en chansons au sein d’un processus oral, peu archivé et fondé sur la mémoire collective.

  - id: REL-S41-A110-CONCEPT-095
    source: S41-A110
    type: prolonge
    cible: CONCEPT-095
    justification: >
      Hook rappelle que la voix de Curtis est d’abord entendue comme cri et intensité, avant d’être analysée comme texte.

  - id: REL-S41-A111-CONCEPT-096
    source: S41-A111
    type: prolonge
    cible: CONCEPT-096
    justification: >
      Le choix Factory donne liberté et partage favorable mais maintient le groupe au travail, donc sans repos pour Curtis.

  - id: REL-S41-A112-CONCEPT-097
    source: S41-A112
    type: prolonge
    cible: CONCEPT-097
    justification: >
      Les démos Eden ouvrent une voie Rushent / Genetic alternative, plus lisible mais moins fondatrice que Hannett selon Hook.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A105
    source_id: S41
    atom_id: S41-A105
    title: "Fatigue collective et déni de l’épilepsie"
    chapters:
      - Chapitre 12
      - Chapitre 6
    tags:
      - epilepsy
      - fatigue
      - carried-on
      - peter-hook
      - ian-curtis
    query_boost:
      - "we buried our heads in the sand"
      - "Peter's fell off his chair again epilepsy carried on"
    use_for:
      - accélération malgré maladie
      - responsabilité organisationnelle du groupe
    avoid_for:
      - jugement moral anachronique

  - id: RAG-S41-A107
    source_id: S41
    atom_id: S41-A107
    title: "John Peel Session comme validation alternative"
    chapters:
      - Chapitre 6
      - Chapitre 8
      - Chapitre 14
    tags:
      - john-peel
      - bbc
      - peel-session
      - radio
      - post-punk
    query_boost:
      - "that was like getting a chart placing back then only better"
      - "John Peel likes the record He wants us in for a session"
    use_for:
      - légitimation radio
      - infrastructure alternative britannique
    avoid_for:
      - succès mainstream

  - id: RAG-S41-A108
    source_id: S41
    atom_id: S41-A108
    title: "T. J. Davidson’s : influence métabolisée"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 6
    tags:
      - tj-davidsons
      - kraftwerk
      - digital
      - shadowplay
      - velvet-underground
    query_boost:
      - "That was the art It sounded like Joy Division"
      - "Kraftwerk Digital Ocean Shadowplay"
    use_for:
      - processus créatif collectif
      - métabolisation des influences
    avoid_for:
      - réduction des chansons à leurs modèles

  - id: RAG-S41-A109
    source_id: S41
    atom_id: S41-A109
    title: "Ian Curtis conducteur de fragments"
    chapters:
      - Chapitre 3
      - Chapitre 10
      - Chapitre 12
    tags:
      - ian-curtis
      - songwriting
      - conductor
      - memory
      - new-order
    query_boost:
      - "He stood there like a conductor and picked out the best bits"
      - "great car that had only three wheels"
    use_for:
      - Curtis arrangeur oral
      - composition collective sans archive
    avoid_for:
      - héroïsation de Curtis seul

  - id: RAG-S41-A110
    source_id: S41
    atom_id: S41-A110
    title: "La voix de Curtis avant les paroles"
    chapters:
      - Chapitre 4
      - Chapitre 12
    tags:
      - ian-curtis
      - voice
      - lyrics
      - scream
      - unknown-pleasures
      - closer
    query_boost:
      - "for two years in the rehearsal room all I really heard was a scream"
      - "I could hear and begin to take notice of the words"
    use_for:
      - voix comme intensité
      - écoute différée des paroles
    avoid_for:
      - opposition simpliste texte / voix

  - id: RAG-S41-A111
    source_id: S41
    atom_id: S41-A111
    title: "Factory vs Genetic : liberté sans repos"
    chapters:
      - Chapitre 8
      - Chapitre 12
      - Chapitre 6
    tags:
      - factory
      - genetic
      - radar
      - stiff
      - advance
      - epilepsy
    query_boost:
      - "London plus advance and small profit split or Manchester with no advance but great profit split"
      - "Genetic 70000 advance Factory no advance"
    use_for:
      - choix industriel Factory
      - coût sanitaire du refus d’avance
    avoid_for:
      - idéalisation Factory

  - id: RAG-S41-A112
    source_id: S41
    atom_id: S41-A112
    title: "Eden Studios : voie Rushent non retenue"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - martin-rushent
      - eden-studios
      - genetic
      - demos
      - hannett
    query_boost:
      - "he was nowhere near as exciting or unpredictable"
      - "Eden Studios Glass Transmission Ice Age Insight Digital"
    use_for:
      - alternative à Hannett
      - Genetic / Rushent
    avoid_for:
      - Rushent comme simple impasse
```
