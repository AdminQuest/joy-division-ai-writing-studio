# Navigation niveau 1 — Registres

Objectif : localiser rapidement le bon registre sans parcourir tout le dépôt.

## Registres validés dans `STATUS.md`

| Registre | Préfixe | Rôle | Emplacement | Dépendances principales | Utilisé par / liens |
| --- | --- | --- | --- | --- | --- |
| Acteurs | `PERSON-` | Stabiliser les personnes du corpus : membres du groupe, entourage, auteurs, journalistes, figures critiques. | `registers/people/` | `registers/people/00_canonical_people.md`, `registers/people/00_authors_canonical.md`, `registers/people/pending_org.json`, `registers/people/pending_concept.json`, `schemas/person_canonical.schema.json`, `tools/validate_people.py` | `exports/generated/people.json`, `apps/people-register/`, `registers/relations/attribution_edges.json`, citations, sources, organisations, concepts. |
| Organisations | `ORG-` | Stabiliser groupes, labels, institutions, médias, organisations et entités non-personnes. | `registers/orgs/` | `registers/orgs/orgs.json`, `schemas/organization_canonical.schema.json`, `tools/validate_orgs.py`, `registers/people/pending_org.json` | `apps/organizations-register/`, personnes, sources, lieux, images. |
| Images | `IMAGE-` | Stabiliser les images et séances iconographiques. | `registers/images/` | `registers/images/images.json`, `schemas/image_canonical.schema.json`, `tools/validate_images.py` | `apps/images-register/`, personnes, lieux, sessions, sources. |
| Chronologie | `EVENT-` ; legacy `CHR-` observé dans les exports | Stabiliser les événements datés et la chronologie documentaire. | `registers/chronology/` | `registers/chronology/events_canonical.md`, `registers/chronology/master_chronology.md`, `tools/validate_chronology.py` | `exports/generated/chronology.json`, `apps/chronology-register/`, concerts, sessions, lieux, personnes, sources. |
| Concerts | `CONCERT-` ; legacy `JD-CONCERT-` | Stabiliser les concerts Joy Division / Warsaw, dates, statuts et lieux. | `registers/concerts/` | `registers/concerts/00_canonical_concerts.md`, `registers/concerts/concert_canonical_units.md`, `schemas/concert_v1.yaml`, `tools/validate_concerts.py` | `exports/generated/concerts.json`, `apps/concerts-register/`, lieux, chronologie, chansons, sources. |
| Lieux | `PLACE-` | Stabiliser les lieux géographiques et lieux de concert, studio, ville, salle. | `registers/places/` | `schemas/places.schema.yaml`, `tools/validate_places.py`, blocs YAML `places:` sous `registers/**/*.md` | `exports/generated/places.json`, `apps/places-register/`, concerts, sessions, chronologie, images. |
| Chansons | `JD-SONG-` ; autres `SONG-` legacy observés | Stabiliser le canon des chansons Joy Division et les entrées liées. | `registers/songs/` | `registers/songs/00_canonical_joy_division_songs.md`, `schemas/song.schema.json`, `tools/validate_songs.py` | `exports/generated/songs.json`, `apps/song-register/`, concerts, sessions, citations, sources. |
| Citations | `QUOTE-` dans `STATUS.md` ; IDs source `SXX-QNNN` observés dans les exports | Centraliser les citations courtes et leurs attributions. | `registers/quotes/` et `registers/relations/attribution_edges.json` | `exports/generated/quotes.json`, `tools/validate_quotes.py`, `tools/build_attribution_edges.py`, `tools/validate_attribution.py` | `apps/quote-register/`, personnes, sources, graphe d'attribution, documents maîtres. |

## Registres transversaux générés ou exploités

