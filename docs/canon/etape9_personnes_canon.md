# Étape 9 — Canonicalisation du registre `PERSON-`

*Construction du registre canonique des acteurs `PERSON-` à partir de la couche
provisoire `PERS-*`, selon l'arbitrage validé. Tous les chiffres ci-dessous sont
recalculés depuis les artefacts générés (`registers/people/00_canonical_people.md`,
`exports/generated/people.json`, `pending_org.json`, `pending_concept.json`) —
aucun n'est patché à la main.*

## 0. Politiques appliquées

- **Gel additif.** Aucun id `PERS-*` n'est renommé ni supprimé. Chaque `PERS-*`
  devient un alias résolu, porté en `same_as` par l'enregistrement canonique
  `PERSON-`. La couche provisoire (`registers/people/*.md`, `people.json`)
  persiste telle quelle — `people.json` contient désormais **les deux** strates
  (305 `PERS-*` + 166 `PERSON-`).
- **SSOT.** Une seule normalisation : `tools/build_people_canon.py`. Le
  validateur et la sentinelle anti-drift rejouent ce générateur et comparent ;
  toute divergence substantielle échoue.
- **Convention d'identité.** `PERSON-` + slug sémantique du nom civil le plus
  complet et usuel ; toutes les autres formes (variantes, noms de scène, noms de
  naissance) → `alt_names`.
- **Exécuter le clair, flagger l'ambigu.** Aucune fusion forcée : tout doublon
  ou rattachement non certain est marqué `a_arbitrer` ; toute double
  appartenance catégorielle est marquée `categorie_a_arbitrer`.

## 1. Livrables

| Livrable | Chemin |
|----------|--------|
| Registre canonique `PERSON-` (généré, ingéré comme `person`) | `registers/people/00_canonical_people.md` |
| Schéma exécutable Draft 2020-12 (FORMAT_CHECKER) | `schemas/person_canonical.schema.json` |
| Extension additive du validateur de champs | `tools/schema_validation.py` (`person_canonical`) |
| Générateur SSOT déterministe | `tools/build_people_canon.py` |
| Validateur gate-able + sentinelle anti-drift | `tools/validate_people.py` (`--check-drift`) |
| Hand-off `ORG-` (étape 10) | `registers/people/pending_org.json` |
| Hand-off concept (étape 10) | `registers/people/pending_concept.json` |
| Aiguillage build `PERSON-` → `person` | `tools/build_registers.py` (`infer_kind`) |

> Le câblage `citation → attribué_à` (arête `PERSON-` sur les 962 citations)
> reste **hors périmètre** (PR suivante) ; il est seulement préparé par les
> `same_as` et la partition des locuteurs établie à l'audit.

## 2. Synthèse chiffrée

| Indicateur | Valeur |
|------------|:------:|
| `PERSON-` canoniques | **166** |
| dont issus d'un éclatement d'entité mixte (id neuf) | 3 |
| Liens `same_as` câblés (ids `PERS-*` rabattus) | **299** |
| `alt_names` (formes secondaires) | 25 |
| Renvois `ORG-` (hand-off) | 4 |
| Renvois concept (hand-off) | 1 |
| Items `a_arbitrer` | 4 |
| `categorie_a_arbitrer` (double appartenance) | 52 |

### Répartition par `categorie`

| Catégorie | Nb |
|-----------|:--:|
| industrie | 43 |
| entourage | 53 |
| auteur_secondaire | 29 |
| theoricien_mobilise | 14 |
| critique_journaliste | 12 |
| influence | 11 |
| membre | 4 |

`membre` = Ian Curtis, Bernard Sumner, Peter Hook, Stephen Morris.
`influence` = Burroughs, Ballard, Proust, Gogol, Nietzsche, Schopenhauer,
Blanchot, Brion Gysin, Daniel Odier, David Bowie, David Byrne.

## 3. Identité de partition (vérifiée)

Les **305** identifiants `PERS-*` distincts de `people.json` se répartissent
**exactement** et sans recouvrement (hors les 2 entrées mixtes, comptées dans
leur éclatement) :

```
305 = 299 (same_as câblés)
    +   3 (PERS-016, PERS-S76-068, PERS-S76-071 → ORG- seul)
    +   1 (PERS-S76-082 → concept)
    +   2 (PERS-S76-052, PERS-S76-064 → entrées mixtes éclatées)
```

Contrôle automatique (`tools/validate_people.py`) : `MISSING = []`,
`EXTRA = []`. Chaque `PERS-*` est rabattu sur **au plus un** `PERSON-`
(pas de double rattachement).

## 4. Déduplications arbitrées (consigne §2)

| Décision | Résolution appliquée |
|----------|----------------------|
| **John Anderson** (4 id) | **Fusion** → `PERSON-john-anderson`. Contrôle source effectué : `PERS-S45-JOHN-ANDERSON` décrit un « producteur / investisseur du projet RCA / Arrow » — **même circuit RCA/Grapevine** que les autres id. Aucun second John Anderson dans un contexte distinct ⇒ fusion sans réserve. |
| **« Steve Morris »** `PERS-S76-021` | Fusionné dans `PERSON-stephen-morris` ; « Steve Morris » en `alt_names`. |
| **T.J. Davidson** `PERS-S75-025` ↔ **Tony Davidson** `PERS-S76-051` | `same_as` ; « T.J. Davidson » + « T. J. Davidson » en `alt_names` ; nom canonique « Tony Davidson ». |
| **Eddie Garrity / Ed Banger** `PERS-S76-040` | Pas de fusion (id unique) → `PERSON-eddie-garrity` ; « Ed Banger » en `alt_names`. |

