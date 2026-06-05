# M0 — Etat du socle existant

Etat date : 2026-06-05.

Cette note complete M0 par un inventaire du socle existant et une cartographie initiale des dependances. Elle prolonge la note `docs/m0-architecture-corpus-rag-manuscript.md` sans la remplacer.

Doctrine M0 conservee :

- Corpus = socle documentaire ;
- RAG = outil d'exploration du corpus ;
- Manuscript = outil redactionnel ;
- documents maitres = vues redactionnelles persistantes du corpus exporte, generees par `tools/build_master_docs.py`.

Cette note est une documentation d'etat. Elle ne modifie pas la roadmap, ne cree pas de script, n'ouvre pas M1, n'ouvre pas M2 et ne lance aucune refonte.

## Perimetre M0 rappele

Le perimetre M0 couvre l'etat observable des composants deja presents :

- applications publiques existantes ;
- registres canoniques ;
- exports generes ;
- audits documentaires ;
- RAG Studio ;
- manuscript-studio, cite par la roadmap mais non materialise par un chemin local verifie ;
- documents maitres ;
- dependances entre outils de build, validation et publication.

M0 doit rendre ce socle lisible sans relire l'historique complet des PR, audits et corrections. Il ne doit pas transformer l'inventaire en chantier d'enrichissement, en refonte d'interface ou en studio d'ajout.

## Etat date des applications existantes

| Application | Chemin | Fonction | Statut connu | Dependances principales | Limites connues |
| --- | --- | --- | --- | --- | --- |
| Portail statique | `index.html` | Point d'entree web local et publie. | Present. | `apps/`, `assets/`, exports et registres consommes par les apps. | Publication dependante de GitHub Pages et du cache navigateur. |
| Registre chronologique | `apps/chronology-register/` | Consulter le registre chronologique. | Present dans `apps/`. | `apps/lib/dynamic-registers.js`, `registers/chronology/`. | Volumetrie canonique et export ne sont pas identiques. |
| Registre concepts / motifs / mythes | `apps/concept-register/` | Explorer concepts, motifs, mythes et liens documentaires. | Present dans `apps/`. | `exports/generated/concepts.json`, `motifs.json`, `myths.json`, `atoms.json`, `quotes.json`, `sources.json`, `edges.json`, `index_by_id.json`. | Depend fortement de la fraicheur des exports generes. |
| Registre des concerts | `apps/concerts-register/` | Consulter concerts canoniques, statuts, lieux et liens. | Present dans `apps/`. | `exports/generated/concerts.json`, `places.json`, `edges.json`, `index_by_id.json`. | Futur formulaire d'ajout explicitement hors M0 et rattache a M2 seulement plus tard. |
| Registre iconographique | `apps/images-register/` | Consulter images et seances iconographiques. | Present dans `apps/`. | `registers/images/images.json`. | Droits, provenance et publication multimedia restent a traiter hors M0. |
| Registre des organisations | `apps/organizations-register/` | Consulter organisations canoniques. | Present dans `apps/`. | `registers/orgs/orgs.json`. | Gestion des entrees privees cote GitHub Pages indiquee dans l'app. |
| Registre des acteurs | `apps/people-register/` | Consulter personnes canoniques, alias, categories et citations attribuees. | Present dans `apps/`. | `apps/lib/dynamic-registers.js`, `registers/people/`, `registers/relations/attribution_edges.json`. | Certains liens d'attribution restent a surveiller par validateurs dedies. |
| Registre des lieux | `apps/places-register/` | Explorer lieux, cartes et relations avec concerts. | Present dans `apps/`. | `exports/generated/places.json`, `concerts.json`, `edges.json`, `index_by_id.json`, Leaflet CDN. | Depend d'un CDN cartographique externe. |
| Registre des citations | `apps/quote-register/` | Consulter les citations depuis l'export genere. | Present dans `apps/`. | `exports/generated/quotes.json`. | Les citations doivent rester reliees aux attributions et sources. |
| RAG Studio | `apps/rag-studio/` | Rechercher, filtrer, regrouper et preparer des prompts depuis le corpus. | Present dans `apps/`. | `exports/generated/all_records.json`, `exports/generated/source_records.json`, `data/registre.json`. | Outil d'exploration ; ne produit pas techniquement les documents maitres. |
| Registre des sessions | `apps/sessions-register/` | Consulter sessions, repetitions, demos, radio, studio et TV. | Present dans `apps/`. | `exports/generated/sessions.json`, `exports/generated/sessions.csv`. | Couverture documentaire a maintenir via exports. |
| Registre des chansons | `apps/song-register/` | Consulter chansons canoniques et donnees de variantes. | Present dans `apps/`. | `apps/lib/dynamic-registers.js`, `registers/songs/`, `sources/`, `schemas/song.schema.json`. | Certaines donnees de variantes sont configurees dans l'app ; `songs.json` reste consomme par le pipeline Python. |
| Registre des sources | `apps/source-register/` | Explorer sources, atomes, citations et relations par source. | Present dans `apps/`. | `exports/generated/sources.json`, `source_records.json`, `quotes.json`, `atoms.json`, `edges.json`, `index_by_id.json`. | Depend de l'alignement entre `data/registre.json`, `sources/` et exports. |
| Serveur RAG local | `tools/rag_server.py` | Sert le portail local, le RAG et les endpoints locaux. | Present comme outil local. | `tools/rag_search.py`, `exports/generated/all_records.json`, `chapters/`. | Outil local, pas une publication autonome. |
| manuscript-studio | Non trouve dans le depot au 2026-06-05. | Outil redactionnel cite conceptuellement par la roadmap. | Non verifie localement. | Documents maitres et materiaux documentaires, selon doctrine M0. | Chemin absent ; etat fonctionnel non verifie dans cette PR. |

