# Registres spécialisés — S43 — Capozzi, *The weight on their shoulders*, 2021

```yaml
source_id: S43
source_label: "S43 — Capozzi, The weight on their shoulders, 2021"
type_unite: registres_specialises
statut: verifie
fiabilite: forte comme source secondaire critique
passage_atomise: "Chapitre complet, p. PDF 64-75"
```

## 1. Concepts structurants à consolider

### CONCEPT-S43-001 — Seconde génération des baby-boomers

```yaml
id: CONCEPT-S43-001
label: "seconde génération des baby-boomers"
source_id: S43
atoms:
  - S43-A002
  - S43-A004
  - S43-A014
chapitres:
  - Chapitre 11
  - Chapitre 14
statut: a_integrer
```

Concept utile pour penser Curtis non comme pur cas individuel, mais comme point de condensation d’une cohorte née dans la normalisation de la golden age occidentale.

### CONCEPT-S43-002 — Révolte sans utopie

```yaml
id: CONCEPT-S43-002
label: "révolte sans utopie"
source_id: S43
atoms:
  - S43-A003
  - S43-A005
  - S43-A006
chapitres:
  - Chapitre 4
  - Chapitre 11
statut: a_integrer
```

Concept central : le punk n’est pas traité comme simple explosion de colère, mais comme révolte privée d’horizon communautaire stable.

### CONCEPT-S43-003 — Jeune vieux / sénescence anticipée

```yaml
id: CONCEPT-S43-003
label: "jeune vieux / sénescence anticipée"
source_id: S43
atoms:
  - S43-A009
  - S43-A014
chapitres:
  - Chapitre 4
  - Chapitre 11
statut: a_integrer
```

Motif de la jeunesse déjà épuisée, particulièrement utile pour lire « Insight » et « Decades » sans biographisme étroit.

### CONCEPT-S43-004 — Sympathie comme thérapie impossible

```yaml
id: CONCEPT-S43-004
label: "sympathie comme thérapie impossible"
source_id: S43
atoms:
  - S43-A012
  - S43-A013
chapitres:
  - Chapitre 11
  - Chapitre 12
statut: a_integrer
```

Notion à manier comme concept de Capozzi, non comme concept explicitement revendiqué par Curtis.

### CONCEPT-S43-005 — Dernière parole au « nous »

```yaml
id: CONCEPT-S43-005
label: "dernière parole au nous"
source_id: S43
atoms:
  - S43-A014
  - S43-A015
chapitres:
  - Chapitre 4
  - Chapitre 11
  - Chapitre 14
statut: a_integrer
```

Concept terminal : la catastrophe intime est reformulée comme expérience collective et générationnelle.

## 2. Motifs à consolider

```yaml
motifs:
  - id: MOTIF-S43-001
    label: "poids sur les épaules"
    source_id: S43
    atoms: [S43-A014]
    chapters: [Chapitre 4, Chapitre 11, Chapitre 14]
  - id: MOTIF-S43-002
    label: "communauté perdue"
    source_id: S43
    atoms: [S43-A012, S43-A013, S43-A014]
    chapters: [Chapitre 11, Chapitre 12, Chapitre 14]
  - id: MOTIF-S43-003
    label: "guide introuvable"
    source_id: S43
    atoms: [S43-A008]
    chapters: [Chapitre 4, Chapitre 11]
  - id: MOTIF-S43-004
    label: "retrait thérapeutique impossible"
    source_id: S43
    atoms: [S43-A011, S43-A012]
    chapters: [Chapitre 11, Chapitre 12]
  - id: MOTIF-S43-005
    label: "jeunes hommes épuisés"
    source_id: S43
    atoms: [S43-A009, S43-A014]
    chapters: [Chapitre 4, Chapitre 11, Chapitre 14]
```

## 3. Mythes et risques historiographiques

