# Étape 9 (point 5) — Refonte de `people-register` sur la charte du hub

*Alignement de `apps/people-register/` sur le gabarit `apps/song-register/`
(charte du hub). Réplication fidèle, structure et charte visuelle reprises avec
un préfixe de classes parallèle `people-*`/`person-*` (miroir de
`songs-*`/`song-*`). Contrôles recalculés depuis la couche canonique, jamais
réinventés.*

## 0. Périmètre respecté

- **DANS** : reconstruction de `index.html`, `style.css`, `app.js`, et nouveau
  `icons.js` (un picto SVG par catégorie). Lecture de la **couche canonique**
  `PERSON-` via `DynamicRegisters`.
- **HORS** : `apps/song-register/` et `apps/lib/dynamic-registers.js` ne sont
  **pas** modifiés → **aucun bump `?v=`** (jeton conservé à `v=7c`, identique à
  song-register). Vue détail `?id=` : **différée** (option par défaut de la
  consigne) ; les cards conservent le « Voir plus » accessible du gabarit.
- `local-editor-links.js` : **non répliqué**. C'est un lien sortant vers
  l'éditeur Songbook privé, spécifique aux chansons ; aucun usage équivalent
  côté acteurs.

## 1. Livrables

| Fichier | Rôle |
|---------|------|
| `apps/people-register/index.html` | Hero + toolbar à facettes + conteneur de sections (classes `people-*`). |
| `apps/people-register/style.css` | Charte du hub répliquée (`--bg #fafaf7`, bleu pétrole `#4c6e7a`, hero, toolbar, sections, cards, badges, tags, « Voir plus », états). |
| `apps/people-register/app.js` | Groupage par catégorie, facettes croisées (boucle de stabilisation), pictos, export CSV, « Voir plus ». |
| `apps/people-register/icons.js` | `window.PeopleIcons` — un picto SVG 24×24 par catégorie + libellés + ordre. |

## 2. Données (lues via `DynamicRegisters`, jamais recalculées)

- **Couche canonique uniquement** : le loader renvoie 433 enregistrements
  `kind=person` (chemin `registers/people/`), dont **204 `PERSON-`** canoniques
  (166 de #47 + 38 `origine=auteur_source`) et ~229 provisoires `PERS-*`/
  `PERSONNE-`. `app.js` **filtre sur le préfixe d'identifiant `PERSON-`** : la
  couche provisoire atomisée est ignorée.
- **Champs par acteur** : nom canonique, `alt_names`, `categorie` (7 valeurs),
  `sources`, chapitres, et **nombre de citations attribuées** (lu depuis
  `registers/relations/attribution_edges.json`, prédicat `attribuee_a`).
- **Exclusions** : les non-personnes (`pending_org.json` — Bedhead, Buzzcocks,
  Minny Pops, Oz PA, HM Treasury, Happy Mondays ; `pending_concept.json` —
  Perry Boys) ne sont pas des `PERSON-` et sont donc **exclues par
  construction**. Vérifié : 0 occurrence de chacune dans la liste rendue.

## 3. Toolbar (miroir song, adapté)

| Facette | Détail |
|---------|--------|
| Recherche | nom canonique **+ `alt_names`** + rôles + sources + chapitres |
| Catégorie | les **7 valeurs** (`membre`, `entourage`, `industrie`, `critique_journaliste`, `auteur_secondaire`, `influence`, `theoricien_mobilise`) |
| Source | racines `SXX` |
| Chapitre | si rattachement disponible |

Boutons **Réinitialiser** + **Exporter CSV** + compteur de résultats. Les
anciennes facettes **« Rôle »** (remplacée par `categorie`) et **« Entité
associée »** (relève des `liens`, étape 12) sont **retirées**. Les facettes se
croisent (chaque select n'offre que les valeurs présentes sous les autres
filtres actifs), exactement comme song-register.

## 4. Groupage, sections et cards

- Les 204 personnes sont groupées par `categorie` en **7 sections**, chacune
  avec **picto + compteur**, dans l'ordre imposé : membre, entourage, industrie,
  critique_journaliste, auteur_secondaire, influence, theoricien_mobilise.
- **Carte personne** (miroir carte chanson) : picto de catégorie, nom canonique,
  libellé de catégorie, badges (nombre de citations attribuées, nombre de
  sources, drapeau « à arbitrer » le cas échéant), `alt_names` en ligne, et un
  « Voir plus » dépliant (formes du nom en badges, sources, chapitres, rôles
  observés). Ancre `id` = identifiant `PERSON-`. Identifiant canonique révélé au
  survol.

## 5. Robustesse / parité (12b) — contrôle visuel et de données

Simulation Node de la chaîne exacte de rendu (extraction + groupage + génération
du HTML des cards) contre les fichiers canoniques réels :

| Contrôle | Attendu | Obtenu |
|----------|:-------:|:------:|
| Personnes affichées | 204 | **204** |
| Somme des compteurs de catégorie | 204 | **204** |
| membre / entourage / industrie | 4 / 53 / 43 | **4 / 53 / 43** |
| critique_journaliste / auteur_secondaire | 12 / 67 | **12 / 67** |
| influence / theoricien_mobilise | 11 / 14 | **11 / 14** |
| Catégories inattendues | 0 | **0** |
| Cards rendues / sections / « Voir plus » | 204 / 7 / 204 | **204 / 7 / 204** |
| Non-personnes (7 entités) dans la liste | 0 | **0** |
| Fuites `undefined` / `[object Object]` / `NaN` | aucune | **aucune** |
| Citations attribuées (Hook / Deborah / Curtis) | 254 / 115 / 18 | **254 / 115 / 18** |
| `alt_names` (Sumner → Albrecht, Dicken) | présents | **présents** |

Les compteurs par catégorie sont **strictement cohérents** avec l'export
canonique (parité SSOT, aucun recomptage divergent : la page lit la donnée, ne
la recalcule pas). Champs manquants gérés sans casser le rendu (badge « aucune
citation », sections omises si vides). Responsive (1/2/3 colonnes à 720/1024 px)
et accessibilité (labels de facettes, `:focus-visible`, contrastes, `aria-expanded`
sur « Voir plus`) à parité avec song-register.

## 6. Non-régression

- `apps/song-register/` et `apps/lib/dynamic-registers.js` : **0 modification**
  (jeton `?v=7c` inchangé).
- `index.html`, `app.js` : **aucune** ancienne classe (`hero`/`layout`/`toolbar`
  bare, `role-filter`, `entity-filter`, `person-period`) résiduelle.
- `node --check` : `app.js` et `icons.js` syntaxiquement valides.

## 7. Lien de la PR

<!-- PR_LINK -->
_À compléter à l'ouverture de la PR `claude/etape9-page-people-refonte`._
