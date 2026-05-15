# S41 — Relations stabilisées et entrées RAG — Timeline Four fin 1979, Europe, Annik, « We carried on »

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A166-CONCEPT-129
    source: S41-A166
    type: prolonge
    cible: CONCEPT-129
    justification: >
      La tournée Buzzcocks montre une variation volontaire des setlists et l’usage du répertoire comme outil de défi scénique.

  - id: REL-S41-A167-CONCEPT-129
    source: S41-A167
    type: prolonge
    cible: CONCEPT-129
    justification: >
      L’Electric Ballroom explicite l’ethos de contrariété : ne pas jouer le jeu attendu, hérité du punk, de Factory et de Throbbing Gristle.

  - id: REL-S41-A168-CONCEPT-130
    source: S41-A168
    type: prolonge
    cible: CONCEPT-130
    justification: >
      Corbijn relie la photographie de 1979 à la mémoire cinématographique de Control.

  - id: REL-S41-A169-CONCEPT-131
    source: S41-A169
    type: prolonge
    cible: CONCEPT-131
    justification: >
      Bournemouth interrompt le set et annule Cardiff, mais la tournée reprend ensuite.

  - id: REL-S41-A170-CONCEPT-132
    source: S41-A170
    type: prolonge
    cible: CONCEPT-132
    justification: >
      La deuxième Peel Session fixe provisoirement des morceaux qui annoncent Closer sans encore former l’album.

  - id: REL-S41-A171-CONCEPT-110
    source: S41-A171
    type: prolonge
    cible: CONCEPT-110
    justification: >
      Les Bains Douches deviennent archive européenne majeure et transitionnelle.

  - id: REL-S41-A172-CONCEPT-133
    source: S41-A172
    type: prolonge
    cible: CONCEPT-133
    justification: >
      La fête Factory montre un apprentissage économique par échec, ultérieurement relié par Hook à la Haçienda.

  - id: REL-S41-A173-CONCEPT-134
    source: S41-A173
    type: prolonge
    cible: CONCEPT-134
    justification: >
      Annik est à la fois figure de soin pour Curtis et facteur de friction morale avec le groupe.

  - id: REL-S41-A174-CONCEPT-135
    source: S41-A174
    type: prolonge
    cible: CONCEPT-135
    justification: >
      La tournée européenne est vécue comme faim, froid, rejet alimentaire et fatigue corporelle.

  - id: REL-S41-A175-CONCEPT-134
    source: S41-A175
    type: prolonge
    cible: CONCEPT-134
    justification: >
      La scène du bordel d’Antwerp condense soin, morale sexuelle, fatigue et brutalité verbale.

  - id: REL-S41-A176-CONCEPT-136
    source: S41-A176
    type: prolonge
    cible: CONCEPT-136
    justification: >
      Hook oppose le refuge scénique à la désagrégation humaine de la tournée.

  - id: REL-S41-A177-CONCEPT-137
    source: S41-A177
    type: prépare
    cible: CONCEPT-137
    justification: >
      La panne matérielle à réparer soi-même annonce la logique du « continuer malgré tout ».

  - id: REL-S41-A178-CONCEPT-137
    source: S41-A178
    type: prolonge
    cible: CONCEPT-137
    justification: >
      Hook formule explicitement la continuation malgré automutilation, crises et vulnérabilité publique.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A166
    source_id: S41
    atom_id: S41-A166
    title: "Buzzcocks tour fin 1979 : setlists variables et crises visibles"
    chapters: [Chapitre 6, Chapitre 12, Chapitre 14]
    tags: [buzzcocks-tour, setlists, leeds, dundee, bournemouth, rainbow-theatre]
    query_boost:
      - "we always varied ours Buzzcocks tour setlists Joy Division"
      - "Leeds Dundee Bournemouth Ian collapses fit Rainbow Theatre 1979"
    use_for: [tournée Buzzcocks, setlist anti-routine, crises publiques]
    avoid_for: [hiérarchie scénique non croisée]

  - id: RAG-S41-A167
    source_id: S41
    atom_id: S41-A167
    title: "Electric Ballroom : contrariété punk / Factory"
    chapters: [Chapitre 6, Chapitre 14]
    tags: [electric-ballroom, factory, throbbing-gristle, i-remember-nothing, setlist]
    query_boost:
      - "whatever the game was we weren’t going to play it"
      - "Electric Ballroom I Remember Nothing Throbbing Gristle Factory ideals"
    use_for: [ethos Factory, provocation scénique]
    avoid_for: [théorisation excessive de chaque setlist]

  - id: RAG-S41-A168
    source_id: S41
    atom_id: S41-A168
    title: "Anton Corbijn : photo 1979 et mémoire Control"
    chapters: [Chapitre 5, Chapitre 14]
    tags: [anton-corbijn, control, tube-station, photography, posthumous-memory]
    query_boost:
      - "those shots he took of us in the tube station"
      - "Anton Corbijn November 1979 Joy Division Control"
    use_for: [iconographie longue durée, postérité visuelle]
    avoid_for: [réduction de Corbijn à Control]

  - id: RAG-S41-A169
    source_id: S41
    atom_id: S41-A169
    title: "Bournemouth : set écourté et hospitalisation"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [bournemouth, hospital, epilepsy, buzzcocks-tour, cardiff-cancelled]
    query_boost:
      - "The set is cut short because Ian has a fit and is taken to hospital"
      - "Bournemouth Winter Gardens Cardiff cancelled Ian fit hospital"
    use_for: [interruption sans reconfiguration, crise scénique]
    avoid_for: [tournant définitivement assumé]

  - id: RAG-S41-A170
    source_id: S41
    atom_id: S41-A170
    title: "Deuxième Peel Session : seuil pré-Closer"
    chapters: [Chapitre 4, Chapitre 8, Chapitre 12]
    tags: [second-peel-session, maida-vale, twenty-four-hours, colony, love-will-tear-us-apart]
    query_boost:
      - "Tracks recorded The Sound of Music Twenty Four Hours Colony Love Will Tear Us Apart"
      - "second John Peel session 26 November 1979"
    use_for: [radio transitionnelle, pré-Closer]
    avoid_for: [anticipation consciente de Closer]

  - id: RAG-S41-A171
    source_id: S41
    atom_id: S41-A171
    title: "Les Bains Douches : archive live européenne"
    chapters: [Chapitre 6, Chapitre 8, Chapitre 14]
    tags: [les-bains-douches, paris, live-archive, europe, december-1979]
    query_boost:
      - "Joy Division play Les Bains Douches Paris"
      - "Bains Douches Passover A Means to an End Warsaw set list"
    use_for: [archive live de transition, mémoire européenne]
    avoid_for: [généralisation à toute la tournée]

  - id: RAG-S41-A172
    source_id: S41
    atom_id: S41-A172
    title: "Factory office party : économie festive bricolée"
    chapters: [Chapitre 8, Chapitre 14]
    tags: [factory-office-party, oldham-street, beer, rob-gretton, hacienda]
    query_boost:
      - "it was easier to give drink away than it was to get people to pay for it"
      - "Factory office party Oldham Street Rob beer float Hacienda"
    use_for: [culture Factory, préhistoire Haçienda]
    avoid_for: [origine causale de la Haçienda]

  - id: RAG-S41-A173
    source_id: S41
    atom_id: S41-A173
    title: "Annik sur la tournée européenne : soin conflictuel"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [annik-honore, european-tour, mother-hen, ian-curtis, chameleon]
    query_boost:
      - "A right mother hen Annik Ian European tour"
      - "with her talking about Burroughs and Dostoyevsky"
    use_for: [relation Annik / Curtis, soin conflictuel]
    avoid_for: [caricature d’Annik]

  - id: RAG-S41-A174
    source_id: S41
    atom_id: S41-A174
    title: "Tournée européenne : faim, froid et classe alimentaire"
    chapters: [Chapitre 6, Chapitre 11]
    tags: [european-tour, food, cold, rice, class, van]
    query_boost:
      - "I just wanted to go home warmth cat proper food"
      - "never had rice European tour Chinese lentils cold van"
    use_for: [corps pauvre en tournée, géographie corporelle]
    avoid_for: [folklore alimentaire]

  - id: RAG-S41-A175
    source_id: S41
    atom_id: S41-A175
    title: "Antwerp brothel : morale, lit et Rob / Annik"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [antwerp, brothel, annik, rob-gretton, hotel, married-man]
    query_boost:
      - "I’m not the one fucking a married man with a kid"
      - "Antwerp brothel Annik Rob immoral hot water mattress"
    use_for: [tensions Annik / groupe, morale sexuelle de tournée]
    avoid_for: [jugement moral univoque]

  - id: RAG-S41-A176
    source_id: S41
    atom_id: S41-A176
    title: "Scène comme refuge pendant la tournée européenne"
    chapters: [Chapitre 6, Chapitre 12]
    tags: [rotterdam, stage-refuge, european-tour, bickering, hunger, cold]
    query_boost:
      - "the only refuge from the cold the hunger Annik’s clucking the band bickering was being on stage"
      - "European tour stage refuge Joy Division"
    use_for: [cohésion scénique / désagrégation humaine]
    avoid_for: [objectivation sans reviews]

  - id: RAG-S41-A178
    source_id: S41
    atom_id: S41-A178
    title: "We carried on : automutilation, crises et continuation"
    chapters: [Chapitre 12, Chapitre 6]
    tags: [we-carried-on, pernod, kitchen-knife, fits-on-stage, epilepsy, self-harm]
    query_boost:
      - "More than anything Ian hated having a fit on stage"
      - "Pernod kitchen knife We carried on Ian fits on stage"
    use_for: [continuation malgré danger, vulnérabilité publique]
    avoid_for: [téléologie suicidaire]
```
