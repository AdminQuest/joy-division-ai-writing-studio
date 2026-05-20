# Compléments de registres — S79 — « Warsaw »

```yaml
source_id: S79
source_label: "S79 — Curtis, So This Is Permanence, 2014"
type_unite: registers_update
coverage: "The handwritten texts — Warsaw ; p. PDF 32-35 ; p. livre 2-5"
song_id: JD-SONG-043
canonical_song: "Warsaw"
```

## Registres structurants

```yaml
concepts:
  - id: concept_s79_warsaw_source_autographe
    label: "Warsaw comme premier texte autographe du corpus S79"
    atoms: [S79-A011, S79-A012]
    chapitres: ["Chapitre 2", "Chapitre 6", "Chapitre 14"]
  - id: concept_s79_warsaw_code_numerique
    label: "motif numérique et identité Warsaw"
    atoms: [S79-A013]
    chapitres: ["Chapitre 2", "Chapitre 5", "Chapitre 6"]
  - id: concept_s79_warsaw_contact_rompu
    label: "faute, contradiction et contact rompu"
    atoms: [S79-A014]
    chapitres: ["Chapitre 6", "Chapitre 11"]

motifs:
  - id: motif_s79_warsaw_31g
    label: "code 31G"
    atoms: [S79-A013]
  - id: motif_s79_warsaw_mur_contact
    label: "mur, contact et contradiction"
    atoms: [S79-A014]

mythes:
  - id: mythe_s79_warsaw_simple_brouillon
    label: "Warsaw serait seulement une ébauche négligeable"
    correction: "Le fac-similé et la transcription montrent un objet précoce mais déjà structuré."
    atoms: [S79-A011, S79-A015]
```

## Registres spécialisés

```yaml
citations_courtes:
  - id: S79-CIT-001
    source_id: S79
    song_id: JD-SONG-043
    atom_id: S79-A013
    citation: "31G"
    pages_pdf: "35"
    usage: "Motif numérique et signalétique."

chansons:
  - song_id: JD-SONG-043
    canonical_song: "Warsaw"
    source_id: S79
    pages_pdf: "32-35"
    statut: "fac-similé et transcription éditée"
    dossier_songbook: "songs/warsaw/"
```
