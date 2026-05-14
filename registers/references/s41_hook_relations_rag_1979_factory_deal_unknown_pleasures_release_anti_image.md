# S41 — Relations stabilisées et entrées RAG — Factory deal, *Unknown Pleasures*, anti-image

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A113-CONCEPT-098
    source: S41-A113
    type: prolonge
    cible: CONCEPT-098
    justification: >
      Le choix Factory donne liberté et partage favorable, mais maintient le groupe dans le travail salarié et la pression d’un grand disque.

  - id: REL-S41-A114-CONCEPT-099
    source: S41-A114
    type: prépare
    cible: CONCEPT-099
    justification: >
      Bowdon Vale montre un groupe live déjà constitué avant la transformation studio d’Unknown Pleasures.

  - id: REL-S41-A115-CONCEPT-090
    source: S41-A115
    type: prolonge
    cible: CONCEPT-090
    justification: >
      La panne de Walthamstow rend visible le coût matériel et conflictuel du van dans l’économie indépendante.

  - id: REL-S41-A116-CONCEPT-099
    source: S41-A116
    type: prolonge
    cible: CONCEPT-099
    justification: >
      Strawberry est présenté comme lieu d’enthousiasme et de haute technologie, mais prépare la tension entre plaisir de session et transformation du son.

  - id: REL-S41-A117-CONCEPT-100
    source: S41-A117
    type: prolonge
    cible: CONCEPT-100
    justification: >
      Hook distingue les seize titres enregistrés des dix titres retenus pour l’album, ouvrant une logique de chutes productives.

  - id: REL-S41-A118-CONCEPT-077
    source: S41-A118
    type: prolonge
    cible: CONCEPT-077
    justification: >
      Hannett construit le son depuis la control room, dans une asymétrie de savoir déjà repérée à Cargo.

  - id: REL-S41-A119-CONCEPT-099
    source: S41-A119
    type: prolonge
    cible: CONCEPT-099
    justification: >
      Hook et Sumner regrettent d’abord la perte du son live, avant de reconnaître la vérité studio produite par Hannett.

  - id: REL-S41-A120-CONCEPT-101
    source: S41-A120
    type: prolonge
    cible: CONCEPT-101
    justification: >
      Le refus du portrait rock et l’anti-image froide structurent la présentation visuelle d’Unknown Pleasures.

  - id: REL-S41-A121-CONCEPT-101
    source: S41-A121
    type: prolonge
    cible: CONCEPT-101
    justification: >
      Le silence imposé par Gretton prolonge l’anti-image dans la stratégie médiatique.

  - id: REL-S41-A122-CONCEPT-102
    source: S41-A122
    type: prolonge
    cible: CONCEPT-102
    justification: >
      Les 10 000 copies d’Unknown Pleasures deviennent charge matérielle avant d’être objet canonique.

  - id: REL-S41-A123-S41-A113
    source: S41-A123
    type: consolide
    cible: S41-A113
    justification: >
      La bonne réception critique et les ventes progressives montrent que le pari économique Factory finit par fonctionner.

  - id: REL-S41-A124-CONCEPT-103
    source: S41-A124
    type: prolonge
    cible: CONCEPT-103
    justification: >
      La session Piccadilly Radio fait apparaître les formes en devenir de « Chance » / « Atmosphere » et « Atrocity Exhibition ».

  - id: REL-S41-A125-CONCEPT-104
    source: S41-A125
    type: prolonge
    cible: CONCEPT-104
    justification: >
      La naissance de Natalie et la politique no-girlfriends rendent visible la séparation entre vie familiale et vie du groupe.

  - id: REL-S41-A126-CONCEPT-103
    source: S41-A126
    type: prolonge
    cible: CONCEPT-103
    justification: >
      « Transmission » devient single hors album par puissance live, selon une logique Factory non classique.

  - id: REL-S41-A127-CONCEPT-093
    source: S41-A127
    type: prolonge
    cible: CONCEPT-093
    justification: >
      Le synthétiseur passe de l’expérimentation Hannett à l’outil de composition du groupe.

  - id: REL-S41-A128-S41-A121
    source: S41-A128
    type: prolonge
    cible: S41-A121
    justification: >
      L’hostilité aux interviews et la pauvreté persistante prolongent la stratégie médiatique de retrait.

  - id: REL-S41-A129-CONCEPT-087
    source: S41-A129
    type: prolonge
    cible: CONCEPT-087
    justification: >
      L’apparition What’s On de « She’s Lost Control » confirme la télévision comme espace de contrainte autant que de visibilité.

  - id: REL-S41-A130-CONCEPT-064
    source: S41-A130
    type: prolonge
    cible: CONCEPT-064
    justification: >
      T. J. Davidson’s reste lieu de continuité, de farce et d’identité même après les premiers succès.

  - id: REL-S41-A131-CONCEPT-090
    source: S41-A131
    type: prolonge
    cible: CONCEPT-090
    justification: >
      La rencontre Hook / Les Pattinson élargit le motif du bassiste-chauffeur à une fraternité logistique post-punk.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A113
    source_id: S41
    atom_id: S41-A113
    title: "Factory choisi : indépendance sans sécurité"
    chapters:
      - Chapitre 8
      - Chapitre 12
    tags:
      - factory
      - genetic
      - no-advance
      - profit-split
      - unknown-pleasures
    query_boost:
      - "Manchester with no advance but great profit split"
      - "Factory deal no advance day jobs Unknown Pleasures"
    use_for:
      - choix Factory
      - coût salarial et sanitaire de l’indépendance
    avoid_for:
      - idéalisation Factory

  - id: RAG-S41-A116
    source_id: S41
    atom_id: S41-A116
    title: "Strawberry Studios : Unknown Pleasures sans éléphant"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - strawberry-studios
      - unknown-pleasures
      - 10cc
      - martin-hannett
      - twenty-four-track
    query_boost:
      - "There was no elephant on Unknown Pleasures"
      - "Strawberry Studios Stockport first foray into twenty-four-track"
    use_for:
      - mémoire de session heureuse
      - studio du Nord-Ouest
    avoid_for:
      - effacement des tensions sonores

  - id: RAG-S41-A117
    source_id: S41
    atom_id: S41-A117
    title: "Unknown Pleasures : seize titres, dix retenus"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - unknown-pleasures
      - sixteen-tracks
      - earcom-2
      - still
      - sessionography
    query_boost:
      - "Of those we recorded sixteen ten of which were used on the album"
      - "Autosuggestion From Safety to Where Exercise One The Only Mistake"
    use_for:
      - album comme sélection
      - chutes productives
    avoid_for:
      - confusion session / album

  - id: RAG-S41-A119
    source_id: S41
    atom_id: S41-A119
    title: "Unknown Pleasures : vérité live contre vérité studio"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - unknown-pleasures
      - live-sound
      - hannett
      - hook
      - sumner
    query_boost:
      - "Why is my guitar so quiet"
      - "we wanted to sound like the Sex Pistols Unknown Pleasures"
    use_for:
      - réception interne de l’album
      - tension Hannett / groupe
    avoid_for:
      - condamnation durable du son

  - id: RAG-S41-A120
    source_id: S41
    atom_id: S41-A120
    title: "Unknown Pleasures : anti-image froide"
    chapters:
      - Chapitre 5
      - Chapitre 8
      - Chapitre 14
    tags:
      - unknown-pleasures-cover
      - peter-saville
      - anti-image
      - anonymity
      - grey
    query_boost:
      - "We didn’t want it to be about us"
      - "anti-image anonymity chilly grey buttoned-up against the cold"
    use_for:
      - esthétique visuelle Joy Division
      - anti-portrait rock
    avoid_for:
      - stratégie consciente totale

  - id: RAG-S41-A122
    source_id: S41
    atom_id: S41-A122
    title: "10 000 copies d’Unknown Pleasures dans l’escalier"
    chapters:
      - Chapitre 8
      - Chapitre 14
    tags:
      - unknown-pleasures
      - palatine-road
      - 10000-copies
      - distribution
      - factory
    query_boost:
      - "carried 10000 copies of Unknown Pleasures up the stairs"
      - "Palatine Road 10000 copies Unknown Pleasures"
    use_for:
      - matérialité de l’objet culte
      - distribution indépendante
    avoid_for:
      - quantification non croisée des profits

  - id: RAG-S41-A124
    source_id: S41
    atom_id: S41-A124
    title: "Piccadilly Radio : Chance avant Atmosphere"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 8
    tags:
      - piccadilly-radio
      - chance
      - atmosphere
      - atrocity-exhibition
      - woolworths-organ
    query_boost:
      - "Chance improved a lot when we re-recorded it"
      - "Piccadilly Radio first version of Atmosphere Chance"
    use_for:
      - transition vers Closer
      - versions préliminaires
    avoid_for:
      - confusion versions radio / Sordide / Closer

  - id: RAG-S41-A126
    source_id: S41
    atom_id: S41-A126
    title: "Transmission : single hors album choisi par puissance live"
    chapters:
      - Chapitre 4
      - Chapitre 8
      - Chapitre 14
    tags:
      - transmission
      - mayflower
      - factory-way
      - single
      - digital
      - disorder
    query_boost:
      - "we had something a bit special on our hands"
      - "Digital Disorder Transmission Factory way"
    use_for:
      - stratégie singles Factory
      - puissance live de Transmission
    avoid_for:
      - uchronie commerciale prise comme certitude

  - id: RAG-S41-A129
    source_id: S41
    atom_id: S41-A129
    title: "What’s On : She’s Lost Control sous contrainte TV"
    chapters:
      - Chapitre 5
      - Chapitre 14
    tags:
      - whats-on
      - granada
      - shes-lost-control
      - television
      - blue-shirt
    query_boost:
      - "slightly nervy and shell-shocked performance"
      - "What’s On She’s Lost Control end credits"
    use_for:
      - télévision comme contrainte
      - archive audiovisuelle
    avoid_for:
      - consécration télévisuelle simple

  - id: RAG-S41-A131
    source_id: S41
    atom_id: S41-A131
    title: "Hook et Les Pattinson : bassistes chauffeurs"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - les-pattinson
      - echo-and-the-bunnymen
      - bass-player
      - van-driver
      - ymca
    query_boost:
      - "both of us the bass player and van driver for our bands"
      - "Hook Les Pattinson van driver bass player"
    use_for:
      - fraternité logistique post-punk
      - économie des groupes émergents
    avoid_for:
      - anecdote surchargée
```
