# M2 - Bilan intermediaire

## 1. Objet de M2

M2 a ete ouvert apres la cloture formelle de M0 et M1. Sa finalite est de structurer l'enrichissement documentaire du corpus : preparer des ajouts, verifier leur recevabilite, exposer les reserves et produire des Pull Requests relisibles.

Difference avec M0 :

- M0 a stabilise le socle : doctrine documentaire, registres existants, exports, applications, documents maitres et limites du depot.
- M2 ne requalifie pas le socle. Il organise la maniere d'ajouter de nouveaux objets ou de nouvelles sources sans degrader ce socle.

Difference avec M1 :

- M1 a fiabilise les controles de coherence documentaire autour des documents maitres : `DM -> atomes`, `DM -> registres`, `DM -> sources`, agregateur et statut consolide.
- M2 n'est pas un nouveau controle M1. Il intervient en amont des enrichissements pour eviter que des propositions mal formees arrivent dans les registres, les sources ou les PR.

Definition retenue :

Le Studio d'enrichissement documentaire est un studio de preparation. Il aide a qualifier une intention d'ajout, proposer une structure, pre-valider, lister les controles et preparer une PR. Il ne valide pas seul une interpretation, ne merge pas, ne corrige pas silencieusement et ne remplace pas la revue humaine.

## 2. Architecture retenue

### Flux A - ajout unitaire

Objectif :

Ajouter un objet documentaire unique deja qualifie : personne, lieu, organisation, image, concert, citation ou occurrence discographique selon le support reel du depot.

Perimetre :

- proposer un identifiant conforme ;
- renseigner les champs requis du modele existant ;
- verifier sources, collisions, relations minimales et schema ;
- produire une proposition relisible avant PR.

Ce flux a ete le plus avance dans M2, avec le contrat M2.1, la pre-validation M2.2, le contrat de PR M2.4 et le prototype PERSON.

### Flux B - integration documentaire

Objectif :

Integrer une source importante : livre, article, interview, fanzine, archive, memoire, these ou dossier documentaire.

Perimetre :

- qualifier la source candidate ;
- proposer ou mettre a jour une source canonique `Sxx` ;
- preparer un dossier source ;
- proposer atomes, citations, relations et enrichissements ;
- passer par les contrats M2.1, M2.2 et M2.4 avant integration effective.

Complementarite :

Le flux A traite un objet cible. Le flux B traite une source qui peut produire plusieurs propositions. Une integration documentaire peut donc declencher des ajouts unitaires, mais ne les dispense pas des validations par type.

## 3. Documents structurants produits

| Document | Role | Etat | Apport principal |
| --- | --- | --- | --- |
| `docs/m2-studio-enrichissement.md` | Cadrage general de M2. | Stabilise. | Definit le studio comme preparation, pas validation automatique. |
| `docs/m2-contrat-ajout-unitaire.md` | Contrat M2.1. | Stabilise. | Liste les types, champs, fichiers, validations et refus pour les ajouts unitaires. |
| `docs/m2-prevalidation-commune.md` | Contrat M2.2. | Stabilise. | Formalise `bloquant`, `reserve`, `information` et les verifications communes. |
| `docs/m2-integration-source-longue.md` | Contrat M2.3. | Stabilise documentairement. | Definit le flux source longue sans implementation. |
| `docs/m2-preparation-pr-assistee.md` | Contrat M2.4. | Stabilise. | Decrit le contenu minimal d'une PR et la revue humaine. |
| `docs/m2-prototype-ajout-person.md` | Specification du prototype PERSON. | Stabilise. | Definit le premier prototype operationnel cible. |
| `docs/m2-retour-usage-add-person.md` | Retour d'usage V1. | Cloture. | Identifie les limites initiales : cible, redondance, aide categorie, reserve, alias. |
| `docs/m2-retour-usage-add-person-v2.md` | Retour d'usage V2. | Cloture. | Valide les ameliorations et conclut que PERSON peut servir de modele. |
| `docs/m2-prototype-ajout-org.md` | Specification du prototype ORG. | Stabilise documentairement. | Definit ORG comme second candidat, sans implementation. |
| `docs/m2-add-person-cli.md` | Documentation utilisateur du CLI PERSON. | En vigueur. | Explique la commande, les parametres, la sortie et les limites. |

