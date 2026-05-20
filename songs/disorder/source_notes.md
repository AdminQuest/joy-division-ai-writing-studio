# Disorder — Sources, atomes et vérifications

```yaml
id: JD-SONG-010-SOURCE-NOTES
song_id: JD-SONG-010
type_unite: song_source_notes
canonical_song: "Disorder"
slug: "disorder"
verification_status: "enrichi automatiquement depuis exports/generated/songs.json ; à vérifier source par source"
last_update: "2026-05-20"
matched_records: 6
```

## 1. Sources internes atomisées

```yaml
internal_sources:

  - source_id: "S34"
    source_label: "S34 — Fraser & Fuoto, Manchester, 1976, 2012"
    matched_song_records: "1"
  - source_id: "S41"
    source_label: "S41"
    matched_song_records: "1"
  - source_id: "S49"
    source_label: "S49 — Farci, Here are the Young Men, the weight on their shoulders, 2021"
    matched_song_records: "1"
  - source_id: "S56"
    source_label: "S56 — Barone, Directionless so plain to see, 2021"
    matched_song_records: "1"
  - source_id: "S75"
    source_label: "S75 — Ott, Joy Division's Unknown Pleasures, 2004"
    matched_song_records: "2"
```

## 2. Mentions internes rattachées

```yaml
matched_song_records:

  - record_id: "SONG-S49-DISORDER"
    source_id: "S49"
    song_title_in_record: "Disorder"
    file: "registers/s49_farci_specialized_registers.md"
    heading: "Chansons"
    chapters:
      - "Chapitre 4"
      - "Chapitre 11"
    usage: "Question de la normalité masculine et des plaisirs d’un homme normal ; paroles à vérifier avant citation."
    themes: []
    keywords: []
  - record_id: "SONG-S56-DISORDER"
    source_id: "S56"
    song_title_in_record: "Disorder"
    file: "registers/s56_barone_specialized_registers.md"
    heading: "Acteurs, lieux, organisations, chansons"
    chapters:
      - "Chapitre 4"
      - "Chapitre 8"
    usage: "Titre d’Unknown Pleasures et matrice de We Were Strangers ; à manier sans citation lyrique non vérifiée."
    themes: []
    keywords: []
  - record_id: "Disorder"
    source_id: "S41"
    song_title_in_record: "Disorder"
    file: "registers/songs/master_songs.md"
    heading: "Disorder"
    chapters:
      - "Chapitre 5"
      - "Chapitre 11"
    usage: "« Disorder » agit comme manifeste d’ouverture de Unknown Pleasures."
    themes:
      - "désorientation"
      - "jeunesse"
      - "énergie nerveuse"
      - "mouvement"
      - "confusion existentielle"
    keywords:
      - "disorder"
      - "speed"
      - "confusion"
      - "youth"
  - record_id: "SONG-S75-016"
    source_id: "S75"
    song_title_in_record: "Disorder"
    file: "registers/songs/s75_ott_songs_part_03.md"
    heading: "SONG-S75-016 — « Disorder »"
    chapters:
      - "Chapitre 3"
      - "Chapitre 4"
      - "Chapitre 6"
    usage:
      - "ouverture album"
      - "architecture sonore"
      - "paroles de Curtis"
    themes: []
    keywords: []
  - record_id: "SONG-S75-003"
    source_id: "S75"
    song_title_in_record: "Disorder"
    file: "registers/songs/s75_ott_songs.md"
    heading: "SONG-S75-003 — « Disorder »"
    chapters:
      - "Chapitre 7"
      - "Chapitre 10"
      - "Chapitre 14"
    usage: "Entrée complémentaire au registre maître, centrée sur la réception par reprise plutôt que sur le morceau original seul."
    themes:
      - "désorientation"
      - "réception posthume"
      - "influence sans imitation"
    keywords:
      - "Bedhead"
      - "Unknown Pleasures"
      - "reprise"
      - "postérité"
  - record_id: "SONG-S34-004"
    source_id: "S34"
    song_title_in_record: "Disorder"
    file: "registers/songs/s34_fraser_fuoto_songs.md"
    heading: "SONG-S34-004 — « Disorder »"
    chapters:
      - "Chapitre 3"
      - "Chapitre 6"
      - "Chapitre 13"
    usage:
      - "espace sonore"
      - "aliénation"
      - "instruments séparés"
    themes:
      - "MOTIF-S34-003"
    keywords: []
```

## 3. Atomes liés

```yaml
related_atoms: 
  - "S34-A008"
  - "S41-096"
  - "S45-018"
  - "S75-A001"
  - "S75-A041"
```

## 4. Citations liées

```yaml
related_quotes: []
```

## 5. Fichiers internes repérés

```yaml
matched_files: 
  - "registers/s49_farci_specialized_registers.md"
  - "registers/s56_barone_specialized_registers.md"
  - "registers/songs/master_songs.md"
  - "registers/songs/s34_fraser_fuoto_songs.md"
  - "registers/songs/s75_ott_songs.md"
  - "registers/songs/s75_ott_songs_part_03.md"
```

## 6. Sources externes à intégrer

```yaml
external_sources: 
  - "joydiv.org"
  - "discogs"
  - "livrets Unknown Pleasures / Heart and Soul"
  - "BBC / Peel references"
```

## 7. Contradictions et arbitrages

```yaml
source_conflicts: []
arbitrages:
  - "Étape 5 : rattachement automatique effectué sur titres canoniques et alias ; chaque donnée reste à vérifier avant usage définitif."
```