```yaml
mythes:
  - id: MYTHE-S43-001
    label: "Closer annonce directement le suicide"
    statut: a_deconstruire
    source_id: S43
    garde_fou: "Capozzi parle d’un accomplissement poétique du détachement, non d’une preuve causale."
    atoms: [S43-A010, S43-A015]
  - id: MYTHE-S43-002
    label: "Curtis porte objectivement toute sa génération"
    statut: a_nuancer
    source_id: S43
    garde_fou: "Capozzi propose une lecture générationnelle, pas un mandat sociologique de Curtis."
    atoms: [S43-A001, S43-A004, S43-A014]
  - id: MYTHE-S43-003
    label: "L’épilepsie explique l’œuvre"
    statut: a_deconstruire
    source_id: S43
    garde_fou: "S43 n’est pas une source clinique. Croiser avec les sources directes et médicales."
    atoms: [S43-A007, S43-A015]
```

## 4. Registre des citations à contrôler

Les extraits de chansons cités par Capozzi sont utiles comme signaux de lecture, mais ne deviennent pas des citations vérifiées du manuscrit. Toute citation doit être reprise depuis une source lyrique fiable et enregistrée séparément dans le registre des citations.

```yaml
citations_a_controler:
  - id: QUOTE-S43-001
    source_id: S43
    chanson: "Born in the Fifties"
    artiste: "The Police"
    usage: "ouverture générationnelle"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-002
    source_id: S43
    chanson: "Leaders of Men"
    artiste: "Joy Division"
    usage: "anti-messianisme et critique des leaders"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-003
    source_id: S43
    chanson: "Disorder"
    artiste: "Joy Division"
    usage: "appel au guide"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-004
    source_id: S43
    chanson: "Insight"
    artiste: "Joy Division"
    usage: "jeunesse perdue et sénescence anticipée"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-005
    source_id: S43
    chanson: "Twenty Four Hours"
    artiste: "Joy Division"
    usage: "sympathie comme thérapie impossible"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-006
    source_id: S43
    chanson: "The Eternal"
    artiste: "Joy Division"
    usage: "communion perdue et contemplation"
    statut: a_verifier_avant_usage
  - id: QUOTE-S43-007
    source_id: S43
    chanson: "Decades"
    artiste: "Joy Division"
    usage: "nous générationnel"
    statut: a_verifier_avant_usage
```

## 5. Chronologie et événements à enregistrer prudemment

S43 ne fournit pas de chronologie originale. Les événements qui apparaissent doivent être rattachés à des sources historiques ou testimoniales principales.

```yaml
chronologie_a_croiser:
  - id: CHR-S43-001
    date: "1978"
    label: "Publication d’An Ideal for Living"
    source_id: S43
    statut: a_croiser
    croiser_avec: [S41, S45, S46, S47, S75, S76]
  - id: CHR-S43-002
    date: "1979"
    label: "Publication d’Unknown Pleasures"
    source_id: S43
    statut: a_croiser
    croiser_avec: [S41, S46, S47, S75, S76]
  - id: CHR-S43-003
    date: "1980-05"
    label: "Mort de Ian Curtis"
    source_id: S43
    statut: a_croiser
    croiser_avec: [S41, S45, S46, S47, S76]
  - id: CHR-S43-004
    date: "1980"
    label: "Publication posthume de Closer"
    source_id: S43
    statut: a_croiser
    croiser_avec: [S41, S46, S47, S75, S76]
```

## 6. Acteurs, lieux, organisations, chansons

```yaml
acteurs:
  - Ian Curtis
  - Eugenio Capozzi
  - Martin Hannett
  - Annik Honoré
  - Sting
  - Rudolf Hess
  - Albert Camus
  - Giacomo Leopardi
  - David Bowie
  - Iggy Pop
  - Jim Morrison
  - William S. Burroughs
  - J. G. Ballard
  - Franz Kafka
  - Nikolai Gogol
  - Fyodor Dostoevsky

lieux:
  - Manchester
  - Manchester ouvrière

organisations:
  - Joy Division
  - The Police

chansons:
  - Born in the Fifties
  - Leaders of Men
  - Failures
  - Disorder
  - Candidate
  - She's Lost Control
  - Shadowplay
  - Insight
  - I Remember Nothing
  - Atrocity Exhibition
  - Isolation
  - Passover
  - Twenty Four Hours
  - The Eternal
  - Decades
  - Love Will Tear Us Apart

albums:
  - An Ideal for Living
  - Unknown Pleasures
  - Closer
```
