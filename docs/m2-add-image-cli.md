# M2.1 - Prototype CLI d'ajout IMAGE

## Objectif

`tools/m2_add_image.py` prepare l'ajout d'un objet iconographique `IMAGE-` sans
modifier le depot.

Il couvre les deux niveaux du registre existant :

- `session` -> `IMAGE-S-NNNN` pour une seance photographique ou visuelle ;
- `image` -> `IMAGE-I-NNNN` pour un cliche ou objet visuel individuel.

Le prototype prepare. L'humain decide.

## Champs pris en charge

Parametres obligatoires :

| Parametre | Role |
| --- | --- |
| `--level` | `session` ou `image`. |
| `--name` | Designation canonique proposee. |
| `--photographer` | Identifiant `PERSON-*` du photographe ou auteur visuel. |
| `--sources` | Sources `Sxx` separees par des virgules. Une URL est acceptee mais signalee en reserve. |
| `--last-verified` | Date de verification humaine au format `YYYY-MM-DD`. |

Parametres facultatifs :

| Parametre | Role |
| --- | --- |
| `--date` | Date complete ou partielle. |
| `--date-precision` | `day`, `month`, `year` ou `approximate`. Par defaut : `approximate`. |
| `--subjects` | Sujets `PERSON-*` ou descriptions libres. |
| `--session-ref` | Session `IMAGE-S-NNNN` parente, obligatoire pour `level=image`. |
| `--place` | Lieu `PLACE-*` ou description libre. |
| `--event-ref` | Reference `EVENT-*` si disponible. |
| `--context` | `promo`, `live`, `portrait`, `artwork`, `rehearsal` ou `other`. |
| `--output-count` | Nombre de cliches connus pour une session. |
| `--usage` | Usages connus : presse, pochette, exposition, archive. |
| `--iconic` | Marque `iconic=true`. |
| `--notes` | Notes documentaires libres. |
| `--gate` | `private` par defaut, ou `public` apres arbitrage humain. |
| `--wikidata` | Identifiant Wikidata `Q...`. |
| `--image-id` | Identifiant explicite si le prochain identifiant ne doit pas etre propose. |
| `--rights-uncertain` | Produit une reserve de droits. |
| `--attribution-uncertain` | Produit une reserve d'attribution. |
| `--pr-summary` | Genere un resume PR dans `exports/generated/`. |

## Exemple session

```bash
python3 tools/m2_add_image.py \
  --level session \
  --name "Seance prototype Hulme" \
  --photographer PERSON-kevin-cummins \
  --date 1979-02 \
  --date-precision month \
  --context promo \
  --subjects PERSON-ian-curtis,PERSON-peter-hook \
  --place PLACE-HULME \
  --sources S41,S76 \
  --last-verified 2026-06-06 \
  --pr-summary
```

## Exemple image individuelle

```bash
python3 tools/m2_add_image.py \
  --level image \
  --session-ref IMAGE-S-0001 \
  --name "Cliche prototype de Ian Curtis" \
  --photographer PERSON-kevin-cummins \
  --date 1979-01-06 \
  --date-precision day \
  --context promo \
  --subjects PERSON-ian-curtis \
  --place PLACE-HULME \
  --usage "presse,archive" \
  --sources S41 \
  --last-verified 2026-06-06 \
  --pr-summary
```

## Decisions possibles

### pre-validee

Aucun bloquant ni reserve.

### pre-validee avec reserve

La proposition peut etre relue, mais un point demande un arbitrage humain.

Reserves frequentes :

- date ou periode approximative ;
- droits image incertains ;
- attribution photographe incertaine ;
- URL non canonique utilisee comme trace documentaire ;
- proximite documentaire avec une image existante ;
- sujet `PERSON-*` ou lieu `PLACE-*` introuvable a arbitrer.

### non pre-validee

La proposition contient au moins un bloquant.

Bloquants frequents :

- identifiant `IMAGE-*` deja utilise ;
- source `Sxx` inconnue ;
- `level=image` sans `session_ref` valide ;
- photographe absent, invalide ou introuvable ;
- date incompatible avec `date_precision` ;
- schema `schemas/image_canonical.schema.json` non respecte.

## Resume PR

Avec `--pr-summary`, la CLI genere :

```text
exports/generated/pr_summary_image_*.md
```

Le resume expose :

- objet ;
- perimetre ;
- validations executees ;
- bloquants ;
- reserves ;
- informations ;
- arbitrages humains ;
- impact documentaire ;
- commandes de verification.

Le resume ne cree pas de branche, n'ouvre pas de PR et ne modifie pas GitHub.

## Usage batch

Le batch accepte :

```json
{
  "family": "image",
  "level": "session",
  "name": "Seance prototype Hulme",
  "photographer": "PERSON-kevin-cummins",
  "date": "1979-02",
  "date_precision": "month",
  "context": "promo",
  "subjects": ["PERSON-ian-curtis"],
  "place": "PLACE-HULME",
  "sources": ["S41"],
  "last_verified": "2026-06-06"
}
```

La campagne produit un rapport consolide et un resume PR individuel IMAGE.

## Limites

Le prototype ne doit pas :

- modifier `registers/images/images.json` ;
- creer une image canonique ;
- telecharger ou republier un fichier image ;
- creer une source ;
- creer un atome ;
- creer une relation ;
- creer une citation ;
- arbitrer les droits d'image ;
- ouvrir une PR GitHub ;
- merger automatiquement.

Le prototype lit `registers/images/images.json`, `data/registre.json`,
`schemas/image_canonical.schema.json`, les registres PERSON et les registres
PLACE. Les decisions documentaires restent humaines.

## Verifications

Commandes utiles :

```bash
python3 tools/m2_add_image.py --help
python3 -m unittest tools.test_m2_add_image
python3 -m unittest tools.test_m2_batch_prevalidation
python3 tools/validate_images.py
```
