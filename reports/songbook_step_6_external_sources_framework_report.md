# Rapport — Songbook Joy Division — Étape 6

```yaml
type_unite: generation_report
scope: "Songbook critique chanson par chanson"
status: "step_6_external_sources_framework_created"
external_sources_registry: "data/songbook_external_sources_registry.json"
external_evidence_schema: "schemas/song_external_evidence.schema.yaml"
external_evidence_tool: "tools/seed_songbook_external_evidence.py"
last_update: "2026-05-20"
```

## 1. Préalable

L’étape 5 a créé l’outil d’enrichissement interne mais doit encore être matérialisée localement par :

```bash
python3 tools/enrich_songbook_from_internal_sources.py
```

L’étape 6 est donc créée comme cadre de travail externe, sans consolidation de données externes dans les dossiers chanson.

## 2. Objet de l’étape 6

L’étape 6 prépare l’intégration des sources externes : sites spécialisés, bases discographiques, sources officielles, livrets, sources de paroles, BBC/Peel, bootlegs et collection personnelle.

Elle ne remplace pas les sources internes atomisées. Elle ajoute une couche de preuves externes qualifiées.

## 3. Registre des sources externes

```text
data/songbook_external_sources_registry.json
```

Ce registre classe les sources selon leur fonction et leur niveau de confiance :

- A : source officielle, livret, archive institutionnelle ;
- B : site spécialisé ou base discographique robuste, à recouper ;
- C : source fan, bootleg, collection personnelle, à vérifier ;
- D : indice faible.

Sources préparées :

```text
EXT-JOYDIV-ORG
EXT-JOYD-SONGS-EPIZY
EXT-DISCOGS-JD
EXT-JD-OFFICIAL
EXT-BBC-PEEL
EXT-OFFICIAL-BOOKLETS
EXT-LYRICS-BOOK
EXT-PERSONAL-BOOTLEGS
```

## 4. Schéma de preuve externe

```text
schemas/song_external_evidence.schema.yaml
```

Le schéma impose :

- un identifiant de preuve ;
- un `song_id` ;
- un titre canonique ;
- une source externe ;
- un type de preuve ;
- une URL ou source physique ;
- une date de consultation ;
- une donnée extraite courte et paraphrasée ;
- un fichier cible ;
- un niveau de confiance ;
- un statut de vérification.

## 5. Outil de préparation

```text
tools/seed_songbook_external_evidence.py
```

L’outil crée, pour les dix dossiers prioritaires :

```text
songs/<slug>/external_evidence.md
```

Il crée également :

```text
data/songbook_external_evidence_index.json
```

## 6. Commande de matérialisation

```bash
python3 tools/seed_songbook_external_evidence.py
```

Commande forcée si les fichiers existent déjà :

```bash
python3 tools/seed_songbook_external_evidence.py --force
```

## 7. Prudences

Aucune donnée externe n’est consolidée automatiquement à ce stade.

Les paroles complètes ne doivent pas être importées depuis internet.

Les données issues de joydiv.org ou de Discogs doivent être recoupées avant intégration définitive.

Les bootlegs de la collection personnelle doivent être rattachés à un fichier source, à une date ou à un événement live quand c’est possible.
