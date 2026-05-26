# S45 — Relations stabilisées et entrées RAG — *An Ideal for Living*, travail social, RCA

Ce fichier consolide les relations et l’indexation RAG du passage atomisé dans `sources/curtis_touching_from_a_distance/source_part_1977_1978_an_ideal_rca.md`.

---

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A035-CONCEPT-009
    source: S45-A035
    type: prolonge
    cible: CONCEPT-009
    justification: >
      Le travail de Curtis auprès des personnes handicapées socialise la question
      médicale avant le diagnostic personnel.

  - id: REL-S45-A036-RISQUE-TELEOLOGIE-MEDICALE
    source: S45-A036
    type: alerte
    cible: RISQUE-TELEOLOGIE-MEDICALE
    justification: >
      Le cours sur l’épilepsie produit une ironie biographique, pas une prophétie.

  - id: REL-S45-A037-MYTH-007
    source: S45-A037
    type: requiert
    cible: MYTH-007
    justification: >
      *Short Circuit* conserve le souvenir Hess et doit être traité dans le cadre
      de la controverse sur l’imagerie.

  - id: REL-S45-A038-MYTH-002
    source: S45-A038
    type: nuance
    cible: MYTH-002
    justification: >
      Le débordement scénique doit être lu comme performance dangereuse, non
      comme prophétie de la mort.

  - id: REL-S45-A040-CONCEPT-013
    source: S45-A040
    type: prolonge
    cible: CONCEPT-013
    justification: >
      Le financement par prêt bancaire sur compte commun fonde l’économie
      domestique du premier disque.

  - id: REL-S45-A041-S45-A040
    source: S45-A041
    type: prolonge
    cible: S45-A040
    justification: >
      La dette domestique débouche sur un objet totalement bricolé : session,
      pochette, pliage, conditionnement.

  - id: REL-S45-A042-MYTH-007
    source: S45-A042
    type: prolonge
    cible: MYTH-007
    justification: >
      La pochette d’*An Ideal for Living* est un nœud majeur de l’imagerie nazie
      et de sa réception litigieuse.

  - id: REL-S45-A043-MOTIF-006
    source: S45-A043
    type: prolonge
    cible: MOTIF-006
    justification: >
      Le Swinging Apple agit comme seuil modeste et anti-triomphal entre Warsaw
      et Joy Division.

  - id: REL-S45-A044-MYTH-007
    source: S45-A044
    type: prolonge
    cible: MYTH-007
    justification: >
      Le nom Joy Division engage explicitement la question des prisonnières
      sexuelles et de la charge morale du terme.

  - id: REL-S45-A045-MOTIF-006
    source: S45-A045
    type: prolonge
    cible: MOTIF-006
    justification: >
      Pips est la première apparition publique sous le nom Joy Division ; seuil
      nominal et scénique.

  - id: REL-S45-A046-S45-A019
    source: S45-A046
    type: prolonge
    cible: S45-A019
    justification: >
      La rupture politique avec Tony Nuttall complète le vote conservateur rapporté
      par Deborah Curtis.

  - id: REL-S45-A048-CONCEPT-auto-habilitation-artistique
    source: S45-A048
    type: prolonge
    cible: CONCEPT-auto-habilitation-artistique
    justification: >
      Le Manchester Musicians’ Collective donne une forme concrète à l’auto-
      habilitation artistique.

  - id: REL-S45-A049-CONCEPT-014
    source: S45-A049
    type: prépare
    cible: CONCEPT-014
    justification: >
      Le bureau RCA de Piccadilly Plaza prépare l’anti-récit RCA comme rencontre
      locale avec l’industrie.

  - id: REL-S45-A050-CONCEPT-014
    source: S45-A050
    type: prolonge
    cible: CONCEPT-014
    justification: >
      Le désir d’enregistrer et l’absence de discussion structurée constituent le
      cœur de l’anti-récit RCA.

  - id: REL-S45-A051-CONCEPT-006
    source: S45-A051
    type: prolonge
    cible: CONCEPT-006
    justification: >
      Les tensions sur la voix, le synthétiseur et le répertoire participent à la
      définition négative de l’architecture sonore.

  - id: REL-S45-A052-CONCEPT-013
    source: S45-A052
    type: prolonge
    cible: CONCEPT-013
    justification: >
      Deborah Curtis et Sue Barlow participent à la production sociale minimale
      du groupe comme faux public.