## 5. Doublons manqués par la détection — intégrés (consigne §3)

| Fusion | `alt_names` | Cible |
|--------|-------------|-------|
| `PERS-010` « Annick Honoré » | « Annick Honoré » | `PERSON-annik-honore` |
| `PERS-S29-008` « Franco Berardi » ↔ `PERS-S31-002` « Franco Berardi Bifo » | « Franco Berardi Bifo », « Bifo » | `PERSON-franco-berardi` (`theoricien_mobilise`) |
| `PERS-S21-003` ↔ `PERS-S77-007` « Andy Zero / Andy Waide » | « Andy Waide » | `PERSON-andy-zero` |
| `PERS-S76-009` « Deborah Woodruff » | « Deborah Woodruff » | `PERSON-deborah-curtis` |

**`PERS-S45-STEPHANIE-MORRIS` (« Stephanie ») — NON rattachée d'office.**
Contrôle source (S45) : « compagne de Stephen Morris avant sa séparation ;
figure d'un épisode trouble rapporté par Deborah ». C'est une **personne réelle
distincte** (pas un artefact de segmentation de « Stephen Morris »), mais au nom
incomplet ⇒ `PERSON-stephanie` propre, marqué **`a_arbitrer`**, tenu distinct de
`PERSON-stephen-morris`.

## 6. Éclatement des entités mixtes (consigne §4)

- **`PERS-S76-052` « Oz PA / Eddy et Oz »** :
  - « Oz PA » → hand-off `ORG-` (`pending_org.json`, `from_pers: PERS-S76-052#oz-pa`) ;
  - « Eddy » → `PERSON-eddy-oz-pa` (`a_arbitrer`, nom incomplet) ;
  - « Oz » → `PERSON-oz-oz-pa` (`a_arbitrer`, nom incomplet).
- **`PERS-S76-064` « Dave Pils et Jasmine »** :
  - « Dave Pils » → `same_as` du `PERSON-dave-pils` existant (issu de
    `PERS-S76-077`), via le marqueur de composante `PERS-S76-064#dave-pils` ;
  - « Jasmine » → `PERSON-jasmine` neuf (`a_arbitrer`, nom incomplet).

Les **4 items `a_arbitrer`** sont donc : `PERSON-eddy-oz-pa`, `PERSON-oz-oz-pa`,
`PERSON-jasmine`, `PERSON-stephanie`.

## 7. Cas sensibles (consigne §6)

- **`PERS-S76-003` « Kevin Curtis »** → `PERSON-kevin-curtis`, **DISTINCT** de
  `PERSON-ian-curtis` (père de Ian *Kevin* Curtis). Jamais fusionné — invariant
  `INV5` du validateur l'interdit explicitement.
- **Bernard Sumner** → `PERSON-bernard-sumner` ; « Bernard Albrecht » et
  « Bernard Dicken » en `alt_names`, **sans identifiant concurrent** (aucun
  `PERS-*` ne les porte).
- **William S. Burroughs** → un seul `PERSON-william-s-burroughs`,
  `categorie=influence`, ses 3 id (`PERS-S54-003`, `PERS-S56-004`,
  `PERS-S75-033`) en `same_as`.

## 8. Typage (consigne §5)

`categorie` (ajout additif, vocabulaire fermé) affecté par priorité aux classes
non-actrices (`influence`, `theoricien_mobilise`, `membre`, `auteur_secondaire`),
puis aux classes actrices où **le rôle professionnel l'emporte sur le lien de
parenté/amitié** (un manager est `industrie`, pas `entourage`). Les doubles
appartenances (critique ET auteur, industrie ET proche) retiennent la catégorie
**primaire** et lèvent `categorie_a_arbitrer` (**52** cas, non bloquants).

### Hand-offs (NE PAS créer ici)

`pending_org.json` : Bedhead (`PERS-016`), Buzzcocks (`PERS-S76-068`),
Minny Pops (`PERS-S76-071`), **Oz PA** (issu de `PERS-S76-052`).
`pending_concept.json` : Perry Boys (`PERS-S76-082`, sous-culture — ni `ORG-`
ni `PERSON-`).

## 9. Validation et anti-drift

```bash
python3 tools/build_registers.py --strict     # errors=0 ; PERSON- ⇒ people.json (166)
python3 tools/validate_people.py               # INV1..INV5 ; exit 0
python3 tools/validate_people.py --check-drift # + sentinelle SSOT ; exit 0
python3 tools/check_generated_sync.py          # sentinelle globale ; « 597 artefacts en phase »
```

Invariants du validateur : **INV1** schéma + vocabulaire fermé · **INV2**
`same_as` résout vers un `PERS-*` existant, jamais vers un `PERSON-` ·
**INV3** partition (≤ 1 rattachement, couverture exhaustive, pas de fantôme) ·
**INV4** unicité id + slug · **INV5** Kevin Curtis jamais fusionné dans Ian
Curtis · **SSOT** registre committé == sortie déterministe du générateur. Le
générateur est **idempotent** (rebuild → regénère à l'identique) et n'ingère que
la couche `PERS-*` (jamais sa propre sortie `PERSON-`).

## 10. Lien de la PR

Pull request : **[https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/47](https://github.com/AdminQuest/joy-division-ai-writing-studio/pull/47)** (branche `claude/etape9-canon-personnes` → `main`). Revue automatique `@codex review` déclenchée à l'ouverture. **Ne pas merger** (le merge reste gaté).
