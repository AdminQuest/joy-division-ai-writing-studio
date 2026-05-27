# Audit du repo documentaire

Généré le : `2026-05-27T05:07:10`

## 1. Verdict

Le repo est techniquement exploitable, mais 1395 bloc(s) YAML ne sont pas classés.
La dette principale reste la migration v2 : 2574 atome(s) incomplet(s) sur 2719.

## 2. Synthèse chiffrée

- Enregistrements : 7307
- Erreurs : 0
- Avertissements : 30557
- Sources déclarées : 89
- Sources utilisées : 75
- Sources exportées : 75
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 2719 |
| chronology | 476 |
| concept | 456 |
| metadata | 264 |
| motif | 424 |
| myth | 101 |
| person | 305 |
| quote | 551 |
| quote_batch | 1 |
| rules | 1 |
| song | 110 |
| source | 114 |
| template | 360 |
| unknown | 1425 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| field_type_error | 665 |
| invalid_controlled_value | 2701 |
| missing_required_field | 9221 |
| schema_warning | 527 |
| unknown_yaml_block | 1395 |
| v2_migration_debt | 16048 |

## 5. Erreurs bloquantes

Aucune.

## 6. Blocs YAML non classés

- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-001] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-002] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-003] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-004] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-005] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-006] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-007] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-008] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-009] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-010] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-011] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-012] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-013] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-014] : Unable to infer documentary kind
- `sources/villani_ti_sfido_a_disperarti/relations_s57.md` [REL-S57-015] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-001] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-002] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-003] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-004] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-005] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-006] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-007] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-008] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-009] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-010] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-011] : Unable to infer documentary kind
- `sources/goddard_missions_dead_souls/relations_stabilisees.md` [REL-S29-012] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-001] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-002] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-003] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-004] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-005] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-006] : Unable to infer documentary kind
- `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` [R-S80-007] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-001] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-002] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-003] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-004] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-005] : Unable to infer documentary kind
- `sources/worley_punk_politics_british_fanzines/relations_s77.md` [REL-S77-006] : Unable to infer documentary kind
- … 1355 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Aucune source utilisée n’est absente de `data/registre.json`.

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

Aucun libellé faible.

## 8. Migration v2

- Atomes : 2719
- Atomes v2 complets : 145
- Atomes v2 incomplets : 2574
- Avertissements de champs v2 manquants : 16048

Cette dette ne doit pas être corrigée mécaniquement sans stratégie d’enrichissement documentaire. Elle relève d’une migration progressive des sources déjà atomisées.

## 9. Fichiers les plus chargés en problèmes

| Fichier | Problèmes |
|---|---:|
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
| sources/morley_piece_by_piece/atoms_dm_s37_part_one_remaining_v2.md | 275 |
| sources/flowers/second_pass_new_order_late_discography.md | 261 |

## 10. Commandes utiles

```bash
python3 tools/build_registers.py
python3 tools/audit_repo.py
python3 tools/audit_repo.py --fail-on-error
```
