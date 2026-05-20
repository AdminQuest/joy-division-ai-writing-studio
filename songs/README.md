# Songbook critique — Joy Division / Warsaw

```yaml
type_unite: songbook_root
status: skeleton_generator_ready
canon_file: "registers/songs/00_canonical_joy_division_songs.md"
generator: "tools/generate_song_dossiers.py"
```

## Fonction

Ce dossier reçoit les dossiers chanson du Songbook critique. Chaque titre canonique Joy Division / Warsaw disposera d’un sous-dossier :

```text
songs/<slug>/
```

Chaque sous-dossier doit contenir :

```text
song.md
lyrics.md
sessions.md
live_occurrences.md
releases.md
bootlegs.md
source_notes.md
```

## Génération

Les dossiers sont générés automatiquement depuis le canon :

```bash
python3 tools/generate_song_dossiers.py
```

Le script est non destructif par défaut : il crée les fichiers absents et conserve les fichiers déjà renseignés.

Pour rafraîchir volontairement les squelettes :

```bash
python3 tools/generate_song_dossiers.py --force
```

## Règle documentaire

Le Songbook distingue :

- la chanson canonique ;
- les versions enregistrées ou jouées ;
- les occurrences en sortie officielle, concert, radio, bootleg ou archive ;
- les sources justifiant chaque information.

Les paroles complètes et variantes doivent rester dans `lyrics.md`, avec statut de vérification.
