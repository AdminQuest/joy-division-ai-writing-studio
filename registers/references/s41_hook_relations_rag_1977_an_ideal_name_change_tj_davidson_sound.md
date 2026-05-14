# S41 — Relations stabilisées et entrées RAG — An Ideal for Living, changement de nom, TJ Davidson’s

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A042-CONCEPT-059
    source: S41-A042
    type: prolonge
    cible: CONCEPT-059
    justification: >
      La publication de An Ideal for Living est une autonomie DIY financée par une dette privée contractée par Curtis.

  - id: REL-S41-A043-CONCEPT-054
    source: S41-A043
    type: prolonge
    cible: CONCEPT-054
    justification: >
      La tentative de faire produire l’EP par Paul Morley montre la confusion des rôles et l’inexpérience studio.

  - id: REL-S41-A044-CONCEPT-020
    source: S41-A044
    type: prolonge
    cible: CONCEPT-020
    justification: >
      Hook voit dans An Ideal for Living le moment où Curtis s’impose comme auteur et chanteur.

  - id: REL-S41-A045-S41-A001
    source: S41-A045
    type: prolonge
    cible: S41-A001
    justification: >
      House of Dolls est à la fois source du nom Joy Division et matériau textuel de No Love Lost.

  - id: REL-S41-A046-CONCEPT-060
    source: S41-A046
    type: prolonge
    cible: CONCEPT-060
    justification: >
      Le son muffled de l’EP s’explique par la contrainte physique du support vinyle.

  - id: REL-S41-A047-REGISTRE-BOOTLEGS
    source: S41-A047
    type: alimente
    cible: REGISTRE-BOOTLEGS
    justification: >
      An Ideal for Living passe d’échec sonore à objet fétichisé et fortement bootleggé.

  - id: REL-S41-A048-S41-A026
    source: S41-A048
    type: prolonge
    cible: S41-A026
    justification: >
      La collision avec Warsaw Pakt prolonge les difficultés nominales déjà ouvertes par Stiff Kittens / Warsaw.

  - id: REL-S41-A049-CONCEPT-061
    source: S41-A049
    type: prolonge
    cible: CONCEPT-061
    justification: >
      Le nom Joy Division devient une marque disputée, entre bootlegs, T-shirts et usages commerciaux.

  - id: REL-S41-A050-CONCEPT-062
    source: S41-A050
    type: prolonge
    cible: CONCEPT-062
    justification: >
      La controverse nazie résulte d’une accumulation de signes dans un contexte antifasciste britannique très sensible.

  - id: REL-S41-A051-CONCEPT-056
    source: S41-A051
    type: prolonge
    cible: CONCEPT-056
    justification: >
      Morris permet une nouvelle créativité rythmique, mais le son reste conflit et équilibre collectif.

  - id: REL-S41-A052-CONCEPT-063
    source: S41-A052
    type: prolonge
    cible: CONCEPT-063
    justification: >
      Le mauvais speaker impose à Hook de jouer haut, transformant une limite matérielle en signature sonore.

  - id: REL-S41-A053-CONCEPT-064
    source: S41-A053
    type: prolonge
    cible: CONCEPT-064
    justification: >
      T. J. Davidson’s devient lieu-matrice du son, du froid, de l’image et de la mémoire Joy Division.

  - id: REL-S41-A054-CONCEPT-054
    source: S41-A054
    type: prolonge
    cible: CONCEPT-054
    justification: >
      Jouer devant personne transforme l’échec live en règle éthique durable.

  - id: REL-S41-A055-S41-A001
    source: S41-A055
    type: prépare
    cible: S41-A001
    justification: >
      Le Swinging Apple clôt 1977 et prépare le premier concert officiel sous le nom Joy Division à Pips en janvier 1978.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A042
    source_id: S41
    atom_id: S41-A042
    title: "An Ideal for Living : DIY financé par dette"
    chapters:
      - Chapitre 8
      - Chapitre 10
    tags:
      - an-ideal-for-living
      - diy
      - bank-loan
      - ian-curtis
      - debbie-curtis
    query_boost:
      - "the only way was to release one of our own to go DIY"
      - "An Ideal for Living bank loan furniture Debbie"
    use_for:
      - économie du DIY
      - risque domestique
    avoid_for:
      - héroïsation du DIY

  - id: RAG-S41-A045
    source_id: S41
    atom_id: S41-A045
    title: "No Love Lost et House of Dolls"
    chapters:
      - Chapitre 4
      - Chapitre 5
      - Chapitre 11
    tags:
      - no-love-lost
      - house-of-dolls
      - ka-tzetnik
      - lyrics
      - ian-curtis
    query_boost:
      - "No Love Lost extract from House of Dolls"
      - "An Ideal for Living No Love Lost spoken word"
    use_for:
      - source littéraire
      - controverse du nom
      - paroles de Curtis
    avoid_for:
      - journal intime transparent

  - id: RAG-S41-A046
    source_id: S41
    atom_id: S41-A046
    title: "Pressage raté de An Ideal for Living"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - an-ideal-for-living
      - pressing
      - grooves
      - muffled
      - pips
    query_boost:
      - "the sound quality’s really bad"
      - "An Ideal for Living grooves really narrow"
      - "Pips Dave Booth An Ideal for Living muffled"
    use_for:
      - contrainte du support vinyle
      - échec matériel du DIY
    avoid_for:
      - explication seulement esthétique

  - id: RAG-S41-A048
    source_id: S41
    atom_id: S41-A048
    title: "Warsaw Pakt et changement de nom"
    chapters:
      - Chapitre 5
      - Chapitre 6
    tags:
      - warsaw-pakt
      - warsaw
      - joy-division-name
      - needle-time
      - booking
    query_boost:
      - "Our group wasn’t getting gigs because we weren’t Warsaw Pakt"
      - "Warsaw Pakt Needle Time Joy Division name change"
    use_for:
      - collision nominale
      - nécessité pratique du changement de nom
    avoid_for:
      - réduction du nom Joy Division à l’administration

  - id: RAG-S41-A050
    source_id: S41
    atom_id: S41-A050
    title: "Controverse nazie : accumulation de signes"
    chapters:
      - Chapitre 5
      - Chapitre 11
    tags:
      - nazi-controversy
      - an-ideal-for-living
      - hitler-youth
      - rudolf-hess
      - rock-against-racism
      - anti-nazi-league
    query_boost:
      - "there was quite a lot of evidence against us"
      - "Another Fascism for Fun and Profit Mob"
      - "Rock Against Racism Anti-Nazi League Joy Division"
    use_for:
      - contextualisation sans excuse
      - réception politique
    avoid_for:
      - excuse totale par naïveté

  - id: RAG-S41-A052
    source_id: S41
    atom_id: S41-A052
    title: "Celestion et basse haute : naissance du son Joy Division"
    chapters:
      - Chapitre 3
      - Chapitre 6
    tags:
      - high-bass
      - celestion
      - sound-city
      - joy-division-sound
      - ian-curtis-arranger
    query_boost:
      - "That was how we got it the Joy Division sound"
      - "Celestion eighteen Hooky play high jungle drums"
    use_for:
      - genèse du son
      - contrainte matérielle productive
    avoid_for:
      - origine unique du son

  - id: RAG-S41-A053
    source_id: S41
    atom_id: S41-A053
    title: "T. J. Davidson’s lieu-matrice"
    chapters:
      - Chapitre 3
      - Chapitre 13
      - Chapitre 14
    tags:
      - tj-davidsons
      - little-peter-street
      - rehearsal-room
      - love-will-tear-us-apart-video
      - photographs
    query_boost:
      - "TJ’s really became our place"
      - "T. J. Davidson’s Little Peter Street Joy Division photographs"
    use_for:
      - lieu de répétition
      - géographie émotionnelle
      - image Joy Division
    avoid_for:
      - déterminisme industriel du son

  - id: RAG-S41-A054
    source_id: S41
    atom_id: S41-A054
    title: "Oldham Tower Club : jouer devant personne"
    chapters:
      - Chapitre 6
    tags:
      - oldham-tower-club
      - no-audience
      - live-ethic
      - frantic-elevators
      - hendrix
    query_boost:
      - "I’ve played for no one before Anything more than that is a bonus"
      - "Oldham Tower Club Frantic Elevators Hendrix Joy Division"
    use_for:
      - éthique live de Hook
      - concerts non listés
    avoid_for:
      - certitude chronologique non vérifiée
```