## Etat date des registres canoniques

Les volumes ci-dessous distinguent, lorsque c'est utile, le volume canonique affiche par `STATUS.md` et le volume exporte dans `exports/generated/`.

| Registre | Chemin | Role | Volumetrie disponible | Statut connu | Limites connues |
| --- | --- | --- | --- | --- | --- |
| Sources | `data/registre.json`, `sources/` | Referencer les sources et porter les unites documentaires atomisees. | 97 sources declarees ; 82 sources exportees ; 82 sources utilisees ; 15 declarees non utilisees. | Actif, exploite par RAG Studio et source-register. | Les sources declarees non utilisees restent a interpreter comme limite d'inventaire, pas comme correction M0. |
| Atomes | `sources/` | Porter les unites documentaires extraites des sources. | 2770 atomes exportes. | Actif, base des exports et documents maitres. | La derivabilite fine des documents maitres vers atomes reste a auditer. |
| Organisations | `registers/orgs/orgs.json` | Stabiliser organisations, labels, medias et entites collectives. | 8 entrees, dont 6 publiques et 2 privees. | Validateur public au vert dans `STATUS.md`. | Distinction personne / organisation a maintenir. |
| Images | `registers/images/images.json` | Stabiliser images et seances iconographiques. | 11 entrees. | Validateur public au vert dans `STATUS.md`. | Droits et provenance multimedia restent hors M0. |
| Chronologie | `registers/chronology/` | Stabiliser evenements dates et chronologie documentaire. | 62 entrees canoniques dans `STATUS.md` ; 539 enregistrements exportes. | Validateur public au vert dans `STATUS.md`. | Ecart de volumetrie entre canon et exports a documenter. |
| Concerts | `registers/concerts/` | Stabiliser concerts, dates, statuts et lieux. | 190 entrees canoniques dans `STATUS.md` ; 388 enregistrements exportes. | Validateur public au vert dans `STATUS.md`. | Application existante a auditer, formulaire d'ajout interdit a ce stade. |
| Acteurs | `registers/people/` | Stabiliser personnes, auteurs, entourage et figures critiques. | 167 entrees canoniques dans `STATUS.md` ; 510 enregistrements exportes. | Validateur public au vert dans `STATUS.md`. | Attributions et doublons critiques restent controles par validateurs dedies. |
| Lieux | `registers/places/` | Stabiliser lieux, villes, salles et studios. | 197 entrees dans `STATUS.md` ; 202 entrees dans `places.json`. | Validateur public au vert dans `STATUS.md`. | Geocodage et precision restent limites connues. |
| Chansons | `registers/songs/` | Stabiliser le canon des chansons Joy Division et entrees liees. | 51 entrees canoniques dans `STATUS.md` ; 110 enregistrements exportes. | Validateur public au vert dans `STATUS.md`. | Variantes et donnees externes doivent rester separees du canon. |
| Citations | `registers/quotes/`, `registers/relations/attribution_edges.json` | Centraliser citations courtes et attributions. | 962 citations / aretes d'attribution couvertes. | Validateur public au vert dans `STATUS.md`. | Les attributions a resoudre restent une zone de suivi. |
| Concepts | `registers/concepts/` | Stabiliser concepts structurants. | 463 enregistrements exportes. | Actif via `tools/build_registers.py`. | Non liste dans les validateurs publics de `STATUS.md`. |
| Motifs | `registers/motifs/` | Stabiliser motifs recurrents. | 427 enregistrements exportes. | Actif via `tools/build_registers.py`. | Non liste dans les validateurs publics de `STATUS.md`. |
| Mythes | `registers/myths/` | Stabiliser mythes, lectures a deconstruire et constructions memorielles. | 102 enregistrements exportes. | Actif via `tools/build_registers.py`. | Non liste dans les validateurs publics de `STATUS.md`. |
| Sessions | `registers/sessions/` | Stabiliser sessions, repetitions, demos, radio, studio et TV. | 26 enregistrements exportes. | Actif via exports et application dediee. | Pas liste dans les validateurs publics de `STATUS.md`. |
| Relations | `registers/relations/` | Porter les aretes documentaires, dont attributions. | 962 aretes d'attribution. | Regenere par `tools/build_attribution_edges.py`. | Divergence possible si attributions et personnes ne sont pas regenerees ensemble. |
| References | `registers/references/` | Regrouper references, relations RAG et complements bibliographiques. | Volumetrie non consolidee dans `STATUS.md`. | Actif via build documentaire. | Typologie heterogene. |
| Registres specialises | `registers/specialized/`, `registers/s*_*.md` | Porter des registres source-specifiques ou thematiques. | Volumetrie non consolidee dans `STATUS.md`. | Actif via build documentaire. | Heterogeneite volontaire, a ne pas normaliser dans M0. |

