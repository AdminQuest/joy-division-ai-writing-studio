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

- `sources/` conserve la matière documentaire atomisée. Les PDF/OCR bruts ne sont pas versionnés dans Git.
- Les atomes extraient les unités historiographiques importantes.
- `registers/` stabilise références, citations, concepts, motifs, mythes, personnes, chansons et chronologies.
- `exports/generated/` rend le corpus exploitable par les outils et le RAG Studio.
- Les diagnostics contrôlent la santé du repo.
- `chapters/XX/document_maitre.md` fournit les dossiers documentaires par chapitre.
- Le RAG Studio permet de chercher, filtrer, regrouper et préparer les corpus de rédaction.
- RAG 4 produit des prompts autonomes exploitables dans une IA externe.
- Le manuscrit est rédigé à partir de ces états documentaires, jamais depuis une accumulation brute de sources.

---

## 2. Statut des documents maîtres

Les documents maîtres ne sont pas des sources primaires. Ils sont des dossiers documentaires de rédaction, produits depuis les atomes.

Ils servent à préparer l’écriture d’un chapitre, donner à l’IA un corpus lisible, synthétiser les atomes par chapitre, repérer sources, citations, motifs, concepts et risques, et contrôler les lacunes documentaires.

Ils ne prouvent pas seuls. La preuve reste dans les atomes, les citations, les références et les sources d’origine.

Les documents maîtres sont les fichiers à déposer en priorité dans les sources d’une IA de rédaction :

```text
chapters/01/document_maitre.md
...
chapters/14/document_maitre.md
```

### 2.1. Règle impérative : aucun dossier `chapters/addenda/`

Le dossier `chapters/addenda/` est interdit. Il crée un flux parallèle non lu par `tools/build_registers.py`, donc non intégré de manière fiable aux exports et aux documents maîtres.

Tout complément destiné à un chapitre doit être placé directement dans le dossier du chapitre concerné :

```text
chapters/01/source_notes_sXX.md
chapters/11/source_notes_sXX.md
chapters/14/source_notes_sXX.md
```

Tout atome, source part ou fichier de passe destiné aux documents maîtres doit être placé dans `sources/<slug>/` sous forme de Markdown contenant des blocs YAML lisibles par le parser. Les notes de chapitre servent seulement à orienter l’usage rédactionnel ; la matière documentaire structurée reste dans `sources/` et `registers/`.

Règle de contrôle : après toute intégration, la commande suivante ne doit retourner aucun fichier :

```bash
find chapters -path "*/addenda/*" -type f
```

Si une source concerne plusieurs chapitres, créer un fichier `source_notes_sXX.md` dans chaque dossier de chapitre concerné, ou un fichier groupé du type `source_notes_s13_s39_s40.md` lorsque la note porte sur plusieurs sources dans le même chapitre.


### 2.2. Injection des notes de chapitre dans les documents maîtres

Les fichiers `chapters/XX/source_notes*.md` sont lus après la génération des documents maîtres. Ils sont injectés dans une section dédiée des `chapters/XX/document_maitre.md`.

Commande recommandée après `build_registers.py` et `audit_repo.py` :

```bash
python3 tools/build_master_docs.py
python3 tools/inject_chapter_source_notes.py
```

Commande équivalente en un seul appel :

```bash
python3 tools/build_master_docs_with_notes.py
```

Il est interdit de recréer `chapters/addenda/`. Toute note transversale doit être dispatchée dans les dossiers `chapters/XX/` concernés.

---

## 3. Règle impérative pour toute atomisation

Toute demande du type :

```text
Atomise cette source.
Atomise ce passage.
Ajoute cette source au repo.
Intègre ce passage selon le workflow industrialisé.
```

signifie obligatoirement : créer ou modifier directement les fichiers nécessaires dans le repo GitHub.

Il est interdit de répondre uniquement par une archive locale, un dossier temporaire ou un contenu non intégré. Le travail n’est considéré comme fait que lorsque les fichiers sont créés ou modifiés dans le repo avec des commits effectifs.

La procédure historique détaillée reste disponible dans :

```text
docs/ATOMISATION_SOURCE.md
```

La présente page fixe le workflow opérationnel courant.

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

Règles :

1. Une source = un identifiant canonique stable.
2. Ne jamais réutiliser un identifiant déjà attribué.
3. Ne jamais confondre deux livres d’un même auteur.
4. Tout atome doit porter le `source_id` canonique.
5. Toute nouvelle source doit être ajoutée à `data/registre.json` avant atomisation définitive.
6. Les anciens identifiants ou alias servent seulement à la migration.
7. Pour les sources longues, créer des fichiers de passages successifs : `source_part_01.md`, `source_part_02.md`, etc.

