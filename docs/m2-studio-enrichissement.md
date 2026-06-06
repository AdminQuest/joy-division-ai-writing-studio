# M2 - Studio d'enrichissement documentaire

## 1. Pourquoi M2 existe

M0 a stabilise le socle du projet. Il a clarifie la doctrine documentaire, l'etat des applications existantes, les registres, les exports, les documents maitres, les dependances de build et les limites a ne pas transformer en chantiers implicites. M0 a aussi fixe une regle structurante : les documents maitres sont des vues persistantes du corpus, pas des sources.

M1 a fiabilise une premiere couche de controle. Les relations `DM -> atomes`, `DM -> registres` et `DM -> sources` sont desormais outillees, rapportees et agregees dans `reports/m1/status_m1.md`. M1 a aussi valide une methode : detecter un ecart, documenter l'audit, corriger de facon ciblee, regenerer les artefacts, puis valider par controle.

L'enrichissement documentaire devient le sujet principal parce que le depot dispose maintenant d'un socle lisible et de garde-fous minimaux. Le risque dominant n'est plus seulement de comprendre l'existant ; il devient d'ajouter correctement de nouveaux objets, de nouvelles sources et de nouvelles relations sans casser les invariants, sans contourner les controles M1 et sans multiplier les editions manuelles dispersees.

M2 doit donc etre defini comme un studio de preparation d'enrichissements documentaires. Il ne remplace pas les registres, les sources, les validateurs, les controles M1 ou la revue humaine. Il organise le passage entre une intention d'ajout et une Pull Request verifiable.

Le present cadrage definit ce que M2 doit etre lorsque la gouvernance l'ouvre operationnellement ; il ne modifie pas a lui seul les verrous de gouvernance existants et ne lance aucune implementation.

## 2. Principes directeurs

Le studio prepare. L'humain valide.

Principes obligatoires :

- aucun contournement des controles ;
- aucune fusion automatique ;
- aucun commit automatique sur `main` ;
- aucun merge automatique ;
- validation humaine obligatoire ;
- aucune correction silencieuse des registres ;
- aucune suppression automatique de donnees ;
- toute proposition d'enrichissement doit rester relisible avant integration ;
- toute sortie du studio doit pouvoir etre controlee par les validateurs et rapports existants.

M2 peut aider a creer une branche, proposer des identifiants, preparer des fichiers, lancer des controles et ouvrir une PR. M2 ne doit pas transformer une proposition en verite documentaire. La decision finale reste humaine, en particulier pour les arbitrages historiographiques, les droits, la provenance, les libelles canoniques, les alias et les relations.

## 3. Les deux cas d'usage principaux

### Cas A - Ajout unitaire

Exemples : personne, lieu, organisation, concert, image, citation, release.

Question : comment ajouter rapidement un objet unique sans editer manuellement plusieurs fichiers ?

Besoins :

- identifier le type d'objet a ajouter ;
- proposer un identifiant canonique conforme aux conventions ;
- renseigner les champs requis du registre cible ;
- distinguer source documentaire, provenance technique, URL de consultation et droits ;
- verifier les doublons probables ;
- verifier les relations minimales vers les objets deja existants ;
- produire une proposition lisible avant commit.

Flux attendu :

```text
demande d'ajout unitaire
↓
qualification du type d'objet
↓
collecte des champs requis
↓
proposition d'identifiant
↓
pre-validation locale
↓
generation d'un patch ou d'une branche
↓
execution des validateurs pertinents
↓
preparation d'une PR
↓
validation humaine
```

Validations attendues :

- schema du registre concerne ;
- unicite de l'identifiant propose ;
- absence de collision avec les alias et `same_as` connus ;
- presence d'une source documentaire lorsque le type d'objet l'exige ;
- separation correcte entre provenance, droits, consultation et sources ;
- absence d'identifiant interne inadapte dans un champ `sources`.

Resultat attendu :

- une PR courte, lisible, limitee a l'objet ajoute et aux artefacts generes necessaires ;
- un resume indiquant l'objet cree, les fichiers modifies, les validations passees et les points restant a arbitrer ;
- aucune modification directe de `main`.

### Cas B - Integration documentaire

Exemples : livre, article, interview, fanzine, archive.

Question : comment integrer une nouvelle source importante dans le corpus ?

Besoins :

- creer ou completer la source canonique dans `data/registre.json` selon les conventions existantes ;
- preparer un dossier source sans confondre fichier de travail, source canonique et registre ;
- proposer des atomes derives de la source ;
- proposer des citations exactes lorsque le droit et le perimetre le permettent ;
- proposer des relations vers personnes, lieux, chansons, concerts, sessions, concepts ou autres objets existants ;
- enrichir les registres uniquement lorsque la source le justifie ;
- preparer une PR relisible avec preuves, limites et controles.

