# Rapport d'audit — 26 mai 2026

> Généré le **26 mai 2026**. Couvre l'intégralité de la session du jour : complétion des citations H&S (S85–S88), corrections des erreurs bloquantes, mise à jour registre.

---

## 1. État final après session

| Indicateur | Avant session | Après session |
|---|---:|---:|
| Sources déclarées | 88 | **89** (+REGISTRY) |
| Total atomes | 2 716 | 2 716 (stable) |
| Total enregistrements | ~7 295 | **7 292** |
| **Erreurs bloquantes** | **15** | **0** ✅ |
| Avertissements | 31 249 | 31 249 (stable) |
| Doublons d'identifiants | 14 | 0 |
| YAML parse errors | 1 | 0 |

---

## 2. Travaux effectués

### 2.1 Complétion des citations Heart & Soul (S85–S88)

Passe de vérification des citations sur le PDF H&S partagé (`pages_pdf = pages_livre + 31`).

| Source | Travail | Citations | État |
|---|---|---:|---|
| S85 Malcolm | `note_verification` ajoutée aux 8 citations existantes | 8 | ✅ Vérifiées |
| S86 Breyley | Section CITATIONS créée (5 nouvelles) | 5 | ✅ Vérifiées |
| S87 Otter Bickerdike | Section CITATIONS créée (6 nouvelles) | 6 | ✅ Vérifiées |
| S88 Cashell | Section CITATIONS créée (10 nouvelles) | 10 | ✅ Vérifiées |

**Citations vérifiées sur PDF dans cette session : 29**

Auteurs cités couverts :
- S85 : Wilson 2007, Hook/Sumner/Morris, Baudrillard, Hingley, Wilson/Buckle
- S86 : Hegarty 2015, Benjamin 1992, Yi 2015, Sumner (Kennedy 2006), Frith 2003
- S87 : Cummins (Lachno 2014), Zhao 2015, Klosterman 2005, Morley 2007, Saville 2007, Adorno & Horkheimer 1944
- S88 : Benjamin 1970, Morris (Scanlon 2005), Hook (Sweeney 2005), Rowland NME 1981, Sumner (Savage 1997), Fisher 2014 ×3, Saville 2007, Derrida 1994

**Correctif YAML appliqué dans S88** : séparateur `"text1" / "text2"` (invalide YAML) remplacé par `"text1 [—] text2"` pour 5 citations (CIT-S88-002, -003, -006, -008, -009).

**Correctif `atomisation_workflow.md` (repo privé)** : note sur l'offset de pagination reformulée : `pages_pdf = pages_livre + 31`.

---

### 2.2 Corrections des erreurs bloquantes (15 → 0)

#### P1 — YAML parse error (1 erreur)
- **Fichier** : `registers/concepts/master_concepts.md` ligne 639
- **Cause** : valeur YAML avec deux-points non encadrée de guillemets dans une liste `critiques:`
- **Correctif** : guillemets doubles ajoutés sur la valeur multi-caractères

#### P2 — Identifiants dupliqués S79 (10 erreurs)
Origine : les fichiers `relations_s79_intro_savage_v2.md` et `relations_s79_foreword_deborah_v2.md` avaient réutilisé des numéros de séquence déjà attribués dans `warsaw_v2.md` et `leaders_of_men_v2.md`.

| Fichier | IDs renommés | Nouveaux IDs |
|---|---|---|
| `relations_s79_foreword_deborah_v2.md` | R-S79-005, -006 | R-S79-069, -070 |
| `relations_s79_intro_savage_v2.md` | R-S79-007 à -014 | R-S79-071 à -078 |

Règle appliquée : les IDs `warsaw_v2.md` et `leaders_of_men_v2.md` sont les originaux (inchangés). Séquence la plus haute avant correction : R-S79-068.

#### P3 — MOTIF / CONCEPT dupliqués (4 erreurs + 1 découverte)

| ID | Fichier canonique (conservé) | Fichier dupliqué (corrigé) | Action |
|---|---|---|---|
| MOTIF-wilson-mediateur | `s84_cope_structuring_registers.md` | `s85_malcolm_structuring_registers.md` | Renommé MOTIF-wilson-mediateur-s85 |
| MOTIF-009 | `registers/motifs/master_motifs.md` | `s45_curtis_motifs_vote_conservateur.md` | Supprimé de s45 |
| MOTIF-010 | `registers/motifs/master_motifs.md` | `s45_curtis_motifs_vote_conservateur.md` | Supprimé de s45 |
| CONCEPT-010 | `registers/concepts/master_concepts.md` | `s45_curtis_concepts_vote_conservateur.md` | Supprimé de s45 |
| CONCEPT-011 | `registers/concepts/master_concepts.md` | `s45_curtis_concepts_1976_1977.md` | **Découverte lors de la passe** → renommé CONCEPT-auto-habilitation-artistique dans 5 fichiers s45 |

