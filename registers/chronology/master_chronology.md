# Registre chronologique maître — Joy Division

## Fonction du registre

Ce registre constitue la colonne vertébrale documentaire du projet.

Il ne remplace pas les chapitres narratifs.
Il sert à :
- stabiliser la chronologie ;
- identifier les contradictions entre sources ;
- relier événements, chansons, concerts, crises, productions et décisions ;
- alimenter automatiquement les futurs exports CSV/JSON ;
- préparer le moteur RAG ;
- sécuriser les transitions entre chapitres.

Le registre doit rester :
- factuel ;
- compact ;
- relationnel ;
- traçable.

Il ne doit jamais devenir un récit littéraire.

---

# Structure normalisée d’un événement

```yaml
schema: chronology_template
id:
date:
precision_date:

event:

type:
  - concert
  - enregistrement
  - biographie
  - santé
  - production
  - sortie
  - presse
  - relation
  - management
  - archive

location:

people:

songs:

sources:

related_atoms:

chapters:

certainty:
  - strong
  - medium
  - weak

contradictions:

notes:
```

---

# Chronologie maître

## 1956

### CHR-1956-001 — Naissance de Ian Curtis

```yaml
id: CHR-1956-001
categorie: jalon

date: 1956-07-15
precision_date: exact

event: >
  Naissance de Ian Kevin Curtis à Old Trafford, Manchester.

type:
  - biographie

location:
  - Old Trafford
  - Manchester

people:
  - Ian Curtis

songs: []

sources:
  - S45

related_atoms:
  - S45-001

chapters:
  - Chapitre 1
  - Chapitre 4

certainty: strong

contradictions: []

notes: >
  Deborah Curtis précise que Ian grandit ensuite principalement à Hurdsfield,
  près de Macclesfield.
```

---

## 1976

### CHR-1976-001 — Concert des Sex Pistols au Lesser Free Trade Hall

```yaml
id: CHR-1976-001
categorie: jalon

date: 1976-06-04
precision_date: exact

event: >
  Concert des Sex Pistols au Lesser Free Trade Hall de Manchester.

type:
  - concert
  - punk

location:
  - Lesser Free Trade Hall
  - Manchester

people:
  - Sex Pistols
  - Bernard Sumner
  - Peter Hook
  - Ian Curtis

songs: []

sources:
  - S41
  - S45

related_atoms:
  - S41-014
  - S41-015
  - S45-011

chapters:
  - Chapitre 2

certainty: strong

contradictions:
  - présence exacte de certains futurs acteurs du mouvement discutée selon les sources

notes: >
  Événement fondateur du récit punk mancunien.
```

---

## 1978

### CHR-1978-001 — Sessions RCA / Arrow

```yaml
id: CHR-1978-001
categorie: jalon

date: 1978-05
precision_date: approximate

event: >
  Sessions RCA / Arrow destinées à produire un album potentiel pour le groupe.

type:
  - enregistrement
  - production

location:
  - Arrow Studios
  - Manchester

people:
  - Joy Division

songs:
  - Transmission
  - Shadowplay

sources:
  - S41

related_atoms:
  - S41-047
  - S41-Q008

chapters:
  - Chapitre 2
  - Chapitre 3

certainty: strong

contradictions:
  - qualité réelle des bandes selon les membres du groupe

notes: >
  Les sessions deviennent rétrospectivement un anti-modèle esthétique.
```

---

### CHR-1978-002 — Premier fit clairement identifié après le Hope and Anchor

```yaml
id: CHR-1978-002
categorie: jalon

date: 1978-12
precision_date: approximate

event: >
  Premier fit clairement identifié de Ian Curtis après un concert au Hope and Anchor.

type:
  - santé
  - concert

location:
  - Hope and Anchor
  - Londres

people:
  - Ian Curtis
  - Bernard Sumner
  - Deborah Curtis

songs: []

sources:
  - S45
  - S41

related_atoms:
  - S45-014
  - S45-015
  - S41-080

chapters:
  - Chapitre 4
  - Chapitre 12

certainty: strong

contradictions:
  - chronologie médicale exacte à consolider

notes: >
  Deborah Curtis insiste sur l’incompréhension initiale de la gravité de la situation.
```

---

## 1979

### CHR-1979-001 — Sortie de A Factory Sample

