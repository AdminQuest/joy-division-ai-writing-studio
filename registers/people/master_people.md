# Registre maître des personnes — Joy Division

## Fonction du registre

Ce registre centralise les personnes, groupes, producteurs, proches, managers, témoins et acteurs institutionnels qui structurent le projet *Joy Division, le son de l’éternel*.

Il sert à :
- stabiliser les identités ;
- croiser les portraits selon les sources ;
- relier personnes, événements, chansons et chapitres ;
- repérer les contradictions mémorielles ;
- préparer les exports CSV/JSON ;
- alimenter le futur moteur RAG ;
- éviter les portraits univoques.

Le registre ne doit pas devenir une galerie biographique exhaustive.
Il doit rester relationnel, documentaire et critique.

---

# Structure normalisée d’une personne

```yaml
schema: person_template
id:
name:
full_name:
role:
  - musicien
  - chanteur
  - manager
  - producteur
  - designer
  - témoin
  - proche
  - journaliste
  - photographe
  - institution

period:

associated_entities:

sources:

portraits_by_source:

related_atoms:

related_quotes:

related_songs:

related_events:

chapters:

certainty:
  - strong
  - medium
  - weak

contradictions:

methodological_warnings:

notes:
```

---

# Personnes

## PERS-001 — Ian Curtis

```yaml
id: PERS-001
name: Ian Curtis
full_name: Ian Kevin Curtis
role:
  - chanteur
  - parolier
  - figure centrale
period: 1956-1980
associated_entities:
  - Warsaw
  - Joy Division
  - Factory Records
sources:
  - S41
  - S45
portraits_by_source:
  S41: >
    Hook décrit Curtis comme chanteur, camarade, force d’agrégation du groupe,
    figure scénique et personnalité progressivement fragmentée.
  S45: >
    Deborah Curtis décrit Ian depuis l’espace domestique : conjoint, père,
    malade, homme silencieux, parfois contrôlant, de plus en plus absent.
related_atoms:
  - S41-021
  - S41-026
  - S41-080
  - S41-144
  - S45-001
  - S45-008
  - S45-014
  - S45-032
  - S45-038
related_quotes:
  - S45-Q003
related_songs:
  - She's Lost Control
  - Love Will Tear Us Apart
  - Decades
related_events:
  - CHR-1956-001
  - CHR-1978-002
  - CHR-1980-003
chapters:
  - Chapitre 4
  - Chapitre 6
  - Chapitre 10
  - Chapitre 11
  - Chapitre 12
  - Chapitre 14
certainty: strong
contradictions:
  - tension entre Curtis figure scénique et Curtis domestique
  - risque de lecture téléologique de sa mort
methodological_warnings:
  - ne pas réduire Ian Curtis à sa maladie
  - ne pas transformer les chansons en autobiographie directe
  - éviter la romantisation du génie torturé
notes: >
  Personne centrale du projet. Le registre doit maintenir la pluralité des points de vue :
  Hook donne le Curtis du groupe ; Deborah donne le Curtis du foyer.
```

---

## PERS-002 — Peter Hook

```yaml
id: PERS-002
name: Peter Hook
full_name: Peter Hook
role:
  - musicien
  - bassiste
  - témoin
  - mémorialiste
period: 1956-
associated_entities:
  - Joy Division
  - New Order
sources:
  - S41
portraits_by_source:
  S41: >
    Hook se présente comme acteur central de la formation du groupe, témoin de la scène,
    artisan de la basse mélodique et gardien d’une mémoire directe mais subjective.
related_atoms:
  - S41-017
  - S41-018
  - S41-036
  - S41-064
related_quotes:
  - S41-Q001
  - S41-Q006
related_songs:
  - Disorder
  - Transmission
  - New Dawn Fades
related_events:
  - CHR-1976-001
chapters:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 9
  - Chapitre 14
certainty: strong
contradictions:
  - centralité narrative de Hook à contrôler par croisement avec Morris et Sumner
methodological_warnings:
  - distinguer mémoire vécue et histoire consolidée
  - repérer les traits humoristiques ou autojustificatifs
notes: >
  Hook est à la fois source et objet. Son témoignage est précieux pour les détails matériels,
  mais doit être recoupé pour les interprétations internes.
```

