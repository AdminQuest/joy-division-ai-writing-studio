# S41 — Relations stabilisées et entrées RAG — Timeline Two, de Warsaw à Joy Division

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A056-CONCEPT-065
    source: S41-A056
    type: prolonge
    cible: CONCEPT-065
    justification: >
      La Timeline Two fonctionne comme armature documentaire de la séquence Warsaw / Joy Division 1976-1977.

  - id: REL-S41-A057-CONCEPT-066
    source: S41-A057
    type: prolonge
    cible: CONCEPT-066
    justification: >
      Le Swan pub devient après coup un lieu-piège mémoriel, associé à Ian et Joy Division.

  - id: REL-S41-A058-CONCEPT-067
    source: S41-A058
    type: prolonge
    cible: CONCEPT-067
    justification: >
      La première review hostile stabilise un événement dont Hook dit ne presque rien se rappeler.

  - id: REL-S41-A059-CONCEPT-050
    source: S41-A059
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Les entrées répétées du Squat confirment le lieu comme infrastructure pauvre de la deuxième vague punk mancunienne.

  - id: REL-S41-A060-CONCEPT-054
    source: S41-A060
    type: prolonge
    cible: CONCEPT-054
    justification: >
      Le talent contest de Walkden montre l’inadéquation productive du groupe aux circuits old-school.

  - id: REL-S41-A061-CONCEPT-067
    source: S41-A061
    type: prolonge
    cible: CONCEPT-067
    justification: >
      La cassette de Middlesbrough devient archive live et origine d’une mémoire collectée.

  - id: REL-S41-A062-CONCEPT-068
    source: S41-A062
    type: prolonge
    cible: CONCEPT-068
    justification: >
      *Short Circuit* reclasse une performance Warsaw sous le nom Joy Division.

  - id: REL-S41-A063-CONCEPT-055
    source: S41-A063
    type: prolonge
    cible: CONCEPT-055
    justification: >
      *It Won’t Sell* documente Gretton comme acteur discographique local avant son rôle de manager.

  - id: REL-S41-A064-CONCEPT-068
    source: S41-A064
    type: prolonge
    cible: CONCEPT-068
    justification: >
      Les sessions *An Ideal for Living* et le dernier concert au Swinging Apple matérialisent le seuil entre Warsaw et Joy Division.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A056
    source_id: S41
    atom_id: S41-A056
    title: "Timeline Two : ossature documentaire 1976-1977"
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - timeline-two
      - warsaw
      - joy-division
      - chronology
      - 1976-1977
    query_boost:
      - "TIMELINE TWO JUNE 1976 DECEMBER 1977"
      - "Peter Hook Timeline Two Warsaw Joy Division"
    use_for:
      - vérification chronologique
      - bornage Warsaw / Joy Division
    avoid_for:
      - causalité narrative autonome

  - id: RAG-S41-A057
    source_id: S41
    atom_id: S41-A057
    title: "Swan pub : lieu de répétition et mémoire d’Ian"
    chapters:
      - Chapitre 13
      - Chapitre 14
    tags:
      - swan-pub
      - eccles-new-road
      - rehearsal-room
      - ian-curtis
      - memory
    query_boost:
      - "Swan pub Eccles New Road poleaxed"
      - "walk into a room associated with Ian"
    use_for:
      - géographie émotionnelle
      - mémoire posthume des lieux
    avoid_for:
      - déterminisme spatial

  - id: RAG-S41-A058
    source_id: S41
    atom_id: S41-A058
    title: "Première review hostile du premier concert Warsaw"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - first-warsaw-gig
      - electric-circus
      - review
      - stiff-kittens
      - tony-wilson
    query_boost:
      - "Mary Whitehouse odometer Stiff Kittens Warsaw"
      - "I can never remember anything if I’m nervous"
    use_for:
      - réception initiale
      - archive contre mémoire
    avoid_for:
      - preuve unique de valeur musicale

  - id: RAG-S41-A060
    source_id: S41
    atom_id: S41-A060
    title: "Stocks Walkden : talent contest impossible"
    chapters:
      - Chapitre 6
    tags:
      - stocks-walkden
      - talent-contest
      - deep-purple
      - db-meter
      - ranch
    query_boost:
      - "If you like Deep Purple you’ll love these lads"
      - "Warsaw talent contest Stocks Walkden DB meter"
    use_for:
      - anti-circuit variété
      - apprentissage par inadéquation
    avoid_for:
      - tournant absolu

  - id: RAG-S41-A061
    source_id: S41
    atom_id: S41-A061
    title: "Middlesbrough : cassette live et obsession de collection"
    chapters:
      - Chapitre 6
      - Chapitre bootlegs
      - Chapitre 14
    tags:
      - middlesbrough
      - bob-last
      - live-tape
      - bootleg
      - warsaw
    query_boost:
      - "start of what was to become a collecting obsession"
      - "Warsaw Live in Middlesboro tape stolen bootlegged"
    use_for:
      - archive live
      - bootlegs
      - auto-écoute du groupe
    avoid_for:
      - confusion cassette personnelle / bootleg public

  - id: RAG-S41-A062
    source_id: S41
    atom_id: S41-A062
    title: "Short Circuit : Featuring Joy Division"
    chapters:
      - Chapitre 8
      - Chapitre 14
    tags:
      - short-circuit
      - at-a-later-date
      - electric-circus
      - featuring-joy-division
      - warsaw
    query_boost:
      - "Short Circuit Featuring Joy Division"
      - "At a Later Date Warsaw re-labelled Joy Division"
    use_for:
      - requalification nominale
      - archive discographique
    avoid_for:
      - confusion date publication / date concert

  - id: RAG-S41-A064
    source_id: S41
    atom_id: S41-A064
    title: "Dernier Warsaw : An Ideal sessions et Swinging Apple"
    chapters:
      - Chapitre 5
      - Chapitre 6
      - Chapitre 8
    tags:
      - an-ideal-for-living
      - pennine-sound
      - swinging-apple
      - last-warsaw
      - joy-division-name
    query_boost:
      - "last the band perform using the name Warsaw"
      - "An Ideal for Living sessions 14 December 1977 Swinging Apple"
    use_for:
      - seuil Warsaw / Joy Division
      - session An Ideal for Living
    avoid_for:
      - rupture esthétique instantanée
```