Flux attendu :

```text
source documentaire candidate
↓
qualification bibliographique et documentaire
↓
creation ou mise a jour de la source canonique
↓
preparation du dossier source
↓
proposition d'atomes
↓
proposition de citations et relations
↓
enrichissement cible des registres
↓
regeneration des exports necessaires
↓
execution des controles et validateurs
↓
preparation d'une PR
↓
validation humaine
```

Validations attendues :

- coherence de l'identifiant source `Sxx` ou `Sxxx` ;
- presence de la source dans le registre canonique ;
- absence de source inconnue dans les documents ou propositions ;
- conformite des atomes proposes au schema courant ;
- coherence des liens vers registres existants ;
- verification des droits et restrictions de citation ;
- detection des doublons avec des sources, atomes ou citations deja presents ;
- controle M1 lorsque les documents maitres ou rapports sont affectes.

Resultat attendu :

- une PR documentaire structuree ;
- une source canonique identifiable ;
- un dossier source exploitable ;
- des atomes et relations proposes, pas imposes ;
- des enrichissements de registres explicites ;
- une liste des arbitrages humains restants.

## 4. Pipeline commun

Les deux flux convergent vers un meme pipeline de gouvernance.

```text
entree
↓
preparation
↓
validation
↓
controles
↓
PR
↓
validation humaine
```

Etapes communes :

| Etape | Role |
| --- | --- |
| Entree | Recevoir une intention d'ajout : objet unique ou source documentaire. |
| Qualification | Determiner le type d'objet, le registre cible, les dependances et les risques. |
| Preparation | Generer une proposition structuree : champs, identifiants, fichiers, relations. |
| Pre-validation | Executer les validations locales disponibles sans modifier `main`. |
| Controles | Lancer les controles pertinents : validateurs de registres, build, controles M1 si necessaire. |
| PR | Ouvrir une Pull Request avec un diff limite, un resume et les resultats de verification. |
| Validation humaine | Relire, demander correction, approuver ou refuser. |

Le pipeline commun doit produire des propositions auditables. Il ne doit jamais masquer l'origine d'une modification ni disperser un ajout dans plusieurs fichiers sans explication.

## 5. Ce que M2 ne doit pas faire

M2 ne doit pas :

- merger automatiquement ;
- publier automatiquement ;
- reecrire automatiquement le corpus ;
- modifier silencieusement les registres ;
- supprimer automatiquement des donnees ;
- contourner les controles M1 ;
- traiter un document maitre comme source ;
- traiter une sortie RAG comme preuve autonome ;
- creer des exceptions de schema pour faciliter un ajout ponctuel ;
- remplir automatiquement les droits ou la provenance sans preuve ;
- inventer une source canonique absente ;
- ecraser des alias, `same_as` ou relations existantes sans audit ;
- transformer une suggestion historiographique en fait canonique ;
- ouvrir M3, M4, M5 ou une refonte d'interface ;
- fusionner les repos ;
- corriger manuellement des artefacts generes hors workflow explicite.

## 6. Architecture cible

Cette section decrit des composants possibles. Elle ne decide pas encore de leur implementation.

| Composant possible | Role | Perimetre | Dependances |
| --- | --- | --- | --- |
| Assistant d'ajout | Accompagner l'ajout d'un objet unique. | Personnes, lieux, organisations, concerts, images, citations, releases. | Conventions d'identifiants, schemas, validateurs du registre cible. |
| Assistant d'integration | Accompagner l'integration d'une source importante. | Livres, articles, interviews, fanzines, archives. | `data/registre.json`, dossiers `sources/`, schemas d'atomes, controles M1. |
| Generateur d'identifiants | Proposer un identifiant disponible et conforme. | Identifiants canoniques et identifiants derives. | Registres existants, exports, conventions de nommage, alias, `same_as`. |
| Pre-validateur | Verifier une proposition avant commit. | Schema, doublons, champs requis, droits, provenance, sources. | Validateurs existants, build, controles de synchronisation. |
| Preparateur de PR | Transformer une proposition validee localement en branche et PR relisibles. | Branche, commit, corps de PR, resultats de controles. | Git, GitHub, politique de PR, contraintes `GITHUB_TOKEN`. |
| Rapporteur d'arbitrages | Lister ce que l'automatisation ne peut pas decider. | Ambiguites de libelles, alias, droits, relations, interpretation historiographique. | Audits, rapports M1, revue humaine. |

La cible doit rester modulaire. Un assistant d'ajout unitaire ne doit pas embarquer toute la logique d'integration d'une source longue. Un assistant d'integration ne doit pas contourner les validateurs des objets unitaires qu'il propose de creer.