Exemple de dossier source :

```text
sources/ott_unknown_pleasures/
  source_part_01.md
  source_part_02.md
```

Exemple d’entrée canonique :

```json
{
  "id": "S75",
  "source_label": "S75 — Ott, Joy Division's Unknown Pleasures, 2004",
  "auteur": "Chris Ott",
  "titre": "Joy Division's Unknown Pleasures",
  "annee": "2004",
  "statut": "atomisation sélective v2",
  "usage": "Unknown Pleasures ; RCA ; Hannett ; Factory ; réception ; mythologies critiques"
}
```

---

## 5. Doctrine documentaire v2 : l’atome comme unité de raisonnement

Depuis la version 2, l’atomisation ne consiste plus à découper exhaustivement les sources en fragments. Chaque atome devient une unité interprétative enrichie.

Un atome mérite d’exister s’il structure un chapitre, relie plusieurs concepts, nourrit le graphe relationnel, éclaire un mythe, stabilise un concept, apporte une contradiction, possède une forte densité narrative, documente une rupture esthétique ou reste réutilisable.

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
- `relations` : liens avec autres atomes, concepts, mythes, citations ou chapitres ;
- `usage_livre` : chapitres où l’atome doit remonter dans les documents maîtres.

---

## 7. Types documentaires et niveau de preuve

Typologies prioritaires :

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
session_radio
lieu
objet_visuel
objet_discographique
archive
archive_visuelle
bootleg
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
interprétation critique appuyée sur écoute
mythe institutionnel avec noyau factuel
```

Tout atome doit signaler les risques qui existent : téléologie, mythologisation, psychologisation, surinterprétation, reconstruction mémorielle douteuse, lecture prophétique de Ian Curtis, Manchester comme matrice absolue, héroïsation de Hannett, romantisation de Factory, sursymbolisation des ruines industrielles.

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

Les relations doivent permettre de repérer ce qui confirme, contredit, nuance, mythologise, déconstruit, déplace un concept, rattache deux chapitres ou signale une prudence.

Un atome sans relation reste isolé. Un atome relationnel devient utile au manuscrit.

---

## 9. Registres

Les registres sont la mémoire stable du repo. Ils ne sont pas des brouillons de rédaction et ne doivent pas devenir des zones de prose libre.

### Registres structurants

Ils stabilisent les grandes catégories interprétatives :

```text
registers/concepts/master_concepts.md
registers/motifs/master_motifs.md
registers/myths/master_myths.md
```

Ils ne doivent être enrichis que si le passage crée un vrai nœud durable. Sinon, les atomes pointent vers l’existant.

### Registres spécialisés

Ils créent des points d’entrée transversaux :

```text
registers/quotes/
registers/chronology/
registers/people/
registers/songs/
registers/references/
```

Ils ne doivent pas être exhaustifs. Ils reçoivent uniquement les citations, dates, personnes et chansons réellement réutilisables.

Pour une source longue déjà ouverte, préférer des fichiers spécialisés par source ou par tranche :

```text
registers/quotes/s75_ott_quotes.md
registers/chronology/s75_ott_chronology.md
registers/songs/s75_ott_songs_part_02.md
registers/people/s75_ott_people_part_02.md
registers/concepts/s75_ott_concepts_part_02.md
```

Les citations restent candidates tant qu’elles n’ont pas été vérifiées mot à mot sur le PDF/OCR ou l’édition papier.

---

## 10. Workflow industrialisé d’atomisation d’un passage

Le mode normal n’est plus l’enchaînement artisanal : atomisation → relations → concepts → motifs → mythes → citations → dates → personnes → chansons → documents maîtres → RAG.

Pour un passage donné, produire un paquet complet en une seule passe.

### Entrée attendue

L’utilisateur fournit un passage, un PDF/OCR ou un extrait, et indique :

```text
Atomise et intègre ce nouveau passage de SXX selon le workflow industrialisé.
Je veux une passe complète : atomes v2, relations stabilisées, registres, documents maîtres, RAG, commandes et contrôles.
Ne fragmente pas le traitement en étapes successives.
```

### Sortie attendue

Le traitement doit créer ou modifier directement :

```text
1. sources/<slug>/source_part_XX.md
2. registres structurants si nécessaire seulement
3. registres spécialisés utiles
4. notes de chapitre éventuelles dans chapters/XX/source_notes_sXX.md
5. scripts de patch ou cleanup si un correctif local est nécessaire
6. consignes terminal pour build_registers / audit / build_master_docs
7. contrôles grep
8. commande git add / commit / push
```

Interdiction absolue : ne jamais créer de fichier dans `chapters/addenda/`. Un addendum transversal n’est pas lu par le pipeline documentaire et devient une source d’erreur. Si un complément concerne plusieurs chapitres, il doit être dispatché dans les dossiers `chapters/XX/` concernés.

### Contenu minimal du paquet

Le paquet doit comprendre :

```text
- atomes v2 complets ;
- relations déjà stabilisées vers CONCEPT-XXX, MOTIF-XXX, MYTH-XXX ou SXX-AXXX ;
- nouveaux concepts / motifs / mythes uniquement si l’existant ne suffit pas ;
- citations candidates limitées ;
- dates structurantes limitées ;
- personnes réellement utiles ;
- chansons réellement utiles ;
- rattachement aux chapitres via usage_livre ;
- notes de chapitre éventuelles dans chapters/XX/ ;
- prudences historiographiques ;
- commandes terminal finales.
```

### Ratio recommandé

Pour un passage de 20 à 40 pages, viser en principe :

```text
10 à 20 atomes maximum ;
0 à 1 concept structurant nouveau ;
0 à 2 motifs ou mythes nouveaux ;
2 à 5 citations candidates ;
3 à 10 dates structurantes ;
3 à 10 personnes ;
3 à 10 chansons.
```

Ces chiffres ne sont pas des plafonds mécaniques. Ils servent à empêcher l’indexation exhaustive.

### Règle sur les relations candidates

Les relations doivent pointer d’abord vers les entrées existantes :

```text
CONCEPT-004 — prudence historiographique
CONCEPT-005 — contrainte productive
CONCEPT-006 — architecture sonore
MOTIF-004 — culture bootleg
MOTIF-006 — seuil
MYTH-002 — Ian Curtis comme prophète
MYTH-003 — Manchester comme matrice unique
MYTH-004 — Martin Hannett comme génie solitaire
MYTH-005 — Factory comme anti-business pur
MYTH-006 — Le génie immédiat de Joy Division
MYTH-007 — L’imagerie nazie comme fascination fasciste
```

Si une cible n’existe pas encore, utiliser provisoirement :

```yaml
relations:
  - type: prépare
    cible: CONCEPT-xxx
    note: "Concept candidat à créer seulement si confirmé par plusieurs atomes."
