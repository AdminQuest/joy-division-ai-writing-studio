# Audit du repo documentaire

Généré le : `2026-05-16T19:34:55`

## 1. Verdict

Le repo est techniquement exploitable, mais 285 bloc(s) YAML ne sont pas classés.
La dette principale reste la migration v2 : 1754 atome(s) incomplet(s) sur 1815.

## 2. Synthèse chiffrée

- Enregistrements : 3972
- Erreurs : 0
- Avertissements : 18843
- Sources déclarées : 51
- Sources utilisées : 25
- Sources exportées : 25
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 1815 |
| chronology | 343 |
| concept | 205 |
| metadata | 64 |
| motif | 280 |
| myth | 27 |
| person | 157 |
| quote | 358 |
| quote_batch | 1 |
| rules | 1 |
| song | 41 |
| source | 59 |
| template | 336 |
| unknown | 285 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| field_type_error | 149 |
| invalid_controlled_value | 1592 |
| missing_required_field | 5055 |
| schema_warning | 400 |
| unknown_yaml_block | 285 |
| v2_migration_debt | 11362 |

## 5. Erreurs bloquantes

Aucune.

## 6. Blocs YAML non classés

- `sources/tomeo_dance_dance_dance/source_part_interzone_rave_era.md` : Unable to infer documentary kind
- `sources/tomeo_dance_dance_dance/source_part_interzone_rave_era.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_structurants_s11.md` [REF-S11-001] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-001] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-002] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-003] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-004] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-005] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-006] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-007] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/relations_stabilisees.md` [REL-S11-008] : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/uk_treasury_fsbr_1987_88/registres_specialises_s11.md` : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [MYTHE-S15-001] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [MYTHE-S15-002] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [REF-S15-001] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [REF-S15-002] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [REF-S15-003] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_structurants_s15.md` [REF-S15-004] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-001] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-002] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-003] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-004] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-005] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-006] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-007] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-008] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-009] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/relations_stabilisees.md` [REL-S15-010] : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_specialises_s15.md` : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_specialises_s15.md` : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_specialises_s15.md` : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_specialises_s15.md` : Unable to infer documentary kind
- `sources/deluca_manchester_punk_threshold/registres_specialises_s15.md` : Unable to infer documentary kind
- `sources/cummins_joy_division_visual_corpus/relations_stabilisees.md` [REL-S09-001] : Unable to infer documentary kind
- `sources/cummins_joy_division_visual_corpus/relations_stabilisees.md` [REL-S09-002] : Unable to infer documentary kind
- … 245 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Aucune source utilisée n’est absente de `data/registre.json`.

Sources déclarées mais non utilisées :
- S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013 — verifie
- S03 — Demographia, England Largest Cities, s.d. — a_consolider
- S04 — Kidd, Manchester: A History, 2006 — verifie
- S07 — Engels, The Condition of the Working Class in England, 1845 — a_consolider
- S08 — Debord, psychogéographie et dérive, 1955–1958 — a_consolider
- S17 — The Fall, « Rowche Rumble », 1979 — a_consolider
- S18 — Fédida, Manchester : L’éveil d’une scène musicale, 2021 — a_consolider
- S19 — Bourdieu, Les trois états du capital culturel, 1979 — verifie
- S21 — City Fun, fanzine, 1978–1983 — a_consolider
- S23 — Rochdale Alternative Press, infrastructure DIY, 1971–1981 — a_consolider
- S24 — Richard Boon / New Hormones, Spiral Scratch, 1977 — a_consolider
- S25 — Factory Records, philosophie d’indépendance, 1978–1992 — a_consolider
- S26 — Butt, Post-Punk Then and Now, 2016 — verifie
- S27 — Crossley, Networks of Sound, Style and Subversion, 2015 — verifie
- S28 — Granada Television / Tony Wilson, So It Goes, 1976–1977 — a_consolider
- S29 — Goddard, Missions of Dead Souls, 2011 — verifie
- S30 — Frith, Sound Effects, 1981 — verifie
- S31 — Allegri, Living in the Ice Age, 2021 — a_consolider
- S32 — Kraftwerk, Trans-Europe Express / Radio-Activity, 1975–1977 — a_consolider
- S33 — Can, Tago Mago, 1971 — a_consolider
- S34 — Fraser & Fuoto, Manchester, 1976, 2012 — verifie
- S36 — Crosthwaite, Trauma and Degeneration, 2016 — a_consolider
- S38 — Saville / Manchester United / adidas, Pulsebeat of Manchester, 2022–2024 — a_consolider
- S39 — Bauman, Liquid Modernity / La vie liquide, 2000–2006 — verifie
- S40 — Cacciatore, Waiting for Something to Happen, 2019 — verifie
- S73 — Blue Orchids, référence historique à consolider, s.d. — référence historique déplacée depuis S41 ; à consolider

Aucun libellé faible.

## 8. Migration v2

- Atomes : 1815
- Atomes v2 complets : 61
- Atomes v2 incomplets : 1754
- Avertissements de champs v2 manquants : 11362

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
| sources/johnson_morley_an_ideal_for_living/source_suite_03.md | 345 |
| sources/johnson_morley_an_ideal_for_living/source_suite_02.md | 340 |
| sources/sumner_chapter_and_verse/source_part_sumner_salford_formation_sound_v2.md | 336 |
| sources/johnson_morley_an_ideal_for_living/source.md | 320 |
| sources/reynolds_rip_it_up/second_pass_scenes_heritage.md | 288 |
| sources/reynolds_rip_it_up/source.md | 285 |
| sources/hook/atomisation_03_unknown_pleasures_1979.md | 284 |
| sources/flowers/second_pass_new_order_late_discography.md | 261 |
| sources/hook/atomisation_04_unknown_pleasures_track_by_track.md | 237 |

## 10. Commandes utiles

```bash
python3 tools/build_registers.py
python3 tools/audit_repo.py
python3 tools/audit_repo.py --fail-on-error
```
