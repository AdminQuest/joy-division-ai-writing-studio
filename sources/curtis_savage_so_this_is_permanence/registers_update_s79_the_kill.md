# Compléments de registres — S79 — « The Kill (Warsaw) »

```yaml
source_id: S79
source_label: "S79 — Curtis, So This Is Permanence, 2014"
type_unite: registers_update
coverage: "The handwritten lyrics — The Kill (Warsaw) ; p. PDF 50-51 ; p. livre 20-21"
song_id: JD-SONG-051
canonical_song: "The Kill (Warsaw)"
distinct_from: "JD-SONG-030 — The Kill (Still)"
```

## Registres structurants

```yaml
concepts:
  - id: concept_s79_the_kill_warsaw_acte_contraint
    label: "acte nécessaire et impulsion contrainte dans The Kill (Warsaw)"
    atoms: [S79-A049, S79-A053, S79-A056]
    chapitres: ["Chapitre 2", "Chapitre 4", "Chapitre 11"]
  - id: concept_s79_the_kill_warsaw_regard_fixation
    label: "regard persistant et fixation relationnelle"
    atoms: [S79-A051, S79-A055]
    chapitres: ["Chapitre 4", "Chapitre 11", "Chapitre 12"]
  - id: concept_s79_the_kill_warsaw_mise_en_ordre
    label: "nettoyage symbolique et mise en ordre ambiguë"
    atoms: [S79-A052, S79-A054]
    chapitres: ["Chapitre 2", "Chapitre 4", "Chapitre 14"]

motifs:
  - id: motif_s79_the_kill_warsaw_rature
    label: "page raturée et stratifiée"
    atoms: [S79-A050]
  - id: motif_s79_the_kill_warsaw_tactique_paiement
    label: "tactique, paiement et conséquence"
    atoms: [S79-A053]
  - id: motif_s79_the_kill_warsaw_chanson_distincte
    label: "chanson distincte du premier corpus Warsaw"
    atoms: [S79-A056]

mythes:
  - id: mythe_s79_the_kill_warsaw_variante_still
    label: "The Kill (Warsaw) serait une variante de The Kill (Still)"
    correction: "The Kill (Warsaw) et The Kill (Still) doivent être traitées comme deux chansons distinctes. Les atomes S79-A049 à S79-A056 relèvent de JD-SONG-051."
    atoms: [S79-A049, S79-A056]
  - id: mythe_s79_the_kill_warsaw_celebration_violence
    label: "The Kill (Warsaw) serait une célébration univoque de la violence"
    correction: "Le titre et certains motifs sont violents, mais le texte reste structuré par la contrainte, le regard et l’ambivalence morale."
    atoms: [S79-A052, S79-A054]

references:
  - id: ref_s79_so_this_is_permanence_the_kill_warsaw
    source_id: S79
    label: "Ian Curtis, So This Is Permanence, « The Kill (Warsaw) », p. PDF 50-51 / p. livre 20-21"
    usage: "source canonique pour fac-similé, transcription éditée et appareil Songbook de JD-SONG-051"
```

## Registres spécialisés

```yaml
citations_courtes:
  - id: S79-THE-KILL-WARSAW-Q001
    source_id: S79
    song_id: JD-SONG-051
    canonical_song: "The Kill (Warsaw)"
    excerpt: "clear it all away"
    pages_pdf: "50-51"
    pages_livre: "20-21"
    usage: "motif de nettoyage symbolique et de mise en ordre morale ambiguë"
    atoms: [S79-A052]

chronologie:
  - id: S79-CHRONO-006
    source_id: S79
    date: "1977"
    precision: "année éditoriale"
    evenement: "Transcription éditée de « The Kill (Warsaw) » donnée comme texte de 1977."
    atoms: [S79-A049, S79-A056]

acteurs:
  - id: ACT-IAN-CURTIS-S79-THE-KILL-WARSAW
    nom: "Ian Curtis"
    role: "auteur du manuscrit et du texte édité"
    atoms: [S79-A050, S79-A056]

chansons:
  - song_id: JD-SONG-051
    canonical_song: "The Kill (Warsaw)"
    source_id: S79
    pages_pdf: "50-51"
    pages_livre: "20-21"
    statut: "fac-similé et transcription éditée ; chanson distincte de JD-SONG-030"
    dossier_songbook: "songs/the-kill-warsaw/"

lieux: []
organisations: []
```