```

Puis créer l’entrée canonique dans le même paquet si elle est manifestement structurante.

### Cas S75 comme modèle

Le modèle opérationnel est le traitement de Chris Ott, `S75`, part 2 :

```text
sources/ott_unknown_pleasures/source_part_02.md
registers/quotes/s75_ott_quotes.md
registers/chronology/s75_ott_chronology.md
registers/concepts/s75_ott_concepts_part_02.md
registers/songs/s75_ott_songs_part_02.md
registers/people/s75_ott_people_part_02.md
```

Ce modèle évite vingt allers-retours : un seul paquet crée les atomes, relations, registres spécialisés et commandes de régénération.

---

## 11. Chaîne locale obligatoire après chaque paquet

Après réception d’un paquet industrialisé, lancer depuis la racine du repo :

```bash
git pull
```

Si un script de nettoyage a été ajouté :

```bash
python3 tools/<script_de_cleanup>.py
```

Puis :

```bash
python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py
```

Résultat attendu :

```text
errors  : 0
unknown : 0
```

Les warnings v2 peuvent rester nombreux tant que les anciens atomes ne sont pas tous enrichis. Ce n’est pas bloquant si les erreurs sont à zéro.

---

## 12. Publication des exports pour le RAG Studio

Le RAG Studio publié sur GitHub Pages ne lit pas directement le repo local. Il lit les exports publiés dans :

```text
exports/generated/
```

Après une nouvelle atomisation, les sources peuvent être présentes localement dans `sources/`, `chapters/` ou les registres, mais rester invisibles dans le RAG si les exports générés ne sont pas poussés.

Après génération :

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
  exports/generated/quotes.json \
  exports/generated/quotes.csv \
  exports/generated/songs.json \
  exports/generated/songs.csv \
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

Si GitHub Pages semble afficher une ancienne version, attendre 1 à 3 minutes, puis ajouter un paramètre de cache :

```text
https://adminquest.github.io/joy-division-ai-writing-studio/apps/rag-studio/?v=YYYYMMDD-HHMM
```

---

## 13. Contrôles grep standard après un paquet

Contrôler la présence des nouveaux atomes :

```bash
grep -R "SXX-A" sources/<slug>/
```

Contrôler la remontée dans les documents maîtres :

```bash
grep -R "SXX-A\|SXX —" chapters/*/document_maitre.md
```

Contrôler qu’aucun addendum transversal n’a été créé :

```bash
find chapters -path "*/addenda/*" -type f
```

Contrôler les registres spécialisés :

```bash
grep -R "SXX-Q\|CHR-\|SONG-SXX\|PERS-SXX\|CONCEPT-" registers/
```

Contrôler les exports RAG :

```bash
grep -n "SXX" exports/generated/all_records.json | head
```

Pour S75 :

```bash
grep -R "S75-A021\|S75-A038\|CONCEPT-007" sources/ott_unknown_pleasures/
grep -R "S75-A021\|S75-A038\|CONCEPT-007" chapters/*/document_maitre.md
grep -R "S75-Q009\|CHR-1979-003\|SONG-S75-012\|PERS-S75-024" registers/
```

---

## 14. RAG Studio

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

### RAG 3 — Dossier regroupé

Regroupement automatique des résultats par rôle documentaire : faits établis, scènes fondatrices, lectures / interprétations, mythes à déconstruire, controverses, citations, concepts / motifs, points de vigilance, autres résultats.

Le bouton « Copier le dossier » exporte un dossier documentaire en Markdown.

### RAG 4 — Prompt de rédaction autonome

Génère un prompt directement utilisable dans une IA externe.

Point décisif : RAG 4 embarque le contenu utile des atomes. Il ne renvoie plus seulement à des identifiants codés dans le repo.

---

## 15. Usage dans une IA de rédaction

Trois modes sont possibles.

### Mode 1 — IA avec accès au repo

Possible seulement si l’IA dispose d’un accès GitHub, web ou connecteur.

```text
https://github.com/AdminQuest/joy-division-ai-writing-studio
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
registers/quotes/
registers/references/
registers/concepts/
registers/motifs/
registers/myths/
registers/chronology/
registers/people/
registers/songs/
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

