# Controle M1 - DM vers sources

## Objet

Rapport genere par `python3 tools/check_dm_sources_consistency.py`.

Ce controle est strictement en lecture sur les documents maitres, le manifeste et le registre canonique `data/registre.json`. Il produit des constats et ne corrige aucun ecart.

## Périmètre

Perimetre M1.3 couvert : existence des identifiants de sources `Sxx` ou `Sxxx` explicitement visibles dans les documents maitres et presence de ces identifiants dans `data/registre.json`.

Dans ce rapport, une source mentionnee mais non declaree designe une reference visible qui n'est pas declaree dans le registre canonique.

Hors perimetre : citations, atomes, relations, granularite section, granularite paragraphe, validite historiographique, qualite de source et usage correct de la source.

## Résumé global

| Indicateur | Valeur |
|------------|---------|
| Documents maîtres déclarés | 14 |
| Documents maîtres présents | 14 |
| Documents maîtres cohérents | 14 |
| Documents maîtres non cohérents | 0 |
| Sources canoniques | 94 |
| Sources visibles | 536 |
| Sources retrouvées | 536 |
| Sources inconnues | 0 |
| Sources mentionnées mais non déclarées | 0 |
| Sources orphelines | 19 |
| Écarts détectés | 0 |
| Manifestes incohérents | 0 |
| Documents maîtres absents sur disque | 0 |
| Documents maîtres invalides | 0 |
| Documents maîtres hors manifeste | 0 |
| Registres sources incohérents | 0 |

## Audit par document maître

| DM | Statut | Sources visibles | Sources retrouvées | Sources inconnues | Écarts |
|----|--------|------------------|--------------------|-------------------|--------|
| `chapters/01/document_maitre.md` | cohérent | 49 | 49 | Aucune | Aucun écart |
| `chapters/02/document_maitre.md` | cohérent | 33 | 33 | Aucune | Aucun écart |
| `chapters/03/document_maitre.md` | cohérent | 42 | 42 | Aucune | Aucun écart |
| `chapters/04/document_maitre.md` | cohérent | 39 | 39 | Aucune | Aucun écart |
| `chapters/05/document_maitre.md` | cohérent | 36 | 36 | Aucune | Aucun écart |
| `chapters/06/document_maitre.md` | cohérent | 35 | 35 | Aucune | Aucun écart |
| `chapters/07/document_maitre.md` | cohérent | 28 | 28 | Aucune | Aucun écart |
| `chapters/08/document_maitre.md` | cohérent | 30 | 30 | Aucune | Aucun écart |
| `chapters/09/document_maitre.md` | cohérent | 26 | 26 | Aucune | Aucun écart |
| `chapters/10/document_maitre.md` | cohérent | 37 | 37 | Aucune | Aucun écart |
| `chapters/11/document_maitre.md` | cohérent | 40 | 40 | Aucune | Aucun écart |
| `chapters/12/document_maitre.md` | cohérent | 31 | 31 | Aucune | Aucun écart |
| `chapters/13/document_maitre.md` | cohérent | 38 | 38 | Aucune | Aucun écart |
| `chapters/14/document_maitre.md` | cohérent | 72 | 72 | Aucune | Aucun écart |

## Sources inconnues

Aucune source inconnue détectée.

## Sources orphelines

- `S01` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S03` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S04` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S07` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S16` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S17` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S18` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S19` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S23` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S24` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S25` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S28` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S30` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S32` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S33` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S38` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S73` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S91` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.
- `S92` — présent dans `data/registre.json`, non mobilisé par les documents maîtres.

## Écarts détectés

Aucun écart détecté dans le perimetre M1.3.

## Conclusion

Le controle DM -> sources est conforme : les sources visibles dans les documents maitres existent dans le registre canonique.

Les sources orphelines sont listees comme information documentaire ; elles ne constituent pas un ecart bloquant dans le controle de niveau 1.
