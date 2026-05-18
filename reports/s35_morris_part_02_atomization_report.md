# Rapport d’atomisation — S35 part 02 — Morris, *Record Play Pause*, 2019

```yaml
id: REPORT-S35-PART-02
source_id: S35
source_part: S35-PART-02
source_label: "S35 — Morris, Record Play Pause, 2019"
type_unite: rapport_atomisation
statut: integre
passage_atomise: "PDF p. 24-50"
```

## 1. Périmètre

Deuxième passe sélective sur Stephen Morris, *Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I*, Constable, 2019, PDF p. 24-50.

Le passage couvre la fin de « Batteries Not Included », « Home and Abroad » et le début de « The Swinging Sixties ».

## 2. Fichiers ajoutés

```text
sources/morris_record_play_pause/source_part_02.md
sources/morris_record_play_pause/relations_stabilisees_part_02.md
sources/morris_record_play_pause/registres_specialises_s35_part_02.md
chapters/01/s35_morris_part_02_complement.md
chapters/02/s35_morris_part_02_complement.md
chapters/03/s35_morris_part_02_complement.md
chapters/05/s35_morris_part_02_complement.md
chapters/11/s35_morris_part_02_complement.md
chapters/12/s35_morris_part_02_complement.md
chapters/14/s35_morris_part_02_complement.md
master_docs/s35_morris_record_play_pause_part_02_master.md
rag/fragments/s35_morris_record_play_pause_part_02.jsonl
reports/s35_morris_part_02_atomization_report.md
```

## 3. Atomes ajoutés

```text
S35-A021 à S35-A032
```

## 4. Relations ajoutées

```text
REL-S35-013 à REL-S35-018
```

## 5. Vérification de la première passe

La première passe S35 est déjà présente et intégrée dans les couches suivantes :

```text
sources/morris_record_play_pause/source.md
sources/morris_record_play_pause/atomes_s35_record_play_pause.md
sources/morris_record_play_pause/relations_stabilisees.md
sources/morris_record_play_pause/registres_specialises_s35.md
sources/morris_record_play_pause/registre_patch_s35.json
registers/references/s35_morris_record_play_pause_source_canonique.md
rag/fragments/s35_morris_record_play_pause.jsonl
chapters/01/s35_morris_complement.md
chapters/02/s35_morris_complement.md
chapters/03/s35_morris_complement.md
chapters/04/s35_morris_complement.md
chapters/05/s35_morris_complement.md
chapters/06/s35_morris_complement.md
chapters/12/s35_morris_complement.md
chapters/14/s35_morris_complement.md
master_docs/s35_morris_record_play_pause_master.md
```

## 6. Statut RAG

Un fragment RAG dédié à la deuxième passe a été créé :

```text
rag/fragments/s35_morris_record_play_pause_part_02.jsonl
```

Les exports générés dans `exports/generated/` doivent être régénérés localement par `tools/build_registers.py --strict`, puis ajoutés avec `git add -f` selon le workflow du README.

## 7. Contrôles recommandés

```bash
grep -R "S35-A021" -n sources registers chapters master_docs rag reports | head -50
grep -R "S35-A032" -n sources registers chapters master_docs rag reports | head -50
grep -R "REL-S35-018" -n sources registers chapters master_docs rag reports | head -50
grep -R "S35-PART-02" -n sources registers chapters master_docs rag reports | head -50
grep -R "The Locomotion" -n sources registers chapters master_docs rag reports | head -50
grep -R "Ballroom dancing" -n sources registers chapters master_docs rag reports | head -50
```