## Etat date des exports generes

| Export | Chemin | Generateur | Usage | Statut | Couverture par `check_generated_sync.py` |
| --- | --- | --- | --- | --- | --- |
| Tous les enregistrements | `exports/generated/all_records.json` | `tools/build_registers.py` via `tools/build_all.py` | Corpus agrege pour RAG Studio et recherche. | Genere et versionne. | Oui, via sentinelle. |
| Index par identifiant | `exports/generated/index_by_id.json` | `tools/build_registers.py` | Resolution d'identifiants par apps et graphes. | Genere et versionne. | Oui. |
| Sources | `exports/generated/sources.json`, `sources.csv`, `source_records.json`, `source_records.csv` | `tools/build_registers.py` | Source-register, RAG Studio, audits. | Genere et versionne. | Oui. |
| Atomes | `exports/generated/atoms.json`, `atoms.csv` | `tools/build_registers.py` | Base documentaire, documents maitres, RAG Studio. | Genere et versionne. | Oui. |
| Citations | `exports/generated/quotes.json`, `quotes.csv` | `tools/build_registers.py`, attributions via `tools/build_attribution_edges.py` | Quote-register, documents maitres, controle d'attribution. | Genere et versionne. | Oui. |
| Concepts / motifs / mythes | `exports/generated/concepts.*`, `motifs.*`, `myths.*` | `tools/build_registers.py` | Concept-register, analyses transversales, prompt context. | Genere et versionne. | Oui. |
| Registres publics | `exports/generated/people.*`, `places.*`, `concerts.*`, `songs.*`, `sessions.*`, `chronology.*` | `tools/build_registers.py` | Applications de consultation et controles. | Genere et versionne. | Oui. |
| Metadata / templates / rules / quote batches | `exports/generated/metadata.*`, `templates.*`, `rules.*`, `quote_batches.*` | `tools/build_registers.py` | Controle documentaire et donnees auxiliaires. | Genere et versionne. | Oui. |
| Aretes d'attribution | `exports/generated/attribution_edges.json` | `tools/build_attribution_edges.py` | Attribution citation -> personne. | Genere et versionne. | Oui. |
| Aretes documentaires | `exports/generated/edges.json` | `tools/build_edges.py` | Navigation inter-registres et apps. | Genere et versionne. | Oui. |
| Index documents maitres | `exports/generated/master_docs_index.json` | `tools/build_master_docs.py` | Inventaire des documents maitres par chapitre. | Genere et versionne. | Oui. |
| Diagnostics | `exports/generated/diagnostics.json`, `diagnostics.md`, `diagnostics.csv` | `tools/build_registers.py` | Suivi des warnings et inconnus. | Genere et versionne ; statut `warning`. | Oui. |
| Audit repo | `exports/generated/audit_repo.json`, `audit_repo.md`, `audit_repo_issues.csv` | `tools/audit_repo.py` | Audit synthetique du repo documentaire. | Genere et versionne ; 0 erreur, 28870 warnings. | Oui. |
| README exports | `exports/generated/README.md` | Redactionnel | Explique certains artefacts. | Versionne. | Non genere. |

