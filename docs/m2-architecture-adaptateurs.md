# M2.8 - Architecture moteur commun et adaptateurs

## 1. Objet de l'architecture

Ce document definit l'architecture cible logique du Studio M2 apres les deux
prototypes effectivement implementes et evalues : `PERSON` et `ORG`.

Il ne cree aucun code, aucun nouveau prototype, aucun registre, aucun schema et
aucun validateur. Il fixe un cadre avant toute refactorisation ou ouverture
d'une nouvelle famille documentaire.

### Moteur commun M2

Le moteur commun M2 designe la couche generique qui pourrait porter les
invariants deja observes dans les prototypes `PERSON` et `ORG` :

- classification des constats ;
- decision de pre-validation ;
- rendu CLI commun ;
- verification des sources canoniques `Sxx` ;
- sortie deterministe ;
- format general des diagnostics ;
- code de sortie ;
- aide generique ;
- socle minimal de tests.

Le moteur commun ne doit pas connaitre le metier propre a une famille
documentaire. Il ne doit pas savoir ce qu'est une fusion de personnes, une
relation Joy Division, un `PERS-*`, un Wikidata ou une couche concert.

### Adaptateur par famille documentaire

Un adaptateur par famille documentaire designe la couche specifique qui traduit
un type reel du depot vers les invariants M2.

Chaque adaptateur conserve :

- la strategie d'identifiant ;
- les champs requis ;
- les vocabulaires fermes ;
- le schema et le validateur ;
- les relations minimales ;
- les collisions utiles ;
- les reserves documentaires ;
- la cible d'ecriture probable ;
- le rendu de l'entree candidate.

L'adaptateur protege le sens documentaire du type. Le moteur commun organise la
pre-validation. Les deux roles ne doivent pas etre confondus.

### Pourquoi maintenant

Cette architecture intervient apres `PERSON` et `ORG` parce que M2 dispose de
deux cycles complets :

```text
specification
  ->
implementation
  ->
tests
  ->
retour d'usage
  ->
stabilisation
```

Avant `ORG`, toute genericite aurait ete deduite d'une seule famille. Apres
`ORG`, le depot montre un noyau commun reel, mais aussi des divergences fortes.

La conclusion de `docs/m2-bilan-genericite.md` reste la reference : M2 doit
poursuivre par une reflexion d'architecture, sans implementation immediate et
sans ouvrir une troisieme famille documentaire.

## 2. Ce que le moteur commun peut gerer

Le moteur commun peut prendre en charge uniquement les invariants observes dans
`tools/m2_add_person.py`, `tools/m2_add_org.py` et leurs tests.

| Responsabilite commune | Comportement observe |
| --- | --- |
| Classification | Les deux prototypes classent les constats en `bloquant`, `reserve` et `information`. |
| Decision | Les deux prototypes produisent `non pre-validee`, `pre-validee avec reserve` ou `pre-validee`. |
| Rendu CLI | Les deux sorties affichent decision, identifiant propose, bloquants, reserves, informations et entree candidate. |
| Source `Sxx` | Les deux prototypes verifient les sources contre `data/registre.json`. |
| Sortie deterministe | Les tests comparent deux rendus identiques produits par la meme entree. |
| Diagnostics | Les deux prototypes produisent des messages courts, deduplicables et classes. |
| Code de sortie | Les deux CLI retournent un code non nul lorsqu'il existe au moins un bloquant. |
| Aide generique | Les deux `--help` exposent le role du prototype et les vocabulaires utiles. |
| Tests minimaux | Les deux suites couvrent cas conforme, source inconnue, collision, reserve, aide et determinisme. |
| Lecture seule | Les deux prototypes lisent le depot et impriment une proposition sans modifier de fichier. |

Le moteur commun peut donc porter un vocabulaire de pre-validation et une
structure de sortie. Il peut aussi fournir des primitives techniques simples :

- chargement des sources canoniques depuis `data/registre.json` ;
- deduplication des diagnostics ;
- calcul de la decision depuis les listes de constats ;
- rendu des listes vides sous la forme `- aucun` ;
- controle du code de retour CLI ;
- format de test de determinisme ;
- aide commune indiquant que le prototype est en lecture seule.

