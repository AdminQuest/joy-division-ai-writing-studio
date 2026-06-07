# Rapport d'atomisation — S95 — Komlenić, « Rock Music, Suicide and Media Influence », 2021

Date : 2026-06-07

## Source canonisée

```text
S95 — KOMLENIĆ, Miroslav, « Rock Music, Suicide and Media Influence », Applied Media Studies Journal, vol. 2, n° 1, 2021, p. 23-33, DOI 10.46630/msae.1.2021.02.
```

Source locale de travail :

```text
sources/_incoming/S95_Rock_Music_Suicide_and_Media_Influence.pdf
```

Le PDF est conservé comme matériau local non versionné, conformément à `.gitignore`.

## Périmètre lu

Lecture complète de l'article, p. 23-33 :

- p. 23 : abstract, objectif critique, hypothèse de médiation ;
- p. 24-25 : facteurs de risque, médiation sociale, prudence causale ;
- p. 26-27 : chansons, accusations, procès et liberté artistique ;
- p. 27-30 : suicides de fans et d'artistes, mention d'Ian Curtis, tableau comparatif ;
- p. 30-31 : discussion, identification, imitation, non-suffisance de la musique ;
- p. 32-33 : références et résumé serbe.

## Nature de la passe

Cette passe est une atomisation historiographique sélective v2.

Elle ne traite pas S95 comme :

- biographie Joy Division ;
- source clinique sur Ian Curtis ;
- preuve causale contre le rock ;
- catalogue de suicides de musiciens.

Elle traite S95 comme :

- source analytique sur musique rock, suicide et influence médiatique ;
- source de prudence méthodologique ;
- source utile à l'écriture responsable des chapitres 12 et 14.

## Nombre d'atomes créés

8 atomes v2 :

| Atome | Titre | Chapitres |
| --- | --- | --- |
| S95-A001 | La source pose une question d'influence, mais son objectif est critique plutôt qu'accusatoire | 12, 14 |
| S95-A002 | Les facteurs sociaux sont des médiateurs ou modérateurs, pas des causes simples | 12 |
| S95-A003 | Les procès contre des chansons rock documentent surtout une controverse de réception | 12, 14 |
| S95-A004 | Ian Curtis apparaît dans une série rock, mais l'article suspend explicitement la causalité | 12, 14 |
| S95-A005 | La panique morale transforme la musique en bouc émissaire explicatif | 14 |
| S95-A006 | L'identification et l'imitation sont des processus de réception, non des automatismes | 12, 14 |
| S95-A007 | La musique peut être self-therapy pour l'artiste avant d'être risque pour l'auditeur | 11, 12 |
| S95-A008 | Conclusion responsable : aucun facteur culturel ne suffit à expliquer le suicide | 12, 14 |

## Registres enrichis

Entrées créées dans `sources/komlenic_rock_music_suicide_media_influence/registers_update_s95_rock_music_suicide_media_influence.md` :

- `CONCEPT-S95-001` — médiation musicale du risque ;
- `CONCEPT-S95-002` — panique morale rock-suicide ;
- `MOTIF-S95-001` — refus de la cause unique ;
- `MYTH-S95-001` — la chanson comme cause directe du suicide ;
- `MYTH-S95-002` — Ian Curtis comme preuve générale du danger du rock.

## Relations créées

6 relations stabilisées :

- `R-S95-001` — non-monocausalité S95 ↔ autopsie psychologique S81 ;
- `R-S95-002` — mention d'Ian Curtis dans une série rock ↔ interdiction de l'usage biographique direct ;
- `R-S95-003` — identification fan-artiste ↔ culte et réception posthume ;
- `R-S95-004` — controverse des chansons accusées ↔ responsabilité critique du chapitre 12 ;
- `R-S95-005` — art comme expression / self-therapy ↔ refus de réduire Curtis à un symptôme ;
- `R-S95-006` — suicide comme authenticité mythique ↔ garde-fou anti-romantisation.

## Chapitres renforcés

| Chapitre | Apport S95 |
| --- | --- |
| Chapitre 11 | Appui secondaire sur l'expression artistique comme médiation de souffrance, sous prudence anti-réduction clinique. |
| Chapitre 12 | Renforcement central : non-monocausalité, prudence causale, suicide et médias, responsabilité d'écriture. |
| Chapitre 14 | Renforcement central : réception posthume, panique morale, culte du martyr, identification et romantisation. |

