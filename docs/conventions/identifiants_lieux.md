# Identifiants de lieux — schéma gelé (étape 12b-1.c)

> Proposition arrêtée et figée dans le cadre de l'étape 4 de la ROADMAP
> (« Carte des lieux »). Pensée pour **survivre** à la spécification
> cross-registres (étape 5) et aux croisements ultérieurs : concerts
> (étape 10), maillage profond (étape 11).
>
> Contrainte doctrinale : `docs/SCHEMA_FREEZE_POLICY.md` interdit le renommage
> des identifiants stabilisés. Ce document atteint la stabilité **sans
> renommer** — par convention canonique + arête d'équivalence additive.

---

## 1. Forme canonique

```text
PLACE-<SLUG>
```

- `<SLUG>` est **source-agnostique** : il dénote un lieu physique, jamais la
  source qui l'atteste ;
- un lieu attesté par plusieurs sources → **un seul** identifiant canonique
  (ex. `PLACE-HULME` documenté par S02, S06, S20) ;
- motif de schéma : `^PLACE-[A-Z0-9][A-Z0-9-]*$`.

Règle de canonicalisation déterministe : voir `docs/NAMING_CONVENTIONS.md` §10.

### Pourquoi source-agnostique

Un identifiant qui encode sa source (`PLACE-S83-001`) **se fragmente** dès qu'un
second auteur décrit le même lieu : on obtient autant d'identifiants que de
sources pour une même réalité géographique. C'est précisément ce qui casse :

- la **carte** (une punaise par identifiant → doublons visuels) ;
- les **croisements** (un concert au Free Trade Hall doit pointer un seul lieu) ;
- le **maillage** (étape 11 : un nœud par lieu, pas un par mention).

Le slug source-agnostique est donc la condition de la « cross-readiness ».

---

## 2. État des lieux (audit du 30/05/2026)

Trois conventions coexistaient dans le corpus :

| Convention | Exemple | Origine | Statut |
|------------|---------|---------|--------|
| **slug v2** (canonique) | `PLACE-TJ-DAVIDSONS` | atomisation v2 (S02, S05, S06, S10, S20), S13, S35 | ✅ retenue |
| scoping-source | `PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET` | S41 | legacy, conservé |
| positionnel | `PLACE-S83-001` | S83 | legacy, conservé |

Détail complet : `docs/audits/audit_unitaire_lieux_12b-1c.md`.

Le gel **interdit de renommer** les formes legacy. On les **conserve** et on les
rattache au canonique par `same_as`.

---

## 3. `same_as` — arête d'équivalence

Champ optionnel, **ajout rétrocompatible** (autorisé par le gel). Porté
**uniquement** par un enregistrement non canonique :

```yaml
# registers/s83_hannett_architecture_specialized_registers.md
id: PLACE-S83-001
label: "Little Peter Street — T.J. Davidson's studio"
same_as: PLACE-TJ-DAVIDSONS   # → lieu canonique
```

### Invariants (vérifiés en CI)

| Code | Invariant | Sévérité / imposé par |
|------|-----------|-----------------------|
| — | **append-only** : le legacy pointe vers le canonique ; le canonique n'est jamais muté | revue + convention |
| — | **mono-valué** : `same_as` est une chaîne (une seule cible), jamais un tableau | `schemas/places.schema.yaml` |
| INV-1 | **cible existante** : `same_as` pointe vers un id de lieu présent | erreur — `tools/validate_places.py` |
| INV-2 | **absence de cycle** | erreur — idem |
| INV-3 | **canonique = point fixe** : la cible ne porte pas elle-même de `same_as` | erreur — idem |
| INV-4 | **convergence unique** : toute chaîne résout vers un canonique unique | erreur — idem (défensif) |
| INV-5 | référence `PLACE-*` cross-registre résoluble | avertissement — **TODO** (résolu au runtime par le loader) |
| INV-6 | deux canoniques ≠ coordonnées identiques sans justification | avertissement — idem |

Clôture transitive (A→B, B→C ⇒ A,B,C fusionnent sur C) : union-find, côté
validateur **et** loader. Tests : `tools/test_validate_places.py` (INV-1..4,
cas passant + cas en échec, incl. le cas réel T.J. Davidson).

### Résolution (union-find)

`apps/lib/dynamic-registers.js` construit la carte `id → représentant
canonique` par suivi des arêtes `same_as` jusqu'au point fixe, puis groupe les
enregistrements **par représentant** (et non par id brut). La composante
fusionne en une seule entrée :

- `id`, `label`, `type` : pilotés par le **canonique** ;
- `sources`, `chapters`, `atoms`, `song_ids`, `usage`, `prudence` : **union** ;
- `lat`/`lng`/`geo_precision`/`reference_croisee`/`prudence_methodologique` :
  **coalescés**, portés par le canonique (cf. §4).

### Équivalences actuelles

```text
PLACE-S83-001                               → PLACE-TJ-DAVIDSONS
PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET  → PLACE-TJ-DAVIDSONS
PLACE-S83-002                               → PLACE-HULME-CRESCENTS
```

Décompte : **83** identifiants distincts → **80** lieux canoniques.

---

## 4. Coordonnées attachées au canonique

Les coordonnées (étape carto) sont portées par l'enregistrement **canonique**,
jamais par un legacy. La réconciliation `same_as` précède l'attachement : on
géolocalise un lieu, pas une mention. Détail : `docs/conventions/carte_lieux_12b-1c.md`.

---

## 5. Cross-readiness — ce qui est gelé pour les étapes 5/10/11

Ce schéma livre, **a minima sur les identifiants** et **sans implémenter le
maillage** (réservé à l'étape 11) :

1. un **espace d'identifiants canonique stable** (`PLACE-<SLUG>`), cible unique
   et durable pour toute référence entrante (un concert → un lieu) ;
2. une **arête d'équivalence** (`same_as`) déjà résolue en clôture transitive —
   primitive directement réutilisable par la spécification cross-registres
   (étape 5) ;
3. un **point d'ancrage d'autorité externe** (`reference_croisee`, ex. QID
   Wikidata) pour les rapprochements futurs.

Ce qui n'est **pas** fait ici (et ne doit pas l'être) : les liens bidirectionnels
riches lieux ↔ concerts ↔ personnes ↔ … (maillage, étape 11).

---

## 6. Procédure pour un nouveau lieu

1. forme canonique `PLACE-<SLUG>` (règle §10 des conventions de nommage) ;
2. si le lieu existe déjà sous un autre id : **ne pas créer de doublon** —
   réutiliser le canonique, ou poser `same_as` si l'id pré-existant est legacy ;
3. `python3 tools/validate_places.py` doit passer (schéma + `same_as`).
