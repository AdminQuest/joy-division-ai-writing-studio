# Audit pilote M1 — Traçabilité des documents maîtres

# Objet de l'audit

Cet audit pilote vérifie si le modèle M1 de traçabilité est applicable aux documents maîtres existants.

Les documents maîtres constituent le premier périmètre d'audit parce qu'ils sont les vues rédactionnelles persistantes les plus exposées du corpus exporté. Ils concentrent des sources, des atomes, des citations, des événements chronologiques, des personnes, des chansons, des concepts et des motifs. Leur fiabilité conditionne donc la réutilisation rédactionnelle du socle documentaire.

La traçabilité est testée avant les autres contrôles M1 parce qu'elle est le prérequis de la dérivabilité, de l'obsolescence et de la cohérence documentaire. Si un document maître ne permet pas d'identifier ses sources, atomes, registres ou exports d'appui, les contrôles ultérieurs ne peuvent pas être interprétés correctement.

L'audit s'appuie sur la typologie M1 déjà définie, en particulier la défaillance de traçabilité : une information présente dans un livrable documentaire ne peut plus être reliée à une source, un atome, un registre, un export ou un script de génération.

# Périmètre

Le périmètre est strictement limité à :

- les 14 documents maîtres `chapters/*/document_maitre.md` ;
- le manifeste `chapters/master_docs.json` ;
- les exports associés disponibles dans `exports/generated/` ;
- les sources mobilisées explicitement listées dans chaque document maître.

L'audit ne porte pas sur l'ensemble du corpus. Il ne vérifie pas tous les atomes, toutes les sources, tous les registres ni tous les exports du dépôt. Il ne corrige aucun écart et ne régénère aucun artefact.

Les exports associés observés sont notamment :

- `exports/generated/master_docs_index.json` ;
- `exports/generated/atoms.json` ;
- `exports/generated/sources.json` ;
- `exports/generated/quotes.json` ;
- `exports/generated/chronology.json` ;
- `exports/generated/people.json` ;
- `exports/generated/songs.json` ;
- `exports/generated/concepts.json` ;
- `exports/generated/motifs.json` ;
- `exports/generated/index_by_id.json`.

Le script `tools/build_master_docs.py` indique que les documents maîtres sont générés depuis `exports/generated/*.json` et `chapters/master_docs.json`. Cette mention sert uniquement de contexte documentaire ; aucun contrôle automatisé n'est créé par cette PR.

# Méthode

La méthode retenue est une lecture documentaire croisée.

Pour chaque document maître, l'audit cherche à répondre aux questions suivantes :

- quelles sources ?
- quels atomes ?
- quels registres ?
- quels exports ?

Les preuves retenues sont uniquement :

- le bloc YAML de chaque document maître ;
- le tableau de bord documentaire interne au document maître ;
- la section `Sources mobilisées` ;
- les sections `Atomes critiques ou majeurs` et `Autres atomes utiles` ;
- les sections `Citations disponibles`, `Chronologie rattachée`, `Personnes et acteurs`, `Chansons rattachées`, `Concepts récurrents`, `Motifs et chaînes relationnelles` ;
- le manifeste `chapters/master_docs.json` ;
- les exports générés disponibles localement sous `exports/generated/`.

Limites de méthode :

- l'audit ne reconstruit pas les documents maîtres ;
- il ne vérifie pas que chaque passage rédactionnel du document maître est relié à un atome précis ;
- il ne vérifie pas l'exhaustivité des atomes listés, car les documents maîtres présentent des listes sélectionnées et des indicateurs de volumétrie ;
- il ne tranche pas les statuts de citations `candidate`, `à vérifier` ou équivalents ;
- il ne transforme pas les exports générés en preuves rédactionnelles autonomes ;
- il distingue le rattachement explicite visible dans le document maître du rattachement technique implicite par le pipeline de génération.

Niveaux utilisés :

- élevé : sources, atomes, registres et exports explicitement reliés de manière exploitable, avec granularité suffisante ;
- moyen : rattachement visible au niveau du document et des sections, mais granularité passage-par-passage insuffisante ;
- faible : rattachement partiel ou lacunaire sur plusieurs familles d'objets ;
- non vérifiable : absence d'élément exploitable dans le périmètre audité.

# Audit par document maître

## Chapitre 1

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/01/document_maitre.md` | 48 lignes de sources listées section 4. | 310 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 15 ; personnes : 24 ; chansons : 1 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Traçabilité forte au niveau des sections, mais pas de lien passage -> atome/export. 2 atomes affichent une source vide. Le comptage inclut S86, source à 0 atome mais 3 citations. |

## Chapitre 2

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/02/document_maitre.md` | 33 lignes de sources listées section 4. | 522 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 40 ; personnes : 34 ; chansons : 10 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Rattachement documentaire riche, mais 13 atomes affichent une source vide. Le comptage inclut S53 et S87, sources à 0 atome mais 1 citation chacune. |

