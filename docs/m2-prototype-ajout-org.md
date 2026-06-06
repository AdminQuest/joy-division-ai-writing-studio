# M2.6 - Prototype d'ajout ORG

## 1. Objet du prototype

Le prototype d'ajout `ORG` definit le second flux operationnel cible du Studio M2, apres la stabilisation du prototype `PERSON`. Il decrit comment un assistant pourrait preparer l'ajout d'une organisation canonique dans le corpus, sans interface graphique et sans automatisation generale.

Perimetre :

- un seul objet principal de type `ORG-` ;
- preparation d'une entree candidate compatible avec `schemas/organization_canonical.schema.json` ;
- verification de l'identifiant numerique `ORG-NNNN` ;
- verification des sources `Sxx` contre `data/registre.json` ;
- verification des collisions de nom canonique, d'alias et d'identifiants externes ;
- verification de la relation documentee avec Joy Division ;
- classification des constats en `bloquant`, `reserve` ou `information`.

Objectifs :

- reprendre les principes valides par le prototype `PERSON` ;
- tester un deuxieme type documentaire structure ;
- eviter la creation manuelle d'un doublon `ORG-` ;
- rendre visibles les arbitrages humains avant toute PR ;
- conserver une sortie relisible, deterministe et limitee au type `ORG`.

Limites :

- aucun code n'est cree par ce document ;
- aucun formulaire ni interface graphique n'est defini ;
- aucune organisation n'est ajoutee automatiquement ;
- aucun registre, schema, export ou validateur n'est modifie ;
- aucune fusion d'organisations n'est decidee automatiquement ;
- aucune PR n'est ouverte automatiquement ;
- aucun commit direct sur `main` n'est autorise.

Prototype ORG != implementation generale M2.

Ce prototype est un contrat fonctionnel limite a `ORG`. Il ne definit pas encore un assistant multi-types, une interface, un generateur universel ou un workflow Git automatise.

## 2. Cas d'usage

Scenario cible :

L'utilisateur souhaite ajouter une nouvelle organisation au corpus.

Donnees connues possibles :

- nom canonique de l'organisation ;
- categorie documentaire ;
- pays ;
- relation avec Joy Division ;
- source documentaire `Sxx` ;
- alias ou variantes de nom ;
- statut de l'organisation ;
- ville, periode d'activite ou sous-categorie ;
- identifiants externes verifies ;
- provenance issue d'un `PERS-*` ou d'une attribution non-personne.

Donnees inconnues possibles :

- prochain numero `ORG-NNNN` disponible ;
- existence d'une organisation deja canonisee sous un autre nom ;
- presence de l'organisation comme alias d'une entree existante ;
- existence d'une organisation proche dans les registres source-specifiques ;
- categorie exacte entre `group`, `label`, `institution`, `venue_org`, `crew`, `media` et `other` ;
- statut exact : `active`, `dissolved`, `dormant` ou `unknown` ;
- relation documentaire suffisamment forte avec Joy Division ;
- provenance attendue dans `registers/people/pending_org.json`.

Resultat attendu :

- une proposition d'identifiant `ORG-NNNN` ;
- une entree candidate JSON compatible avec le schema canonique ;
- une classification des constats en `bloquant`, `reserve` ou `information` ;
- la liste des validations a executer ;
- les reserves et arbitrages humains restants ;
- une PR relisible selon M2.4 si aucun bloquant n'est present.

## 3. Entrees minimales

Le prototype doit demander uniquement les informations necessaires au modele `ORG` reel.

### Entrees obligatoires

| Entree | Champ cible | Regle |
| --- | --- | --- |
| nom canonique | `canonical_name` | Non vide. |
| categorie | `category` | Valeur du vocabulaire ferme du schema. |
| pays | `country` | Code ISO 3166-1 alpha-2, par exemple `GB`, `US`, `NL`. |
| relation avec Joy Division | `joy_division_relation.type` | Non vide ; decrit la nature minimale de la relation. |
| source(s) | `sources` | Liste non vide d'identifiants `Sxx` presents dans `data/registre.json`. |
| statut | `status` | Valeur du vocabulaire ferme du schema. |
| visibilite | `gate` | `public` ou `private`. |
| date de verification humaine | `last_verified` | Date ISO `YYYY-MM-DD`, fournie explicitement ; pas de date dynamique implicite. |

Categories valides :

