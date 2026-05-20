# Rapport — Songbook Joy Division — Étapes 2 et 3

```yaml
type_unite: generation_report
scope: "Songbook critique chanson par chanson"
status: "steps_2_3_generated_as_templates_and_generator"
step_1_status: "canon already fixed in registers/songs/00_canonical_joy_division_songs.md"
step_2_status: "templates and schemas created"
step_3_status: "generator created ; skeleton materialization by local command"
```

## 1. Étape 2 — Template de dossier chanson

L’étape 2 est générée sous forme de modèles stricts dans `templates/` :

```text
templates/song_dossier_template.md
templates/song_lyrics_template.md
templates/song_sessions_template.md
templates/song_live_occurrences_template.md
templates/song_releases_template.md
templates/song_bootlegs_template.md
templates/song_source_notes_template.md
```

Ces modèles distinguent :

- la chanson canonique ;
- les paroles et variantes ;
- les sessions et versions enregistrées ;
- les occurrences live ;
- les sorties officielles et compilations ;
- les bootlegs ;
- les sources, atomes, citations, contradictions et arbitrages.

## 2. Schémas documentaires

Les schémas ont été créés ou étendus :

```text
schemas/song.schema.yaml
schemas/song_version.schema.yaml
schemas/song_occurrence.schema.yaml
```

Ils fixent la distinction centrale du Songbook :

```text
SONG = chanson canonique
VERSION = version enregistrée ou jouée
OCCURRENCE = apparition dans une sortie, un concert, une diffusion, un bootleg ou une archive
SOURCE = preuve documentaire
```

## 3. Étape 3 — Génération des dossiers chanson

Le générateur est créé :

```text
tools/generate_song_dossiers.py
```

Il lit le canon :

```text
registers/songs/00_canonical_joy_division_songs.md
```

Puis il génère automatiquement :

```text
songs/<slug>/song.md
songs/<slug>/lyrics.md
songs/<slug>/sessions.md
songs/<slug>/live_occurrences.md
songs/<slug>/releases.md
songs/<slug>/bootlegs.md
songs/<slug>/source_notes.md
```

Il écrit également :

```text
data/song_dossiers_index.json
```

## 4. Racine du Songbook

Le dossier racine est amorcé par :

```text
songs/README.md
```

Il explique le rôle du Songbook et la commande de génération.

## 5. Commande de matérialisation

La matérialisation des 50 dossiers s’effectue localement par :

```bash
python3 tools/generate_song_dossiers.py
```

La commande est non destructive : elle ne remplace pas les fichiers existants déjà renseignés.

Pour régénérer volontairement les squelettes :

```bash
python3 tools/generate_song_dossiers.py --force
```

## 6. Prudence

Le dépôt contient maintenant l’architecture complète et le générateur. Les 50 dossiers sont produits par commande afin d’éviter une création manuelle massive et fragile de plusieurs centaines de fichiers par l’interface GitHub. Cette méthode permet aussi de régénérer le Songbook si le canon de 50 titres évolue.