---

## PERS-003 — Bernard Sumner

```yaml
id: PERS-003
name: Bernard Sumner
full_name: Bernard Sumner
role:
  - musicien
  - guitariste
  - témoin
period: 1956-
associated_entities:
  - Warsaw
  - Joy Division
  - New Order
sources:
  - S41
portraits_by_source:
  S41: >
    Hook décrit Sumner comme ami ancien, guitariste autodidacte, partenaire initial
    dans la décision de former le groupe.
related_atoms:
  - S41-008
  - S41-016
  - S41-019
related_quotes: []
related_songs:
  - Transmission
  - Ceremony
related_events:
  - CHR-1976-001
chapters:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 14
certainty: medium
contradictions:
  - portrait à compléter avec *Chapter and Verse*
methodological_warnings:
  - ne pas dépendre uniquement de Hook pour le portrait de Sumner
notes: >
  Source encore sous-intégrée. L’atomisation du livre de Sumner deviendra nécessaire.
```

---

## PERS-004 — Stephen Morris

```yaml
id: PERS-004
name: Stephen Morris
full_name: Stephen Paul David Morris
role:
  - musicien
  - batteur
  - témoin
period: 1957-
associated_entities:
  - Joy Division
  - New Order
sources:
  - S41
portraits_by_source:
  S41: >
    Hook insiste sur la précision, la puissance et la texture du jeu de Morris.
related_atoms:
  - S41-027
  - S41-094
  - S41-117
related_quotes: []
related_songs:
  - She's Lost Control
  - Disorder
  - Transmission
related_events:
  - CHR-1977-001
chapters:
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 7
certainty: medium
contradictions:
  - portrait à compléter avec *Record Play Pause* et *Fast Forward*
methodological_warnings:
  - ne pas réduire Morris à une « machine » rythmique
notes: >
  Morris est essentiel pour comprendre la mécanique expressive de Joy Division.
```

---

## PERS-005 — Deborah Curtis

```yaml
id: PERS-005
name: Deborah Curtis
full_name: Deborah Curtis
role:
  - témoin
  - proche
  - autrice
  - gardienne d’archive
period: 1956-
associated_entities:
  - Ian Curtis
  - Joy Division memory
  - Control
sources:
  - S45
portraits_by_source:
  S45: >
    Deborah Curtis se présente comme épouse, témoin intime, figure progressivement isolée,
    puis gardienne d’une mémoire personnelle contre le mythe public.
related_atoms:
  - S45-021
  - S45-029
  - S45-034
  - S45-041
  - S45-044
related_quotes:
  - S45-Q005
related_songs:
  - Love Will Tear Us Apart
related_events:
  - CHR-1980-003
chapters:
  - Chapitre 4
  - Chapitre 10
  - Chapitre 12
  - Chapitre 14
certainty: strong
contradictions:
  - tension entre témoignage intime et réception publique de Curtis
methodological_warnings:
  - ne pas faire de Deborah Curtis une clé explicative unique
  - distinguer observation domestique et interprétation rétrospective
notes: >
  Source située, affective, légitime et indispensable, mais non souveraine.
```

---

## PERS-006 — Rob Gretton