- `group`
- `label`
- `institution`
- `venue_org`
- `crew`
- `media`
- `other`

Statuts valides :

- `active`
- `dissolved`
- `dormant`
- `unknown`

Champs techniques obligatoires a produire dans la proposition :

- `org_id`, propose par le prototype ;
- `canonical_name`, issu du nom fourni ;
- `aliases`, tableau vide ou alias fournis ;
- `category`, issue de l'entree utilisateur ;
- `country`, issu de l'entree utilisateur ;
- `status`, issu de l'entree utilisateur ;
- `same_as`, objet d'identifiants externes avec valeurs documentees ou `null` ;
- `joy_division_relation`, objet contenant au minimum `type` ;
- `sources`, issu de l'entree utilisateur ;
- `identity_frozen`, toujours `true` seulement si la proposition est prete a validation humaine ;
- `drift_sentinel`, version attendue par le validateur, actuellement `v1.0` ;
- `gate`, issu de l'entree utilisateur ;
- `last_verified`, date explicite de verification humaine.

### Entrees facultatives

| Entree | Champ cible | Usage |
| --- | --- | --- |
| alias | `aliases` | Detecter les collisions et conserver les formes secondaires. |
| sous-categorie | `subcategory` | Preciser le type, par exemple `punk`, `archive`, `sound_engineering`. |
| ville | `city` | Localiser l'organisation lorsque c'est documente. |
| debut d'activite | `active_from` | Annee ou date partielle documentee. |
| fin d'activite | `active_until` | Chaine ou `null` si toujours active ou non bornee. |
| periode de relation | `joy_division_relation.period` | Periode documentee de la relation, ou `null`. |
| notes de relation | `joy_division_relation.notes` | Precision libre, non substituable a une source. |
| Wikidata | `same_as.wikidata` | Identifiant `Q...` verifie. |
| Discogs | `same_as.discogs` | URL ou identifiant documentaire verifie selon l'usage existant. |
| MusicBrainz | `same_as.musicbrainz` | UUID MusicBrainz verifie. |
| provenance `PERS-*` | `provenance.from_pers` | Origine issue d'un hand-off `registers/people/pending_org.json`. |
| provenance attribution | `provenance.from_attribution` | Origine issue d'une attribution non-personne. |

Le prototype ne doit pas inventer de champ supplementaire. Les champs facultatifs ne doivent etre proposes que s'ils existent dans le schema ou dans le registre canonique observe.

## 4. Verifications realisees

### Identifiant

Format attendu :

```text
ORG-NNNN
```

Verifications :

- l'identifiant respecte `^ORG-\d{4}$` ;
- le numero est zero-padde sur quatre chiffres ;
- l'identifiant n'existe pas deja dans `registers/orgs/orgs.json` ;
- le numero propose est disponible ;
- le prochain numero est calcule a partir du plus grand `ORG-NNNN` existant.

Etat observe du registre canonique :

- `ORG-0001` a `ORG-0008` existent ;
- le prochain numero libre attendu serait `ORG-0009`, sous reserve de relecture au moment de l'ajout.

Classification :

- identifiant deja utilise : `bloquant` ;
- trou numerique volontaire ou numero non contigu : `reserve` si justifie, sinon `bloquant` si incoherent ;
- prochain numero propose automatiquement : `information`.

### Nom canonique

Verifications :

- `canonical_name` est non vide ;
- collision stricte avec un `canonical_name` existant ;
- collision stricte avec un alias existant ;
- collision probable par proximite de libelle ;
- confusion possible avec une personne, un lieu ou un concept lorsque le nom est ambigu.

Classification :

- meme organisation evidente : `bloquant` ;
- organisation proche ou libelle ambigu : `reserve` ;
- simple variante documentee et non conflictuelle : `information`.

### Source documentaire

Verifications :

- chaque source a le format attendu par l'usage `Sxx` ;
- chaque source existe dans `data/registre.json` ;
- `sources` est une liste non vide ;
- un identifiant interne `ORG-*`, `PERSON-*`, `IMAGE-*` ou une URL seule ne remplace pas une source documentaire.

Classification :

- source absente : `bloquant` ;
- source inconnue : `bloquant` ;
- source connue mais relation documentaire faible : `reserve`.

### Categorie

Verifications :

- `category` appartient au vocabulaire reel du schema :
  - `group`
  - `label`
  - `institution`
  - `venue_org`
  - `crew`
  - `media`
  - `other`
