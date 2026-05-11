# Joy Division — AI Writing Studio

Environnement local de pilotage documentaire et rédactionnel pour la production du livre *Joy Division, le son de l’éternel*.

Le projet combine deux fonctions distinctes :

- un **Prompt Studio**, destiné à construire des prompts contraints pour la rédaction, la relecture et le contrôle éditorial ;
- un **RAG Studio**, destiné à interroger localement le corpus atomisé : sources, citations, registres, chansons, personnes et événements.

Le système n’est pas conçu comme un générateur de texte autonome. Il vise à structurer le travail de recherche, sécuriser les sources et fournir à l’IA des matériaux contrôlés.

---

## 0. Règle impérative pour toute atomisation

Toute demande du type :

```text
Atomise cette source.
Atomise ce livre.
Ajoute cette source au repo.
```

signifie obligatoirement :

```text
Créer ou modifier directement les fichiers nécessaires dans le repo GitHub.
```

Il est interdit de répondre uniquement par une archive locale, un dossier local, un fichier temporaire ou un contenu à copier-coller. Le travail n’est considéré comme fait que lorsque les fichiers sont créés ou modifiés dans le repo avec des commits effectifs.

La procédure obligatoire est décrite ici :

```text
docs/ATOMISATION_SOURCE.md
```

Cette procédure prime sur toute pratique antérieure.

---

## 0 bis. Doctrine documentaire v2 — l’atome comme unité de raisonnement

Depuis la version 2 du repo, l’atomisation ne consiste plus uniquement à découper des sources en fragments documentaires.

Chaque atome devient une unité interprétative enrichie.

L’objectif n’est plus seulement :

- stocker ;
- retrouver ;
- citer.

Le système doit désormais permettre :

- la propagation conceptuelle ;
- le contrôle des dérives interprétatives ;
- la qualification du niveau de preuve ;
- la détection des mythologies rétrospectives ;
- la cartographie argumentative du livre ;
- un RAG sémantique avancé.

Les atomes doivent donc intégrer :

- rôle argumentatif ;
- niveau de preuve ;
- stabilité ;
- importance ;
- risque de surinterprétation ;
- liens interchapitres ;
- liens vers citations ;
- motifs ;
- concepts dérivés.

Le repo devient ainsi progressivement :

```text
un environnement historiographique assisté par IA
```

et non plus un simple manuscrit augmenté.

---

## 1. Convention unique de codification des sources

Toute source intellectuelle mobilisée dans le repo doit respecter le format suivant :

```text
SXX — Auteur, Titre court, Année
```

Exemples :

```text
S41 — Hook, Unknown Pleasures, 2012
S45 — Curtis, Touching from a Distance, 1995
S68 — Broll, Joy Division, s.d.
S69 — Greig & Strong, But We Remember When We Were Young, 2014
```

Règles :

1. `SXX` est l’identifiant source canonique.
2. Si une source existe déjà dans le registre, son numéro est conservé.
3. Si une source nouvelle n’existe pas dans le registre, elle reçoit le prochain numéro libre.
4. Les anciens identifiants longs ou techniques sont traités comme alias de migration, jamais comme identifiants d’affichage.
5. Chaque atome, citation ou événement doit porter le champ `source_id` canonique.
6. Les interfaces doivent afficher le champ `source_label` lorsqu’il existe.
7. Toute nouvelle source doit être ajoutée à `data/registre.json`.

---

## 2. Architecture générale

```text
joy-division-ai-writing-studio/

  index.html

  apps/
  data/
  sources/
  registers/
  schemas/
  tools/
  exports/
  indexes/
  docs/
```

Le repo fonctionne désormais comme :

```text
sources atomisées
→ atomes enrichis
→ registres consolidés
→ exports structurés
→ moteur RAG
→ pilotage rédactionnel
```

---

## 3. Atomes enrichis

Un atome version 2 doit désormais répondre aux questions suivantes :

| Question | Champ |
|---|---|
| Que dit l’atome ? | contenu |
| Pourquoi compte-t-il ? | role_argumentatif |
| Est-ce solide ? | niveau_preuve |
| Est-ce stable ? | stabilite |
| Quel poids a-t-il ? | importance |
| Où devient-il dangereux ? | risque_surinterpretation |
| Où circule-t-il dans le livre ? | liens_interchapitres |
| À quelles citations est-il relié ? | liens_citations |
| Quels motifs mobilise-t-il ? | motifs |
| Quels concepts secondaires produit-il ? | concepts_derives |

Les schémas documentaires imposent désormais cette structure.

---

## 4. Types documentaires d’atomes

Les atomes ne doivent plus être implicitement homogènes.

Le repo distingue désormais explicitement :

```text
fait
lecture
concept
citation_clef
mythe
controverse
```

Cette distinction est essentielle pour éviter :

- la confusion entre mémoire et fait ;
- la téléologie ;
- la mythologisation de Joy Division ;
- les dérives interprétatives.

---

## 5. Niveau de preuve

Le champ `niveau_preuve` devient obligatoire.

Il distingue :

```text
établi
fortement corroboré
corroboré
plausible
fragile
contesté
hypothèse
```

Cette qualification devient centrale pour :

- les usages IA ;
- les exports ;
- les contrôles documentaires ;
- les synthèses automatiques.

---

## 6. Risque de surinterprétation

Tout atome doit désormais expliciter son risque de dérive interprétative.

Exemples typiques dans le corpus Joy Division :

- lecture prophétique de Ian Curtis ;
- téléologie du post-punk ;
- Manchester comme matrice absolue ;
- sursymbolisation des ruines industrielles.

Ce champ devient critique pour :

- les prompts IA ;
- les synthèses automatiques ;
- la stabilisation historiographique.

---

## 7. Motifs et concepts dérivés

Les motifs permettent de suivre les récurrences sensibles ou symboliques :

```text
ruine industrielle
isolement
spectralité
froideur
mémoire ouvrière
fragmentation
```

Les concepts dérivés permettent de suivre les dérivations interprétatives secondaires :

```text
ville spectrale
hantologie sonore
cartographie émotionnelle
futur perdu
```

Cette couche devient essentielle pour les futures recherches transversales.

---

## 8. RAG enrichi

Le système RAG ne doit plus fonctionner seulement par proximité lexicale.

Les nouveaux champs permettront progressivement :

- recherche argumentative ;
- recherche conceptuelle ;
- recherche probabiliste ;
- recherche historiographique.

Exemple cible :

```text
retrouver tous les atomes fortement corroborés
liant Hannett, spatialisation sonore et mémoire industrielle
sans utiliser Fisher
```

---

## 9. Parseur documentaire

Le parseur documentaire devient désormais responsable :

- de la validation des champs enrichis ;
- du contrôle des types ;
- de la cohérence des niveaux de preuve ;
- du contrôle des listes argumentatives ;
- de la préparation d’un graphe documentaire.

Le parseur est lancé avec :

```bash
python tools/build_registers.py --strict
```

---

## 10. Objectif stratégique

Le projet ne vise plus uniquement à écrire un livre.

Le repo devient progressivement :

```text
une base historiographique vivante sur Joy Division,
Manchester et le post-punk.
```

L’écriture finale devient alors une orchestration narrative d’atomes enrichis, et non un simple empilement documentaire.
