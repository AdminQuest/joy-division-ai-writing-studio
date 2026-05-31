# Interface web locale — Joy Division AI Writing Studio

## Objectif

L’interface web locale donne accès à deux ateliers distincts :

- le **Prompt Studio**, qui construit des prompts contraints pour le travail rédactionnel ;
- le **RAG Studio**, qui interroge le corpus documentaire structuré.

Le système reste local par défaut :

- aucun appel API ;
- aucun service cloud ;
- aucune génération automatique de texte ;
- aucune interrogation directe des PDF OCR bruts.

---

# Architecture actuelle

```text
Browser
→ index.html                       # portail général
  ├── apps/prompt-studio/           # atelier de prompts
  └── apps/rag-studio/              # interface RAG documentaire

RAG Studio
→ /api/status
→ /api/search
→ tools/rag_server.py
→ tools/rag_search.py
→ exports/generated/all_records.json
```

---

# Fichiers concernés

```text
index.html

apps/
  prompt-studio/
    index.html
    style.css
    app.js
    prompt-builder.js

  rag-studio/
    index.html
    style.css
    app.js

tools/
  build_registers.py
  rag_search.py
  rag_server.py
```

---

# Démarrage

## Étape 1 — Installer les dépendances

Depuis la racine du repo :

```bash
pip install -r requirements.txt
```

---

## Étape 2 — Générer les exports documentaires

```bash
python tools/build_registers.py
```

Cette commande produit les fichiers régénérables dans :

```text
exports/generated/
```

---

## Étape 3 — Lancer le serveur local

```bash
python tools/rag_server.py
```

Par défaut :

```text
http://127.0.0.1:8765
```

---

# Routes disponibles

```text
/                       portail général
/prompt                 Prompt Studio
/rag                    RAG Studio
/apps/prompt-studio/    accès direct au Prompt Studio
/apps/rag-studio/       accès direct au RAG Studio
/api/status             état du corpus documentaire
/api/search             endpoint de recherche RAG
```

---

# Prompt Studio

## Fonction

Le Prompt Studio sert à construire des prompts selon :

- le niveau IA ;
- le chapitre ;
- l’atelier ;
- le mode de sortie ;
- le matériau collé par l’utilisateur.

Il s’appuie sur :

```text
data/chapitres.json
data/ateliers.json
data/niveaux.json
data/registre.json
```

## Usage

Ouvrir :

```text
http://127.0.0.1:8765/prompt
```

ou :

```text
http://127.0.0.1:8765/apps/prompt-studio/
```

---

# RAG Studio

## Fonction

Le RAG Studio permet d’interroger :

- les atomes ;
- les citations ;
- la chronologie ;
- les chansons ;
- les personnes ;
- les registres transversaux.

Il ne rédige pas encore de synthèse. Il retrouve les documents pertinents pour préparer ensuite le travail avec l’IA.

## Usage

Ouvrir :

```text
http://127.0.0.1:8765/rag
```

ou :

```text
http://127.0.0.1:8765/apps/rag-studio/
```

---

# Exemples de recherches RAG

```text
Ian Curtis epilepsy domestic life
```

```text
Hannett live sound studio frustration
```

```text
Transmission first real Joy Division song
```

```text
Rob Gretton Factory management
```

---

# Résultats affichés

Le RAG Studio affiche :

- le score de pertinence ;
- l’identifiant documentaire ;
- le type de document ;
- le fichier source ;
- les champs documentaires principaux.

---

# Philosophie documentaire

L’interface web n’est qu’une couche d’accès.

Le système documentaire reste fondé sur :

```text
PDF OCR
→ atomisation Markdown/YAML
→ schémas
→ parseur documentaire
→ exports JSON/CSV
→ retrieval
→ usage rédactionnel contrôlé
```

Ne jamais brancher directement l’IA générative sur des PDF OCR bruts.

---

# Évolutions prévues

Prochaines étapes possibles :

- synthèse documentaire automatique ;
- navigation relationnelle entre atomes, personnes, chansons et événements ;
- graphe documentaire ;
- recherche hybride lexicale/vectorielle ;
- mode rédaction assistée ;
- citations automatiques ;
- export Word.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création de l’interface web locale v0.1 | ChatGPT |
| 2026-05-10 | Mise à jour vers portail unique et studios modulaires | ChatGPT |

---

## Convention de cache — loader partagé `apps/lib/dynamic-registers.js`

Toutes les pages registres (`apps/*-register/index.html`) chargent le **même**
loader `apps/lib/dynamic-registers.js`. GitHub Pages et les navigateurs mettent
ce fichier en cache de façon agressive (asset statique de longue durée).

**Règle** : les pages l'incluent avec un **jeton de version** —
`<script src="../lib/dynamic-registers.js?v=<jeton>"></script>` — et **à chaque
modification du loader, on BUMPE le jeton dans TOUTES les pages** qui l'incluent :

```
grep -rl 'lib/dynamic-registers.js' apps/*/index.html   # liste des pages à mettre à jour
```

Sans ce bump, le cache rejoue l'ancien loader et les pages se cassent
silencieusement (incident concerts 7c : l'ancien loader, en cache, ignorait les
listes YAML de 1er niveau et ne classait pas `CONCERT-` → page vide alors que
données + code étaient corrects sur `main`).

**Jeton courant : `v=7c`** (8 pages : song, organizations, concerts, concept,
places, people, quote, chronology). Étape 8 (citations) touchant le loader :
passer à `v=8`, etc.