- le choix ne transforme pas une personne, un lieu physique ou un concept en organisation ;
- `subcategory` reste libre mais ne remplace pas `category`.

Classification :

- categorie hors vocabulaire : `bloquant` ;
- categorie possible mais a arbitrer : `reserve` ;
- sous-categorie absente : `information`, sauf si elle est necessaire a la comprehension du cas.

### Pays

Verifications :

- `country` respecte `^[A-Z]{2}$` ;
- le code correspond a un ISO 3166-1 alpha-2 ;
- le pays est coherent avec l'organisation documentee.

Classification :

- format invalide : `bloquant` ;
- pays inconnu ou incertain mais code techniquement valide : `reserve` ;
- pays absent : `bloquant`, car le champ est requis.

### Joy Division relation

Verifications :

- `joy_division_relation` est un objet ;
- `joy_division_relation.type` est present et non vide ;
- la relation est compatible avec les exemples observes : `peer_group`, `successor_scene`, `influence_recipient`, `label_mate`, `technical_crew`, `contextual`, `archive`, `press_coverage` ;
- `period` vaut une chaine ou `null` ;
- `notes` precise la relation sans remplacer la source.

Le champ `type` n'est pas un vocabulaire ferme dans le schema actuel. Le prototype ne doit donc pas refuser une valeur nouvelle uniquement parce qu'elle n'apparait pas dans les entrees existantes. Il doit en revanche signaler une valeur vague ou non documentee.

Classification :

- relation absente ou vide : `bloquant` ;
- relation trop vague ou trop forte pour la source : `reserve` ;
- relation claire mais periode absente : `information` si `period: null` est justifie.

### Schéma

Verifications :

- l'entree candidate satisfait `schemas/organization_canonical.schema.json` ;
- `tools/validate_orgs.py` passe sans erreur ;
- `identity_frozen` vaut `true` ;
- `drift_sentinel` vaut la version attendue par le validateur, actuellement `v1.0` ;
- `gate` vaut `public` ou `private` ;
- `last_verified` respecte `YYYY-MM-DD` ;
- `same_as.wikidata`, si present, respecte le format `Q...`.

Classification :

- schema invalide : `bloquant` ;
- warning de provenance : `reserve` ou `information` selon le cas documente ;
- absence d'identifiant externe : `information` si les valeurs `null` sont explicites.

## 5. Classification

Le prototype ORG reutilise strictement la classification M2.2.

| Classification | Definition | Cas typiques ORG |
| --- | --- | --- |
| `bloquant` | La proposition n'est pas recevable en l'etat. | `ORG-` deja utilise ; source inconnue ; categorie invalide ; pays invalide ; relation vide ; schema invalide ; collision certaine. |
| `reserve` | La proposition peut etre revue seulement si l'arbitrage est explicite. | Organisation proche ; alias ambigu ; pays incertain ; categorie a arbitrer ; relation Joy Division trop vague ; provenance non retrouvee mais documentee. |
| `information` | Constat utile sans correction immediate. | Prochain numero propose ; `same_as` externe absent et mis a `null` ; `period: null` ; sous-categorie absente ; cible d'ecriture confirmee. |

Regles non negociables :

- collision certaine -> `bloquant` ;
- organisation proche -> `reserve` ;
- alias ambigu -> `reserve` ;
- source inconnue -> `bloquant` ;
- schema invalide -> `bloquant` ;
- validation humaine conservee dans tous les cas.

## 6. Generation proposee

Le prototype prepare une proposition. Il ne l'applique pas directement.

Elements prepares :

- identifiant `ORG-NNNN` propose ;
- entree candidate JSON compatible avec le schema ;
- resume documentaire ;
- liste des validations executees ou a executer ;
- liste des bloquants, reserves et informations ;
- cible d'ecriture probable ;
- diff propose, uniquement dans une future implementation.

Cible d'ecriture normale :

```text
registers/orgs/orgs.json
```

Validations attendues :

- `python3 tools/validate_orgs.py`
- `python3 tools/check_generated_sync.py` ou `python3 tools/build_all.py` seulement si le pipeline du depot signale des artefacts a synchroniser.

Ce qui n'est jamais genere automatiquement :

- une fusion d'organisations ;
- une source `Sxx` absente de `data/registre.json` ;
- une categorie hors vocabulaire ;
- une relation Joy Division inventee ;
- un pays reconstruit sans preuve ;
- un identifiant externe non verifie ;
- une date dynamique implicite pour `last_verified` ;
- une modification de schema ou de validateur ;
- une PR mergee ou un commit direct sur `main`.

