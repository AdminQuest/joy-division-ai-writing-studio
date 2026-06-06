# M2 - Bilan final officiel

## 1. Rappel de l'objectif de M2

M2 a ete lance pour transformer le depot Joy Division AI Writing Studio en
studio d'enrichissement documentaire.

A la fin de M1, le projet disposait d'un socle plus fiable :

- les documents maitres etaient mieux relies aux atomes, registres et sources ;
- les controles documentaires etaient mieux structures ;
- les ecarts pouvaient etre audites, corriges et revalides ;
- le depot etait suffisamment stabilise pour ouvrir la question des ajouts.

La limite principale restait le passage d'une intention d'enrichissement a une
proposition relisible. Ajouter une personne, une organisation ou une source
longue demandait encore trop de saisies manuelles, trop de reconstitution de
contexte et trop de prudence implicite dans la revue.

M2 a donc vise a industrialiser la preparation documentaire, sans transformer
la preparation en validation automatique.

Principe de phase :

```text
Le studio prepare. L'humain valide.
```

Cette philosophie a guide tous les chantiers M2 :

- les outils peuvent produire des diagnostics ;
- les outils peuvent exposer les bloquants, reserves et informations ;
- les outils peuvent preparer des resumes et rapports ;
- les outils peuvent faciliter la saisie ;
- la decision documentaire reste humaine.

## 2. Architecture obtenue

L'architecture finale de M2 se resume ainsi :

```text
Formulaire
  ->
Adaptateurs
  ->
Diagnostics
  ->
Resumes PR
  ->
Rapports consolides
  ->
Validation humaine
```

Le moteur documentaire reste separe des interfaces.

Le formulaire est une couche de saisie locale. Il produit des commandes ou des
JSON compatibles avec les CLI existantes. Il ne valide pas les objets et ne
duplique pas les regles documentaires.

Les adaptateurs portent les regles metier des familles documentaires :

- `PERSON` ;
- `ORG` ;
- `SOURCE LONGUE`.

Ils connaissent les champs, schemas, collisions, reserves et diagnostics propres
a leur famille.

Le noyau commun reste generique. Il porte les structures et rendus partages :

- diagnostics ;
- decisions ;
- resumes de PR ;
- resultats batch ;
- rapports consolides.

Il ne connait pas les details metier des personnes, organisations ou sources
longues.

## 3. Chantiers realises

### Noyau commun

Le noyau commun M2 a ete stabilise dans `tools/m2_core.py`.

Il mutualise les invariants communs aux flux M2 :

- `CheckResult` ;
- listes de `blockers`, `reserves` et `information` ;
- calcul de decision ;
- deduplication preservant l'ordre ;
- rendu commun des diagnostics ;
- structures communes pour les resumes PR ;
- structures communes pour les campagnes batch.

La decision M2 est stable :

- `pre-validee` ;
- `pre-validee avec reserve` ;
- `non pre-validee`.

Le noyau commun ne porte aucune logique documentaire specifique a une famille.

### PERSON

Le prototype PERSON a ete implemente dans `tools/m2_add_person.py`.

Il permet de preparer une proposition d'ajout PERSON en lecture seule :

- proposition d'identifiant `PERSON-*` ;
- verification des sources `Sxx` ;
- verification du schema PERSON ;
- detection de collisions de nom, alias, identifiant et `same_as` ;
- production d'un diagnostic classe ;
- production d'un resume PR lorsque `--pr-summary` est demande.

La documentation et les retours d'usage PERSON ont stabilise le prototype et
ses limites. PERSON sert de modele d'ajout unitaire pour les familles futures.

### ORG

Le prototype ORG a ete implemente dans `tools/m2_add_org.py`.

Il permet de preparer une proposition d'ajout ORG en lecture seule :

- proposition du prochain identifiant `ORG-NNNN` ;
- verification des sources `Sxx` ;
- verification du schema ORG ;
- detection de collisions de nom, alias, identifiant et identifiants externes ;
- qualification de la relation documentee a Joy Division ;
- production d'un diagnostic classe ;
- production d'un resume PR lorsque `--pr-summary` est demande.

ORG a valide que l'architecture adaptateur pouvait couvrir une famille JSON,
numerique et distincte de PERSON.

