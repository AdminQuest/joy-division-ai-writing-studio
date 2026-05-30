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
  réseau à l'exécution. *(L'environnement de cette PR n'a d'ailleurs pas accès à
  `query.wikidata.org` — host hors allowlist : le recoupement live est par
  construction hors-bande.)*
- Chaque coordonnée porte une **provenance et une honnêteté de précision** :

| Champ | Rôle |
|-------|------|
| `lat`, `lng` | degrés décimaux WGS84 |
| `geo_precision` | granularité ordinale : `exacte` \| `rue` \| `quartier` \| `ville` (axe distinct de la confiance) |
| `reference_croisee` | tableau d'identifiants préfixés par autorité, ex. `["wikidata:Q204686"]` (`musicbrainz:place:…`, `osm:node:…`) |
| `prudence_methodologique` | lieu démoli, coordonnée approximative, désambiguïsation, QID à recouper |

- La coordonnée s'attache au lieu **canonique**, après réconciliation `same_as`
  (cf. `docs/conventions/identifiants_lieux.md`). On géolocalise un lieu, pas
  une mention.

### Périmètre du seed (amorce)

L'amorce couvre **37 lieux identifiables** (repères JD majeurs + villes /
quartiers nettement localisables). Les lieux à localisation incertaine restent
**sans coordonnées** (honnêteté > exhaustivité) : ils n'apparaissent pas sur la
carte mais demeurent dans le registre. Le script d'amorce, traçable, est
`tools/_seed_places_geo.py` (idempotent).

QID `reference_croisee` posé **uniquement à confiance élevée** (11 lieux). Le
*backfill* des QID restants est un **suivi réseau-dépendant** (nécessite l'accès
à Wikidata), explicitement hors-périmètre de cette PR.

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
- *backfill* exhaustif des QID Wikidata et complétion des coordonnées des lieux
  restants → suivi réseau-dépendant.
