# Couche cartographique des lieux — plan (étape 12b-1.c)

> Achève le registre des lieux par une couche carto : géolocalisation et
> visualisation des venues, studios et lieux-clés de l'univers Joy Division.
> Couche **additive** sur le registre existant ; aucune donnée documentaire
> n'est altérée.

---

## 1. Source des coordonnées

**Vérité = curation manuelle**, amorcée et recoupée depuis **Wikidata**
(propriété **P625** *coordinate location*, données **CC0** — stockables sans
attribution).

- **Pas de géocodage live au build.** Les coordonnées sont des **données
  commitées** (dans les fiches de lieux), reproductibles, sans dépendance
  réseau à l'exécution.
- Chaque coordonnée porte une **provenance et une honnêteté de précision** :

| Champ | Rôle |
|-------|------|
| `lat`, `lng` | degrés décimaux WGS84 |
| `geo_precision` | granularité ordinale : `exacte` < `rue` < `quartier` < `ville` < `region` (axe distinct de la confiance) |
| `reference_croisee` | tableau d'identifiants préfixés par autorité, ex. `["wikidata:Q204686"]` (`musicbrainz:place:…`, `osm:node:…`) |
| `prudence_methodologique` | lieu démoli, coordonnée approximative, désambiguaïsation, QID à recouper |

- La coordonnée s'attache au lieu **canonique**, après réconciliation `same_as`
  (cf. `docs/conventions/identifiants_lieux.md`). On géolocalise un lieu, pas
  une mention.

### Périmètre de la couche (après backfill 2026-05-30)

La couche couvre **42 lieux identifiables** (venues JD majeures + quartiers /
villes / régions nettement localisables). Les lieux à localisation incertaine
restent **sans coordonnées** (honnêteté > exhaustivité) : ils n'apparaissent pas
sur la carte mais demeurent dans le registre.

Deux scripts de curation, traçables et idempotents :
- `tools/_seed_places_geo.py` — amorce initiale (PR #27, 36 lieux)
- `tools/wikidata_places_backfill.py` — backfill Wikidata P625 (session 2026-05-30, +6 lieux)

QID `reference_croisee` posé **uniquement à confiance élevée** (20 lieux
appréciable après backfill). Chaque QID vérifié manuellement via
`wbgetentities` (P625 rapatrié, plausibilité géographique contrôlée).

### Rendu : points vs zones

Les granularités fines (`exacte`, `rue`, `quartier`) sont des **venues précises**
→ punaises ponctuelles. Les granularités grossières (`ville`, `region`) sont des
**zones** (étendues, non ponctuelles) → cercles translucides, dans une **couche
séparée et activable** (toggle), exclues des punaises, avec entrée de légende. Le
seuil grossier est une constante unique (`COARSE_PRECISIONS`), partagée entre
`app.js` (rendu) et `validate_places.py` (exemption INV-6). Détail : convention
`docs/NAMING_CONVENTIONS.md` §10.8.

---

## 2. Fond de carte

**OpenStreetMap** (tuiles standard) via **Leaflet 1.9.4**.

- Leaflet chargé depuis le CDN **jsdelivr** — même hôte que `js-yaml` déjà
  utilisé par `apps/lib/dynamic-registers.js` (cohérence, aucune nouvelle
  origine réseau introduite côté infra).
- Tuiles : `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`, attribution
  « © OpenStreetMap » affichée (exigence de licence ODbL).
- Vue initiale centrée sur Manchester (`53.4808, -2.2426`), recadrage
  automatique (`fitBounds`) sur le jeu filtré.

---

## 3. Intégration dans `apps/places-register`

Couche posée **sans rien retirer** de l'app liste existante.

| Fichier | Ajout |
|---------|-------|
| `index.html` | feuille Leaflet (CDN) ; bascule **Liste / Carte** ; conteneur `#places-map` ; note de provenance |
| `app.js` | init Leaflet **paresseuse** (au 1er passage en vue carte) ; marqueurs des lieux géolocalisés du **jeu filtré courant** ; popups (titre, type, usage, précision, prudence, sources) ; recadrage ; compteur « N/M géolocalisés » |
| `style.css` | conteneur carte, épingles (picto de famille réutilisé d'`icons.js`), popups, bascule de vue |

Principes :

- **Filtres partagés** : recherche, type, détail, source, chapitre filtrent
  liste **et** carte (mêmes facettes, même `matches()`).
- **Marqueurs canoniques** : la carte consomme les enregistrements déjà
  dédupliqués + réconciliés `same_as` par le loader → une punaise par lieu.
- **Picto par famille** : l'épingle réutilise le SVG de `PlaceIcons` (cohérence
  visuelle liste ↔ carte).
- **Dégradation propre** : un lieu sans `lat`/`lng` est simplement absent de la
  carte ; aucune erreur.

---

## 4. Validation

`tools/validate_places.py` (CI) couvre désormais :

- schéma JSON (Draft 2020-12, `FormatChecker`), incluant les bornes
  `lat ∈ [-90, 90]`, `lng ∈ [-180, 180]` et l'énum `geo_precision` ;
- intégrité `same_as` (cible existante, point fixe, absence de cycle) ;
- décompte canonique post-réconciliation.

---

## 5. Hors-périmètre (réservé aux étapes ultérieures)

- maillage bidirectionnel lieux ↔ concerts ↔ personnes ↔ … → **étape 11** ;
- croisement avec les 196 concerts → **étape 10** ;
- *backfill* exhaustif des coordonnées restantes (49/91 non géolocalisés après
  session 2026-05-30) → suivi réseau-dépendant, sources historiques ou Wikidata
  P625 si disponible.
