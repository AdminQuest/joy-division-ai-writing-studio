# Joy Division — AI Writing Studio

Environnement documentaire, historiographique et rédactionnel pour la production du livre *Joy Division, le son de l’éternel*.

Le repo n’est pas un simple stockage documentaire, ni un RAG brut, ni un brouillon de manuscrit. Il constitue une infrastructure historiographique relationnelle au service du livre. Le manuscrit final est une projection narrative temporaire du système documentaire.

Le projet cherche la densité, non l’exhaustivité : nœuds critiques, relations structurantes, chaînes argumentatives, scènes significatives, concepts stabilisés, motifs récurrents, mythes à déconstruire, controverses et tensions documentaires.

Principe directeur : 20 % des atomes structurent 80 % du livre.

---

## 1. Architecture générale

Le système repose sur la chaîne suivante :

```text
sources
→ atomes
→ registres
→ exports générés
→ audit / diagnostics
→ documents maîtres
→ RAG Studio
→ prompts autonomes
→ rédaction IA
→ manuscrit
```

Chaque niveau a une fonction différente.

- `sources/` conserve la matière documentaire première.
- Les atomes extraient les unités historiographiques importantes.
- `registers/` stabilise les références, citations, concepts, motifs, mythes, personnes et chronologies.
- `exports/generated/` rend le corpus exploitable par les outils.
- Les diagnostics contrôlent la santé du repo.
- `chapters/XX/document_maitre.md` fournit les dossiers documentaires par chapitre.
- Le RAG Studio permet de chercher, filtrer, regrouper et préparer les corpus de rédaction.
- RAG 4 produit des prompts autonomes exploitables dans une IA externe.
- Le manuscrit est rédigé à partir de ces états documentaires, jamais depuis une accumulation brute de sources.

---

## 2. Statut des documents maîtres

Les documents maîtres ne sont pas des sources primaires. Ils sont des dossiers documentaires de rédaction, produits depuis les atomes.

Ils servent à :

- préparer l’écriture d’un chapitre ;
- donner à l’IA un corpus lisible ;
- synthétiser les atomes par chapitre ;
- repérer les sources, citations, motifs, concepts et risques ;
- contrôler les lacunes documentaires.

Ils ne servent pas à prouver seuls. La preuve reste dans les atomes, les citations, les références et les sources d’origine.

Les documents maîtres sont les fichiers à déposer en priorité dans les sources d’une IA de rédaction :

```text
chapters/01/document_maitre.md
...
chapters/14/document_maitre.md
```

---

## 3. Règle impérative pour toute atomisation

Toute demande du type :

```text
Atomise cette source.
Atomise ce livre.
Ajoute cette source au repo.
```

signifie obligatoirement : créer ou modifier directement les fichiers nécessaires dans le repo GitHub.

Il est interdit de répondre uniquement par une archive locale, un dossier temporaire ou un contenu non intégré. Le travail n’est considéré comme fait que lorsque les fichiers sont créés ou modifiés dans le repo avec des commits effectifs.

La procédure historique détaillée reste disponible dans :

```text
docs/ATOMISATION_SOURCE.md
```

La présente page fixe toutefois le workflow opérationnel courant.

---

## 4. Étape préalable : fixation de la source canonique

Avant toute atomisation, la source canonique doit être fixée.

Vérifier d’abord si la source existe déjà dans :

```text
data/registre.json
```

Si elle existe, reprendre exactement son identifiant. Si elle n’existe pas, créer une nouvelle entrée avec le prochain identifiant libre.

Convention :

```text
SXX — Auteur, Titre court, Année
```

Exemples :

```text
S41 — Hook, Unknown Pleasures, 2012
S45 — Curtis, Touching from a Distance, 1995
S74 — Middles, From Joy Division to New Order, 1996
S75 — Middles, Torn Apart, 2006
S76 — Ott, Joy Division’s Unknown Pleasures, 2004
```

Règles :

1. Une source = un identifiant canonique stable.
2. Ne jamais réutiliser un identifiant déjà attribué.
3. Ne jamais confondre deux livres d’un même auteur.
4. Tout atome doit porter le `source_id` canonique.
5. Toute nouvelle source doit être ajoutée à `data/registre.json` avant atomisation définitive.
6. Les anciens identifiants ou alias servent seulement à la migration.

