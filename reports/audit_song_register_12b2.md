# AUDIT PRÉALABLE — Registre public des chansons (`apps/song-register/`) — étape 12b-2

- **Date :** 29 mai 2026
- **Auteur :** Audit conduit par Claude (session collaborative avec Fabrice)
- **Statut :** référence pour la roadmap 12b-2 (refonte registre des chansons)

> Audit en lecture pure. Aucune modification de code applicatif effectuée. Tous les chiffres sont vérifiés sur les sources locales des 4 repos (`joy-division-ai-writing-studio`, `-releases`, `-collection`, `-studio-private`).

---

## SECTION 1 — Structure du code (Phase 1)

### Arborescence `apps/song-register/`

```
apps/song-register/
├── index.html            2 525 o   — page + toolbar de filtres
├── app.js               14 791 o   — logique de chargement/agrégation/rendu (cœur)
├── app-atoms.js            127 o   — shim vide (compat héritée, ne fait RIEN)
├── local-editor-links.js 2 547 o   — injecte les liens vers l'éditeur privé
└── style.css             2 996 o   — thème sombre

Dépendance partagée :
apps/lib/dynamic-registers.js  11 569 o — pipeline de chargement commun à TOUS les registres
```

| Type | Fichiers |
|---|---|
| HTML | `index.html` |
| JS | `app.js`, `app-atoms.js`, `local-editor-links.js`, + `../lib/dynamic-registers.js` |
| CSS | `style.css` |
| Données | **aucune en local** — tout est chargé à distance (voir §2) |

### Dépendances externes (CDN / libs)

- **js-yaml@4** via `cdn.jsdelivr.net` (chargé dynamiquement par `dynamic-registers.js` pour parser le YAML embarqué dans les `.md`).
- **API GitHub** (`api.github.com/.../git/trees/main?recursive=1`) pour lister les fichiers.
- **raw.githubusercontent.com** pour récupérer le contenu brut.
- Police : `Inter` (fallback `system-ui`), non auto-hébergée.
- Aucun framework (vanilla JS, DOM natif).

### Emprunts de code à un autre registre — **à signaler explicitement**

1. **`apps/lib/dynamic-registers.js` est partagé** avec tous les registres. Tout son code de *dédoublonnage* (`mergeGroup`, `dedupeById`) est **scopé `kind === 'place'`** : ces fonctions, les `console.warn('[places] …')`, le filtre anti-parasite `type_unite !== 'place'` sont du code écrit pour le **registre des lieux** et qui transite ici sans effet sur les chansons.
2. **`app-atoms.js` est un fossile** : un IIFE vide avec un commentaire « les atomes sont désormais chargés directement par app.js ». Reliquat d'une ancienne architecture — **dette morte**.
3. À la racine du repo : `index-legacy.html` et `index-pre-cosmetic.html` (27 Ko, identique à `index.html`) — vestiges d'une refonte du hub, sans rapport direct mais révélateurs d'un historique « pré-cosmétique ».

---

## SECTION 2 — Structure des données (Phase 2 + 2 bis)

### Pipeline de chargement

`app.js → loadSongs()` lance **trois** appels `DynamicRegisters.loadRecords` :

```js
const allSongs       = loadRecords({ prefixes:['registers/songs/','registers/','sources/'], kinds:['song'] });
const atomRecords    = loadRecords({ prefixes:['sources/'], kinds:['atom'] });
const songbookRecords= loadRecords({ prefixes:['songs/'] });   // ⚠ retourne VIDE (voir ci-dessous)
```

Le pipeline ne lit **pas le disque local** : il interroge l'arbre Git de la branche `main` via l'API GitHub, puis télécharge chaque `.md` en raw, et extrait les blocs ` ```yaml ` (`parseMarkdown`).

### Container keys reconnus pour les chansons

Dans `dynamic-registers.js`, les clés-conteneurs sont :
```js
['chronology','events','people','persons','places','organizations','organisations',
 'orgs','songs','citations','quotes','concepts','motifs','mythes','myths','records']
