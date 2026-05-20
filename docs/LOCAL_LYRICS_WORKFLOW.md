# Workflow local — paroles complètes et appareil éditorial

```yaml
type_unite: workflow_documentation
scope: "Songbook critique ; paroles complètes conservées hors versionnement ; extraction éditoriale contrôlée vers le repo"
status: "ready"
local_workspace: "local_data/songbook_lyrics/"
versioned_outputs:
  - "songs/<slug>/lyrics_editorial.md"
  - "data/songbook_lyrics_editorial_index.json"
  - "rag/fragments/songbook_lyrics_editorial.jsonl"
```

## 1. Principe

Les paroles complètes sont conservées dans un espace local non versionné :

```text
local_data/songbook_lyrics/<slug>/full_lyrics.txt
```

Le repo ne versionne que l’appareil éditorial : source de référence, page, variantes décrites, courts extraits utiles, notes de sens, motifs, prudences et liens vers chapitres.

## 2. Initialiser l’espace local

```bash
python3 tools/init_local_lyrics_workspace.py
```

Le script crée, pour chaque chanson canonique :

```text
local_data/songbook_lyrics/<slug>/full_lyrics.txt
local_data/songbook_lyrics/<slug>/editorial_notes.json
```

`full_lyrics.txt` reste local. `editorial_notes.json` est également local ; il sert à préparer les sorties éditoriales contrôlées.

## 3. Renseigner manuellement

Dans `full_lyrics.txt`, tu peux conserver les paroles complètes pour ton travail personnel.

Dans `editorial_notes.json`, tu renseignes uniquement les éléments exploitables par le repo :

- source canonique ;
- page ou localisation ;
- courts extraits ;
- variantes décrites ;
- notes de signification ;
- motifs ;
- chapitres liés ;
- statut de vérification.

## 4. Extraire l’appareil éditorial vers le repo

```bash
python3 tools/extract_local_lyrics_editorial.py
```

Le script produit :

```text
songs/<slug>/lyrics_editorial.md
data/songbook_lyrics_editorial_index.json
rag/fragments/songbook_lyrics_editorial.jsonl
```

## 5. Règles de prudence

- Ne pas versionner `full_lyrics.txt`.
- Ne pas copier les paroles complètes dans `songs/<slug>/lyrics_editorial.md`.
- Limiter les extraits à des fragments courts et utiles à l’analyse.
- Documenter toute variante par une source, une version ou un événement.
- Utiliser les notes éditoriales pour le RAG et le registre des chansons.

## 6. Contrôles

```bash
grep -R "full_lyrics" -n songs data rag exports | head -20
find local_data/songbook_lyrics -name full_lyrics.txt | head
python3 tools/extract_local_lyrics_editorial.py --dry-run
```

Le premier contrôle ne doit pas afficher de paroles complètes dans les dossiers versionnés.
