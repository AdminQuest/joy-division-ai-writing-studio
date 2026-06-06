# M2.7 - Bilan de genericite M2

## 1. Objet du bilan

Ce document etablit le premier bilan d'architecture de M2 a partir des deux prototypes effectivement implementes et evalues : `PERSON` et `ORG`.

Il existe pour repondre a deux questions :

- qu'est-ce qui est reellement commun aux prototypes M2 deja observes ?
- qu'est-ce qui doit rester specifique a chaque famille documentaire ?

Il intervient apres `PERSON` et `ORG` parce que le projet dispose maintenant de deux cas concrets, avec specifications, scripts, tests, documentation CLI et retours d'usage. Avant `ORG`, toute conclusion de genericite aurait repose sur un seul type documentaire. Apres `ORG`, il devient possible de distinguer un invariant M2 d'une habitude propre a `PERSON`.

Il precede toute nouvelle famille documentaire parce qu'une extension immediate vers `PLACE`, `IMAGE`, `CONCERT`, `RELEASE` ou `CITATION` risquerait de reproduire soit une duplication inutile, soit une abstraction prematuree. Le bilan doit donc clarifier les points communs, les limites et la prochaine decision d'architecture.

Ce document ne cree aucun code, aucun prototype, aucun registre, aucun schema et aucun validateur.

## 2. Comparaison PERSON / ORG

| Sujet | PERSON | ORG | Convergence | Divergence |
| --- | --- | --- | --- | --- |
| Identifiant | `PERSON-<slug>` derive du nom, par exemple `PERSON-martin-hannett`. | `ORG-NNNN` numerique, prochain numero calcule depuis `registers/orgs/orgs.json`. | Chaque prototype propose un identifiant et bloque la duplication stricte. | Le calcul est semantique pour `PERSON`, numerique pour `ORG`. |
| Format de donnees | Entree candidate YAML compatible avec `schemas/person_canonical.schema.json`. | Entree candidate JSON compatible avec `schemas/organization_canonical.schema.json`. | Les deux produisent une entree candidate structuree et relisible. | Les champs, la serialisation et la couche de stockage sont differentes. |
| Sources | `sources` liste non vide de `Sxx`; verification contre `data/registre.json`. | `sources` liste non vide de `Sxx`; verification contre `data/registre.json` avec controle de format `Sxx`. | Source canonique obligatoire et source inconnue bloquante. | ORG verifie explicitement le format `Sxx`; PERSON controle surtout l'existence canonique. |
| Collisions | Identifiant, nom, alias, `same_as` vers `PERS-*`, auteurs-sources. | Identifiant propose, nom canonique, alias, Wikidata duplique. | Collision certaine = `bloquant`; proximite nom/alias = `reserve`. | Les indices de collision dependent du modele : `PERS-*` pour PERSON, Wikidata et alias ORG pour ORG. |
| Relations | `same_as` rattache des `PERS-*`; `origin=auteur_source` impose `same_as` vide; cible d'ecriture a confirmer. | `joy_division_relation.type` non vide; `same_as` porte des identifiants externes; provenance possible. | Les relations obligatoires ou structurantes sont verifiees avant pre-validation. | PERSON traite une relation de canonicalisation interne; ORG traite une relation documentaire avec Joy Division et des identifiants externes. |
| Validateurs | Schema PERSON via `tools/schema_validation.py`; validation canonique attendue avec `tools/validate_people.py`. | Schema JSON ORG via `jsonschema`; validation canonique attendue avec `tools/validate_orgs.py`. | Chaque prototype s'aligne sur un schema et un validateur existants. | Les validateurs, chemins et formats d'erreur ne sont pas communs. |
| Gouvernance | Lecture seule, pas de registre modifie, pas de PR ouverte automatiquement, validation humaine. | Lecture seule, pas de registre modifie, pas de PR ouverte automatiquement, validation humaine. | Principe M2 identique : le prototype prepare, l'humain valide. | PERSON a une cible d'ecriture parfois incertaine; ORG cible directement `registers/orgs/orgs.json` comme registre probable. |
| Sortie CLI | `Decision`, identifiant propose, bloquants, reserves, informations, entree candidate YAML. | `Decision`, identifiant propose, bloquants, reserves, informations, entree candidate JSON. | Structure de sortie commune et deterministe. | Le bloc candidat et les informations de cible different. |
| Tests | 11 tests : conforme, source inconnue, categorie invalide, collision, auteur-source, cible d'ecriture, reserves, alias, aide, determinisme. | 10 tests : conforme, source inconnue, categorie invalide, pays invalide, collision, Wikidata, reserve alias, relation vide, aide, determinisme. | Les tests couvrent pre-validation, reserve, aide et determinisme. | Les cas specifiques suivent les risques de chaque famille. |
| Reserves | `identity_arbitration`, `categorie_a_arbitrer`, alias proche, nom proche. | Organisation proche, alias proche. | Une ambiguite documentee peut produire `pre-validee avec reserve`. | Les reserves PERSON portent aussi sur l'identite et la categorie; ORG ne reserve pas encore une relation vague non vide. |
| Champs metier | `categorie`, `role`, `same_as`, `alt_names`, `a_arbitrer`, `categorie_a_arbitrer`, `origine`. | `category`, `country`, `status`, `gate`, `joy_division_relation`, `same_as`, `identity_frozen`, `drift_sentinel`, `last_verified`. | Les champs obligatoires sont derives du schema reel. | Aucun noyau de champs metier commun n'est suffisant pour generer les deux objets sans adaptateur. |

