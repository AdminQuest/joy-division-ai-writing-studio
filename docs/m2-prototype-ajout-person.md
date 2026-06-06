# M2.5 - Prototype d'ajout PERSON

## 1. Objet du prototype

Le prototype d'ajout `PERSON` definit le premier flux operationnel cible du Studio M2 sans interface graphique. Il decrit comment un assistant pourrait preparer l'ajout d'une personne canonique dans le corpus, en s'appuyant sur le modele reel du depot.

Perimetre :

- un seul objet principal de type `PERSON-` ;
- qualification des champs requis par `schemas/person_canonical.schema.json` ;
- verification de l'unicite de l'identifiant et des collisions de nom ou d'alias ;
- verification des sources `Sxx` contre `data/registre.json` ;
- preparation d'une entree candidate compatible avec le schema canonique ;
- preparation d'un diff, d'un resume, des validations et des reserves pour une PR.

Objectifs :

- tester le flux complet M2 sur un type limite et gateable ;
- eviter l'edition manuelle dispersee ;
- conserver la generation controlee du registre canonique ;
- rendre visibles les arbitrages humains ;
- produire une PR relisible avant toute implementation plus large.

Limites :

- aucun code n'est cree par ce document ;
- aucun formulaire ni interface graphique n'est defini ;
- aucune modification des registres, schemas ou validateurs n'est effectuee ;
- aucune personne n'est ajoutee automatiquement ;
- aucune fusion d'identites n'est decidee automatiquement ;
- aucun commit direct sur `main` n'est autorise.

Prototype != implementation generale M2.

Ce prototype est un contrat fonctionnel limite a `PERSON`. Il ne definit pas encore un assistant multi-types, une interface, une automatisation complete ou un nouveau modele de donnees.

## 2. Cas d'usage

Scenario cible :

L'utilisateur souhaite ajouter une nouvelle personne au corpus.

Donnees connues possibles :

- nom canonique de la personne ;
- categorie documentaire ;
- role ou roles observes ;
- source documentaire `Sxx` ;
- alias ou variantes de nom ;
- rattachement eventuel a un ou plusieurs `PERS-*` provisoires ;
- note de prudence ou d'arbitrage.

Donnees inconnues possibles :

- existence d'un `PERSON-` deja cree sous un autre slug ;
- presence de la personne comme alias d'une entree existante ;
- presence d'un `PERS-*` provisoire deja rattache ;
- categorie primaire exacte ;
- besoin de `categorie_a_arbitrer` ;
- incertitude d'identite justifiant `a_arbitrer` ;
- source suffisante ou source seulement indirecte.

Resultat attendu :

- une proposition d'identifiant `PERSON-<slug>` ;
- une entree candidate respectant le schema canonique ;
- une classification des constats en `bloquant`, `reserve` ou `information` ;
- la liste des fichiers potentiellement concernes ;
- les commandes de validation a executer ;
- une PR prete a ouvrir selon M2.4 si aucun bloquant n'est present.

## 3. Entrees minimales

Le prototype doit demander seulement les informations necessaires au modele `PERSON` reel.

### Entrees obligatoires

| Entree | Utilisation |
| --- | --- |
| nom | Alimente `name` et sert a proposer le slug de `id`. |
| categorie | Alimente `categorie`, limitee au vocabulaire ferme du schema. |
| role | Alimente `role`, tableau non vide. |
| source(s) | Alimente `sources`, tableau non vide d'identifiants `Sxx`. |

Categories valides :

- `membre`
- `entourage`
- `industrie`
- `critique_journaliste`
- `auteur_secondaire`
- `influence`
- `theoricien_mobilise`

Champs techniques obligatoires a produire dans la proposition :

- `id`, propose par le prototype ;
- `type_unite`, toujours `person` ;
- `name`, issu du nom fourni ;
- `categorie`, issue de l'entree utilisateur ;
- `role`, issu de l'entree utilisateur ;
- `sources`, issu de l'entree utilisateur ;
- `same_as`, tableau vide ou liste de `PERS-*` valides ;
- `alt_names`, tableau vide ou alias fournis ;
- `categorie_a_arbitrer`, booleen explicite ;
- `a_arbitrer`, booleen explicite.

### Entrees facultatives

| Entree | Utilisation |
| --- | --- |
| alias eventuels | Alimente `alt_names` et sert a detecter les collisions. |
| `PERS-*` provisoires | Alimente `same_as` si les identifiants existent et ne sont pas deja rattaches. |
| note | Alimente `note` si une prudence de canonicalisation doit etre visible. |
| origine | Peut valoir `auteur_source` uniquement lorsque le cas correspond au schema. |
| categorie a arbitrer | Alimente `categorie_a_arbitrer` si double appartenance documentaire. |
| identite a arbitrer | Alimente `a_arbitrer` si nom incomplet, homonymie ou rattachement incertain. |