Exemple logique d'entree candidate :

```json
{
  "org_id": "ORG-0009",
  "canonical_name": "Exemple Organisation",
  "aliases": [],
  "category": "label",
  "country": "GB",
  "status": "unknown",
  "same_as": {
    "wikidata": null,
    "musicbrainz": null,
    "discogs": null
  },
  "joy_division_relation": {
    "type": "label",
    "period": null,
    "notes": "Relation documentee par la source indiquee."
  },
  "sources": ["Sxx"],
  "identity_frozen": true,
  "drift_sentinel": "v1.0",
  "gate": "private",
  "last_verified": "YYYY-MM-DD"
}
```

L'exemple ci-dessus est une forme logique. Il ne doit pas etre copie tel quel avec `Sxx` ou `YYYY-MM-DD`.

## 7. Sortie attendue

Le prototype ORG doit produire une sortie parallele a celle du prototype PERSON :

- decision : `pre-validee`, `pre-validee avec reserve` ou `non pre-validee` ;
- identifiant propose ;
- entree candidate ;
- bloquants ;
- reserves ;
- informations ;
- cible d'ecriture ;
- validations a executer.

Exemple de forme de sortie :

```text
Decision : pre-validee avec reserve
Identifiant propose : ORG-0009
Bloquants :
- aucun
Reserves :
- alias proche a arbitrer: Exemple Org ~ Exemple Organisation (ORG-0007)
Informations :
- Cible d'ecriture probable : registers/orgs/orgs.json
Entree candidate :
{ ... }
```

La sortie doit permettre a un humain de repondre rapidement :

- quelle organisation est proposee ?
- quelle source la justifie ?
- quel numero `ORG-` est propose ?
- quels champs requis restent a completer ?
- quels doublons ont ete recherches ?
- quelles reserves restent ouvertes ?

## 8. Cas de refus

Le prototype doit refuser ou classer comme `non pre-validee` toute proposition dans les cas suivants :

- `ORG` deja existante ;
- identifiant `ORG-` deja utilise ;
- identifiant ne respectant pas `ORG-NNNN` ;
- numero non disponible ;
- nom canonique vide ;
- collision forte de nom ou d'alias ;
- source absente ;
- source inconnue dans `data/registre.json` ;
- categorie invalide ;
- pays invalide ;
- statut invalide ;
- `gate` invalide ;
- `joy_division_relation.type` absent ou vide ;
- relation Joy Division inventee ou non documentee ;
- `same_as.wikidata` invalide ;
- schema invalide ;
- `identity_frozen` different de `true` apres validation humaine ;
- `drift_sentinel` different de la version attendue ;
- `last_verified` absent ou mal forme ;
- organisation en realite de type `PERSON`, `PLACE` ou concept ;
- demande de fusion automatique ;
- demande de suppression automatique ;
- demande de commit direct sur `main`.

Un cas doit aussi etre refuse ou reclasse hors prototype si la demande implique une integration documentaire longue, la creation d'une nouvelle source canonique, une refonte du registre ORG ou une interface.

## 9. Articulation avec M2

### Lien avec M2.1

Le prototype applique le contrat d'ajout unitaire :

- un seul objet `ORG` est prepare ;
- les champs requis du schema reel sont respectes ;
- la source documentaire est obligatoire ;
- les relations minimales existantes sont explicites : `joy_division_relation`, `same_as`, `provenance` ;
- le diff futur doit rester limite a l'objet et aux artefacts strictement necessaires.

### Lien avec M2.2

Le prototype reprend la pre-validation commune :

- `bloquant` pour source inconnue, identifiant duplique, categorie invalide, pays invalide, relation vide ou schema invalide ;
- `reserve` pour collision probable, alias proche, categorie a arbitrer, pays incertain ou relation trop vague ;
- `information` pour numero propose, cible d'ecriture, champ facultatif absent ou identifiant externe `null`.

La reserve ne doit jamais masquer une source absente, une collision certaine ou un schema invalide.

### Lien avec M2.4

Le prototype prepare une future PR relisible :

- branche dediee ;
- diff limite ;
- resume documentaire ;
- validations executees ;
- reserves visibles ;
- validation humaine obligatoire ;
- aucun merge automatique.