Convergences principales :

- lecture seule ;
- preparation d'une entree candidate ;
- source canonique obligatoire ;
- schema ou validateur comme reference ;
- collision stricte bloquante ;
- ambiguite explicite en reserve ;
- sortie deterministe ;
- validation humaine conservee.

Divergences principales :

- format et strategie d'identifiant ;
- structure de registre ;
- nature des relations ;
- vocabulaire metier ;
- cible d'ecriture ;
- validateur et schema ;
- types de reserves utiles.

## 3. Invariants communs M2

Les invariants ci-dessous sont reellement observes dans `tools/m2_add_person.py`, `tools/m2_add_org.py`, leurs tests et leurs retours d'usage.

| Invariant | Observation |
| --- | --- |
| Lecture seule | Les prototypes lisent le depot et impriment une proposition. Ils ne modifient aucun registre, schema, export ou validateur. |
| Source obligatoire | Une proposition sans source ou avec source inconnue ne doit pas etre pre-validee. Les sources sont controlees contre `data/registre.json`. |
| Pre-validation avant PR | Les prototypes classent la proposition avant toute ouverture de PR. |
| `bloquant` | Un ecart formel fort rend la proposition `non pre-validee`. |
| `reserve` | Une ambiguite acceptable seulement avec arbitrage humain rend la proposition `pre-validee avec reserve`. |
| `information` | Les informations utiles n'empechent pas la pre-validation. |
| Collision stricte bloquante | Identifiant deja utilise, nom manifeste ou relation interdite bloquent la proposition. |
| Ambiguite visible | Nom proche, alias proche ou identite a arbitrer ne sont pas acceptes silencieusement. |
| Schema compatible | L'entree candidate doit rester compatible avec le schema ou le validateur du type. |
| Aide CLI | Le `--help` expose les vocabulaires utiles au moins pour les categories, et pour ORG aussi les statuts et gates. |
| Sortie deterministe | Les tests verifient que deux evaluations identiques produisent la meme sortie. |
| Validation humaine | Aucun prototype ne tranche une interpretation historiographique, ne merge, ne commit sur `main` ou ne corrige silencieusement. |
| Exit code utile | Les deux CLI retournent un code non nul en presence de bloquants. |

Ces invariants definissent une grammaire commune de M2. Ils ne prouvent pas encore qu'un moteur logiciel commun soit pret.

## 4. Variations specifiques

Certaines variations doivent rester propres a chaque famille documentaire.

| Variation | Pourquoi elle doit rester specifique |
| --- | --- |
| Format d'identifiant | `PERSON-<slug>` encode le nom; `ORG-NNNN` encode une sequence numerique. Les collisions et propositions ne se calculent pas de la meme maniere. |
| Schema | Les champs obligatoires sont differents. PERSON attend `role`, `same_as` liste, `alt_names`; ORG attend `country`, `status`, `gate`, `joy_division_relation`, `same_as` objet. |
| Relations | PERSON canonicalise des identites via `PERS-*`; ORG documente une relation avec Joy Division et des identifiants externes. |
| Vocabulaire metier | Les categories PERSON et ORG n'ont pas le meme sens et ne doivent pas etre confondues. |
| Cible d'ecriture | PERSON peut impliquer `registers/people/*.md` et des artefacts generes; ORG pointe vers `registers/orgs/orgs.json`. |
| Validateur | PERSON s'appuie sur le pipeline people et les artefacts `exports/generated/people.json`; ORG s'appuie sur le validateur ORG JSON. |
| Reserves | PERSON possede `a_arbitrer` et `categorie_a_arbitrer`; ORG reserve surtout les proximites de noms et alias. |
| Identifiants externes | PERSON controle `PERS-*`; ORG controle notamment Wikidata. |
| Champs temporels et statut | ORG expose `last_verified`, `status`, `gate`, `identity_frozen`; PERSON ne suit pas ce contrat. |