## Chapitre 3

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/03/document_maitre.md` | 42 lignes de sources listées section 4. | 471 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 25 ; personnes : 33 ; chansons : 27 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Les familles d'objets sont visibles. 5 atomes affichent une source vide. Le comptage inclut S86, source à 0 atome mais 2 citations. |

## Chapitre 4

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/04/document_maitre.md` | 36 lignes de sources listées section 4. | 387 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 63 ; personnes : 53 ; chansons : 36 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Très bonne exposition des citations et registres rattachés, mais 2 atomes affichent une source vide et l'audit ne peut pas vérifier une traçabilité complète phrase par phrase. |

## Chapitre 5

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/05/document_maitre.md` | 35 lignes de sources listées section 4. | 431 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 44 ; personnes : 49 ; chansons : 11 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Les liens vers sources et registres sont visibles. 2 atomes affichent une source vide. Le comptage inclut S86 et S87, sources à 0 atome mais porteuses de citations. |

## Chapitre 6

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/06/document_maitre.md` | 35 lignes de sources listées section 4. | 572 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 47 ; personnes : 53 ; chansons : 33 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | La couverture par objets est solide. 3 atomes affichent une source vide ; la traçabilité export -> section du DM demeure globale et non directement pointée. |

## Chapitre 7

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/07/document_maitre.md` | 27 lignes de sources listées section 4. | 184 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 17 ; personnes : 23 ; chansons : 18 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Le DM expose les familles d'objets nécessaires. 1 atome affiche une source vide et plusieurs citations sont candidates ou à vérifier. |

## Chapitre 8

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/08/document_maitre.md` | 30 lignes de sources listées section 4. | 344 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 36 ; personnes : 40 ; chansons : 11 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Les sources et registres sont identifiables. 3 atomes affichent une source vide ; la preuve de rattachement reste principalement sectionnelle et non passage-par-passage. |

## Chapitre 9

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/09/document_maitre.md` | 22 lignes de sources listées section 4. | 220 atomes déclarés ; 37 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 3 ; personnes : 14 ; chansons : 4 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Périmètre documentaire plus compact, donc plus lisible. 2 atomes affichent une source vide ; le niveau reste moyen faute de liens directs entre passages rédigés et atomes/exports. |

## Chapitre 10

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/10/document_maitre.md` | 37 lignes de sources listées section 4. | 351 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 29 ; personnes : 56 ; chansons : 14 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Les objets sont bien exposés. 2 atomes affichent une source vide ; plusieurs citations restent candidates ou à vérifier. |

## Chapitre 11

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/11/document_maitre.md` | 38 lignes de sources listées section 4. | 391 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 17 ; personnes : 29 ; chansons : 34 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Les sections de registres et d'atomes sont exploitables pour un audit humain. 2 atomes affichent une source vide ; la dérivabilité fine des formulations n'est pas démontrée par le DM seul. |

## Chapitre 12

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/12/document_maitre.md` | 31 lignes de sources listées section 4. | 447 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 63 ; personnes : 51 ; chansons : 18 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Chapitre sensible du point de vue documentaire : 6 atomes affichent une source vide et l'audit ne peut pas conclure à une traçabilité élevée sans liens directs passage -> source/atome. |

## Chapitre 13

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/13/document_maitre.md` | 34 lignes de sources listées section 4. | 196 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 31 ; personnes : 53 ; chansons : 13 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Le rattachement thématique est lisible. 1 atome affiche une source vide ; le niveau reste moyen en raison d'une granularité insuffisante pour relier chaque affirmation à son export ou atome. |

## Chapitre 14

| DM | Sources identifiées | Atomes identifiés | Registres identifiés | Exports identifiés | Niveau de traçabilité | Observations |
|----|----|----|----|----|----|----|
| `chapters/14/document_maitre.md` | 72 lignes de sources listées section 4. | 1323 atomes déclarés ; 60 critiques/majeurs affichés ; autres atomes utiles listés. | Chronologie : 138 ; personnes : 161 ; chansons : 34 ; concepts et motifs présents. | `master_docs_index.json` confirme atomes, citations, chronologie, personnes et chansons ; exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts`, `motifs`. | moyen | Chapitre très volumineux : 4 atomes affichent une source vide et le DM ne fournit pas une table complète de rattachement passage -> source -> atome -> export. |

# Synthèse globale

## Forces observées