### Reutilisation du prototype PERSON

Le prototype ORG reprend de PERSON :

- sortie en sections `Decision`, `Bloquants`, `Reserves`, `Informations`, `Entree candidate` ;
- distinction entre collision stricte et collision probable ;
- aide sur vocabulaire ferme ;
- explication de la cible d'ecriture ;
- refus des sources inconnues ;
- conservation de la validation humaine.

Il adapte ces principes au modele ORG :

- identifiant numerique sequentiel, pas slug semantique ;
- entree JSON canonique, pas bloc YAML `PERSON` ;
- relation `joy_division_relation` obligatoire ;
- controle `country`, `status`, `gate`, `identity_frozen`, `drift_sentinel` et `last_verified` ;
- provenance eventuelle depuis `registers/people/pending_org.json`.

## 10. Criteres de succes

Le prototype ORG pourra etre considere reussi si les conditions suivantes sont remplies :

- aucun `ORG-` duplique n'est propose ;
- le prochain numero disponible est calcule de facon deterministe ;
- toutes les sources `Sxx` sont connues dans `data/registre.json` ;
- la categorie appartient au vocabulaire reel ;
- le pays respecte ISO alpha-2 ;
- `joy_division_relation.type` est present ;
- l'entree candidate satisfait `schemas/organization_canonical.schema.json` ;
- `python3 tools/validate_orgs.py` passe apres integration ;
- les collisions de nom et d'alias sont detectees ;
- les reserves restent visibles ;
- aucune modification de schema ou de validateur n'est necessaire ;
- la PR future est relisible ;
- la validation humaine est conservee.

## 11. Comparaison avec PERSON

| Sujet | PERSON | ORG |
| --- | --- | --- |
| Identifiant | `PERSON-<slug>` derive du nom canonique. | `ORG-NNNN` numerique, zero-padde sur quatre chiffres. |
| Registre canonique | `registers/people/00_canonical_people.md` et `00_authors_canonical.md`, avec generation controlee depuis la couche provisoire. | `registers/orgs/orgs.json`, valide par `tools/validate_orgs.py`. |
| Format d'entree | Bloc YAML. | Objet JSON. |
| Champs requis principaux | `name`, `categorie`, `role`, `sources`, `same_as`, `alt_names`. | `canonical_name`, `category`, `country`, `status`, `same_as`, `joy_division_relation`, `sources`, champs de gouvernance. |
| Categories | `membre`, `entourage`, `industrie`, `critique_journaliste`, `auteur_secondaire`, `influence`, `theoricien_mobilise`. | `group`, `label`, `institution`, `venue_org`, `crew`, `media`, `other`. |
| Collisions | Nom, alias, `same_as` vers `PERS-*`, auteurs-sources. | Nom canonique, alias, identifiants externes, confusion personne/lieu/concept. |
| Sources | `sources` non vide, identifiants `Sxx`. | `sources` non vide, identifiants `Sxx`. |
| Relations | `same_as` vers `PERS-*`, origine auteur-source eventuelle. | `joy_division_relation`, `same_as` externes, `provenance` eventuelle. |
| Risques | Fusionner deux personnes, accepter un alias ambigu, rattacher un mauvais `PERS-*`. | Fusionner deux organisations, confondre personne/organisation/lieu, surestimer la relation Joy Division. |
| Reserve typique | Identite ou categorie a arbitrer, alias proche. | Alias proche, organisation proche, categorie ou relation a arbitrer, provenance non retrouvee. |
| Validateur | `python3 tools/validate_people.py`. | `python3 tools/validate_orgs.py`. |

## 12. Decision proposee

ORG est-il un bon second prototype M2 ?

Decision proposee :

Oui.

Justification :

- `ORG` dispose d'un schema canonique executable ;
- `ORG` dispose d'un validateur gateable ;
- le registre canonique est limite et relisible ;
- les risques de collision, alias et source sont proches de ceux deja traites par `PERSON` ;
- les differences avec `PERSON` sont structurantes mais controlables : identifiant numerique, JSON, relation Joy Division et champs de gouvernance ;
- le prototype permet de tester la generisation du modele M2 sans ouvrir une famille plus complexe comme `PLACE`, `CONCERT`, `IMAGE` ou `RELEASE`.

Le premier prototype ORG doit donc etre defini comme un assistant de preparation en lecture seule : il propose, verifie, classe et documente. L'humain valide.