```

---

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A035
    source_id: S45
    atom_id: S45-A035
    title: Curtis à l’Employment Exchange et le handicap au travail
    chapters:
      - Chapitre 12
      - Chapitre 10
    tags:
      - ian-curtis
      - employment-exchange
      - disability
      - epilepsy
      - ernest-beard
      - travail-social
    query_boost:
      - "Assistant Disablement Resettlement Officer"
      - "Employment Exchange Macclesfield Ian Curtis"
      - "Curtis epilepsy course Department"
    use_for:
      - socialiser la question de l’épilepsie
      - éviter téléologie médicale
      - contextualiser handicap et travail
    avoid_for:
      - prophétie de la maladie
      - preuve médicale

  - id: RAG-S45-A040
    source_id: S45
    atom_id: S45-A040
    title: Les 400 livres d’An Ideal for Living
    chapters:
      - Chapitre 2
      - Chapitre 8
    tags:
      - an-ideal-for-living
      - deborah-curtis
      - diy
      - prêt-bancaire
      - économie-domestique
    query_boost:
      - "£400 towards the recording and pressing"
      - "An Ideal for Living joint bank account"
      - "Deborah Curtis loan An Ideal for Living"
    use_for:
      - matérialiser le premier EP
      - corriger la mythologie DIY
      - documenter la participation domestique
    avoid_for:
      - récit héroïque du DIY sans dette

  - id: RAG-S45-A042
    source_id: S45
    atom_id: S45-A042
    title: An Ideal for Living et imagerie nazie
    chapters:
      - Chapitre 2
      - Chapitre 5
      - Chapitre 11
    tags:
      - an-ideal-for-living
      - imagerie-nazie
      - hitler-youth
      - umlauts
      - controversy
    query_boost:
      - "Hitler Youth Movement banging a drum"
      - "fuelled more speculation about the name of the band"
      - "An Ideal for Living political affiliations"
    use_for:
      - contextualiser la controverse d’An Ideal for Living
      - distinguer provocation et affiliation
      - traiter MYTH-007
    avoid_for:
      - excuse romantique
      - accusation non contextualisée

  - id: RAG-S45-A048
    source_id: S45
    atom_id: S45-A048
    title: Manchester Musicians’ Collective comme laboratoire de risque
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - manchester-musicians-collective
      - experimentation
      - risk
      - scene-locale
      - ian-curtis
    query_boost:
      - "The Collective was a really good thing for Joy Division"
      - "We were allowed to take risks"
      - "music that needs to draw an audience"
    use_for:
      - montrer l’infrastructure d’apprentissage
      - relier scène locale et expérimentation
      - anti-Londres / auto-habilitation
    avoid_for:
      - romantisation du collectif

  - id: RAG-S45-A050
    source_id: S45
    atom_id: S45-A050
    title: RCA / Arrow comme désir de studio et naïveté industrielle
    chapters:
      - Chapitre 2
      - Chapitre 3
      - Chapitre 8
    tags:
      - RCA
      - Arrow-Studios
      - Richard-Searling
      - John-Anderson
      - Bernie-Binnick
      - anti-récit-RCA
    query_boost:
      - "someone else was going to pay for the recording"
      - "Greendow Arrow Studios Manchester"
      - "Joy Division RCA project Deborah Curtis"
    use_for:
      - structurer RCA comme anti-récit
      - montrer l’inexpérience industrielle
      - préparer Hannett / Factory
    avoid_for:
      - industrie caricaturée comme seul coupable
```
