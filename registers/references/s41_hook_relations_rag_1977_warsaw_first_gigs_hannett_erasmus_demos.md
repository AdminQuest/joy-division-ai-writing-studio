# S41 — Relations stabilisées et entrées RAG — Warsaw, premiers concerts, Hannett/Erasmus, démos

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A025-CONCEPT-053
    source: S41-A025
    type: prolonge
    cible: CONCEPT-053
    justification: >
      Pete Shelley et les Buzzcocks fournissent à Warsaw un apprentissage pratique et une première scène.

  - id: REL-S41-A026-S41-A001
    source: S41-A026
    type: prépare
    cible: S41-A001
    justification: >
      Le passage de Stiff Kittens à Warsaw prépare la logique des noms froids et controversables qui culminera avec Joy Division.

  - id: REL-S41-A027-CONCEPT-054
    source: S41-A027
    type: prolonge
    cible: CONCEPT-054
    justification: >
      Le premier concert Warsaw fonctionne par incompétence, peur et croyance plutôt que par maîtrise technique.

  - id: REL-S41-A028-S41-A021
    source: S41-A028
    type: prolonge
    cible: S41-A021
    justification: >
      La désillusion devant les Heartbreakers prolonge l’usure de l’imaginaire punk initial.

  - id: REL-S41-A030-CONCEPT-050
    source: S41-A030
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Le Squat et Stuff the Jubilee inscrivent Warsaw dans la deuxième vague punk mancunienne.

  - id: REL-S41-A032-CONCEPT-055
    source: S41-A032
    type: prolonge
    cible: CONCEPT-055
    justification: >
      Hannett et Erasmus apparaissent d’abord dans un conflit de running order, avant toute stabilisation Factory.

  - id: REL-S41-A033-CONCEPT-043
    source: S41-A033
    type: prolonge
    cible: CONCEPT-043
    justification: >
      Curtis devient un problème scénique et organisationnel dans une physicalité encore non médicalisée.

  - id: REL-S41-A034-CONCEPT-049
    source: S41-A034
    type: prolonge
    cible: CONCEPT-049
    justification: >
      La démo Warsaw donne une trace sonore d’un groupe encore en apprentissage, mais déjà doté d’indices futurs.

  - id: REL-S41-A035-CONCEPT-054
    source: S41-A035
    type: prolonge
    cible: CONCEPT-054
    justification: >
      Le ratage des cassettes de Terry Mason montre comment le DIY peut saboter sa propre circulation.

  - id: REL-S41-A037-CONCEPT-056
    source: S41-A037
    type: prolonge
    cible: CONCEPT-056
    justification: >
      Stephen Morris stabilise la section rythmique et transforme la dynamique du groupe.

  - id: REL-S41-A038-CONCEPT-057
    source: S41-A038
    type: prolonge
    cible: CONCEPT-057
    justification: >
      Hook décrit Joy Division comme un archipel musical que Curtis tient ensemble.

  - id: REL-S41-A040-CONCEPT-058
    source: S41-A040
    type: prolonge
    cible: CONCEPT-058
    justification: >
      Short Circuit combine première opportunité discographique et premier piège publishing.

  - id: REL-S41-A041-CONCEPT-055
    source: S41-A041
    type: prolonge
    cible: CONCEPT-055
    justification: >
      Salford Technical College lie violence inter-scène, Gretton pré-manager et possible premier regard de Hannett.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A025
    source_id: S41
    atom_id: S41-A025
    title: "Buzzcocks comme école pratique"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - buzzcocks
      - pete-shelley
      - punk-ethos
      - warsaw
      - support-slot
    query_boost:
      - "proper punk ethos Pete Shelley Buzzcocks Warsaw"
      - "Buzzcocks support slot Warsaw first gig"
    use_for:
      - tutorat punk informel
      - infrastructure relationnelle
    avoid_for:
      - idéalisation générale de la scène

  - id: RAG-S41-A026
    source_id: S41
    atom_id: S41-A026
    title: "Warsaw : nom froid et austère"
    chapters:
      - Chapitre 5
      - Chapitre 6
    tags:
      - warsaw
      - stiff-kittens
      - low
      - warszawa
      - name
    query_boost:
      - "We picked it because it was cold and austere"
      - "Warsaw Stiff Kittens Warszawa Low"
    use_for:
      - construction esthétique du nom
      - préhistoire de Joy Division
    avoid_for:
      - programme esthétique trop stabilisé

  - id: RAG-S41-A033
    source_id: S41
    atom_id: S41-A033
    title: "Curtis à Rafters : violence scénique pré-médicale"
    chapters:
      - Chapitre 6
      - Chapitre 12
    tags:
      - ian-curtis
      - rafters
      - iggy-pop
      - broken-glass
      - performance
    query_boost:
      - "This was our mate going mental here"
      - "Ian Curtis Rafters broken glass table Iggy"
    use_for:
      - physicalité de Curtis
      - performance avant médicalisation
    avoid_for:
      - téléologie suicidaire ou médicale

  - id: RAG-S41-A034
    source_id: S41
    atom_id: S41-A034
    title: "Warsaw demo : Pennine Sound et The Kill"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - warsaw-demo
      - pennine-sound
      - the-kill
      - steve-brotherdale
      - transition
    query_boost:
      - "the sound of a band still finding its feet"
      - "Warsaw demo The Kill Pennine Sound"
    use_for:
      - démo de transition
      - premières traces studio
    avoid_for:
      - origine totale du son Joy Division

  - id: RAG-S41-A037
    source_id: S41
    atom_id: S41-A037
    title: "Stephen Morris : révélation rythmique"
    chapters:
      - Chapitre 3
      - Chapitre 6
    tags:
      - stephen-morris
      - drums
      - abraham-moss
      - jazz
      - rhythm-section
    query_boost:
      - "At last, we had a drummer"
      - "Stephen Morris jazz trio power texture punk"
    use_for:
      - arrivée de Morris
      - stabilisation rythmique
    avoid_for:
      - cause unique du son

  - id: RAG-S41-A040
    source_id: S41
    atom_id: S41-A040
    title: "Short Circuit : Rudolf Hess et publishing piégé"
    chapters:
      - Chapitre 5
      - Chapitre 8
      - Chapitre 11
    tags:
      - short-circuit
      - electric-circus
      - rudolf-hess
      - publishing
      - virgin
    query_boost:
      - "You all forgot Rudolf Hess"
      - "signed away in perpetuity"
      - "Short Circuit At a Later Date publishing Virgin"
    use_for:
      - controverse nazie
      - discographie
      - industrie musicale
    avoid_for:
      - lecture isolée de la provocation
```
