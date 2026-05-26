# Registres structurants — S84 — Cope, « Nothing Here Now but the Recordings », 2018

```yaml
source_id: S84
source_label: "S84 — Cope, Moving Image Record of Joy Division and Factory Video Unit, 2018"
type: registres_structurants
date_creation: "2026-05-26"
```

---

## CONCEPTS

```yaml
id: CONCEPT-archive-audiovisuelle-independante
nom: "Archive audiovisuelle indépendante"
label: "Archive audiovisuelle indépendante (independent moving image archive)"
definition: "Corpus d'enregistrements visuels réalisés hors des structures industrielles de radiodiffusion, sur des équipements domestiques ou semi-professionnels (Super 8, VHS, Betamax), par des individus motivés par l'engagement culturel plutôt que par une commande commerciale. Dans le cas Joy Division : 9 documents entre 1978-1980."
fonction_argumentative: "Fonde la spécificité de la mémoire visuelle de Joy Division comme archive lacunaire et impure, distincte des productions télévisuelles professionnelles — ce qui conditionne toutes les mémorialisations ultérieures (documentaires, expositions, plateformes)."
atomes: [S84-A001, S84-A002, S84-A007, S84-A009, S84-A010, S84-A015]
chapitres: [8, 10, 14]
```

```yaml
id: CONCEPT-culture-diy-multimedia
nom: "Culture DIY multimédia post-punk"
label: "Culture DIY multimédia post-punk (punk/DIY multimedia culture)"
definition: "Pratique culturelle issue du mouvement punk-post-punk consistant à produire, distribuer et diffuser des artefacts visuels et sonores avec des moyens artisanaux et des budgets infimes, en contournant les structures industrielles des grands médias. Reynolds (2005) : 'samizdat culture'. Welsh (1984) : 'populist tendency'."
fonction_argumentative: "Situe Factory Records, Ikon FCL et les filmeurs amateurs de Joy Division dans un écosystème alternatif cohérent (Cabaret Voltaire/Doublevision, Throbbing Gristle/Industrial, Derek Jarman) — leur pratique est le résultat d'une orientation idéologique, pas seulement de contraintes budgétaires."
atomes: [S84-A014, S84-A013, S84-A007]
chapitres: [1, 8, 9]
```

```yaml
id: CONCEPT-qualite-degradee-authenticite
nom: "Qualité dégradée comme authenticité"
label: "Qualité dégradée comme authenticité (degraded quality as authenticity)"
definition: "Réévaluation esthétique et historiographique selon laquelle la qualité technique déficiente des enregistrements amateurs (image brûlée, son saturé, montage grossier) constitue non un défaut mais une marque d'authenticité contextuelle, témoignage direct des conditions réelles de performance plutôt que d'une représentation idéalisée."
fonction_argumentative: "Cadre critique pour aborder les archives audiovisuelles live de Joy Division comme sources primaires valides malgré leurs limitations — et pour comprendre la réévaluation posthume de ce matériau dans les années 2000-2010."
atomes: [S84-A015, S84-A016]
chapitres: [8, 10, 14]
```

```yaml
id: CONCEPT-pre-ere-video-clip
nom: "Pré-ère du clip vidéo"
label: "Pré-ère du clip vidéo (pre-promo video age)"
definition: "Période (fin des années 1970 - début des années 1980) antérieure à la généralisation du clip promotionnel imposée par MTV (lancé en août 1981) et à la multiplication des chaînes musicales, caractérisée par une présence audiovisuelle très limitée des groupes pop/rock dans les médias grand public."
fonction_argumentative: "Explique structurellement la rareté des enregistrements Joy Division et positionne leur héritage visuel comme artefact d'un moment de bascule médiatique — le groupe existe juste avant que la visibilité télévisuelle ne devienne normative pour les groupes de rock."
atomes: [S84-A001, S84-A003]
chapitres: [2, 8, 10]
```

---

## MOTIFS