Exemple d’entrée canonique :

```json
{
  "id": "S75",
  "source_label": "S75 — Middles, Torn Apart, 2006",
  "auteur": "Mick Middles",
  "titre": "Torn Apart: The Life of Ian Curtis",
  "annee": "2006",
  "statut": "atomisation sélective v2",
  "usage": "Ian Curtis ; biographie ; mémoire ; santé ; réception ; mythologies rétrospectives"
}
```

Créer ensuite le dossier source correspondant, par exemple :

```text
sources/middles_torn_apart/
sources/ott_unknown_pleasures/
```

---

## 5. Doctrine documentaire v2 : l’atome comme unité de raisonnement

Depuis la version 2, l’atomisation ne consiste plus à découper exhaustivement les sources en fragments. Chaque atome devient une unité interprétative enrichie.

Le système doit permettre :

- la propagation conceptuelle ;
- le contrôle des dérives interprétatives ;
- la qualification du niveau de preuve ;
- la détection des mythologies rétrospectives ;
- la cartographie argumentative du livre ;
- un RAG sémantique et historiographique.

Un atome mérite d’exister s’il :

- structure un chapitre ;
- relie plusieurs concepts ;
- nourrit le graphe relationnel ;
- éclaire un mythe ;
- stabilise un concept ;
- apporte une contradiction ;
- possède une forte densité narrative ;
- documente une rupture esthétique ;
- reste réutilisable.

Un atome faible encombre le système. Un atome fort crée des relations.

---

## 6. Schéma minimal d’un atome v2

Un atome v2 doit contenir ou tendre vers les champs suivants :

```yaml
id:
type_unite:
titre:
source_id:
pages:
citation:
resume:
role_argumentatif:
niveau_preuve:
  statut:
  corroboration:
  confiance:
stabilite:
  statut:
importance:
  niveau:
risque_surinterpretation:
  niveau:
  raison:
motifs:
concepts_derives:
relations:
couche_narrative:
usage_livre:
```

Champs critiques :

- `role_argumentatif` : pourquoi l’atome compte ;
- `niveau_preuve` : solidité documentaire ;
- `importance` : poids dans l’économie du livre ;
- `risque_surinterpretation` : prudence historiographique ;
- `motifs` : récurrences sensibles ou symboliques ;
- `concepts_derives` : dérivations interprétatives ;
- `relations` : liens avec autres atomes, concepts, mythes, citations ou chapitres.

---

## 7. Types documentaires et niveau de preuve

Les atomes doivent distinguer les natures documentaires. Typologies prioritaires :

```text
fait
lecture
concept
citation_clef
mythe
controverse
scene_fondatrice
temoignage
biographie
session
lieu
objet_visuel
reception
```

Cette distinction évite la confusion entre fait, mémoire, reconstruction, mythe, interprétation et téléologie.

Le champ `niveau_preuve` distingue notamment :

```text
établi
fortement corroboré
corroboré
plausible
fragile
contesté
hypothèse
reconstruction rétrospective
témoignage direct rapporté
interprétation critique
```

Tout atome doit signaler explicitement les risques suivants lorsqu’ils existent :

- téléologie ;
- mythologisation ;
- psychologisation ;
- surinterprétation ;
- reconstruction mémorielle douteuse ;
- lecture prophétique de Ian Curtis ;
- Manchester comme matrice absolue ;
- sursymbolisation des ruines industrielles.

---

## 8. Relations

La priorité absolue du système est relationnelle.

Exemples :

```yaml
relations:
  - type: mythologise
    cible: MYTH-002

  - type: nuance
    cible: CONCEPT-001

  - type: contredit
    cible: AT_CH05_0018

  - type: prolonge
    cible: MOTIF-003

  - type: corrobore
    cible: S41-A022
```

Les relations doivent permettre de repérer :

- ce qui confirme ;
- ce qui contredit ;
- ce qui nuance ;
- ce qui mythologise ;
- ce qui déconstruit ;
- ce qui déplace un concept ;
- ce qui rattache deux chapitres ;
- ce qui signale une prudence.