Le prototype ne doit pas inventer de champs supplementaires. Les champs facultatifs ne doivent etre produits que s'ils existent dans le schema ou le modele observe.

## 4. Verifications realisees

Le prototype applique les verifications suivantes avant toute PR.

| Verification | Regle | Classification |
| --- | --- | --- |
| unicite `PERSON-*` | L'identifiant propose n'existe pas deja dans `registers/people/00_canonical_people.md` ni dans les artefacts disponibles. | bloquant si duplication stricte |
| format d'identifiant | `id` respecte `^PERSON-[a-z0-9]+(?:-[a-z0-9]+)*$`. | bloquant si invalide |
| collision de nom | Le nom fourni ne correspond pas manifestement a un `name` existant. | bloquant si meme personne evidente ; reserve si proximite a arbitrer |
| collision alias | Les alias fournis ne sont pas deja portes par `alt_names` d'une autre entree. | bloquant ou reserve selon certitude |
| source `Sxx` connue | Chaque source existe dans `data/registre.json`. | bloquant si source inconnue |
| source suffisante | La source justifie l'existence de la personne, pas seulement une URL ou une provenance technique. | bloquant si absente ; reserve si insuffisance a arbitrer |
| categorie valide | `categorie` appartient au vocabulaire ferme du schema. | bloquant si invalide |
| role non vide | `role` contient au moins un element. | bloquant si absent ou vide |
| `same_as` resolu | Chaque `same_as` pointe vers un `PERS-*` existant et pas vers un `PERSON-`. | bloquant si invalide |
| double rattachement `PERS-*` | Un `PERS-*` propose n'est pas deja rattache a un autre `PERSON-`. | bloquant si deja rattache |
| schema valide | L'entree candidate satisfait `schemas/person_canonical.schema.json`. | bloquant si invalide |
| drift genere | Le registre canonique genere reste coherent avec `tools/build_people_canon.py`. | bloquant si `validate_people.py --check-drift` echoue |
| arbitrage visible | `categorie_a_arbitrer`, `a_arbitrer` et `note` rendent visibles les incertitudes. | reserve si arbitrage documentaire reste ouvert |

Classification M2.2 :

- `bloquant` : la proposition ne doit pas devenir une PR ouverte comme prete a revue ;
- `reserve` : la PR peut etre ouverte seulement si la reserve est visible et soumise a validation humaine ;
- `information` : constat utile sans correction immediate.

Une source inconnue, un identifiant duplique, une categorie invalide, un `same_as` fantome ou un schema invalide ne peuvent jamais etre classes comme simples reserves.

## 5. Generation proposee

Le prototype prepare une proposition. Il ne l'applique pas directement a `main`.

Elements prepares :

- identifiant `PERSON-<slug>` propose a partir du nom ;
- entree canonique candidate au format YAML compatible avec le schema ;
- emplacement de modification propose dans la couche source/provisoire `registers/people/*.md` lorsque le cas dispose d'un `PERS-*` source ;
- regeneration controlee de `registers/people/00_canonical_people.md` uniquement par le pipeline existant si le flux le requiert ;
- diff propose limite a la personne et aux artefacts strictement necessaires ;
- resume documentaire ;
- liste des controles a executer ;
- reserves et arbitrages humains.

Exemple logique d'entree candidate :

