# M2.6.1 - Retour d'usage du prototype ORG

## 1. Objet du retour d'usage

Ce document evalue le comportement reel du prototype CLI d'ajout `ORG`, implemente dans `tools/m2_add_org.py`, apres le cadrage fonctionnel `docs/m2-prototype-ajout-org.md`.

Le role du prototype est de preparer l'ajout d'une organisation canonique sans modifier le depot. Il lit le registre canonique `registers/orgs/orgs.json`, le registre des sources `data/registre.json` et le schema `schemas/organization_canonical.schema.json`, puis produit une proposition d'entree candidate.

Perimetre couvert :

- proposition du prochain identifiant `ORG-NNNN` ;
- preparation d'une entree candidate JSON ;
- verification des sources ;
- verification de la categorie, du pays, du statut, du gate et de la relation Joy Division minimale ;
- detection des collisions de nom, d'alias et de Wikidata ;
- classification en `bloquant`, `reserve` et `information`.

Limites :

- aucune ecriture dans `registers/orgs/orgs.json` ;
- aucune modification de schema, registre, export ou validateur ;
- aucune ouverture automatique de branche, commit ou PR ;
- aucune decision historiographique automatique ;
- aucune generalisation a une autre famille documentaire.

Le prototype prepare. L'humain valide.

## 2. Cas d'essai realises

Les essais ci-dessous ont ete executes avec le prototype courant. Le registre ORG contient `ORG-0001` a `ORG-0008`, donc l'identifiant propose observe est `ORG-0009`.

| Cas | Commande resumee | Decision observee | Constats |
| --- | --- | --- | --- |
| Cas conforme | `--name "Durutti Column Archive" --category institution --country GB --jd-relation archive --sources S21 --last-verified 2026-06-01` | `pre-validee` | Aucun bloquant, aucune reserve. Le prototype propose `ORG-0009`, cible `registers/orgs/orgs.json` et confirme la lecture seule. |
| Source inconnue | meme entree avec `--sources S999` | `non pre-validee` | Bloquant unique observe : `source inconnue: S999`. |
| Categorie invalide | meme entree avec `--category publisher` | `non pre-validee` | Bloquant observe : `categorie invalide: publisher`. Le message liste les categories autorisees. |
| Pays invalide | meme entree avec `--country FRA` | `non pre-validee` | Bloquant observe : `pays invalide: FRA (format attendu: ISO alpha-2)`. |
| Collision stricte | `--name "Buzzcocks" --category group --country GB --jd-relation peer_group --sources S76 --last-verified 2026-06-01` | `non pre-validee` | Bloquant observe : `collision certaine de nom: Buzzcocks deja present dans ORG-0001`. |
| Organisation proche | `--name "Buzzcock" --category group --country GB --jd-relation peer_group --sources S76 --last-verified 2026-06-01` | `pre-validee avec reserve` | Reserve observee : `organisation proche a arbitrer: Buzzcock ~ Buzzcocks (ORG-0001)`. |
| Alias ambigu | `--name "New Archive Org" --aliases "The Buzzcock" --category institution --country GB --jd-relation archive --sources S21 --last-verified 2026-06-01` | `pre-validee avec reserve` | Reserve observee : `alias proche d'un alias existant a arbitrer: The Buzzcock ~ The Buzzcocks (ORG-0001)`. |
| Relation absente | meme entree conforme avec `--jd-relation ""` | `non pre-validee` | Bloquants observes : `relation Joy Division absente` et `schema invalide: Field must be non-empty: joy_division_relation.type`. |
| Wikidata duplique | entree conforme avec `--wikidata Q485898` | `non pre-validee` | Bloquant observe : `wikidata deja utilise: Q485898 dans ORG-0001`. |

Le prototype supporte donc des cas conformes, des refus explicites et des reserves. Il ne produit pas aujourd'hui de reserve pour une relation Joy Division vague mais non vide : seule l'absence de relation est bloquante.

## 3. Ergonomie

La commande est comprehensible pour un usage technique local. Les parametres obligatoires sont explicites : `--name`, `--category`, `--country`, `--jd-relation`, `--sources` et `--last-verified`.

Points positifs observes :

- `--help` liste les categories, statuts et gates autorises ;
- les messages source, categorie, pays et collision sont courts ;
- les erreurs de categorie et de pays evitent une duplication excessive avec le schema ;
- la sortie affiche toujours la decision, les bloquants, les reserves, les informations et l'entree candidate ;
- la cible d'ecriture probable est visible sans declencher d'ecriture.

Points moins confortables observes :

- `--last-verified` impose une date explicite, ce qui est conforme au determinisme mais ajoute une contrainte d'usage ;
- la relation vide produit deux diagnostics pour une meme cause : le bloquant metier et le bloquant de schema ;
- la sortie JSON complete est utile pour relecture, mais longue pour un simple diagnostic rapide.

Dans l'ensemble, l'ergonomie est suffisante pour un prototype CLI de preparation, a condition de rester dans un usage expert ou semi-expert.

