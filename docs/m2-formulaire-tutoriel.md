# M2 - Tutoriel d'utilisation du formulaire

## 1. A quoi sert le formulaire M2 ?

Le formulaire M2 sert a preparer des enrichissements documentaires sans
commencer par ecrire une commande a la main.

Il aide a saisir :

- une personne candidate ;
- une organisation candidate ;
- un lieu documentaire candidat ;
- une image ou seance iconographique candidate ;
- une source longue candidate ;
- une petite campagne batch avec plusieurs personnes, organisations, lieux et images.

Le formulaire produit :

- une commande CLI copiable ;
- ou un JSON batch copiable.

Il ne produit pas une validation documentaire.

Il ne modifie aucun registre.

Il ne cree pas de personne, d'organisation, de source canonique, d'atome, de
citation ou de relation.

Principe M2 :

```text
Le studio prepare. L'humain valide.
```

Le formulaire est donc une aide a la saisie. Les diagnostics sont produits
ensuite par les outils M2 en ligne de commande.

Dans l'interface `apps/m2-formulaire/index.html`, le bloc `Mode d'emploi`
resume ce parcours et renvoie vers ce tutoriel complet.

## 2. Vue generale du workflow

Le workflow habituel est :

```text
Formulaire
  ->
Commande ou JSON
  ->
CLI M2
  ->
Diagnostic
  ->
Resume PR
  ->
Validation humaine
```

Etapes :

1. Ouvrir le formulaire dans `apps/m2-formulaire/`.
2. Lire le bloc `Mode d'emploi` si le parcours n'est pas encore familier.
3. Choisir l'onglet correspondant au besoin : `PERSON`, `ORG`, `PLACE`, `IMAGE`,
   `SOURCE LONGUE` ou `BATCH`.
4. Remplir les champs utiles.
5. Copier la commande ou le JSON genere.
6. Executer la commande dans le depot.
7. Lire le diagnostic.
8. Lire le resume PR genere dans `exports/generated/`.
9. Soumettre la proposition a revue humaine.

Le formulaire s'arrete a l'etape de preparation. La CLI M2 produit le diagnostic
et le resume. L'humain decide ensuite.

## 3. Premier ajout PERSON

### Saisie dans le formulaire

Ouvrir l'onglet `PERSON`.

Exemple de saisie :

```text
name: Prototype Person
category: industrie
roles: producteur
sources: S41
notes: rattachement a verifier en revue
```

Les champs importants sont :

- `name` : nom de la personne candidate ;
- `category` : categorie documentaire PERSON ;
- `roles` : un ou plusieurs roles separes par des virgules ;
- `sources` : sources `Sxx` separees par des virgules ;
- `notes` : prudence ou contexte a garder visible.

### Commande generee

Le formulaire produit une commande du type :

```bash
python3 tools/m2_add_person.py --name 'Prototype Person' --category 'industrie' --role 'producteur' --sources 'S41' --note 'rattachement a verifier en revue' --pr-summary
```

### Execution

Copier la commande et l'executer depuis la racine du depot.

La CLI affiche un diagnostic.

Exemple de structure attendue :

```text
Decision : pre-validee
Identifiant propose : PERSON-prototype-person
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- ...
Entree candidate :
- bloc YAML de la proposition
```

Si une source est inconnue, si la categorie est invalide ou si une collision est
detectee, la decision peut devenir `non pre-validee`.

### Resume PR obtenu

Avec `--pr-summary`, un fichier Markdown est genere dans :

```text
exports/generated/pr_summary_person_*.md
```

Ce resume sert a preparer la revue humaine. Il ne cree pas de PR GitHub.

## 4. Premier ajout ORG

### Saisie dans le formulaire

Ouvrir l'onglet `ORG`.

Exemple de saisie :

```text
name: Prototype Organisation
category: label
country: GB
jd_relation: label_mate
sources: S41
last_verified: 2026-06-06
notes: relation documentaire a confirmer
```

Les champs importants sont :

- `name` : nom canonique propose ;
- `category` : categorie ORG ;
- `country` : code pays ;
- `jd_relation` : relation documentee avec Joy Division ;
- `sources` : sources `Sxx` ;
- `last_verified` : date de verification humaine explicite ;
- `notes` : commentaire de relation ou prudence.

### Commande generee

Le formulaire produit une commande du type :

```bash
python3 tools/m2_add_org.py --name 'Prototype Organisation' --category 'label' --country 'GB' --jd-relation 'label_mate' --sources 'S41' --last-verified '2026-06-06' --relation-notes 'relation documentaire a confirmer' --pr-summary
```

### Execution et resultat

La CLI ORG propose le prochain identifiant `ORG-NNNN` disponible, puis affiche
le diagnostic.

Exemple de structure attendue :

