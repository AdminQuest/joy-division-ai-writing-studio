# CLAUDE.md — Règles permanentes du projet

> Mise à jour : 2026-06-07, alignée sur la roadmap stratégique 2026
> (`docs/roadmap-strategique-2026.md`, version 2.3), après lecture des
> documents `docs/` (clôtures M0/M1/M2, état de référence) et audit des dépôts
> public (`joy-division-ai-writing-studio`) et privé
> (`joy-division-studio-private`).
>
> **Roadmap de référence unique** : `docs/roadmap-strategique-2026.md` (repo
> public). L'ancien `ROADMAP.md` du repo privé a été supprimé pour éviter toute
> confusion.
>
> **Étape courante : M3 (lancé le 2026-06-07).** M0, M1 et M2 sont clôturés.
> **Objectif n°1 de M3 : supprimer les deux dépôts public et privé au profit
> d'un dépôt unique, nouveau, privé, exposé derrière Cloudflare Zero Trust.**
> Ce chantier impose une **reprise de l'architecture globale** (rôle confié à
> l'assistant).
>
> La roadmap stratégique est une **couche de lecture additive** : elle ne
> remplace aucun découpage technique existant. Tout lot technique doit se
> rattacher à l'un des jalons M0 à M7.

## Principe directeur 2026

Le corpus est suffisamment constitué. La priorité n'est plus la collecte mais
**documenter et fiabiliser l'existant**. Les outils nouveaux viennent ensuite.

> Priorité actuelle : documenter et fiabiliser. Les outils nouveaux viennent
> ensuite.

### Calendrier des jalons (M0 → M7)