## Apports historiographiques

S95 apporte un cadrage transversal sur les risques éthiques d'une écriture qui associe musique rock et suicide.

Ses apports réellement nouveaux :

- distinguer influence, médiation, identification et causalité ;
- replacer la mention de Ian Curtis dans une série médiatique rock sans l'utiliser comme preuve biographique ;
- fournir un vocabulaire pour parler des chansons accusées sans reproduire la panique morale ;
- verrouiller le chapitre 12 contre la cause unique ;
- verrouiller le chapitre 14 contre la transformation du suicide en authenticité artistique.

## Limites de la passe

- La source est secondaire et synthétique : elle n'établit pas de causalité empirique propre à Joy Division.
- Certaines listes ou exemples de l'article doivent être recoupés si le manuscrit les mobilise factuellement.
- S95 n'est pas une source médicale spécialisée ; S81 reste prioritaire sur le suicide de Curtis.
- S95 n'est pas une source biographique Joy Division ; les sources S35, S41, S45, S67, S76 et S81 restent prioritaires selon le sujet.

## Points à vérifier ultérieurement

- Recouper les exemples de procès et de controverses si le manuscrit les détaille.
- Ne pas citer longuement les paroles suicidaires mentionnées par l'article.
- Vérifier la compatibilité de l'usage S95 avec les recommandations éditoriales de prévention du suicide si le chapitre 12 devient plus public-facing.

## Contrôles exécutés

- `python3 tools/build_registers.py --strict`
  - résultat : `errors: 0`
  - note : warnings hérités de la dette existante du dépôt ; aucune alerte S95 après correction des YAML S95.
- `python3 tools/audit_repo.py`
  - résultat : `errors: 0`
  - note : warnings globaux existants inchangés hors S95.
- `python3 tools/build_master_docs.py`
  - résultat : documents maîtres reconstruits ; index généré dans `exports/generated/master_docs_index.json`.

Vérifications demandées :

```bash
grep -R "S95-A" sources exports/generated chapters reports
grep -R "S95" exports/generated/index_by_id.json
grep -R "S95" exports/generated/all_records.json
```

## Preuve de propagation

| Atome | Fichier source | Export présent | DM impactés | Registres impactés |
| --- | --- | --- | --- | --- |
| S95-A001 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 12, 14 ; S95 visible dans les tables sources des DM ch.12 et ch.14 | `CONCEPT-S95-001` |
| S95-A002 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitre 12 ; S95 visible dans la table sources du DM ch.12 | `CONCEPT-S95-001`, `MOTIF-S95-001` |
| S95-A003 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 12, 14 ; S95 visible dans les tables sources des DM ch.12 et ch.14 | `CONCEPT-S95-002`, `MYTH-S95-001` |
| S95-A004 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 12, 14 ; S95 visible dans les tables sources des DM ch.12 et ch.14 | `MOTIF-S95-001`, `MYTH-S95-002` |
| S95-A005 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitre 14 ; S95 visible dans la table sources du DM ch.14 | `CONCEPT-S95-002` |
| S95-A006 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 12, 14 ; S95 visible dans les tables sources des DM ch.12 et ch.14 | `CONCEPT-S95-001` |
| S95-A007 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 11, 12 ; S95 visible dans les tables sources des DM ch.11 et ch.12 | — |
| S95-A008 | `sources/komlenic_rock_music_suicide_media_influence/atoms_dm_s95_rock_music_suicide_media_influence_v2.md` | `exports/generated/index_by_id.json`, `exports/generated/all_records.json`, `exports/generated/atoms.json`, `exports/generated/atoms.csv` | Chapitres 12, 14 ; S95 visible dans les tables sources des DM ch.12 et ch.14 | `MOTIF-S95-001`, `MYTH-S95-001`, `MYTH-S95-002` |

Traces documents maîtres :

- `chapters/11/document_maitre.md` : table sources, `S95`, 1 atome.
- `chapters/12/document_maitre.md` : table sources, `S95`, 7 atomes.
- `chapters/14/document_maitre.md` : table sources, `S95`, 6 atomes.

Conclusion :

**A. S95 est canonisée et pleinement intégrée.**