Un atome sans relation reste isolé. Un atome relationnel devient utile au manuscrit.

---

## 9. Registres

Mettre à jour uniquement les registres utiles :

```text
registers/references/master_references.md
registers/quotes/master_quotes.md
registers/concepts/master_concepts.md
registers/motifs/master_motifs.md
registers/myths/master_myths.md
registers/chronology/master_chronology.md
registers/people/master_people.md
```

Les registres servent à :

- stabiliser ;
- superviser ;
- cartographier ;
- contrôler la cohérence ;
- éviter les doublons ;
- préparer le RAG.

Ils ne sont pas des brouillons de rédaction et ne doivent pas devenir des zones de prose libre.

---

## 10. Workflow quotidien

### Étape 1 — Lecture stratégique

Lire : livre, article, interview, bootleg, presse, archive, notice discographique, témoignage, document iconographique.

Objectif : identifier uniquement les passages qui structurent réellement le livre.

Chercher : passages pivots, concepts, motifs, mythes, contradictions, scènes importantes, formulations fortes, témoignages décisifs, éléments de chronologie, tensions entre sources.

Ne pas chercher : tout extraire, tout résumer, atomiser tout le livre, multiplier les reformulations.

### Étape 2 — Source canonique

Fixer ou créer la source dans `data/registre.json` avant tout atome définitif.

### Étape 3 — Extraction sélective

Créer uniquement les atomes critiques, relationnels et argumentatifs.

### Étape 4 — Enrichissement v2

Qualifier `role_argumentatif`, `niveau_preuve`, `stabilite`, `importance`, `risque_surinterpretation`, `motifs`, `concepts_derives`, `relations`, `couche_narrative`, `usage_livre`.

### Étape 5 — Relations

Créer les liens utiles vers atomes, concepts, motifs, mythes, citations ou chapitres.

### Étape 6 — Registres

Mettre à jour seulement les registres nécessaires.

### Étape 7 — Exports

```bash
python3 tools/build_registers.py --strict
```

Résultat attendu :

```text
errors  : 0
unknown : 0
```

Les warnings v2 peuvent rester nombreux tant que les anciens atomes ne sont pas tous enrichis. Ce n’est pas bloquant si les erreurs sont à zéro.

### Étape 8 — Audit

```bash
python3 tools/audit_repo.py
```

Sorties :

```text
exports/generated/audit_repo.md
exports/generated/audit_repo.json
exports/generated/audit_repo_issues.csv
```

Résultat attendu :

```text
errors  : 0
unknown : 0
```

### Étape 9 — Documents maîtres

```bash
python3 tools/build_master_docs.py
```

Sorties :

```text
chapters/01/document_maitre.md
...
chapters/14/document_maitre.md
```

### Étape 10 — Publication des exports pour le RAG Studio

Le RAG Studio publié sur GitHub Pages ne lit pas directement le repo local. Il lit les exports publiés dans :

```text
exports/generated/
```

Après une nouvelle atomisation, les sources peuvent être présentes localement dans `sources/`, `chapters/` ou les registres, mais rester invisibles dans le RAG si les exports générés ne sont pas poussés.

Après :

```bash
python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py
```

committer les fichiers de travail :

```bash
git add data/registre.json sources/ registers/ chapters/
```

Puis pousser explicitement les exports nécessaires au RAG, même s’ils sont ignorés par `.gitignore` :

```bash
git add -f exports/generated/all_records.json \
  exports/generated/index_by_id.json \
  exports/generated/diagnostics.json \
  exports/generated/atoms.json \
  exports/generated/atoms.csv \
  exports/generated/sources.json \
  exports/generated/sources.csv \
  exports/generated/master_docs_index.json
```

Puis :

```bash
git commit -m "Update atomized sources and generated RAG exports"
git push
```

Après le push :

```text
https://adminquest.github.io/joy-division-ai-writing-studio/apps/rag-studio/
Cmd + Shift + R
```

Résultat attendu : les nouvelles sources apparaissent dans « Sources atomisées », les filtres RAG 2 sont mis à jour, les regroupements RAG 3 et prompts RAG 4 intègrent les nouveaux atomes.

