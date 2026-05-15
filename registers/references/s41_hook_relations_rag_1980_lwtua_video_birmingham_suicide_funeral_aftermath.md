# S41 — Relations stabilisées et entrées RAG — « Love Will Tear Us Apart » vidéo, Birmingham, suicide, funérailles, après-coup

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A201-CONCEPT-153
    source: S41-A201
    type: prolonge
    cible: CONCEPT-153
    justification: >
      L’annulation des concerts protège Curtis mais peut aussi, selon Hook, le rapprocher de la crise domestique.

  - id: REL-S41-A202-CONCEPT-154
    source: S41-A202
    type: prolonge
    cible: CONCEPT-154
    justification: >
      Hook oppose l’excitation américaine qu’il observe aux propos rapportés par Genesis P-Orridge.

  - id: REL-S41-A203-CONCEPT-155
    source: S41-A203
    type: prolonge
    cible: CONCEPT-155
    justification: >
      La vidéo de Love Will Tear Us Apart transforme un choix anti-playback raté en objet audiovisuel canonique.

  - id: REL-S41-A204-CONCEPT-156
    source: S41-A204
    type: prolonge
    cible: CONCEPT-156
    justification: >
      Birmingham reste un bon concert selon Hook, mais traversé par la surveillance constante de l’état de Curtis.

  - id: REL-S41-A205-CONCEPT-157
    source: S41-A205
    type: prolonge
    cible: CONCEPT-157
    justification: >
      Le dernier souvenir de Hook ne contient pas de signe clair, seulement une euphorie américaine rétrospectivement illisible.

  - id: REL-S41-A206-CONCEPT-158
    source: S41-A206
    type: prolonge
    cible: CONCEPT-158
    justification: >
      La dernière nuit est décrite comme faisceau de couches, sans cause unique isolable.

  - id: REL-S41-A207-CONCEPT-159
    source: S41-A207
    type: prolonge
    cible: CONCEPT-159
    justification: >
      Hook décrit la réception de l’appel de police comme engourdissement, dissociation et silence collectif.

  - id: REL-S41-A208-CONCEPT-159
    source: S41-A208
    type: prolonge
    cible: CONCEPT-159
    justification: >
      Les funérailles prolongent le deuil sidéré, entre refus du corps, pub et prophétie de Rob.

  - id: REL-S41-A209-CONCEPT-160
    source: S41-A209
    type: prolonge
    cible: CONCEPT-160
    justification: >
      Le retour au local et Dreams Never End montrent que la continuité musicale sert de stratégie de survie.

  - id: REL-S41-A210-CONCEPT-161
    source: S41-A210
    type: prolonge
    cible: CONCEPT-161
    justification: >
      Le mac et l’écharpe donnés au charity shop deviennent objets pauvres de mémoire et de culpabilité après-coup.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A201
    source_id: S41
    atom_id: S41-A201
    title: "Pause après Bury : repos nécessaire, retour au foyer"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [cancelled-gigs, rest, bury, domestic-problems, ian-curtis]
    query_boost:
      - "we pulled some gigs"
      - "gigging break did him in domestic problems Hook"
    use_for: [repos ambivalent, arrêt protecteur]
    avoid_for: [causalité contrefactuelle]

  - id: RAG-S41-A202
    source_id: S41
    atom_id: S41-A202
    title: "Amérique : excitation Hook contre rather die Genesis"
    chapters: [Chapitre 10, Chapitre 12, Chapitre 14]
    tags: [america-tour, genesis-p-orridge, rather-die, ian-curtis, memory]
    query_boost:
      - "No rather die about it"
      - "Genesis P-Orridge rather die America Hook cock-a-hoop"
    use_for: [contradiction documentaire, Amérique horizon contradictoire]
    avoid_for: [trancher une intention intime]

  - id: RAG-S41-A203
    source_id: S41
    atom_id: S41-A203
    title: "Love Will Tear Us Apart vidéo : erreur devenue légende"
    chapters: [Chapitre 5, Chapitre 8, Chapitre 14]
    tags: [love-will-tear-us-apart, video, tj-davidsons, no-miming, australia]
    query_boost:
      - "Mistakes that then became legends"
      - "Love Will Tear Us Apart video T J Davidson’s live performance Australia"
    use_for: [vidéo LWTUA, anti-playback, canon audiovisuel]
    avoid_for: [stratégie consciente totale]

  - id: RAG-S41-A204
    source_id: S41
    atom_id: S41-A204
    title: "Birmingham : dernier concert, Still et surveillance"
    chapters: [Chapitre 6, Chapitre 12, Chapitre 14]
    tags: [birmingham, high-hall, still, decades, digital, last-gig]
    query_boost:
      - "it would be our last-ever gig as Joy Division"
      - "Birmingham Still Decades wobble Digital last gig"
    use_for: [dernier concert, performance sous risque]
    avoid_for: [prophétie scénique]

  - id: RAG-S41-A205
    source_id: S41
    atom_id: S41-A205
    title: "Dernier trajet : I never said goodbye"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [last-lift, failsworth, moston, america, goodbye]
    query_boost:
      - "I never said goodbye"
      - "last time I saw him Friday night America car whooping"
    use_for: [dernier souvenir sans signe, culpabilité Hook]
    avoid_for: [euphorie comme preuve]

  - id: RAG-S41-A206
    source_id: S41
    atom_id: S41-A206
    title: "Dernière nuit : Stroszek The Idiot lettre"
    chapters: [Chapitre 12]
    tags: [stroszek, the-idiot, barton-street, letter, suicide, deborah]
    query_boost:
      - "wished he was dead but made no mention of any intention to kill himself"
      - "Stroszek The Idiot coffee spirits Barton Street letter"
    use_for: [dernière nuit par faisceau, absence de cause unique]
    avoid_for: [cause unique]

  - id: RAG-S41-A207
    source_id: S41
    atom_id: S41-A207
    title: "Appel de la police : deuil sidéré"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [police-call, sunday-lunch, numb, grief, hook]
    query_boost:
      - "I went numb"
      - "police rang Sunday lunch Ian killed himself Hook"
    use_for: [deuil sidéré, réaction Hook]
    avoid_for: [absence d’affect]

  - id: RAG-S41-A208
    source_id: S41
    atom_id: S41-A208
    title: "Funérailles : Rob prédit la postérité"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [funeral, chapel-of-rest, rob-gretton, prophecy, joy-division]
    query_boost:
      - "Joy Division will be really big in ten years’ time"
      - "chapel of rest refused body funeral Rob prediction"
    use_for: [deuil et postérité, Factory wake]
    avoid_for: [Rob prophète froid]

  - id: RAG-S41-A209
    source_id: S41
    atom_id: S41-A209
    title: "Dreams Never End : New Order comme survie"
    chapters: [Chapitre 14]
    tags: [dreams-never-end, new-order, six-string-bass, monday-rehearsal, aftermath]
    query_boost:
      - "The beginning of our new life as New Order"
      - "Dreams Never End six-string bass Minton Street Monday rehearsal"
    use_for: [naissance New Order, continuité comme survie]
    avoid_for: [froideur ou deuil résolu]

  - id: RAG-S41-A210
    source_id: S41
    atom_id: S41-A210
    title: "Culpabilité : mac, écharpe, charity shop"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [guilt, mac, scarf, charity-shop, inquest, goodbye]
    query_boost:
      - "Guilty that I never said goodbye"
      - "Ian mac scarf charity shop Hook guilt inquest"
    use_for: [culpabilité après-coup, objets pauvres de mémoire]
    avoid_for: [aveu causal]
```
