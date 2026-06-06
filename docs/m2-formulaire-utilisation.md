# M2 - Utilisation du formulaire de saisie

## Role

Le formulaire M2 est une couche locale de saisie.

Il prepare :

- une commande `tools/m2_add_person.py` ;
- une commande `tools/m2_add_org.py` ;
- une commande `tools/m2_add_place.py` ;
- une commande `tools/m2_add_image.py` ;
- une commande `tools/m2_integrate_source.py` ;
- un JSON de campagne compatible avec `tools/m2_batch_prevalidation.py`.

Il ne valide pas les objets. Les diagnostics restent produits par les CLI M2.

## Emplacement

```text
apps/m2-formulaire/
```

La page fonctionne localement dans un navigateur avec :

```text
apps/m2-formulaire/index.html
```

La page affiche un bloc `Mode d'emploi` qui resume le workflow, les usages
PERSON / ORG / PLACE / IMAGE / SOURCE LONGUE / BATCH et les limites du
formulaire.

Le portail racine expose aussi un lien vers l'application dans l'onglet
`Outils du livre`.

## Limites

Le formulaire ne doit jamais :

- creer une source canonique ;
- creer un atome ;
- creer une citation ;
- creer une relation ;
- modifier un registre ;
- appeler GitHub ;
- creer une Pull Request ;
- merger ;
- dupliquer les regles documentaires des adaptateurs Python.

Il collecte des champs et produit du texte copiable.

## Exemple PERSON

Champs saisis :

```text
name: Prototype Person
category: industrie
roles: producteur
sources: S41
notes: prudence sur le rattachement
```

Commande generee :

```bash
python3 tools/m2_add_person.py --name 'Prototype Person' --category 'industrie' --role 'producteur' --sources 'S41' --note 'prudence sur le rattachement' --pr-summary
```

Commande a executer apres copie :

```bash
python3 tools/m2_add_person.py --name 'Prototype Person' --category 'industrie' --role 'producteur' --sources 'S41' --note 'prudence sur le rattachement' --pr-summary
```

## Exemple ORG

Champs saisis :

```text
name: Prototype Organisation
category: label
country: GB
jd_relation: label_mate
sources: S41
last_verified: 2026-06-06
notes: relation a confirmer en revue
```

Commande generee :

```bash
python3 tools/m2_add_org.py --name 'Prototype Organisation' --category 'label' --country 'GB' --jd-relation 'label_mate' --sources 'S41' --last-verified '2026-06-06' --relation-notes 'relation a confirmer en revue' --pr-summary
```

## Exemple PLACE

Champs saisis :

```text
label: Prototype Venue
type: salle
type_detail: club
sources: S41
aliases: Prototype Club
usage: concert
prudence: verifier la distinction avec le batiment voisin
```

Commande generee :

```bash
python3 tools/m2_add_place.py --label 'Prototype Venue' --type 'salle' --sources 'S41' --aliases 'Prototype Club' --type-detail 'club' --usage 'concert' --prudence 'verifier la distinction avec le batiment voisin' --pr-summary
```

## Exemple IMAGE

Champs saisis :

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

Commande generee :

```bash
python3 tools/m2_add_image.py --level 'session' --name 'Prototype Image Session' --photographer 'PERSON-kevin-cummins' --sources 'S41' --last-verified '2026-06-06' --date '1979-02' --date-precision 'month' --context 'promo' --subjects 'PERSON-ian-curtis' --place 'PLACE-HULME' --notes 'droits et provenance a confirmer en revue' --pr-summary
```

## Exemple SOURCE LONGUE

Champs saisis :

```text
title: Prototype Long Source
author: Prototype Author
type: livre
year: 2026
reference: Prototype Author, Prototype Long Source, Test Press, 2026.
notes: pages utiles a renseigner ensuite si necessaire
```

Commande generee :

```bash
python3 tools/m2_integrate_source.py --title 'Prototype Long Source' --author 'Prototype Author' --type 'livre' --year '2026' --reference 'Prototype Author, Prototype Long Source, Test Press, 2026.' --pr-summary
# notes: pages utiles a renseigner ensuite si necessaire
```

Les notes SOURCE LONGUE restent un memo de saisie. Elles ne sont pas transmises
au CLI si aucun parametre correspondant n'existe.

## Exemple batch

Le formulaire permet d'ajouter plusieurs items PERSON, ORG, PLACE et IMAGE dans
une campagne.

JSON genere :

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
      "note": "prudence sur le rattachement"
    },
    {
      "family": "org",
      "name": "Prototype Organisation",
      "category": "label",
      "country": "GB",
      "jd_relation": "label_mate",
      "sources": ["S41"],
      "last_verified": "2026-06-06",
      "relation_notes": "relation a confirmer en revue"
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

Commande a executer apres avoir enregistre le JSON dans un fichier :

```bash
python3 tools/m2_batch_prevalidation.py path/to/campaign.json
```

## Commandes utiles

Verifications manuelles apres copie :

```bash
python3 tools/m2_add_person.py --help
python3 tools/m2_add_org.py --help
python3 tools/m2_add_place.py --help
python3 tools/m2_add_image.py --help
python3 tools/m2_integrate_source.py --help
python3 tools/m2_batch_prevalidation.py --help
```

Verifications de non-regression M2 :

```bash
python3 -m unittest discover -s tools -p 'test_*.py'
```
