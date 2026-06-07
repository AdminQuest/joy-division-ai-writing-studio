# M3 — Architecture du dépôt unique privé (hub)

> Document de conception, à valider par décision humaine **avant** toute
> migration. Il ne déclenche aucune bascule : M3 commence par la conception.
>
> Références : `docs/roadmap-strategique-2026.md` (jalon M3), `CLAUDE.md`
> (section « Cap M3 »), `docs/projet-etat-de-reference-2026-06.md` (modèle des
> cinq espaces).
>
> Date : 2026-06-07. Statut : proposition d'architecture cible.

## 1. Objet

Concevoir le dépôt unique qui remplacera les **quatre** dépôts actuels par un
**hub privé unique**, exposé derrière Cloudflare Zero Trust, sans perte de
fonctionnalité et selon un **réagencement léger** (mapping logique, pas de
déplacement massif de dossiers, apps non réécrites).

Décisions déjà actées (rappel) :

- dépôt **neuf**, commit initial propre ; les quatre dépôts actuels sont
  archivés en **lecture seule** (pas de fusion d'historiques git) ;
- **rien ne reste public** : tout le hub est privé derrière Zero Trust ; aucune
  diffusion publique, y compris pour `releases` (ex-CC BY-SA) ;
- **organisation par fonction** : cinq espaces — La Collection, L'Usine, Le
  Fonds, L'Atelier, La Vigie — comme **couche de lecture**, pas comme dossiers ;
- périmètre absorbé : `joy-division-ai-writing-studio` (public),
  `joy-division-studio-private` (privé), `joy-division-releases` (variantes,
  14ᵉ registre), `joy-division-collection` (Collection perso).

## 2. Principes directeurs

1. **Zéro perte fonctionnelle** : 14 registres, RAG, manuscript-studio,
   corpus-dashboard, Collection et veille marché (`daily-watch`) restent
   opérationnels.
2. **Réagencement léger** : la colonne vertébrale est l'arborescence actuelle du
   dépôt public ; on y replie le privé par **union**, et on ajoute `releases/`
   et `collection/` comme sous-arbres autonomes.
3. **Mapping logique** : les cinq espaces vivent dans un manifest + des README de
   navigation, pas dans un déplacement de dossiers.
4. **Autonomie runtime** : plus aucune dépendance à un fetch GitHub distant ;
   tout est lu en local / même origine, servi derrière Zero Trust.
5. **Réversibilité** : tant que l'archivage final n'est pas prononcé, les quatre
   dépôts restent la source ; la bascule est progressive et vérifiable.

## 3. Arborescence cible du hub

Spine = dépôt public, complété par union du privé et par deux sous-arbres pour
`releases` et `collection` (qui possèdent leurs propres `data/`, `docs/`,
`schema/`, `scripts/`, `site/`, `tests/` — d'où l'isolement sous un dossier
dédié pour éviter les collisions).

```text
/ (hub privé unique)
├── README.md                     # porte d'entrée + carte des cinq espaces
├── MANIFEST_ESPACES.md           # mapping cinq espaces -> dossiers/apps réels
├── CLAUDE.md                     # règles permanentes
├── apps/                         # TOUTES les apps (ex-public + ex-privé)
│   ├── lib/                                  (ex-public)
│   ├── chronology-register/ concept-register/ concerts-register/
│   ├── images-register/ organizations-register/ people-register/
│   ├── places-register/ quote-register/ sessions-register/
│   ├── song-register/ source-register/       (les 11 apps registres)
│   ├── rag-studio/                            (RAG)
│   ├── m2-formulaire/                         (studio de préparation M2)
│   ├── corpus-dashboard/                      (ex-privé — Vigie)
│   ├── manuscript-studio/                     (ex-privé — Atelier)
│   ├── master-docs/                           (ex-privé — Atelier)
│   ├── prompt-studio/                         (ex-privé — Atelier)
│   └── local-songbook-editor/                 (ex-privé — Atelier)
├── sources/  registers/  exports/  rag/  schemas/  indexes/
├── chapters/                     # DM générés (ex-public) + matière éditoriale (ex-privé), par union
├── master_docs/  prompts/  templates/  assets/  data/  reports/  docs/  _meta/
├── songs/  sources_pdf/          (ex-privé)
├── tools/                        # union ex-public + ex-privé
├── releases/                     # ex joy-division-releases (data/variants, schema, scripts, site, tests)
├── collection/                   # ex joy-division-collection (data, scripts, collectors, site, tests)
└── .github/workflows/            # CI unifiée
```

Aucune app n'est déplacée hors de `apps/` ni réécrite : seules les **sources de
données** qu'elles consomment changent d'adresse (voir §6).

## 4. Manifest des cinq espaces (couche de lecture)

`MANIFEST_ESPACES.md` (et un éventuel `spaces.yaml` lisible par le dashboard)
déclare, sans rien déplacer, le rattachement fonctionnel :

| Espace | Fonction | Dossiers / apps rattachés |
|---|---|---|
| **La Collection** | Conserver les objets possédés | `collection/`, `releases/` |
| **L'Usine** | Transformer la matière brute en données structurées | `tools/`, `apps/m2-formulaire/`, `schemas/`, sas `sources/_incoming/` |
| **Le Fonds** | Conserver, structurer, interroger le corpus (RAG) | `sources/`, `registers/`, `exports/`, `rag/`, `indexes/`, `data/`, `apps/{11 registres, rag-studio}` |
| **L'Atelier** | Produire le manuscrit | `chapters/`, `master_docs/`, `prompts/`, `songs/`, `sources_pdf/`, `apps/{manuscript-studio, master-docs, prompt-studio, local-songbook-editor}` |
| **La Vigie** | Piloter qualité et stratégie | `reports/`, `docs/`, `STATUS*.md`, `apps/corpus-dashboard/` |

Flux : **Collection → Usine → Le Fonds → Atelier → Vigie**. Les IA (Claude,
Codex, ChatGPT) sont des **opérateurs** transverses, pas un espace.

## 5. Procédure d'import des quatre dépôts

Import par **copie** (pas de `git merge` / `subtree`), dans cet ordre :

1. **Spine public** : copier intégralement `joy-division-ai-writing-studio`
   (hors `.git`) à la racine du hub.
2. **Union privée** : copier `joy-division-studio-private` ; les dossiers
   présents des deux côtés sont fusionnés par union :
   - `chapters/` : la matière éditoriale privée (notes de sources, suppléments,
     compléments) est la **source** ; le `document_maitre.md` public en est la
     **sortie générée** → conserver les deux, l'éditorial fait foi ;
   - `tools/` : union ; seul `generate_status.py` existe des deux côtés →
     conserver la variante du build canonique, garder `generate_consolidated_status.py`,
     `import_editorial_notes.py`, `setup_github_rulesets.sh` ;
   - `docs/`, `prompts/`, `reports/`, `_meta/` : union (contenus distincts) ;
   - `songs/`, `sources_pdf/` : ajout direct.
3. **Sous-arbres autonomes** : copier `joy-division-releases` dans `releases/`
   et `joy-division-collection` dans `collection/` (leurs `data/`, `docs/`,
   `schema/`, `scripts/`, `site/`, `tests/` restent encapsulés).
4. **Manifest + navigation** : ajouter `MANIFEST_ESPACES.md`, le `README.md`
   d'entrée et les liens de navigation des cinq espaces.

Vérification après import : `python tools/build_all.py` puis
`python tools/audit_repo.py --fail-on-error` doivent passer ; comparer
volumétries de registres et nombre d'apps avant/après.

## 6. Bascule des dépendances runtime distantes → lecture locale

Point technique principal. Les apps privées consomment aujourd'hui des sources
**distantes** ; dans le hub, elles deviennent **locales / même origine** :

| Dépendance actuelle | Usage | Cible dans le hub |
|---|---|---|
| `https://adminquest.github.io/joy-division-ai-writing-studio/...` (Pages public) | site public + apps `rag-studio`, `source-register` | chemins relatifs même origine dans le hub |
| `raw.githubusercontent.com/<public>/main/<SONGS_PATH>` | lecture de fichiers du repo public | chemin local `…/songs` ou export généré |
| GitHub API `CONTENTS_API_URL`, `COMMITS_API_URL`, `repos/<PRIVATE_REPO>` (avec token) | lecture du repo privé via API | lecture locale / génération au build ; le token disparaît |

Conséquences : suppression des `RAW_BASE` / `API_BASE` / `PUBLIC_REPO` /
`PRIVATE_REPO` codés en dur, remplacés par une **base locale** unique. Plus de
rate-limit GitHub ni de token de lecture inter-repo. Les `fetch(path, {cache:
'no-store'})` déjà relatifs sont conservés tels quels.

## 7. CI unifiée

Un seul gate requis remplace les deux gates actuels :

- ex-public `check-generated-sync.yml` : `check_generated_sync.py`,
  `build_all.py --quiet`, `audit_repo.py --fail-on-error`, validateurs
  (`orgs/images/chronology/concerts/places/songs/quotes`,
  `people --check-drift`, `attribution --check-drift`, `edges`) ;
- ex-privé `private-drift-check.yml` : comparaison normalisée de `STATUS.md` /
  `STATUS_CONSOLIDATED.md`.

→ **Gate hub unique** : exécute la chaîne `check-generated-sync` **et** le
contrôle anti-drift des STATUS dans un même workflow requis (le dépôt étant
unique, la distinction public/privé n'a plus lieu d'être).

Autres workflows :

- `update-status.yml` (ex-privé, **push direct sur `main`**) : remplacé par un
  flux PR ou une vérification bloquante sans push (cohérent avec le ruleset
  `main`) ;
- `deploy-pages.yml` (releases **et** collection, publication **publique**) :
  **neutralisés** ; remplacés par le build Cloudflare Pages privé (§9) ;
- `daily-watch.yml` (collection, veille Discogs/eBay) : **conservé**, scopé à
  `collection/`, sortant autorisé par la politique réseau, tokens en secrets.

## 8. Secrets et accès

- veille marché : tokens Discogs/eBay en **secrets** du hub (jamais commités) ;
  le `.env` reste git-ignored ;
- lecture inter-repo par token GitHub : **supprimée** (tout est local) ;
- ruleset `main` (PR obligatoire, review, linear history, gate requis) reporté
  sur le hub.

## 9. Exposition Cloudflare Pages + Zero Trust

- build statique du hub publié via **Cloudflare Pages** (privé) ;
- accès protégé par **Cloudflare Zero Trust** (politique d'accès nominative) ;
- aucune surface publique : la `daily-watch` reste un job sortant, pas une
  publication entrante ;
- **inventorier l'abonnement GitHub Pages Pro** existant pour éviter un coût ou
  une infra orphelins.

## 10. Plan de migration réversible

| Phase | Action | Vérif / repli |
|---|---|---|
| 0 | Créer le hub privé vide ; geler (annonce) les 4 dépôts | les 4 dépôts restent la source |
| 1 | Import par copie (§5) | `build_all` + `audit_repo` verts ; volumétries identiques |
| 2 | Manifest des 5 espaces + navigation | revue humaine de la carte |
| 3 | Bascule des fetchs distants → local (§6) ; neutraliser deploy-pages publics | apps testées une à une |
| 4 | CI unifiée (§7) | gate hub vert |
| 5 | Cloudflare Pages + Zero Trust (§9) | accès ZT vérifié |
| 6 | Vérif fonctionnelle complète | 14 registres, RAG, manuscript-studio, dashboard, collection, daily-watch |
| 7 | Archiver les 4 dépôts en lecture seule | **point de non-retour** : ne le franchir qu'après 6 validé |

Tant que la phase 7 n'est pas prononcée, la migration est **réversible** : les
dépôts d'origine restent intacts et faisant foi.

## 11. Risques et points de réconciliation

- collisions de chemins lors de l'union (traitées par les sous-arbres
  `releases/` et `collection/` et l'union maîtrisée des dossiers communs) ;
- divergence `chapters/` (éditorial privé source vs DM généré) — règle posée en
  §5 ;
- perte de la diffusion publique et du référencement (assumée) ;
- abonnement Pages Pro potentiellement orphelin (à inventorier) ;
- politique réseau du hub : doit autoriser le sortant Discogs/eBay sous peine de
  bloquer la veille.

## 12. Critères de sortie de ce lot d'architecture

- arborescence cible et manifest des cinq espaces validés par décision humaine ;
- procédure d'import et de réconciliation acceptée ;
- liste des bascules runtime distantes → locales arrêtée ;
- conception de la CI unifiée et de l'exposition Zero Trust validée ;
- plan de migration réversible approuvé, **avant** toute exécution.

La migration effective (phases 1+) ne démarre qu'après validation de ce
document.
