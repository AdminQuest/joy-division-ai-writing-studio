# M2.2 - Pre-validation commune

## 1. Objet de la pre-validation

La pre-validation est la couche commune qui examine une proposition d'enrichissement avant qu'elle devienne une Pull Request.

Elle intervient apres la preparation de l'ajout et avant l'execution des controles complets. Elle sert a detecter tot les erreurs simples, les incoherences de forme, les collisions probables et les arbitrages humains a exposer.

La pre-validation verifie :

- l'unicite des identifiants proposes ;
- l'existence des sources documentaires attendues ;
- la presence des champs obligatoires connus ;
- la resolution des relations vers des objets existants ;
- l'absence de collision documentaire evidente ;
- la coherence des artefacts generes avec le pipeline existant ;
- la separation entre source documentaire, provenance, droits, URL et identifiant interne.

La pre-validation ne decide pas :

- qu'une interpretation historique est vraie ;
- qu'une attribution incertaine est tranchee ;
- qu'un conflit documentaire est resolu ;
- qu'un droit de reproduction est acquis ;
- qu'une fusion d'identites peut etre effectuee ;
- qu'une relation nouvelle peut etre creee sans validation humaine.

Pre-validation != validation historiographique.

La pre-validation prepare une decision. Elle ne la remplace pas.

## 2. Position dans le pipeline M2

Pipeline commun :

```text
entree
  ->
preparation
  ->
pre-validation
  ->
controles
  ->
PR
  ->
validation humaine
```

| Etape | Role |
| --- | --- |
| Entree | Recevoir une intention d'enrichissement : ajout unitaire, integration documentaire ou proposition issue d'un futur assistant. |
| Preparation | Qualifier le type d'objet, collecter les champs, proposer les identifiants, reperer les fichiers concernes et documenter la source. |
| Pre-validation | Examiner la proposition avant commit : identifiants, sources, schemas, relations, collisions, artefacts generes et limites. |
| Controles | Executer les validateurs, build, sentinelles et controles M1 pertinents. Ces controles restent les preuves executables. |
| PR | Ouvrir une Pull Request lisible avec diff limite, resume, validations passees, reserves et arbitrages humains restants. |
| Validation humaine | Relire, demander correction, accepter, refuser ou differer l'enrichissement. |

La pre-validation peut produire une sortie exploitable par un futur assistant ou formulaire. Elle ne doit pas ecrire dans `main`, merger, corriger silencieusement les registres ou masquer les reserves.

## 3. Verifications universelles

Les verifications suivantes s'appliquent a toute proposition d'enrichissement, quel que soit le type d'objet.

### Unicite d'identifiant

Question : l'identifiant existe-t-il deja ?

Regle :

- rechercher l'identifiant propose dans les registres, exports disponibles et fichiers de travail pertinents ;
- verifier les deux couches lorsque le modele en possede deux, par exemple `CONCERT-` et `JD-CONCERT-*` ;
- traiter comme bloquante toute duplication stricte ;
- traiter comme reserve toute collision probable de slug, libelle, alias ou `same_as`.

Exemples :

- `PERSON-ian-curtis` existe deja : bloquant ;
- `ORG-0007` existe deja : bloquant ;
- un nouveau lieu a le meme libelle qu'un `PLACE-` existant : reserve au minimum, bloquant si l'identite est manifestement la meme.

### Source connue

Question : les sources `Sxx` existent-elles dans `data/registre.json` ?

Regle :

- verifier tout champ qui attend une source canonique `Sxx` contre `data/registre.json` ;
- ne pas utiliser `registers/references/` comme source de verite canonique ;
- distinguer source canonique, URL, provenance technique et identifiant interne ;
- signaler explicitement les cas ou le modele accepte une URL ou une description libre au lieu d'un `Sxx`.

Exemples :

- `S76` existe dans `data/registre.json` : conforme ;
- `S999` absent de `data/registre.json` : bloquant ;
- `IMAGE-I-0001` place dans un champ `sources` qui attend une source documentaire : bloquant ;
- URL unique pour une image documentee mais non canonisee en `Sxx` : reserve ou information selon le cas, jamais preuve silencieuse.

### Schema compatible

Question : les champs obligatoires sont-ils presents ?

Regle :