Le moteur commun ne doit pas contenir de logique metier `PERSON` ou `ORG`.

Il ne doit donc pas gerer :

- le format `PERSON-<slug>` ;
- le format `ORG-NNNN` ;
- `same_as` vers `PERS-*` ;
- `joy_division_relation` ;
- Wikidata ;
- les categories `PERSON` ou `ORG` ;
- les schemas de chaque famille ;
- les decisions de collision propres a une famille.

## 3. Ce que les adaptateurs doivent gerer

Les adaptateurs restent responsables de tout ce qui depend du modele reel de la
famille documentaire.

| Responsabilite specifique | `PERSON` observe | `ORG` observe |
| --- | --- | --- |
| Format d'identifiant | `PERSON-<slug>` derive du nom. | `ORG-NNNN`, prochain numero calcule depuis `registers/orgs/orgs.json`. |
| Proposition d'identifiant | Slugification du nom canonique. | Plus grand numero existant + 1. |
| Format candidat | YAML. | JSON. |
| Schema | `schemas/person_canonical.schema.json`. | `schemas/organization_canonical.schema.json`. |
| Validateur canonique | `tools/validate_people.py`. | `tools/validate_orgs.py`. |
| Champs requis | `id`, `type_unite`, `name`, `categorie`, `role`, `sources`, `same_as`, `alt_names`, `categorie_a_arbitrer`, `a_arbitrer`. | `org_id`, `canonical_name`, `aliases`, `category`, `country`, `status`, `same_as`, `joy_division_relation`, `sources`, `identity_frozen`, `drift_sentinel`, `gate`, `last_verified`. |
| Vocabulaire ferme | Categories `membre`, `entourage`, `industrie`, `critique_journaliste`, `auteur_secondaire`, `influence`, `theoricien_mobilise`. | Categories `group`, `label`, `institution`, `venue_org`, `crew`, `media`, `other`; statuts et gates. |
| Relations | `same_as` vers `PERS-*`, origine `auteur_source`. | `joy_division_relation`, identifiants externes et provenance. |
| Collisions | Identifiant, nom, alias, `same_as` deja rattache, auteur-source. | Identifiant, nom, alias, Wikidata duplique. |
| Reserves | Identite a arbitrer, categorie a arbitrer, nom ou alias proche. | Organisation proche, alias proche. |
| Cible d'ecriture | `registers/people/*.md` puis regeneration, ou pipeline d'attribution, ou cible non identifiable. | `registers/orgs/orgs.json`. |
| Artefacts candidats | Entree YAML `PERSON`. | Entree JSON `ORG`. |

Un adaptateur doit donc connaitre la famille qu'il sert. Il doit refuser les
entrees formellement invalides, exposer les reserves et produire une entree
candidate compatible avec les schemas et validateurs existants.

## 4. Contrat minimal d'un adaptateur

Ce contrat est documentaire et technique. Il decrit ce qu'un adaptateur doit
fournir, sans figer une API Python.

Un adaptateur M2 minimal doit documenter ou fournir les elements suivants.

| Element | Role attendu |
| --- | --- |
| `family_name` | Nom stable de la famille documentaire, par exemple `PERSON` ou `ORG`. |
| `id_strategy` | Methode de proposition et verification d'identifiant. |
| `required_fields` | Champs obligatoires issus du schema ou du validateur reel. |
| `allowed_values` | Vocabulaires fermes utiles a l'aide CLI et aux erreurs. |
| `source_fields` | Champs qui attendent des sources canoniques `Sxx`. |
| `schema_validation` | Schema, validateur ou verification locale applicable. |
| `collision_checks` | Collisions strictes et proximites a rechercher. |
| `relation_checks` | Relations minimales a verifier et relations interdites. |
| `candidate_renderer` | Format de rendu de l'entree candidate : YAML, JSON ou autre format reel. |
| `write_target_hint` | Cible d'ecriture probable ou raison de l'absence de cible identifiable. |
| `test_cases` | Cas minimaux : conforme, source inconnue, categorie ou champ invalide, collision, reserve, aide, determinisme. |

Le contrat impose aussi des garanties :

