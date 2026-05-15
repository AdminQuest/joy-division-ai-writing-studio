# Audit du repo documentaire

Généré le : `2026-05-15T16:13:39`

## 1. Verdict

Le repo est techniquement exploitable, mais 106 bloc(s) YAML ne sont pas classés.
La dette principale reste la migration v2 : 1520 atome(s) incomplet(s) sur 1581.

## 2. Synthèse chiffrée

- Enregistrements : 3237
- Erreurs : 0
- Avertissements : 16111
- Sources déclarées : 19
- Sources utilisées : 12
- Sources exportées : 12
- Sources utilisées absentes du registre : 0
- Libellés faibles : 0

## 3. Enregistrements par type

| Type | Nombre |
|---|---:|
| atom | 1581 |
| chronology | 331 |
| concept | 143 |
| metadata | 18 |
| motif | 218 |
| myth | 11 |
| person | 157 |
| quote | 353 |
| quote_batch | 1 |
| rules | 1 |
| song | 41 |
| source | 56 |
| template | 220 |
| unknown | 106 |

## 4. Catégories de problèmes

| Catégorie | Nombre |
|---|---:|
| field_type_error | 135 |
| invalid_controlled_value | 1320 |
| missing_required_field | 4580 |
| schema_warning | 399 |
| unknown_yaml_block | 106 |
| v2_migration_debt | 9571 |

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
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [ALBUM-S41-A-FACTORY-SAMPLE-FAC2-TIMELINE-1979] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [PHOTO-S41-CUMMINS-PRINCESS-PARKWAY-NME] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [RADIO-S41-FIRST-PEEL-SESSION-1979] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [ALBUM-S41-UNKNOWN-PLEASURES-FACT10-TIMELINE] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [RADIO-S41-PICCADILLY-RADIO-1979-CHANCE-ATROCITY] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [LIVE-S41-YMCA-NASHVILLE-LEIGH-AUGUST-1979] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [FILM-S41-THE-FACTORY-FLICK-FAC9] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [TV-S41-SOMETHING-ELSE-SLC-TRANSMISSION] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_unknown_pleasures_track_by_track_2_timeline_four_jan_oct.md` [COMP-S41-EARCOM2-FAST9B] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-STIFF-CHISWICK-RAFTERS-1978-04-14] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [DISC-S41-AN-IDEAL-12-INCH-GRETTON] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-FIRST-FACTORY-RUSSELL-CLUB-1978-06-09] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [LIVE-S41-BAND-ON-THE-WALL-1978] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_stiff_chiswick_rca_gretton_factory_granada.md` [TV-S41-GRANADA-REPORTS-SHADOWPLAY-1978-09-20] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [TOUR-S41-BUZZCOCKS-OCT-NOV-1979-END] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [LIVE-S41-ELECTRIC-BALLROOM-1979-10-26] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [PHOTO-S41-ANTON-CORBIJN-1979] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [LIVE-S41-BOURNEMOUTH-WINTER-GARDENS-HOSPITAL] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [RADIO-S41-SECOND-PEEL-SESSION-1979-11-26] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [LIVE-S41-LES-BAINS-DOUCHES-1979-12-18] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [EVENT-S41-FACTORY-OFFICE-PARTY-1979-12-31] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [TOUR-S41-EUROPEAN-TOUR-JAN-1980-ANNIK] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1979_1980_timeline_four_end_europe_annnik_we_carried_on.md` [LIVE-S41-WE-CARRIED-ON-FITS-STAGE] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1980_closer_britannia_row_lwtua_mix_annnik_saville.md` [ALBUM-S41-CLOSER-BRITANNIA-ROW-SESSIONS] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1980_closer_britannia_row_lwtua_mix_annnik_saville.md` [TECH-S41-HANNETT-AURATONES-ARP-GATES] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1980_closer_britannia_row_lwtua_mix_annnik_saville.md` [VISUAL-S41-CLOSER-STAGLIENO-SAVILLE-WOLFF] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1980_closer_britannia_row_lwtua_mix_annnik_saville.md` [NETWORK-S41-U2-11-OCLOCK-TICK-TOCK-HANNETT] : Unable to infer documentary kind
- `registers/songs/s41_hook_songs_1978_pips_first_joy_division_gig.md` [BOOK-S41-HOUSE-OF-DOLLS-NAME] : Unable to infer documentary kind
- … 66 bloc(s) supplémentaire(s) dans `audit_repo.json`.

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

- Atomes : 1581
- Atomes v2 complets : 61
- Atomes v2 incomplets : 1520
- Avertissements de champs v2 manquants : 9571

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
