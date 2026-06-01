# Status — Joy Division AI Writing Studio
> Genere automatiquement le 2026-06-01 11:45 UTC — ne pas editer manuellement.

## Registres

| Registre | Prefixe | Entrees | Public | Prive | Validateur | Dernier verifie |
|----------|---------|---------|--------|-------|------------|-----------------|
| Organisations | `ORG-` | 8 | 6 | 2 | pass | 2026-06-01 |
| Images | `IMAGE-` | 9 | 9 | 0 | pass | 2026-06-01 |
| Chronologie | `EVENT-` | 62 | — | — | pass | — |
| Concerts | `CONCERT-` | 190 | — | — | pass | — |
| Acteurs | `PERSON-` | 166 | — | — | pass | — |
| Lieux | `PLACE-` | 192 | — | — | pass | — |
| Chansons | `JD-SONG-` | 51 | — | — | pass | — |
| Citations | `QUOTE-` | 962 | — | — | pass | — |

## Validateurs

- `tools/validate_orgs.py` : pass — PASS (0 erreurs)
- `tools/validate_images.py` : pass — PASS (0 erreurs)
- `tools/validate_chronology.py` : pass — PASS (0 erreurs)
- `tools/validate_concerts.py` : pass — PASS (0 erreurs)
- `tools/validate_people.py` : pass — PASS (0 erreurs)
- `tools/validate_places.py` : pass — PASS (0 erreurs)
- `tools/validate_songs.py` : pass — PASS (0 erreurs)
- `tools/validate_quotes.py` : pass — PASS (0 erreurs)

## Schemas

- `image_canonical.schema.json` — drift_sentinel v1.0
- `organization_canonical.schema.json` — drift_sentinel v1.0
- `person_canonical.schema.json`
- `song.schema.json`

## Lacunes connues

Aucune lacune documentee.

## Prochaine etape

Step 12 — Cross-registres profond

## Metadata

- Repo : joy-division-ai-writing-studio
- Branche : main
- Dernier commit : 936ad14
- Genere par : tools/generate_status.py
