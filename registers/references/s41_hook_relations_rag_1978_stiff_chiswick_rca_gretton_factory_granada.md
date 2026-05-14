# S41 — Relations stabilisées et entrées RAG — Stiff/Chiswick, RCA, Gretton, Factory, Granada

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A065-CONCEPT-071
    source: S41-A065
    type: prépare
    cible: CONCEPT-071
    justification: >
      L’humiliation du booking par Hook explique structurellement pourquoi le groupe a besoin d’un manager réel.

  - id: REL-S41-A066-CONCEPT-069
    source: S41-A066
    type: prolonge
    cible: CONCEPT-069
    justification: >
      Le Stiff/Chiswick Challenge fonctionne comme audition punk concurrentielle, moitié tremplin, moitié champ de bataille local.

  - id: REL-S41-A067-CONCEPT-073
    source: S41-A067
    type: nuance
    cible: CONCEPT-073
    justification: >
      La reconnaissance de Wilson se construit dans le conflit et l’insistance, avant l’intégration Factory proprement dite.

  - id: REL-S41-A068-CONCEPT-070
    source: S41-A068
    type: prolonge
    cible: CONCEPT-070
    justification: >
      La commande Swan/RCA est une tentative commerciale qui n’est productive que par son rejet et sa transformation en Interzone.

  - id: REL-S41-A069-CONCEPT-070
    source: S41-A069
    type: prolonge
    cible: CONCEPT-070
    justification: >
      Les sessions RCA/Arrow représentent pour Hook le contre-modèle d’un son Joy Division rendu conventionnel.

  - id: REL-S41-A070-CONCEPT-071
    source: S41-A070
    type: prolonge
    cible: CONCEPT-071
    justification: >
      Gretton apparaît comme réponse organisationnelle au désordre du groupe, sans être encore la figure mythique de Factory.

  - id: REL-S41-A071-CONCEPT-071
    source: S41-A071
    type: prolonge
    cible: CONCEPT-071
    justification: >
      Les premières décisions de Gretton réparent les problèmes sonores, graphiques, financiers et documentaires accumulés.

  - id: REL-S41-A072-CONCEPT-071
    source: S41-A072
    type: prolonge
    cible: CONCEPT-071
    justification: >
      Le Transit de Hook convertit le booking de Gretton en autonomie matérielle et en économie de concerts.

  - id: REL-S41-A073-CONCEPT-072
    source: S41-A073
    type: prolonge
    cible: CONCEPT-072
    justification: >
      Transmission devient morceau-révélateur lorsque le soundcheck suspend le travail des personnes présentes.

  - id: REL-S41-A074-CONCEPT-073
    source: S41-A074
    type: prolonge
    cible: CONCEPT-073
    justification: >
      Le Russell Club inscrit Joy Division dans Factory comme club, affiche, réseau et événement avant le label.

  - id: REL-S41-A075-CONCEPT-050
    source: S41-A075
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Le Manchester Musicians’ Collective complète l’infrastructure punk mancunienne par une forme d’entraide procédurale.

  - id: REL-S41-A076-CONCEPT-074
    source: S41-A076
    type: prolonge
    cible: CONCEPT-074
    justification: >
      Le Band on the Wall montre Gretton réinvestissant les recettes dans le son, au prix d’une tension domestique autour de Curtis.

  - id: REL-S41-A077-CONCEPT-075
    source: S41-A077
    type: prolonge
    cible: CONCEPT-075
    justification: >
      Granada Reports constitue une première validation audiovisuelle régionale et une scène d’image administrée.

  - id: REL-S41-A078-CONCEPT-063
    source: S41-A078
    type: prolonge
    cible: CONCEPT-063
    justification: >
      Burnel et Simonon complètent la généalogie du style Hook : contrainte matérielle, timbre recherché et posture visuelle.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A066
    source_id: S41
    atom_id: S41-A066
    title: "Stiff/Chiswick : X Factor pour punks"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - stiff-test
      - chiswick-challenge
      - rafters
      - negatives
      - rob-gretton
      - tony-wilson
    query_boost:
      - "It was like The X Factor for punks"
      - "Stiff Chiswick Challenge Rafters Joy Division Negatives"
    use_for:
      - audition punk concurrentielle
      - reconnaissance Wilson/Gretton
    avoid_for:
      - audition providentielle unique

  - id: RAG-S41-A068
    source_id: S41
    atom_id: S41-A068
    title: "RCA/Swan : Keep On Keepin’ On devient Interzone"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 8
    tags:
      - rca
      - swan-records
      - nf-porter
      - keep-on-keeping-on
      - interzone
    query_boost:
      - "Keep On Keepin On Interzone Peter Hook RCA"
      - "it changed into something completely different Interzone"
    use_for:
      - transformation créative par rejet
      - origine circonstancielle d’Interzone
    avoid_for:
      - réduction d’Interzone à une reprise

  - id: RAG-S41-A069
    source_id: S41
    atom_id: S41-A069
    title: "Arrow Studios / RCA : anti-Joy Division sonore"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - rca
      - arrow-studios
      - john-anderson
      - bootlegs
      - commercial-sound
    query_boost:
      - "what a turkey it was"
      - "Arrow Studios John Anderson backing vocals Joy Division"
    use_for:
      - commercialisation déformante
      - RCA sessions source-cadre Hook
    avoid_for:
      - détails Strawberry non attribués à Hook seul

  - id: RAG-S41-A070
    source_id: S41
    atom_id: S41-A070
    title: "Arrivée de Rob Gretton comme manager"
    chapters:
      - Chapitre 6
      - Chapitre 10
    tags:
      - rob-gretton
      - manager
      - tj-davidsons
      - stiffe-chiswick
      - notebooks
    query_boost:
      - "I want to be your manager"
      - "Rob Gretton T. J. Davidson’s we manager Joy Division"
    use_for:
      - bascule managériale
      - organisation du groupe
    avoid_for:
      - héroïsation de Gretton

  - id: RAG-S41-A071
    source_id: S41
    atom_id: S41-A071
    title: "Gretton corrige An Ideal for Living et les bandes RCA"
    chapters:
      - Chapitre 5
      - Chapitre 8
      - Chapitre 10
    tags:
      - an-ideal-for-living
      - nazi-artwork
      - twelve-inch
      - rabid-records
      - arrow-tapes
    query_boost:
      - "We need to get rid of this Nazi artwork too"
      - "King Street scaffolding An Ideal for Living twelve inch Gretton"
    use_for:
      - management réparateur
      - correction graphique et sonore
    avoid_for:
      - sauveur providentiel

  - id: RAG-S41-A073
    source_id: S41
    atom_id: S41-A073
    title: "Transmission au Mayflower : stop-the-press moment"
    chapters:
      - Chapitre 3
      - Chapitre 4
      - Chapitre 6
    tags:
      - transmission
      - mayflower
      - soundcheck
      - oz-pa
      - emergency
    query_boost:
      - "a real stop-the-press moment Transmission Mayflower"
      - "Transmission sound-check Mayflower Emergency Risk Oz PA"
    use_for:
      - morceau-révélateur live
      - confiance du groupe
    avoid_for:
      - canonisation immédiate du single

  - id: RAG-S41-A074
    source_id: S41
    atom_id: S41-A074
    title: "Factory au Russell Club : Factory avant label"
    chapters:
      - Chapitre 6
      - Chapitre 8
      - Chapitre 14
    tags:
      - factory-club
      - russell-club
      - fac-1
      - peter-saville
      - alan-erasmus
    query_boost:
      - "the first Factory event to involve us"
      - "Russell Club FAC 1 Factory Clearance Saville"
    use_for:
      - Factory avant label
      - entrée dans orbite Wilson/Erasmus/Saville
    avoid_for:
      - téléologie Factory Records

  - id: RAG-S41-A077
    source_id: S41
    atom_id: S41-A077
    title: "Granada Reports / Shadowplay : première télévision"
    chapters:
      - Chapitre 5
      - Chapitre 6
      - Chapitre 14
    tags:
      - granada-reports
      - shadowplay
      - tony-wilson
      - bob-greaves
      - salford
    query_boost:
      - "the most interesting sound we’ve come across in the last six months"
      - "Granada Reports Shadowplay Joy Division Salford guitarist"
    use_for:
      - reconnaissance télévisuelle locale
      - image Joy Division
    avoid_for:
      - consécration nationale immédiate

  - id: RAG-S41-A078
    source_id: S41
    atom_id: S41-A078
    title: "Burnel et Simonon : son et posture de basse"
    chapters:
      - Chapitre 3
      - Chapitre 5
    tags:
      - jean-jacques-burnel
      - paul-simonon
      - bass-sound
      - low-strap
      - peter-hook
    query_boost:
      - "I got my sound from Jean-Jacques and my strap from Paul Simonon"
      - "Hook Burnel Simonon bass sound strap"
    use_for:
      - influences instrumentales
      - style Hook son/image
    avoid_for:
      - réduction du style à deux influences
```
