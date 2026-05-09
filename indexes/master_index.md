# Index documentaire global — Joy Division AI Writing Studio

## Fonction de l’index

Cet index constitue la carte d’ensemble du système documentaire.

Il ne remplace pas :
- les sources atomisées ;
- les registres ;
- les exports générés ;
- les schémas ;
- les futurs index RAG.

Il sert à :
- localiser rapidement les éléments du corpus ;
- suivre l’état d’avancement ;
- relier sources, citations, registres et exports ;
- préparer les automatisations ;
- éviter les doublons ;
- documenter les priorités.

---

# 1. Architecture documentaire actuelle

```text
joy-division-ai-writing-studio/

  sources/
    hook/
    deborah_curtis/

  registers/
    chronology/
    songs/
    people/

  schemas/
    atom.schema.yaml
    quote.schema.yaml
    chronology.schema.yaml
    song.schema.yaml
    person.schema.yaml

  tools/
    build_registers.py

  exports/
    generated/
      atoms.json
      quotes.json
      chronology.json
      songs.json
      people.json
      all_records.json
      index_by_id.json
      diagnostics.json
      *.csv

  indexes/
    master_index.md
```

---

# 2. Sources atomisées

## S41 — Peter Hook

```yaml
source_id: S41
source_auteur: Peter Hook
source_titre: Unknown Pleasures: Inside Joy Division
nature: mémoire / source primaire rétrospective
status: atomisation primaire terminee
priority: source majeure
```

### Fichiers

| Fichier | Fonction | Statut |
|---|---|---|
| `sources/hook/source.md` | fiche maîtresse + atomisation initiale | actif |
| `sources/hook/atomisation_02_transmission_1978.md` | période 1978 / Factory / Transmission | actif |
| `sources/hook/atomisation_03_unknown_pleasures_1979.md` | période Unknown Pleasures | actif |
| `sources/hook/atomisation_04_unknown_pleasures_track_by_track.md` | analyse morceaux + transition Closer | actif |
| `sources/hook/atomisation_05_closer_phase_terminale_1980.md` | phase terminale / timeline finale | actif |
| `sources/hook/atomisation_06_consolidation_finale.md` | consolidation finale | actif |
| `sources/hook/citations_exactes.md` | registre citationnel normalisé | actif |

### Couverture documentaire

```yaml
coverage:
  - formation du groupe
  - Salford / Manchester
  - Lesser Free Trade Hall
  - Warsaw
  - Factory
  - Rob Gretton
  - RCA / Arrow
  - Martin Hannett
  - A Factory Sample
  - Unknown Pleasures
  - Closer
  - derniers concerts
  - suicide de Ian Curtis
  - postérité discographique immédiate
```

### Usages principaux

```yaml
chapters:
  - Chapitre 1
  - Chapitre 2
  - Chapitre 3
  - Chapitre 5
  - Chapitre 6
  - Chapitre 7
  - Chapitre 9
  - Chapitre 10
  - Chapitre 14
```

---

## S45 — Deborah Curtis

```yaml
source_id: S45
source_auteur: Deborah Curtis
source_titre: Touching from a Distance: Ian Curtis and Joy Division
nature: mémoire / témoignage intime / source primaire indirecte
status: atomisation primaire terminee
priority: source majeure sensible
```

### Fichiers

| Fichier | Fonction | Statut |
|---|---|---|
| `sources/deborah_curtis/source.md` | fiche maîtresse | actif |
| `sources/deborah_curtis/atomisation_01_enfance_mariage_warsaw.md` | enfance, mariage, pré-Warsaw, premier fit | actif |
| `sources/deborah_curtis/atomisation_02_unknown_pleasures_domesticite_maladie.md` | Unknown Pleasures, domesticité, maladie | actif |
| `sources/deborah_curtis/atomisation_03_closer_derniers_mois_memoire_v2.md` | Closer, derniers mois, mémoire | actif |
| `sources/deborah_curtis/citations_exactes.md` | registre citationnel normalisé | actif |

### Couverture documentaire

```yaml
coverage:
  - Ian Curtis avant Joy Division
  - Macclesfield
  - mariage
  - domesticité
  - grossesse
  - Natalie Curtis
  - épilepsie au quotidien
  - relation avec Annick Honoré
  - séparation conjugale
  - derniers jours
  - mémoire posthume
  - critique du mythe romantique
```

### Usages principaux

```yaml
chapters:
  - Chapitre 4
  - Chapitre 6
  - Chapitre 10
  - Chapitre 11
  - Chapitre 12
  - Chapitre 14
```

---

# 3. Registres transversaux

## Chronologie

```yaml
path: registers/chronology/master_chronology.md
status: v1
function: stabilisation des événements et contradictions temporelles
```

### Contient actuellement

```yaml
included_events:
  - naissance de Ian Curtis
  - Lesser Free Trade Hall
  - sessions RCA / Arrow
  - premier fit reconnu
  - A Factory Sample
  - Unknown Pleasures
  - Derby Hall
  - dernier concert officiel
  - suicide de Ian Curtis
  - sortie de Closer
```

---

## Chansons

```yaml
path: registers/songs/master_songs.md
status: v1
function: cartographie des morceaux, thèmes, production, réception et usages par chapitre
```

### Contient actuellement

```yaml
included_songs:
  - Transmission
  - She's Lost Control
  - Disorder
  - Love Will Tear Us Apart
  - Atmosphere
  - Decades
  - Ceremony
```

---

## Personnes

```yaml
path: registers/people/master_people.md
status: v1
function: portraits croisés, contradictions mémorielles et liens documentaires
```

### Contient actuellement