---

## 11. RAG Studio

Interface principale :

```text
https://adminquest.github.io/joy-division-ai-writing-studio/apps/rag-studio/
```

### RAG 1 — Recherche lexicale

Recherche par mots-clés dans le corpus.

Exemples :

```text
Electric Circus punk Manchester
Hannett live sound studio frustration
Curtis epilepsy domestic life
An Ideal for Living controversy
```

### RAG 2 — Filtres structurés

Filtres par chapitre, source, type documentaire, type d’atome, importance, niveau de preuve, concept, motif.

Exemples :

```text
Chapitre 2 + Source S74
Chapitre 2 + Importance critique
Curtis epilepsy + Type documentaire atom
```

### RAG 3 — Dossier regroupé

Regroupement automatique des résultats par rôle documentaire :

```text
faits établis
scènes fondatrices
lectures / interprétations
mythes à déconstruire
controverses
citations
concepts / motifs
points de vigilance
autres résultats
```

Le bouton « Copier le dossier » exporte un dossier documentaire en Markdown.

### RAG 4 — Prompt de rédaction autonome

Génère un prompt directement utilisable dans une IA externe.

Le prompt contient :

- objectif ;
- périmètre du corpus ;
- index rapide ;
- dossier documentaire autonome ;
- dossier regroupé ;
- citations disponibles ;
- contraintes historiographiques ;
- contraintes stylistiques ;
- consigne de rédaction.

Point décisif : RAG 4 embarque le contenu utile des atomes. Il ne renvoie plus seulement à des identifiants codés dans le repo.

---

## 12. Usage dans une IA de rédaction

Trois modes sont possibles.

### Mode 1 — IA avec accès au repo

Possible seulement si l’IA dispose d’un accès GitHub, web ou connecteur.

Donner l’URL :

```text
https://github.com/AdminQuest/joy-division-ai-writing-studio
```

Et préciser les chemins utiles :

```text
chapters/02/document_maitre.md
registers/quotes/master_quotes.md
registers/references/master_references.md
exports/generated/all_records.json
```

Mode moins stable.

### Mode 2 — IA avec sources déposées

Mode recommandé pour ChatGPT Projects, Claude Projects ou NotebookLM.

Déposer en priorité :

```text
chapters/01/document_maitre.md
...
chapters/14/document_maitre.md
```

Puis les registres transversaux :

```text
registers/quotes/master_quotes.md
registers/references/master_references.md
registers/concepts/master_concepts.md
registers/motifs/master_motifs.md
registers/myths/master_myths.md
registers/chronology/master_chronology.md
registers/people/master_people.md
```

À éviter sauf besoin technique :

```text
exports/generated/all_records.json
exports/generated/atoms.json
```

Ces fichiers sont utiles pour un moteur, mais moins lisibles pour une IA de rédaction.

### Mode 3 — Prompt RAG 4 autonome

Mode le plus portable.

Procédure : filtrer dans RAG Studio, vérifier le dossier RAG 3, générer le prompt RAG 4, copier le prompt, coller dans l’IA, demander une rédaction ou une reprise ciblée.

Ce mode fonctionne même si l’IA n’a pas accès au repo.

---

## 13. Commandes terminal

Toujours lancer les commandes depuis la racine du repo.

### Migration minimale v2

```bash
python3 tools/migrate_atoms_v2.py
```

À utiliser après ajout d’anciens atomes, import legacy ou anciennes atomisations.

### Génération des registres / exports

```bash
python3 tools/build_registers.py --strict
```

À utiliser après ajout ou modification d’atomes, avant audit, avant documents maîtres, avant session rédactionnelle importante.

### Audit du repo

```bash
python3 tools/audit_repo.py
```

À utiliser après génération des registres, avant commit important, après intégration de nouvelles sources.

### Génération des documents maîtres

```bash
python3 tools/build_master_docs.py
```

À utiliser après génération des registres et avant dépôt dans une IA.

### Diagnostics historiographiques

```bash
python3 tools/build_historiographical_diagnostics.py
```

