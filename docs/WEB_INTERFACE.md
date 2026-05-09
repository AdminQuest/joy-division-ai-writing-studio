# Interface web locale — Joy Division AI Writing Studio

## Objectif

L’interface web locale permet d’interroger le corpus documentaire sans utiliser directement la ligne de commande.

Le système reste entièrement local :
- aucun appel API ;
- aucun service cloud ;
- aucune dépendance externe obligatoire.

---

# Architecture

```text
Browser
→ web/index.html
→ rag_server.py
→ rag_search.py
→ exports/generated/all_records.json
```

---

# Fichiers

```text
web/
  index.html
  style.css
  app.js

tools/
  rag_server.py
```

---

# Démarrage

## Étape 1 — Générer les exports documentaires

Depuis la racine du repo :

```bash
python tools/build_registers.py
```

---

## Étape 2 — Lancer le serveur local

```bash
python tools/rag_server.py
```

Par défaut :

```text
http://127.0.0.1:8765
```

---

# Fonctionnalités actuelles

## Recherche documentaire

Exemples :

```text
Ian Curtis epilepsy domestic life
```

```text
Hannett live sound studio frustration
```

```text
Transmission first real Joy Division song
```

---

## Filtrage par type

- Atomes
- Citations
- Chronologie
- Chansons
- Personnes

---

## Résultats affichés

- score de pertinence ;
- ID documentaire ;
- fichier source ;
- champs documentaires principaux.

---

# Philosophie

Cette interface n’est pas encore un assistant conversationnel.

Elle constitue :
- une couche de retrieval ;
- une console documentaire ;
- un poste de recherche historiographique.

---

# Évolutions prévues

## Étape suivante

Ajouter :
- synthèse automatique ;
- navigation entre relations ;
- graphe documentaire ;
- recherche hybride vectorielle ;
- mode rédaction ;
- prompts contextualisés ;
- citations automatiques ;
- export Word.

---

# Important

Le système doit toujours fonctionner dans cet ordre :

```text
PDF
→ atomisation
→ YAML
→ exports
→ retrieval
→ IA générative
```

Ne jamais brancher directement l’IA générative sur des PDF OCR bruts.

---

# Historique

| Date | Action | Auteur |
|---|---|---|
| 2026-05-09 | Création de l’interface web locale v0.1 | ChatGPT |
