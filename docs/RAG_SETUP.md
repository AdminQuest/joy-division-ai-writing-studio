# RAG local — Mise en place

## Objectif

Le projet dispose désormais d’un premier moteur RAG local.

Ce moteur :
- ne génère pas de texte ;
- ne dépend d’aucune API externe ;
- n’utilise pas encore d’embeddings vectoriels ;
- fonctionne entièrement à partir des exports documentaires générés localement.

Il sert à :
- retrouver rapidement les atomes pertinents ;
- croiser citations, personnes, chansons et événements ;
- préparer les futurs prompts IA ;
- réduire les hallucinations documentaires.

---

# Architecture

```text
Markdown atomisé
    ↓
YAML documentaires
    ↓
python tools/build_registers.py
    ↓
exports/generated/*.json
    ↓
python tools/rag_search.py
    ↓
retrieval documentaire
```

---

# Étape 1 — Générer les exports

Depuis la racine du repo :

```bash
python tools/build_registers.py
```

Cela produit :

```text
exports/generated/
```

avec :
- atoms.json
- quotes.json
- chronology.json
- songs.json
- people.json
- all_records.json
- index_by_id.json
- diagnostics.json

---

# Étape 2 — Lancer une recherche

## Recherche simple

```bash
python tools/rag_search.py "Ian Curtis epilepsy domestic life"
```

---

## Recherche ciblée

```bash
python tools/rag_search.py "Transmission Mayflower Gretton"
```

---

## Restreindre à un type documentaire

```bash
python tools/rag_search.py "Hannett Unknown Pleasures" --kind atom
```

Types disponibles :
- atom
- quote
- chronology
- song
- person

---

## Sortie JSON

```bash
python tools/rag_search.py "Love Will Tear Us Apart" --json
```

---

# Ce que le moteur fait déjà

## Il sait :

- indexer les YAML ;
- retrouver les concepts proches ;
- rechercher dans :
  - citations ;
  - chansons ;
  - événements ;
  - personnes ;
  - atomes ;
- pondérer les termes rares ;
- détecter les correspondances exactes.

---

# Ce qu’il ne fait pas encore

## Pas encore de :

- recherche vectorielle ;
- embeddings ;
- reranking ;
- chunking sémantique ;
- génération IA ;
- synthèse automatique.

Le système reste volontairement :
- simple ;
- vérifiable ;
- transparent ;
- local.

---

# Évolution prévue

## Étape suivante

Ajouter :

```text
tools/rag_embeddings.py
```

avec :
- sentence-transformers ;
- ChromaDB ou FAISS ;
- recherche hybride lexical + vectoriel.

---

# Philosophie documentaire

Le RAG n’est pas le système documentaire.

Le système documentaire reste :
- les sources ;
- les atomes ;
- les citations ;
- les registres ;
- les schémas.

Le RAG n’est qu’une couche de retrieval.

---

# Règle fondamentale

Ne jamais interroger directement les PDF.

Toujours :

```text
PDF
→ atomisation
→ YAML
→ exports
→ RAG
```

Sinon :
- citations instables ;
- hallucinations ;
- incohérences ;
- perte des relations documentaires.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création du premier moteur RAG local | ChatGPT |
