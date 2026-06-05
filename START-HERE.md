# START HERE

Ce fichier est le point d'entree stable du depot.

Il doit etre lu avant toute intervention, par un agent IA comme par un contributeur humain.

## 1. Objet du projet

Ce depot est l'environnement documentaire, historiographique et redactionnel du projet *Joy Division, le son de l'eternel*. Il ne sert pas seulement a stocker des fichiers. Il organise un corpus de travail sur Joy Division, Manchester, le post-punk, les sources critiques, les temoignages, les chansons, les lieux, les concerts, les images, les concepts, les motifs et les mythes.

Le depot repose sur une chaine documentaire stable : sources, atomes, registres, exports generes, audits, documents maitres, RAG Studio, prompts autonomes et redaction. Les sources et atomes portent la matiere documentaire. Les registres canoniques stabilisent les entites et les relations utiles au livre.

Les registres canoniques sont dans `registers/`. Ils couvrent notamment les personnes, organisations, lieux, chansons, concerts, sessions, citations, images, chronologie, concepts, motifs, mythes, references et relations. Les schemas sont dans `schemas/`. Les validateurs et outils de build sont dans `tools/`.

Les exports generes sont dans `exports/generated/`. Ils rendent le corpus exploitable par les outils, les applications et les flux RAG. Les applications de consultation sont dans `apps/`, dont les interfaces de registres et le RAG Studio. Les documents maitres par chapitre sont dans `chapters/`.

## 2. Regle de lecture pour agent IA

Un agent IA doit commencer par lire, dans cet ordre :

1. `START-HERE.md`
2. `STATUS.md`
3. `docs/roadmap-strategique-2026.md`

Il doit ensuite lire seulement les fichiers specialises necessaires a la tache. Il ne doit pas parcourir tout le depot sans objectif precis. Il ne doit pas lancer de chantier hors perimetre.

## 3. Etat de reference

`STATUS.md` donne l'etat technique courant du depot.

Ce fichier est genere automatiquement. Il ne doit pas etre edite manuellement.

Il resume l'etat des registres, des validateurs, des schemas, des lacunes connues et de la prochaine etape. Il indique aussi la branche et la reference git observees au moment de sa generation.

Si la roadmap, les audits ou les artefacts de pilotage changent, `STATUS.md` doit etre regenere avec `python3 tools/generate_status.py`, puis inclus dans le commit si son contenu differe.

## 4. Roadmap de reference

`docs/roadmap-strategique-2026.md` est la couche strategique du depot.

Elle ne remplace pas les fichiers techniques existants. Elle donne une lecture superieure des priorites et rattache les chantiers aux jalons M0 a M7.

M0 et M1 sont les seuls jalons activables immediatement. Ils portent sur la stabilisation du socle et la fiabilisation du corpus.

M2 est interdit tant que M0 et M1 ne sont pas stabilises. Il ne faut donc pas lancer de studio d'enrichissement documentaire, de refonte d'interface ou de fusion de repos dans le cadre d'une tache M0 ou M1.

## 5. Ou chercher l'information

| Besoin | Lire d'abord |
| --- | --- |
| Etat technique du depot | `STATUS.md` |
| Strategie et priorites | `docs/roadmap-strategique-2026.md` |
| Doctrine generale du depot | `REPO_DOCTRINE.md` |
| Workflow operationnel courant | `README.md` |
| Registres canoniques | `registers/` |
| Sources atomisees | `sources/` |
| Registre canonique des sources | `data/registre.json` |
| Schemas | `schemas/` |
| Validateurs | `tools/validate_*.py` |
| Generation du statut | `tools/generate_status.py` |
| Build global | `tools/build_all.py` |
| Synchronisation des artefacts generes | `tools/check_generated_sync.py` |
| Audit global | `tools/audit_repo.py` |
| Exports generes | `exports/generated/` |
| Applications de consultation | `apps/` |
| RAG Studio | `apps/rag-studio/` |
| Contextes RAG | `rag/context/` |
| Prompts autonomes | `prompts/` |
| Documents maitres par chapitre | `chapters/` |
| Documents maitres par source | `master_docs/` |
| Index existants | `indexes/` |
| Lacunes connues | `_meta/known_gaps.md` |

## 6. Regles de contribution

- Travailler sur une branche dediee.
- Ne pas modifier directement la branche principale.
- Limiter les changements au perimetre demande.
- Ne pas editer manuellement les fichiers generes.
- Regenerer `STATUS.md` lorsque la roadmap, les audits ou les artefacts de pilotage changent.
- Lancer les controles pertinents avant de conclure.

## 7. Commandes de controle

Ces commandes sont les controles de reference mentionnes par la roadmap, si les fichiers correspondants existent dans le depot :

```bash
python3 tools/generate_status.py
python3 tools/build_all.py
python3 tools/check_generated_sync.py
python3 tools/audit_repo.py
git status
```

`tools/generate_status.py` regenere directement `STATUS.md`.

`tools/build_all.py` controle le pipeline global : registres, documents maitres, exports et audits.

`tools/check_generated_sync.py` verifie la synchronisation des artefacts generes couverts par la sentinelle.

`tools/audit_repo.py` produit l'audit global.

`git status` doit etre consulte avant de conclure, avant de commit et avant d'ouvrir une pull request.

## 8. Ce que START-HERE.md n'est pas

Ce fichier ne remplace pas `STATUS.md`.

Il ne remplace pas `docs/roadmap-strategique-2026.md`.

Il ne remplace pas les validateurs.

Il ne constitue pas un index exhaustif du corpus.

Il ne decrit pas toutes les cartes de navigation possibles.

Il sert uniquement de porte d'entree stable avant lecture des documents specialises.
