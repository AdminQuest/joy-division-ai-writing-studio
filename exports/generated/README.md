# `exports/generated/` — artefacts de build

Ce dossier contient des **artefacts régénérés** par le pipeline de build
(`tools/build_registers.py` et apparentés). Son contenu est **gitignoré**
(seul ce `README.md` est suivi) : il se reconstruit, il ne se versionne pas.

## `songs.json` — ne pas supprimer à la légère

`songs.json` est généré par `tools/build_registers.py` et **consommé** par :

- `tools/build_master_docs.py` (`load_json("songs.json")`),
- `tools/audit_song_canon.py`,
- `tools/enrich_songbook_from_internal_sources.py`.

⚠️ Ce n'est **pas** un orphelin. L'application web `apps/song-register/` ne le
lit pas (elle charge directement le YAML canonique de
`registers/songs/00_canonical_joy_division_songs.md`), mais le pipeline Python en
dépend. Toute suppression doit s'accompagner d'une mise à jour des consommateurs
ci-dessus.

Le contrat public exécutable des chansons vit dans `schemas/song.schema.json`
et est validé par `tools/validate_songs.py`.
