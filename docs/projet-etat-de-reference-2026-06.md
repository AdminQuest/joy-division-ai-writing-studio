# État de référence du projet

État de référence : juin 2026.

Le projet est aujourd'hui un atelier documentaire et rédactionnel consacré au livre Joy Division. Il rassemble un corpus structuré, des registres canoniques, des exports générés, des documents maîtres, des applications de consultation, un RAG d'exploration et des workflows de contrôle.

Le projet n'est pas un simple dépôt de notes, ni une application unique, ni un studio d'enrichissement automatisé. Il n'est pas encore une architecture finale unifiée, ni une chaîne de publication définitive. Les évolutions futures doivent respecter les décisions stabilisées avant d'ajouter de nouvelles surfaces.

# Architecture stabilisée

```text
Collection
↓
Usine
↓
Entrepôt
↓
Atelier
↓
Vigie
```

## Collection

| Champ | Valeur |
| --- | --- |
| Fonction | Rassembler les sources, atomes, références, registres et matériaux documentaires. |
| Périmètre | `sources/`, `registers/`, `data/registre.json`, conventions et schemas. |
| Objets principaux | Sources, atomes, citations, personnes, lieux, concerts, chansons, images, organisations, concepts, motifs, mythes, sessions, relations. |
| Limites | Les données restent hétérogènes par nature ; les écarts de volumétrie et les diagnostics existants relèvent de la fiabilisation, pas d'une refonte M0. |

## Usine

| Champ | Valeur |
| --- | --- |
| Fonction | Produire les exports, documents maîtres, arêtes, audits et snapshots depuis le corpus. |
| Périmètre | `tools/build_all.py`, `tools/build_registers.py`, `tools/build_master_docs.py`, `tools/build_edges.py`, `tools/audit_repo.py`, `tools/generate_status.py`. |
| Objets principaux | Exports JSON/CSV, documents maîtres, manifest, index, diagnostics, audit repo, `STATUS.md`. |
| Limites | `tools/generate_status.py` reste le producteur direct de `STATUS.md`; `tools/build_all.py` reste le contrôle global du pipeline documentaire mais ne produit pas directement `STATUS.md`. |

## Entrepôt

| Champ | Valeur |
| --- | --- |
| Fonction | Conserver les vues et artefacts exploitables par les applications, audits et outils d'exploration. |
| Périmètre | `exports/generated/`, `chapters/*/document_maitre.md`, `chapters/master_docs.json`, `exports/generated/master_docs_index.json`. |
| Objets principaux | Exports générés, diagnostics, audits, documents maîtres, manifest, index et arêtes. |
| Limites | Les artefacts générés ne doivent pas être corrigés manuellement ; tout écart doit être régénéré par l'outil canonique ou signalé. |

## Atelier

| Champ | Valeur |
| --- | --- |
| Fonction | Préparer la rédaction du manuscrit à partir du corpus, des documents maîtres et des explorations RAG. |
| Périmètre | Documents maîtres, notes rédactionnelles, prompts, usage de Manuscript / Forge / Atelier comme espace de production du manuscrit. |
| Objets principaux | Dossiers de chapitre, matériaux de rédaction, prompts, synthèses, livrables conservés ou temporaires. |
| Limites | L'Atelier ne remplace pas le corpus et ne devient pas source de vérité documentaire. Les choix rédactionnels doivent rester séparés de l'autorité documentaire. |

## Vigie

| Champ | Valeur |
| --- | --- |
| Fonction | Observer la cohérence du socle et signaler les écarts avant publication ou merge. |
| Périmètre | `tools/check_generated_sync.py`, validateurs, audits, GitHub Actions, revue humaine. |
| Objets principaux | Checks CI, diagnostics, audits, statuts de validation, réserves documentées. |
| Limites | La CI dépend de GitHub Actions et n'est pas un artefact versionné. Les décisions de clôture ou de passage de jalon restent humaines. |

# Doctrine documentaire stabilisée