```yaml
id: PERS-006
name: Rob Gretton
full_name: Robert Leo Gretton
role:
  - manager
  - stratège
  - médiateur
period: 1953-1999
associated_entities:
  - Joy Division
  - Factory Records
  - New Order
sources:
  - S41
  - S45
portraits_by_source:
  S41: >
    Hook décrit Gretton comme accélérateur systémique, protecteur, organisateur,
    adversaire des avances discographiques et défenseur de l’indépendance.
  S45: >
    Deborah Curtis laisse apparaître Gretton comme partie d’un écosystème qui absorbe
    progressivement Ian hors du foyer.
related_atoms:
  - S41-045
  - S41-049
  - S41-050
  - S41-054
  - S41-083
  - S45-016
related_quotes:
  - S41-Q003
related_songs:
  - Transmission
  - Love Will Tear Us Apart
related_events:
  - CHR-1978-001
  - CHR-1979-002
chapters:
  - Chapitre 5
  - Chapitre 9
  - Chapitre 14
certainty: strong
contradictions:
  - protecteur artistique selon Hook
  - force d’absorption du groupe depuis le point de vue domestique
methodological_warnings:
  - ne pas transformer Gretton en simple manager pittoresque
  - articuler liberté artistique et coût humain
notes: >
  Figure structurante. Gretton rend possible Joy Division comme groupe professionnel,
  mais contribue aussi à l’intensification du dispositif.
```

---

## PERS-007 — Tony Wilson

```yaml
id: PERS-007
name: Tony Wilson
full_name: Anthony Howard Wilson
role:
  - journaliste
  - entrepreneur culturel
  - fondateur Factory
  - médiateur
period: 1950-2007
associated_entities:
  - Granada Television
  - Factory Records
sources:
  - S41
  - S45
portraits_by_source:
  S41: >
    Hook décrit Wilson comme figure charismatique, médiateur symbolique et acteur décisif
    de l’écosystème Factory.
  S45: >
    Deborah le voit surtout à travers l’effet Factory sur la vie de Ian.
related_atoms:
  - S41-044
  - S41-057
  - S41-068
  - S41-069
  - S45-016
related_quotes: []
related_songs:
  - Shadowplay
related_events:
  - CHR-1979-001
  - CHR-1979-002
chapters:
  - Chapitre 5
  - Chapitre 9
  - Chapitre 14
certainty: strong
contradictions:
  - médiateur culturel versus facteur de mythification
methodological_warnings:
  - ne pas reprendre sans distance l’auto-mythologie Factory
notes: >
  Wilson est un passeur entre télévision, scène locale, art, label et mythe mancunien.
```

---

## PERS-008 — Martin Hannett

```yaml
id: PERS-008
name: Martin Hannett
full_name: James Martin Hannett
role:
  - producteur
  - ingénieur sonore
  - expérimentateur
period: 1948-1991
associated_entities:
  - Factory Records
  - Joy Division
sources:
  - S41
  - S45
portraits_by_source:
  S41: >
    Hook décrit Hannett comme reconstructeur sonore, parfois incompris par le groupe,
    capable de transformer le son live en architecture froide.
  S45: >
    Deborah Curtis perçoit l’effet Hannett à travers un son plus net et plus froid.
related_atoms:
  - S41-071
  - S41-093
  - S41-095
  - S41-128
  - S45-013
related_quotes:
  - S45-Q004
  - S41-Q007
related_songs:
  - Digital
  - Glass
  - She's Lost Control
  - Atmosphere
  - Decades
related_events:
  - CHR-1979-001
  - CHR-1979-002
  - CHR-1980-004
chapters:
  - Chapitre 3
  - Chapitre 5
  - Chapitre 6
  - Chapitre 7
  - Chapitre 14
certainty: strong
contradictions:
  - génie sonore versus trahison du son live
  - rôle de Hannett à distinguer de celui des ingénieurs Brierley, Johnson, Caffery
methodological_warnings:
  - ne pas attribuer tout le son Joy Division à Hannett seul
  - conserver la tension groupe/producteur
notes: >
  Hannett est l’un des principaux opérateurs de la transformation post-punk du groupe.
```

---

## PERS-009 — Peter Saville