- lecture seule par defaut ;
- aucun commit, merge ou push automatique ;
- aucune correction silencieuse ;
- aucun ajout de source canonique implicite ;
- aucun contournement des validateurs existants ;
- diagnostic explicite pour tout bloquant ou reserve ;
- sortie deterministe.

Le moteur commun peut exiger ces garanties. L'adaptateur decide comment les
honorer pour sa famille.

## 5. Ce qui ne doit jamais etre mutualise

Les points suivants ne doivent pas etre portes par le moteur commun, meme si
plusieurs familles semblent les utiliser.

| Point non mutualisable | Raison |
| --- | --- |
| Interpretation historiographique | Le moteur ne peut pas decider de la solidite d'une lecture historique. |
| Arbitrage de droits | Les droits d'image, citation ou reproduction exigent une decision humaine. |
| Fusion d'identites | Fusionner personnes, organisations, lieux ou objets peut detruire une nuance documentaire. |
| Creation de relation | Une relation nouvelle modifie le graphe documentaire et doit rester explicite. |
| Relation Joy Division | `joy_division_relation` est propre au modele `ORG` observe. |
| `same_as` | La structure et le sens different entre `PERSON` et `ORG`. |
| `PERS-*` | Les rattachements provisoires sont specifiques au pipeline people. |
| `CONCERT-*` et `JD-CONCERT-*` | La coexistence de couches concert exige une doctrine propre. |
| Niveaux session/image | `IMAGE-S-*` et `IMAGE-I-*` portent des contraintes qui ne sont pas observees dans PERSON/ORG. |
| Citations longues | Les questions de verbatim, droits et attribution ne sont pas un rendu CLI generique. |
| Decisions de merge | Le Studio M2 prepare ; la validation humaine decide. |

Le moteur commun peut afficher qu'une reserve existe. Il ne doit pas trancher la
reserve.

## 6. Architecture cible logique

L'architecture cible logique est une separation en trois couches.

```text
entree utilisateur
  |
  v
adaptateur de famille
  |
  |-- construit l'entree candidate
  |-- propose l'identifiant
  |-- applique les controles metier
  |-- expose les reserves documentaires
  v
moteur commun M2
  |
  |-- classe bloquants / reserves / informations
  |-- calcule la decision
  |-- rend la sortie CLI
  |-- gere le code de sortie
  |-- garantit le format deterministe
  v
sortie relisible
  |
  v
validation humaine puis PR eventuelle
```

Vue par composants :

```text
moteur commun M2
  |
  |-- adaptateur PERSON
  |     |-- schema PERSON
  |     |-- registres people
  |     |-- PERS-* et same_as
  |
  |-- adaptateur ORG
  |     |-- schema ORG
  |     |-- registers/orgs/orgs.json
  |     |-- joy_division_relation
  |
  |-- adaptateur futur, seulement apres decision
```

Le flux reste celui de M2 :

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

Cette architecture ne remplace pas M2.4. Elle prepare une PR relisible, mais ne
l'ouvre pas automatiquement et ne la merge jamais.

## 7. Conditions de refactorisation

Faut-il refactoriser les prototypes `PERSON` et `ORG` vers cette architecture
immediatement ?

Non.

La refactorisation ne doit etre ouverte que si les conditions suivantes sont
reunies :

| Condition | Exigence |
| --- | --- |
| Contrat d'adaptateur valide | Le contrat minimal ci-dessus est accepte comme doctrine M2. |
| Tests de non-regression | Les tests `tools/test_m2_add_person.py` et `tools/test_m2_add_org.py` passent avant et apres refactorisation. |
| Sortie identique ou documentee | Toute variation de sortie CLI est soit identique, soit explicitement justifiee et relue. |
| Aucun diagnostic perdu | Les bloquants, reserves et informations actuellement observes restent visibles. |
| Aucun nouveau type dans la meme PR | La refactorisation ne doit pas ouvrir `PLACE`, `IMAGE`, `CONCERT`, `RELEASE` ou `CITATION`. |
| Lecture seule conservee | Aucun fichier de registre, schema, export ou validateur n'est modifie par le moteur. |
| Perimetre limite | La PR de refactorisation doit porter sur la structure interne, pas sur une nouvelle doctrine documentaire. |

