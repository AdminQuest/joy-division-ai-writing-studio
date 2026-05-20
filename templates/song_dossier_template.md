# {{SONG_TITLE}}

```yaml
id: {{SONG_ID}}
type_unite: song_dossier
canonical_song: "{{SONG_TITLE}}"
slug: "{{SONG_SLUG}}"
category: "{{SONG_CATEGORY}}"
period: "{{SONG_PERIOD}}"
status: "{{SONG_STATUS}}"
albums: {{SONG_ALBUMS_YAML}}
aliases: {{SONG_ALIASES_YAML}}
include_variants: {{SONG_VARIANTS_YAML}}
verification_status: "dossier créé ; à renseigner source par source"
last_update: "{{GENERATED_DATE}}"
```

## 1. Fonction du dossier

Ce dossier rassemble les informations documentaires relatives au titre canonique « {{SONG_TITLE}} » : paroles, variantes, sessions, sorties, concerts, bootlegs, sources et atomes liés.

## 2. Règle d’usage

- Ne pas confondre la chanson canonique avec ses versions enregistrées, jouées ou publiées.
- Ne pas recopier de longues paroles sans vérification et sans nécessité éditoriale.
- Toute variante de paroles doit être rattachée à une source, une session ou un concert.
- Les reprises, mentions contextuelles et titres extérieurs au canon Joy Division / Warsaw doivent rester hors de ce dossier, sauf note explicite.

## 3. Fichiers du dossier

```text
songs/{{SONG_SLUG}}/song.md
songs/{{SONG_SLUG}}/lyrics.md
songs/{{SONG_SLUG}}/sessions.md
songs/{{SONG_SLUG}}/live_occurrences.md
songs/{{SONG_SLUG}}/releases.md
songs/{{SONG_SLUG}}/bootlegs.md
songs/{{SONG_SLUG}}/source_notes.md
```

## 4. Synthèse documentaire

À renseigner progressivement.

## 5. Atomes et sources liés

À renseigner automatiquement ou manuellement depuis les atomes du repo.