```yaml
id: PERS-009
name: Peter Saville
full_name: Peter Andrew Saville
role:
  - designer
  - directeur artistique
period: 1955-
associated_entities:
  - Factory Records
sources:
  - S41
portraits_by_source:
  S41: >
    Hook présente Saville à travers la matérialité Factory : affiches, objets, retards,
    packaging et abstraction visuelle.
related_atoms:
  - S41-057
  - S41-066
  - S41-074
  - S41-098
  - S41-149
related_quotes: []
related_songs:
  - Atmosphere
related_events:
  - CHR-1979-002
  - CHR-1980-004
chapters:
  - Chapitre 5
  - Chapitre 14
certainty: medium
contradictions:
  - rôle exact dans certaines pochettes à sécuriser
methodological_warnings:
  - vérifier précisément chaque attribution graphique
notes: >
  Figure majeure de la transformation de Joy Division en objet visuel et patrimonial.
```

---

## PERS-010 — Annick Honoré

```yaml
id: PERS-010
name: Annick Honoré
full_name: Annick Honoré
role:
  - proche
  - témoin
period: 1957-2014
associated_entities:
  - Ian Curtis
  - Joy Division
  - Bruxelles
sources:
  - S45
portraits_by_source:
  S45: >
    Deborah Curtis présente Annick Honoré comme un point de rupture supplémentaire
    dans la relation conjugale.
related_atoms:
  - S45-027
related_quotes: []
related_songs:
  - Love Will Tear Us Apart
related_events: []
chapters:
  - Chapitre 4
  - Chapitre 6
  - Chapitre 10
  - Chapitre 14
certainty: medium
contradictions:
  - statut exact de la relation selon les sources
  - récit Deborah à compléter par d’autres témoignages
methodological_warnings:
  - éviter la réduction d’Annick Honoré à une fonction narrative de rupture
  - ne pas moraliser la relation
notes: >
  Personne sensible à traiter avec sobriété et pluralité documentaire.
```

---

## PERS-011 — Natalie Curtis

```yaml
id: PERS-011
name: Natalie Curtis
full_name: Natalie Curtis
role:
  - proche
  - enfant de Ian Curtis
period: 1979-
associated_entities:
  - Ian Curtis
  - Deborah Curtis
sources:
  - S45
portraits_by_source:
  S45: >
    Natalie apparaît dans le récit comme enfant née dans un contexte d’épuisement,
    de maladie et de désorganisation conjugale.
related_atoms:
  - S45-022
related_quotes: []
related_songs: []
related_events: []
chapters:
  - Chapitre 4
  - Chapitre 10
certainty: strong
contradictions: []
methodological_warnings:
  - traiter avec grande réserve
  - éviter tout détail inutile
notes: >
  Présence importante pour comprendre la dimension domestique du récit Deborah Curtis.
```

---

## PERS-012 — John Brierley

```yaml
id: PERS-012
name: John Brierley
full_name: John Brierley
role:
  - ingénieur du son
  - producteur
period: actif années 1970
associated_entities:
  - Cargo Studios
sources:
  - S41
portraits_by_source:
  S41: >
    Hook présente Brierley comme contrepoint rationnel et professionnel à Hannett.
related_atoms:
  - S41-070
  - S41-072
  - S41-073
related_quotes: []
related_songs:
  - Digital
  - Glass
related_events:
  - CHR-1979-001
chapters:
  - Chapitre 3
  - Chapitre 5
  - Chapitre 7
certainty: medium
contradictions:
  - rôle exact dans la captation à préciser
methodological_warnings:
  - ne pas effacer les ingénieurs derrière la figure Hannett
notes: >
  Important pour décentrer le récit du seul génie Hannett.
```

---

# État du registre

## Sources actuellement intégrées

| Source | Statut |
|---|---|
| S41 — Peter Hook | intégré partiellement |
| S45 — Deborah Curtis | intégré partiellement |

---

## Priorités suivantes

1. Ajouter Bernard Sumner à partir de *Chapter and Verse*.
2. Ajouter Stephen Morris à partir de *Record Play Pause*.
3. Ajouter les producteurs et ingénieurs de *Closer*.
4. Ajouter les critiques : Paul Morley, Jon Savage, Simon Reynolds.
5. Ajouter les photographes : Kevin Cummins, Anton Corbijn.
6. Créer les liens automatiques avec le registre chronologique et le registre chansons.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création du registre maître des personnes Joy Division v1 | ChatGPT |