- Corpus = socle documentaire.
- RAG = outil d'exploration du corpus.
- Documents maîtres = vues rédactionnelles persistantes du corpus exporté.
- `tools/build_master_docs.py` = producteur technique actuel des documents maîtres.
- Forge / Atelier = espace de production du manuscrit.
- Documentation et rédaction restent séparées.
- Les vues générées n'ont pas d'autorité documentaire propre.
- Les informations rédactionnelles doivent rester traçables vers le corpus lorsqu'elles portent un fait, une citation, une relation ou une interprétation appuyée.

# Décisions majeures acquises

- Le corpus est la source de vérité documentaire.
- Les documents maîtres ne sont ni des sources, ni des preuves autonomes, ni des registres canoniques.
- Le RAG explore, filtre, regroupe et assemble des vues du corpus, mais ne produit pas techniquement les documents maîtres.
- Les objets persistants sont distingués des vues générées.
- Les artefacts générés sont produits par les outils canoniques et ne doivent pas être corrigés manuellement.
- `tools/generate_status.py` produit directement `STATUS.md`.
- `tools/build_all.py` reste le contrôle global du pipeline registres / documents maîtres / exports / audits.
- M0 est clôturé et ne doit pas être rouvert pour corriger des réserves déjà acceptées comme non bloquantes.

# M0

| Champ | Valeur |
| --- | --- |
| Objectif | Stabiliser le socle existant et rendre lisible l'état réel du projet. |
| Livrables | `docs/m0-architecture-corpus-rag-manuscript.md`, `docs/m0-etat-du-socle.md`, `docs/m0-audit-sortie.md`, `docs/m0-cloture.md`. |
| Résultat | Architecture, inventaire, dépendances, critères de sortie et réserves non bloquantes documentés. |
| Date de clôture | 2026-06-05, à compter de la PR de clôture M0. |

# M1

M1 a pour objectif général de fiabiliser le corpus documentaire sans ouvrir de studio d'enrichissement. Son périmètre attendu porte sur les contrôles, la traçabilité, les invariants, les validateurs, les écarts documentaires et la cohérence entre registres, exports, documents maîtres et sources.

Les sujets déjà identifiés sont :

- fiabilisation des liens inter-registres, invariants et validateurs ;
- traçabilité fine des documents maîtres vers sources, atomes, registres et exports ;
- qualification documentaire des livrables RAG conservés ;
- analyse des warnings et blocs inconnus signalés par les diagnostics générés ;
- clarification des écarts de volumétrie entre canons et exports lorsque ces écarts affectent la fiabilité documentaire.

Ce document ne détaille pas les travaux M1 et ne les ouvre pas.

# Sujets explicitement reportés

- Cloudflare.
- Architecture finale unifiée.
- `manuscript-studio`.
- Génération dynamique éventuelle des documents maîtres.
- Formulaires d'ajout documentaire.
- Studio d'enrichissement documentaire.
- Génération automatique d'identifiants pour ajouts courants.
- Contrôles avant commit liés à un workflow d'ajout.
- Améliorations d'interface visant l'ajout ou la modification des données.
- Refondre ou non les interfaces de consultation.
- Intégration d'un repo privé unifié.
- Politique multimédia, droits, provenance et republication.

# Invariants du projet

- Le corpus est la source de vérité.
- Les documents maîtres ne sont pas des sources.
- Le RAG n'est pas le producteur technique des documents maîtres.
- Les documents maîtres sont générés actuellement par `tools/build_master_docs.py`.
- Les artefacts générés ne sont jamais corrigés manuellement.
- `STATUS.md` est généré par `tools/generate_status.py`.
- `tools/build_all.py` ne doit pas être présenté comme générateur direct de `STATUS.md` sauf changement explicite du code.
- Les réserves acceptées à la clôture M0 ne doivent pas être transformées rétroactivement en blocages M0.
- M2 ne doit pas être ouvert avant décision explicite.
- Les décisions d'architecture doivent être documentées avant toute refonte.

# Utilisation du document

Ce document sert :

- à reprendre le projet après interruption ;
- à accueillir un nouvel agent ;
- à préparer les futures évolutions ;
- à éviter de rouvrir les décisions M0 déjà stabilisées ;
- à distinguer les décisions acquises, les sujets reportés et les futurs jalons.

Il doit être lu comme un repère de continuité stratégique, pas comme une roadmap et pas comme une demande d'exécution.