## 7. Priorisation

### M2.1 - Contrat d'ajout unitaire

Valeur : tres forte.

Raison : les ajouts courants sont le cas le plus frequent et le plus facile a securiser. Ils reduisent l'edition manuelle des JSON ou Markdown de registres sans introduire d'interpretation historiographique lourde.

Livrable futur attendu : specification operationnelle du flux d'ajout unitaire, champs requis par type, validations minimales, format de proposition et regles de PR.

### M2.2 - Pre-validation commune

Valeur : tres forte.

Raison : les deux cas d'usage ont besoin d'une couche commune qui detecte collisions, champs manquants, erreurs de schema, sources absentes et separations provenance/droits avant qu'une PR soit ouverte.

Livrable futur attendu : specification de la pre-validation, sans encore imposer une interface.

### M2.3 - Integration documentaire source longue

Valeur : forte.

Raison : l'integration d'un livre, article, entretien, fanzine ou archive apporte beaucoup de valeur au corpus, mais elle porte davantage de risques : atomisation, citations, relations, droits et arbitrages historiographiques.

Livrable futur attendu : cadrage du flux source -> dossier -> atomes -> relations -> registres -> PR.

### M2.4 - Preparation de PR assistee

Valeur : forte.

Raison : une PR bien preparee rend la validation humaine plus fiable. Cette etape peut rester commune aux ajouts unitaires et aux integrations documentaires.

Livrable futur attendu : modele de corps de PR, liste des controles a joindre, politique de commit et limites de l'automatisation.

### M2.5 - Interfaces ou formulaires

Valeur : moyenne a terme, faible immediatement.

Raison : une interface peut ameliorer l'ergonomie, mais elle risque d'encoder trop tot des regles encore instables. Les formulaires doivent venir apres stabilisation des contrats d'ajout et de pre-validation.

Livrable futur attendu : seulement apres M2.1 et M2.2, specification d'interface si le besoin reste confirme.

Premier chantier recommande : M2.1, contrat d'ajout unitaire, suivi de M2.2, pre-validation commune.

## 8. Risques

### Risques techniques

- generer des identifiants en collision avec des objets existants ;
- modifier trop de fichiers pour un ajout simple ;
- produire une PR dont les artefacts generes ne sont pas synchronises ;
- dependre d'un workflow GitHub qui ne declenche pas les checks attendus ;
- rendre l'outil difficile a maintenir en melangeant ajout unitaire et integration longue.

### Risques documentaires

- confondre source documentaire, URL de consultation, provenance technique et droits ;
- introduire un objet sans source suffisante ;
- creer des doublons au lieu d'utiliser `same_as` ou alias ;
- enrichir un registre sans regenerer les exports necessaires ;
- laisser une proposition d'atome ou relation sans statut clair.

### Risques historiographiques

- transformer une interpretation en fait canonique ;
- attribuer une relation causale trop forte a partir d'une source unique ;
- atomiser une source sans conserver ses limites, son statut et son contexte ;
- survaloriser une citation ou un temoignage sans arbitrage humain ;
- masquer les incertitudes derriere une interface trop affirmative.

### Risques de gouvernance

- contourner les controles M1 parce que l'ajout semble simple ;
- merger sans revue humaine ;
- creer un outil qui pousse directement vers `main` ;
- ouvrir en pratique M3, M4 ou M5 sous couvert de M2 ;
- laisser l'automatisation prendre des decisions documentaires qui doivent rester humaines.

## 9. Décision proposée

Definition operationnelle de M2 :

M2 est le studio de preparation des enrichissements documentaires. Il transforme une intention d'ajout en proposition controlee, relisible et prete pour PR. Il couvre deux flux principaux : ajout unitaire d'objet canonique et integration documentaire d'une source importante. Il peut assister la generation d'identifiants, la preparation de fichiers, la pre-validation, l'execution de controles et la preparation de PR. Il ne valide pas historiographiquement, ne merge pas, ne publie pas, ne modifie pas silencieusement le corpus et ne contourne aucun controle.

Ordre de priorite propose :

| Priorite | Chantier |
| --- | --- |
| M2.1 | Contrat d'ajout unitaire. |
| M2.2 | Pre-validation commune. |
| M2.3 | Integration documentaire source longue. |
| M2.4 | Preparation de PR assistee. |
| M2.5 | Interfaces ou formulaires, seulement apres stabilisation des contrats. |

Premier chantier recommande :

M2.1 - definir le contrat d'ajout unitaire pour les objets courants, sans interface et sans implementation automatique. Ce chantier apporte la plus forte valeur immediate parce qu'il reduit l'edition manuelle dispersee tout en restant suffisamment limite pour respecter les controles M1 et la validation humaine.
