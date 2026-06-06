# M2 - Utilisation du formulaire de saisie

## Role

Le formulaire M2 est une couche locale de saisie.

Il prepare :

- une commande `tools/m2_add_person.py` ;
- une commande `tools/m2_add_org.py` ;
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

Le formulaire permet d'ajouter plusieurs items PERSON et ORG dans une campagne.

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
python3 tools/m2_integrate_source.py --help
python3 tools/m2_batch_prevalidation.py --help
```

Verifications de non-regression M2 :

```bash
python3 -m unittest discover -s tools -p 'test_*.py'
```