- utiliser les schemas et validateurs existants comme reference ;
- ne pas inventer un champ obligatoire absent du depot ;
- ne pas ignorer un champ exige par un validateur gateable meme s'il est seulement recommande dans un schema lisible ;
- classer comme bloquante l'absence d'un champ requis par le modele applicable.

Validations existantes utiles selon le type :

- `python3 tools/validate_people.py`
- `python3 tools/validate_places.py`
- `python3 tools/validate_orgs.py`
- `python3 tools/validate_images.py`
- `python3 tools/validate_concerts.py`
- `python3 tools/validate_quotes.py`

Cas particulier : il n'existe pas encore de validateur gateable dedie aux occurrences `RELEASE` de `schemas/song_occurrence.schema.yaml`. `tools/validate_songs.py` valide les chansons canoniques, pas les occurrences discographiques.

### Relations resolues

Question : les objets references existent-ils ?

Regle :

- verifier que les identifiants relies existent dans le registre ou l'artefact attendu ;
- verifier les relations minimales imposees par le modele ;
- signaler les relations facultatives non resolues comme reserve ou information selon leur effet ;
- refuser toute relation creee automatiquement pour faire passer une autre verification.

Relations courantes a verifier :

- `PERSON-*` dans `photographer`, `subjects`, attributions ou relations ;
- `PLACE-*` dans les lieux canonises ;
- `IMAGE-S-*` pour une image individuelle rattachee a une session ;
- `CONCERT-*` et `JD-CONCERT-*` dans la reconciliation concert ;
- `JD-SONG-*` pour les occurrences discographiques ;
- `EVENT-*` lorsqu'un ancrage chronologique est declare ;
- atomes `Sxx-Axxx` lorsque le champ les reference ;
- `source_id` ou `sources` lorsque le champ attend une source documentaire.

### Absence de collision documentaire

Question : l'objet existe-t-il deja sous un autre nom ?

Regle :

- rechercher les libelles proches, alias, `same_as`, slugs, dates, lieux, numeros de catalogue et sources similaires ;
- ne pas fusionner automatiquement deux objets ;
- ne pas creer un doublon pour eviter un arbitrage ;
- rendre visible toute ambiguite dans la sortie de pre-validation.

Exemples :

- personne avec variante orthographique deja portee en `alt_names` : reserve ou bloquant ;
- concert meme date, meme lieu, meme source : bloquant probable ;
- image meme photographe, meme session, meme description mais identifiant nouveau : reserve forte ;
- citation meme source et meme texte sous ordinal different : reserve ou bloquant selon le contexte.

### Artefacts generes synchronises

Question : les artefacts generes restent-ils coherents ?

Regle :

- ne pas editer manuellement les fichiers declares generes ;
- regenerer les artefacts lorsque le pipeline existant le demande ;
- committer les artefacts regeneres lorsque `tools/check_generated_sync.py` ou `tools/build_all.py` les produit comme correction attendue ;
- verifier que la proposition ne laisse pas d'exports, registres generes ou documents maitres obsoletes.

Outils existants :

- `python3 tools/build_all.py`
- `python3 tools/check_generated_sync.py`

La pre-validation doit seulement definir que la coherence des artefacts est requise. Elle ne cree pas de nouveau mecanisme de synchronisation.

## 4. Verifications par famille d'objet

Cette section resume les points particuliers par famille. Le detail du contrat d'ajout unitaire reste dans `docs/m2-contrat-ajout-unitaire.md`.

| Famille | Verifications particulieres |
| --- | --- |
| PERSON | Verifier le format `PERSON-<slug>`, les champs requis du schema canonique, la categorie fermee, les `sources`, les `same_as` vers `PERS-*`, les collisions avec `alt_names` et le risque de fusion de personnes distinctes. |
| PLACE | Verifier le format `PLACE-<SLUG>`, les champs `id`, `label`, `type`, le vocabulaire de type, les sources documentaires, les coordonnees si presentes, `same_as` et les collisions de lieux physiques. |
| ORG | Verifier le format `ORG-NNNN`, les champs requis JSON, `country`, `category`, `status`, `joy_division_relation.type`, les sources, les alias et la distinction avec personne, lieu ou concept. |
| IMAGE | Verifier `IMAGE-S-NNNN` ou `IMAGE-I-NNNN`, `level`, `session_ref` pour les images individuelles, `photographer`, `subjects`, `sources`, droits/provenance, et accepter `place` comme `PLACE-`, description libre ou `null` selon le schema. |
| CONCERT | Verifier la couche canonique `CONCERT-<SLUG>` lorsque le concert entre dans son perimetre, la couche legacy `JD-CONCERT-*`, `membres_reconcilies`, `same_as`, `lieu` resolu vers `PLACE-`, date/date_precision et statut. |
| RELEASE | Verifier que l'objet est une occurrence discographique rattachee au Songbook, pas un nouveau registre `RELEASE-*`; verifier `song_id`, `occurrence_id`, `occurrence_type`, source documentaire et limites dues a l'absence de validateur gateable dedie. |
| CITATION | Verifier les conventions d'id reconnues, `source_id`, `texte`, `type`, `page` ou `inconnue`, `locuteur`, attribution non inventee, longueur compatible avec les droits et distinction verbatim/paraphrase/concept. |