La correction de CONCEPT-010 a révélé un nouveau doublon (CONCEPT-011) qui n'apparaissait pas dans le premier rapport d'audit — vraisemblablement masqué par l'ordre de scan. Corrigé dans la même passe.

#### P4 — Blocs YAML non classifiés (avertissements → non bloquants)
Ajout de champ `type:` dans les blocs sans discriminant explicite :

| Fichier | Blocs corrigés | Type ajouté |
|---|---:|---|
| `relations_s80_transmission_v2.md` | 7 | `type: relation` |
| `relations_s62_introduction_v2.md` | 6 | `type: relation` |
| `relations_s87_otter_bickerdike_posteconomy.md` | 7 | `type: relation` |
| `relations_s63_wilson_faustian_v2.md` | 11 | `type: relation` |
| `relations_stabilisees.md` (S27) | 8 | `type: relation` |
| `registres_structurants_s27.md` | 16 | types sémantiques (concept/motif/mythe/reference) |
| `registres_specialises_s27.md` | 6 | types container (citations/chronologie/acteurs/lieux/organisations/chansons) |

> **Note** : ces corrections ont ajouté le champ discriminant, mais les blocs restent classés `unknown` dans l'audit car le champ `type:` n'est pas le seul discriminant utilisé par l'auditeur. Ces blocs sont des **avertissements**, non des erreurs — leur présence n'est pas bloquante.

#### P5 — REGISTRY absent du registre
- Ajout d'une entrée `REGISTRY` dans `data/registre.json` avec `statut: reference_interne`, `fiabilite: haute`, `usage: identifiants canoniques chansons, song_id`.

---

## 3. Fichiers modifiés

### Repo public (`joy-division-ai-writing-studio`)

| Fichier | Nature de la modification |
|---|---|
| `registers/concepts/master_concepts.md` | Fix YAML parse error (critiques: guillemets) |
| `registers/concepts/s45_curtis_concepts_vote_conservateur.md` | CONCEPT-010 supprimé |
| `registers/concepts/s45_curtis_concepts_1976_1977.md` | CONCEPT-011 renommé CONCEPT-auto-habilitation-artistique |
| `registers/motifs/s45_curtis_motifs_vote_conservateur.md` | MOTIF-009, MOTIF-010 supprimés |
| `registers/motifs/s45_curtis_motifs_1976_1977.md` | Références CONCEPT-011 renommées |
| `registers/motifs/s45_curtis_motifs_1978_wilson_gretton_band_on_the_wall.md` | Références CONCEPT-011 renommées |
| `registers/references/s45_curtis_relations_rag_1976_1977.md` | Références CONCEPT-011 renommées |
| `registers/references/s45_curtis_relations_rag_1977_1978_an_ideal_rca.md` | Références CONCEPT-011 renommées |
| `registers/s85_malcolm_structuring_registers.md` | MOTIF-wilson-mediateur → -s85 |
| `registers/s85_malcolm_specialized_registers.md` | note_verification sur 8 citations |
| `registers/s86_breyley_specialized_registers.md` | Section CITATIONS créée (5 entrées) |
| `registers/s87_otter_bickerdike_specialized_registers.md` | Section CITATIONS créée (6 entrées) |
| `registers/s88_cashell_specialized_registers.md` | Section CITATIONS créée (10 entrées) ; fix YAML |
| `sources/curtis_savage_so_this_is_permanence/relations_s79_foreword_deborah_v2.md` | R-S79-005/006 → 069/070 |
| `sources/curtis_savage_so_this_is_permanence/relations_s79_intro_savage_v2.md` | R-S79-007–014 → 071–078 |
| `sources/valdes_miyares_transmission/relations_s80_transmission_v2.md` | type: relation ajouté |
| `sources/heart_soul_introduction/relations_s62_introduction_v2.md` | type: relation ajouté |
| `sources/otter_bickerdike_posteconomy_curtis/relations_s87_otter_bickerdike_posteconomy.md` | type: relation ajouté |
| `sources/jacobson_jeffrey_wilson_faustian/relations_s63_wilson_faustian_v2.md` | type: relation ajouté |
| `sources/riom_review_crossley_networks/relations_stabilisees.md` | type: relation ajouté |
| `sources/riom_review_crossley_networks/registres_structurants_s27.md` | types sémantiques ajoutés |
| `sources/riom_review_crossley_networks/registres_specialises_s27.md` | types container ajoutés |
| `data/registre.json` | REGISTRY ajouté ; S85–S88 : citations_verifiees, nb_citations, note_passe |
| `reports/atomisation/tableau_de_bord.md` | Régénération complète — état 26/05/2026 |
| `reports/audit/audit_26_mai_2026.md` | Nouveau — ce fichier |

