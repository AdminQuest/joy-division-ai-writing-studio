# S41 — Relations stabilisées et entrées RAG — *Closer*, Britannia Row, mix de « Love Will Tear Us Apart », Annik, Saville

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A179-CONCEPT-138
    source: S41-A179
    type: prolonge
    cible: CONCEPT-138
    justification: >
      Le passage place Closer dans une superposition de carrière, domesticité, maladie et traitement médical.

  - id: REL-S41-A180-CONCEPT-139
    source: S41-A180
    type: prolonge
    cible: CONCEPT-139
    justification: >
      Hook oppose la canonisation ultérieure d’Unknown Pleasures à la pauvreté réelle du groupe au moment de Closer.

  - id: REL-S41-A181-CONCEPT-140
    source: S41-A181
    type: prolonge
    cible: CONCEPT-140
    justification: >
      Hannett organise le mix de Love Will Tear Us Apart comme espace de maîtrise dont les musiciens sont largement exclus.

  - id: REL-S41-A182-CONCEPT-141
    source: S41-A182
    type: prolonge
    cible: CONCEPT-141
    justification: >
      Britannia Row est décrit comme espace clos, nocturne et clinique dont l’atmosphère se dépose dans le son de Closer.

  - id: REL-S41-A183-CONCEPT-142
    source: S41-A183
    type: prolonge
    cible: CONCEPT-142
    justification: >
      Hook explicite la doctrine Hannett de clarté et séparation, appuyée sur Auratones, ARP, sequencers et gates.

  - id: REL-S41-A184-CONCEPT-143
    source: S41-A184
    type: prolonge
    cible: CONCEPT-143
    justification: >
      Les différents milieux de Curtis revendiquent des figures concurrentes du vrai Ian.

  - id: REL-S41-A185-CONCEPT-144
    source: S41-A185
    type: prolonge
    cible: CONCEPT-144
    justification: >
      Les compagnes sont invitées à Londres mais restent en attente et à distance, tandis qu’Annik est visible dans l’espace des sessions.

  - id: REL-S41-A186-CONCEPT-134
    source: S41-A186
    type: prolonge
    cible: CONCEPT-134
    justification: >
      Les japes contre Ian et Annik prolongent la tension entre soin, jalousie, classe et culture masculine de tournée.

  - id: REL-S41-A187-CONCEPT-145
    source: S41-A187
    type: prolonge
    cible: CONCEPT-145
    justification: >
      La crise aux toilettes de Britannia Row fait entrer l’épilepsie dans le lieu de production même.

  - id: REL-S41-A188-CONCEPT-130
    source: S41-A188
    type: prolonge
    cible: CONCEPT-130
    justification: >
      La scène U2 situe Joy Division comme modèle pour d’autres trajectoires post-punk et comme point de bifurcation industrielle.

  - id: REL-S41-A189-CONCEPT-146
    source: S41-A189
    type: prolonge
    cible: CONCEPT-146
    justification: >
      Les images de Staglieno sont choisies avant la mort de Curtis et se chargent ensuite d’une signification funéraire posthume.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A179
    source_id: S41
    atom_id: S41-A179
    title: "Avant Closer : Amérique, Annik, Candy et barbituriques"
    chapters: [Chapitre 10, Chapitre 12, Chapitre 8]
    tags: [closer, america-tour, annik, deborah, candy, barbiturates, epilepsy]
    query_boost:
      - "By now plans were being made to tour America"
      - "Candy sent away barbiturates Annik Debbie Closer sessions"
    use_for: [pression avant Closer, contexte médical et domestique]
    avoid_for: [téléologie morbide]

  - id: RAG-S41-A180
    source_id: S41
    atom_id: S41-A180
    title: "Succès sans star-system avant Closer"
    chapters: [Chapitre 8, Chapitre 14]
    tags: [unknown-pleasures, no-money, independent-music, rob-gretton, keep-bands-poor]
    query_boost:
      - "We never felt like we were stars at all"
      - "Always keep your bands poor That way they make great music"
    use_for: [économie indépendante, pauvreté Factory]
    avoid_for: [romantisation de la pauvreté]

  - id: RAG-S41-A181
    source_id: S41
    atom_id: S41-A181
    title: "Mix de Love Will Tear Us Apart : exclusion par Hannett"
    chapters: [Chapitre 4, Chapitre 8]
    tags: [love-will-tear-us-apart, strawberry, hannett, mix, air-conditioning]
    query_boost:
      - "he hated having the musicians around during the mix"
      - "Love Will Tear Us Apart two in the morning air conditioning"
    use_for: [production Hannett, mix comme exclusion]
    avoid_for: [Hannett seulement tyran]

  - id: RAG-S41-A182
    source_id: S41
    atom_id: S41-A182
    title: "Britannia Row : spatialité sonore de Closer"
    chapters: [Chapitre 3, Chapitre 8, Chapitre 13]
    tags: [closer, britannia-row, pink-floyd, studio, airless, night]
    query_boost:
      - "It had an enclosed spaceship atmosphere"
      - "Britannia Row airless sealed off from the outside world Closer"
    use_for: [spatialité sonore de Closer, studio comme espace clos]
    avoid_for: [studio comme cause unique]

  - id: RAG-S41-A183
    source_id: S41
    atom_id: S41-A183
    title: "Hannett : clarté, séparation, Auratones, ARP et gates"
    chapters: [Chapitre 3, Chapitre 8]
    tags: [hannett, auratones, arp, gates, clarity, separation, britannia-row]
    query_boost:
      - "for a recording to have lasting effect and impact it had to have clarity and separation"
      - "Auratones ARP synthesizers sequencers audio gates Britannia Row"
    use_for: [techniques Hannett, clarté et séparation]
    avoid_for: [détails techniques non croisés]

  - id: RAG-S41-A184
    source_id: S41
    atom_id: S41-A184
    title: "Qui connaît le vrai Ian ?"
    chapters: [Chapitre 10, Chapitre 12, Chapitre 14]
    tags: [ian-curtis, annik, genesis-p-orridge, deborah, real-ian]
    query_boost:
      - "I bet even Ian didn’t know who the real Ian was"
      - "Annik Genesis Debbie real Ian arty Bohemian"
    use_for: [Curtis pluralisé, identité relationnelle]
    avoid_for: [psychologisation]

  - id: RAG-S41-A185
    source_id: S41
    atom_id: S41-A185
    title: "Compagnes à Londres : domesticité déplacée au studio"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [annnik, iris, sue, lesley, gillian, debbie, london-flats]
    query_boost:
      - "Annik was hanging around"
      - "Sue Lesley Gillian Iris London studio Debbie bill"
    use_for: [domesticité déplacée, asymétrie des présences]
    avoid_for: [réduction des femmes au conflit]

  - id: RAG-S41-A186
    source_id: S41
    atom_id: S41-A186
    title: "Japes contre Ian et Annik : perte du camarade"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [annnik, ironing, teddy-bear, sneaky-japing-tossers, ian-curtis]
    query_boost:
      - "We’re losing our mate here"
      - "i-ron-ing teddy bear ironing board bed English peegs"
    use_for: [jalousie de groupe, masculinité de tournée]
    avoid_for: [reproduction de la brutalité du récit]

  - id: RAG-S41-A187
    source_id: S41
    atom_id: S41-A187
    title: "Crise aux toilettes de Britannia Row"
    chapters: [Chapitre 8, Chapitre 12]
    tags: [closer, britannia-row, toilet-fit, epilepsy, carried-on]
    query_boost:
      - "He Said He Was All Right So We Carried On"
      - "found him in the toilet big gash in his head"
    use_for: [crise médicalisée au studio, continuation malgré danger]
    avoid_for: [procès moral simpliste]

  - id: RAG-S41-A188
    source_id: S41
    atom_id: S41-A188
    title: "U2 à Britannia Row : bifurcation post-punk"
    chapters: [Chapitre 8, Chapitre 14]
    tags: [u2, hannett, 11-oclock-tick-tock, britannia-row, bono]
    query_boost:
      - "star-struck young pretenders"
      - "U2 11 O’Clock Tick Tock Hannett Britannia Row"
    use_for: [postérité Joy Division, bifurcation U2 / New Order]
    avoid_for: [filiation directe totale]

  - id: RAG-S41-A189
    source_id: S41
    atom_id: S41-A189
    title: "Saville, Staglieno et image funéraire après-coup"
    chapters: [Chapitre 5, Chapitre 8, Chapitre 12, Chapitre 14]
    tags: [saville, staglieno, bernard-pierre-wolff, closer-cover, love-will-tear-us-apart]
    query_boost:
      - "We all loved the pictures especially Ian"
      - "Staglieno Cemetery Closer Love Will Tear Us Apart Peter Saville"
    use_for: [image funéraire après-coup, anti-téléologie visuelle]
    avoid_for: [prophétie funéraire]
```
