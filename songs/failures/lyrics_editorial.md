# Failures — Appareil éditorial des paroles

```yaml
id: JD-SONG-042-LYRICS-EDITORIAL
song_id: JD-SONG-042
type_unite: song_lyrics_editorial
canonical_song: "Failures"
slug: "failures"
canonical_lyrics_source: "S79 — Curtis, So This Is Permanence, 2014"
source_id: S79
source_page: "p. PDF 45-47 / p. livre 15-17"
full_lyrics_local_path: "local_data/songbook_lyrics/failures/full_lyrics.txt"
completeness: "complete_local_not_versioned"
verification_status: "verifie_s79"
last_update: "2026-05-23"
```

## 1. Règle d’usage

Les paroles complètes sont conservées localement et ne sont pas reproduites dans le repo. Ce fichier ne contient que des éléments éditoriaux exploitables : courts extraits, motifs, variantes décrites, notes de signification et prudences.

## 2. Courts extraits citables

```yaml
short_excerpts:
  - excerpt: "Modern Man"
    source_id: S79
    pages_pdf: "45-47"
    pages_livre: "15-17"
    usage: "Marqueur de critique sociale et de type humain moderne."
    verification_status: "verifie_s79"
  - excerpt: "Caesar’s side"
    source_id: S79
    pages_pdf: "47"
    pages_livre: "17"
    usage: "Indice de grandeur antique et d’héroïsme ambigu."
    verification_status: "verifie_s79"
```

## 3. Variantes décrites

```yaml
variants:
  - type: "fac-simile"
    source_id: S79
    pages_pdf: "45-46"
    pages_livre: "15-16"
    description: "Deux pages manuscrites denses, avec ratures et reprises visibles."
    verification_status: "verifie_s79"
  - type: "transcription_editee"
    source_id: S79
    pages_pdf: "47"
    pages_livre: "17"
    description: "Transcription éditée de Failures, donnée comme texte de 1977."
    verification_status: "verifie_s79"
```

## 4. Motifs et champs lexicaux

```yaml
motifs:
  - "sequence_carnets"
  - "chronologie_relative"
  - "premier_age_warsaw"
  - "modern_man"
  - "echec"
  - "choix_impossible"
  - "filiation"
  - "image_paternelle"
  - "heroisme_ambigu"
  - "declin_moderne"
  - "chanson_de_crise"
```

## 5. Notes éditoriales

```yaml
editorial_notes:
  - "S79 constitue la source canonique à utiliser pour le fac-similé et la transcription éditée de Failures."
  - "La chanson doit être traitée comme pièce du premier corpus Warsaw, utile pour les motifs d’échec, de modern man et de crise de décision."
  - "Le vocabulaire de grandeur et de force doit être lu avec prudence : il est retourné vers la faillite, non vers une célébration univoque."
  - "Ne pas reproduire les paroles complètes dans le repo ; conserver les transcriptions longues dans l’espace local non versionné."
```

## 6. Chapitres liés

```yaml
chapters:
  - "Chapitre 2"
  - "Chapitre 4"
  - "Chapitre 6"
  - "Chapitre 10"
  - "Chapitre 11"
  - "Chapitre 12"
  - "Chapitre 14"
```

## 7. Renvois RAG et atomes

```yaml
rag_notes:
  - "Atomes : sources/curtis_savage_so_this_is_permanence/atoms_dm_s79_failures_v2.md"
  - "Relations : sources/curtis_savage_so_this_is_permanence/relations_s79_failures_v2.md"
  - "Contexte RAG : rag/context/s79_failures.yaml"
  - "Fragments RAG : rag/fragments/s79_failures.jsonl"
```