```yaml
id: MOTIF-archive-lacunaire
nom: "Archive lacunaire"
occurrences: [S84-A001, S84-A002, S84-A015, S84-A017]
description: "Motif de l'insuffisance documentaire comme condition constitutive de la réception et de la mémorialisation de Joy Division — le peu qui reste acquiert une valeur démesurée."
chapitres: [8, 10, 14]
```

```yaml
id: MOTIF-wilson-mediateur
nom: "Wilson comme médiateur culturel"
occurrences: [S84-A003, S84-A004, S84-A005]
description: "Tony Wilson comme figure pivot entre la scène post-punk manchesterienne et les institutions médiatiques (Granada TV, Factory Records), rendant visible ce qui resterait invisible sans sa double position de journaliste et entrepreneur culturel."
chapitres: [1, 2, 5, 8]
```

```yaml
id: MOTIF-danse-curtis-television
nom: "Danse de Curtis à la télévision"
occurrences: [S84-A004, S84-A006]
description: "La danse de Curtis — mouvement compulsif, brutal, confiné — comme signature visuelle du groupe documentée dès la première apparition télévisée (Granada Reports, 1978) et consacrée par Something Else (BBC2, 1979)."
chapitres: [2, 6, 8]
```

```yaml
id: MOTIF-ikon-fcl-pionnier
nom: "Ikon FCL pionnier vidéo indépendant"
occurrences: [S84-A013, S84-A014, S84-A017]
description: "Factory Records et Ikon FCL comme acteurs précurseurs de la distribution vidéo alternative au Royaume-Uni, devançant Doublevision (Cabaret Voltaire) et Jettisoundz d'au moins deux ans."
chapitres: [5, 8, 10]
```

---

## RELATIONS

```yaml
id: R-S84-001
source_id: S84
relation_type: enrichit
from_atoms: [S84-A004]
to_atoms: [S82-A008]
description: "S84-A004 (Granada Reports, danse Curtis) documente empiriquement la danse que S82-A008 (Parmar) analyse théoriquement dans Something Else."
concepts: [danse_curtis_television, corps_dance_curtis]
chapitres: [2, 6, 8]
force: forte
```

```yaml
id: R-S84-002
source_id: S84
relation_type: complemente
from_atoms: [S84-A011]
to_atoms: [S83-A010]
description: "S84-A011 documente en détail le tournage du clip LWTA (T.J. Davidson's, 28 avril 1980, Stuart Orme, 16mm) — S83-A010 (Greenwood & Tarpey) le mentionne brièvement comme exemple d'appropriation de l'espace industriel."
concepts: [tj_davidsons_video, espace_industriel_coopte]
chapitres: [8, 14]
force: forte
song_id: JD-SONG-035
```

```yaml
id: R-S84-003
source_id: S84
relation_type: fonde
from_atoms: [S84-A002]
to_atoms: [S84-A009, S84-A010, S84-A012]
description: "S84-A002 (Table 11.1) est le document de référence canonique dont S84-A009, A010 et A012 développent le détail analytique."
concepts: [inventaire_canonique_audiovisuel]
chapitres: [8, 9, 10]
force: forte
```

```yaml
id: R-S84-004
source_id: S84
relation_type: contextualise
from_atoms: [S84-A014]
to_atoms: [S84-A013, S84-A007]
description: "S84-A014 (cadre DIY multimédia post-punk) contextualise idéologiquement les pratiques de Whitehead (S84-A007) et d'Ikon FCL (S84-A013) dans un réseau plus large."
concepts: [culture_diy_multimedia, punk_television_alternative]
chapitres: [1, 8, 9]
force: forte
```

```yaml
id: R-S84-005
source_id: S84
relation_type: revalue
from_atoms: [S84-A015]
to_atoms: [S84-A009, S84-A010, S84-A012]
description: "S84-A015 (qualité dégradée comme authenticité) revalue rétrospectivement les enregistrements low-budget (S84-A009, A010) et leur compilation (S84-A012) dont la critique contemporaine soulignait surtout les défauts techniques."
concepts: [qualite_degradee_authenticite, media_archaeology_live]
chapitres: [8, 10, 14]
force: forte
```
