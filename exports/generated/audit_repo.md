# Audit du repo documentaire

Généré le : `2026-05-14T16:42:15`

## 1. Verdict

Le repo est techniquement exploitable, mais 55 bloc(s) YAML ne sont pas classés.
La dette principale reste la migration v2 : 1404 atome(s) incomplet(s) sur 1465.

## 2. Synthèse chiffrée

- Enregistrements : 2813
- Erreurs : 0
- Avertissements : 15018
- Sources déclarées : 19
- Sources utilisées : 12
- Sources exportées : 12
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 1465 |
| chronology | 331 |
| concept | 78 |
| metadata | 18 |
| motif | 120 |
| myth | 11 |
| person | 157 |
| quote | 353 |
| quote_batch | 1 |
| rules | 1 |
| song | 41 |
| source | 56 |
| template | 126 |
| unknown | 55 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| field_type_error | 135 |
| invalid_controlled_value | 1223 |
| missing_required_field | 4000 |
| schema_warning | 399 |
| unknown_yaml_block | 55 |
| v2_migration_debt | 9206 |

## 5. Erreurs bloquantes

Aucune.

## 6. Blocs YAML non classés

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
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [LIVE-S41-OLDHAM-TOWER-CLUB-NO-AUDIENCE] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1977_an_ideal_name_change_tj_davidson_sound.md` [LIVE-S41-SWINGING-APPLE-1977-12-31] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-STIFF-CHISWICK-RAFTERS-1978-04-14] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [DISC-S41-AN-IDEAL-12-INCH-GRETTON] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-FIRST-FACTORY-RUSSELL-CLUB-1978-06-09] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-BAND-ON-THE-WALL-1978] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [TV-S41-GRANADA-REPORTS-SHADOWPLAY-1978-09-20] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_pips_first_joy_division_gig.md` [BOOK-S41-HOUSE-OF-DOLLS-NAME] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_pips_first_joy_division_gig.md` [LIVE-S41-PIPS-FIRST-JOY-DIVISION-GIG] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1956_1976_salford_jamaica_music_pistols_epiphany.md` [MEDIA-S41-MELODY-MAKER-PISTOLS-APRIL-1976] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1956_1976_salford_jamaica_music_pistols_epiphany.md` [FILM-S41-THATLL-BE-THE-DAY] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1956_1976_salford_jamaica_music_pistols_epiphany.md` [ARTIST-S41-SEX-PISTOLS-AS-CLASS-PERMISSION] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_european_tour_annik_closer_threshold.md` [FILM-S45-ERASERHEAD-ABSENCE] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_european_tour_annik_closer_threshold.md` [LIVE-S45-NEW-OSBOURNE-CITY-FUN] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [LIVE-S45-MOONLIGHT-RAINBOW-APRIL-1980] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [LIVE-S45-DERBY-HALL-BURY-1980] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [LIVE-S45-BIRMINGHAM-HIGH-HALL-FINAL-GIG] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [OBJ-S45-SORDIDE-SENTIMENTALE-1106] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [FILM-S45-STROSZEK-DEADLINE] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1980_moonlight_overdose_bury_divorce_last_clinic.md` [OBJ-S45-LAST-PHOTOGRAPH-NATALIE] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1979_annik_apollo_rainbow_marriage_collapse.md` [FILM-S45-ERASERHEAD-DISPARITION] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1979_annik_apollo_rainbow_marriage_collapse.md` [LIVE-S45-APOLLO-MANCHESTER-1979] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1979_annik_apollo_rainbow_marriage_collapse.md` [LIVE-S45-RAINBOW-THEATRE-1979] : Unable to infer documentary kind
- `registers/songs/s45_curtis_songs_1979_annik_apollo_rainbow_marriage_collapse.md` [LIVE-S45-FACTORY-NYE-SECTION-25] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [PLACE-S41-SWAN-PUB-ECCLES-NEW-ROAD] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [LIVE-S41-STOCKS-WALKDEN-TALENT-CONTEST] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [LIVE-S41-MIDDLESBROUGH-TAPE-1977-09-14] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [DISC-S41-SHORT-CIRCUIT-FEATURING-JOY-DIVISION] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [DISC-S41-PANIK-IT-WONT-SELL-RAINY-CITY] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1976_1977_timeline_two_warsaw_to_joy_division.md` [LIVE-S41-SWINGING-APPLE-LAST-WARSAW-TL2] : Unable to infer documentary kind
- … 15 bloc(s) supplémentaire(s) dans `audit_repo.json`.

## 7. Registre des sources

Aucune source utilisée n’est absente de `data/registre.json`.

Sources déclarées mais non utilisées :
- S01 — Blakeley & Evans, The Regeneration of East Manchester, 2013 — consolidée
- S02 — Sueur, Villes du futur, futur des villes, 2011 — consolidée
- S03 — Demographia, England Largest Cities, s.d. — consolidée comme source statistique web ; à archiver
- S04 — Kidd, Manchester: A History, 2006 — consolidée
- S05 — Jeffery, Tufail & Jackson, Policing and the Reproduction of Local Social Order, 2015 — consolidée
- S06 — Carter, Youth, race and the inner-city estate, 2023 — consolidée
- S73 — Blue Orchids, référence historique à consolider, s.d. — référence historique déplacée depuis S41 ; à consolider

Aucun libellé faible.

## 8. Migration v2

- Atomes : 1465
- Atomes v2 complets : 61
- Atomes v2 incomplets : 1404
- Avertissements de champs v2 manquants : 9206

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
| sources/johnson_morley_an_ideal_for_living/source.md | 320 |
| sources/reynolds_rip_it_up/second_pass_scenes_heritage.md | 288 |
| sources/reynolds_rip_it_up/source.md | 285 |
| sources/hook/atomisation_03_unknown_pleasures_1979.md | 284 |
| sources/flowers/second_pass_new_order_late_discography.md | 261 |
| sources/hook/atomisation_04_unknown_pleasures_track_by_track.md | 237 |
| sources/hook/atomisation_05_closer_phase_terminale_1980.md | 219 |

## 10. Commandes utiles

```bash
python3 tools/build_registers.py
python3 tools/audit_repo.py
python3 tools/audit_repo.py --fail-on-error
```
