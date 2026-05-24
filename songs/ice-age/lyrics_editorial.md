# Ice Age — Appareil éditorial des paroles

```yaml
id: JD-SONG-032-LYRICS-EDITORIAL
song_id: JD-SONG-032
type_unite: song_lyrics_editorial
canonical_song: "Ice Age"
slug: "ice-age"
canonical_lyrics_source: "S79 — Curtis, So This Is Permanence, 2014"
source_id: S79
source_page: "p. PDF 48-49 / p. livre 18-19"
full_lyrics_local_path: "local_data/songbook_lyrics/ice-age/full_lyrics.txt"
completeness: "complete_local_not_versioned"
verification_status: "verifie_s79"
last_update: "2026-05-24"
```

## 1. Règle d’usage

Les paroles complètes sont conservées localement et ne sont pas reproduites dans le repo. Ce fichier ne contient que des éléments éditoriaux exploitables : courts extraits, motifs, variantes décrites, notes de signification et prudences.

## 2. Courts extraits citables

```yaml
short_excerpts:
  - excerpt: "Ice age"
    source_id: S79
    pages_pdf: "48-49"
    pages_livre: "18-19"
    usage: "Titre-formule et motif post-catastrophique."
    verification_status: "verifie_s79"
  - excerpt: "stockpiled safety"
    source_id: S79
    pages_pdf: "48-49"
    pages_livre: "18-19"
    usage: "Marqueur de sécurité sélective et d’abri inégal."
    verification_status: "verifie_s79"
```

## 3. Variantes décrites

```yaml
variants:
  - type: "fac-simile"
    source_id: S79
    pages_pdf: "48"
    pages_livre: "18"
    description: "Fac-similé bref et concentré, avec blocs d’images autour des atrocités, de la sécurité, de la porte et des puits désaffectés."
    verification_status: "verifie_s79"
  - type: "transcription_editee"
    source_id: S79
    pages_pdf: "49"
    pages_livre: "19"
    description: "Transcription éditée de Ice Age, donnée comme texte de 1977."
    verification_status: "verifie_s79"
```

## 4. Motifs et champs lexicaux

```yaml
motifs:
  - "sequence_carnets"
  - "chronologie_relative"
  - "premier_age_warsaw"
  - "post_catastrophe"
  - "guerre_froide"
  - "non_futur"
  - "abri_degrade"
  - "souterrain"
  - "securite_selective"
  - "survie_minimale"
  - "froid"
```

## 5. Notes éditoriales

```yaml
editorial_notes:
  - "S79 constitue la source canonique à utiliser pour le fac-similé et la transcription éditée de Ice Age."
  - "La chanson doit être traitée comme une pièce de post-catastrophe et d’abri dégradé, sans réduction nucléaire univoque."
  - "La page manuscrite documente une écriture brève, condensée, organisée par blocs d’images."
  - "Ne pas reproduire les paroles complètes dans le repo ; conserver les transcriptions longues dans l’espace local non versionné."
```

## 6. Chapitres liés

```yaml
chapters:
  - "Chapitre 1"
  - "Chapitre 2"
  - "Chapitre 4"
  - "Chapitre 6"
  - "Chapitre 10"
  - "Chapitre 11"
  - "Chapitre 14"
```

## 7. Renvois RAG et atomes

```yaml
rag_notes:
  - "Atomes : sources/curtis_savage_so_this_is_permanence/atoms_dm_s79_ice_age_v2.md"
  - "Relations : sources/curtis_savage_so_this_is_permanence/relations_s79_ice_age_v2.md"
  - "Contexte RAG : rag/context/s79_ice_age.yaml"
  - "Fragments RAG : rag/fragments/s79_ice_age.jsonl"
```