Limite connue : `exports/generated/README.md` affirme un modele de gitignore qui ne decrit pas completement l'etat observe, car de nombreux exports sont bien suivis par Git et couverts par la sentinelle. Cette note signale l'ecart documentaire sans le corriger.

## Etat date des audits documentaires

| Audit | Chemin | Generateur | Fonction | Statut | Limites connues |
| --- | --- | --- | --- | --- | --- |
| Audit repo synthetique | `exports/generated/audit_repo.md`, `audit_repo.json`, `audit_repo_issues.csv` | `tools/audit_repo.py` | Synthese des records, diagnostics, sources et problemes. | Genere ; 8644 records, 0 erreur, 28870 warnings, 1404 unknown. | Les warnings existants ne sont pas resolus par M0. |
| Diagnostics repo | `exports/generated/diagnostics.md`, `diagnostics.json`, `diagnostics.csv` | `tools/build_registers.py` | Liste des diagnostics produits par le parser documentaire. | Genere ; statut `warning`. | Volume eleve de warnings existants. |
| Audit chronologie 12b-3 | `docs/audits/audit_unitaire_chronologie_12b-3.md` | Audit redactionnel | Controle unitaire chronologie. | Documente. | Non regenere automatiquement par cette PR. |
| Audit citations 12b-5 | `docs/audits/audit_unitaire_citations_12b-5.md` | Audit redactionnel | Controle unitaire citations. | Documente. | Non regenere automatiquement par cette PR. |
| Audit concerts 12b-4 | `docs/audits/audit_unitaire_concerts_12b-4.md` | Audit redactionnel | Controle unitaire concerts. | Documente. | Non regenere automatiquement par cette PR. |
| Audit lieux 12b-1c | `docs/audits/audit_unitaire_lieux_12b-1c.md` | Audit redactionnel | Controle unitaire lieux. | Documente. | Non regenere automatiquement par cette PR. |
| Audit personnes etape 9 | `docs/audits/etape9_personnes_audit.md` | Audit redactionnel | Controle personnes, typage et rattachements. | Documente. | Non regenere automatiquement par cette PR. |
| Notes canon etape 9 | `docs/canon/etape9_*.md` | Notes de canonisation | Documenter attribution, personnes et refonte people. | Documente. | Documentation d'etape, pas audit global M0. |

## Etat date des documents maitres