- Les 14 documents maîtres possèdent un bloc YAML indiquant `source_generation: "tools/build_master_docs.py"`, `statut: genere` et une même date de génération.
- Les 14 documents maîtres sont déclarés dans `chapters/master_docs.json`.
- Chaque document maître contient une section `Sources mobilisées` avec un nombre de sources et des lignes source par source.
- Chaque document maître contient un tableau de bord documentaire avec volumétrie d'atomes, citations, chronologie, personnes, chansons et sources mobilisées.
- Les sections d'atomes critiques ou majeurs donnent des identifiants d'atomes, des sources, des types, des importances et des niveaux de preuve.
- Les sections de registres rattachés sont présentes dans tous les documents maîtres : chronologie, personnes, chansons, concepts, motifs et relations.
- `exports/generated/master_docs_index.json` reflète les 14 chapitres et reprend les volumétriques principales.
- Les exports globaux `atoms`, `sources`, `quotes`, `chronology`, `people`, `songs`, `concepts` et `motifs` fournissent un point d'appui pour de futurs audits plus outillés.

## Faiblesses observées

- Aucun document maître ne fournit une table explicite passage -> source -> atome -> registre -> export.
- La traçabilité est surtout sectionnelle : elle relie le document maître à des familles d'objets, mais pas chaque affirmation à une preuve précise.
- Les listes d'atomes affichées sont sélectionnées ; elles ne suffisent pas à vérifier l'ensemble des atomes déclarés dans la volumétrie.
- Les exports sont associés par le pipeline et par les volumétriques, mais le document maître ne cite pas directement, pour chaque section, le fichier export utilisé.
- Des atomes affichent une source vide dans tous les chapitres inspectés, avec une intensité variable selon les chapitres.
- Les documents maîtres signalent eux-mêmes une limite récurrente : vérifier les atomes anciens encore incomplets au regard du schéma v2.
- Les citations possèdent souvent un statut explicite `candidate`, `à vérifier`, `a_verifier` ou équivalent ; ce n'est pas une anomalie de statut, mais cela limite la réutilisation sans vérification.
- Les liens interchapitres sont mentionnés comme point de vigilance, mais ils ne sont pas audités ici.

## Défaillances M1 rencontrées

| Défaillance M1 | Observation | Portée | Bloquant pour poursuivre M1 ? |
| --- | --- | --- | --- |
| Traçabilité | Absence de table explicite reliant chaque passage du document maître à ses sources, atomes, registres et exports. | Tous les documents maîtres. | Non, mais cela empêche de qualifier la traçabilité comme élevée. |
| Traçabilité | Présence d'atomes affichant `Source :  ;`, donc source non exposée dans le DM pour ces entrées. | Observé dans les 14 documents maîtres, avec un nombre variable d'occurrences. | Non pour l'audit pilote, mais à traiter avant un audit de traçabilité fin. |
| Traçabilité | Rattachement aux exports implicite par le pipeline et les volumétriques, sans lien sectionnel direct vers les fichiers export. | Tous les documents maîtres. | Non, mais limite la vérification export -> DM. |

Défaillances non retenues dans cet audit :

- dérivabilité : non auditée ici, car l'audit ne reconstruit pas les informations depuis le corpus exporté ;
- obsolescence : non observée dans le périmètre, car aucune comparaison temporelle ou régénération n'a été effectuée ;
- cohérence documentaire : non observée dans le périmètre, car l'audit ne compare pas les contenus entre registres, exports et DM ;
- statut documentaire : non retenue comme défaillance, car les documents maîtres indiquent leur statut généré et les citations candidates ou à vérifier sont explicitement qualifiées.

# Recommandations

Les recommandations sont strictement documentaires.

- Ajouter ultérieurement une annexe de traçabilité par document maître, sans modifier les documents maîtres existants dans cette PR.
- Définir un format de rattachement DM -> atomes permettant d'identifier les atomes supportant chaque grande section du document maître.
- Documenter explicitement les exports attendus pour l'audit DM -> exports, notamment `atoms.json`, `sources.json`, `quotes.json`, `chronology.json`, `people.json`, `songs.json`, `concepts.json` et `motifs.json`.
- Qualifier les atomes affichant une source vide dans un audit dédié, sans correction manuelle des documents maîtres générés.
- Définir une règle documentaire pour distinguer les citations candidates, les citations vérifiées et les citations simplement disponibles.
- Préparer une grille de lecture permettant de distinguer trace globale, trace sectionnelle et trace passage-par-passage.

Ces recommandations ne créent aucun script, aucune application, aucun formulaire, aucune automatisation lourde, aucun chantier Cloudflare et aucun chantier M2.

# Conclusion

Le modèle M1 de traçabilité des documents maîtres est partiellement applicable.

Il est applicable au niveau du document maître comme objet : les 14 documents possèdent un manifeste, un statut généré, des sources mobilisées, des atomes déclarés, des registres rattachés, des volumétriques et un index généré correspondant.

Il n'est pas encore pleinement applicable au niveau fin attendu par M1 : l'audit ne peut pas relier chaque passage du document maître à des sources, atomes, registres et exports précis sans créer une couche documentaire supplémentaire ou un futur contrôle dédié.

La conclusion pilote est donc la suivante : le socle actuel permet un audit humain de traçabilité de niveau moyen, mais il ne suffit pas encore pour une traçabilité élevée ni pour un contrôle automatisé fiable.
