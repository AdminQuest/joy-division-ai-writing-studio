# Rapport — Songbook Joy Division — Étape 5

```yaml
type_unite: generation_report
scope: "Songbook critique chanson par chanson"
status: "step_5_internal_sources_enrichment_ready"
seed_file: "data/songbook_priority_seed_v1.json"
enrichment_tool: "tools/enrich_songbook_from_internal_sources.py"
output_index: "data/songbook_internal_sources_index.json"
last_update: "2026-05-20"
```

## 1. Objet de l’étape 5

L’étape 5 consiste à enrichir les dix dossiers chanson prioritaires à partir des sources internes déjà atomisées et des registres générés.

Elle intervient avant l’enrichissement externe par `joydiv.org`, Discogs, livrets officiels, bases BBC/Peel ou collections personnelles.

## 2. Outil créé

```text
tools/enrich_songbook_from_internal_sources.py
```

L’outil lit :

```text
data/songbook_priority_seed_v1.json
registers/songs/00_canonical_joy_division_songs.md
exports/generated/songs.json
```

Puis il met à jour, pour les dix dossiers prioritaires :

```text
songs/<slug>/source_notes.md
```

Il écrit également :

```text
data/songbook_internal_sources_index.json
```

## 3. Dossiers concernés

```text
songs/transmission/source_notes.md
songs/shadowplay/source_notes.md
songs/shes-lost-control/source_notes.md
songs/atmosphere/source_notes.md
songs/love-will-tear-us-apart/source_notes.md
songs/digital/source_notes.md
songs/dead-souls/source_notes.md
songs/decades/source_notes.md
songs/atrocity-exhibition/source_notes.md
songs/disorder/source_notes.md
```

## 4. Méthode

L’outil rattache les mentions internes par titre canonique et alias déclarés dans le canon.

Il extrait, pour chaque mention interne :

- identifiant de record ;
- fichier source ;
- source canonique ;
- titre tel qu’il apparaît dans le record ;
- chapitres ;
- usage ;
- thèmes ;
- mots-clés ;
- atomes liés ;
- citations liées.

## 5. Limite assumée

L’étape 5 reste interne au repo. Elle ne va pas chercher de données sur internet.

Elle prépare les dossiers à recevoir les données externes, mais ne les consolide pas encore.

## 6. Commande de matérialisation

```bash
python3 tools/enrich_songbook_from_internal_sources.py
```

Commande de contrôle sans écriture :

```bash
python3 tools/enrich_songbook_from_internal_sources.py --dry-run
```

## 7. Prudences

Le rattachement automatique par titre ou alias est un amorçage. Chaque information reste à vérifier avant usage éditorial définitif.

Les titres homonymes, les reprises, les mentions contextuelles et les variantes doivent être contrôlés manuellement.

Les paroles complètes ne sont pas générées ni injectées par cette étape.
