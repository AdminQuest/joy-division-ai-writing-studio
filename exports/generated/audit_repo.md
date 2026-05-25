# Audit du repo documentaire

Généré le : `2026-05-25T15:40:05`

## 1. Verdict

Le repo n’est pas strict-compliant : 14 erreur(s) bloquante(s) subsistent.
La dette principale reste la migration v2 : 2432 atome(s) incomplet(s) sur 2505.

## 2. Synthèse chiffrée

- Enregistrements : 6448
- Erreurs : 14
- Avertissements : 27855
- Sources déclarées : 73
- Sources utilisées : 60
- Sources exportées : 60
- Sources utilisées absentes du registre : 1
- Libellés faibles : 1

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 2505 |
| chronology | 429 |
| concept | 392 |
| metadata | 203 |
| motif | 389 |
| myth | 100 |
| person | 289 |
| quote | 507 |
| quote_batch | 1 |
| rules | 1 |
| song | 110 |
| source | 99 |
| template | 357 |
| unknown | 1066 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| duplicate_id | 13 |
| field_type_error | 474 |
| invalid_controlled_value | 2414 |
| missing_required_field | 8443 |
| schema_warning | 527 |
| unknown_yaml_block | 1036 |
| v2_migration_debt | 14961 |
| yaml_parse_error | 1 |

## 5. Erreurs bloquantes

- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-007] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_warsaw_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-008] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_warsaw_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-009] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-010] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-011] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-012] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-013] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` [R-S79-014] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_foreword_deborah_v2.md` [R-S79-005] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_warsaw_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `sources/curtis_savage_so_this_is_permanence/relations_s79_foreword_deborah_v2.md` [R-S79-006] : Duplicate id also found in sources/curtis_savage_so_this_is_permanence/relations_s79_warsaw_v2.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/motifs/master_motifs.md` [MOTIF-009] : Duplicate id also found in registers/motifs/s45_curtis_motifs_vote_conservateur.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/motifs/master_motifs.md` [MOTIF-010] : Duplicate id also found in registers/motifs/s45_curtis_motifs_vote_conservateur.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/concepts/master_concepts.md` [CONCEPT-010] : Duplicate id also found in registers/concepts/s45_curtis_concepts_vote_conservateur.md → Renommer ou fusionner l’identifiant en doublon.
- **yaml_parse_error** — `registers/concepts/master_concepts.md` : YAML parse error: while scanning a simple key
  in "<unicode string>", line 45, column 5:
        sa formation était simplement no ... 
        ^
could not find expected ':'
  in "<unicode string>", line 47, column 1:
    atomes_lies:
    ^ → Corriger la syntaxe YAML du bloc concerné.

## 6. Blocs YAML non classés

- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_specialises_s27.md` : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-001] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-002] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-003] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-004] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-005] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-006] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-007] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/relations_stabilisees.md` [REL-S27-008] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_structurants_s27.md` [REF-S27-001] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_structurants_s27.md` [REF-S27-002] : Unable to infer documentary kind
- `sources/riom_review_crossley_networks/registres_structurants_s27.md` [REF-S27-003] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/dm_rag_update_s50.md` [DM-RAG-S50] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-001] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-002] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-003] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-004] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-005] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-006] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-007] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-008] : Unable to infer documentary kind
- `sources/bertetti_morreale_reimmaginare_immaginario/relations_s50.md` [REL-S50-009] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-009] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-010] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-011] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-012] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-013] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_leaders_of_men_v2.md` [R-S79-014] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-037] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-038] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-039] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-040] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-041] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-042] : Unable to infer documentary kind
- `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_fin_v2.md` [R-S79-043] : Unable to infer documentary kind
- … 996 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Sources utilisées mais absentes de `data/registre.json` :
- REGISTRY

Sources déclarées mais non utilisées :
- S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013 — verifie
- S03 — Demographia, England Largest Cities, s.d. — a_consolider
- S04 — Kidd, Manchester: A History, 2006 — verifie
- S18 — Fédida, Manchester : L’éveil d’une scène musicale, 2021 — a_consolider
- S23 — Rochdale Alternative Press, infrastructure DIY, 1971–1981 — a_consolider
- S24 — Richard Boon / New Hormones, Spiral Scratch, 1977 — a_consolider
- S25 — Factory Records, philosophie d’indépendance, 1978–1992 — a_consolider
- S28 — Granada Television / Tony Wilson, So It Goes, 1976–1977 — a_consolider
- S30 — Frith, Sound Effects, 1981 — verifie
- S32 — Kraftwerk, Trans-Europe Express / Radio-Activity, 1975–1977 — a_consolider
- S33 — Can, Tago Mago, 1971 — a_consolider
- S36 — Crosthwaite, Trauma and Degeneration, 2016 — a_consolider
- S38 — Saville / Manchester United / adidas, Pulsebeat of Manchester, 2022–2024 — a_consolider
- S73 — Blue Orchids, référence historique à consolider, s.d. — référence historique déplacée depuis S41 ; à consolider

Libellés faibles :
- REGISTRY : Registre canonique interne — chansons Joy Division / Warsaw

## 8. Migration v2

- Atomes : 2505
- Atomes v2 complets : 73
- Atomes v2 incomplets : 2432
- Avertissements de champs v2 manquants : 14961

Cette dette ne doit pas être corrigée mécaniquement sans stratégie d’enrichissement documentaire. Elle relève d’une migration progressive des sources déjà atomisées.

## 9. Fichiers les plus chargés en problèmes

| Fichier | Problèmes |
|---|---:|
| sources/mike_west_joy_division/source_atomisation_02.md | 734 |
| sources/mike_west_joy_division/source_atomisation_03.md | 483 |
| sources/flowers/source.md | 432 |
| sources/mike_west_joy_division/source_atomisation_04.md | 417 |
| sources/mike_west_joy_division/source_atomisation_01.md | 417 |
| sources/hook/atomisation_02_transmission_1978.md | 406 |
| sources/johnson_morley_an_ideal_for_living/source_suite_06.md | 376 |
| sources/hook/source.md | 365 |
| sources/suatoni/source.md | 363 |
| sources/marco_broll/source.md | 351 |
| sources/johnson_morley_an_ideal_for_living/source_suite_05.md | 350 |
| sources/curtis_savage_so_this_is_permanence/atoms_dm_s79_handwritten_songs_v2.md | 348 |
| sources/johnson_morley_an_ideal_for_living/source_suite_03.md | 345 |
| sources/johnson_morley_an_ideal_for_living/source_suite_02.md | 340 |
| sources/sumner_chapter_and_verse/source_part_sumner_salford_formation_sound_v2.md | 336 |
| sources/johnson_morley_an_ideal_for_living/source.md | 320 |
| sources/reynolds_rip_it_up/second_pass_scenes_heritage.md | 288 |
| sources/reynolds_rip_it_up/source.md | 285 |
| sources/hook/atomisation_03_unknown_pleasures_1979.md | 284 |
| sources/flowers/second_pass_new_order_late_discography.md | 261 |

## 10. Commandes utiles

```bash
python3 tools/build_registers.py
python3 tools/audit_repo.py
python3 tools/audit_repo.py --fail-on-error
```
