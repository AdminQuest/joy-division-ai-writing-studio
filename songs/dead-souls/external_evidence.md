# Dead Souls — Preuves externes à intégrer

```yaml
id: JD-SONG-033-EXTERNAL-EVIDENCE
song_id: JD-SONG-033
type_unite: song_external_evidence_file
canonical_song: "Dead Souls"
slug: "dead-souls"
status: "external evidence container created ; no external facts consolidated yet"
last_update: "2026-05-20"
registry: "data/songbook_external_sources_registry.json"
schema: "schemas/song_external_evidence.schema.yaml"
```

## 1. Sources externes à vérifier pour ce titre

```yaml
preferred_external_sources: 
  - "joydiv.org"
  - "discogs"
  - "Sordide Sentimental references"
```

## 2. Sources externes disponibles dans le registre

```yaml
registered_external_sources: 
  - "EXT-JOYDIV-ORG"
  - "EXT-JOYD-SONGS-EPIZY"
  - "EXT-DISCOGS-JD"
  - "EXT-JD-OFFICIAL"
  - "EXT-BBC-PEEL"
  - "EXT-OFFICIAL-BOOKLETS"
  - "EXT-LYRICS-BOOK"
  - "EXT-PERSONAL-BOOTLEGS"
```

## 3. Preuves externes collectées

```yaml
external_evidence: []
```

## 4. Données en attente par type

```yaml
pending_external_tasks:
  lyrics: "source imprimée ou officielle à vérifier ; ne pas importer automatiquement depuis internet"
  sessions: "vérifier joydiv.org, livrets officiels, BBC/Peel et sources discographiques"
  releases: "vérifier Discogs puis recouper avec livrets officiels"
  live_occurrences: "vérifier joydiv.org et setlists spécialisées avant consolidation"
  bootlegs: "rattacher à la collection personnelle, à Discogs et à un concert si possible"
```

## 5. Prudence

Aucune donnée externe n’est consolidée dans ce fichier tant qu’elle n’a pas reçu un `evidence_id`, une source, une date de consultation, un type de preuve et un statut de vérification.
