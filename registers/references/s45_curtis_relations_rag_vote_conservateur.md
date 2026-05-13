# S45 — Relations stabilisées et entrée RAG — vote conservateur rapporté

Ce fichier consolide les relations et l’indexation RAG du passage atomisé dans `sources/curtis_touching_from_a_distance/source_part_vote_conservateur.md`.

---

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A019-MYTH-003
    source: S45-A019
    type: nuance
    cible: MYTH-003
    justification: >
      L’anecdote introduit une discordance entre la matrice mancunienne et les
      comportements politiques individuels ; Manchester conditionne, mais ne
      détermine pas mécaniquement.

  - id: REL-S45-A019-MYTH-011
    source: S45-A019
    type: nuance
    cible: MYTH-011
    justification: >
      Le passage interdit de projeter sur Curtis une position politique attendue
      du milieu ou de l’esthétique post-punk.

  - id: REL-S45-A019-CONCEPT-010
    source: S45-A019
    type: prolonge
    cible: CONCEPT-010
    justification: >
      L’atome constitue un cas d’application de l’anti-déterminisme sociologique.

  - id: REL-S45-A019-CONCEPT-004
    source: S45-A019
    type: requiert
    cible: CONCEPT-004
    justification: >
      La scène exige de distinguer témoignage, anecdote, reconstruction et usage
      argumentatif.

  - id: REL-S45-A020-FORMULATION-VOTE-THATCHER
    source: S45-A020
    type: corrige
    cible: FORMULATION-IAN-CURTIS-VOTE-THATCHER
    justification: >
      Le passage établit un vote conservateur rapporté, non un vote Thatcher
      explicitement documenté.

  - id: REL-S45-A020-REGISTRE-CITATIONS
    source: S45-A020
    type: stabilise
    cible: REGISTRE-CITATIONS-VERIFIEES
    justification: >
      La citation doit être conservée comme candidate vérifiée sur OCR, avec
      pagination papier et PDF à verrouiller.

  - id: REL-S45-A020-RISQUE-SURTRADUCTION-POLITIQUE
    source: S45-A020
    type: alerte
    cible: RISQUE-SURTRADUCTION-POLITIQUE
    justification: >
      « Conservateur » ne doit pas être surtraduit en « thatchérien » sans source
      complémentaire.
```

---

## Entrée RAG candidate

```yaml
rag_index:
  - id: RAG-S45-A019
    source_id: S45
    atom_id: S45-A019
    title: Vote conservateur rapporté par Deborah Curtis
    chapters:
      - Chapitre 1
      - Chapitre 10
    tags:
      - deborah-curtis
      - ian-curtis
      - politique
      - conservatisme
      - anti-determinisme
      - manchester
      - mythe
      - prudence-historiographique
    query_boost:
      - "Ian Curtis voted Conservative"
      - "vote conservateur Ian Curtis"
      - "Curtis Thatcher prudence"
      - "Joy Division politique Manchester"
      - "Deborah Curtis vote Conservative"
    use_for:
      - nuancer lecture sociale de Joy Division
      - éviter déterminisme Manchester
      - corriger formulation vote Thatcher
      - illustrer contradiction biographique
    avoid_for:
      - diagnostic psychologique
      - portrait idéologique complet de Curtis
      - preuve d’adhésion thatchérienne
      - lecture anti-sociale de Joy Division
```

---

## Formulations contrôlées

```yaml
formulations_autorisees:
  - "Deborah Curtis rapporte qu’Ian Curtis vote conservateur lors d’une élection locale."
  - "L’anecdote introduit une discordance utile avec la lecture homogène d’un Joy Division politiquement lisible par son seul contexte."
  - "Le passage impose une prudence : conservateur ne signifie pas, à lui seul, thatchérien."

formulations_a_proscrire_sans_source_complementaire:
  - "Ian Curtis vote Thatcher."
  - "Ian Curtis est thatchérien."
  - "Joy Division exprime politiquement le conservatisme de Curtis."
  - "Le vote de Curtis contredit le rôle du contexte social mancunien."
```
