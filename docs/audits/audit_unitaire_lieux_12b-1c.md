# Audit unitaire — registre des lieux (préalable à l'étape 12b-1.c)

> Audit **préalable à tout enrichissement**, conformément à la contrainte de
> l'étape 4 : on inspecte l'existant (entrées manuelles anciennes vs atomisées
> v2) **avant** de poser la couche cartographique.
>
> Date création : 30/05/2026. Mis à jour : 31/05/2026 (curation manuelle — 42 → 55 lieux).
> Périmètre : `registers/**/*.md`, lus comme le fait le
> runtime (`apps/lib/dynamic-registers.js`) et `tools/validate_places.py`.

---

## 1. Volumétrie

| Mesure | Valeur |
|--------|-------:|
| Enregistrements-source de lieux (parasites d'en-tête exclus) | 91 |
| Identifiants distincts (après dédup par id) | 83 |
| **Lieux canoniques** (après réconciliation `same_as`) | **79** |
| Alias résolus (`same_as`) | 4 |
| Lieux géolocalisés — état courant | **55 / 91 = 60 %** (voir §8 pour l'historique) |

Répartition canonique par famille : `ville` 17, `salle` 14, `quartier` 13,
`habitat` 10, `studio` 9, `education` 7, `commerce` 7, `lieu_memoire` 4,
`industrie` 3, `sante` 1, `science` 1, `infrastructure` 1, `pouvoir` 1.

---

## 2. Manuelles anciennes vs atomisées v2

| Famille de fichier | Enreg. | Format d'id | Champs typiques |
|--------------------|-------:|-------------|------------------|
| **Atomisées v2** (`*_v2.md` : S02, S05, S06, S10, S20) | 51 | slug canonique | `sources`, `usage`, `atoms`, `type`/`type_detail` |
| **Manuelles / spécialisées** (S13, S35, S41, S83) | 40 | hétérogène (slug, scoping-source, positionnel) | `_legacy_format`, `usage`/`usage_sXX`, blocs standalone |

Constats unitaires :

- **v2** : homogènes, déjà au format canonique slug, propres. Aucune anomalie.
- **S35** (manuel) : slugs canoniques, mais champ `_legacy_format`
  (`s35-lieux-fonction` / `s35-lieux-role`) — traçabilité conservée, RAS.
- **S13** (spécialisé) : slugs canoniques, `_legacy_format: s13-lieux`. RAS.
- **S41** (registre songs) : ids **scoping-source**
  (`PLACE-S41-…`) — non conformes à la règle canonique.
- **S83** (registre spécialisé Hannett) : ids **positionnels**
  (`PLACE-S83-00N`) — non conformes ; blocs YAML standalone.

---

## 3. Anomalie structurante : trois conventions d'identifiants

Un même lieu physique apparaissait sous **trois** identifiants distincts —
le studio **T.J. Davidson's, Little Peter Street** :

| Identifiant | Source | Convention |
|-------------|--------|------------|
| `PLACE-TJ-DAVIDSONS` | S10 | slug v2 (canonique) |
| `PLACE-S83-001` | S83 | positionnel |
| `PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET` | S41 | scoping-source |

La dédup runtime ne fusionnant que sur **id exact**, ces trois entrées
produisaient trois punaises distinctes pour un seul lieu — incompatible avec une
carte et avec les croisements futurs (concerts, maillage).

### Résolution (sans renommage — gel respecté)

Convention canonique gelée + arête d'équivalence `same_as` posée sur les
**legacy** (cf. `docs/conventions/identifiants_lieux.md`) :

```text
PLACE-S83-001                               → PLACE-TJ-DAVIDSONS
PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET  → PLACE-TJ-DAVIDSONS
PLACE-S83-002 (Hulme Crescents)             → PLACE-HULME-CRESCENTS
PLACE-MANCHESTER-CITY                       → PLACE-MANCHESTER       (lot B)
```

Loader et validateur résolvent la clôture transitive (union-find). Décompte :
83 → **79** lieux canoniques.

---

## 4. Granularités d'échelle — décisions (fusionner vs distinguer)

- **`PLACE-MANCHESTER-CITY` → réconcilié vers `PLACE-MANCHESTER`** (lot B) :
  même référent physique (la ville de Manchester). S02 forge « City of
  Manchester » comme *échelle municipale*, dont le contraste est avec Greater
  Manchester — pas avec Manchester. La nuance municipale est préservée (usage et
  sources S02 unionés sur le canonique). La contrainte ville/région est portée
  par le couple `PLACE-MANCHESTER` (ville) vs `PLACE-GREATER-MANCHESTER` (region).
- **Conservés distincts** (échelles / registres sémantiques réellement
  différents) : `PLACE-MANCHESTER` (ville) · `PLACE-MANCHESTER-CENTRE` (quartier,
  centralité) · `PLACE-GREATER-MANCHESTER` (region, comté) ·
  `PLACE-MANCHESTER-GLOBAL-MEMORY` (lieu_memoire, réception mondiale).
- `PLACE-FREE-TRADE-HALL` vs `PLACE-LESSER-FREE-TRADE-HALL` — **deux salles**
  (le grand hall et la petite salle), même bâtiment, événements distincts (le
  Lesser FTH = concert Sex Pistols de 1976). Coordonnée partagée justifiée
  (`prudence_methodologique`), identifiants séparés.

---

## 5. Legacy singletons non conformes — conservés en l'état

Ids legacy **sans doublon** (aucun canonique équivalent à réconcilier). Le gel
**interdit le renommage** ; ils restent valides et référençables. Les futurs
enregistrements, eux, suivent la forme canonique.

- `PLACE-S41-SWAN-PUB-ECCLES-NEW-ROAD` (Swan pub, Eccles New Road) ;
- `PLACE-S83-003` (Ferranti's manufacturing plant) ;
- `PLACE-S83-004` (Salford Technical School).

---

## 6. Couche cartographique (après curation manuelle)

- **55 lieux géolocalisés** (lat/lng WGS84) : venues précises (points :
  exacte/rue/quartier) + zones (étendues : ville/region), rendues
  distinctement (cf. `docs/NAMING_CONVENTIONS.md` §10.8).
- Précision honnête par lieu (`geo_precision`, échelle ordinale à 5 paliers),
  provenance dans `prudence_methodologique` (adresse + source + URL + réserve) ;
  `reference_croisee` pour les identifiants d'autorité structurés (Wikidata QID,
  `gias:<URN>` pour établissements scolaires anglais).
- Coordonnées attachées au lieu **canonique**, après réconciliation.
- Détail : `docs/conventions/carte_lieux_12b-1c.md`.

---

## 7. Conformité

`python3 tools/validate_places.py` (post-backfill) :

```text
Source place records (parasites excluded) : 91
Distinct ids after id-deduplication        : 83
  dont alias legacy (same_as)              : 4
Canonical places after same_as merge       : 79
Valid against schema                        : 91/91
All place records are valid (schéma + same_as INV-1..4).
```

Tests unitaires INV-1..4 (16 cas) :

```text
python3 -m unittest tools.test_validate_places   # depuis la racine
python3 tools/test_validate_places.py            # exécution directe
```

Aucune donnée documentaire existante n'a été modifiée : les seuls ajouts sont
des champs **optionnels rétrocompatibles** (`same_as`, `lat`/`lng`,
`geo_precision`, `reference_croisee`, `prudence_methodologique`).

---

## 8. Historique du backfill géographique

### Phase 1 — Backfill Wikidata P625 (PR #28, 2026-05-30)

Source unique : Wikidata P625 (CC0). Script : `tools/wikidata_places_backfill.py`.
Méthode : `wbgetentities` par QID ou titre enwiki. Aucun géocodage texte libre.
**+6 lieux géolocalisés (36 → 42).**

| ID | QID | lat | lng | geo_precision | Fichier |
|----|-----|-----|-----|---------------|---------|
| PLACE-CHORLTONVILLE | Q5105186 | 53.434 | −2.279 | quartier | s20 |
| PLACE-BESWICK | Q4897126 | 53.4743 | −2.20266 | quartier | s20 |
| PLACE-LITTLE-IRELAND | Q10567938 | 53.4731 | −2.2419 | quartier | s20 |
| PLACE-GREENGATE | Q5604052 | 53.4843 | −2.25238 | quartier | s10 |
| PLACE-LUTON-HOSPITAL | Q101277612 | 51.89382 | −0.4753 | exacte | s10 |
| PLACE-GUIDE-BRIDGE | Q5615429 | 53.4744 | −2.1127 | quartier | s35 |

QIDs rejetés : Q49584641 (Angel Meadow Californie) · Q6536190 (Lewis's Liverpool).

### Phase 2 — Curation manuelle (cette PR, 2026-05-31)

Sources primaires et archives citées dans `prudence_methodologique` de chaque lieu.
Aucun géocodage automatique. **+13 lieux géolocalisés (42 → 55) · 2 lieux « coordonnée inconnue ».**

| ID | lat | lng | geo_precision | Source abrégée |
|----|-----|-----|---------------|----------------|
| PLACE-RAFTERS-MANCHESTER | 53.47500 | −2.24080 | exacte | Wikipedia Rafters nightclub |
| PLACE-PENNINE-STUDIOS-OLDHAM | 53.53950 | −2.10540 | rue | Discogs label/309892 |
| PLACE-GREY-MARE | 53.48198 | −2.30548 | exacte | CAMRA pubs/grey-mare-weaste |
| PLACE-NORTH-SALFORD-YOUTH-CLUB | 53.50400 | −2.25670 | rue | Cylex North Salford Civic |
| PLACE-GRAVEYARD-STUDIO | 53.53000 | −2.28600 | quartier | prestwich.org.uk/history |
| PLACE-WHEATHILL-CHEMICAL-WORKS | 53.49900 | −2.26000 | rue | Sumner, Chapter and Verse |
| PLACE-FORT-BESWICK | 53.47430 | −2.20070 | quartier | Dodge / manchester.ac.uk |
| PLACE-PIPS | 53.48480 | −2.24460 | rue | joydiv.org/places |
| PLACE-STONEGROUND-MAYFLOWER | 53.46100 | −2.18200 | rue | manchesterbeat.com |
| PLACE-HARDROCK | 53.45980 | −2.28930 | rue | manchesterbeat.com |
| PLACE-WHITE-CITY | 53.46200 | −2.28700 | rue | Wikipedia White City Stadium |
| PLACE-AUDENSHAW-GRAMMAR-SCHOOL | 53.46669 | −2.11910 | exacte | gias:136273 (GIAS URN) |
| PLACE-ATWELL-AND-JENNERS-MILL | 53.25700 | −2.12480 | rue | Cheshire Archives DRY/5/7 |

Lieux avec **coordonnée inconnue** documentée :
- `PLACE-GREENDOW-COMMERCIALS-STUDIO` — Arrow Studios/Greendow Commercials : aucune adresse fiable retrouvée.
- `PLACE-HODGSONS` — magasin probable à Macclesfield : aucune source de preuve suffisante.

Autorité `gias` : *Get Information About Schools* (service.gov.uk), préfixe admis dans
`reference_croisee` pour les établissements scolaires anglais (URN normalisé).

### Couverture — historique

| Étape | Géolocalisés / Total | % |
|-------|----------------------|---|
| Amorce (PR #27) | 36 / 91 | 40 % |
| Backfill P625 (PR #28) | 42 / 91 | 46 % |
| **Curation manuelle (cette PR)** | **55 / 91** | **60 %** |

Les **36 lieux restants** sans coordonnée sont : 2 venues sans adresse fiable
(ci-dessus), rues ordinaires, lieux symboliques/anonymes, et venues pour lesquelles
aucune source primaire suffisante n'a été retrouvée. Tout ajout ultérieur requiert
une source primaire citée dans `prudence_methodologique`.