## 4. Valeur documentaire

Par rapport a un ajout manuel, le prototype apporte une valeur documentaire nette.

Gains :

- propose automatiquement le prochain identifiant `ORG-0009` a partir du registre reel ;
- evite l'oubli des champs obligatoires du schema ;
- force la declaration d'au moins une source ;
- verifie l'existence des sources dans `data/registre.json` ;
- signale les collisions evidentes avant toute modification du registre ;
- detecte les proximites de nom ou d'alias comme reserves plutot que de les accepter silencieusement ;
- bloque un Wikidata deja utilise, ce que le validateur canonique refuserait ensuite ;
- produit une entree candidate directement relisible.

Limites :

- l'utilisateur doit deja connaitre la categorie documentaire adequate ;
- le prototype ne qualifie pas la solidite historiographique de la source ;
- il ne decide pas si la relation Joy Division fournie est suffisamment precise, sauf lorsqu'elle est vide ;
- il ne remplace pas la relecture humaine de l'entree candidate.

Risques evites :

- doublon `ORG-` ;
- source inexistante ;
- categorie hors schema ;
- pays non conforme au format attendu ;
- collision stricte de nom ou d'alias ;
- Wikidata duplique.

## 5. Qualite des controles

### Sources

Le controle fonctionne. Une source connue comme `S21` permet la pre-validation ; une source inconnue comme `S999` bloque l'ajout. Le prototype verifie aussi le format `Sxx`.

Reste a demontrer : le controle ne juge pas si la source mobilisee est la meilleure ou si elle documente vraiment l'organisation proposee. Cette evaluation reste humaine.

### Categories

Le controle fonctionne. Une categorie hors vocabulaire comme `publisher` est bloquante, avec rappel du vocabulaire autorise :

- `group`
- `label`
- `institution`
- `venue_org`
- `crew`
- `media`
- `other`

Reste a demontrer : le prototype ne sait pas arbitrer une categorie techniquement valide mais historiographiquement discutable.

### Pays

Le controle fonctionne pour le format. `GB` est accepte ; `FRA` est refuse car le prototype attend un code ISO alpha-2.

Reste a demontrer : le prototype ne verifie pas la validite geographique complete du code ni la coherence documentaire du pays choisi.

### Relation Joy Division

Le controle minimal fonctionne. Une relation non vide comme `archive` est acceptee ; une relation vide est bloquante.

Limite observee : le prototype ne produit pas de reserve pour une relation vague, trop large ou insuffisamment justifiee. Il controle l'existence minimale de la relation, pas sa qualite documentaire.

### Collisions

Le controle fonctionne sur plusieurs niveaux :

- collision stricte de nom : bloquante ;
- nom proche : reserve ;
- alias proche d'un alias existant : reserve.

Le comportement est adapte au retour d'usage attendu : une ambiguite n'est ni acceptee silencieusement, ni refusee systematiquement.

### Wikidata

Le controle fonctionne. Un identifiant Wikidata deja present dans le registre, par exemple `Q485898`, est bloquant.

Ce point est important car `tools/validate_orgs.py` rejette aussi les doublons Wikidata. Le prototype evite donc de produire une proposition qui echouerait ensuite au validateur canonique.

## 6. Limites observees

Limites reellement observees :

- la relation Joy Division vide produit deux diagnostics proches ;
- une relation non vide mais vague n'est pas classee en reserve ;
- les categories valides mais discutables ne sont pas arbitrees ;
- la sortie est volontairement complete, donc assez longue ;
- le prototype reste strictement en lecture seule et ne prepare pas encore une PR.

Ces limites sont coherentes avec le perimetre du prototype. Elles ne bloquent pas l'usage comme outil de preparation, mais elles doivent etre connues avant toute generalisation.

## 7. Decision

Le prototype ORG est-il suffisamment stable pour servir de second cas valide de M2 ?

oui

Justification :

- le cas conforme est pre-valide ;
- les bloquants attendus sont bien detectes ;
- les reserves de proximite nom/alias sont exercees ;
- le controle Wikidata couvre un invariant canonique important ;
- la sortie reste deterministe et en lecture seule ;
- le prototype respecte les contrats M2.1, M2.2 et M2.4.

La stabilite est suffisante pour valider ORG comme second cas M2, sans conclure encore a une generalisation automatique du modele.

## 8. Recommandation

Suite recommandee :

bilan de genericite M2

Justification :

PERSON et ORG disposent maintenant chacun d'un cycle documentaire et technique suffisant pour comparer les invariants communs et les divergences utiles :

- identifiant canonique ;
- sources obligatoires ;
- collisions strictes ;
- reserves d'ambiguite ;
- sortie lecture seule ;
- compatibilite schema ;
- validation humaine conservee.

Il est preferable de produire un bilan de genericite avant d'ouvrir une nouvelle famille documentaire. Cela permettra de distinguer ce qui peut devenir commun a M2 de ce qui doit rester specifique a chaque type.

Il n'est donc pas recommande d'ouvrir immediatement un troisieme prototype documentaire.
