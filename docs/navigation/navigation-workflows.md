# Navigation niveau 1 — Workflows

Objectif : repérer les workflows présents et leurs points d'entrée.

## Ajout ou atomisation de source

| Champ | Valeur |
| --- | --- |
| Point d'entrée documentaire | `docs/ATOMISATION_SOURCE.md`, `README.md`, `WORKFLOW_OFFICIEL.md` |
| Point d'entrée script | `tools/atomize_new_sources.py` |
| Fichiers sources | `data/registre.json`, `sources/<slug>/` |
| Scripts associés | `tools/apply_s*_registre_patch.py`, `tools/build_registers.py`, `tools/audit_repo.py` |
| Fichiers générés ou impactés | `exports/generated/*.json`, `exports/generated/*.csv`, `exports/generated/diagnostics.*`, `exports/generated/audit_repo.*` |
| Contrôles | `python3 tools/build_registers.py --strict`, `python3 tools/audit_repo.py`, `python3 tools/check_generated_sync.py` |

Séquence observée dans l'orchestrateur :

```text
tools/atomize_new_sources.py --detect
tools/atomize_new_sources.py --prepare SXX
travail documentaire dans sources/ et registers/
tools/atomize_new_sources.py --commit-and-pr SXX
tools/atomize_new_sources.py --finalize SXX
```

## Enrichissement documentaire

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `WORKFLOW_OFFICIEL.md`, `docs/MAINTENANCE_WORKFLOW.md` |
| Cible | Atomes, relations, concepts, motifs, mythes, registres transversaux. |
| Répertoires | `sources/`, `registers/`, `rag/context/`, `prompts/` |
| Scripts associés | `tools/build_registers.py`, `tools/build_historiographical_diagnostics.py`, `tools/build_prompt_context.py` |
| Fichiers générés | `exports/generated/atoms.json`, `exports/generated/concepts.json`, `exports/generated/motifs.json`, `exports/generated/myths.json`, `exports/generated/historiographical_diagnostics.json`, `exports/generated/prompt_context.json` |
| Contrôles | `python3 tools/build_registers.py --strict`, `python3 tools/build_historiographical_diagnostics.py`, `python3 tools/build_prompt_context.py` |

Ne pas confondre ce workflow avec M2. Ce niveau documente l'existant. Il ne crée pas de studio d'enrichissement.

## Validation

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `STATUS.md`, validateurs `tools/validate_*.py` |
| Registres couverts | Organisations, images, chronologie, concerts, personnes, lieux, chansons, citations, attribution, edges. |
| Scripts | `tools/validate_orgs.py`, `tools/validate_images.py`, `tools/validate_chronology.py`, `tools/validate_concerts.py`, `tools/validate_people.py`, `tools/validate_places.py`, `tools/validate_songs.py`, `tools/validate_quotes.py`, `tools/validate_attribution.py`, `tools/validate_edges.py` |
| Schémas | `schemas/` |
| Fichiers générés | Aucun par principe ; les validateurs contrôlent. |
| Contrôle global associé | `python3 tools/generate_status.py` exécute les validateurs affichés dans `STATUS.md`. |

## Génération documentaire

| Champ | Valeur |
| --- | --- |
| Point d'entrée global | `tools/build_all.py` |
| Étape 1 | `tools/build_registers.py` avec option `--strict` |
| Étape 2 | `tools/build_attribution_edges.py` |
| Étape 3 | `tools/build_registers.py` avec option `--strict` |
| Étape 4 | `tools/build_master_docs.py` |
| Étape 5 | `tools/build_edges.py` |
| Étape 6 | `tools/audit_repo.py` |
| Option | `tools/inject_chapter_source_notes.py` via `tools/build_all.py` avec option `--with-source-notes` |
| Fichiers générés | `exports/generated/`, `chapters/XX/document_maitre.md`, `chapters/master_docs.json`, `registers/relations/attribution_edges.json` |
| Contrôle associé | `python3 tools/check_generated_sync.py` |

## Documents maîtres

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `chapters/XX/document_maitre.md` |
| Scripts | `tools/build_master_docs.py`, `tools/build_master_docs_with_notes.py`, `tools/inject_chapter_source_notes.py` |
| Entrées | `exports/generated/atoms.json`, `exports/generated/quotes.json`, `chapters/XX/source_notes*.md` |
| Fichiers générés | `chapters/XX/document_maitre.md`, `chapters/master_docs.json`, `exports/generated/master_docs_index.json` |
| Contrôles | `python3 tools/build_all.py`, `python3 tools/check_generated_sync.py` |

## RAG local et recherche

| Champ | Valeur |
| --- | --- |
| Point d'entrée doc | `docs/RAG_SETUP.md`, `docs/WEB_INTERFACE.md` |
| Point d'entrée script | `tools/rag_search.py`, `tools/rag_server.py` |
| Application | `apps/rag-studio/` |
| Entrées | `exports/generated/all_records.json`, `exports/generated/source_records.json`, `data/registre.json` |
| Fichiers générés | Aucun par la recherche ; les exports doivent être produits avant usage. |
| Contrôles | `python3 tools/build_registers.py`, puis recherche avec `python3 tools/rag_search.py "<requête>"` ou serveur avec `python3 tools/rag_server.py` |

## Publication / interface web

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `index.html`, `apps/`, `docs/WEB_INTERFACE.md` |
| Applications présentes | `apps/*-register/`, `apps/rag-studio/` |
| Assets | `assets/` |
| Serveur local | `tools/rag_server.py` |
| Entrées | Exports générés, registres JSON, Markdown parsé par `apps/lib/dynamic-registers.js` |
| Contrôles | Vérifier les chemins d'apps, puis `python3 tools/check_generated_sync.py` pour les exports. |

## Audit

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `tools/audit_repo.py` |
| Entrées | Exports générés et diagnostics. |
| Fichiers générés | `exports/generated/audit_repo.md`, `exports/generated/audit_repo.json`, `exports/generated/audit_repo_issues.csv` |
| Contrôles | `python3 tools/audit_repo.py`, puis `python3 tools/check_generated_sync.py` si les artefacts générés ont changé. |

## Statut du dépôt

| Champ | Valeur |
| --- | --- |
| Point d'entrée | `STATUS.md` |
| Générateur | `tools/generate_status.py` |
| Entrées | `registers/`, `schemas/`, `_meta/known_gaps.md`, validateurs listés dans le générateur. |
| Fichier généré | `STATUS.md` |
| Contrôle | `python3 tools/generate_status.py`, puis vérifier le diff. |

## Commandes de contrôle usuelles

```bash
python3 tools/generate_status.py
python3 tools/build_all.py
python3 tools/check_generated_sync.py
python3 tools/audit_repo.py
git status
```
