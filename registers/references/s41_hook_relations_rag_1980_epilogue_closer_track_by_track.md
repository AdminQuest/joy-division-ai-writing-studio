# S41 — Relations stabilisées et entrées RAG — Épilogue et *Closer Track by Track*

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A211-CONCEPT-162
    source: S41-A211
    type: prolonge
    cible: CONCEPT-162
    justification: >
      Les survivants se retirent de la promotion au moment même où la postérité publique de Joy Division se construit.

  - id: REL-S41-A212-CONCEPT-163
    source: S41-A212
    type: prolonge
    cible: CONCEPT-163
    justification: >
      La reprise du travail musical montre l’absence de Curtis comme centre de validation et d’orientation créative.

  - id: REL-S41-A213-CONCEPT-164
    source: S41-A213
    type: prolonge
    cible: CONCEPT-164
    justification: >
      Joy Division cesse nominalement, tandis que les survivants poursuivent la pratique musicale sous un autre nom.

  - id: REL-S41-A214-CONCEPT-165
    source: S41-A214
    type: prolonge
    cible: CONCEPT-165
    justification: >
      « Atrocity Exhibition » illustre l’absence au mix : Hannett transforme le son de Hook pendant qu’il n’est pas là.

  - id: REL-S41-A215-CONCEPT-166
    source: S41-A215
    type: prolonge
    cible: CONCEPT-166
    justification: >
      « Isolation » naît d’une structure simple, de synthés et d’un montage analogique fragile.

  - id: REL-S41-A216-CONCEPT-167
    source: S41-A216
    type: prolonge
    cible: CONCEPT-167
    justification: >
      « Passover » fixe la six-string bass, le Clone Theory et le delay comme son de basse-guitare de Hook.

  - id: REL-S41-A217-CONCEPT-168
    source: S41-A217
    type: prolonge
    cible: CONCEPT-168
    justification: >
      Hook lit Closer comme album fragile et mélancolique mais entièrement confiant.

  - id: REL-S41-A218-CONCEPT-169
    source: S41-A218
    type: prolonge
    cible: CONCEPT-169
    justification: >
      « A Means to an End » fait apparaître une pop / dance déformée dans Closer.

  - id: REL-S41-A219-CONCEPT-170
    source: S41-A219
    type: prolonge
    cible: CONCEPT-170
    justification: >
      « Heart and Soul » déplace une basse écrite par Hook vers le synthétiseur, libérant une ligne supérieure.

  - id: REL-S41-A220-CONCEPT-171
    source: S41-A220
    type: prolonge
    cible: CONCEPT-171
    justification: >
      La puissance vocale de Curtis brouille la lisibilité immédiate de sa détresse.

  - id: REL-S41-A221-CONCEPT-172
    source: S41-A221
    type: prolonge
    cible: CONCEPT-172
    justification: >
      « The Eternal » devient pour Hook mémoire de la solidité collective irrépétable des quatre.

  - id: REL-S41-A222-CONCEPT-173
    source: S41-A222
    type: prolonge
    cible: CONCEPT-173
    justification: >
      « Decades » et Closer apparaissent chez Hook comme objets de plaisir d’écoute, non seulement comme monuments posthumes.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A211
    source_id: S41
    atom_id: S41-A211
    title: "Joy Division mis en boîte : postérité sans participation"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [epilogue, posthumous-success, no-promotion, ceremony, in-a-lonely-place]
    query_boost:
      - "we packed everything in a little box once he’d gone"
      - "no promotion Love Will Tear Us Apart Closer after Ian died"
    use_for: [postérité sans participation, mise en boîte de Joy Division]
    avoid_for: [absence d’attachement]

  - id: RAG-S41-A212
    source_id: S41
    atom_id: S41-A212
    title: "See you on Monday : création sans Curtis"
    chapters: [Chapitre 14]
    tags: [dreams-never-end, new-order, spotter, mentor, monday]
    query_boost:
      - "we’d lost our spotter our mentor"
      - "See you on Monday Dreams Never End spotter New Order"
    use_for: [naissance New Order, création sans centre]
    avoid_for: [froideur]

  - id: RAG-S41-A213
    source_id: S41
    atom_id: S41-A213
    title: "Joy Division was over : fin nominale"
    chapters: [Chapitre 14]
    tags: [joy-division-over, pact, no-new-singer, new-name, new-order]
    query_boost:
      - "Joy Division was over"
      - "we’d had a pact from early days if something happened to one of us"
    use_for: [fin du nom Joy Division, intégrité quatuor]
    avoid_for: [continuité simple]

  - id: RAG-S41-A214
    source_id: S41
    atom_id: S41-A214
    title: "Atrocity Exhibition : instrument swap et absence au mix"
    chapters: [Chapitre 3, Chapitre 8]
    tags: [atrocity-exhibition, instrument-swap, hannett, marshall-time-waster, mix]
    query_boost:
      - "Barney plays bass and I play guitar on Atrocity Exhibition"
      - "Marshall Time Waster Rob said you weren’t there so you can’t say anything"
    use_for: [Atrocity Exhibition, mix Hannett, échange instruments]
    avoid_for: [Hannett tyran uniquement]

  - id: RAG-S41-A215
    source_id: S41
    atom_id: S41-A215
    title: "Isolation : synthés, simplicité, edit sauvé"
    chapters: [Chapitre 3, Chapitre 8]
    tags: [isolation, no-guitar, arp, transcendent, razor-edit, mike-johnson]
    query_boost:
      - "it has no guitar on it"
      - "Isolation razor blade edit Mike Johnson"
    use_for: [simplicité moderne, montage analogique]
    avoid_for: [détails techniques non croisés]

  - id: RAG-S41-A216
    source_id: S41
    atom_id: S41-A216
    title: "Passover : six-string bass et Clone Theory"
    chapters: [Chapitre 3, Chapitre 8, Chapitre 14]
    tags: [passover, six-string-bass, clone-theory, delay, peter-hook]
    query_boost:
      - "Everyone thinks it’s a guitar but it’s not it’s the six-string bass"
      - "Clone Theory short eighty-millisecond delay Passover"
    use_for: [basse-guitare, son Hook phase suivante]
    avoid_for: [transition New Order monocausale]

  - id: RAG-S41-A217
    source_id: S41
    atom_id: S41-A217
    title: "Closer : confiance mélancolique"
    chapters: [Chapitre 8, Chapitre 12]
    tags: [closer, colony, confident, melancholic, music-chemistry]
    query_boost:
      - "Every song is confident"
      - "Closer melancholic fragile but intense music chemistry"
    use_for: [lecture anti-funéraire de Closer, chimie du groupe]
    avoid_for: [vérité critique universelle]

  - id: RAG-S41-A218
    source_id: S41
    atom_id: S41-A218
    title: "A Means to an End : fucked-up disco"
    chapters: [Chapitre 8, Chapitre 14]
    tags: [a-means-to-an-end, fucked-up-disco, pop-song, hannett]
    query_boost:
      - "This is the pop song on the album It’s a fucked-up disco song"
      - "A Means to an End finished in the studio Martin stamp"
    use_for: [dance abîmée, proto-New Order]
    avoid_for: [rétroprojection directe]

  - id: RAG-S41-A219
    source_id: S41
    atom_id: S41-A219
    title: "Heart and Soul : basse transférée au synthé"
    chapters: [Chapitre 3, Chapitre 8, Chapitre 14]
    tags: [heart-and-soul, low-bass, synthesizer, mr-melody, new-order]
    query_boost:
      - "I wrote the low bass and we transferred it to the synthesizer"
      - "Heart and Soul Mr Melody low bass synth"
    use_for: [matrice New Order, synthétiseur et basse]
    avoid_for: [procédé unique]

  - id: RAG-S41-A220
    source_id: S41
    atom_id: S41-A220
    title: "Twenty Four Hours : Curtis vulnérable et rock god"
    chapters: [Chapitre 4, Chapitre 12]
    tags: [twenty-four-hours, ian-curtis, vocal, lyrics, vulnerable]
    query_boost:
      - "on the one hand he was ill and vulnerable on the other he was a screaming rock god"
      - "Twenty Four Hours why didn’t you realize he was so bad"
    use_for: [illisibilité de la détresse performée, voix et santé]
    avoid_for: [paroles comme diagnostic immédiat]

  - id: RAG-S41-A221
    source_id: S41
    atom_id: S41-A221
    title: "The Eternal : chimie irrépétable des quatre"
    chapters: [Chapitre 8, Chapitre 12, Chapitre 14]
    tags: [the-eternal, six-string, transcendent, white-noise, echo-plate]
    query_boost:
      - "the solidity between me Ian Steve and Bernard was very very powerful"
      - "The Eternal favourite lyric Transcendent white noise echo plate"
    use_for: [chimie irrépétable, mémoire sonore des quatre]
    avoid_for: [hiérarchie objective]

  - id: RAG-S41-A222
    source_id: S41
    atom_id: S41-A222
    title: "Decades : beauté finale et Closer plaisir d’écoute"
    chapters: [Chapitre 8, Chapitre 12, Chapitre 14]
    tags: [decades, atmosphere, closer, favourite-albums, six-string]
    query_boost:
      - "I think it’s more beautiful than Atmosphere"
      - "Closer easier to listen to than Unknown Pleasures favourite albums"
    use_for: [Closer comme plaisir d’écoute, anti-téléologie funéraire]
    avoid_for: [canon critique universel]
```
