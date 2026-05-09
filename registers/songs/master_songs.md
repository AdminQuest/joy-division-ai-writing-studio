# Registre maître des chansons — Joy Division

## Fonction du registre

Ce registre centralise les informations documentaires, analytiques et relationnelles relatives aux chansons de Joy Division.

Il sert à :
- relier les chansons aux chapitres ;
- stabiliser les thématiques ;
- croiser paroles, production, concerts et réception ;
- relier les chansons aux sources primaires ;
- identifier les contradictions interprétatives ;
- préparer les exports RAG et les futures analyses transversales.

Le registre ne doit pas devenir :
- une encyclopédie discographique ;
- une simple liste de paroles ;
- une analyse littéraire exhaustive.

Il doit rester :
- synthétique ;
- relationnel ;
- documenté ;
- extensible.

---

# Structure normalisée d’une chanson

```yaml
song:

type:
  - studio
  - live
  - demo
  - unreleased

period:

writers:

themes:

keywords:

production:

live_history:

lyrics:

sources:

related_atoms:

related_quotes:

chapters:

certainty:
  - strong
  - medium
  - weak

contradictions:

notes:
```

---

# Chansons

## Transmission

```yaml
song: Transmission

type:
  - studio
  - live

period: 1978-1979

writers:
  - Bernard Sumner
  - Peter Hook
  - Ian Curtis
  - Stephen Morris

themes:
  - communication
  - isolement
  - circulation culturelle
  - radio
  - répétition

keywords:
  - dance
  - radio
  - voice
  - movement
  - control

production:
  producer:
    - Martin Hannett
  label:
    - Factory Records
  sound_characteristics:
    - batterie spatialisée
    - basse motrice
    - guitare minimale
    - tension répétitive

live_history:
  important_performances:
    - Mayflower Club
    - Paradiso
  observations:
    - chanson centrale du basculement live du groupe

lyrics:
  notable_lines:
    - "Dance, dance, dance, dance, dance to the radio"
  recurring_motifs:
    - transmission
    - répétition
    - communication vide

sources:
  - S41
  - S45

related_atoms:
  - S41-055
  - S41-Q004
  - S45-011

related_quotes:
  - S41-Q004

chapters:
  - Chapitre 3
  - Chapitre 5
  - Chapitre 9
  - Chapitre 11

certainty: strong

contradictions:
  - statut exact comme première grande chanson Joy Division selon les membres

notes: >
  « Transmission » constitue probablement le premier morceau où le groupe perçoit
  collectivement la singularité de son identité sonore.
```

---

## She's Lost Control

```yaml
song: She's Lost Control

type:
  - studio
  - live

period: 1978-1979

writers:
  - Joy Division

themes:
  - épilepsie
  - perte de contrôle
  - corps
  - observation clinique
  - dissociation

keywords:
  - control
  - seizure
  - body
  - repetition

production:
  producer:
    - Martin Hannett
  sound_characteristics:
    - percussion mécanique
    - froideur clinique
    - espace sonore vide

live_history:
  important_performances:
    - Eindhoven
    - Rainbow Theatre
  observations:
    - réception souvent ambiguë du public face aux mouvements de Curtis

lyrics:
  notable_lines:
    - "She's lost control again"
  recurring_motifs:
    - répétition
    - perte corporelle
    - détachement

sources:
  - S41
  - S45

related_atoms:
  - S45-019
  - S45-025
  - S41-136

related_quotes: []

chapters:
  - Chapitre 4
  - Chapitre 5
  - Chapitre 7
  - Chapitre 11
  - Chapitre 12

certainty: strong

contradictions:
  - lien exact entre expérience personnelle et personnage de la chanson

notes: >
  La chanson oscille entre observation extérieure et expérience intime de la perte de contrôle.
```

---

## Disorder

```yaml
song: Disorder

type:
  - studio
  - live

period: 1978-1979

writers:
  - Joy Division

themes:
  - désorientation
  - jeunesse
  - énergie nerveuse
  - mouvement
  - confusion existentielle

keywords:
  - disorder
  - speed
  - confusion
  - youth

production:
  producer:
    - Martin Hannett
  sound_characteristics:
    - ouverture explosive
    - batterie réverbérée
    - guitare scintillante

live_history:
  important_performances:
    - Factory concerts
  observations:
    - morceau d’ouverture emblématique

lyrics:
  notable_lines:
    - "I've been waiting for a guide to come and take me by the hand"
  recurring_motifs:
    - perte de direction
    - recherche de sens

sources:
  - S41
  - S45

related_atoms:
  - S41-096
  - S45-018

related_quotes: []

chapters:
  - Chapitre 5
  - Chapitre 11

certainty: strong

contradictions:
  - interprétation politique ou existentielle du texte

notes: >
  « Disorder » agit comme manifeste d’ouverture de Unknown Pleasures.
```

---

## Love Will Tear Us Apart

