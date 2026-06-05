# Navigation niveau 1 — Applications

Objectif : identifier les applications présentes et leurs dépendances.

## Applications trouvées dans `apps/`

| Application | Emplacement | Finalité | Public visé | Dépendances principales |
| --- | --- | --- | --- | --- |
| Registre chronologique | `apps/chronology-register/` | Consulter le registre chronologique. | Contributeur documentaire, agent IA. | `apps/lib/dynamic-registers.js`, `registers/chronology/`. |
| Registre concepts / motifs / mythes | `apps/concept-register/` | Explorer concepts, motifs, mythes et liens documentaires. | Contributeur documentaire, rédacteur, agent IA. | `exports/generated/concepts.json`, `exports/generated/motifs.json`, `exports/generated/myths.json`, `exports/generated/atoms.json`, `exports/generated/quotes.json`, `exports/generated/sources.json`, `exports/generated/edges.json`, `exports/generated/index_by_id.json`. |
| Registre des concerts | `apps/concerts-register/` | Consulter concerts canoniques, statuts, lieux et liens. | Contributeur documentaire, vérification factuelle. | `exports/generated/concerts.json`, `exports/generated/places.json`, `exports/generated/edges.json`, `exports/generated/index_by_id.json`. |
| Registre iconographique | `apps/images-register/` | Consulter images et séances iconographiques. | Contributeur documentaire, contrôle iconographique. | `registers/images/images.json`. |
| Registre des organisations | `apps/organizations-register/` | Consulter organisations canoniques. | Contributeur documentaire. | `registers/orgs/orgs.json`. |
| Registre des acteurs | `apps/people-register/` | Consulter personnes canoniques, aliases, catégories et citations attribuées. | Contributeur documentaire, agent IA. | `apps/lib/dynamic-registers.js`, `registers/people/`, `registers/relations/attribution_edges.json`. |
| Registre des lieux | `apps/places-register/` | Explorer lieux, cartes et relations avec concerts. | Contributeur documentaire, contrôle géographique. | `exports/generated/places.json`, `exports/generated/concerts.json`, `exports/generated/edges.json`, `exports/generated/index_by_id.json`, Leaflet CDN. |
| Registre des citations | `apps/quote-register/` | Consulter les citations depuis l'export généré. | Contributeur documentaire, rédaction, vérification. | `exports/generated/quotes.json`. |
| RAG Studio | `apps/rag-studio/` | Rechercher dans le corpus documentaire, filtrer, regrouper, préparer des prompts. | Rédacteur, agent IA, contributeur documentaire. | `exports/generated/all_records.json`, `exports/generated/source_records.json`, `data/registre.json`. |
| Registre des sessions | `apps/sessions-register/` | Consulter sessions, répétitions, démos, radio, studio, TV. | Contributeur documentaire, vérification musicale. | `exports/generated/sessions.json`, `exports/generated/sessions.csv`. |
| Registre des chansons | `apps/song-register/` | Consulter chansons canoniques et données de variantes. | Contributeur documentaire, rédaction musicale. | `apps/lib/dynamic-registers.js`, `registers/songs/`, `registers/`, `sources/`, `schemas/song.schema.json`, données de variantes externes configurées dans l'app. |
| Registre des sources | `apps/source-register/` | Explorer sources, atomes, citations et relations par source. | Agent IA, contributeur documentaire. | `exports/generated/sources.json`, `exports/generated/source_records.json`, `exports/generated/quotes.json`, `exports/generated/atoms.json`, `exports/generated/edges.json`, `exports/generated/index_by_id.json`. |

## Outils web locaux associés

| Outil | Emplacement | Rôle | Dépendances |
| --- | --- | --- | --- |
| Serveur RAG local | `tools/rag_server.py` | Sert le portail local, le RAG et les endpoints `/api/*`. | `tools/rag_search.py`, `exports/generated/all_records.json`, `chapters/`. |
| Moteur de recherche RAG | `tools/rag_search.py` | Recherche lexicale locale dans les exports. | `exports/generated/all_records.json`. |
| Portail racine | `index.html` | Point d'accès web statique principal. | `apps/`, `assets/`. |

## Quelle application utiliser pour...

| Besoin | Application |
| --- | --- |
| Chercher une source et ses enregistrements | `apps/source-register/` |
| Chercher une citation | `apps/quote-register/` |
| Chercher une personne | `apps/people-register/` |
| Chercher une organisation | `apps/organizations-register/` |
| Chercher un lieu ou une salle | `apps/places-register/` |
| Vérifier un concert | `apps/concerts-register/` |
| Vérifier une session ou répétition | `apps/sessions-register/` |
| Vérifier une chanson | `apps/song-register/` |
| Explorer concepts, motifs ou mythes | `apps/concept-register/` |
| Explorer la chronologie | `apps/chronology-register/` |
| Explorer images ou séances photo | `apps/images-register/` |
| Préparer une recherche documentaire transversale | `apps/rag-studio/` |
| Interroger le corpus via serveur local | `tools/rag_server.py` puis `http://127.0.0.1:8765/rag` |

## Limite de cette carte

Cette carte ne liste que les applications présentes dans `apps/`.

Les références legacy vers des applications absentes ne sont pas traitées ici. Elles relèvent d'un futur audit de documentation ou de publication.