Etat global :

M2 possede maintenant une architecture documentaire coherente. L'implementation reste limitee volontairement au prototype PERSON.

## 4. Prototype PERSON

### Objectifs

Le prototype PERSON teste le flux d'ajout unitaire sur une famille documentaire limitee, gateable et frequente.

Il vise a :

- proposer un identifiant `PERSON-<slug>` ;
- verifier les sources `Sxx` contre `data/registre.json` ;
- verifier la categorie PERSON ;
- detecter les collisions d'identifiant, nom, alias et `same_as` ;
- produire une entree candidate YAML ;
- classer les constats en `bloquant`, `reserve` ou `information` ;
- rester en lecture seule.

### Implementation

L'implementation existe dans `tools/m2_add_person.py`.

Comportement reel :

- lit `data/registre.json` ;
- lit `registers/people/00_canonical_people.md` ;
- lit `registers/people/00_authors_canonical.md` ;
- lit `exports/generated/people.json` pour les `PERS-*` ;
- valide la forme de l'entree candidate avec le schema PERSON ;
- produit une sortie deterministe ;
- retourne un code non nul en presence de bloquants ;
- ne modifie aucun fichier.

Les tests existent dans `tools/test_m2_add_person.py`. Ils couvrent notamment :

- cas conforme ;
- source inconnue ;
- categorie invalide ;
- collision d'identifiant ;
- auteur-source avec `same_as` interdit ;
- cible d'ecriture sans `same_as` ;
- cible probable avec `same_as` ;
- reserve d'identite ;
- alias proche ;
- aide CLI ;
- determinisme.

### Resultats

Le retour V1 a confirme une valeur documentaire reelle mais a conclu : `A ameliorer avant extension`.

Les ameliorations ont ensuite traite :

- cible d'ecriture plus explicite ;
- messages redondants reduits ;
- aide categorie renforcee ;
- cas reel de `reserve` ;
- alias ambigu classe en reserve.

Le retour V2 a conclu :

```text
oui
```

Le prototype PERSON est suffisamment stable pour servir de modele a une autre famille documentaire.

### Limites

Limites restantes observees :

- outil CLI reserve a un utilisateur connaissant les sources `Sxx` ;
- sortie YAML longue pour un simple diagnostic ;
- cible d'ecriture avec `same_as` probable mais pas resolue jusqu'au fichier exact ;
- detection d'ambiguite sans explication historiographique ;
- pas de generation de patch ;
- pas d'ouverture de PR ;
- pas d'ecriture dans les registres.

Ces limites sont coherentes avec le perimetre du prototype : lecture seule et preparation, pas integration automatique.

## 5. Enseignements tires

### Ce qui fonctionne

- Le modele `bloquant` / `reserve` / `information` est exploitable en CLI.
- Une sortie de pre-validation peut etre utile sans ecrire dans le depot.
- Les sources inconnues peuvent etre bloquees tot.
- Les categories fermees sont mieux controlees par un outil que par edition manuelle.
- Les collisions de nom, alias et identifiant sont detectables avant PR.
- Une entree candidate structuree aide la revue humaine.

### Ce qui a ete valide

- Le principe lecture seule est praticable.
- La pre-validation M2.2 a une valeur concrete.
- La documentation d'usage est indispensable pour eviter les mauvaises interpretations.
- Le retour d'usage avant extension evite de generaliser trop vite un prototype imparfait.
- Les tests automatises sont utiles meme pour un prototype documentaire local.

### Ce qui reste a demontrer

