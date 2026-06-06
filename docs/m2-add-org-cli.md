# M2 - Prototype CLI d'ajout ORG

## Objectif

`tools/m2_add_org.py` est le prototype local du Studio M2 pour preparer l'ajout d'une organisation canonique `ORG-`.

Il sert a :

- proposer le prochain identifiant `ORG-NNNN` disponible ;
- verifier les sources `Sxx` contre `data/registre.json` ;
- verifier la categorie, le pays, le statut, le gate et la relation Joy Division minimale ;
- detecter les collisions evidentes de nom canonique et d'alias ;
- refuser un identifiant Wikidata deja utilise par une ORG existante ;
- signaler en reserve les proximites faibles de nom ou d'alias ;
- produire une entree candidate JSON compatible avec `schemas/organization_canonical.schema.json` ;
- classer les constats en `bloquant`, `reserve` ou `information`.

Le prototype prepare. L'humain decide.

## Commande

```bash
python3 tools/m2_add_org.py \
  --name "Factory Records" \
  --category label \
  --country GB \
  --jd-relation label_mate \
  --sources S41,S74 \
  --last-verified 2026-06-01
```

Parametres obligatoires :

| Parametre | Role |
| --- | --- |
| `--name` | Nom canonique de l'organisation. |
| `--category` | Categorie ORG. |
| `--country` | Code pays ISO alpha-2. |
| `--jd-relation` | Type de relation documentee avec Joy Division. |
| `--sources` | Sources `Sxx` separees par des virgules. |
| `--last-verified` | Date explicite de verification humaine, au format `YYYY-MM-DD`. Aucune date dynamique n'est generee. |

Parametres facultatifs :

| Parametre | Role |
| --- | --- |
| `--aliases` | Alias separes par des virgules. |
| `--status` | Statut ORG. Par defaut : `unknown`. |
| `--gate` | Gate de visibilite. Par defaut : `private`. |
| `--subcategory` | Sous-categorie libre. |
| `--city` | Ville principale. |
| `--active-from` | Debut d'activite documente. |
| `--active-until` | Fin d'activite documentee, ou `null`. |
| `--relation-period` | Periode de relation avec Joy Division. |
| `--relation-notes` | Notes courtes sur la relation documentee. |
| `--wikidata` | Identifiant Wikidata `Q...` verifie. |
| `--discogs` | URL ou identifiant Discogs verifie. |
| `--musicbrainz` | UUID MusicBrainz verifie. |
| `--provenance-from-pers` | Identifiant `PERS-*` d'origine si hand-off documente. |
| `--provenance-from-attribution` | Produit `provenance.from_attribution: true`. |

Categories valides, egalement visibles dans `--help` :

- `group`
- `label`
- `institution`
- `venue_org`
- `crew`
- `media`
- `other`

Statuts valides :

- `active`
- `dissolved`
- `dormant`
- `unknown`

Gates valides :

- `public`
- `private`

## Sortie

La sortie est deterministe et ne contient aucune date dynamique.

Exemple conforme :

````text
Decision : pre-validee
Identifiant propose : ORG-0009
Bloquants :
- aucun
Reserves :
- aucun
Informations :
- prochain numero disponible detecte: ORG-0009
- cible d'ecriture probable: registers/orgs/orgs.json
- lecture seule: aucune modification du registre ORG
Entree candidate :
```json
{
  "org_id": "ORG-0009",
  "canonical_name": "Factory Records",
  "aliases": [],
  "category": "label",
  "country": "GB",
  "status": "unknown",
  "same_as": {
    "wikidata": null,
    "musicbrainz": null,
    "discogs": null
  },
  "joy_division_relation": {
    "type": "label_mate",
    "period": null
  },
  "sources": [
    "S41",
    "S74"
  ],
  "identity_frozen": true,
  "drift_sentinel": "v1.0",
  "gate": "private",
  "last_verified": "2026-06-01"
}
```
````

Exemple non pre-valide :

```text
Decision : non pre-validee
Identifiant propose : ORG-0009
Bloquants :
- source inconnue: S999
```

Exemple avec reserve :

```text
Decision : pre-validee avec reserve
Reserves :
- alias proche d'un nom a arbitrer: Factory Record ~ Factory Records (ORG-0001)
```

Une collision stricte reste bloquante. Une proximite faible de nom ou d'alias devient une reserve visible.

## Limites

Le prototype ne doit pas :

- modifier `registers/orgs/orgs.json` ;
- modifier les schemas ;
- modifier les exports ;
- ouvrir une PR ;
- creer une branche Git ;
- merger automatiquement ;
- prendre une decision historiographique ;
- corriger automatiquement une collision ;
- creer une couche commune PERSON/ORG ;
- preparer un prototype multi-types.

Le prototype lit `registers/orgs/orgs.json` pour proposer le prochain `ORG-NNNN` et detecter les collisions. Il lit `data/registre.json` pour verifier les sources. Il utilise `schemas/organization_canonical.schema.json` comme contrat de forme de l'entree candidate.

## Lien avec M2

Lien avec M2.1 :

- le prototype applique le contrat d'ajout unitaire `ORG` ;
- il produit une seule entree candidate ;
- il conserve les sources avant enrichissement ;
- il ne cree pas de nouvelle source canonique.

Lien avec M2.2 :

- les constats sont classes en `bloquant`, `reserve` ou `information` ;
- source inconnue, identifiant duplique, Wikidata deja utilise, categorie invalide, pays invalide, relation absente et schema invalide restent bloquants ;
- alias proche ou organisation proche deviennent des reserves.

Lien avec M2.4 :

- la sortie est faite pour alimenter une future PR relisible ;
- les validations et reserves sont visibles ;
- la validation humaine reste obligatoire ;
- le prototype n'ouvre pas lui-meme de PR.

## Verifications

Commandes utiles :

```bash
python3 tools/m2_add_org.py --help
python3 -m unittest tools.test_m2_add_org
python3 tools/validate_orgs.py
```