| Jalon | Statut | Intention |
|---|---|---|
| M0 — Stabilisation du socle | **clôturé (2026-06-05)** | État réel du projet rendu lisible, socle consolidé. |
| M1 — Fiabilisation du corpus | **clôturé (2026-06-06)** | Contrôles DM→atomes/registres/sources, traçabilité, invariants. |
| M2 — Studio d'enrichissement documentaire | **clôturé (2026-06-06)** | Studio de préparation (CLI PERSON/ORG/IMAGE/PLACE/SOURCE, formulaire, batch, résumés PR). |
| M3 — Corpus privé unifié | **actif — lancé 2026-06-07 (P1)** | **Objectif n°1 : dépôt unique privé derrière Cloudflare Zero Trust** (reprise d'architecture globale), industrialisation documentaire et autonomisation du studio privé. |
| M4 — Studio de rédaction | ultérieur (P2) | Clarifier RAG Studio / manuscript-studio sans refonte. |
| M5 — Fonds documentaire multimédia | ultérieur (P3) | Photos, scans, bootlegs, vidéos, droits et provenance. |
| M6 — Assistant historiographique | ultérieur (P3) | Exploiter relations, concepts, motifs, mythes, chaînes argumentatives. |
| M7 — Publication et pérennisation | ultérieur (P3) | Exports, sauvegardes, documentation de reprise. |

### Règle de progression

- **Jalon actif : M3** (M0, M1 et M2 clôturés), **lancé le 2026-06-07**.
- **Priorité n°1 : unification en un dépôt unique privé derrière Cloudflare
  Zero Trust**, devant l'industrialisation documentaire et l'autonomisation du
  studio privé (M3.X), qui en deviennent des sous-chantiers.
- M4 à M7 : ultérieurs, non activés.
- Tout nouveau lot technique doit se rattacher explicitement à un jalon.

## Doctrine M2 acquise (à respecter en M3)

Le studio M2 reste un outil de **préparation**, pas d'intégration automatique :

> Le studio prépare. L'humain valide.

Garde-fous structurants conservés : aucune création automatique de sources,
atomes, citations ou relations ; aucune modification automatique de registres ;
aucun GitHub automatique (branche / PR / merge) ; décision documentaire toujours
humaine. Les CLI M2 (`tools/m2_add_person.py`, `m2_add_org.py`,
`m2_add_image.py`, `m2_add_place.py`, `m2_integrate_source.py`,
`m2_batch_prevalidation.py`) produisent des diagnostics et des résumés PR
relisibles, jamais une validation.

## Cap M3 — dépôt unique privé derrière Cloudflare Zero Trust

**Décision actée le 2026-06-07 : M3 est lancé.** L'ancienne interdiction de
fusion des dépôts est **levée**. Objectif n°1 :

> Supprimer les deux dépôts (`joy-division-ai-writing-studio` public et
> `joy-division-studio-private` privé) au profit d'un **dépôt unique, nouveau,
> privé, exposé derrière Cloudflare Zero Trust**.

Ce chantier impose une **reprise de l'architecture globale** — c'est le rôle
confié à l'assistant. Avant toute migration :

1. **Architecture cible** du dépôt unique : arborescence, séparation interne des
   surfaces autrefois public / privé, organisation des exports, des apps et de
   la CI, gestion des secrets et des accès Zero Trust ;
2. **Plan de migration réversible** : reprise d'historique utile, aucune perte
   de données, bascule progressive et vérifiable, stratégie de repli ;
3. **Sas documentaire** : aucune source nouvelle sans sas normalisé
   (`sources/_incoming/Sxx/` : `source.pdf`, `source.txt`, `source_meta.yaml`) ;
4. **Canonisation outillée** + **atomisation reproductible** produisant une
   **preuve de propagation** (`Sxx_propagation_report.md`) vers exports,
   registres, DM et interfaces ;
5. **Fin des dépendances runtime** aux fetchs GitHub distants : lecture locale
   synchronisée des exports, registres et documents maîtres ;
6. **Exposition finale** derrière Cloudflare Pages + Zero Trust.

**Décisions d'architecture actées (2026-06-07) :**

- **historique git** : le dépôt unique repart d'un commit initial propre ; les
  deux dépôts actuels sont archivés en lecture seule (pas de fusion
  d'historiques) ;
- **rien ne reste public** : un seul dépôt **privé**, tout exposé derrière
  Cloudflare Zero Trust ; la frontière actuelle entre dépôt public et dépôt
  privé **disparaît** ;
- **organisation par fonction, pas par technologie** : la structure interne du
  hub suit le modèle à cinq espaces ci-dessous, et non un découpage
  ex-public / ex-privé ;
- **périmètre** : le hub absorbe les **quatre** dépôts actuels —
  `joy-division-ai-writing-studio`, `joy-division-studio-private`,
  `joy-division-releases` (14ᵉ registre, variantes) et `joy-division-collection`
  (Collection perso) ; `releases`, aujourd'hui public en CC BY-SA, **bascule en
  privé** comme le reste ;
- **réagencement léger = mapping logique** : l'arborescence actuelle est
  conservée et les apps ne sont pas réécrites ; les cinq espaces sont une
  **couche de lecture** (README / manifest + navigation), pas un déplacement
  massif de dossiers ; aucune fonctionnalité n'est perdue (14 registres, RAG,
  manuscript-studio, dashboard, collection).

### Modèle d'organisation cible — hub fonctionnel

Modèle retenu pour le hub unifié (cadre d'organisation, **non figé** comme
architecture technique définitive) :

| Espace | Fonction | Contenu typique |
|---|---|---|
| **La Collection** | Conserver / documenter / valoriser les objets possédés | vinyles, CD, cassettes, bootlegs, livres, affiches, photos, objets, scans, métadonnées de provenance |
| **L'Usine** | Transformer la matière brute en données structurées | atomisation, enrichissement, intégration de sources, création de registres, normalisation, validation, workflows Codex |
| **Le Fonds** | Conserver, structurer et interroger le corpus | sources, atomes, registres, relations, chronologies, citations, exports, **moteur RAG** |
| **L'Atelier** | Produire le manuscrit | exports RAG, documents maîtres, Forge, manuscrits, audits de chapitres, versions de travail |
| **La Vigie** | Piloter qualité et stratégie | roadmap, audits, contrôles, rapports, agrégation, tableau de bord, indicateurs |

Flux : **Collection → Usine → Le Fonds → Atelier → Vigie**.

Règles structurantes :

- **Collection ≠ Corpus** : un objet peut exister dans la Collection sans être
  intégré au Corpus ; l'**Usine** fabrique le Corpus à partir de la matière ;
- **Le Fonds** est le cœur : on y cherche, on n'y rédige pas ; le **RAG** y vit ;
- l'**Atelier** est le seul espace de rédaction ;
- la **Vigie** est ce que M1 a commencé à construire (contrôles, agrégation,
  tableau de bord qualité) ;
- les **IA** (Claude, Codex, ChatGPT, futurs agents) ne sont pas un espace : ce
  sont des **opérateurs** pouvant intervenir à chaque niveau.

Tant que l'architecture cible et le plan de migration ne sont pas validés par
décision humaine, la fusion effective et la suppression des dépôts existants ne
sont pas exécutées : M3 commence par la **conception**, pas par la bascule. Le
dossier d'architecture détaillé sera produit sur instruction ultérieure.

### Dette M1 résiduelle basculée en M3

La dette acceptée à la clôture M1 (cf. `docs/m1-cloture.md`) est reprise comme
chantiers M3, sans rouvrir le jalon M1 :

- tableau de bord qualité complet (volumétrie / intégrité / vérification),
  généré par le build et non saisi manuellement ;
- audit **Pennie Smith** clos et documenté ;
- indicateurs consolidés : `0` lien inter-registres orphelin sur le périmètre
  publié, `0` identifiant canonique dupliqué, validation de schéma à `100 %` ;
- réserves `DM → registres` : 29 libellés divergents, 51 familles hors MVP
  (concepts, motifs, mythes, organisations, relations) ;
- vérification des champs de provenance / droits et des champs `sources` hors
  documents maîtres (aucun `IMAGE-*` à la place d'une source `Sxx`).

## Commandes de contrôle de référence

    python3 tools/generate_status.py      # générateur DIRECT de STATUS.md
    python3 tools/build_all.py            # contrôle global du pipeline
    python3 tools/check_generated_sync.py # sentinelle anti-drift des exports
    python3 tools/audit_repo.py
    git status

Nuances importantes :

- `tools/generate_status.py` est le **seul** générateur direct de `STATUS.md` ;
  `build_all.py` n'est pas présenté comme tel.
- `tools/check_generated_sync.py` ne couvre pas nécessairement `STATUS.md` : sa
  fraîcheur est assurée par exécution explicite de `generate_status.py` puis
  commit du snapshot régénéré lorsqu'il diffère.
- La référence git inscrite dans `STATUS.md` désigne l'état observé **avant** le
  commit du snapshot ; ne pas chercher à la faire correspondre au commit final
  (cela créerait une boucle de commits de snapshots).

## Régénération des exports (OBLIGATOIRE avant tout push)

À la fin de chaque session qui modifie des fichiers sources
(`registers/`, `sources/`, `apps/`, `chapters/`), exécuter AVANT tout push :

    python tools/build_all.py
    git add exports/generated/
    git commit -m "chore(generated): régénération exports [session]"

`build_all.py` est le contrôle global du pipeline registres / documents maîtres
/ exports / audits ; il régénère notamment le graphe relationnel
`exports/generated/edges.json` via `tools/build_edges.py`.

Le check requis `check-generated-sync` doit passer à vert avant toute PR.
Ne jamais pousser sans avoir régénéré les exports. Régénérer `STATUS.md` via
`generate_status.py` lorsque la roadmap, les audits ou les artefacts de
pilotage changent.

## Invariants hérités de M0 / M1 (toujours actifs)

Les jalons M0 et M1 sont clôturés (clôtures : `docs/m0-cloture.md`,
`docs/m1-cloture.md` puis PR de clôture M1) mais leurs invariants restent
opposables :

- le corpus est la source de vérité ; les documents maîtres ne sont pas des
  sources et sont générés par `tools/build_master_docs.py` ;
- les artefacts générés ne sont jamais corrigés manuellement ;
- traçabilité DM → atomes / registres / sources contrôlée
  (`tools/check_dm_atoms_traceability.py`,
  `tools/check_dm_registers_consistency.py`,
  `tools/check_dm_sources_consistency.py`, agrégés par `tools/aggregate_m1.py`) ;
- invariants critiques au vert, dont la distinction **Kevin Curtis / Ian
  Curtis** ;
- aucun champ `sources` ne doit contenir un identifiant interne comme `IMAGE-*`
  à la place d'une source documentaire `Sxx`.

La dette M1 résiduelle n'est plus portée par M1 : elle est **basculée en M3**
(voir la sous-section « Dette M1 résiduelle basculée en M3 »).

## Gouvernance GitHub et PR

`main` est protégée sur les deux dépôts par le ruleset `A1 — main governance` :

- toute modification de `main` passe par une PR (jamais de commit direct) ;
- au moins une review obligatoire, conversations de review résolues ;
- linear history imposée ; suppression et force-push interdits ; bypass supprimés ;
- check public requis : `check-generated-sync` ;
- check privé requis : `private-drift-check`.

La PR est le lieu normal de toute modification structurante. Ne jamais merger
une PR avec des checks rouges.

Contraintes d'automatisation (anticipation M2) : une automatisation peut préparer
une branche, générer les IDs, lancer les contrôles et **ouvrir** une PR, mais
elle ne doit **jamais merger** ni contourner la validation humaine. Le principe
« aucun commit sans validation humaine » reste applicable. Tenir compte des
limites du `GITHUB_TOKEN` (il ne déclenche pas nécessairement les workflows
attendus sur `pull_request`).

## Validation avant commit (CI publique requise)

Toujours relancer les validateurs concernés et obtenir **zéro erreur** avant
push. Le gate public requis `check-generated-sync` exécute, dans cet ordre :

    python tools/check_generated_sync.py
    python tools/build_all.py --quiet
    python tools/audit_repo.py --fail-on-error
    python tools/validate_orgs.py
    python tools/validate_images.py
    python tools/validate_chronology.py
    python tools/validate_concerts.py
    python tools/validate_places.py
    python tools/validate_songs.py
    python tools/validate_quotes.py
    python tools/validate_people.py --check-drift
    python tools/validate_attribution.py --check-drift
    python tools/validate_edges.py

## CI privée anti-drift

Côté repo privé, le check requis `private-drift-check` empêche la dérive des
artefacts générés sur toute PR vers `main`. Il contrôle aujourd'hui `STATUS.md`
et `STATUS_CONSOLIDATED.md` par comparaison normalisée (les métadonnées
volatiles — horodatage, branche, SHA — sont ignorées). Extension progressive
prévue : `chapters/master_docs.json`, documents maîtres générés et exports
privés.

## Synchronisation Knowledge Base Claude (après chaque passe)

Après toute mise à jour de `chapters/` dans le repo PRIVÉ, exécuter depuis le
repo PUBLIC :

    python tools/sync_dm_to_claude_kb.py

Le script génère `exports/generated/DM_consolidated_for_kb.md`. Uploader ce
fichier dans la KB du projet Claude si des DM ont changé. L'upload API sera
automatisé quand Anthropic exposera l'endpoint.

## Conventions de branche

Toutes les branches Claude : préfixe `claude/*`.
Jamais de commit direct sur `main` (interdit par le ruleset).

## Confirmation humaine

Toujours afficher le diff avant de commiter.
Toujours attendre confirmation humaine avant push vers `main`.
Jamais merger sans validation explicite.
