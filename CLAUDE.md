# CLAUDE.md — Règles permanentes du projet

## Régénération des exports (OBLIGATOIRE avant tout push)

À la fin de chaque session qui modifie des fichiers sources
(registers/, sources/, apps/), exécuter AVANT tout push :

    python tools/build_all.py
    git add registers/ exports/generated/ chapters/*/document_maitre.md chapters/master_docs.json
    git commit -m "chore(generated): régénération artefacts [session]"

Le check `check-generated-sync` doit passer à vert avant toute PR.
Ne jamais pousser sans avoir régénéré les exports.

## Conventions de branche

Toutes les branches Claude : préfixe `claude/*`
Jamais de commit direct sur `main`.

## Validation avant commit

Toujours relancer les validateurs concernés :
    python tools/validate_places.py
    python tools/validate_orgs.py
    python tools/validate_images.py
    # etc.

Zéro erreur requis avant push.

## Confirmation humaine

Toujours afficher le diff avant de commiter.
Toujours attendre confirmation humaine avant push.
Jamais merger sans validation explicite.