À utiliser après enrichissements importants ou avant rédaction d’un chapitre.

### Graphe documentaire

```bash
python3 tools/build_graph.py
```

À utiliser après ajout de relations et avant revue structurelle.

### Contexte IA

```bash
python3 tools/build_prompt_context.py
```

À utiliser avant usage intensif de l’IA.

### Portail local

```bash
python3 -m http.server 8000
```

Puis ouvrir :

```text
http://localhost:8000/apps/rag-studio/
```

---

## 14. Workflow hebdomadaire

Ordre recommandé :

```bash
python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py
python3 tools/build_historiographical_diagnostics.py
python3 tools/build_graph.py
python3 tools/build_prompt_context.py
```

Puis :

```bash
git add data/registre.json sources/ registers/ chapters/
git add -f exports/generated/all_records.json \
  exports/generated/index_by_id.json \
  exports/generated/diagnostics.json \
  exports/generated/atoms.json \
  exports/generated/atoms.csv \
  exports/generated/sources.json \
  exports/generated/sources.csv \
  exports/generated/master_docs_index.json

git commit -m "Update documentary corpus and generated RAG exports"
git push
```

Objectifs : cohérence, stabilité, supervision, contrôle des dérives, préparation rédactionnelle, mise à jour du RAG.

---

## 15. Workflow de rédaction

Ordre recommandé :

1. Ouvrir RAG Studio.
2. Filtrer par chapitre, source, importance, concept ou motif.
3. Lire les résultats RAG 2.
4. Vérifier le regroupement RAG 3.
5. Générer le prompt RAG 4.
6. Copier le prompt autonome.
7. Coller dans l’IA de rédaction.
8. Faire produire une section.
9. Réviser humainement.
10. Réinjecter les éventuelles nouvelles relations ou prudences dans le repo.

La rédaction ne doit jamais produire directement de nouveaux faits sans retour au système documentaire.

---

## 16. Workflow mobile

Depuis téléphone, sont autorisés : lecture, annotation, enrichissement qualitatif, relations, concepts, motifs, mythes, qualification historiographique, préparation de prompts, consultation RAG Studio.

À éviter : refactoring, migration massive, restructuration, automatisations lourdes, renommage d’identifiants, modification du schéma.

Le téléphone est un outil d’enrichissement qualitatif, pas de maintenance lourde.

---

## 17. Priorités documentaires

Sources prioritaires : Peter Hook, Deborah Curtis, Martin Hannett, Simon Reynolds, Factory, Tony Wilson, Rob Gretton, Manchester, Salford, *Unknown Pleasures*, *Closer*, RCA sessions, *An Ideal for Living*, bootlegs majeurs, performances live, archives visuelles, réception contemporaine.

Axes prioritaires : spatialité sonore, désindustrialisation, Factory, Hannett, Saville, Curtis, Gretton, mythes rétrospectifs, controverses, mémoire ouvrière, mélancolie post-industrielle, géographie émotionnelle, spectralité, culture bootleg, postérité numérique.

---

## 18. Interdits

Sont interdits :

- atomisation exhaustive ;
- nouveaux schémas concurrents ;
- duplication documentaire ;
- registres improvisés ;
- renommage d’identifiants ;
- réutilisation d’un identifiant source déjà attribué ;
- atomisation d’une source non canonisée ;
- oubli de pousser les exports générés après atomisation ;
- workflows parallèles ;
- rédaction sans corpus ;
- citation non vérifiée présentée comme certaine ;
- fusion entre témoignage et fait établi ;
- téléologie morbide autour de Curtis ;
- ajout d’atomes faibles ;
- multiplication d’exports non maintenus.

---

## 19. Objectif final

Le système doit progressivement devenir stable, relationnel, historiographiquement prudent, maintenable, dense, non redondant, exploitable par IA, utile à la rédaction et contrôlable humainement.

Le livre se construit depuis les relations.

Les atomes sont la matière.

Les registres sont la mémoire.

Les documents maîtres sont les dossiers de rédaction.

Le RAG Studio est l’atelier de sélection.

RAG 4 est le pont vers l’IA.

La rédaction est l’ultime projection narrative du système.
