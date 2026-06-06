# M2 - Prototype CLI d'ajout PERSON

## Objectif

`tools/m2_add_person.py` est le premier prototype operationnel local du Studio M2 pour preparer l'ajout d'une personne canonique `PERSON-`.

Il sert a :

- proposer un identifiant `PERSON-<slug>` a partir d'un nom ;
- verifier les sources `Sxx` contre `data/registre.json` ;
- verifier la categorie contre le vocabulaire canonique ;
- detecter les collisions evidentes d'identifiant, nom, alias et `same_as` ;
- produire une entree candidate YAML ;
- classer les constats en `bloquant`, `reserve` ou `information`.

Le prototype prepare. L'humain decide.

## Commande

```bash
python3 tools/m2_add_person.py \
  --name "Nom Personne" \
  --category industrie \
  --role producteur \
  --sources S41,S74
```

Parametres obligatoires :

| Parametre | Role |
| --- | --- |
| `--name` | Nom canonique propose. |
| `--category` | Categorie PERSON. |
| `--role` | Role documentaire. Peut etre repete ou contenir des valeurs separees par des virgules. |
| `--sources` | Sources `Sxx` separees par des virgules. |

Parametres facultatifs :

| Parametre | Role |
| --- | --- |
| `--aliases` | Alias separes par des virgules. |
| `--same-as` | Identifiants provisoires `PERS-*` separes par des virgules. |
| `--note` | Note de prudence ou de canonicalisation. |
| `--origin auteur_source` | Cas auteur-source supporte par le schema. |
| `--category-arbitration` | Produit `categorie_a_arbitrer: true`. |
| `--identity-arbitration` | Produit `a_arbitrer: true`. |

Categories valides :

- `membre`
- `entourage`
- `industrie`
- `critique_journaliste`
- `auteur_secondaire`
- `influence`
- `theoricien_mobilise`

## Sortie

La sortie est deterministe et ne contient aucune date dynamique.

Exemple conforme :

````text
Decision : pre-validee
Identifiant propose : PERSON-exemple-personne
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- same_as vide: cible d'ecriture a confirmer avant integration
Entree candidate :
```yaml
id: PERSON-exemple-personne
type_unite: person
name: Exemple Personne
categorie: industrie
role:
- producteur
sources:
- S41
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```
````

Exemple non pre-valide :

```text
Decision : non pre-validee
Identifiant propose : PERSON-exemple-personne
Bloquants :
- source inconnue: S999
```

## Limites

Le prototype ne doit pas :

- modifier les registres ;
- modifier les schemas ;
- modifier les exports ;
- ouvrir une PR ;
- creer une branche Git ;
- merger automatiquement ;
- prendre une decision historiographique ;
- corriger automatiquement une collision.

Le prototype lit `registers/people/00_canonical_people.md` et `registers/people/00_authors_canonical.md` pour detecter les collisions `PERSON-`. Il lit aussi `exports/generated/people.json` pour verifier les rattachements `PERS-*` lorsque `--same-as` est utilise.

## Lien avec M2

Lien avec M2.1 :

- le prototype applique le contrat d'ajout unitaire `PERSON` ;
- il produit une seule entree candidate ;
- il conserve les sources avant enrichissement.

Lien avec M2.2 :

- les constats sont classes en `bloquant`, `reserve` ou `information` ;
- source inconnue, identifiant duplique, categorie invalide et schema invalide restent bloquants.

Lien avec M2.4 :

- la sortie est faite pour alimenter une future PR relisible ;
- les validations et reserves sont visibles ;
- la validation humaine reste obligatoire.

## Verifications

Commandes utiles :

```bash
python3 tools/m2_add_person.py --help
python3 -m unittest tools.test_m2_add_person
python3 tools/validate_people.py
```