- Qu'un second type documentaire peut reprendre le meme patron sans duplication excessive.
- Que les cas JSON comme `ORG` se pretent aussi bien au modele que les blocs YAML PERSON.
- Que la preparation de PR peut etre assistee sans masquer les reserves.
- Que l'integration documentaire longue peut rester decoupee et relisible.
- Que des interfaces ou formulaires n'encodent pas trop tot des regles encore mouvantes.

## 6. Prototype ORG

### Etat actuel

`docs/m2-prototype-ajout-org.md` existe et definit le prototype fonctionnel d'ajout ORG. Aucun code ORG n'est encore implemente.

Le modele reel s'appuie sur :

- `schemas/organization_canonical.schema.json` ;
- `registers/orgs/orgs.json` ;
- `tools/validate_orgs.py` ;
- `registers/people/pending_org.json` pour certaines provenances.

Etat observe lors du cadrage ORG :

- 8 organisations canoniques ;
- identifiants `ORG-0001` a `ORG-0008` ;
- prochain identifiant attendu : `ORG-0009`, sous reserve de relecture au moment d'un ajout ;
- validateur ORG gateable disponible.

### Role

ORG est le second candidat logique apres PERSON. Il permet de tester la generisation du modele sur un type proche mais different :

- identite canonique ;
- alias ;
- collisions ;
- source obligatoire ;
- schema executable ;
- validateur gateable.

### Differences avec PERSON

| Sujet | PERSON | ORG |
| --- | --- | --- |
| Identifiant | `PERSON-<slug>` semantique. | `ORG-NNNN` numerique. |
| Format | YAML dans registres people. | JSON dans `registers/orgs/orgs.json`. |
| Relation principale | `same_as` vers `PERS-*`, origine auteur-source possible. | `joy_division_relation`, `same_as` externes, provenance possible. |
| Champs specifiques | `categorie`, `role`, `a_arbitrer`. | `country`, `status`, `gate`, `identity_frozen`, `drift_sentinel`, `last_verified`. |
| Risque principal | Fusion de personnes. | Confusion organisation/personne/lieu/concept et relation Joy Division trop forte. |

### Risques specifiques

- creer un `ORG-` pour une entite qui releve en fait de `PERSON`, `PLACE` ou concept ;
- surestimer la relation avec Joy Division ;
- utiliser un pays ou statut techniquement valide mais documentairement fragile ;
- ajouter une date `last_verified` sans validation humaine effective ;
- creer un identifiant numerique non disponible ;
- dupliquer une organisation deja presente comme alias ou dans les registres source-specifiques.

### Niveau de preparation

ORG est pret pour une implementation limitee de prototype CLI, sur le modele de PERSON, si le prochain chantier reste strictement borne :

- lecture seule ;
- aucune modification de `registers/orgs/orgs.json` ;
- proposition d'entree candidate seulement ;
- tests unitaires ;
- validation par `tools/validate_orgs.py` sur donnees de test ou entree candidate ;
- aucun prototype PLACE, CONCERT, IMAGE ou RELEASE dans le meme chantier.

ORG ne doit pas encore devenir un assistant generalise multi-types.

## 7. Dette M2 restante

Dette ouverte :

- prototype ORG non implemente ;
- pre-validation commune encore principalement contractuelle, sauf comportement concret dans PERSON ;
- preparation de PR assistee non automatisee ;
- integration documentaire source longue non implementee ;
- absence de patch generation pour PERSON ;
- absence de flux de branche/PR automatise dans le prototype ;
- absence d'interface ou formulaire ;
- absence d'outil generique multi-familles.

Dette reportee :

- interfaces et formulaires ;
- generalisation a PLACE, CONCERT, IMAGE, RELEASE ou CITATION ;
- automatisation de PR avancee ;
- aide contextuelle historiographique ;
- resolution automatique des arbitrages ;
- integration documentaire longue outillee.