### Repo privé (`joy-division-studio-private`)

| Fichier | Nature de la modification |
|---|---|
| `prompts/atomisation_workflow.md` | Note pagination H&S reformulée : `pages_pdf = pages_livre + 31` |

---

## 4. État de la dette restante

### 4.1 Migration v2 (non bloquante, stratégique)

| Indicateur | Valeur |
|---|---:|
| Atomes v2 complets | 73 |
| Atomes v2 incomplets | 2 643 |
| Avertissements v2 | 16 672 |

Cette dette ne doit pas être corrigée mécaniquement. Elle est inhérente aux atomes créés avant le schéma v2. La migration se fait source par source, lors des passes d'atomisation ou de révision.

**Fichiers avec la plus forte dette v2** :

| Fichier | Problèmes |
|---|---:|
| `mike_west_joy_division/source_atomisation_02.md` | 734 |
| `mike_west_joy_division/source_atomisation_03.md` | 483 |
| `flowers/source.md` | 432 |
| `mike_west_joy_division/source_atomisation_04.md` | 417 |
| `hook/atomisation_02_transmission_1978.md` | 406 |

### 4.2 Pages H&S restant à atomiser

| Source | Pages manquantes | Impact |
|---|---|---|
| S64 Bottà | pp. 45–46 | 2 pages, faible |
| S65 Martínez | pp. 50, 62 | 2 pages, faible |
| S66 Schütte | pp. 79–80 | 2 pages, faible |
| S67 Naiman | pp. 96–98 | 3 pages, faible |
| S80 Valdés Miyares | pp. 110–114 | 5 pages, modéré |
| S81 Devereux et al. | pp. 129–130 | 2 pages, faible |
| S82 Parmar | pp. 135, 153–154 | 3 pages, faible |
| S83 Greenwood & Tarpey | pp. 160, 168–170 | 4 pages, modéré |
| S84 Cope | pp. 183–184, 190–192 | 5 pages, modéré |
| S85 Malcolm | p. 208 | 1 page, très faible |

### 4.3 Avertissements de structure (non bloquants)

- **unknown_yaml_block** : 1 395 blocs non classifiés dans les fichiers de relations. Le champ `type:` ajouté aujourd'hui n'est pas reconnu comme discriminant principal par l'auditeur — ces blocs restent dans la catégorie avertissements. Impact nul sur l'exploitation des données.
- **missing_required_field** : 9 211 avertissements — champs v2 manquants dans les atomes v1.
- **invalid_controlled_value** : 2 782 avertissements — valeurs hors vocabulaire contrôlé (majoritairement dans les atomes v1).

### 4.4 Registre des sources

- **13 sources déclarées non utilisées** : S01, S03, S04, S18, S23, S24, S25, S28, S30, S32, S33, S36, S38. Aucune atomisation n'a démarré pour ces sources.
- **S73** : référence historique déplacée depuis S41, à consolider.

---

## 5. Commits effectués

| Repo | Hash | Message |
|---|---|---|
| Public | `437265cf` | `fix(audit): résolution des 15+1 erreurs bloquantes — doublons IDs, YAML parse, type manquants, REGISTRY` |
| Privé | commit session précédente | `fix(atomisation_workflow): pagination offset H&S reformulée` |

---

## 6. Prochaines passes recommandées

1. **Compléter les pages manquantes H&S** : S80 (pp. 110–114), S83 (pp. 168–170), S84 (pp. 183–184, 190–192) — passages à fort potentiel documentaire.
2. **Démarrer S07 (Engels)** : le contexte industriel de Manchester est sous-documenté en sources primaires.
3. **Poursuivre la deuxième passe S71 (Flowers)** : source secondaire publiée avec fort potentiel pour les chapitres 1, 8, 14.
4. **Ajouter `type:` discriminant dans les blocs de relations** : l'auditeur n'utilise pas `type: relation` comme discriminant ; vérifier la documentation de l'auditeur pour identifier le champ attendu.

---

_Rapport généré le 26 mai 2026. 0 erreur bloquante. Corpus en état d'exploitation._