```
→ pour les chansons, la clé est **`songs:`**. Le `kind:'song'` est ensuite inféré par `inferKind()` :
```js
if (id.startsWith('SONG-') || id.startsWith('ALBUM-') || data.song || data.titre && /songs?\//.test(file)) return 'song';
```

### Volumétrie (vérifiée)

| Métrique | Valeur réelle | Source de vérité |
|---|---|---|
| Fichiers source `registers/songs/` | **51 fichiers `.md`** | `find` |
| Entrées canoniques (`canonical_song:true & exclude:false`) | **51** (JD-SONG-001→050 + 051) | `grep` |
| Titres explicitement exclus | **6** (Blue Monday, Boredom, Love Battery, Louie Louie, Sister Ray, The Passenger) | fichier canon |
| Records `kind:song` (export pré-généré) | **110** | `exports/generated/songs.json` |
| Mentions brutes « SONG- » dans `registers/songs/` | **145** | `grep` |
| « 440 records → 52 canoniques » (chiffre hub) | **non reproductible tel quel** — voir alerte ci-dessous |

> ⚠️ **Discordance de compteurs.** Le hub annonce **52 titres / 440 mentions**, codé en dur dans `index.html` (`<span class="card-counter">52 titres</span>` + `<li>52 titres canoniques … 440 mentions</li>`). Le canon contient en réalité **51** entrées canoniques. Le compteur de l'app, lui, est **dynamique** (`canonicalSongs.length`) et affichera **51**. Le hub est donc **statique et faux d'une unité**.

### Schéma effectif d'une entrée canonique (≥80 % renseignés)

Tiré de `00_canonical_joy_division_songs.md` :

```yaml
- id: JD-SONG-034            # 100% — convention JD-SONG-NNN (zero-padded)
  type_unite: song           # 100%
  canonical_song: true       # 100%
  song: "Atmosphere"         # 100% — titre canonique
  slug: "atmosphere"         # 100%
  category: "œuvre originale complète"  # 100%
  period: "Joy Division"     # 100%
  status: "canonique"        # 100%
  albums: ["Licht und Blindheit","Still","Substance"]  # ~100%
  aliases: ["Chance"]        # présent ~100% (souvent []  → vide ~55%)
  include_variants: [...]    # 100%
  exclude: false             # 100%
```

Champ **souvent vide (<20 % de contenu utile)** : `aliases` (tableau présent mais vide pour la majorité), `separate_from` (lu par l'app mais **absent du canon** — jamais renseigné).

### Schéma des **mentions** brutes (hétérogène, non canonique)

Ex. `s45_curtis_songs_*.md` :
```yaml
id: SONG-S45-UNKNOWN-PLEASURES-STRAWBERRY
source_id: S45
titre: Unknown Pleasures      # FR "titre", pas "song"
artiste: Joy Division
nature: album / session
usage: >  …texte libre…
atomes_lies: [S45-A078]
chapitres: [Chapitre 3, Chapitre 8]
prudence: > …
```
Convention d'id des mentions : `SONG-S{n}-…` (préfixe source). Convention canon : `JD-SONG-NNN`.

### Distribution des `type_unite` dans `registers/songs/` (révèle l'hétérogénéité)

```
111 song          5 live_set_bootleg_context   3 release_or_session
  6 live_set_context   4 registre_chansons      3 song_session
  2 album   2 song_or_cover   2 song_or_release   1 song_canon
  + film_context, media_context, tv_session, song_pair, release_design…
```
→ Le dossier mélange chansons, contextes live, objets-release, sessions, métadonnées de registre. C'est un **corpus documentaire**, pas une table normalisée.

### Schémas JSON/YAML formels — **présents et riches** (`schemas/`)

Il existe **8 schémas liés aux chansons** :
`song.schema.yaml`, `song_lyrics_editorial.schema.yaml`, `song_external_evidence.schema.yaml`, `song_occurrence.schema.yaml`, `song_version.schema.yaml`, `song_web_source.schema.yaml`, + `session_v1.yaml`, `concert_v1.yaml`.

**Mais** : ces schémas sont **descriptifs (documentaires)**, pas exécutables. **Aucune validation runtime** n'est faite par l'app — `dynamic-registers.js` ne charge aucun schéma. Le `song.schema.yaml` v2 décrit déjà la scission publique/privée (voir §7) :
> *« Les paroles complètes doivent rester dans lyrics.md avec source et statut de vérification. »*
> *« Les citations longues de paroles ne doivent pas être réinjectées dans les atomes. »*

### Logique d'agrégation canonique (Phase 2 bis)

```js
function extractCanonicalSongs(records) {       // critère de canonicité
  records.map(i=>i.data||{})
    .filter(d => d.type_unite==='song' && d.canonical_song===true && d.exclude!==true)
    …  // → 51 objets canoniques
}
```
Le rattachement des mentions au canon est fait par `canonicalForRecord()` :
1. si `song_id` explicite → match direct par id ;
2. sinon par **titre normalisé** (`norm()` : minuscules, sans accents, sans ponctuation) via `aliasIndex` ;
3. sinon par titre **sans préfixe « the »**.

`groupSongRecords()` produit pour chaque canon : `{records[], lyricsEditorial[], sourceIds, types, themes, chapters}`.

**Que deviennent les non-canoniques ?** Calculés mais **non affichés** :
```js
const orphan = rawSongRecords.filter(r => !canonicalForRecord(r)).length;
// → seulement comptés dans la status-card : "… ; N mention(s) exclue(s) ou hors canon."
```
Il n'existe **aucune page de détail** ni « voir les mentions hors canon ». Les atomes rattachés sont affichés **inline** dans la carte (plafonnés à 30, « +N masquées »).

---

## SECTION 3 — Rendu fonctionnel actuel (Phase 3)

- **Vue par défaut** : layout 2 colonnes (toolbar sticky 340 px + liste de cartes). Une `status-card` annonce « N titre(s) canoniques ; M mentions atomisées ; … ». Toutes les chansons sont affichées, triées par titre (`localeCompare` numérique).
- **Filtres** : Chanson canonique (select groupé par `category`), Recherche plein-texte (sur tout le haystack, y compris `JSON.stringify` des records), Source, Type, Thème (plafonné à 250 options), Chapitre.
- **Actions** : Réinitialiser, **Exporter CSV** (11 colonnes : song, category, period, status, aliases, albums, variants, atomized_mentions, lyrics_editorial, sources, chapters).
- **Format d'affichage** : carte par titre → badges (canon, période, statut, n mentions, lyrics éditorial) + sections (catégorie, albums, alias, variantes, sources, chapitres, thèmes, appareil éditorial, mentions atomisées).
- **Liens vers d'autres registres documentaires** (lieux/acteurs/citations/concepts) : **aucun**. Les thèmes/chapitres sont du texte brut, non cliquable.
- **Liens vers `joy-division-releases`** : **aucun**.
- **Lien sortant unique** : `local-editor-links.js` injecte un badge « ouvrir éditeur » → `adminquest.github.io/joy-division-studio-private/apps/local-songbook-editor/?slug=…` (le repo **privé**). C'est aujourd'hui le **seul pont public→privé**.
- **Responsive** : un seul breakpoint `@media (max-width:960px)` → passage 1 colonne, toolbar non-sticky. Pas d'optimisation mobile fine.

---

## SECTION 4 — Esthétique actuelle (Phase 4)

| Propriété | Valeur |
|---|---|
| Fond | `#0f1115` (quasi-noir) |
| Texte | `#e6e6e6` |
| Accent | bleus (`#93c5fd`, `#1d4ed8`, `#bfdbfe`) |
| Hero | dégradé `#111827→#1f2937` |
| Cartes | `#10151c`, bord `#2f3845`, radius 12-14 px |
| Badges | pilules `#243041`, canon en bleu `#1d4ed8`, éditorial en violet `#3f2d5f` |
| Typo | Inter, titres `-0.02em` |
| Ombres | aucune (design plat) |

### Comparaison écosystème

| Surface | Identité visuelle |
|---|---|
| Hub d'accueil | **crème, accents atténués** |
| Registre releases | bleu sobre |
| Collection privée | terracotta |
| Registre des lieux (refondu) | **crème, ocre rouille, pictos par type** |
| **Registre des chansons** | **🌑 sombre + bleu électrique** |

**Verdict subjectif : en franc décalage.** C'est le seul registre resté en **dark mode bleu**, alors que l'écosystème converge vers une base **claire crème + accent terre (ocre/rouille/terracotta)**. C'est visuellement le membre le plus « ancien génération » de la famille — typiquement « pré-cosmétique ». Il a manqué la vague de refonte qui a touché lieux et hub.

---

## SECTION 5 — Points faibles (Phase 5, par impact)

**🔴 Élevé**
1. **Compteur hub statique & faux** : « 52 titres / 440 mentions » codé en dur, réel = 51 canoniques. Désync garantie à chaque ajout.
2. **`songbookRecords = loadRecords({prefixes:['songs/']})` retourne toujours vide** : il n'existe **aucun dossier `songs/` à la racine du repo public** et **aucun record `song_lyrics_editorial`** dans le public (vérifié). Toute la branche « appareil éditorial des paroles » de l'app (`renderLyricsEditorial`, badge `lyrics éditorial`, colonne CSV `lyrics_editorial`) est **du code mort côté public**. (Bon pour les droits d'auteur — mais c'est de la dette : l'app prétend une capacité qu'elle n'a pas.)
3. **Esthétique hors-charte** (voir §4) — impact perçu utilisateur fort.

**🟠 Moyen**
4. **Dépendance dure à l'API GitHub non authentifiée** : `git/trees?recursive=1` est soumis au **rate-limit 60 req/h/IP**. En cas de dépassement → `GitHub tree 403` et registre vide. Fragilité de robustesse réelle.
5. **Code mort / fossiles** : `app-atoms.js` (shim vide), `separate_from` lu mais jamais présent, `exports/generated/songs.json` (110 records) généré mais **jamais consommé** par l'app (parallel artifact qui dérive).
6. **Pollution par le code « places »** dans la lib partagée (`console.warn('[places]…')` peut s'afficher, dédoublonnage scopé places inopérant ici).

**🟡 Faible**
7. **Recherche brute** : le haystack inclut `JSON.stringify(data)` → faux positifs (un terme matche un nom de champ).
8. **Ergonomie** : pas de page de détail, pas de liens cliquables, atomes plafonnés à 30 sans pagination, filtre Thème tronqué à 250.
9. **Données incohérentes** : double entrée `The Kill (Still)` / `The Kill (Warsaw)` avec **alias partagés** (« The Kill », « Kill ») — l'app gère par commentaire défensif (`ne pas laisser un alias nu écraser un titre distinct`) mais le rattachement des mentions « The Kill » nues est **ambigu par conception**.

---

## SECTION 6 — Opportunités (Phase 6)

- **Pictogrammes par catégorie/variante** : le canon porte déjà `category` (œuvre complète / Warsaw / démo-répétition / inédit-instrumental / terminal-transition) et `include_variants` (studio, single, album, Peel, BBC, live, demo, rehearsal, instrumental, Warsaw…) → matière directe à un jeu de pictos, dans l'esprit des « pictos par type » du registre des lieux refondu.
- **Liens croisés documentaires** : rendre thèmes/chapitres/sources cliquables vers les registres concept/chronology/quote/people.
- **Liens vers `joy-division-releases`** : **opportunité réelle mais non-triviale** — le repo releases modélise des `variant` avec `tracklist → audio_track.title` (string), **sans `song_id`**. Un pont nécessiterait soit un matching par titre normalisé (réutilisable depuis `norm()`), soit l'ajout d'un FK `song_id` côté tracks. À planifier explicitement.
- **Filtres supplémentaires** : par album (déjà dans `albums[]`), par période (déjà `period`), par variante d'enregistrement (`include_variants`).
- **Tris** : par id chronologique d'œuvre, par nombre de mentions (déjà calculé : `group.records.length`).
- **Mode timeline** : `period` + (à venir) dates de session/release.
- **Page de détail par chanson** : agrégerait mentions + (cross-repo) releases + concerts + citations. C'est le candidat naturel à `12b-2.c`.

---

## SECTION 7 — Mapping public / privé (Phase 7) — **table de référence**

Champs constatés dans les **YAML publics** (`registers/songs/00_canonical…md`) + champs **privés** observés dans `joy-division-studio-private/songs/<slug>/*.md`.

### 7.1 — Champs du registre **public** canonique

| Champ | Statut actuel | Statut cible (Piste B) | Justification |
|---|---|---|---|
| `id` (JD-SONG-NNN) | public | **RESTE PUBLIC** | clé de jointure cross-repo, non confidentielle |
| `type_unite` | public | **RESTE PUBLIC** | métadonnée structurelle |
| `canonical_song` | public | **RESTE PUBLIC** | drapeau de canonicité |
| `song` (titre) | public | **RESTE PUBLIC** | titre = donnée publique |
| `slug` | public | **RESTE PUBLIC** | clé d'URL, partagée avec le privé |
| `category` | public | **RESTE PUBLIC** | taxonomie éditoriale, non confidentielle |
| `period` | public | **RESTE PUBLIC** | métadonnée historique |
| `status` | public | **RESTE PUBLIC** | statut de canonicité |
| `albums` | public | **RESTE PUBLIC** | discographie = donnée publique |
| `aliases` | public | **RESTE PUBLIC** | variantes de titre publiques |
| `include_variants` | public | **RESTE PUBLIC** | typologie des versions |
| `exclude` / `exclusion_reason` | public | **RESTE PUBLIC** | logique de toilettage du canon |
| `sources` / `source_id` (mentions) | public | **RESTE PUBLIC** | références documentaires |
| `usage`, `nature`, `artiste` (mentions) | public | **RESTE PUBLIC** | analyse documentaire publiable |
| `themes` / `motifs` (issus atomes) | public | **RESTE PUBLIC** | thématique, pas de reproduction de paroles |
| `chapters` | public | **RESTE PUBLIC** | rattachement éditorial |

### 7.2 — Champs **privés** (songbook) → classification cible

| Champ (privé actuel) | Statut actuel | Statut cible (Piste B) | Justification |
|---|---|---|---|
| `lyrics_versions`, `lyrics_variants` (lyrics.md) | privé | **RESTE PRIVÉ** | paroles intégrales — droits d'auteur |
| `full_lyrics_local_path` | privé (non versionné) | **RESTE PRIVÉ (hors repo)** | pointe vers `local_data/…`, jamais versionné |
| `short_excerpts` (lyrics_editorial) | privé | **À DÉCIDER** | courts extraits *fair-use* — publiables si strictement critiques ; par prudence → privé tant que non arbitré |
| `motifs` / champs lexicaux (editorial) | privé | **PUBLIABLE** | motif ≠ reproduction ; candidat à remonter au public |
| `editorial_notes` | privé | **À DÉCIDER** | notes analytiques : publiables, sauf annotations personnelles/critiques sensibles → arbitrage cas par cas |
| `variants` décrites (editorial) | privé | **PUBLIABLE** | description sans reproduction |
| `sessions` (sessions.md) | privé | **PUBLIABLE** | faits discographiques publics |
| `live_occurrences` | privé | **PUBLIABLE** | setlists/concerts = faits publics |
| `official_releases`, `compilation_occurrences` | privé | **PUBLIABLE** (→ idéalement dans `releases`) | discographie publique |
| `bootleg_occurrences`, `sound_quality_notes`, `source_conflicts` | privé | **À DÉCIDER** | renvoie à une **collection personnelle** / Google Drive → garder privé par défaut |
| `external_evidence`, `external_sources` | privé | **PUBLIABLE** | sources web/externes citables |
| `internal_sources_to_mobilize`, `priority`, `lyrics_tasks`… (priority_notes) | privé | **RESTE PRIVÉ** | notes de travail/pilotage internes |
| `matched_records`, `related_atoms` (source_notes) | privé (dérivé du public) | **DÉRIVÉ — ne pas dupliquer** | doit être *calculé* depuis le public, pas stocké des deux côtés |
| `verification_status`, `last_update` | les deux | **par couche** | chaque couche garde son propre statut |

**Champ de jointure unique : `song_id` (= `id` public JD-SONG-NNN) + `slug`.** Tous les fichiers privés le portent déjà → la jointure runtime est **déjà possible sans migration de clé**.

**Constat-clé de duplication** : `songs/<slug>/song.md` (privé) **recopie** `id, canonical_song, slug, category, period, status, albums, aliases, include_variants` — strictement les champs publics. C'est exactement la duplication que Piste B doit supprimer (le privé doit cesser de stocker ces champs et les lire depuis le public).

---

## SECTION 7 BIS — Confirmation du songbook privé (Phase 7 bis)

**Confirmé par accès direct au repo `joy-division-studio-private`** (pas seulement par inférence) :

- **L'éditeur existe** : `apps/local-songbook-editor/` (`index.html` 6.8 Ko, `app.js` 18 Ko, `style.css` 9 Ko).
- **Authentification** : token GitHub PAT (scope `repo`) stocké en `localStorage`, lecture/écriture directe via l'API GitHub. Écran bloquant tant que le token n'est pas saisi.
- **Données** : `songs/` contient **50 dossiers-chansons** (un par slug canonique) + `README.md` + `priority_index.md`.
- **Structure d'un dossier** (11 fichiers) : `song.md`, `lyrics.md`, `lyrics_editorial.md`, `sessions.md`, `live_occurrences.md`, `releases.md`, `bootlegs.md`, `source_notes.md`, `external_evidence.md`, `editorial_notes.md`, `priority_notes.md`.
- **Piste B déjà amorcée** : l'éditeur charge **la liste des chansons depuis le repo PUBLIC** (`const PUBLIC_REPO='AdminQuest/joy-division-ai-writing-studio'; SONGS_PATH='registers/songs/00_canonical_joy_division_songs.md'`) puis lit/écrit les notes dans le privé. Le sens public→privé est donc **déjà fonctionnel** ; il reste à généraliser la fusion runtime et à supprimer la duplication dans `song.md`.
- **Inconnues / à arbitrer** : la majorité des dossiers privés sont encore des gabarits (`[]`, « à renseigner ») — le contenu confidentiel réel (paroles, bootlegs) est en grande partie **non encore saisi**. L'éditeur n'écrit aujourd'hui que `editorial_notes.md` (les autres fichiers sont en lecture).

---

## SECTION 8 — Roadmap de refonte (Phase 8)

> Effort estimé en jours-homme indicatifs (`j`), à calibrer.

### 12b-2.a — Refonte data + scission public/privé — **3-4 j**
1. **Schéma public formel exécutable** : convertir `song.schema.yaml` en contrat validable + script de validation (CI) sur `registers/songs/`.
2. **Geler le contrat de clé** : `id` (JD-SONG-NNN) + `slug` comme jointure unique (déjà respecté → coût faible).
3. **Dé-dupliquer le privé** : retirer de `songs/<slug>/song.md` les champs recopiés du public ; le privé ne garde que lyrics + couches confidentielles (cf. table §7).
4. **Migration paroles** : confirmer que **toute** parole reste hors repo public (déjà le cas — code mort `songs/` à nettoyer) ; formaliser `local_data/` non versionné côté privé.
5. **Corriger le compteur hub** (statique 52 → dynamique 51) et nettoyer code mort (`app-atoms.js`, `separate_from`, `songs/` loader, export `songs.json` orphelin).
- *Risque* : aucun changement de clé requis → migration faible risque.

### 12b-2.b — Refonte design du registre public — **2-3 j**
- Aligner sur la charte crème + ocre/rouille de l'écosystème (sortir du dark/bleu).
- Pictogrammes par `category` et `include_variants` (§6).
- Robustesse : cache / fallback sur l'API GitHub (rate-limit), états d'erreur propres.
- Sortir le code « places » de la lib partagée ou le scoper proprement.

### 12b-2.c — Page de détail par chanson + agrégation cross-registres — **4-6 j (optionnel/différé)**
- Route `?id=JD-SONG-NNN`.
- Agrège : mentions internes + thèmes + chapitres + **releases** (matching titre `norm()` faute de `song_id` côté releases — voir dépendance) + concerts + citations.
- *Dépendance* : nécessite soit un FK `song_id` dans `joy-division-releases` (idéal), soit un matcher par titre (tactique).

### 12b-2.d — Refonte de l'éditeur privé (fusion public+privé) — **3-4 j**
- Généraliser la fusion runtime : l'éditeur lit le canon public (déjà fait pour la liste) **et** affiche les champs publics en lecture seule, n'éditant que les couches privées.
- Étendre l'écriture au-delà de `editorial_notes.md` (lyrics, sessions, etc.) selon la table §7.
- Supprimer définitivement la copie locale des champs publics.

**Séquencement recommandé** : a → b en parallèle léger, puis d (dépend de a), c en dernier (dépend de a et idéalement d'un FK releases).

---

## Synthèse exécutive

Le registre public des chansons est un **registre canonique propre côté données** (51 titres bien structurés, clé `JD-SONG-NNN`/`slug` déjà partagée avec le privé, **déjà sans paroles**), mais **vieillissant côté code et design** : thème sombre hors-charte, compteur hub statique faux (52 vs 51), code mort hérité (shim atoms, loader `songs/` vide, export `songs.json` orphelin, résidus « places » dans la lib partagée), fragilité au rate-limit GitHub, et aucune liaison cross-registres/releases. La **Piste B est déjà à moitié câblée** : le songbook privé existe, est indexé par le même `song_id`, et consomme déjà le canon public pour sa liste. Le vrai travail de scission consiste surtout à **supprimer la duplication des métadonnées publiques dans `song.md` privé** et à formaliser la fusion runtime — pas à déplacer les paroles, qui sont **déjà** exclusivement privées.