| Element | Chemin | Generateur | Statut | Limites connues |
| --- | --- | --- | --- | --- |
| Documents maitres par chapitre | `chapters/*/document_maitre.md` | `tools/build_master_docs.py` via `tools/build_all.py` | 14 vues redactionnelles persistantes du corpus exporte. | Risque d'obsolescence ; tracabilite a renforcer vers atomes, registres, sources et exports. |
| Manifeste documents maitres | `chapters/master_docs.json` | `tools/build_master_docs.py` | 14 documents declares. | Doit rester coherent avec les fichiers de chapitre. |
| Index documents maitres | `exports/generated/master_docs_index.json` | `tools/build_master_docs.py` | 14 chapitres indexes pour controle et navigation. | Date de generation a maintenir via pipeline, pas par edition manuelle. |
| Synchronisation Claude KB | `tools/sync_dm_to_claude_kb.py` | Script de sync externe | Dependence M0 identifiee par la roadmap. | Usage cible externe ; etat non verifie par les controles M0 de cette PR. |

Les documents maitres ne sont pas des sources, pas des preuves autonomes et pas des registres. Ils sont des vues persistantes produites par le pipeline actuel a partir du corpus exporte.

## Table des dependances build / validation / publication

| Outil | Chemin | Type | Entrees | Sorties | Dependances | Artefacts couverts | Statut M0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Generation STATUS | `tools/generate_status.py` | validation | `registers/`, `schemas/`, `_meta/known_gaps.md`, validateurs publics | `STATUS.md` | `tools/validate_orgs.py`, `validate_images.py`, `validate_chronology.py`, `validate_concerts.py`, `validate_people.py`, `validate_places.py`, `validate_songs.py`, `validate_quotes.py` | `STATUS.md` | Producteur direct de `STATUS.md`. |
| Build canonique | `tools/build_all.py` | build | `sources/`, `registers/`, exports existants selon etapes | `exports/generated/`, `chapters/*/document_maitre.md`, `chapters/master_docs.json`, `registers/relations/attribution_edges.json` | `build_registers.py`, `build_attribution_edges.py`, `build_master_docs.py`, `build_edges.py`, `audit_repo.py` | Pipeline registres / documents maitres / exports / audits | Controle global ; ne genere pas directement `STATUS.md` dans le code observe. |
| Build registres | `tools/build_registers.py` | generation | `sources/`, `registers/`, `data/registre.json` | Exports JSON/CSV, diagnostics | Parser documentaire et schemas | `exports/generated/*.json`, `*.csv`, diagnostics | Actif. |
| Build attributions | `tools/build_attribution_edges.py` | generation | Citations, personnes, arbitrages internes | `registers/relations/attribution_edges.json`, `exports/generated/attribution_edges.json` | Registres people et quotes | Attributions citation -> personne | Actif. |
| Build documents maitres | `tools/build_master_docs.py` | generation | `exports/generated/atoms.json`, `quotes.json`, registres/exports utiles | `chapters/*/document_maitre.md`, `chapters/master_docs.json`, `exports/generated/master_docs_index.json` | Corpus exporte | Documents maitres | Producteur technique actuel des documents maitres. |
| Build aretes | `tools/build_edges.py` | generation | `exports/generated/index_by_id.json`, documents maitres | `exports/generated/edges.json` | Exports et documents maitres | Aretes documentaires | Actif. |
| Audit repo | `tools/audit_repo.py` | audit | Exports generes et diagnostics | `exports/generated/audit_repo.*` | `exports/generated/` | Audit documentaire | Actif. |
| Sentinelle anti-drift | `tools/check_generated_sync.py` | validation | Artefacts generes courants | Aucun en succes ; artefacts regeneres laisses en echec | `tools/build_all.py`, `tools/buildlib.py` | Registres, exports, documents maitres, audit repo | Controle M0 requis. |
| Recherche RAG | `tools/rag_search.py` | validation | `exports/generated/all_records.json` | Resultats de recherche stdout | Exports generes | Exploration corpus | Outil d'exploration, pas generateur DM. |
| Serveur RAG local | `tools/rag_server.py` | publication | `apps/`, exports, `chapters/` | Routes locales `/rag`, `/masters`, `/api/*` | `tools/rag_search.py` | Interface locale | Actif localement. |
| Workflow CI sentinelle | `.github/workflows/check-generated-sync.yml` | validation | Pull requests et push main | Job GitHub Actions | Python, requirements, `check_generated_sync.py`, `build_all.py`, validateurs | Artefacts generes et validateurs publics | Actif en CI. |
| Publication statique | `index.html`, `apps/` | publication | Exports generes, registres JSON/Markdown | Interface GitHub Pages / locale | GitHub Pages, cache navigateur, apps JS | Applications publiques | Existant, sans refonte M0. |
| Sync documents maitres | `tools/sync_dm_to_claude_kb.py` | publication | `chapters/*/document_maitre.md`, `chapters/master_docs.json` | Base de connaissance externe | Repo prive cible optionnel | Documents maitres exportes hors repo public | A cartographier ; non verifie par controles M0. |

