# Rapport — Workflow local paroles complètes / extraction éditoriale

```yaml
type_unite: workflow_report
scope: "Songbook critique ; paroles complètes hors versionnement ; extraction éditoriale vers registre et RAG"
status: "implemented"
local_workspace: "local_data/songbook_lyrics/"
ignore_rule: "local_data/"
versioned_outputs:
  - "songs/<slug>/lyrics_editorial.md"
  - "data/songbook_lyrics_editorial_index.json"
  - "rag/fragments/songbook_lyrics_editorial.jsonl"
last_update: "2026-05-20"
```

## 1. Objet

Le workflow permet de conserver les paroles complètes dans un dossier local non versionné, tout en extrayant vers le repo les seuls éléments éditoriaux exploitables par le RAG et le registre des chansons : courts extraits, variantes décrites, motifs, notes de signification, chapitres liés et statut de vérification.

## 2. Dossier local non versionné

Le dossier local retenu est :

```text
local_data/songbook_lyrics/
```

Il est ignoré par Git via `.gitignore`.

Chaque chanson canonique reçoit localement :

```text
local_data/songbook_lyrics/<slug>/full_lyrics.txt
local_data/songbook_lyrics/<slug>/editorial_notes.json
```

`full_lyrics.txt` peut contenir les paroles complètes pour usage personnel. Il ne doit jamais être versionné.

## 3. Initialisation

L’outil suivant crée l’espace local :

```text
tools/init_local_lyrics_workspace.py
```

Commande :

```bash
python3 tools/init_local_lyrics_workspace.py
```

## 4. Extraction éditoriale

L’outil suivant extrait les notes éditoriales locales vers le repo :

```text
tools/extract_local_lyrics_editorial.py
```

Commande :

```bash
python3 tools/extract_local_lyrics_editorial.py
```

Sorties versionnées :

```text
songs/<slug>/lyrics_editorial.md
data/songbook_lyrics_editorial_index.json
rag/fragments/songbook_lyrics_editorial.jsonl
```

## 5. Intégration dans l’application

`apps/song-register/app.js` charge désormais les fichiers `songs/<slug>/lyrics_editorial.md` et les rattache à la chanson canonique correspondante.

L’application affiche :

- les courts extraits citables ;
- les variantes décrites ;
- les motifs ;
- les notes éditoriales ;
- la source canonique des lyrics, si renseignée.

`apps/song-register/style.css` ajoute une présentation visuelle dédiée aux cartes d’appareil éditorial.

## 6. Prudences

Le repo ne contient pas les paroles complètes.

Les fichiers `lyrics_editorial.md` ne doivent contenir que des fragments courts et utiles à l’analyse, des descriptions de variantes et des notes critiques.

Les fichiers locaux peuvent être complets, mais ils ne doivent jamais être ajoutés par `git add -f`.

## 7. Contrôles recommandés

```bash
git check-ignore -v local_data/songbook_lyrics/transmission/full_lyrics.txt
python3 tools/extract_local_lyrics_editorial.py --dry-run
grep -R "full_lyrics.txt" -n songs data rag exports | head -20
```

Le dernier contrôle peut afficher un chemin indicatif, mais ne doit jamais afficher les paroles complètes.