## 5. Classification des resultats

La pre-validation classe chaque constat dans une des trois categories suivantes.

| Categorie | Definition | Exemples | Consequence |
| --- | --- | --- | --- |
| bloquant | Ecart qui rend la proposition non recevable en l'etat. | Identifiant deja utilise ; source `Sxx` inconnue ; champ obligatoire absent ; relation requise introuvable ; schema incompatible ; artifact genere obsolete non committe ; ajout dans un registre inexistant. | La PR ne doit pas etre ouverte, ou doit rester en correction avant demande de revue. |
| reserve | Point acceptable seulement s'il est explicite, documente et soumis a validation humaine. | Alias proche ; lieu non canonicalise mais decrit ; attribution incertaine ; source URL unique pour une image ; absence de validateur dedie pour `RELEASE` ; divergence de libelle non bloquante. | La PR peut etre ouverte si la reserve est visible dans le resume et ne masque aucun bloquant. |
| information | Constat utile qui n'appelle pas de correction immediate. | Artefact non concerne ; relation facultative absente ; source orpheline informative ; controle M1 non applicable ; champ facultatif non renseigne. | La PR peut etre ouverte ; l'information aide la revue humaine. |

Regle de synthese :

- au moins un bloquant : proposition non pre-validee ;
- aucune erreur bloquante, mais une ou plusieurs reserves : proposition pre-validee avec reserve ;
- aucun bloquant ni reserve : proposition pre-validee.

La categorie "reserve" ne doit jamais servir a accepter une source inconnue, une collision d'identifiant ou un schema invalide.

## 6. Decisions interdites a la pre-validation

La pre-validation ne doit pas prendre les decisions suivantes.

| Decision interdite | Pourquoi |
| --- | --- |
| Validation historiographique | Une verification formelle ne prouve pas la justesse d'une interpretation historique. |
| Resolution d'un conflit documentaire | Les contradictions entre sources doivent etre exposees, pas tranchees automatiquement. |
| Arbitrage de droits | Les droits de reproduction, citation ou republication exigent une decision humaine et souvent contextuelle. |
| Fusion d'identites | Fusionner personnes, lieux, organisations, concerts ou citations peut detruire une nuance documentaire. |
| Creation automatique de relations | Une relation nouvelle modifie le sens du graphe documentaire et doit etre relue. |
| Creation automatique d'une source canonique | Ajouter une source dans `data/registre.json` releve de l'integration documentaire, pas d'une correction implicite. |
| Correction silencieuse des registres | Toute modification doit etre visible dans un diff et rattachee a une intention. |
| Suppression automatique de donnees | La suppression peut effacer une preuve, un legacy ou une reserve utile. |

La pre-validation peut recommander une action. Elle ne doit pas l'executer sans workflow explicite.

## 7. Sortie attendue

Un futur systeme de pre-validation doit produire une sortie lisible avant ouverture de PR.

Sortie minimale attendue :

- resume de la proposition ;
- type d'enrichissement : ajout unitaire ou integration documentaire ;
- type d'objet ou familles concernees ;
- fichiers concernes ;
- sources declarees ;
- relations declarees ;
- erreurs bloquantes ;
- reserves ;
- informations ;
- controles existants a executer ;
- artefacts generes a regenerer ou a verifier ;
- arbitrages humains restants ;
- decision de pre-validation.

Format logique recommande :

