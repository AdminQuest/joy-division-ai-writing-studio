# Rapport d’atomisation — S35 part 04 — Morris, *Record Play Pause*, 2019

```yaml
id: REPORT-S35-PART-04
source_id: S35
source_part: S35-PART-04
source_label: "S35 — Morris, Record Play Pause, 2019"
type_unite: rapport_atomisation
statut: integre
passage_atomise: "PDF p. 75-102"
```

## 1. Périmètre

Quatrième passe sélective sur Stephen Morris, *Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I*, Constable, 2019, PDF p. 75-102.

Le passage couvre la fin du chapitre 5 (« Little Drummer Boy »), le chapitre 6 (« Isolation ») et le chapitre 7 (« The Great Vinyl Robbery »), jusqu’à la formule de clôture « I wanted to break out ».

## 2. Fichiers ajoutés

```text
sources/morris_record_play_pause/source_part_04.md
sources/morris_record_play_pause/relations_stabilisees_part_04.md
sources/morris_record_play_pause/registres_specialises_s35_part_04.md
registers/concepts/s35_morris_concepts_part_04.md
registers/motifs/s35_morris_motifs_part_04.md
registers/myths/s35_morris_mythes_part_04.md
registers/references/s35_morris_record_play_pause_part_04_reference_supplement.md
registers/quotes/s35_morris_quotes_part_04.md
registers/chronology/s35_morris_chronology_part_04.md
registers/people/s35_morris_people_part_04.md
registers/places/s35_morris_places_part_04.md
registers/organizations/s35_morris_organizations_part_04.md
registers/songs/s35_morris_songs_part_04.md
chapters/01/s35_morris_part_04_complement.md
chapters/02/s35_morris_part_04_complement.md
chapters/03/s35_morris_part_04_complement.md
chapters/08/s35_morris_part_04_complement.md
chapters/10/s35_morris_part_04_complement.md
chapters/12/s35_morris_part_04_complement.md
chapters/13/s35_morris_part_04_complement.md
chapters/14/s35_morris_part_04_complement.md
master_docs/s35_morris_record_play_pause_part_04_master.md
rag/fragments/s35_morris_record_play_pause_part_04.jsonl
reports/s35_morris_part_04_atomization_report.md
```

## 3. Atomes ajoutés

```text
S35-A048 à S35-A065
```

## 4. Relations ajoutées

```text
REL-S35-029 à REL-S35-040
```

## 5. Registres ajoutés

Compléments ajoutés aux registres structurants : concepts, motifs, mythes, références.

Compléments ajoutés aux registres spécialisés : citations candidates, chronologie, acteurs, lieux, organisations, chansons / albums.

## 6. Documents maîtres et RAG

Notes de chapitre ajoutées : chapitres 1, 2, 3, 8, 10, 12, 13 et 14.

Document maître source ajouté :

```text
master_docs/s35_morris_record_play_pause_part_04_master.md
```

Fragment RAG ajouté :

```text
rag/fragments/s35_morris_record_play_pause_part_04.jsonl
```

## 7. Thèse de la passe

Cette passe montre que Morris ne passe pas linéairement de l’école à Joy Division. Elle stabilise une zone d’apprentissage négatif : drogues adolescentes, exclusion scolaire, Manchester comme école parallèle, travail textile, culture vinyle, bootlegs, concerts pré-punk, festivals désenchantés, petite criminalité, Macclesfield comme espace à quitter.

Trois axes deviennent particulièrement forts :

1. La batterie de Morris se construit contre la démonstration virtuose, dans une morale anti-solo nourrie par Jaki Liebezeit, Moe Tucker, Can, Neu!, Kraftwerk et Captain Beefheart.
2. Le disque apparaît comme chasse matérielle : imports américains, Rare Records, Black Sedan, bootlegs, Discogs, pressages, rareté, promesse et déception.
3. La fuite adolescente est désacralisée : elle passe par le blackout, la commune pauvre, le vol de disques, l’arrestation et le désir de rupture.

## 8. Contrôles grep recommandés

```bash
grep -R "S35-PART-04" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "S35-A048" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "S35-A065" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "REL-S35-040" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Atwell and Jenner" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Black Sedan" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Great Vinyl Robbery" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Discogs" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Jaki Liebezeit" -n data sources registers chapters master_docs rag reports exports | head -50
grep -R "Manchester comme école parallèle" -n data sources registers chapters master_docs rag reports exports | head -50
```