| Registre | Préfixe | Rôle | Emplacement | Dépendances principales | Utilisé par / liens |
| --- | --- | --- | --- | --- | --- |
| Sources | `SXX` | Référencer les sources canoniques du corpus. | `data/registre.json` et `sources/` | `tools/build_registers.py`, `tools/atomize_new_sources.py`, scripts `tools/apply_s*_registre_patch.py` | `exports/generated/sources.json`, `exports/generated/source_records.json`, `apps/source-register/`, RAG Studio, atomes, citations. |
| Atomes | `SXX-ANNN` | Porter les unités documentaires extraites des sources. | `sources/` | Blocs YAML dans `sources/**/*.md`, `tools/build_registers.py`, schémas via `tools/schema_validation.py` | `exports/generated/atoms.json`, documents maîtres, RAG Studio, diagnostics, concepts, motifs, mythes. |
| Concepts | `CONCEPT-` | Stabiliser les concepts structurants. | `registers/concepts/` | `tools/build_registers.py`, blocs YAML `concept`, `exports/generated/concepts.json` | `apps/concept-register/`, atomes, citations, RAG Studio, prompt context. |
| Motifs | `MOTIF-` | Stabiliser les motifs récurrents. | `registers/motifs/` | `tools/build_registers.py`, blocs YAML `motif`, `exports/generated/motifs.json` | `apps/concept-register/`, atomes, documents maîtres, diagnostics. |
| Mythes | `MYTH-` | Stabiliser les mythes, lectures à déconstruire et constructions mémorielles. | `registers/myths/` | `tools/build_registers.py`, blocs YAML `myth`, `exports/generated/myths.json` | `apps/concept-register/`, diagnostics historiographiques, documents maîtres. |
| Références | Variable, souvent par source `SXX` | Regrouper références, relations RAG et compléments bibliographiques. | `registers/references/` | `tools/build_registers.py`, `data/registre.json`, sources atomisées | Sources, atomes, RAG Studio, audits. |
| Relations | Pas de préfixe unique | Porter les arêtes documentaires, notamment les attributions de citations. | `registers/relations/` | `registers/relations/attribution_edges.json`, `tools/build_edges.py`, `tools/build_attribution_edges.py`, `tools/validate_edges.py` | `exports/generated/edges.json`, `exports/generated/attribution_edges.json`, apps concerts/lieux/concepts/sources, graphe documentaire. |
| Sessions | `JD-SESSION-` | Stabiliser sessions, répétitions, démos, studio, radio et télévision. | `registers/sessions/` | `registers/sessions/joy_division_sessions_register_v1.md`, `schemas/session_v1.yaml` | `exports/generated/sessions.json`, `apps/sessions-register/`, lieux, chansons, chronologie, sources. |
| Spécialisés | Variable | Registres source-spécifiques ou thématiques non normalisés en un seul préfixe. | `registers/specialized/` et fichiers `registers/s*_*.md` | `tools/build_registers.py`, sources correspondantes | Exports générés, RAG Studio, diagnostics. |

## Je cherche ...

| Je cherche | Aller vers |
| --- | --- |
| Une personne, un auteur, un membre du groupe | `PERSON-` dans `registers/people/` |
| Une organisation, un label, un média, une institution | `ORG-` dans `registers/orgs/` |
| Une image ou une séance photo | `IMAGE-` dans `registers/images/` |
| Un événement daté | `EVENT-` / `CHR-` dans `registers/chronology/` |
| Un concert | `CONCERT-` / `JD-CONCERT-` dans `registers/concerts/` |
| Un lieu | `PLACE-` dans `registers/places/` |
| Une chanson | `JD-SONG-` dans `registers/songs/` |
| Une citation | `SXX-QNNN` / `QUOTE-` via `registers/quotes/` et `exports/generated/quotes.json` |
| Une source canonique | `SXX` dans `data/registre.json` |
| Un atome documentaire | `SXX-ANNN` dans `sources/` |
| Un concept | `CONCEPT-` dans `registers/concepts/` ou `exports/generated/concepts.json` |
| Un motif | `MOTIF-` dans `registers/motifs/` ou `exports/generated/motifs.json` |
| Un mythe | `MYTH-` dans `registers/myths/` ou `exports/generated/myths.json` |
| Une relation citation → personne | `registers/relations/attribution_edges.json` |
| Une session studio, radio, répétition ou TV | `JD-SESSION-` dans `registers/sessions/` |
