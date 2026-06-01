# ROADMAP — Joy Division, AI Writing Studio

> Suivi de la trajectoire de refonte des registres canoniques. Style sobre,
> présent de l'indicatif. Ce fichier est le point d'entrée de l'avancement ; il
> renvoie aux rapports détaillés (`docs/canon/`, `docs/audits/`) et aux PR.
>
> Convention : une étape est **terminée (données)** quand sa couche canonique
> est gelée, validée par une porte gate-able et une sentinelle anti-drift, et
> mergée sur `main`. La refonte de page associée peut rester **en revue** sans
> bloquer la donnée.

---

## État synthétique

| Étape | Objet | Statut |
|-------|-------|--------|
| 4 | Lieux (`PLACE-`) | terminée |
| 6 | Chronologie (`EVENT-`) | terminée |
| 7 | Concerts (`CONCERT-`) | terminée |
| 8 | Citations (`QUOTE-`) — backbone & attribution | terminée |
| **9** | **Acteurs (`PERSON-`)** | **terminée (données) ; page en revue** |
| **10** | **Organisations (`ORG-`)** | **à lancer** |
| 11 | Maillage profond (`liens` transversaux, concepts) | à venir |
| 12 | Relations fines (entités associées, `liens` PERSON↔ORG) | à venir |

---

## Étape 9 — Registre des acteurs (`PERSON-`) — TERMINÉE (données)

Refonte de la couche provisoire `PERS-*` (atomisée) en un registre canonique
`PERSON-` gelé, puis câblage des attributions de citations et refonte de la page
publique.

- **PR #46** — audit en lecture seule de la couche provisoire `PERS-*`
  (`docs/audits/etape9_personnes_audit.md`). Aucune écriture de donnée :
  inventaire, grappes de doublons, cas sensibles.
- **PR #47** — canonicalisation : **166 `PERSON-`** (slugs sémantiques,
  `same_as` vers la couche `PERS-*`, `alt_names`, champ `categorie`). 5
  collectifs renvoyés vers `pending_org` ; Perry Boys vers `pending_concept`.
  Invariant **`INV5`** : « Kevin Curtis » (père) ≠ « Ian Curtis ».
- **PR #48** — câblage `citation → attribué_à → PERSON-` : total **204
  `PERSON-`** (166 + 38 `origine=auteur_source`), couverture **962/962** des
  citations, **0 arête pendante**. Prédicats XR `attribuee_a`,
  `a_pour_auteur_source`, `rapportee_par`. Sentinelle anti-drift à **double
  passage** (garde anti-récidive). Rapport :
  `docs/canon/etape9_cablage_attribution.md`.
- **PR #49** — refonte de la page `apps/people-register/` sur la charte du hub
  (miroir `song-register`, classes `people-*`/`person-*`, 7 catégories, pictos
  SVG, export CSV) — **en revue**. Rapport :
  `docs/canon/etape9_page_people_refonte.md`.

### Résidus tracés (non bloquants)

- **52** `categorie_a_arbitrer` — catégorie d'acteur à confirmer.
- **4** `a_arbitrer` — Stephanie, Eddy, Oz, Jasmine (identités à trancher).
- `pagination_papier` S41/S45 à vérifier ou annuler (drift exports).

---

## Étape 10 — Organisations (`ORG-`) — À LANCER

Promotion des entités collectives et morales en un registre canonique `ORG-`,
sur le modèle éprouvé des étapes 7 à 9 (identité gelée, `same_as`, porte
gate-able, sentinelle anti-drift).

- **Intrants prêts** :
  - `registers/people/pending_org.json` — Bedhead, Buzzcocks, Minny Pops,
    Oz PA, HM Treasury, Happy Mondays ;
  - `registers/people/pending_concept.json` — Perry Boys.
- **Périmètre** : labels, groupes, salles-organisations, institutions, équipes.

---

## Rubrique 12b — audits unitaires & parité des registres

Travail transverse de vérification unitaire (existant manuel ancien vs atomisé
v2) **préalable à tout enrichissement**, et de parité SSOT entre données et
pages publiques.

| Sous-lot | Registre | Rapport |
|----------|----------|---------|
| 12b-1.c | Lieux | `docs/audits/audit_unitaire_lieux_12b-1c.md`, `docs/conventions/carte_lieux_12b-1c.md` |
| 12b-3 | Chronologie | `docs/audits/audit_unitaire_chronologie_12b-3.md` |
| 12b-4 | Concerts | `docs/audits/audit_unitaire_concerts_12b-4.md` |
| 12b-5 | Citations | `docs/audits/audit_unitaire_citations_12b-5.md` |

Principe : la page publique affiche exactement les volumes de l'export canonique
(parité SSOT, aucun recomptage divergent) ; les champs manquants sont gérés sans
casser le rendu.