```yaml
included_people:
  - Ian Curtis
  - Peter Hook
  - Bernard Sumner
  - Stephen Morris
  - Deborah Curtis
  - Rob Gretton
  - Tony Wilson
  - Martin Hannett
  - Peter Saville
  - Annick Honoré
  - Natalie Curtis
  - John Brierley
```

---

# 4. Schémas documentaires

```yaml
schemas:
  - path: schemas/atom.schema.yaml
    function: unités atomiques documentaires
  - path: schemas/quote.schema.yaml
    function: citations exactes et traductions
  - path: schemas/chronology.schema.yaml
    function: événements chronologiques
  - path: schemas/song.schema.yaml
    function: registre chansons
  - path: schemas/person.schema.yaml
    function: registre personnes
```

### Rôle

Les schémas servent à empêcher la dérive documentaire :
- clés variables ;
- statuts incohérents ;
- YAML non parsable ;
- citations sans original ;
- atomes non reliés aux chapitres ;
- registres non synchronisables.

---

# 5. Parseur documentaire

```yaml
path: tools/build_registers.py
status: v0.1
function: extraction automatique des blocs YAML et génération d’exports
```

### Exports prévus

```yaml
exports:
  - exports/generated/atoms.json
  - exports/generated/quotes.json
  - exports/generated/chronology.json
  - exports/generated/songs.json
  - exports/generated/people.json
  - exports/generated/all_records.json
  - exports/generated/index_by_id.json
  - exports/generated/diagnostics.json
  - exports/generated/atoms.csv
  - exports/generated/quotes.csv
  - exports/generated/chronology.csv
  - exports/generated/songs.csv
  - exports/generated/people.csv
```

### Commande

```bash
python tools/build_registers.py
```

Mode strict :

```bash
python tools/build_registers.py --strict
```

---

# 6. Relations documentaires principales

## Hook / Deborah Curtis

```yaml
relation_id: REL-S41-S45-001
sources:
  - S41
  - S45
object: Ian Curtis
relation_type: portrait_concurrent
summary: >
  Hook documente principalement le Curtis du groupe, de la scène et de la dynamique musicale.
  Deborah Curtis documente le Curtis domestique, conjugal, malade et posthumément disputé.
methodological_value: forte
```

---

## Gretton

```yaml
relation_id: REL-GRETTON-001
person: Rob Gretton
sources:
  - S41
  - S45
contrast: >
  Hook fait de Gretton un protecteur stratégique et un accélérateur de carrière.
  Deborah Curtis permet de percevoir Factory/Gretton comme partie d’un dispositif qui absorbe Ian hors du foyer.
chapters:
  - Chapitre 5
  - Chapitre 9
  - Chapitre 14
```

---

## Épilepsie

```yaml
relation_id: REL-EPILEPSIE-001
sources:
  - S41
  - S45
summary: >
  Hook observe l’épilepsie depuis le groupe, les concerts, la tournée et la crise publique.
  Deborah Curtis l’observe depuis le foyer, la surveillance, les médicaments et la peur quotidienne.
chapters:
  - Chapitre 4
  - Chapitre 12
methodological_warning: >
  Ne pas esthétiser la maladie ; ne pas réduire l’œuvre à un symptôme.
```

---

## Unknown Pleasures

```yaml
relation_id: REL-UP-001
sources:
  - S41
  - S45
summary: >
  Hook documente la production, Hannett, la frustration interne et la naissance du son canonique.
  Deborah Curtis documente l’effet domestique et biographique de la montée du groupe.
chapters:
  - Chapitre 5
  - Chapitre 7
  - Chapitre 14
```

---

# 7. État d’avancement global

```yaml
status:
  sources_atomisees:
    - S41
    - S45
  citations_normalisees:
    - S41
    - S45
  registres_crees:
    - chronology
    - songs
    - people
  schemas_crees: true
  parser_created: true
  exports_generated: pending_local_execution
  rag_ready: false
```

---

# 8. Prochaines priorités

## Priorité 1 — Exécuter le parseur localement

```bash
python tools/build_registers.py
```

Objectif : vérifier :
- IDs dupliqués ;
- YAML cassés ;
- champs manquants ;
- citations mal structurées ;
- compatibilité des registres.

---

## Priorité 2 — Corriger les diagnostics

Après exécution, traiter :
- erreurs YAML ;
- doublons ;
- champs obligatoires manquants ;
- statuts incohérents.

---

## Priorité 3 — Atomiser une troisième source

Ordre recommandé :

```yaml
next_sources:
  - S43 Stephen Morris — Record Play Pause
  - S42 Bernard Sumner — Chapter and Verse
  - Simon Reynolds
  - Mick Middles / Lindsay Reade
  - Peter Saville
```

---

## Priorité 4 — Créer les registres suivants

```yaml
next_registers:
  - registers/places/master_places.md
  - registers/concepts/master_concepts.md
  - registers/sources/master_sources.md
  - registers/contradictions/master_contradictions.md
```

---

# 9. Règles permanentes

1. Ne jamais stocker les PDF ou OCR complets dans Git.
2. Conserver les citations originales en langue source.
3. Ne jamais mélanger citation, traduction et interprétation.
4. L’atome documentaire n’est pas un paragraphe final du livre.
5. Les registres sont des vues relationnelles, non des récits.
6. Les sources sensibles doivent être croisées avant usage rédactionnel.
7. Toute nouvelle source doit avoir :
   - `source.md` ;
   - fichiers d’atomisation ;
   - `citations_exactes.md` ;
   - consolidation éventuelle.
8. Toute nouvelle donnée structurée doit respecter `schemas/`.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création de l’index documentaire global v1 | ChatGPT |