```text
Decision de pre-validation : pre-validee | pre-validee avec reserve | non pre-validee

Resume :
- ...

Bloquants :
- ...

Reserves :
- ...

Informations :
- ...

Fichiers concernes :
- ...

Controles a executer :
- ...

Arbitrages humains :
- ...
```

Cette sortie doit rester deterministe pour une meme proposition. Elle ne doit pas contenir de date dynamique obligatoire.

## 8. Articulation avec M1

M1 fournit des controles P0 sur les documents maitres :

- `DM -> atomes`, via `tools/check_dm_atoms_traceability.py` ;
- `DM -> registres`, via `tools/check_dm_registers_consistency.py` ;
- `DM -> sources`, via `tools/check_dm_sources_consistency.py` ;
- agregation minimale, via `tools/aggregate_m1.py` et `reports/m1/status_m1.md`.

La pre-validation M2 intervient avant la PR. Elle verifie qu'une proposition d'enrichissement est recevable localement : identifiants, sources, champs, relations, collisions, artefacts et limites.

Les controles M1 interviennent lorsque les documents maitres, rapports M1 ou relations DM sont affectes. Ils restent des controles executables et agregeables. La pre-validation ne recalcule pas leurs diagnostics et ne remplace pas leurs rapports.

Repartition :

| Sujet | Pre-validation M2 | Controles M1 |
| --- | --- | --- |
| Source `Sxx` declaree dans une proposition | Verifie que la source existe dans `data/registre.json`. | Verifie les sources visibles dans les documents maitres contre `data/registre.json`. |
| Atome reference dans une proposition | Verifie que l'identifiant est resoluble si l'artefact existe. | Verifie les atomes visibles dans les documents maitres. |
| Identifiant de registre reference dans une proposition | Verifie que l'objet cible existe ou que la relation est signalee comme reserve. | Verifie les identifiants P0 visibles dans les documents maitres. |
| Document maitre modifie | Signale que les controles M1 doivent etre lances. | Produit les rapports M1 et le status consolide. |
| Rapport M1 absent, illisible ou non conforme | Signale un bloquant si la PR affecte M1. | L'agregateur M1 statue selon ses regles propres. |

La pre-validation ne doit pas ouvrir un nouveau controle M1, modifier l'agregateur ou changer les seuils existants.

## 9. Risques

### Risques techniques

- transformer le contrat en validateur implicite sans implementation ;
- supposer qu'un schema lisible est toujours gateable ;
- utiliser un outil existant pour un perimetre qu'il ne couvre pas ;
- oublier de regenerer ou committer les artefacts produits par le pipeline ;
- classer un bloquant comme reserve pour faciliter une PR ;
- produire une sortie non deterministe ou dependante d'un etat externe non documente.

### Risques documentaires

- confondre source canonique, URL, provenance, droit et identifiant interne ;
- creer des doublons faute de recherche d'alias ;
- masquer une incertitude d'attribution ;
- rendre invisible une collision de lieu, concert, image ou citation ;
- transformer une absence de validateur en validation implicite ;
- laisser une source inconnue dans un champ `sources`.

### Risques de gouvernance

- contourner la validation humaine ;
- ouvrir une PR avec des bloquants connus ;
- merger automatiquement une proposition pre-validee ;
- faire de la pre-validation une validation historiographique ;
- modifier M1, les schemas ou les exports pour satisfaire un cas ponctuel ;
- lancer une interface ou un formulaire avant stabilisation du contrat.

## 10. Decision proposee

Decision proposee :

La version minimale de la pre-validation commune M2.2 est definie comme une couche de verification documentaire avant PR, commune aux ajouts unitaires et aux integrations documentaires, qui classe les constats en `bloquant`, `reserve` ou `information`.

Cette version minimale est suffisante avant toute interface ou formulaire si elle respecte les conditions suivantes :

- aucune creation de script ou validateur nouveau ;
- aucune modification des schemas, controles M1 ou exports ;
- appui exclusif sur l'etat reel du depot ;
- identification claire des outils existants et de leurs limites ;
- refus des identifiants dupliques, sources inconnues, schemas incompatibles et relations requises introuvables ;
- exposition explicite des reserves et arbitrages humains ;
- conservation du principe : le studio prepare, l'humain valide.

Une proposition d'enrichissement peut devenir une Pull Request seulement si la pre-validation ne contient aucun bloquant et si les reserves restantes sont documentees dans la PR.