La variation n'est pas un defaut. Elle protege le sens documentaire de chaque famille. Un outil commun qui gommerait ces differences produirait des propositions plus homogenes mais moins fiables.

## 5. Risque d'abstraction prematuree

Le projet possede-t-il suffisamment de recul pour creer une couche commune ?

Reponse : pas encore pour une couche commune executable complete.

Le recul est suffisant pour formaliser un contrat commun de sortie, de classification et de tests. Il n'est pas encore suffisant pour creer un moteur unique qui genererait correctement les ajouts `PERSON`, `ORG` et les futures familles.

Avantages possibles d'une couche commune :

- reduire la duplication de `CheckResult`, `decision`, rendu des listes et tri des diagnostics ;
- harmoniser la sortie CLI ;
- partager les controles de source connue et de determinisme ;
- faciliter la preparation de PR assistee ;
- rendre les tests de base plus coherents.

Risques :

- imposer un modele trop pauvre aux familles riches ;
- masquer les differences de schemas ;
- melanger source documentaire, relation, provenance et identifiant externe ;
- transformer des reserves specifiques en messages generiques moins utiles ;
- rendre plus difficile une correction locale sur une famille ;
- creer une dette d'abstraction avant d'avoir observe `PLACE`, `IMAGE` ou `CONCERT`.

Limites du recul actuel :

- seulement deux familles ont ete implementees ;
- les deux sont des identites canoniques proches ;
- aucun prototype n'a encore traite une image, un concert, une citation ou une occurrence discographique ;
- aucune preparation de PR automatisee n'a ete implementee ;
- la question des artefacts generes reste plus sensible pour PERSON que pour ORG.

Conclusion : la bonne genericite actuelle est contractuelle, pas encore technique.

## 6. Scenarios d'evolution possibles

### Option A - un prototype par famille

Benefices :

- respecte fortement les schemas et validateurs de chaque famille ;
- limite le risque d'abstraction prematuree ;
- facilite les corrections ciblees ;
- rend explicite le vocabulaire documentaire propre a chaque type.

Couts :

- duplication de code de rendu, classification et lecture des sources ;
- coherence UX a maintenir manuellement ;
- risque de divergences entre prototypes ;
- multiplication des tests similaires.

Risques :

- accumulation de scripts proches mais pas alignes ;
- dette de maintenance si plusieurs familles deviennent actives ;
- absence de langage commun pour la preparation de PR.

### Option B - moteur commun + adaptateurs par famille

Benefices :

- partage possible des primitives communes : decision, rendu, source connue, schema, collisions simples, determinisme ;
- chaque famille conserve un adaptateur pour identifiant, champs, relations et reserves ;
- trajectoire compatible avec PERSON et ORG sans nier leurs differences ;
- meilleure base pour M2.4 si la preparation de PR devient outillee.

Couts :

- conception prealable necessaire ;
- migration prudente des deux prototypes existants ;
- tests de non-regression a renforcer ;
- risque de creer un contrat interne trop tot si le perimetre est mal borne.

Risques :

- confusion entre invariants M2 et logique specifique ;
- couche commune plus couteuse que deux prototypes simples ;
- tentation d'ajouter une nouvelle famille avant d'avoir stabilise les adaptateurs.

### Option C - assistant documentaire unique

Benefices :

- experience utilisateur unifiee ;
- point d'entree unique pour le Studio M2 ;
- pourrait guider l'utilisateur entre ajout unitaire et integration documentaire ;
- pourrait preparer directement une PR relisible.

Couts :

- complexite elevee ;
- besoin d'une doctrine stabilisee pour toutes les familles ;
- risque d'interface ou de workflow avant stabilisation des invariants ;
- maintenance plus lourde.

Risques :

- masquer les reserves ;
- encourager la fusion automatique de decisions documentaires ;
- transformer M2 en automate de validation, contraire a la doctrine ;
- ouvrir trop vite les familles non encore evaluees.