## Table de rattachement initiale

| Composant | Chemin | Groupe roadmap | Pathspec minimal | Statut | Commentaire |
| --- | --- | --- | --- | --- | --- |
| Registres canoniques | `registers/` | registres | `registers/` | Disponible | Couvre canons publics, transversaux, relations et registres specialises. |
| Sources et atomes | `sources/`, `data/registre.json` | registres | `sources/`, `data/registre.json` | Disponible | Socle documentaire d'entree du build. |
| Exports generes | `exports/generated/` | exports generes | `exports/generated/` | Disponible | Couverts par sentinelle sauf fichiers explicitement redactionnels comme README. |
| Documents maitres par chapitre | `chapters/*/document_maitre.md` | documents maitres | `chapters/*/document_maitre.md` | Disponible | 14 vues persistantes. |
| Manifest documents maitres | `chapters/master_docs.json` | manifest | `chapters/master_docs.json` | Disponible | Produit par `tools/build_master_docs.py`. |
| Index documents maitres | `exports/generated/master_docs_index.json` | exports generes | `exports/generated/master_docs_index.json` | Disponible | Produit par `tools/build_master_docs.py`. |
| Applications statiques | `apps/`, `index.html` | applications | `apps/`, `index.html` | Disponible | Consultation et exploration, pas refonte. |
| RAG Studio | `apps/rag-studio/` | applications | `apps/rag-studio/` | Disponible | Exploration du corpus. |
| manuscript-studio | Aucun chemin local verifie | applications | Non applicable | Non verifie | Cite par la roadmap ; absence locale a noter. |
| Audits generes | `exports/generated/audit_repo.*`, `diagnostics.*` | audits | `exports/generated/audit_repo.*`, `exports/generated/diagnostics.*` | Disponible | Produits par build/audit. |
| Audits redactionnels | `docs/audits/`, `docs/canon/` | audits | `docs/audits/`, `docs/canon/` | Disponible | Notes d'audit et canonisation existantes. |
| Scripts build | `tools/build_all.py`, `tools/build_registers.py`, `tools/build_master_docs.py`, `tools/build_edges.py` | scripts | `tools/build_all.py`, `tools/build_registers.py`, `tools/build_master_docs.py`, `tools/build_edges.py` | Disponible | Pipeline documentaire canonique. |
| Scripts validation | `tools/validate_*.py`, `tools/check_generated_sync.py`, `tools/generate_status.py` | scripts | `tools/validate_*.py`, `tools/check_generated_sync.py`, `tools/generate_status.py` | Disponible | Validations et statut. |
| Workflow CI | `.github/workflows/check-generated-sync.yml` | scripts | `.github/workflows/check-generated-sync.yml` | Disponible | Controle PR/push main. |

## Limites connues