```text
Decision : pre-validee
Identifiant propose : ORG-0009
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- prochain numero disponible detecte: ORG-0009
- cible d'ecriture probable: registers/orgs/orgs.json
```

Le numero exact peut varier selon l'etat du registre au moment de l'execution.

### Resume PR obtenu

Avec `--pr-summary`, un fichier Markdown est genere dans :

```text
exports/generated/pr_summary_org_*.md
```

Ce resume expose les validations, les reserves eventuelles et les arbitrages
humains attendus.

## 5. Premier ajout PLACE

### Saisie dans le formulaire

Ouvrir l'onglet `PLACE`.

Exemple de saisie :

```text
label: Prototype Venue
type: salle
type_detail: club
sources: S41
aliases: Prototype Club
usage: concert
prudence: verifier la distinction avec le batiment voisin
```

Les champs importants sont :

- `label` : label canonique propose pour le lieu ;
- `type` : type PLACE, par exemple `salle`, `studio`, `quartier` ou
  `lieu_memoire` ;
- `type_detail` : precision libre utile a la revue ;
- `sources` : sources `Sxx` ;
- `aliases` : noms alternatifs utilises pour le diagnostic ;
- `usage` : usage documentaire attendu ;
- `prudence` : note visible pour la revue.

### Commande generee

Le formulaire produit une commande du type :

```bash
python3 tools/m2_add_place.py --label 'Prototype Venue' --type 'salle' --sources 'S41' --aliases 'Prototype Club' --type-detail 'club' --usage 'concert' --prudence 'verifier la distinction avec le batiment voisin' --pr-summary
```

### Execution et resultat

La CLI PLACE propose un identifiant `PLACE-<SLUG>`, puis affiche le diagnostic.

Exemple de structure attendue :

```text
Decision : pre-validee
Identifiant propose : PLACE-PROTOTYPE-VENUE
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- cible d'ecriture probable: registers/places/*.md
- lecture seule: aucune modification du registre PLACE
```

Une collision exacte avec un lieu existant bloque la pre-validation. Une
proximite de label ou d'alias devient une reserve a lire humainement.

### Resume PR obtenu

Avec `--pr-summary`, un fichier Markdown est genere dans :

```text
exports/generated/pr_summary_place_*.md
```

Ce resume expose le lieu propose, les validations executees, les reserves et
les arbitrages humains attendus. Il ne modifie aucun registre.

## 6. Premier ajout IMAGE

### Saisie dans le formulaire

Ouvrir l'onglet `IMAGE`.

Exemple de saisie :

```text
level: session
name: Prototype Image Session
photographer: PERSON-kevin-cummins
sources: S41
date: 1979-02
date_precision: month
context: promo
subjects: PERSON-ian-curtis
place: PLACE-HULME
last_verified: 2026-06-06
notes: droits et provenance a confirmer en revue
```

Les champs importants sont :

- `level` : `session` pour une seance, `image` pour un cliche individuel ;
- `name` : designation canonique proposee ;
- `photographer` : identifiant `PERSON-*` du photographe ou auteur visuel ;
- `sources` : sources `Sxx` documentant l'objet ;
- `date` et `date_precision` : date ou periode disponible ;
- `subjects` : sujets visibles, en `PERSON-*` ou descriptions libres ;
- `session_ref` : session parente obligatoire pour `level=image` ;
- `place` : lieu `PLACE-*` ou description libre ;
- `last_verified` : date explicite de verification humaine ;
- `notes` : droits, provenance, attribution ou prudence.

### Commande generee

Le formulaire produit une commande du type :

```bash
python3 tools/m2_add_image.py --level 'session' --name 'Prototype Image Session' --photographer 'PERSON-kevin-cummins' --sources 'S41' --last-verified '2026-06-06' --date '1979-02' --date-precision 'month' --context 'promo' --subjects 'PERSON-ian-curtis' --place 'PLACE-HULME' --notes 'droits et provenance a confirmer en revue' --pr-summary
```

### Execution et resultat

La CLI IMAGE propose le prochain identifiant `IMAGE-S-NNNN` ou `IMAGE-I-NNNN`,
puis affiche le diagnostic.

Exemple de structure attendue :

```text
Decision : pre-validee
Identifiant propose : IMAGE-S-0008
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- cible d'ecriture probable: registers/images/images.json
- lecture seule: aucune modification du registre IMAGE
```

Les incertitudes de date, d'attribution ou de droits produisent des reserves.
Une source inconnue, un photographe introuvable ou une image individuelle sans
`session_ref` valide produit un bloquant.

### Resume PR obtenu

Avec `--pr-summary`, un fichier Markdown est genere dans :

```text
exports/generated/pr_summary_image_*.md
```

Ce resume expose l'objet iconographique propose, les validations, les reserves,
les bloquants et les arbitrages humains attendus. Il ne cree pas d'image
canonique et ne republie aucun fichier image.

