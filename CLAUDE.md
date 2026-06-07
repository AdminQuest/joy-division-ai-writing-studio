# CLAUDE.md — Règles permanentes du projet

> Mise à jour : 2026-06-07, après audit des dépôts public
> (`joy-division-ai-writing-studio`) et privé (`joy-division-studio-private`)
> et alignement sur la `ROADMAP.md` 2026.

## Principe directeur 2026

Le corpus est désormais suffisamment constitué pour alimenter le manuscrit.
Le projet sort de la phase d'accumulation documentaire ; la priorité est la
**consolidation** : protection GitHub, CI contraignante, synchronisation
public / privé, graphe relationnel inter-registres, atomisation augmentée par
mesure d'impact, puis reprise sélective du Studio après retour d'usage réel.

Règle de conduite :

> Ne pas augmenter fortement le volume documentaire tant que les contraintes de
> validation, de synchronisation et de relation ne sont pas stabilisées.

Priorité opérationnelle immédiate (voir `ROADMAP.md` — repo privé) :

1. C3A-7 — audit joydiv.org pour enrichissement public du hub ;
2. C3A — densifier les liens inter-registres (concerts ↔ chronologie,
   releases ↔ chronologie / lieux / sessions, chansons ↔ concerts, personnes ↔
   concerts / sessions) ;
3. C3B — mesure d'impact intégrée au flux d'atomisation ;
4. Studio du manuscrit — expérimentation réelle, **sans nouveau développement**
   jusqu'au retour d'usage.

## Régénération des exports (OBLIGATOIRE avant tout push)

À la fin de chaque session qui modifie des fichiers sources
(registers/, sources/, apps/, chapters/), exécuter AVANT tout push :

    python tools/build_all.py
    git add exports/generated/
    git commit -m "chore(generated): régénération exports [session]"

`build_all.py` est le build canonique : il régénère notamment le graphe
relationnel `exports/generated/edges.json` via `tools/build_edges.py`.

Le check requis `check-generated-sync` doit passer à vert avant toute PR.
Ne jamais pousser sans avoir régénéré les exports.

## Gouvernance GitHub et PR (Phase A — terminée)

`main` est protégée sur les deux dépôts par le ruleset `A1 — main governance` :

- toute modification de `main` passe par une PR (jamais de commit direct) ;
- au moins une review obligatoire, conversations de review résolues ;
- linear history imposée ; suppression et force-push interdits ; bypass supprimés ;
- check public requis : `check-generated-sync` ;
- check privé requis : `private-drift-check`.

La PR est le lieu normal de toute modification structurante. Ne jamais merger
une PR avec des checks rouges.

## Validation avant commit (CI publique B1)

Toujours relancer les validateurs concernés et obtenir **zéro erreur** avant
push. Le gate public requis exécute, dans cet ordre :

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

## CI privée anti-drift (Phase B2 — lot minimal terminé)

Côté repo privé, le check `private-drift-check` empêche la dérive des
artefacts générés sur toute PR vers `main`. Il contrôle aujourd'hui
`STATUS.md` et `STATUS_CONSOLIDATED.md` par comparaison normalisée (les
métadonnées volatiles — horodatage, branche, SHA — sont ignorées).
Extension progressive prévue : `chapters/master_docs.json`, documents maîtres
générés et exports privés.

## Synchronisation Knowledge Base Claude (après chaque passe)

Après toute mise à jour de chapters/ dans le repo PRIVÉ,
exécuter depuis le repo PUBLIC :

    python tools/sync_dm_to_claude_kb.py

Le script génère `exports/generated/DM_consolidated_for_kb.md`.
Uploader ce fichier dans la KB du projet Claude si des DM ont changé.
L'upload API sera automatisé quand Anthropic exposera l'endpoint.

## Conventions de branche

Toutes les branches Claude : préfixe `claude/*`.
Jamais de commit direct sur `main` (interdit par le ruleset).

## Actions explicitement suspendues (phases A à D)

- atomisation massive de nouvelles sources ;
- création de nouveaux registres non indispensables ;
- enrichissement manuel des documents maîtres générés ;
- chasse exhaustive aux champs v2 manquants ;
- grosses intégrations non reliées au graphe ;
- nouveaux développements Studio jusqu'au retour d'usage réel.

Une nouvelle source reste possible seulement si elle sert une lacune
identifiée, une controverse, un chapitre faible, une relation manquante ou une
vérification citationnelle.

## Confirmation humaine

Toujours afficher le diff avant de commiter.
Toujours attendre confirmation humaine avant push vers `main`.
Jamais merger sans validation explicite.
