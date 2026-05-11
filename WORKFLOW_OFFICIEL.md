# WORKFLOW OFFICIEL — JOY DIVISION AI WRITING STUDIO

## Statut

Ce document constitue désormais :

- le workflow officiel ;
- la procédure standard ;
- la règle du jeu obligatoire du repo.

Toute nouvelle contribution doit respecter ce workflow.

---

# 1. Philosophie générale

Le repo n’est plus :

- un stockage documentaire ;
- un simple RAG ;
- un système d’archives.

Le repo devient :

une infrastructure historiographique relationnelle au service du manuscrit.

Le manuscrit devient :

une projection narrative temporaire du système documentaire.

---

# 2. Architecture générale

Le système repose sur :

sources
→ atomes
→ registres
→ diagnostics
→ rédaction

Les documents maîtres ne sont plus des sources.

Ils deviennent des états rédactionnels.

---

# 3. Règle fondamentale

Le projet ne recherche plus :

- l’exhaustivité ;
- l’atomisation intégrale.

Le projet recherche :

- les nœuds critiques ;
- les relations structurantes ;
- les chaînes argumentatives.

Principe directeur :

20 % des atomes structurent 80 % du livre.

---

# 4. Workflow quotidien

## Étape 1 — Lecture stratégique

Identifier uniquement :

- passages structurants ;
- concepts ;
- motifs ;
- mythes ;
- contradictions ;
- scènes importantes.

Ne pas chercher l’extraction exhaustive.

---

## Étape 2 — Extraction d’atomes importants

Créer uniquement :

- atomes critiques ;
- atomes relationnels ;
- atomes à forte valeur argumentative.

---

## Étape 3 — Enrichissement v2

Chaque atome important reçoit :

- role_argumentatif
- niveau_preuve
- stabilite
- importance
- risque_surinterpretation
- motifs
- concepts_derives
- relations
- couche_narrative

Priorité absolue :

les relations.

---

## Étape 4 — Relations

Les relations deviennent le cœur du système.

---

## Étape 5 — Registres

Les registres servent à :

- stabiliser ;
- superviser ;
- cartographier.

Ils ne servent plus à rédiger.

---

# 5. Commandes officielles

## Migration v2

Utilisation :

- anciens contenus ;
- imports legacy.

Commande :

python tools/migrate_atoms_v2.py

---

## Registres

Commande :

python tools/build_registers.py --strict

Fréquence :

quasi quotidienne.

---

## Diagnostics historiographiques

Commande :

python tools/build_historiographical_diagnostics.py

---

## Graphe documentaire

Commande :

python tools/build_graph.py

---

## Contexte IA

Commande :

python tools/build_prompt_context.py

---

## Portail local

Commande :

python tools/rag_server.py

---

# 6. Workflow hebdomadaire obligatoire

Ordre recommandé :

python tools/build_registers.py --strict
python tools/build_historiographical_diagnostics.py
python tools/build_graph.py
python tools/build_prompt_context.py

Objectifs :

- cohérence ;
- stabilité ;
- supervision ;
- contrôle des dérives.

---

# 7. Workflow mobile

Depuis téléphone :

AUTORISÉ :

- lecture ;
- enrichissement ;
- relations ;
- concepts ;
- motifs ;
- qualification historiographique.

À ÉVITER :

- refactoring ;
- migration massive ;
- restructuration ;
- automatisations lourdes.

---

# 8. Priorités absolues

Sources prioritaires :

- Hook ;
- Deborah Curtis ;
- Hannett ;
- Reynolds ;
- Factory ;
- Manchester ;
- Unknown Pleasures ;
- Closer ;
- RCA sessions ;
- bootlegs majeurs.

---

# 9. Interdictions structurelles

Interdit :

- atomisation exhaustive ;
- nouveaux schémas concurrents ;
- duplication documentaire ;
- registres improvisés ;
- renommage d’identifiants ;
- workflows parallèles.

---

# 10. Objectif final

Le système doit devenir :

- stable ;
- relationnel ;
- historiographiquement prudent ;
- maintenable ;
- dense ;
- non redondant.
