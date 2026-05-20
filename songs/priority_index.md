# Songbook — index des dossiers prioritaires

```yaml
type_unite: songbook_priority_index
status: "étape 4 réalisée"
seed_file: "data/songbook_priority_seed_v1.json"
last_update: "2026-05-20"
```

## Fonction

Cet index amorce l’étape 4 du Songbook critique : remplir progressivement, chanson par chanson, les dossiers prioritaires avant enrichissement externe massif.

La passe ne renseigne pas encore les paroles complètes, les setlists, les bootlegs ou les sessions de façon définitive. Elle fixe les axes de travail, les sources internes à mobiliser, les sources externes à vérifier et les tâches par sous-dossier.

## Dossiers prioritaires amorcés

| Priorité | Titre | Dossier | Fonction documentaire |
|---:|---|---|---|
| 1 | Transmission | `songs/transmission/priority_notes.md` | Single, transmission collective, versions studio/live/Peel-BBC à distinguer. |
| 2 | Shadowplay | `songs/shadowplay/priority_notes.md` | Seuil spatial, Manchester, image télévisuelle, performance Granada à vérifier. |
| 3 | She’s Lost Control | `songs/shes-lost-control/priority_notes.md` | Contrôle, épilepsie, corps, versions album/single/live à distinguer. |
| 4 | Atmosphere | `songs/atmosphere/priority_notes.md` | Sordide Sentimental, alias `Chance`, mémoire posthume et réemploi. |
| 5 | Love Will Tear Us Apart | `songs/love-will-tear-us-apart/priority_notes.md` | Single posthume, versions Pennine/Strawberry, prudence biographique. |
| 6 | Digital | `songs/digital/priority_notes.md` | Factory Sample, dernier titre joué à vérifier, motif digital/fade away. |
| 7 | Dead Souls | `songs/dead-souls/priority_notes.md` | Sordide Sentimental, hantise, reprises à distinguer du canon. |
| 8 | Decades | `songs/decades/priority_notes.md` | Clôture de *Closer*, temporalité générationnelle, mémoire et fin. |
| 9 | Atrocity Exhibition | `songs/atrocity-exhibition/priority_notes.md` | Ouverture de *Closer*, Ballard, spectacle de la catastrophe. |
| 10 | Disorder | `songs/disorder/priority_notes.md` | Ouverture d’*Unknown Pleasures*, son Hannett, tension sensorielle. |

## Règles pour la suite

1. Remplir d’abord `source_notes.md` avec les sources internes atomisées.
2. Alimenter ensuite `sessions.md`, `releases.md` et `live_occurrences.md` à partir des sources vérifiées.
3. Ne renseigner `lyrics.md` qu’avec une source de paroles identifiée.
4. Ne renseigner `bootlegs.md` qu’après rattachement à un événement live ou à une source discographique fiable.
5. Ne jamais créer une nouvelle chanson pour une variante : rattacher la variante au titre canonique.
