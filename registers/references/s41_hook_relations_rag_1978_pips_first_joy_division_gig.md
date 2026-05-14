# S41 — Relations stabilisées et entrées RAG — Pips et premier concert Joy Division

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A001-MYTH-007
    source: S41-A001
    type: nuance
    cible: MYTH-007
    justification: >
      Hook confirme l’origine *House of Dolls* du nom, mais reformule la controverse en défense salfordienne et punk plutôt qu’en idéologie.

  - id: REL-S41-A001-CONCEPT-025
    source: S41-A001
    type: prolonge
    cible: CONCEPT-025
    justification: >
      Le passage impose une contextualisation sans excuse : comprendre la provocation sans neutraliser sa charge éthique.

  - id: REL-S41-A002-CONCEPT-043
    source: S41-A002
    type: prolonge
    cible: CONCEPT-043
    justification: >
      Curtis prépare une entrée scénique mais devient immédiatement un problème pratique pour le concert.

  - id: REL-S41-A003-CONCEPT-043
    source: S41-A003
    type: prolonge
    cible: CONCEPT-043
    justification: >
      Le chanteur indispensable doit être récupéré auprès du bouncer pour que le concert puisse commencer.

  - id: REL-S41-A004-CONCEPT-041
    source: S41-A004
    type: prolonge
    cible: CONCEPT-041
    justification: >
      La panne de basse contredit toute vision d’une naissance maîtrisée du groupe.

  - id: REL-S41-A005-CONCEPT-041
    source: S41-A005
    type: prolonge
    cible: CONCEPT-041
    justification: >
      La bagarre du public intime rend l’origine scénique socialement chaotique.

  - id: REL-S41-A006-MYTH-002
    source: S41-A006
    type: nuance
    cible: MYTH-002
    justification: >
      Le premier concert officiel Joy Division relève du ratage matériel et social avant toute aura tragique.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A001
    source_id: S41
    atom_id: S41-A001
    title: "Le nom Joy Division : House of Dolls et défense salfordienne"
    chapters:
      - Chapitre 5
      - Chapitre 11
    tags:
      - joy-division-name
      - house-of-dolls
      - nazism-controversy
      - salford
      - peter-hook
    query_boost:
      - "No. We’re not fucking Nazis. We’re from Salford."
      - "House of Dolls Joy Division Peter Hook"
      - "Joy Division name oppressed not oppressors"
    use_for:
      - controverse du nom
      - contextualisation sans excuse
      - défense rétrospective de Hook
    avoid_for:
      - excuse sociale totale
      - preuve d’innocence politique complète

  - id: RAG-S41-A002
    source_id: S41
    atom_id: S41-A002
    title: "Trans-Europe Express à Pips"
    chapters:
      - Chapitre 6
    tags:
      - pips
      - kraftwerk
      - trans-europe-express
      - ian-curtis
      - intro-music
    query_boost:
      - "Trans-Europe Express Pips Ian Curtis"
      - "He loved that record"
      - "kicking broken glass Trans-Europe Express"
    use_for:
      - rituel d’entrée scénique
      - Kraftwerk et Joy Division
      - désordre pré-scénique
    avoid_for:
      - programme esthétique entièrement conscient

  - id: RAG-S41-A004
    source_id: S41
    atom_id: S41-A004
    title: "Hondo II et basse défaillante"
    chapters:
      - Chapitre 3
      - Chapitre 6
    tags:
      - peter-hook
      - bass
      - hondo-ii
      - pips
      - technical-failure
    query_boost:
      - "Boing Hondo II Rickenbacker Copy"
      - "string flipped off the guitar Pips"
    use_for:
      - anti-mythe technique
      - débuts matériels de Hook
    avoid_for:
      - analyse sonore générale du style Hook

  - id: RAG-S41-A006
    source_id: S41
    atom_id: S41-A006
    title: "Premier concert Joy Division comme anti-mythe fondateur"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - first-gig
      - pips
      - joy-division
      - fight
      - origin-myth
    query_boost:
      - "Our first gig as Joy Division"
      - "didn’t play another one for almost two months"
      - "first gig Joy Division ended in a fight"
    use_for:
      - naissance publique du groupe
      - anti-mythe fondateur
      - chaos live
    avoid_for:
      - téléologie tragique
```
