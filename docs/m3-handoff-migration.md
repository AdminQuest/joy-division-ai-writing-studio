# Point de sauvegarde — Migration M3 vers `joy-division-hub`

> Brief de continuité pour reprendre la migration M3 dans une nouvelle session.
> À coller comme premier message d'une session incluant les cinq dépôts.
> Le plan détaillé fait foi : `docs/m3-architecture-depot-unique.md`.
>
> Date : 2026-06-07.

## Setup requis de la session

Inclure dans le périmètre les **cinq** dépôts :

- `joy-division-hub` ← cible (privé, vide, déjà créé) ;
- `joy-division-ai-writing-studio` (public, source) ;
- `joy-division-studio-private` (privé, source) ;
- `joy-division-releases` (source) ;
- `joy-division-collection` (source).

Sans les cinq, l'assistant ne peut pas lire-copier les sources vers le hub.
Branches de travail : préfixe `claude/*`. Jamais de commit direct sur `main`.

## Où on en est

- M0 (2026-06-05), M1 (2026-06-06), M2 (2026-06-06) : **clôturés**. M3 : **lancé** (2026-06-07).
- Roadmap de référence **unique** : `docs/roadmap-strategique-2026.md` (v2.3, repo public, sur `main`).
- Dossier d'architecture validé et mergé : `docs/m3-architecture-depot-unique.md` (repo public) — **c'est le plan à exécuter, à lire en premier**.
- Règles permanentes : `CLAUDE.md` (repo public, sur `main`).

## Décisions actées (ne pas rouvrir)

- Hub = un dépôt unique **privé** `joy-division-hub`, derrière Cloudflare Zero Trust.
- Absorbe les quatre dépôts. Tout devient privé : **aucune diffusion publique** (`releases` incluse).
- Repo **neuf**, commit initial propre. Les quatre anciens dépôts → **archivés en lecture seule** (pas de fusion d'historiques git).
- Réagencement **léger** = mapping logique. Arborescence actuelle conservée, apps non réécrites. Les cinq espaces sont une couche de lecture (manifest + navigation) : **La Collection · L'Usine · Le Fonds · L'Atelier · La Vigie**.
- Zéro perte fonctionnelle : 14 registres, RAG, manuscript-studio, corpus-dashboard, collection, veille marché.
- Description « About » du hub :
  > Hub privé unique du projet Joy Division — corpus, registres, RAG, manuscrit et collection, organisés en cinq espaces (Collection · Usine · Le Fonds · Atelier · Vigie).

## Tâche immédiate — Phase 1 (import), selon le dossier d'architecture §3 et §5

1. Assembler l'arborescence cible dans `joy-division-hub` :
   - spine = contenu de `ai-writing-studio` (hors `.git`) ;
   - union de `studio-private` : `chapters/` (matière éditoriale privée = **source**, `document_maitre.md` = sortie générée), `tools/` (garder la variante canonique de `generate_status.py`), `docs/` `prompts/` `reports/` `_meta/` par union, ajout direct de `songs/` et `sources_pdf/` ;
   - sous-arbres autonomes : `releases/` (← `joy-division-releases`) et `collection/` (← `joy-division-collection`).
2. Ajouter `MANIFEST_ESPACES.md` (cinq espaces → dossiers/apps réels), le `README.md` d'entrée, et la description.
3. Vérifier : `python tools/build_all.py` puis `python tools/audit_repo.py --fail-on-error` ; comparer volumétries registres + nombre d'apps avant/après.
4. Commit initial propre → branche `claude/*` → PR.

## Ensuite (phases 3 → 7 du dossier, ne pas sauter l'ordre)

- **Phase 3** : rebrancher les trois dépendances runtime distantes en lecture **locale** :
  - (a) `https://adminquest.github.io/joy-division-ai-writing-studio/...` → chemins relatifs même origine ;
  - (b) `raw.githubusercontent.com/<public>/main/<SONGS_PATH>` → chemin local ;
  - (c) GitHub API (`CONTENTS_API_URL` / `COMMITS_API_URL` / `repos/<PRIVATE_REPO>` + token) → lecture locale, le token disparaît.

  Neutraliser les `deploy-pages` **publics** (`releases` + `collection`). **Conserver** `daily-watch` (veille Discogs/eBay : sortant + secrets).
- **Phase 4** : CI unifiée (un seul gate = `check-generated-sync` ∪ `private-drift-check`) ; `update-status.yml` → flux PR, pas de push direct sur `main`.
- **Phase 5** : Cloudflare Pages + Zero Trust (inventorier l'abonnement Pages Pro existant).
- **Phase 6** : vérification fonctionnelle complète.
- **Phase 7** : archiver les quatre dépôts en lecture seule = **point de non-retour**.

## Garde-fous (impératifs)

- **Ne jamais exécuter la phase 7** (archivage / suppression des anciens dépôts) sans validation humaine explicite.
- Migration **réversible** : tant que la phase 7 n'est pas prononcée, les quatre dépôts restent la source de vérité.
- Sur **chaque PR** : traiter la revue Codex → résoudre les fils → reposter `@codex review` → répéter jusqu'au feu vert Codex, en plus des checks requis (règle inscrite dans `CLAUDE.md`).
- Jamais de merge sur checks rouges ; toujours afficher le diff avant commit ; régénérer les exports (`build_all`) avant push si `registers/` `sources/` `apps/` `chapters/` changent.
- Politique réseau du hub : autoriser le sortant Discogs/eBay, sinon la veille casse.

## Prompt d'amorce

> Lis `docs/m3-architecture-depot-unique.md` et `CLAUDE.md` sur `main` du repo
> public, puis exécute la **phase 1** de la migration vers `joy-division-hub`
> (import + `MANIFEST_ESPACES.md` + `README`), sur une branche `claude/*`, et
> ouvre une PR. N'exécute jamais la phase 7 sans ma validation.
