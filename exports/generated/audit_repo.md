# Audit du repo documentaire

Généré le : `2026-05-16T12:50:57`

## 1. Verdict

Le repo n’est pas strict-compliant : 5 erreur(s) bloquante(s) subsistent.
La dette principale reste la migration v2 : 1707 atome(s) incomplet(s) sur 1768.

## 2. Synthèse chiffrée

- Enregistrements : 3780
- Erreurs : 5
- Avertissements : 18208
- Sources déclarées : 51
- Sources utilisées : 21
- Sources exportées : 21
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 1768 |
| chronology | 343 |
| concept | 183 |
| metadata | 44 |
| motif | 262 |
| myth | 14 |
| person | 157 |
| quote | 358 |
| quote_batch | 1 |
| rules | 1 |
| song | 41 |
| source | 55 |
| template | 336 |
| unknown | 217 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| duplicate_id | 5 |
| field_type_error | 149 |
| invalid_controlled_value | 1532 |
| missing_required_field | 4971 |
| schema_warning | 400 |
| unknown_yaml_block | 217 |
| v2_migration_debt | 10939 |

## 5. Erreurs bloquantes

- **duplicate_id** — `registers/concepts/s13_tomeo_concepts_interzone_rave_era.md` [CONCEPT-065] : Duplicate id also found in registers/concepts/s41_hook_concepts_1976_1977_timeline_two_warsaw_to_joy_division.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/concepts/s13_tomeo_concepts_interzone_rave_era.md` [CONCEPT-066] : Duplicate id also found in registers/concepts/s41_hook_concepts_1976_1977_timeline_two_warsaw_to_joy_division.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/concepts/s13_tomeo_concepts_interzone_rave_era.md` [CONCEPT-067] : Duplicate id also found in registers/concepts/s41_hook_concepts_1976_1977_timeline_two_warsaw_to_joy_division.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/concepts/s13_tomeo_concepts_interzone_rave_era.md` [CONCEPT-068] : Duplicate id also found in registers/concepts/s41_hook_concepts_1976_1977_timeline_two_warsaw_to_joy_division.md → Renommer ou fusionner l’identifiant en doublon.
- **duplicate_id** — `registers/concepts/s13_tomeo_concepts_interzone_rave_era.md` [CONCEPT-069] : Duplicate id also found in registers/concepts/s41_hook_concepts_1978_stiff_chiswick_rca_gretton_factory_granada.md → Renommer ou fusionner l’identifiant en doublon.

## 6. Blocs YAML non classés

- `sources/tomeo_dance_dance_dance/source_part_interzone_rave_era.md` : Unable to infer documentary kind
- `sources/tomeo_dance_dance_dance/source_part_interzone_rave_era.md` : Unable to infer documentary kind
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
- `registers/organizations/s06_carter_organizations_hulme_lived_discursive_space_v2.md` [ORGS-S06-HULME-LIVED-DISCURSIVE-SPACE-V2] : Unable to infer documentary kind
- `registers/organizations/s05_jeffery_tufail_jackson_organizations_public_order_v2.md` [ORGS-S05-PUBLIC-ORDER-GREATER-MANCHESTER-V2] : Unable to infer documentary kind
- `registers/organizations/s20_dodge_organizations_housing_geographies_v2.md` [ORGS-S20-HOUSING-GEOGRAPHIES-V2] : Unable to infer documentary kind
- `registers/organizations/s12_press_aids_anderton_organizations_moral_order_v2.md` [ORGS-S12-AIDS-ANDERTON-MORAL-ORDER-V2] : Unable to infer documentary kind
- `registers/organizations/s02_sueur_organizations_manchester_shrinking_city_v2.md` [ORGS-S02-MANCHESTER-SHRINKING-CITY-V2] : Unable to infer documentary kind
- `registers/organizations/s10_sumner_organizations_late_jd_transition_memory_v2.md` [ORGS-S10-LATE-JD-TRANSITION-MEMORY-V2] : Unable to infer documentary kind
- `registers/organizations/s10_sumner_organizations_salford_formation_sound_v2.md` [ORGS-S10-SUMNER-SALFORD-FORMATION-SOUND-V2] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [DISC-S41-A-FACTORY-SAMPLE-DIGITAL-GLASS] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [LIVE-S41-REZILLOS-UNDERTONES-TOUR-1978] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [LIVE-S41-BRUNEL-SPITTING-1978] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [LIVE-S41-BRISTOL-LOCARNO-EJECTION] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [LIVE-S41-HOPE-ANCHOR-FIRST-LONDON] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_factory_sample_rezillos_hope_anchor_epilepsy.md` [MED-S41-LUTON-DUNSTABLE-FIRST-FIT] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [DISC-S41-AN-IDEAL-FOR-LIVING-EP] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [BAND-S41-WARSAW-PAKT-NEEDLE-TIME] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [INST-S41-CELESTION-18-HIGH-BASS] : Unable to infer documentary kind
- … 177 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Aucune source utilisée n’est absente de `data/registre.json`.

Sources déclarées mais non utilisées :
- S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013 — verifie
- S03 — Demographia, England Largest Cities, s.d. — a_consolider
- S04 — Kidd, Manchester: A History, 2006 — verifie
- S07 — Engels, The Condition of the Working Class in England, 1845 — a_consolider
- S08 — Debord, psychogéographie et dérive, 1955–1958 — a_consolider
- S09 — Cummins, Joy Division, 2010 — verifie
- S11 — UK Treasury / DTI, Financial Statement and Budget Report, 1978–1988 — a_consolider
- S14 — Happy Mondays, « God’s Cop », 1990 — verifie
- S17 — The Fall, « Rowche Rumble », 1979 — a_consolider
- S18 — Fédida, Manchester : L’éveil d’une scène musicale, 2021 — a_consolider
- S19 — Bourdieu, Les trois états du capital culturel, 1979 — verifie
- S21 — City Fun, fanzine, 1978–1983 — a_consolider
- S22 — Wilkinson, City Fun and the politics of post-punk, 2018 — verifie
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

- Atomes : 1768
- Atomes v2 complets : 61
- Atomes v2 incomplets : 1707
- Avertissements de champs v2 manquants : 10939

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
