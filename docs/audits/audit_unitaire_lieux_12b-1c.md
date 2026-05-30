# Audit unitaire — registre des lieux (préalable à l'étape 12b-1.c)

> Audit **préalable à tout enrichissement**, conformément à la contrainte de
> l'étape 4 : on inspecte l'existant (entrées manuelles anciennes vs atomisées
> v2) **avant** de poser la couche cartographique.
>
> Date : 30/05/2026. Périmètre : `registers/**/*.md`, lus comme le fait le
> runtime (`apps/lib/dynamic-registers.js`) et `tools/validate_places.py`.

---

## 1. Volumétrie

| Mesure | Valeur |
|--------|-------:|
| Enregistrements-source de lieux (parasites d'en-tête exclus) | 91 |
| Identifiants distincts (après dédup par id) | 83 |
| **Lieux canoniques** (après réconciliation `same_as`) | **80** |
| Alias legacy résolus (`same_as`) | 3 |
| Lieux géolocalisés (amorce) | 37 |

Répartition canonique par famille : `ville` 17, `salle` 14, `quartier` 13,
`habitat` 10, `studio` 9, `education` 7, `commerce` 7, `lieu_memoire` 4,
`industrie` 3, `sante` 1, `science` 1, `infrastructure` 1, `pouvoir` 1.

---

## 2. Manuelles anciennes vs atomisées v2

| Famille de fichier | Enreg. | Format d'id | Champs typiques |
|--------------------|-------:|-------------|-----------------|
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
```

Loader et validateur résolvent la clôture transitive (union-find). Décompte :
83 → **80** lieux canoniques.

---

## 4. Doublons écartés (faux positifs — à NE PAS fusionner)

Granularités délibérément distinctes, conservées séparées (documenté pour éviter
une fusion abusive ultérieure) :

- `PLACE-MANCHESTER` / `PLACE-MANCHESTER-CITY` / `PLACE-MANCHESTER-CENTRE` /
  `PLACE-GREATER-MANCHESTER` / `PLACE-MANCHESTER-GLOBAL-MEMORY` — échelles
  urbaines et registres sémantiques distincts (ville, centralité, comté,
  réception mémorielle) ;
- `PLACE-FREE-TRADE-HALL` vs `PLACE-LESSER-FREE-TRADE-HALL` — **deux salles**
  (le grand hall et la petite salle), même bâtiment, événements distincts (le
  Lesser FTH = concert Sex Pistols de 1976). Coordonnée partagée, identifiants
  séparés.

---

## 5. Legacy singletons non conformes — conservés en l'état

Ids legacy **sans doublon** (aucun canonique équivalent à réconcilier). Le gel
**interdit le renommage** ; ils restent valides et référençables. Les futurs
enregistrements, eux, suivent la forme canonique.

- `PLACE-S41-SWAN-PUB-ECCLES-NEW-ROAD` (Swan pub, Eccles New Road) ;
- `PLACE-S83-003` (Ferranti's manufacturing plant) ;
- `PLACE-S83-004` (Salford Technical School).

---

## 6. Couche cartographique (amorce)

- 37 lieux géolocalisés (lat/lng WGS84), précision honnête par lieu
  (`geo_precision`), provenance Wikidata P625 (`reference_croisee`, QID à
  confiance élevée), prudences pour lieux démolis / approximatifs.
- Coordonnées attachées au lieu **canonique**, après réconciliation.
- Détail : `docs/conventions/carte_lieux_12b-1c.md`.

---

## 7. Conformité

`python3 tools/validate_places.py` :

```text
Source place records (parasites excluded) : 91
Distinct ids after id-deduplication        : 83
  dont alias legacy (same_as)              : 3
Canonical places after same_as merge       : 80
Valid against schema                        : 91/91
All place records are valid (schéma + same_as).
```

Aucune donnée documentaire existante n'a été modifiée : les seuls ajouts sont
des champs **optionnels rétrocompatibles** (`same_as`, `lat`/`lng`,
`geo_precision`, `reference_croisee`, `prudence_methodologique`).