### SOURCE LONGUE

Le flux SOURCE LONGUE a ete implemente dans
`tools/m2_integrate_source.py`.

Il permet de preparer l'integration documentaire d'une source candidate :

- qualification bibliographique ;
- comparaison avec `data/registre.json` ;
- detection de doublon certain ;
- detection de proximite documentaire ;
- proposition de `Sxx` existant ou probable ;
- proposition de dossier source probable ;
- production d'un diagnostic classe ;
- production d'un resume PR lorsque `--pr-summary` est demande.

Le flux source longue reste volontairement preparatoire. Il ne cree pas de
source canonique, d'atome, de citation ou de relation.

### Preparation de PR

La preparation de PR a ete industrialisee avec `PRSummary` et les fonctions
communes associees.

Chaque flux M2 actif peut produire un resume Markdown standardise :

```text
exports/generated/pr_summary_*.md
```

Le resume expose :

- objet ;
- perimetre ;
- validations executees ;
- bloquants ;
- reserves ;
- informations ;
- arbitrages humains ;
- impact documentaire ;
- commandes de verification.

Le resume PR prepare la revue humaine. Il ne cree pas de branche, n'ouvre pas
de PR GitHub, ne commit pas et ne merge pas.

### Batch

Le batch de pre-validation a ete implemente dans
`tools/m2_batch_prevalidation.py`.

Il permet de traiter une campagne documentaire :

```text
N objets
  -> N diagnostics
  -> 1 rapport consolide
  -> N resumes PR
```

Le moteur batch reste au-dessus des adaptateurs. Il orchestre des objets, des
adaptateurs et des resultats de diagnostic.

Les rapports consolides sont produits en Markdown :

```text
exports/generated/batch_summary_*.md
```

Ils exposent :

- synthese ;
- statistiques ;
- liste des objets ;
- reserves ;
- bloquants ;
- arbitrages humains.

Le batch prepare les campagnes documentaires massives sans modifier les
registres et sans automatiser GitHub.

### Formulaire

Le formulaire M2 a ete implemente dans :

```text
apps/m2-formulaire/
```

Il couvre la saisie :

- `PERSON` ;
- `ORG` ;
- `SOURCE LONGUE` ;
- campagne batch `PERSON` / `ORG`.

Il produit :

- commandes CLI copiables ;
- JSON batch copiable.

Il ne contient aucune logique documentaire autonome. Les validations restent
dans les adaptateurs Python et dans les controles existants.

## 4. Capacites desormais disponibles

M2 dispose desormais des capacites suivantes :

- pre-validation unitaire ;
- diagnostics classes ;
- reserves explicites ;
- arbitrages humains visibles ;
- resumes PR standardises ;
- batch documentaire ;
- rapports consolides ;
- formulaire de saisie.

Ces capacites permettent de preparer une proposition documentaire sans masquer
les risques ni transformer une suggestion en validation.

## 5. Capacites volontairement exclues

M2 ne fait pas :

- validation humaine ;
- creation automatique de sources ;
- creation automatique d'atomes ;
- creation automatique de citations ;
- creation automatique de relations ;
- modification automatique de registres ;
- GitHub automatique ;
- ouverture automatique de Pull Request ;
- merge automatique ;
- decisions documentaires autonomes.

Ces exclusions sont des garde-fous structurants. Elles garantissent que M2 reste
un studio de preparation et non une chaine d'integration automatique.

## 6. Decision de cloture

M2 est considere comme cloture.

Les objectifs de M2 sont atteints.

Le depot dispose maintenant d'une chaine coherente pour passer d'une saisie ou
d'une intention d'enrichissement a une proposition documentee, diagnostiquee,
resumee et relisible par un humain.

La validation finale reste humaine.

## 7. Perspectives M3

Les perspectives M3 ne sont pas arbitrees dans ce document.

Les axes possibles sont :

- ergonomie ;
- assistants documentaires ;
- generation assistee ;
- navigation ;
- outils de redaction ;
- exploitation du graphe documentaire.

M3 devra s'appuyer sur les acquis M2 sans rouvrir les arbitrages de cloture :
separation entre saisie, logique documentaire, diagnostics et validation
humaine.
