# Compléments de registres — S79 — « Ice Age »

```yaml
source_id: S79
source_label: "S79 — Curtis, So This Is Permanence, 2014"
type_unite: registers_update
coverage: "The handwritten lyrics — Ice Age ; p. PDF 48-49 ; p. livre 18-19"
song_id: JD-SONG-032
canonical_song: "Ice Age"
```

## Registres structurants

```yaml
concepts:
  - id: concept_s79_ice_age_post_catastrophe
    label: "post-catastrophe et non-futur dans le premier corpus"
    atoms: [S79-A041, S79-A045, S79-A047]
    chapitres: ["Chapitre 1", "Chapitre 2", "Chapitre 4", "Chapitre 11"]
  - id: concept_s79_ice_age_abri_degrade
    label: "abri dégradé et survie minimale"
    atoms: [S79-A043, S79-A044, S79-A048]
    chapitres: ["Chapitre 1", "Chapitre 4", "Chapitre 11"]
  - id: concept_s79_ice_age_refrain_condition
    label: "refrain comme condition d’habitation"
    atoms: [S79-A046]
    chapitres: ["Chapitre 6", "Chapitre 11"]

motifs:
  - id: motif_s79_ice_age_froid
    label: "froid, survie et horizon réduit"
    atoms: [S79-A041, S79-A045, S79-A046]
  - id: motif_s79_ice_age_souterrain
    label: "souterrain, porte et puits désaffectés"
    atoms: [S79-A044]
  - id: motif_s79_ice_age_securite_selective
    label: "sécurité stockée et protection inégale"
    atoms: [S79-A043]
  - id: motif_s79_ice_age_condensation_manuscrite
    label: "écriture brève par blocs d’images"
    atoms: [S79-A042]

mythes:
  - id: mythe_s79_ice_age_nucleaire_univoque
    label: "Ice Age serait uniquement une chanson nucléaire"
    correction: "Le texte peut être lu dans l’horizon de la guerre froide, mais il travaille plus largement le froid, l’abri, la survie minimale et le non-futur."
    atoms: [S79-A041, S79-A047]

references:
  - id: ref_s79_so_this_is_permanence_ice_age
    source_id: S79
    label: "Ian Curtis, So This Is Permanence, « Ice Age », p. PDF 48-49 / p. livre 18-19"
    usage: "source canonique pour fac-similé, transcription éditée et appareil Songbook"
```

## Registres spécialisés

```yaml
citations_courtes:
  - id: S79-ICE-AGE-Q001
    source_id: S79
    song_id: JD-SONG-032
    canonical_song: "Ice Age"
    excerpt: "Ice age"
    pages_pdf: "48-49"
    pages_livre: "18-19"
    usage: "titre-formule et motif post-catastrophique"
    atoms: [S79-A041]
  - id: S79-ICE-AGE-Q002
    source_id: S79
    song_id: JD-SONG-032
    canonical_song: "Ice Age"
    excerpt: "stockpiled safety"
    pages_pdf: "48-49"
    pages_livre: "18-19"
    usage: "marqueur de sécurité sélective et d’abri inégal"
    atoms: [S79-A043]

chronologie:
  - id: S79-CHRONO-005
    source_id: S79
    date: "1977"
    precision: "année éditoriale"
    evenement: "Transcription éditée de « Ice Age » donnée comme texte de 1977."
    atoms: [S79-A041, S79-A048]

acteurs:
  - id: ACT-IAN-CURTIS-S79-ICE-AGE
    nom: "Ian Curtis"
    role: "auteur du manuscrit et du texte édité"
    atoms: [S79-A042, S79-A048]

chansons:
  - song_id: JD-SONG-032
    canonical_song: "Ice Age"
    source_id: S79
    pages_pdf: "48-49"
    pages_livre: "18-19"
    statut: "fac-similé et transcription éditée"
    dossier_songbook: "songs/ice-age/"

lieux: []
organisations: []
```
