# M2.4 - Preparation de PR assistee

## 1. Objet de la preparation de PR

La preparation de PR est le contrat de sortie du Studio M2. Elle transforme une proposition d'enrichissement pre-validee en Pull Request relisible, bornee et verifiable.

Elle a pour role :

- d'isoler la proposition sur une branche dediee ;
- de rendre l'objet de la PR immediatement comprehensible ;
- de limiter le diff a l'objet documentaire traite et aux artefacts strictement necessaires ;
- de joindre les resultats de validations disponibles ;
- de rendre visibles les reserves et arbitrages humains restants.

Elle se place apres la preparation de l'enrichissement, la pre-validation commune et l'execution des controles pertinents. Elle prepare une decision de revue. Elle ne decide pas :

- qu'un ajout est historiographiquement valide ;
- qu'une source est suffisante au fond ;
- qu'une reserve peut etre ignoree ;
- qu'une correction peut etre appliquee silencieusement ;
- qu'une PR peut etre mergee.

Preparation de PR != validation humaine.

La preparation de PR produit une proposition exploitable par la revue. La validation finale reste humaine.

## 2. Position dans le pipeline M2

```text
entree
  |
  v
preparation
  |
  v
pre-validation
  |
  v
controles
  |
  v
preparation de PR
  |
  v
PR
  |
  v
validation humaine
```

| Etape | Role |
| --- | --- |
| Entree | Recevoir l'intention d'enrichissement : objet unique, correction, audit, documentation ou integration documentaire future. |
| Preparation | Identifier les fichiers concernes, les sources, les relations, les artefacts generes possibles et les limites du changement. |
| Pre-validation | Classer les constats en `bloquant`, `reserve` ou `information` selon le contrat M2.2. |
| Controles | Executer les validateurs, build, sentinelles de synchronisation et controles M1 pertinents, sans creer de nouveau controle. |
| Preparation de PR | Rediger une PR relisible : branche, objet, diff limite, resume, validations, reserves et demande de revue. |
| PR | Ouvrir la Pull Request sur GitHub, sans merge automatique et sans commit direct sur `main`. |
| Validation humaine | Examiner le fond documentaire, traiter les remarques, arbitrer les reserves et decider du merge ou du refus. |

Une PR ne doit pas etre ouverte avec un bloquant connu. Si une reserve demeure, elle doit etre explicite dans le corps de PR et rattachee a une decision humaine attendue.

## 3. Contenu minimal d'une PR

Une PR produite par le Studio M2 doit contenir les elements suivants.

### Branche dediee

La branche doit etre specifique au changement et ne pas melanger plusieurs chantiers.

Exemples de prefixes acceptables :

- `feat/...` pour un enrichissement fonctionnel ou documentaire outille ;
- `fix/...` pour une correction ciblee ;
- `docs/...` pour un cadrage, une decision ou une documentation ;
- `audit/...` pour un audit ou une correction issue d'audit.

Une branche dediee ne doit pas contenir de modifications sans lien avec l'objet annonce.

### Objet clairement identifie

La PR doit repondre a la question :

Quel enrichissement est propose ?

L'objet doit nommer le type de changement et le perimetre documentaire : objet ajoute, source traitee, registre affecte, correction appliquee ou document cree.

### Diff limite

La PR doit repondre a la question :

Le diff est-il limite a son objet ?

Le diff attendu comprend seulement :

- les fichiers sources strictement necessaires ;
- les artefacts generes lorsque le pipeline les produit et que leur synchronisation est requise ;
- les documents d'audit ou de cadrage lorsque l'objet de la PR les exige.

Les refontes opportunistes, corrections voisines, nettoyages de style non lies et modifications de schema non prevues sont hors perimetre.

### Resume documentaire

La PR doit repondre a la question :

Pourquoi cet ajout existe-t-il ?

Le resume doit indiquer :

- l'intention documentaire ;
- la source ou le contexte qui justifie le changement ;
- les fichiers modifies ;
- la limite explicite de ce qui n'est pas traite.

### Resultat des validations

La PR doit repondre a la question :

Quels controles ont ete executes ?

Le corps de PR doit lister les commandes lancees et leur resultat. Si un controle n'est pas applicable, cela doit etre dit explicitement. Si un validateur dedie n'existe pas, l'absence de validateur ne doit pas etre presentee comme une validation.

### Reserves

La PR doit repondre a la question :

Quels points restent soumis a arbitrage ?

Les reserves doivent etre visibles et classees. Une reserve ne peut pas masquer :

