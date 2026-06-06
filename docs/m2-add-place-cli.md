# M2.1 - Prototype CLI d'ajout PLACE

## Objectif

`tools/m2_add_place.py` est le prototype local du Studio M2 pour preparer
l'ajout d'un lieu documentaire canonique `PLACE-`.

Il sert a :

- proposer un identifiant `PLACE-<SLUG>` conforme aux conventions existantes ;
- verifier les sources `Sxx` contre `data/registre.json` ;
- verifier le type de lieu contre `schemas/places.schema.yaml` ;
- detecter les collisions evidentes d'identifiant et de label ;
- utiliser les alias saisis pour detecter des collisions ou proximites ;
- signaler en reserve les proximites documentaires faibles ;
- produire une entree candidate YAML ;
- classer les constats en `bloquant`, `reserve` ou `information` ;
- produire un resume PR standardise avec `--pr-summary`.

Le prototype prepare. L'humain decide.

## Commande

```bash
python3 tools/m2_add_place.py \
  --label "Russell Club" \
  --type salle \
  --sources S41,S74 \
  --type-detail club \
  --aliases "The Factory" \
  --pr-summary
```

Parametres obligatoires :

| Parametre | Role |
| --- | --- |
| `--label` | Label canonique propose pour le lieu. |
| `--type` | Type PLACE canonique, selon `schemas/places.schema.yaml`. |
| `--sources` | Sources `Sxx` separees par des virgules. |

Parametres facultatifs :

| Parametre | Role |
| --- | --- |
| `--aliases` | Alias de saisie separes par des virgules. Ils servent au diagnostic et ne sont pas integres automatiquement au candidat. |
| `--type-detail` | Precision libre du type de lieu, par exemple `club`, `studio`, `ecole`. |
| `--usage` | Usage documentaire attendu du lieu. |
| `--prudence` | Note de prudence documentaire ou d'arbitrage. |
| `--pr-summary` | Genere `exports/generated/pr_summary_place_*.md`. |

Types valides, egalement visibles dans `--help` :

- `ville`
- `quartier`
- `habitat`
- `studio`
- `salle`
- `commerce`
- `education`
- `sante`
- `industrie`
- `science`
- `infrastructure`
- `pouvoir`
- `lieu_memoire`

## Sortie

La sortie est deterministe et ne contient aucune date dynamique.

Exemple conforme :

````text
Decision : pre-validee
Identifiant propose : PLACE-RUSSELL-CLUB
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- cible d'ecriture probable: registers/places/*.md
- lecture seule: aucune modification du registre PLACE
Entree candidate :
```yaml
id: PLACE-RUSSELL-CLUB
label: Russell Club
type: salle
sources:
- S41
- S74
type_detail: club
```
````

Exemple avec reserve :

```text
Decision : pre-validee avec reserve
Reserves :
- alias proche d'un lieu a arbitrer: Factory Record ~ Factory Records (PLACE-FACTORY-RECORDS)
```

Une proximite faible de label ou d'alias devient une reserve. Une collision
stricte d'identifiant ou de label reste bloquante.

Exemple non pre-valide :

```text
Decision : non pre-validee
Identifiant propose : PLACE-RUSSELL-CLUB
Bloquants :
- source inconnue: S999
```

## Resume PR

Avec `--pr-summary`, la CLI genere un resume Markdown dans :

```text
exports/generated/pr_summary_place_*.md
```

Le resume expose :

- l'objet PLACE propose ;
- le perimetre de lecture seule ;
- les validations executees ;
- les reserves ;
- les bloquants ;
- les arbitrages humains attendus ;
- l'impact documentaire potentiel ;
- les commandes de verification.

Le resume ne cree pas de branche, n'ouvre pas de PR et ne modifie pas GitHub.

## Limites

Le prototype ne doit pas :

- modifier `registers/places/` ;
- modifier les schemas ;
- modifier `data/registre.json` ;
- creer une source canonique ;
- creer un atome ;
- creer une relation ;
- ouvrir une PR ;
- creer une branche Git ;
- merger automatiquement ;
- prendre une decision historiographique ;
- corriger automatiquement une collision.

Le prototype lit `registers/places/**/*.md` pour detecter les lieux existants.
Il lit `data/registre.json` pour verifier les sources et
`schemas/places.schema.yaml` pour verifier la forme de l'entree candidate.

## Lien avec M2.1

PLACE applique les memes principes que PERSON et ORG :

- une entree candidate ;
- un diagnostic ;
- un resume PR optionnel ;
- aucune integration automatique ;
- validation humaine obligatoire.

Le batch peut utiliser la famille :

```json
{
  "family": "place",
  "label": "Russell Club",
  "type": "salle",
  "sources": ["S41"]
}
```

## Verifications

Commandes utiles :

```bash
python3 tools/m2_add_place.py --help
python3 -m unittest tools.test_m2_add_place
python3 tools/validate_places.py
```