```yaml
song: Love Will Tear Us Apart

type:
  - studio
  - live

period: 1979-1980

writers:
  - Joy Division

themes:
  - désagrégation conjugale
  - intimité
  - répétition affective
  - impossibilité relationnelle

keywords:
  - love
  - separation
  - routine
  - silence

production:
  producer:
    - Martin Hannett
  sound_characteristics:
    - mélodie lumineuse
    - tension émotionnelle
    - contraste texte/musique

live_history:
  important_performances:
    - Eindhoven
    - Birmingham University
  observations:
    - devient rapidement chanson emblématique du groupe

lyrics:
  notable_lines:
    - "Love will tear us apart again"
  recurring_motifs:
    - séparation
    - répétition
    - usure émotionnelle

sources:
  - S41
  - S45

related_atoms:
  - S45-027
  - S45-037
  - S45-042

related_quotes: []

chapters:
  - Chapitre 4
  - Chapitre 6
  - Chapitre 10
  - Chapitre 11
  - Chapitre 14

certainty: strong

contradictions:
  - réduction autobiographique systématique de la chanson

notes: >
  La chanson ne doit pas être réduite à une simple transcription documentaire du couple Curtis.
```

---

## Atmosphere

```yaml
song: Atmosphere

type:
  - studio

period: 1979-1980

writers:
  - Joy Division

themes:
  - disparition
  - transcendance
  - isolement
  - gravité

keywords:
  - silence
  - atmosphere
  - absence
  - elevation

production:
  producer:
    - Martin Hannett
  sound_characteristics:
    - lenteur cérémonielle
    - synthétiseurs étendus
    - espace spectral

live_history:
  important_performances: []
  observations:
    - chanson progressivement sacralisée après la mort de Curtis

lyrics:
  notable_lines:
    - "Walk in silence"
  recurring_motifs:
    - silence
    - disparition
    - suspension

sources:
  - S41

related_atoms:
  - S41-149

related_quotes: []

chapters:
  - Chapitre 6
  - Chapitre 10
  - Chapitre 14

certainty: strong

contradictions:
  - lecture posthume téléologique de la chanson

notes: >
  « Atmosphere » devient progressivement un lieu de mémoire collectif autour de Joy Division.
```

---

## Decades

```yaml
song: Decades

type:
  - studio
  - live

period: 1980

writers:
  - Joy Division

themes:
  - mémoire
  - génération
  - perte
  - temps historique

keywords:
  - decades
  - youth
  - crisis
  - memory

production:
  producer:
    - Martin Hannett
  sound_characteristics:
    - synthétiseurs enveloppants
    - lenteur dramatique
    - voix distante

live_history:
  important_performances:
    - Birmingham University
  observations:
    - souvent interprétée comme clôture symbolique du groupe

lyrics:
  notable_lines:
    - "Where have they been?"
  recurring_motifs:
    - disparition générationnelle
    - mémoire
    - désillusion

sources:
  - S41
  - S45

related_atoms:
  - S41-143
  - S45-031

related_quotes: []

chapters:
  - Chapitre 6
  - Chapitre 10
  - Chapitre 11
  - Chapitre 14

certainty: medium

contradictions:
  - interprétation politique versus existentielle

notes: >
  « Decades » fonctionne comme méditation terminale sur une génération perdue.
```

---

## Ceremony

```yaml
song: Ceremony

type:
  - live
  - posthumous

period: 1980

writers:
  - Joy Division

themes:
  - transition
  - disparition
  - passage
  - continuité

keywords:
  - ceremony
  - inheritance
  - transition

production:
  producer:
    - New Order period
  sound_characteristics:
    - transition stylistique
    - tension entre Joy Division et New Order

live_history:
  important_performances:
    - Birmingham University
  observations:
    - morceau-charnière entre les deux groupes

lyrics:
  notable_lines:
    - "This is why events unnerve me"
  recurring_motifs:
    - passage
    - désorientation
    - continuité brisée

sources:
  - S41

related_atoms:
  - S41-143
  - S41-Q009

related_quotes:
  - S41-Q009

chapters:
  - Chapitre 6
  - Chapitre 14

certainty: medium

contradictions:
  - statut exact du morceau comme chanson Joy Division ou New Order

notes: >
  « Ceremony » constitue l’un des principaux points de passage entre les deux groupes.
```

---

# État du registre

## Sources actuellement intégrées

| Source | Statut |
|---|---|
| S41 — Peter Hook | partiellement intégré |
| S45 — Deborah Curtis | partiellement intégré |

---

## Priorités suivantes

1. Ajouter les chansons de Closer restantes.
2. Relier chaque chanson aux paroles exactes.
3. Ajouter les versions live majeures.
4. Ajouter Reynolds et Middles.
5. Construire les liens avec le registre chronologique.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création du registre maître des chansons Joy Division v1 | ChatGPT |
