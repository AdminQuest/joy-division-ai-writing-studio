# Compléments de registres — S79 — « Failures »

```yaml
source_id: S79
source_label: "S79 — Curtis, So This Is Permanence, 2014"
type_unite: registers_update
coverage: "The handwritten lyrics — Failures ; p. PDF 45-47 ; p. livre 15-17"
song_id: JD-SONG-042
canonical_song: "Failures"
```

## Registres structurants

```yaml
concepts:
  - id: concept_s79_failures_modern_man
    label: "échec du modern man dans le premier corpus"
    atoms: [S79-A033, S79-A038, S79-A039]
    chapitres: ["Chapitre 2", "Chapitre 4", "Chapitre 11"]
  - id: concept_s79_failures_choix_impossible
    label: "choix impossible et suspension de la décision"
    atoms: [S79-A036, S79-A039]
    chapitres: ["Chapitre 4", "Chapitre 11", "Chapitre 12"]
  - id: concept_s79_failures_heroisme_defait
    label: "héroïsme ambigu et grandeur retournée vers l’échec"
    atoms: [S79-A037, S79-A038]
    chapitres: ["Chapitre 2", "Chapitre 4", "Chapitre 14"]

motifs:
  - id: motif_s79_failures_filiation
    label: "filiation brisée et image paternelle"
    atoms: [S79-A035]
  - id: motif_s79_failures_rature_atelier
    label: "rature et densité manuscrite"
    atoms: [S79-A034]
  - id: motif_s79_failures_chanson_crise
    label: "chanson de crise du premier corpus"
    atoms: [S79-A040]

mythes:
  - id: mythe_s79_failures_celebration_force
    label: "Failures célébrerait la force ou l’homme total"
    correction: "La chanson emploie un vocabulaire de grandeur et de force, mais le retourne vers l’échec, le doute et l’impossibilité de choisir."
    atoms: [S79-A037, S79-A038]

references:
  - id: ref_s79_so_this_is_permanence_failures
    source_id: S79
    label: "Ian Curtis, So This Is Permanence, « Failures », p. PDF 45-47 / p. livre 15-17"
    usage: "source canonique pour fac-similé, transcription éditée et appareil Songbook"
```

## Registres spécialisés

```yaml
citations_courtes:
  - id: S79-FAILURES-Q001
    source_id: S79
    song_id: JD-SONG-042
    canonical_song: "Failures"
    excerpt: "Modern Man"
    pages_pdf: "45-47"
    pages_livre: "15-17"
    usage: "marqueur du type humain moderne et de la critique sociale"
    atoms: [S79-A033]
  - id: S79-FAILURES-Q002
    source_id: S79
    song_id: JD-SONG-042
    canonical_song: "Failures"
    excerpt: "Caesar’s side"
    pages_pdf: "47"
    pages_livre: "17"
    usage: "indice de grandeur antique et d’héroïsme ambigu"
    atoms: [S79-A037]

chronologie:
  - id: S79-CHRONO-004
    source_id: S79
    date: "1977"
    precision: "année éditoriale"
    evenement: "Transcription éditée de « Failures » donnée comme texte de 1977."
    atoms: [S79-A033, S79-A040]

acteurs:
  - id: ACT-IAN-CURTIS-S79-FAILURES
    nom: "Ian Curtis"
    role: "auteur du manuscrit et du texte édité"
    atoms: [S79-A034, S79-A040]

chansons:
  - song_id: JD-SONG-042
    canonical_song: "Failures"
    source_id: S79
    pages_pdf: "45-47"
    pages_livre: "15-17"
    statut: "fac-similé et transcription éditée"
    dossier_songbook: "songs/failures/"

lieux: []
organisations: []
```
