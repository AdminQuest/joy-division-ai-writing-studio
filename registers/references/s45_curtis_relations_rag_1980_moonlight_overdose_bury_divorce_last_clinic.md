# S45 — Relations stabilisées et entrées RAG — Moonlight, overdose, Bury, divorce, dernier rendez-vous médical

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A133-CONCEPT-026
    source: S45-A133
    type: prolonge
    cible: CONCEPT-026
    justification: >
      Le calendrier Moonlight / Rainbow montre que la professionnalisation empêche concrètement le repos médical.

  - id: REL-S45-A134-CONCEPT-037
    source: S45-A134
    type: prolonge
    cible: CONCEPT-037
    justification: >
      Les crises de Curtis deviennent une composante attendue de la performance pour une part du public.

  - id: REL-S45-A135-CONCEPT-034
    source: S45-A135
    type: prolonge
    cible: CONCEPT-034
    justification: >
      La présence d’Annik transforme une crise scénique en humiliation intime et confirme la contradiction genrée de tournée.

  - id: REL-S45-A136-CONCEPT-019
    source: S45-A136
    type: prolonge
    cible: CONCEPT-019
    justification: >
      L’overdose de Phenobarbitone doit être inscrite dans le faisceau maladie, médicaments, relation Annik, tournée, fatigue et solitude.

  - id: REL-S45-A137-CONCEPT-038
    source: S45-A137
    type: prolonge
    cible: CONCEPT-038
    justification: >
      L’intervention Wilson / Reade / Erasmus illustre Factory comme entourage de care amateur et de dépossession documentaire.

  - id: REL-S45-A138-CONCEPT-038
    source: S45-A138
    type: prolonge
    cible: CONCEPT-038
    justification: >
      Le déplacement de Curtis à Charlesworth externalise le care et retire l’accès à Deborah.

  - id: REL-S45-A139-CONCEPT-039
    source: S45-A139
    type: prolonge
    cible: CONCEPT-039
    justification: >
      Bury constitue le cas paradigmatique du concert impossible maintenu.

  - id: REL-S45-A140-CONCEPT-038
    source: S45-A140
    type: prolonge
    cible: CONCEPT-038
    justification: >
      Yeats et l’hypnose montrent des tentatives de soin culturel ou amateur sans dispositif médical stabilisé.

  - id: REL-S45-A141-CONCEPT-036
    source: S45-A141
    type: prolonge
    cible: CONCEPT-036
    justification: >
      La scène du Factory révèle à Deborah le dispositif logistique de Closer et son exclusion pratique.

  - id: REL-S45-A142-CONCEPT-021
    source: S45-A142
    type: prolonge
    cible: CONCEPT-021
    justification: >
      L’anniversaire de Natalie sans son père montre le déplacement du care entre Deborah et Lindsay Reade.

  - id: REL-S45-A143-CONCEPT-029
    source: S45-A143
    type: prolonge
    cible: CONCEPT-029
    justification: >
      Le calme apparent du repas d’Alderley Edge ne répare pas la vérité conjugale différée.

  - id: REL-S45-A144-CONCEPT-036
    source: S45-A144
    type: prolonge
    cible: CONCEPT-036
    justification: >
      La vidéo de Love Will Tear Us Apart est produite alors que la crise intime est suspendue par les impératifs professionnels.

  - id: REL-S45-A145-CONCEPT-026
    source: S45-A145
    type: prolonge
    cible: CONCEPT-026
    justification: >
      Le désir de quitter Joy Division et le rendez-vous manqué de Parkside signalent l’impossibilité de sortie du dispositif professionnel.

  - id: REL-S45-A146-CONCEPT-029
    source: S45-A146
    type: prolonge
    cible: CONCEPT-029
    justification: >
      Le secret conjugal sort du cercle du groupe et devient affaire parentale, juridique et familiale.

  - id: REL-S45-A147-CONCEPT-021
    source: S45-A147
    type: nuance
    cible: CONCEPT-021
    justification: >
      La sortie avec Jeff montre Deborah sortant un instant du rôle de soignante et d’épouse effacée.

  - id: REL-S45-A148-CONCEPT-035
    source: S45-A148
    type: requiert
    cible: CONCEPT-035
    justification: >
      La phrase sur les lésions cérébrales doit rester un indice d’ambivalence, non une preuve d’intention.

  - id: REL-S45-A149-CONCEPT-035
    source: S45-A149
    type: prolonge
    cible: CONCEPT-035
    justification: >
      Le rendez-vous psychiatrique oppose deux présentations incompatibles : Deborah effondrée, Ian calme.

  - id: REL-S45-A150-CONCEPT-038
    source: S45-A150
    type: prolonge
    cible: CONCEPT-038
    justification: >
      Le minder de tournée est une réponse managériale à un problème qui aurait peut-être nécessité hospitalisation.

  - id: REL-S45-A151-CONCEPT-040
    source: S45-A151
    type: prolonge
    cible: CONCEPT-040
    justification: >
      Le dernier rendez-vous d’épilepsie produit une impression favorable qui masque possiblement un calme trompeur.

  - id: REL-S45-A152-CONCEPT-040
    source: S45-A152
    type: prolonge
    cible: CONCEPT-040
    justification: >
      La dernière photographie est un signe final affectif mais non une preuve intentionnelle.

  - id: REL-S45-A153-CONCEPT-040
    source: S45-A153
    type: prolonge
    cible: CONCEPT-040
    justification: >
      Stroszek et l’Amérique doivent être lus comme miroir final, non cause unique.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A133
    source_id: S45
    atom_id: S45-A133
    title: "Moonlight / Rainbow : calendrier pathogène"
    chapters:
      - Chapitre 6
      - Chapitre 12
    tags:
      - moonlight
      - rainbow
      - epilepsy
      - live-schedule
      - sleep
    query_boost:
      - "we did some gigs that we shouldn’t have done"
      - "Moonlight Rainbow Stranglers Ian Curtis fit"
    use_for:
      - calendrier contre soin
      - non-monocausalité médicale
    avoid_for:
      - cause unique

  - id: RAG-S45-A134
    source_id: S45
    atom_id: S45-A134
    title: "Crises sur scène comme partie attendue de l’acte"
    chapters:
      - Chapitre 12
      - Chapitre 14
    tags:
      - stage-fit
      - performance
      - audience
      - illness
      - myth
    query_boost:
      - "expected part of Joy Division’s act"
      - "Ian Curtis fit on stage expected part"
    use_for:
      - maladie spectaculaire
      - réception du corps malade
    avoid_for:
      - accusation univoque du public

  - id: RAG-S45-A136
    source_id: S45
    atom_id: S45-A136
    title: "Overdose de Phenobarbitone du 7 avril"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - overdose
      - phenobarbitone
      - suicide-note
      - annik
      - rob-gretton
    query_boost:
      - "no need to fight now"
      - "give his love to Annik"
      - "Phenobarbitone overdose Deborah Curtis"
    use_for:
      - tentative de suicide
      - note comme preuve fragmentaire
    avoid_for:
      - causalité romantique unique

  - id: RAG-S45-A139
    source_id: S45
    atom_id: S45-A139
    title: "Derby Hall Bury : concert impossible maintenu"
    chapters:
      - Chapitre 6
      - Chapitre 12
      - Chapitre bootlegs
    tags:
      - bury
      - derby-hall
      - riot
      - harry-demac
      - bootleg
      - rob-gretton
    query_boost:
      - "Derby Hall Bury complete riot"
      - "Harry Demac four-track recording"
      - "the gig probably seemed more important than it was"
    use_for:
      - live crise
      - bootlegs
      - inertie professionnelle
    avoid_for:
      - responsabilité unique de Gretton

  - id: RAG-S45-A144
    source_id: S45
    atom_id: S45-A144
    title: "Love Will Tear Us Apart vidéo et productivité sous crise"
    chapters:
      - Chapitre 5
      - Chapitre 12
      - Chapitre 14
    tags:
      - love-will-tear-us-apart
      - video
      - music-business
      - crisis
      - factory
    query_boost:
      - "music-business puppet"
      - "Love Will Tear Us Apart video recorded 25 April 1980"
    use_for:
      - objet canonique sous crise
      - audiovisuel
    avoid_for:
      - réduction à exploitation

  - id: RAG-S45-A149
    source_id: S45
    atom_id: S45-A149
    title: "Rendez-vous psychiatrique : dernière occasion manquée"
    chapters:
      - Chapitre 12
      - Chapitre 10
    tags:
      - psychiatrist
      - parkside
      - terry-mason
      - deborah-curtis
      - medical-care
    query_boost:
      - "This was the best opportunity he’d had to get help"
      - "I might I might not"
      - "I’m never coming home"
    use_for:
      - collision des récits médicaux
      - care professionnel manqué
    avoid_for:
      - accusation médicale simpliste

  - id: RAG-S45-A151
    source_id: S45
    atom_id: S45-A151
    title: "Dernier rendez-vous d’épilepsie et dons d’objets"
    chapters:
      - Chapitre 8
      - Chapitre 12
    tags:
      - epilepsy-clinic
      - terry-mason
      - sordide-sentimentale
      - atmosphere
      - dead-souls
      - objects
    query_boost:
      - "Sordide Sentimentale single Atmosphere Dead Souls serial number 1106"
      - "finally getting his life together epilepsy clinic"
    use_for:
      - objets donnés
      - calme trompeur final
    avoid_for:
      - signe suicidaire certain

  - id: RAG-S45-A153
    source_id: S45
    atom_id: S45-A153
    title: "Stroszek et deadline américaine"
    chapters:
      - Chapitre 12
      - Chapitre 14
    tags:
      - stroszek
      - werner-herzog
      - american-tour
      - deadline
      - final-weekend
    query_boost:
      - "I believe Ian chose his deadline"
      - "Stroszek American tour Ian Curtis Deborah Curtis"
    use_for:
      - calme trompeur final
      - film miroir dangereux
    avoid_for:
      - cause unique du suicide
```