```yaml
id: CHR-1979-001
categorie: jalon

date: 1979-01
precision_date: approximate

event: >
  Publication de A Factory Sample contenant « Digital » et « Glass ».

type:
  - sortie
  - production

location:
  - Manchester

people:
  - Joy Division
  - Martin Hannett

songs:
  - Digital
  - Glass

sources:
  - S41
  - S45

related_atoms:
  - S41-073
  - S41-Q005
  - S45-013
  - S45-Q004

chapters:
  - Chapitre 3
  - Chapitre 5
  - Chapitre 7

certainty: strong

contradictions:
  - rôle exact de Hannett et Brierley à préciser

notes: >
  Première apparition pleinement stabilisée du son Joy Division.
```

---

### CHR-1979-002 — Sortie de Unknown Pleasures

```yaml
id: CHR-1979-002
categorie: jalon

date: 1979-06-14
precision_date: exact

event: >
  Sortie de l’album Unknown Pleasures chez Factory Records.

type:
  - sortie
  - production

location:
  - Manchester

people:
  - Joy Division
  - Martin Hannett
  - Peter Saville

songs:
  - Disorder
  - She's Lost Control
  - Shadowplay

sources:
  - S41
  - S45

related_atoms:
  - S41-096
  - S41-097
  - S41-Q007
  - S45-018

chapters:
  - Chapitre 5
  - Chapitre 7
  - Chapitre 14

certainty: strong

contradictions:
  - réception initiale divergente entre Hook et la critique

notes: >
  Hook juge initialement que l’album ne restitue pas correctement le son live du groupe.
```

---

## 1980

### CHR-1980-001 — Concert du Derby Hall à Bury

```yaml
id: CHR-1980-001
categorie: jalon

date: 1980-04-08
precision_date: exact

event: >
  Concert du Derby Hall à Bury marqué par l’état critique de Ian Curtis.

type:
  - concert
  - santé

location:
  - Derby Hall
  - Bury

people:
  - Ian Curtis
  - Joy Division

songs: []

sources:
  - S41
  - S45

related_atoms:
  - S41-139
  - S45-035

chapters:
  - Chapitre 6
  - Chapitre 9

certainty: strong

contradictions:
  - déroulement exact de la soirée selon les témoins

notes: >
  L’événement apparaît comme un moment où la crise devient publiquement visible.
```

---

### CHR-1980-002 — Dernier concert officiel à Birmingham University

```yaml
id: CHR-1980-002
categorie: jalon

date: 1980-05-02
precision_date: exact

event: >
  Dernier concert officiel de Joy Division à Birmingham University.

type:
  - concert
  - archive

location:
  - Birmingham University

people:
  - Joy Division

songs:
  - Ceremony
  - Decades

sources:
  - S41

related_atoms:
  - S41-142
  - S41-143

chapters:
  - Chapitre 6
  - Chapitre 14

certainty: strong

contradictions:
  - statut exact de certaines versions live

notes: >
  Une partie importante du matériau live sera réutilisée plus tard sur Still.
```

---

### CHR-1980-003 — Suicide de Ian Curtis

```yaml
id: CHR-1980-003
categorie: jalon

date: 1980-05-18
precision_date: exact

event: >
  Suicide de Ian Curtis à Macclesfield.

type:
  - biographie
  - santé
  - trauma

location:
  - Macclesfield

people:
  - Ian Curtis
  - Deborah Curtis

songs: []

sources:
  - S41
  - S45

related_atoms:
  - S41-144
  - S45-038
  - S45-039

chapters:
  - Chapitre 10
  - Chapitre 12
  - Chapitre 14

certainty: strong

contradictions:
  - causalités interprétatives multiples selon les biographies

notes: >
  Le registre ne documente ici que le fait chronologique et ses liens documentaires.
```

---

### CHR-1980-004 — Sortie de Closer

```yaml
id: CHR-1980-004
categorie: jalon

date: 1980-07-18
precision_date: exact

event: >
  Sortie posthume de l’album Closer.

type:
  - sortie
  - production
  - archive

location:
  - Royaume-Uni

people:
  - Joy Division
  - Martin Hannett
  - Peter Saville

songs:
  - Isolation
  - The Eternal
  - Decades

sources:
  - S41
  - S45

related_atoms:
  - S41-149
  - S41-150
  - S45-031

chapters:
  - Chapitre 6
  - Chapitre 7
  - Chapitre 14

certainty: strong

contradictions:
  - réception initiale interne du disque

notes: >
  L’album devient immédiatement un objet posthume et mémoriel.
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

1. Ajouter Morris.
2. Ajouter Reynolds.
3. Consolider les dates concerts.
4. Générer ensuite un export CSV.
5. Construire un parseur YAML automatique.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création du registre chronologique maître Joy Division v1 | ChatGPT |
