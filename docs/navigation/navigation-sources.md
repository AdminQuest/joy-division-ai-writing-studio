# Navigation niveau 1 — Sources

Objectif : comprendre où circule la matière documentaire.

## Schéma de lecture documentaire

```text
SOURCE
↓
ATOMISATION
↓
DOCUMENTS MAÎTRES
↓
REGISTRES
↓
EXPORTS
```

Note : le pipeline technique de génération ne suit pas exactement cet ordre de lecture. `tools/build_all.py` produit d'abord registres et exports depuis `sources/` et `registers/`, puis génère les documents maîtres.

## Répertoires réellement utilisés

| Couche | Emplacement | Rôle | Scripts / dépendances |
| --- | --- | --- | --- |
| Registre canonique des sources | `data/registre.json` | Liste les sources `SXX`, leurs libellés, statuts et métadonnées. | `tools/build_registers.py`, `tools/atomize_new_sources.py`, `tools/apply_s*_registre_patch.py` |
| Sources atomisées | `sources/` | Contient les fiches source, passages atomisés, atomes, citations, relations et patches de registre. | `tools/build_registers.py`, `tools/atomize_new_sources.py` |
| Configuration d'atomisation | `tools/atomisation/` | Contient la configuration locale de l'orchestrateur d'atomisation. | `tools/atomize_new_sources.py` |
| Registres | `registers/` | Stabilise les entités et relations extraites ou consolidées. | `tools/build_registers.py`, validateurs `tools/validate_*.py` |
| Documents maîtres par chapitre | `chapters/` | Contient `chapters/XX/document_maitre.md` et `chapters/master_docs.json`. | `tools/build_master_docs.py`, `tools/build_master_docs_with_notes.py`, `tools/inject_chapter_source_notes.py` |
| Documents maîtres par source | `master_docs/` | Contient des documents maîtres source ou passe documentaire. | Consultés comme dossiers documentaires existants. |
| Exports générés | `exports/generated/` | Produit les JSON/CSV exploités par apps, RAG, audits et contrôles. | `tools/build_registers.py`, `tools/build_all.py`, `tools/build_edges.py`, `tools/audit_repo.py` |
| Contextes RAG | `rag/context/` | Stocke des contextes YAML spécialisés par source ou passage. | RAG Studio, prompts, usage rédactionnel. |
| Prompts | `prompts/` | Contient des prompts et routeurs pour usage IA. | `exports/generated/prompt_context.json`, RAG Studio, workflows IA. |
| Rapports | `reports/` | Contient des rapports ponctuels ou de consolidation. | Audits et chantiers documentaires existants. |

## Cycle opérationnel

| Étape | Point d'entrée | Produit attendu | Contrôle associé |
| --- | --- | --- | --- |
| Fixer la source | `data/registre.json` | Identifiant `SXX` stable. | Vérifier unicité de l'identifiant. |
| Créer ou enrichir le dossier source | `sources/<slug>/` | Fiche source, fichiers `source_part_*.md`, atomes `SXX-ANNN`, citations `SXX-QNNN`, relations. | Respecter `docs/ATOMISATION_SOURCE.md`. |
| Consolider les registres | `registers/` | Entrées personnes, lieux, chansons, concepts, motifs, mythes, etc. | `python3 tools/build_registers.py --strict` |
| Produire les documents maîtres | `chapters/XX/document_maitre.md` | Dossiers documentaires par chapitre. | `python3 tools/build_master_docs.py` ou `python3 tools/build_all.py` |
| Produire les exports | `exports/generated/` | `exports/generated/atoms.json`, `exports/generated/quotes.json`, `exports/generated/sources.json`, `exports/generated/all_records.json`, etc. | `python3 tools/build_all.py` |
| Auditer | `exports/generated/audit_repo.*` | Rapport d'erreurs, warnings et blocs inconnus. | `python3 tools/audit_repo.py` |
| Vérifier la synchronisation | Artefacts générés | Aucun drift substantif. | `python3 tools/check_generated_sync.py` |

## Exports utiles

| Besoin | Export |
| --- | --- |
| Tous les enregistrements RAG | `exports/generated/all_records.json` |
| Atomes | `exports/generated/atoms.json` |
| Citations | `exports/generated/quotes.json` |
| Sources | `exports/generated/sources.json` |
| Enregistrements par source | `exports/generated/source_records.json` |
| Personnes | `exports/generated/people.json` |
| Lieux | `exports/generated/places.json` |
| Concerts | `exports/generated/concerts.json` |
| Sessions | `exports/generated/sessions.json` |
| Chansons | `exports/generated/songs.json` |
| Concepts | `exports/generated/concepts.json` |
| Motifs | `exports/generated/motifs.json` |
| Mythes | `exports/generated/myths.json` |
| Graphe / arêtes | `exports/generated/edges.json` |
| Index par identifiant | `exports/generated/index_by_id.json` |
| Audit | `exports/generated/audit_repo.md` |

## Règles de navigation

- Chercher d'abord la source dans `data/registre.json`.
- Chercher la matière documentaire dans `sources/<slug>/`.
- Chercher l'état consolidé dans `registers/`.
- Chercher l'état exploitable par outils dans `exports/generated/`.
- Ne pas modifier manuellement les fichiers générés.
- Ne pas créer de flux parallèle sous le dossier interdit chapters/addenda/.
