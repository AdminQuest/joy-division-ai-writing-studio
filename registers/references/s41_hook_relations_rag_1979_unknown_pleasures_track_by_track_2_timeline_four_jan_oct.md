# S41 — Relations stabilisées et entrées RAG — *Unknown Pleasures* track by track II et Timeline Four janvier-octobre 1979

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A154-CONCEPT-120
    source: S41-A154
    type: prolonge
    cible: CONCEPT-120
    justification: >
      « Interzone » redistribue la fonction vocale : Hook chante la voix principale et Curtis soutient en backing vocal.

  - id: REL-S41-A155-CONCEPT-121
    source: S41-A155
    type: prolonge
    cible: CONCEPT-121
    justification: >
      « I Remember Nothing » clôt Unknown Pleasures par jam, bruitages, synthétiseur bricolé et indistinction instrumentale.

  - id: REL-S41-A156-CONCEPT-122
    source: S41-A156
    type: prolonge
    cible: CONCEPT-122
    justification: >
      La Timeline Four organise 1979 par couches distinctes d’événements, sans imposer de causalité unique.

  - id: REL-S41-A157-CONCEPT-123
    source: S41-A157
    type: prolonge
    cible: CONCEPT-123
    justification: >
      Les clichés Princess Parkway deviennent iconiques dans une économie photographique pauvre et rapide.

  - id: REL-S41-A158-CONCEPT-124
    source: S41-A158
    type: prolonge
    cible: CONCEPT-124
    justification: >
      Le diagnostic d’épilepsie s’insère dans la montée de visibilité presse, Factory et radio, au lieu de remplacer ces couches.

  - id: REL-S41-A159-CONCEPT-125
    source: S41-A159
    type: prolonge
    cible: CONCEPT-125
    justification: >
      La première Peel Session confirme la radio comme reconnaissance pratique et professionnelle, au-delà du prestige symbolique.

  - id: REL-S41-A160-S41-A117
    source: S41-A160
    type: consolide
    cible: S41-A117
    justification: >
      La Timeline Four verrouille la session Unknown Pleasures, sa fin, ses crédits et sa sortie FACT 10.

  - id: REL-S41-A161-CONCEPT-103
    source: S41-A161
    type: prolonge
    cible: CONCEPT-103
    justification: >
      Piccadilly Radio fait apparaître « Chance » / « Atmosphere », « Atrocity Exhibition » et « These Days » comme seuil post-album.

  - id: REL-S41-A162-S41-A126
    source: S41-A162
    type: prolonge
    cible: S41-A126
    justification: >
      « Transmission » devient single autonome par étapes : Central Sound, Strawberry, sortie FAC 13.

  - id: REL-S41-A163-CONCEPT-126
    source: S41-A163
    type: prolonge
    cible: CONCEPT-126
    justification: >
      Le Nashville Rooms montre « Atmosphere » utilisé comme ouverture de set avant son recouvrement funéraire posthume.

  - id: REL-S41-A164-CONCEPT-127
    source: S41-A164
    type: prolonge
    cible: CONCEPT-127
    justification: >
      Futurama, The Factory Flick et Something Else superposent festival, film Factory et télévision.

  - id: REL-S41-A165-CONCEPT-128
    source: S41-A165
    type: prolonge
    cible: CONCEPT-128
    justification: >
      Octobre 1979 superpose Earcom 2, FAC 13, Sordide Sentimental et tournée Buzzcocks.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A154
    source_id: S41
    atom_id: S41-A154
    title: "Interzone : chant Hook et backing Curtis"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 8
    tags:
      - interzone
      - hook-vocal
      - curtis-backing-vocal
      - rca
      - keep-on-keepin-on
    query_boost:
      - "Me singing the main vocal while Ian does the low backing vocal"
      - "Interzone Keep On Keepin On RCA"
    use_for:
      - chant redistribué
      - métabolisation RCA
    avoid_for:
      - réduction à une reprise

  - id: RAG-S41-A155
    source_id: S41
    atom_id: S41-A155
    title: "I Remember Nothing : Transcendent 2000 et clôture atmosphérique"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - i-remember-nothing
      - transcendent-2000
      - shattering-glass
      - unknown-pleasures
      - hannett
    query_boost:
      - "This is a great atmospheric track and came together very quickly"
      - "Transcendent 2000 shattering glass I Remember Nothing"
    use_for:
      - clôture atmosphérique
      - synthétiseur bricolé
    avoid_for:
      - préfiguration mécanique de New Order

  - id: RAG-S41-A156
    source_id: S41
    atom_id: S41-A156
    title: "Timeline Four : ossature documentaire de 1979"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 6
      - Chapitre 8
      - Chapitre 12
      - Chapitre 14
    tags:
      - timeline-four
      - 1979
      - sessions
      - factory
      - chronology
    query_boost:
      - "TIMELINE FOUR JANUARY DECEMBER 1979"
      - "1979 Joy Division A Factory Sample Peel Unknown Pleasures Transmission Sordide"
    use_for:
      - chronologie 1979
      - verrouillage dates sessions sorties concerts
    avoid_for:
      - causalité téléologique

  - id: RAG-S41-A157
    source_id: S41
    atom_id: S41-A157
    title: "Princess Parkway : Cummins et icône par contrainte"
    chapters:
      - Chapitre 5
      - Chapitre 14
    tags:
      - kevin-cummins
      - princess-parkway
      - nme-cover
      - photography
      - ian-curtis
    query_boost:
      - "Kevin freely admits he only took seven shots"
      - "Princess Parkway NME cover Ian Curtis smoking"
    use_for:
      - iconographie Joy Division
      - photographie punk pauvre
    avoid_for:
      - réduction de Cummins à la contrainte matérielle

  - id: RAG-S41-A158
    source_id: S41
    atom_id: S41-A158
    title: "23 janvier 1979 : diagnostic d’épilepsie"
    chapters:
      - Chapitre 6
      - Chapitre 12
    tags:
      - epilepsy
      - diagnosis
      - ian-curtis
      - january-1979
      - factory
    query_boost:
      - "Ian Curtis diagnosed with epilepsy"
      - "23 January 1979 epilepsy diagnosis Joy Division"
    use_for:
      - santé comme couche de professionnalisation
      - chronologie médicale
    avoid_for:
      - causalité médicale totale

  - id: RAG-S41-A159
    source_id: S41
    atom_id: S41-A159
    title: "Première Peel Session : BBC et professionnalisation radio"
    chapters:
      - Chapitre 6
      - Chapitre 8
      - Chapitre 14
    tags:
      - john-peel
      - bbc
      - bob-sargeant
      - peel-session
      - radio
    query_boost:
      - "I loved that session"
      - "first John Peel session Bob Sargeant Exercise One Insight Transmission She’s Lost Control"
    use_for:
      - professionnalisation radiophonique
      - BBC comme seuil
    avoid_for:
      - succès commercial

  - id: RAG-S41-A160
    source_id: S41
    atom_id: S41-A160
    title: "Unknown Pleasures : chronologie FACT 10"
    chapters:
      - Chapitre 3
      - Chapitre 5
      - Chapitre 8
      - Chapitre 12
    tags:
      - unknown-pleasures
      - fact-10
      - strawberry-studios
      - natalie-curtis
      - chris-nagle
    query_boost:
      - "Unknown Pleasures Factory Records FACT 10 released"
      - "Natalie Curtis born Macclesfield Unknown Pleasures recording session ends"
    use_for:
      - chronologie album
      - session sortie crédits
    avoid_for:
      - interprétation psychologique directe

  - id: RAG-S41-A161
    source_id: S41
    atom_id: S41-A161
    title: "Piccadilly Radio : seuil post-album"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 8
    tags:
      - piccadilly-radio
      - these-days
      - chance
      - atmosphere
      - atrocity-exhibition
    query_boost:
      - "Tracks recorded These Days Candidate The Only Mistake Chance Atmosphere Atrocity Exhibition"
      - "Piccadilly Radio Pennine Sound Stuart James 4 June 1979"
    use_for:
      - transition Unknown Pleasures vers Closer
      - versions radio
    avoid_for:
      - anticipation consciente de Closer

  - id: RAG-S41-A162
    source_id: S41
    atom_id: S41-A162
    title: "Transmission FAC 13 : trajectoire single"
    chapters:
      - Chapitre 4
      - Chapitre 8
      - Chapitre 14
    tags:
      - transmission
      - novelty
      - fac13
      - central-sound
      - strawberry-studios
    query_boost:
      - "The Transmission Novelty seven-inch single Factory Records FAC 13 released"
      - "Central Sound Strawberry Transmission single version Novelty"
    use_for:
      - single autonome
      - trajectoire Factory du morceau
    avoid_for:
      - simple extrait d’album

  - id: RAG-S41-A163
    source_id: S41
    atom_id: S41-A163
    title: "Atmosphere avant funérailles : Nashville, YMCA, Leigh"
    chapters:
      - Chapitre 4
      - Chapitre 6
      - Chapitre 12
      - Chapitre 14
    tags:
      - atmosphere
      - nashville-rooms
      - annik-honore
      - ymca
      - anti-teleology
    query_boost:
      - "Back then it was a good song to start with"
      - "Atmosphere death march before connotations Nashville Rooms"
    use_for:
      - anti-téléologie Atmosphere
      - montée live août 1979
    avoid_for:
      - lecture uniquement funéraire

  - id: RAG-S41-A164
    source_id: S41
    atom_id: S41-A164
    title: "Futurama Factory Flick Something Else : visibilité audiovisuelle"
    chapters:
      - Chapitre 5
      - Chapitre 14
    tags:
      - futurama
      - factory-flick
      - fac9
      - something-else
      - malcolm-whitehead
    query_boost:
      - "The Factory Flick Factory FAC 9 1979"
      - "Something Else She’s Lost Control Transmission Futurama"
    use_for:
      - image hors pochette
      - archives audiovisuelles 1979
    avoid_for:
      - maîtrise complète de l’image

  - id: RAG-S41-A165
    source_id: S41
    atom_id: S41-A165
    title: "Octobre 1979 : Earcom 2 FAC13 Sordide Buzzcocks"
    chapters:
      - Chapitre 6
      - Chapitre 8
      - Chapitre 12
      - Chapitre 14
    tags:
      - earcom-2
      - fac13
      - sordide-sentimental
      - buzzcocks-tour
      - october-1979
    query_boost:
      - "The Sordide Sentimental session Cargo Studios Rochdale"
      - "Earcom 2 Transmission Novelty Buzzcocks tour October 1979"
    use_for:
      - octobre carrefour
      - discographie et tournée
    avoid_for:
      - fusion des objets discographiques
```
