# Audit du repo documentaire

Généré le : `2026-05-30T11:44:04`

## 1. Verdict

Le repo est techniquement exploitable, mais 1481 bloc(s) YAML ne sont pas classés.
La dette principale reste la migration v2 : 2497 atome(s) incomplet(s) sur 2737.

## 2. Synthèse chiffrée

- Enregistrements : 7611
- Erreurs : 0
- Avertissements : 29947
- Sources déclarées : 95
- Sources utilisées : 79
- Sources exportées : 79
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 2737 |
| chronology | 476 |
| concept | 456 |
| concert | 197 |
| metadata | 269 |
| motif | 424 |
| myth | 101 |
| person | 305 |
| quote | 556 |
| quote_batch | 1 |
| rules | 1 |
| session | 18 |
| song | 110 |
| source | 119 |
| template | 360 |
| unknown | 1481 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| field_type_error | 677 |
| invalid_controlled_value | 2668 |
| missing_required_field | 9281 |
| schema_warning | 497 |
| unknown_yaml_block | 1481 |
| v2_migration_debt | 15343 |

## 5. Erreurs bloquantes

Aucune.

## 6. Blocs YAML non classés

- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-001] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-002] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-003] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-004] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-005] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-006] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-007] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-008] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-009] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-010] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-011] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-012] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-013] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-014] : Unable to infer documentary kind
- `sources/allegri_living_in_the_ice_age/relations_s31.md` [REL-S31-015] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-001] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-002] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-003] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-004] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-005] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-006] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-007] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-008] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-009] : Unable to infer documentary kind
- `sources/amendola_troianiello_metropoli_spazio_periferico/relations_s42_metropoli_spazio_periferico_v2.md` [REL-S42-010] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-001] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-002] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-003] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-004] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-005] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-006] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-007] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-008] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-009] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-010] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-011] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-012] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-013] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-014] : Unable to infer documentary kind
- `sources/barone_directionless_so_plain_to_see/relations_s56.md` [REL-S56-015] : Unable to infer documentary kind
- … 1441 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Aucune source utilisée n’est absente de `data/registre.json`.

Sources déclarées mais non utilisées :
- REGISTRY-CONCERTS — joydiv.org/concerts.htm — reference_externe
- REGISTRY-SESSIONS — joydiv.org/sessions.htm — reference_externe
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

- Atomes : 2737
- Atomes v2 complets : 240
- Atomes v2 incomplets : 2497
- Avertissements de champs v2 manquants : 15343

Cette dette ne doit pas être corrigée mécaniquement sans stratégie d’enrichissement documentaire. Elle relève d’une migration progressive des sources déjà atomisées.

## 9. Fichiers les plus chargés en problèmes

| Fichier | Problèmes |
|---|---:|
| sources/mike_west_joy_division/source_atomisation_01.md | 417 |
| sources/mike_west_joy_division/source_atomisation_04.md | 417 |
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
| sources/morris_record_play_pause/source_part_06.md | 251 |
| sources/morris_record_play_pause/atomes_s35_record_play_pause.md | 240 |

## 10. Commandes utiles

```bash
python3 tools/build_registers.py
python3 tools/audit_repo.py
python3 tools/audit_repo.py --fail-on-error
```