- une source inconnue ;
- un identifiant deja utilise ;
- un schema invalide ;
- un artefact genere obsolete ;
- une relation obligatoire introuvable ;
- une remarque de revue non traitee.

### Modele minimal de corps de PR

```markdown
## Objet

<Quel enrichissement est propose ?>

## Perimetre

- Fichiers modifies :
- Type de PR :
- Hors perimetre :

## Resume documentaire

<Pourquoi cet ajout existe-t-il ?>

## Validations

- [ ] `<commande>` : resultat
- [ ] `<commande>` : non applicable, raison

## Reserves et arbitrages

- Reserve :
- Arbitrage humain attendu :

## Revue

- @codex review demande
- Remarques traitees dans le fil GitHub
```

## 4. Classification des PR

| Categorie | Objectif | Perimetre | Taille attendue |
| --- | --- | --- | --- |
| ajout unitaire | Ajouter un objet unique acceptable selon M2.1. | Un objet principal, ses relations minimales, ses artefacts generes strictement requis et le resume de validations. | Petite ; diff court et centre sur un type d'objet. |
| integration documentaire | Integrer une source importante dans le corpus. | Creation ou mise a jour de source canonique, dossier source, propositions d'atomes, relations et enrichissements. | Moyenne a grande ; doit etre decoupee si plusieurs decisions independantes sont melangees. |
| correction | Corriger un ecart identifie par audit, validation, revue ou usage. | Ecart cible, cause documentee, correction minimale, artefacts regeneres si necessaire. | Petite a moyenne ; aucune refonte opportuniste. |
| audit | Documenter un diagnostic ou une verification. | Rapport, constat, methode, limites, recommandations et eventuelles corrections separees si le diff devient mixte. | Petite a moyenne ; lisible sans reconstruire tout l'historique. |
| documentation | Cadrer une doctrine, un contrat, une decision ou un usage. | Document concerne uniquement et references au depot reel. | Petite ; aucun script, schema, registre ou export sauf demande explicite du chantier. |

Une PR qui combine plusieurs categories doit expliquer pourquoi la combinaison est necessaire. Si elle masque plusieurs decisions independantes, elle doit etre decoupee.

## 5. Controles obligatoires avant ouverture

Les controles a executer dependent du perimetre reel de la PR. M2.4 ne cree aucun controle nouveau.

### Validateurs de registres et objets

Commandes existantes utilisables selon les fichiers modifies :

- `python3 tools/validate_people.py`
- `python3 tools/validate_places.py`
- `python3 tools/validate_orgs.py`
- `python3 tools/validate_images.py`
- `python3 tools/validate_concerts.py`
- `python3 tools/validate_quotes.py`
- `python3 tools/validate_songs.py`, seulement pour les chansons canoniques lorsque le perimetre les concerne.

Note sur `RELEASE` : dans l'etat documente par M2.1, il n'existe pas de validateur gateable dedie aux occurrences discographiques de `schemas/song_occurrence.schema.yaml`. `tools/validate_songs.py` ne doit pas etre presente comme preuve de validation d'une occurrence `RELEASE`.

### Build et synchronisation

Commandes existantes utilisables selon le perimetre :

- `python3 tools/build_all.py`
- `python3 tools/check_generated_sync.py`
- `python3 tools/generate_status.py`, lorsque les documents de pilotage ou artefacts qui alimentent `STATUS.md` sont modifies.

Si le pipeline regenere des artefacts attendus, ils doivent etre relus et committes avec la PR lorsque les controles de synchronisation l'exigent. Une PR ne doit pas laisser un drift genere connu sans l'exposer.

### Controles M1 eventuels

Les controles M1 sont requis lorsque la PR affecte les documents maitres, les rapports M1, le status M1 consolide ou les relations documentaires couvertes par M1.

Commandes existantes :

- `python3 tools/check_dm_atoms_traceability.py`
- `python3 tools/check_dm_registers_consistency.py`
- `python3 tools/check_dm_sources_consistency.py`
- `python3 tools/aggregate_m1.py`
- `python3 -m unittest tools.test_aggregate_m1`, lorsque l'agregateur M1 ou son comportement est concerne.

Ces controles restent ceux de M1. La preparation de PR ne modifie ni leurs seuils, ni leurs rapports, ni leur agregateur.

### Regle de declaration

Le corps de PR doit distinguer :

- controles executes avec succes ;
- controles executes en echec et corrections apportees ;
- controles non applicables, avec justification ;
- controles existants non executes, avec raison explicite.