## 7. Premiere SOURCE LONGUE

### Saisie dans le formulaire

Ouvrir l'onglet `SOURCE LONGUE`.

Exemple de saisie :

```text
title: Prototype Long Source
author: Prototype Author
type: livre
year: 2026
reference: Prototype Author, Prototype Long Source, Test Press, 2026.
notes: verifier les pages utiles avant integration
```

Les champs importants sont :

- `title` : titre de la source candidate ;
- `author` : auteur, autrice ou responsable documentaire ;
- `type` : type documentaire ;
- `year` : annee ou date principale ;
- `reference` : reference bibliographique complete ;
- `notes` : memo de travail.

### Commande generee

Le formulaire produit une commande du type :

```bash
python3 tools/m2_integrate_source.py --title 'Prototype Long Source' --author 'Prototype Author' --type 'livre' --year '2026' --reference 'Prototype Author, Prototype Long Source, Test Press, 2026.' --pr-summary
# notes: verifier les pages utiles avant integration
```

Les notes sont affichees comme memo. Elles ne remplacent pas les champs pris en
charge par la CLI.

### Diagnostic

La CLI SOURCE LONGUE compare la source candidate au registre des sources.

Elle peut indiquer :

- une source deja presente ;
- une proximite documentaire a arbitrer ;
- un `Sxx` probable ;
- un dossier source probable ;
- des bloquants si les champs minimaux ne permettent pas la pre-validation.

### Source candidate et source canonique

Une source candidate est une proposition saisie pour diagnostic.

Une source canonique est une source effectivement acceptee dans
`data/registre.json`.

Le formulaire et la CLI de pre-validation ne creent pas la source canonique. Ils
preparent seulement la revue.

## 8. Premiere campagne BATCH

Le batch sert lorsqu'il faut preparer plusieurs objets ensemble.

Exemple simple :

- une personne candidate ;
- une organisation candidate ;
- un lieu candidat ;
- une image candidate.

### Constituer le lot

1. Aller dans l'onglet `PERSON`.
2. Remplir les champs PERSON.
3. Cliquer sur `Ajouter au batch`.
4. Aller dans l'onglet `ORG`.
5. Remplir les champs ORG.
6. Cliquer sur `Ajouter au batch`.
7. Aller dans l'onglet `PLACE`.
8. Remplir les champs PLACE.
9. Cliquer sur `Ajouter au batch`.
10. Aller dans l'onglet `IMAGE`.
11. Remplir les champs IMAGE.
12. Cliquer sur `Ajouter au batch`.
13. Aller dans l'onglet `BATCH`.
14. Renseigner un nom de campagne.

### JSON obtenu

Le formulaire produit un JSON du type :

```json
{
  "campaign": "campagne-demo",
  "items": [
    {
      "family": "person",
      "name": "Prototype Person",
      "category": "industrie",
      "roles": ["producteur"],
      "sources": ["S41"],
      "note": "rattachement a verifier en revue"
    },
    {
      "family": "org",
      "name": "Prototype Organisation",
      "category": "label",
      "country": "GB",
      "jd_relation": "label_mate",
      "sources": ["S41"],
      "last_verified": "2026-06-06",
      "relation_notes": "relation documentaire a confirmer"
    },
    {
      "family": "place",
      "label": "Prototype Venue",
      "type": "salle",
      "type_detail": "club",
      "sources": ["S41"],
      "aliases": ["Prototype Club"],
      "usage": "concert",
      "prudence": "verifier la distinction avec le batiment voisin"
    },
    {
      "family": "image",
      "level": "session",
      "name": "Prototype Image Session",
      "photographer": "PERSON-kevin-cummins",
      "sources": ["S41"],
      "date": "1979-02",
      "date_precision": "month",
      "context": "promo",
      "subjects": ["PERSON-ian-curtis"],
      "place": "PLACE-HULME",
      "last_verified": "2026-06-06",
      "notes": "droits et provenance a confirmer en revue"
    }
  ]
}
```

Enregistrer ce JSON dans un fichier de travail, par exemple :

```text
exports/generated/campagne-demo.json
```

### Commande batch

Executer :

```bash
python3 tools/m2_batch_prevalidation.py exports/generated/campagne-demo.json
```

### Rapport consolide

La commande produit un rapport Markdown :

```text
exports/generated/batch_summary_campagne-demo.md
```

Le rapport indique :

- nombre d'objets ;
- nombre de pre-validations ;
- nombre de pre-validations avec reserve ;
- nombre de refus ;
- reserves ;
- bloquants ;
- arbitrages humains.

### Resumes PR individuels

Chaque item produit aussi un resume PR individuel :

```text
exports/generated/pr_summary_*.md
```

Le rapport consolide la campagne. Les resumes PR individuels permettent de
relire chaque proposition separement.

## 9. Comment lire les diagnostics

### pre-validee