Depend d'une decision future :

- implementer ORG maintenant ou renforcer encore PERSON ;
- creer une couche commune de pre-validation partagee entre PERSON et ORG ;
- transformer M2.4 en outil de preparation de PR ;
- prioriser M2.3 source longue avant de multiplier les ajouts unitaires.

## 8. Etat de maturite de M2

### Stabilise

- doctrine M2 : le studio prepare, l'humain valide ;
- separation entre ajout unitaire et integration documentaire ;
- contrat d'ajout unitaire ;
- pre-validation commune ;
- contrat de preparation de PR ;
- prototype PERSON en lecture seule ;
- tests du prototype PERSON ;
- retour d'usage V1 et V2 ;
- specification ORG.

### Experimental

- extension du modele a une deuxieme famille ;
- classification des reserves hors PERSON ;
- generation d'entrees candidates JSON ;
- usage du modele sur des relations plus ouvertes comme `joy_division_relation.type` ;
- articulation future entre pre-validation et preparation de PR.

### Necessite encore validation

- prototype ORG implemente et teste ;
- effet reel d'une PR preparee par un outil ;
- integration documentaire d'une source longue ;
- ergonomie d'un flux non technique ;
- robustesse face a des cas ambigus plus riches que les tests PERSON actuels.

Niveau de confiance actuel :

Le niveau de confiance est bon pour le cadre documentaire et pour le prototype PERSON. Il reste modere pour la generisation de M2, car un seul type documentaire est implemente. M2 peut avancer, mais par extensions courtes et controlees.

## 9. Arbitrages ouverts

Options plausibles pour la suite :

| Option | Interet | Risque | Appreciation |
| --- | --- | --- | --- |
| Implementer ORG | Tester la generisation sur un second type proche de PERSON. | Dupliquer trop vite du code si aucune couche commune n'est identifiee. | Option la plus logique si le perimetre reste strict. |
| Generaliser le modele | Factoriser les concepts communs de pre-validation. | Abstraction prematuree avec seulement un prototype implemente. | A differer apres un prototype ORG minimal. |
| Renforcer PERSON | Ameliorer encore l'ergonomie et la cible d'ecriture. | Rendement decroissant apres le retour V2. | Utile seulement si un usage concret revele un nouveau blocage. |
| Preparer l'integration documentaire | Attaquer M2.3. | Beaucoup plus de surface : sources, atomes, citations, relations. | Important, mais plus risque que ORG a ce stade. |
| Travailler les interfaces | Ameliorer l'accessibilite. | Encoder trop tot des regles non stabilisees. | A reporter. |
| Automatiser la preparation de PR | Reduire la friction de revue. | Confondre proposition pre-validee et validation humaine. | A cadrer apres au moins deux prototypes. |

## 10. Recommandation

Question :

Quelle doit etre la prochaine etape de M2 ?

Recommandation :

Implementer un prototype CLI ORG minimal, en lecture seule, strictement derive de `docs/m2-prototype-ajout-org.md`.

Conditions :

- ne pas creer de prototype multi-types ;
- ne pas modifier les registres ORG ;
- ne pas creer d'interface ;
- ne pas automatiser Git ou GitHub ;
- reutiliser seulement les principes PERSON qui ont ete valides ;
- ajouter des tests ORG des le premier chantier ;
- documenter un retour d'usage ORG avant toute nouvelle extension.

Justification :

ORG est le meilleur test de generisation actuellement disponible : assez proche de PERSON pour reutiliser le modele, assez different pour verifier que M2 ne depend pas d'un cas particulier. L'etape suivante ne doit donc pas etre une interface ni une integration documentaire longue, mais un second prototype controle.

Decision intermediaire :

M2 est suffisamment mature pour poursuivre vers un prototype ORG minimal. M2 n'est pas encore suffisamment mature pour une generalisation multi-familles, une interface ou une automatisation complete de PR.