```yaml
id: PERSON-exemple-personne
type_unite: person
name: Exemple Personne
categorie: auteur_secondaire
role:
  - auteur
sources:
  - Sxx
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

Ce qui n'est jamais genere automatiquement :

- une fusion d'identites ;
- un rattachement `same_as` sans verification ;
- une source `Sxx` absente ;
- une categorie hors vocabulaire ;
- une note d'arbitrage inventee ;
- une modification manuelle du registre canonique genere ;
- une suppression de `PERS-*`, `PERSON-*`, alias ou relation ;
- une PR mergee ou un commit sur `main`.

## 6. Sortie attendue

Un futur assistant sans interface graphique doit produire :

- une branche dediee ;
- une modification proposee limitee a l'ajout `PERSON` ;
- l'entree candidate ;
- le diff lisible ;
- le resultat de `python3 tools/validate_people.py` ;
- le resultat de `python3 tools/validate_people.py --check-drift` si le registre canonique genere est affecte ;
- le resultat de `python3 tools/check_generated_sync.py` si des artefacts generes sont affectes ;
- les reserves et arbitrages humains restants ;
- un resume de PR conforme a M2.4 ;
- une PR prete a ouvrir si aucun bloquant n'est present.

La sortie doit permettre a un humain de repondre rapidement :

- quelle personne est proposee ?
- quelle source la justifie ?
- quel identifiant est propose ?
- quels champs sont renseignes ?
- quels doublons ont ete recherches ?
- quels controles ont ete executes ?
- quelles reserves restent ouvertes ?

## 7. Cas de refus

Le prototype doit refuser ou classer comme non pre-validee toute proposition dans les cas suivants :

- `PERSON` deja existante ;
- identifiant `PERSON-*` deja utilise ;
- collision forte de nom ou d'alias ;
- source absente ;
- source `Sxx` inconnue dans `data/registre.json` ;
- source insuffisante pour etablir l'existence de la personne ;
- categorie invalide ;
- role absent ou vide ;
- `same_as` pointant vers un `PERSON-*` ;
- `same_as` pointant vers un `PERS-*` inexistant ;
- `PERS-*` deja rattache a un autre `PERSON-` ;
- schema invalide ;
- ajout qui contourne la generation controlee de `00_canonical_people.md` ;
- demande de fusion automatique ;
- demande de suppression automatique ;
- demande de commit direct sur `main`.

Un cas doit aussi etre refuse ou reclasse hors prototype si la demande implique une integration documentaire longue, la creation d'une source canonique, une refonte du generateur ou une interface.

## 8. Articulation avec M2

### Lien avec M2.1

Le prototype applique le contrat d'ajout unitaire :

- un seul objet principal ;
- type `PERSON` ;
- source documentaire avant enrichissement ;
- champs minimaux issus du schema reel ;
- diff limite ;
- controle avant PR.

Il ne traite pas les integrations longues, les ajouts massifs ou les arbitrages historiographiques complexes.

### Lien avec M2.2

Le prototype applique la pre-validation commune :

- unicite d'identifiant ;
- source connue ;
- schema compatible ;
- relations `same_as` resolues ;
- absence de collision documentaire ;
- artefacts generes synchronises ;
- classification en `bloquant`, `reserve` ou `information`.

Le prototype ne transforme pas la pre-validation en validation historiographique.

### Lien avec M2.4

Le prototype prepare une PR conforme a M2.4 :

- branche dediee ;
- objet clairement identifie ;
- diff limite ;
- resume documentaire ;
- validations listees ;
- reserves explicites ;
- demande `@codex review` ;
- validation humaine conservee.

Le prototype ne merge pas, ne corrige pas silencieusement et ne decide pas a la place de la revue humaine.

## 9. Criteres de succes

Le prototype peut etre considere comme reussi si :

- l'utilisateur n'a pas besoin d'editer manuellement le registre canonique genere ;
- aucun identifiant `PERSON-*` duplique n'est propose ;
- aucune source inconnue n'est acceptee ;
- aucune categorie hors vocabulaire n'est acceptee ;
- les collisions de nom et d'alias sont visibles ;
- les `same_as` proposes sont resolus ou refuses ;
- `python3 tools/validate_people.py` passe apres generation controlee ;
- `python3 tools/validate_people.py --check-drift` passe lorsque le registre canonique est affecte ;
- les artefacts generes requis sont synchronises ;
- la PR est courte, relisible et limitee a la personne ajoutee ;
- les reserves sont documentees ;
- la validation humaine reste obligatoire.

Un prototype reussi ne prouve pas que tout M2 est implementable. Il prouve seulement que le flux `PERSON` est un bon support pour tester l'ajout unitaire controle.

## 10. Decision proposee

Ce prototype est un bon premier candidat pour l'implementation M2.

Raisons :

- `PERSON` dispose d'un schema canonique executable ;
- `PERSON` dispose d'un validateur gateable ;
- le vocabulaire de categorie est ferme ;
- les sources `Sxx` sont verifiables contre `data/registre.json` ;
- les collisions de nom, alias et `same_as` sont controlables ;
- la generation du registre canonique possede une sentinelle anti-drift ;
- le flux reste suffisamment limite pour tester M2.1, M2.2 et M2.4 sans ouvrir une interface generale.

Decision proposee :

Le premier prototype operationnel M2 doit porter sur l'ajout unitaire `PERSON`, sans interface graphique et sans automatisation generale. Il doit preparer une proposition, executer ou lister les controles existants, produire une PR relisible et maintenir la validation humaine comme decision finale.