Un controle non execute sans justification est une reserve de revue. Un controle obligatoire echoue est un bloquant.

## 6. Revue obligatoire

Le workflow de revue adopte par le projet est le suivant :

```text
ouverture de PR
  |
  v
@codex review
  |
  v
traitement des remarques
  |
  v
reponses dans le fil GitHub
  |
  v
nouveau @codex review
```

Toute remarque Codex doit etre traitee explicitement :

- par une correction commitee ;
- par une reponse documentee expliquant pourquoi aucune modification n'est retenue ;
- par un reclassement clair en hors perimetre si la remarque depasse l'objet de la PR.

Aucune remarque ne doit etre ignoree. Une correction silencieuse n'est pas acceptable : le fil GitHub doit permettre de comprendre ce qui a ete change ou pourquoi la remarque n'a pas entraine de changement.

Apres chaque serie de corrections, un nouveau `@codex review` doit etre demande. La PR ne peut etre consideree prete a decision humaine que lorsque les remarques actionnables ont ete traitees ou explicitement arbitrees.

## 7. Decisions interdites

La preparation de PR assistee ne doit jamais effectuer ou supposer les decisions suivantes :

- merge automatique ;
- commit sur `main` ;
- validation historiographique automatique ;
- correction silencieuse ;
- suppression automatique ;
- contournement des controles M1 ;
- modification implicite des schemas ;
- creation d'un nouveau registre hors chantier explicite ;
- requalification d'un bloquant en reserve pour faciliter l'ouverture d'une PR ;
- presentation d'une absence de validateur comme une preuve de conformite ;
- declenchement d'un workflow GitHub dont les limites ne sont pas documentees.

Les contraintes d'automatisation de la roadmap restent applicables : une automatisation peut preparer une branche, lancer des controles et ouvrir une PR, mais elle ne doit pas merger, contourner la validation humaine ou supposer que `GITHUB_TOKEN` declenche tous les workflows attendus.

## 8. Sortie attendue

Un futur assistant M2 de preparation de PR doit produire au minimum :

- une branche dediee ;
- la liste des fichiers modifies ;
- le type de PR retenu ;
- un resume documentaire ;
- le resultat des validations executees ;
- les validations non applicables ou non executees, avec justification ;
- les reserves et arbitrages humains restants ;
- une Pull Request ouverte sans merge automatique ;
- une demande `@codex review` ;
- les reponses aux remarques dans le fil GitHub.

La sortie attendue doit permettre a un humain de repondre rapidement :

- quel changement est propose ?
- pourquoi existe-t-il ?
- quels fichiers changent ?
- quels controles ont ete passes ?
- quelles reserves restent a trancher ?
- quelles remarques de revue ont ete traitees ?

## 9. Risques

### Risques techniques

- ouvrir une PR avec un drift d'artefacts generes ;
- oublier un validateur pertinent ;
- dependre d'un workflow GitHub qui ne declenche pas les checks attendus ;
- melanger plusieurs chantiers dans une branche ;
- produire un corps de PR incomplet ou non reproductible.

### Risques documentaires

- masquer l'origine exacte d'un ajout ;
- confondre source documentaire, provenance technique et droits ;
- presenter une reserve comme une validation ;
- creer une correction locale qui affaiblit un invariant documentaire ;
- ouvrir une PR dont le diff ne permet pas de comprendre la decision attendue.

### Risques de gouvernance

- contourner la revue humaine sous couvert d'assistance ;
- ignorer une remarque Codex ;
- merger une PR avant traitement des reserves ;
- transformer M2.4 en automatisation avant d'avoir stabilise son contrat ;
- utiliser la preparation de PR pour ouvrir indirectement un chantier hors perimetre.

## 10. Decision proposee

La version minimale de la preparation de PR assistee est definie comme un contrat de sortie commun au Studio M2.

Une PR acceptable produite par M2 est une Pull Request ouverte depuis une branche dediee, limitee a son objet, accompagnee d'un resume documentaire, de la liste des fichiers modifies, des validations executees, des controles non applicables justifies, des reserves restantes et d'une demande de revue Codex.

Cette version minimale est suffisante avant toute automatisation si elle respecte les limites suivantes :

- aucun nouveau script ;
- aucun workflow GitHub ;
- aucun controle M1 modifie ;
- aucun schema ou export modifie par le contrat lui-meme ;
- aucune validation historiographique automatique ;
- aucun merge automatique.

La preparation de PR assistee prepare la revue. Elle ne remplace pas la validation humaine.
