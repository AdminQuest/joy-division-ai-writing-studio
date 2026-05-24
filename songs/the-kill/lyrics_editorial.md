# The Kill — Appareil éditorial des paroles

```yaml
id: JD-SONG-030-LYRICS-EDITORIAL
song_id: JD-SONG-030
type_unite: song_lyrics_editorial
canonical_song: "The Kill"
slug: "the-kill"
canonical_lyrics_source: "S79 — Curtis, So This Is Permanence, 2014"
source_id: S79
source_page: "p. PDF 50-51 / p. livre 20-21"
full_lyrics_local_path: "local_data/songbook_lyrics/the-kill/full_lyrics.txt"
completeness: "complete_local_not_versioned"
verification_status: "verifie_s79"
last_update: "2026-05-24"
```

## 1. Règle d’usage

Les paroles complètes sont conservées localement et ne sont pas reproduites dans le repo. Ce fichier ne contient que des éléments éditoriaux exploitables : courts extraits, motifs, variantes décrites, notes de signification et prudences.

## 2. Courts extraits citables

```yaml
short_excerpts:
  - excerpt: "clear it all away"
    source_id: S79
    pages_pdf: "50-51"
    pages_livre: "20-21"
    usage: "Motif de nettoyage symbolique et de mise en ordre morale ambiguë."
    verification_status: "verifie_s79"
```

## 3. Variantes décrites

```yaml
variants:
  - type: "fac-simile"
    source_id: S79
    pages_pdf: "50"
    pages_livre: "20"
    description: "Fac-similé raturé, avec titre repris, segments corrigés et stabilisation partielle."
    verification_status: "verifie_s79"
  - type: "transcription_editee"
    source_id: S79
    pages_pdf: "51"
    pages_livre: "21"
    description: "Transcription éditée de The Kill, donnée comme texte de 1977."
    verification_status: "verifie_s79"
```

## 4. Motifs et champs lexicaux

```yaml
motifs:
  - "sequence_carnets"
  - "chronologie_relative"
  - "premier_age_warsaw"
  - "acte_contraint"
  - "impulsion"
  - "regard"
  - "fixation_relationnelle"
  - "mise_en_ordre"
  - "rature"
  - "prudence_interpretative"
```

## 5. Notes éditoriales

```yaml
editorial_notes:
  - "S79 constitue la source canonique à utiliser pour le fac-similé et la transcription éditée de The Kill."
  - "La chanson doit être traitée comme pièce d’impulsion contrainte du premier corpus."
  - "Le titre et le vocabulaire de mise en ordre doivent être lus avec prudence : le texte ne se réduit pas à une célébration simple de la violence."
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
  - "Atomes : sources/curtis_savage_so_this_is_permanence/atoms_dm_s79_the_kill_v2.md"
  - "Relations : sources/curtis_savage_so_this_is_permanence/relations_s79_the_kill_v2.md"
  - "Contexte RAG : rag/context/s79_the_kill.yaml"
  - "Fragments RAG : rag/fragments/s79_the_kill.jsonl"
```