## 7. Etat de maturite de M2

Ce qui est stabilise :

- doctrine : le studio prepare, l'humain valide ;
- lecture seule pour les prototypes ;
- source canonique obligatoire ;
- classification `bloquant`, `reserve`, `information`;
- sortie CLI deterministe ;
- tests unitaires pour PERSON et ORG ;
- documentation d'usage et retours d'usage ;
- integration avec les validateurs existants, sans creation de controle nouveau.

Ce qui reste experimental :

- ergonomie CLI pour un utilisateur non expert ;
- formulation precise des reserves par famille ;
- preparation de PR assistee ;
- factorisation technique ;
- articulation avec des familles non identitaires comme `IMAGE`, `CONCERT` ou `CITATION`.

Ce qui manque encore :

- contrat d'interface interne entre un eventuel moteur commun et des adaptateurs ;
- criteres pour decider quand une famille merite un prototype ;
- evaluation d'une famille structurellement differente de PERSON/ORG ;
- doctrine sur les cas ou un prototype doit produire un refus plutot qu'une reserve ;
- decision sur le degre de mutualisation acceptable avant tout nouvel outil.

Niveau de confiance actuel :

M2 est mature comme doctrine de preparation et comme patron de pre-validation pour des identites canoniques. M2 n'est pas encore mature comme moteur general multi-familles.

## 8. Arbitrages ouverts

Options plausibles pour la suite :

| Option | Coherence avec l'etat reel | Commentaire |
| --- | --- | --- |
| Implementer `PLACE` | Plausible, mais premature sans decision d'architecture. | `PLACE` a un schema et un validateur, mais son modele differe fortement de PERSON/ORG : lieux physiques, coordonnees, `same_as`, usages legacy. |
| Implementer `IMAGE` | Plausible plus tard. | Les questions de droits, niveaux session/image, photographe, sujets et provenance rendent l'abstraction plus risquee. |
| Implementer `CONCERT` | Plausible mais sensible. | La coexistence de couches `CONCERT-*` et `JD-CONCERT-*` demande une doctrine propre. |
| Factoriser maintenant tout le code | Non recommande. | Deux familles ne suffisent pas pour figer un moteur commun complet. |
| Definir une architecture d'adaptateurs | Recommande. | Permet de formaliser les invariants communs sans nier les variations. |
| Attendre sans avancer | Non recommande. | Les retours PERSON/ORG donnent assez de matiere pour une decision d'architecture documentaire. |

L'arbitrage principal porte donc sur le niveau de mutualisation : contrat commun de sortie et adaptateurs par famille, ou scripts separes jusqu'au troisieme prototype.

## 9. Recommandation

Quelle doit etre la prochaine etape de M2 ?

Recommandation :

Definir une architecture M2 d'adaptateurs, sans encore refactoriser les prototypes existants ni ouvrir une troisieme famille documentaire.

Cette etape devrait produire un cadrage documentaire, pas du code. Elle devrait decrire :

- le contrat commun minimal d'une pre-validation ;
- les champs communs d'une sortie CLI ;
- les responsabilites d'un adaptateur par famille ;
- les controles partageables sans perte de sens ;
- les controles explicitement non partageables ;
- les criteres d'entree pour un futur prototype `PLACE`, `IMAGE` ou `CONCERT`.

Arguments :

- PERSON et ORG prouvent un noyau commun, mais seulement sur deux familles identitaires ;
- les divergences de schema et de relation sont trop fortes pour un moteur unique immediat ;
- le prochain risque n'est pas l'absence de code commun, mais la confusion entre genericite utile et uniformisation excessive ;
- une architecture d'adaptateurs permettrait ensuite de choisir lucidement entre nouveau prototype et factorisation limitee.

## 10. Decision proposee

M2 doit-il poursuivre par un nouveau prototype ou par une reflexion d'architecture ?

Decision proposee :

M2 doit poursuivre par une reflexion d'architecture.

Orientation principale retenue :

Definir le contrat d'architecture d'un modele `moteur commun + adaptateurs par famille`, sans implementation immediate et sans ouverture d'une nouvelle famille documentaire.

Cette decision ne ferme pas `PLACE`, `IMAGE`, `CONCERT`, `RELEASE` ou `CITATION`. Elle impose seulement de clarifier d'abord ce qui sera partage, ce qui restera specifique et quels criteres permettront d'ouvrir le prochain prototype sans affaiblir la gouvernance M2.