La proposition n'a pas de bloquant ni de reserve.

Exemple :

```text
Decision : pre-validee
Bloquants :
- aucun
Reserves :
- aucun
```

Cela signifie que la proposition peut etre relue humainement sur une base
propre. Ce n'est pas une validation definitive.

### pre-validee avec reserve

La proposition n'a pas de bloquant, mais un point doit etre arbitre.

Exemple :

```text
Decision : pre-validee avec reserve
Bloquants :
- aucun
Reserves :
- nom proche a arbitrer: Prototype Person ~ Existing Person
```

La proposition peut avancer vers une revue, mais la reserve doit etre lue et
traitee.

### non pre-validee

La proposition contient au moins un bloquant.

Exemple :

```text
Decision : non pre-validee
Bloquants :
- source inconnue: S999
```

Il faut corriger le bloquant avant de considerer la proposition comme prete pour
revue.

## 10. Comment lire un resume PR

Un resume PR M2 est un document Markdown genere dans `exports/generated/`.

Sections principales :

- `Objet` : ce qui est propose ;
- `Perimetre` : ce que couvre la proposition ;
- `Validations executees` : controles realises par la CLI ;
- `Bloquants` : points qui empechent la pre-validation ;
- `Reserves` : points a arbitrer ;
- `Informations` : contexte utile ;
- `Arbitrages humains` : decisions attendues du reviewer ;
- `Impact documentaire` : ce qui changerait si la proposition etait acceptee ;
- `Commandes de verification` : controles a relancer.

Pour preparer la revue :

1. Lire d'abord `Bloquants`.
2. Lire ensuite `Reserves`.
3. Verifier que les validations annoncees correspondent au flux utilise.
4. Lire les arbitrages humains.
5. Relancer les commandes de verification utiles.

Un resume PR ne remplace pas la PR ni la revue. Il rend la proposition plus
facile a relire.

## 11. Questions frequentes

### Le formulaire cree-t-il une personne ?

Non. Il prepare une commande. La CLI produit ensuite un diagnostic. La creation
effective d'une personne reste une decision humaine et une modification de
registre separee.

### Le formulaire cree-t-il un lieu ?

Non. L'onglet `PLACE` prepare une commande ou une entree batch. La creation
effective d'un lieu reste une modification de registre separee, relue et
validee humainement.

### Le formulaire cree-t-il une image canonique ?

Non. L'onglet `IMAGE` prepare une commande ou une entree batch. La creation
effective d'une entree `IMAGE-`, et toute question de droits ou de reproduction,
restent des decisions humaines separees.

### Le formulaire modifie-t-il le registre ?

Non. Le formulaire fonctionne localement dans le navigateur et ne modifie aucun
fichier du depot.

### Pourquoi ai-je une reserve ?

Une reserve signale un point qui ne bloque pas techniquement la pre-validation,
mais qui demande une decision humaine. Par exemple : nom proche, alias ambigu,
qualification documentaire incertaine.

### Quand utiliser BATCH ?

Utiliser `BATCH` lorsqu'il faut preparer plusieurs objets PERSON, ORG, PLACE et
IMAGE dans une meme campagne, puis obtenir un rapport consolide.

Pour un seul objet, l'onglet `PERSON`, `ORG`, `PLACE` ou `IMAGE` suffit.

### Quand utiliser PLACE ?

Utiliser `PLACE` lorsqu'il faut preparer un lieu documentaire : salle de
concert, studio, club, pub, ecole, quartier, batiment, lieu de repetition, lieu
photographique ou lieu historique.

### Quand utiliser IMAGE ?

Utiliser `IMAGE` lorsqu'il faut preparer une seance photographique, un cliche,
une pochette, une affiche, un scan, une image de presse, une capture video, une
image de concert, une image de lieu ou un document visuel d'archive.

### Quand utiliser SOURCE LONGUE ?

Utiliser `SOURCE LONGUE` lorsqu'il faut examiner une source documentaire
candidate : livre, article, interview, fanzine, archive, memoire, these ou
dossier documentaire.

SOURCE LONGUE ne sert pas a ajouter directement une personne ou une organisation
au registre.

## 12. Bonnes pratiques

- Toujours verifier les sources `Sxx` avant de lancer une proposition.
- Toujours lire les reserves.
- Toujours corriger les bloquants avant revue.
- Toujours conserver une validation humaine finale.
- Toujours garder le resume PR avec le diagnostic correspondant.
- Ne jamais considerer un diagnostic comme une validation definitive.
- Ne jamais deduire qu'une source candidate est canonique tant qu'elle n'a pas
  ete acceptee dans le registre.
- Ne jamais considerer une attribution ou des droits image comme etablis sans
  arbitrage humain explicite.
- Utiliser le batch pour une campagne, pas pour masquer plusieurs propositions
  sans revue detaillee.