Une refactorisation acceptable serait donc une extraction prudente de primitives
communes deja observees : `CheckResult`, calcul de decision, rendu de listes,
chargement des sources, deduplication des diagnostics, code de sortie et tests
de determinisme.

Elle ne devrait pas extraire les collisions, identifiants, relations ou
candidats metier.

## 8. Conditions d'ouverture d'une nouvelle famille

Une nouvelle famille documentaire ne doit etre ouverte qu'apres validation des
criteres suivants.

| Critere | Question a verifier |
| --- | --- |
| Schema ou modele reel | Le depot possede-t-il un schema, un validateur ou un modele documentaire suffisamment explicite ? |
| Source canonique | La famille sait-elle distinguer source `Sxx`, URL, provenance et identifiant interne ? |
| Identifiant stable | Le format d'identifiant et la strategie de proposition sont-ils definis ? |
| Champs requis | Les champs minimaux sont-ils connus sans inventer de nouvelles obligations ? |
| Relations minimales | Les relations obligatoires sont-elles identifiables et verifiables ? |
| Collisions utiles | Les doublons stricts et ambiguites probables peuvent-ils etre recherches ? |
| Reserves pertinentes | Le type possede-t-il des cas de reserve non artificiels ? |
| Validateur existant | Les commandes de verification existantes sont-elles identifiees, ou l'absence de validateur est-elle documentee ? |
| Cible d'ecriture | Le fichier ou pipeline probable est-il connu ? |
| Dette de gouvernance | L'ouverture ne contourne-t-elle pas M2.1, M2.2 et M2.4 ? |

Application aux familles citees par M2 :

| Famille | Condition particuliere avant ouverture |
| --- | --- |
| `PLACE` | Clarifier lieux physiques, `PLACE-*`, coordonnees, `same_as`, collisions de libelles et validateur places. |
| `IMAGE` | Clarifier droits, provenance, photographe, sujets, niveaux session/image et sources. |
| `CONCERT` | Clarifier la coexistence `CONCERT-*` et `JD-CONCERT-*`, date, lieu et reconciliation. |
| `RELEASE` | Clarifier l'absence de validateur gateable dedie aux occurrences discographiques. |
| `CITATION` | Clarifier texte, droits, locuteur, source, page et limites du verbatim. |

Ces conditions ne ferment aucune famille. Elles empechent seulement d'ouvrir un
prototype sans base documentaire suffisante.

## 9. Risques

### Risques techniques

- creer une couche commune plus complexe que les deux prototypes actuels ;
- rigidifier trop tot une API interne ;
- rendre les tests plus abstraits et moins lisibles ;
- perdre des diagnostics utiles pendant une extraction ;
- produire une sortie commune qui masque les differences YAML / JSON.

### Risques documentaires

- confondre source, provenance, relation et identifiant externe ;
- transformer une reserve specifique en message generique trop faible ;
- creer des candidats formellement corrects mais pauvres au fond ;
- gommer la difference entre ajout unitaire et integration documentaire.

### Risques de gouvernance

- presenter une pre-validation comme une validation humaine ;
- ouvrir une nouvelle famille dans une PR de refactorisation ;
- automatiser une PR avant d'avoir stabilise les reserves ;
- encourager un merge automatique contraire a M2 ;
- contourner les controles M1 ou les validateurs existants.

## 10. Decision proposee

Faut-il refactoriser maintenant ?

Non.

Decision :

M2 doit adopter l'orientation `moteur commun + adaptateurs par famille` comme
architecture cible logique, sans refactorisation immediate.

Prochaine etape recommandee :

Stabiliser ce contrat d'adaptateurs par revue documentaire, puis ouvrir
separement une PR de refactorisation limitee si le projet veut reduire la
duplication entre `PERSON` et `ORG`.

Cette future PR, si elle est ouverte, devra :

- ne modifier aucun comportement documentaire ;
- conserver les sorties ou documenter explicitement les ecarts ;
- garder les tests `PERSON` et `ORG` comme filet de non-regression ;
- ne pas creer de prototype `PLACE`, `IMAGE`, `CONCERT`, `RELEASE` ou
  `CITATION` dans le meme changement.

Orientation principale retenue :

Formaliser l'architecture d'adaptateurs avant toute nouvelle famille
documentaire et avant toute generalisation executable.