---

## 16. Commandes terminal

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

## 17. Workflow hebdomadaire

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
  exports/generated/quotes.json \
  exports/generated/quotes.csv \
  exports/generated/songs.json \
  exports/generated/songs.csv \
  exports/generated/sources.json \
  exports/generated/sources.csv \
  exports/generated/master_docs_index.json

git commit -m "Update documentary corpus and generated RAG exports"
git push
```

Objectifs : cohérence, stabilité, supervision, contrôle des dérives, préparation rédactionnelle, mise à jour du RAG.

---

## 18. Workflow de rédaction

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

## 19. Workflow mobile

Depuis téléphone, sont autorisés : lecture, annotation, enrichissement qualitatif, relations, concepts, motifs, mythes, qualification historiographique, préparation de prompts, consultation RAG Studio.

À éviter : refactoring, migration massive, restructuration, automatisations lourdes, renommage d’identifiants, modification du schéma.

Le téléphone est un outil d’enrichissement qualitatif, pas de maintenance lourde.

---

## 20. Priorités documentaires

Sources prioritaires : Peter Hook, Deborah Curtis, Martin Hannett, Simon Reynolds, Factory, Tony Wilson, Rob Gretton, Manchester, Salford, *Unknown Pleasures*, *Closer*, RCA sessions, *An Ideal for Living*, bootlegs majeurs, performances live, archives visuelles, réception contemporaine.

Axes prioritaires : spatialité sonore, désindustrialisation, Factory, Hannett, Saville, Curtis, Gretton, mythes rétrospectifs, controverses, mémoire ouvrière, mélancolie post-industrielle, géographie émotionnelle, spectralité, culture bootleg, postérité numérique.

---

## 21. Interdits

Sont interdits :

- atomisation exhaustive ;
- nouveaux schémas concurrents ;
- duplication documentaire ;
- registres improvisés ;
- création ou maintien d’un dossier `chapters/addenda/` ;
- ajout d’un complément documentaire dans un dossier transversal non lu par le pipeline ;
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

## 22. Objectif final

Le système doit progressivement devenir stable, relationnel, historiographiquement prudent, maintenable, dense, non redondant, exploitable par IA, utile à la rédaction et contrôlable humainement.

Le livre se construit depuis les relations.

Les atomes sont la matière.

Les registres sont la mémoire.

Les documents maîtres sont les dossiers de rédaction.

Le RAG Studio est l’atelier de sélection.

RAG 4 est le pont vers l’IA.

La rédaction est l’ultime projection narrative du système.
