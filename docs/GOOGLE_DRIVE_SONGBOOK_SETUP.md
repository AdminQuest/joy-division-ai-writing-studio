# Configuration Google Drive — Songbook privé synchronisé

```yaml
type_unite: workflow_documentation
scope: "Songbook privé multi-supports"
status: "ready"
recommended_storage: "Google Drive / Projet de livre"
sync_tool: "tools/songbook_sync.py"
```

## 1. Objectif

Le Songbook doit pouvoir être utilisé depuis plusieurs supports sans dépendre exclusivement du Mac local.

Les paroles complètes et notes privées restent hors versionnement Git, mais peuvent être synchronisées dans un dossier Google Drive privé.

Le repo GitHub ne reçoit que l’appareil éditorial : courts extraits, variantes décrites, motifs, notes critiques et sorties RAG.

## 2. Structure recommandée dans Google Drive

Créer dans le dossier privé :

```text
Projet de livre/
  songbook_lyrics/
    warsaw/
      full_lyrics.txt
      editorial_notes.json
    transmission/
      full_lyrics.txt
      editorial_notes.json
    disorder/
      full_lyrics.txt
      editorial_notes.json
```

## 3. Déclarer le dossier synchronisé

Sur le Mac :

```bash
export SONGBOOK_LYRICS_ROOT="$HOME/Library/CloudStorage/GoogleDrive-xxx/My Drive/Projet de livre/songbook_lyrics"
```

Le chemin exact dépend du nom de ton compte Google Drive dans macOS.

## 4. Initialiser automatiquement les chansons

```bash
python3 tools/init_local_lyrics_workspace.py
```

Le script utilisera automatiquement `SONGBOOK_LYRICS_ROOT` s’il est défini.

## 5. Workflow simplifié

Commande unique :

```bash
python3 tools/songbook_sync.py --diagnostics
```

La commande :

- extrait les notes éditoriales ;
- reconstruit registres et RAG ;
- exécute les audits ;
- affiche les diagnostics utiles ;
- montre le `git status` final.

## 6. Ce qui reste privé

Les fichiers suivants ne sont jamais versionnés :

```text
full_lyrics.txt
PDF sources privés
notes longues personnelles
```

## 7. Ce qui entre dans GitHub

Le repo reçoit uniquement :

```text
songs/<slug>/lyrics_editorial.md
rag/fragments/songbook_lyrics_editorial.jsonl
data/songbook_lyrics_editorial_index.json
```

## 8. Avantage

Tu peux désormais :

- travailler depuis plusieurs Mac ;
- travailler depuis tout poste connecté à ton Google Drive ;
- garder les paroles complètes dans un espace privé ;
- conserver un Songbook critique et un RAG propres dans GitHub.
