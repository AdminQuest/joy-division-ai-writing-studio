# S41 — Relations stabilisées et entrées RAG — *Licht und Blindheit*, « Love Will Tear Us Apart », Bournemouth, *Unknown Pleasures* track by track I

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A143-CONCEPT-112
    source: S41-A143
    type: prolonge
    cible: CONCEPT-112
    justification: >
      Licht und Blindheit place deux titres majeurs dans une édition limitée, sans logique commerciale normale.

  - id: REL-S41-A144-CONCEPT-113
    source: S41-A144
    type: prolonge
    cible: CONCEPT-113
    justification: >
      « Atmosphere » naît de deux moitiés assemblées, avant sa canonisation funéraire ultérieure.

  - id: REL-S41-A145-CONCEPT-114
    source: S41-A145
    type: prolonge
    cible: CONCEPT-114
    justification: >
      Le riff de basse de Hook devient selon lui la mélodie du refrain de « Love Will Tear Us Apart ».

  - id: REL-S41-A146-CONCEPT-115
    source: S41-A146
    type: prolonge
    cible: CONCEPT-115
    justification: >
      La crise de Bournemouth est encadrée par une formule démonologique qui révèle l’incompréhension de la maladie.

  - id: REL-S41-A147-CONCEPT-116
    source: S41-A147
    type: prolonge
    cible: CONCEPT-116
    justification: >
      Les erreurs de basse de « Disorder » deviennent partie intégrante du morceau publié.

  - id: REL-S41-A148-CONCEPT-117
    source: S41-A148
    type: prolonge
    cible: CONCEPT-117
    justification: >
      Les claviers imposés par Hannett sur « Day of the Lords » sont reconnus après coup par Hook comme justes.

  - id: REL-S41-A149-CONCEPT-117
    source: S41-A149
    type: prolonge
    cible: CONCEPT-117
    justification: >
      La contrainte d’écrire deux morceaux et la guitare inversée montrent la production comme contrainte féconde.

  - id: REL-S41-A150-CONCEPT-118
    source: S41-A150
    type: prolonge
    cible: CONCEPT-118
    justification: >
      « Insight » exemplifie la basse compositrice et l’intégration de l’environnement sonore enregistré par Hannett.

  - id: REL-S41-A151-CONCEPT-118
    source: S41-A151
    type: prolonge
    cible: CONCEPT-118
    justification: >
      Le Marshall de Hook relie timbre, composition et fragilité matérielle domestique.

  - id: REL-S41-A152-CONCEPT-119
    source: S41-A152
    type: prolonge
    cible: CONCEPT-119
    justification: >
      « She’s Lost Control » révèle l’écart entre sophistication sonore et découverte tardive du matériau médical des paroles.

  - id: REL-S41-A153-CONCEPT-118
    source: S41-A153
    type: prolonge
    cible: CONCEPT-118
    justification: >
      « Wilderness » et « Shadowplay » prolongent la basse motrice et les structures non conventionnelles.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A143
    source_id: S41
    atom_id: S41-A143
    title: "Licht und Blindheit : 1 578 exemplaires et logique contraire"
    chapters:
      - Chapitre 8
      - Chapitre 14
    tags:
      - licht-und-blindheit
      - sordide-sentimental
      - atmosphere
      - dead-souls
      - 1578
    query_boost:
      - "The run was 1,578 copies"
      - "Sordide Sentimental 1578 copies mail order only Joy Division"
    use_for:
      - anti-commercialisme Factory
      - Sordide Sentimental
    avoid_for:
      - clairvoyance stratégique totale

  - id: RAG-S41-A144
    source_id: S41
    atom_id: S41-A144
    title: "Atmosphere : deux moitiés assemblées"
    chapters:
      - Chapitre 4
      - Chapitre 8
      - Chapitre 12
    tags:
      - atmosphere
      - chance
      - woolies-organ
      - stephen-morris
      - peter-hook
    query_boost:
      - "Atmosphere was originally written in two halves"
      - "Chance Woolies organ bass and drums vocals keyboards"
    use_for:
      - genèse d’Atmosphere
      - chanson composite
    avoid_for:
      - lecture uniquement funéraire

  - id: RAG-S41-A145
    source_id: S41
    atom_id: S41-A145
    title: "Love Will Tear Us Apart : riff, batterie, refrain"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 12
    tags:
      - love-will-tear-us-apart
      - bass-riff
      - stephen-morris
      - second-peel-session
      - tj-davidsons
    query_boost:
      - "I had the riff Steve built the drum part"
      - "using the bass riff as the melody for the chorus"
    use_for:
      - genèse collective de LWTUA
      - mélodie issue de la basse
    avoid_for:
      - assignation du référent lyrique

  - id: RAG-S41-A146
    source_id: S41
    atom_id: S41-A146
    title: "Bournemouth : crise et regard démonologique"
    chapters:
      - Chapitre 12
      - Chapitre 14
    tags:
      - bournemouth
      - epilepsy
      - buzzcocks-tour
      - devil
      - heavy-medication
    query_boost:
      - "He’s possessed by the devil that twat"
      - "Bournemouth heavy medication wife baby affairs of the heart"
    use_for:
      - maladie mal interprétée
      - crises sur tournée Buzzcocks
    avoid_for:
      - romantisation démonologique

  - id: RAG-S41-A147
    source_id: S41
    atom_id: S41-A147
    title: "Disorder : erreurs de basse canonisées"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - disorder
      - bum-notes
      - bass
      - good-mistake
      - unknown-pleasures
    query_boost:
      - "It’s a mistake but it ended up being a good mistake"
      - "Disorder bum notes Peter Hook plectrum"
    use_for:
      - imperfection canonisée
      - track-by-track Unknown Pleasures
    avoid_for:
      - théorie générale de l’erreur

  - id: RAG-S41-A150
    source_id: S41
    atom_id: S41-A150
    title: "Insight : basse compositrice et lift Strawberry"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - insight
      - bass-riff
      - strawberry-lift
      - vocal-pumping
      - hannett
    query_boost:
      - "we used the bass to write the songs"
      - "creaky old freight lift in Strawberry"
    use_for:
      - basse compositrice
      - techniques Hannett
    avoid_for:
      - certitude technique non croisée

  - id: RAG-S41-A152
    source_id: S41
    atom_id: S41-A152
    title: "She’s Lost Control : Synare, aérosol et paroles médicales"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 12
    tags:
      - shes-lost-control
      - synare
      - aerosol
      - epilepsy
      - lyrics
    query_boost:
      - "Again I wasn’t really paying that much attention to the lyrics"
      - "Synare aerosol epileptic young lady"
    use_for:
      - production percussive
      - écoute différée des paroles
      - épilepsie et chanson
    avoid_for:
      - psychologisation totale de Curtis

  - id: RAG-S41-A153
    source_id: S41
    atom_id: S41-A153
    title: "Shadowplay / Wilderness : structure, religion, basse"
    chapters:
      - Chapitre 3
      - Chapitre 4
    tags:
      - shadowplay
      - wilderness
      - the-ocean
      - religion
      - monster-bass-line
    query_boost:
      - "Monster bass line"
      - "Shadowplay The Ocean Wilderness religion"
    use_for:
      - basse motrice
      - structures sans refrain
      - paroles et religion
    avoid_for:
      - lecture unique de Wilderness
```