- Le chemin `manuscript-studio` n'est pas present dans le depot observe au 2026-06-05.
- `exports/generated/README.md` ne reflete pas completement le fait que de nombreux exports generes sont suivis par Git et couverts par la sentinelle.
- Les volumes canoniques de `STATUS.md` et les volumes exportes different pour certains registres, car ils ne mesurent pas toujours le meme perimetre.
- Les diagnostics generes indiquent 28870 warnings et 1404 blocs inconnus ; M0 les inventorie sans les resoudre.
- Les documents maitres restent exposes au risque d'obsolescence tant que la tracabilite vers sources, atomes, registres et exports n'est pas outillee.
- La publication GitHub Pages peut etre affectee par le cache navigateur/CDN.

## Anomalies

- Aucune anomalie bloquante nouvelle n'est introduite par cette note.
- L'ecart documentaire du README des exports est signale comme anomalie de documentation potentielle, sans correction dans cette PR.
- Les warnings et unknown existants sont des anomalies ou dettes documentaires deja visibles dans les artefacts d'audit ; ils ne sont pas traites dans M0 par cette PR.

## Sujets reportes

- Fiabilisation approfondie de la tracabilite des documents maitres vers sources, atomes, registres et exports.
- Qualification exhaustive des livrables RAG conserves.
- Clarification fonctionnelle de `manuscript-studio` si un chemin ou repo cible est fourni.
- Traitement des droits, provenance et publication multimedia.
- Refonte eventuelle des interfaces de consultation.
- Formulaires d'ajout documentaire.

## Chantiers interdits a ce stade

- Ouvrir M2 ou creer un studio d'enrichissement documentaire.
- Creer un nouveau script de controle dans cette PR.
- Modifier la roadmap strategique.
- Corriger manuellement des artefacts generes.
- Presenter les documents maitres comme sources ou preuves.
- Presenter le RAG comme producteur technique des documents maitres.
- Presenter `tools/build_all.py` comme generateur direct de `STATUS.md` : le code observe ne montre pas d'appel a `tools/generate_status.py`.
- Lancer une refonte d'interface ou de publication.

## Critères de sortie M0 — état actuel

| Critere | Statut | Preuve ou fichier concerne | Action restante |
| --- | --- | --- | --- |
| `STATUS.md` se regenere sans erreur via `tools/generate_status.py`. | rempli | `STATUS.md`, controle local `python3 tools/generate_status.py` | Snapshot regenere a inclure dans la PR. |
| Artefacts generes couverts par la sentinelle. | rempli | `tools/check_generated_sync.py`, `exports/generated/`, `chapters/*/document_maitre.md`, `chapters/master_docs.json` | Verifier le check CI apres ouverture de PR. |
| `build_all.py` reste controle global et n'est pas presente comme generateur direct de `STATUS.md`. | rempli | `tools/build_all.py`, `tools/generate_status.py`, controle local `python3 tools/build_all.py` | Maintenir cette distinction dans les docs et PR. |
| `check_generated_sync` est au vert sur la derniere PR. | partiel | Controle local `python3 tools/check_generated_sync.py` ; workflow `.github/workflows/check-generated-sync.yml` | Verifier le statut GitHub Actions de cette PR apres creation. |
| Inventaire des applications existantes disponible et date. | rempli | Section "Etat date des applications existantes" | Mettre a jour si nouvelle app ou chemin Manuscript. |
| Inventaire des registres canoniques disponible avec volumetrie. | rempli | Section "Etat date des registres canoniques", `STATUS.md`, `exports/generated/*.json` | Clarifier les ecarts canon/export si necessaire. |
| Table des dependances build / validation / publication disponible. | rempli | Section "Table des dependances build / validation / publication" | Completer si nouveau workflow. |
| Table de rattachement initiale renseignee. | rempli | Section "Table de rattachement initiale" | Completer si nouveaux groupes roadmap. |
| Limites connues distinguees des anomalies. | rempli | Sections "Limites connues" et "Anomalies" | Maintenir la separation dans les PR suivantes. |
| Aucun chantier M2 lance. | rempli | Cette note ; absence de script nouveau ; absence de modification roadmap | Continuer a bloquer formulaires/refontes jusqu'a cloture M0/M1. |
