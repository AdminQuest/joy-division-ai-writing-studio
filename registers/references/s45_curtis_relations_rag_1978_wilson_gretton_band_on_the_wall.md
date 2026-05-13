# S45 — Relations stabilisées et entrées RAG — Wilson, Gretton, Band on the Wall

Ce fichier consolide les relations et l’indexation RAG du passage atomisé dans `sources/curtis_touching_from_a_distance/source_part_1978_wilson_gretton_band_on_the_wall.md`.

---

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A053-MOTIF-013
    source: S45-A053
    type: prolonge
    cible: MOTIF-013
    justification: >
      Le Stiff/Chiswick Challenge montre la scène mancunienne comme marché d’attention
      où les rôles restent instables.

  - id: REL-S45-A054-S45-A039
    source: S45-A054
    type: prolonge
    cible: S45-A039
    justification: >
      L’obsession Granada de Curtis devient accès direct à Tony Wilson par l’invective.

  - id: REL-S45-A055-MYTH-009
    source: S45-A055
    type: nuance
    cible: MYTH-009
    justification: >
      Gretton découvre Joy Division dans une scène de détermination, non comme
      sauveur extérieur tombé du ciel.

  - id: REL-S45-A056-CONCEPT-015
    source: S45-A056
    type: prolonge
    cible: CONCEPT-015
    justification: >
      Le passage Granada de « Shadowplay » fixe une lecture audiovisuelle de Joy
      Division par la ville monochrome.

  - id: REL-S45-A056-MYTH-003
    source: S45-A056
    type: nuance
    cible: MYTH-003
    justification: >
      Manchester devient médiation télévisuelle, non cause naturelle du son.

  - id: REL-S45-A057-CONCEPT-016
    source: S45-A057
    type: prolonge
    cible: CONCEPT-016
    justification: >
      Gretton devient dépositaire d’une confiance intime et médiateur confidentiel.

  - id: REL-S45-A057-MYTH-009
    source: S45-A057
    type: nuance
    cible: MYTH-009
    justification: >
      La protection de Gretton s’accompagne d’une dépossession informationnelle
      du côté de Deborah Curtis.

  - id: REL-S45-A058-CONCEPT-006
    source: S45-A058
    type: prolonge
    cible: CONCEPT-006
    justification: >
      La centralité de la basse de Peter Hook est reliée à un conflit interne et à
      un rééquilibrage instrumental.

  - id: REL-S45-A058-CONCEPT-017
    source: S45-A058
    type: prolonge
    cible: CONCEPT-017
    justification: >
      L’incident du second guitariste constitue un cas de conflit productif interne.

  - id: REL-S45-A059-S45-A048
    source: S45-A059
    type: prolonge
    cible: S45-A048
    justification: >
      Le Manchester Musicians’ Collective devient, au Band on the Wall, une pratique
      de répétition publique chaotique.

  - id: REL-S45-A059-MYTH-007
    source: S45-A059
    type: requiert
    cible: MYTH-007
    justification: >
      La critique de Mick Middles sur la connexion nazie impose de traiter la
      controverse comme contemporaine, non seulement rétrospective.

  - id: REL-S45-A060-CONCEPT-012
    source: S45-A060
    type: prolonge
    cible: CONCEPT-012
    justification: >
      Candy rappelle que Barton Street est aussi foyer et contrepoint affectif,
      pas seulement lieu de crise ou atelier.
```

---

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A054
    source_id: S45
    atom_id: S45-A054
    title: Curtis force l’accès à Tony Wilson par l’invective
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - tony-wilson
      - granada
      - television
      - rafters
      - ian-curtis
      - media-access
    query_boost:
      - "Cause you haven’t put us on television"
      - "Ian Curtis Tony Wilson Rafters television"
      - "Joy Division Granada access Deborah Curtis"
    use_for:
      - expliquer l’accès à Granada
      - relier Curtis, Wilson et visibilité télévisuelle
      - nuancer la stratégie médiatique
    avoid_for:
      - héroïsation de l’insulte
      - stratégie professionnelle entièrement consciente

  - id: RAG-S45-A056
    source_id: S45
    atom_id: S45-A056
    title: « Shadowplay » sur Granada et la ville monochrome
    chapters:
      - Chapitre 1
      - Chapitre 5
      - Chapitre 6
    tags:
      - shadowplay
      - granada
      - world-in-action
      - monochrome
      - manchester
      - television
      - cityscape
    query_boost:
      - "With monochrome footage of a dire cityscape"
      - "Shadowplay Granada World in Action"
      - "Joy Division cityscape television"
    use_for:
      - analyser la médiation audiovisuelle de Manchester
      - relier son et image
      - préparer le monochrome Factory
    avoid_for:
      - Manchester comme cause totale
      - image télévisuelle comme essence du groupe

  - id: RAG-S45-A057
    source_id: S45
    atom_id: S45-A057
    title: Gretton comme gardien et médiateur confidentiel
    chapters:
      - Chapitre 6
      - Chapitre 10
      - Chapitre 12
    tags:
      - rob-gretton
      - management
      - deborah-curtis
      - surrogate-parents
      - guardians
      - confidentiality
    query_boost:
      - "as if they were his guardians, or surrogate parents"
      - "Rob Gretton Ian Curtis Deborah guardians"
      - "Gretton solicitor doctor patient confidentiality"
    use_for:
      - nuancer Gretton manager sauveur
      - analyser management et intimité
      - montrer dépossession informationnelle de Deborah
    avoid_for:
      - psychologisation familiale simpliste
      - manager contre épouse

  - id: RAG-S45-A058
    source_id: S45
    atom_id: S45-A058
    title: La basse de Hook avance par conflit interne
    chapters:
      - Chapitre 3
      - Chapitre 6
    tags:
      - peter-hook
      - bass
      - bernard-sumner
      - sound-architecture
      - internal-conflict
    query_boost:
      - "this incident that brought Peter Hook’s bass-playing more up front"
      - "second rhythm guitarist Peter Hook bass"
      - "Joy Division bass brought more up front Deborah Curtis"
    use_for:
      - expliquer la centralité de la basse
      - relier architecture sonore et conflit interne
      - anti-génie immédiat
    avoid_for:
      - causalité unique de la basse

  - id: RAG-S45-A059
    source_id: S45
    atom_id: S45-A059
    title: Band on the Wall comme laboratoire chaotique
    chapters:
      - Chapitre 2
      - Chapitre 6
    tags:
      - band-on-the-wall
      - musicians-union-collective
      - the-fall
      - mick-middles
      - paul-morley
      - rehearsal
    query_boost:
      - "not so much gigs as rehearsals"
      - "Band on the Wall Joy Division rehearsals"
      - "exploited beyond tolerance animated volatile eloquence direction"
    use_for:
      - analyser apprentissage public
      - montrer réception critique divergente
      - contextualiser controverse nazie contemporaine
    avoid_for:
      - sélectionner seulement les lectures favorables
```
