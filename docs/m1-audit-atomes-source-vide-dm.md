# Audit M1 — Atomes à source vide dans les documents maîtres

# Objet de l'audit

Cet audit traite la seule défaillance M1 effectivement démontrée par l'audit pilote de traçabilité des documents maîtres : des atomes affichent `Source :  ;` dans les documents maîtres.

L'audit pilote concluait à une traçabilité moyenne des documents maîtres. Il ne démontrait pas l'existence d'informations non traçables passage par passage, mais il établissait une défaillance observable : certaines entrées d'atomes ne présentent pas de source dans la vue générée.

Ce document ne corrige pas cette défaillance. Il cherche uniquement à identifier les occurrences, les atomes concernés, la source éventuellement retrouvable et l'origine probable de l'écart.

# Périmètre

Le périmètre est strictement limité à :

- `chapters/*/document_maitre.md` ;
- les occurrences d'atomes affichant `Source :  ;` ;
- les exports ou fichiers d'entrée nécessaires pour comprendre l'origine de cette source vide.

Les fichiers consultés sont :

- les 14 documents maîtres `chapters/*/document_maitre.md` ;
- `exports/generated/atoms.json` ;
- `exports/generated/sources.json` ;
- `sources/morris_record_play_pause/source_part_06.md` ;
- `tools/build_master_docs.py`, uniquement pour comprendre quel champ est affiché.

L'audit ne modifie aucun document maître, aucun atome, aucun registre, aucun export, aucun générateur et aucune roadmap.

# Méthode

Les occurrences sont repérées par recherche exacte de la chaîne `Source :  ;` dans les documents maîtres.

Pour chaque occurrence, l'audit relève :

- le chapitre ;
- le chemin du document maître ;
- l'identifiant de l'atome ;
- le titre de l'atome ;
- la ligne de l'atome et la section concernée lorsque possible ;
- la source affichée dans le document maître ;
- la source disponible dans les exports ou fichiers d'origine si elle est vérifiable ;
- l'origine probable de l'écart.

La source retrouvée est considérée comme vérifiable uniquement lorsqu'elle apparaît dans un fichier inspecté. Pour les 17 atomes uniques concernés, `exports/generated/atoms.json` contient l'atome mais ne contient pas `data.source_id`. En revanche, `sources/morris_record_play_pause/source_part_06.md` porte une métadonnée de fichier `source_id: S35` et `source_label: "S35 — Morris, Record Play Pause, 2019"`. `exports/generated/sources.json` contient également l'entrée S35 et référence `sources/morris_record_play_pause/source_part_06.md`.

La fonction d'affichage des atomes dans `tools/build_master_docs.py` utilise le champ `data.source_id` de l'atome exporté. Ce constat explique pourquoi une absence de `source_id` dans `atoms.json` peut produire un affichage vide dans le document maître.

# Tableau d'audit

| Chapitre | Document maître | Atome | Titre | Source affichée | Source retrouvée | Origine probable | Gravité | Action recommandée |
|----------|-----------------|-------|-------|-----------------|------------------|-------------------|---------|--------------------|
| 01 | `chapters/01/document_maitre.md` | S35-A092, section atomes critiques, ligne 118 | Émotions non dites : Warsaw comme décharge générationnelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | `source_id` absent de l'atome exporté ; source présente au niveau du fichier `source_part_06.md`. | majeur | Ouvrir ensuite une correction ciblée de provenance S35, sans correction manuelle du DM. |
| 01 | `chapters/01/document_maitre.md` | S35-A097, section atomes critiques, ligne 120 | T. J. Davidson's : froid, piss tins et séparation Hook / Sumner | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Même origine probable : champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A086, section atomes critiques, ligne 117 | Drummer and Driver : Morris entre par la voiture autant que par la batterie | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | `source_id` absent de l'atome exporté ; source présente au niveau du fichier `source_part_06.md`. | majeur | Ouvrir ensuite une correction ciblée de provenance S35. |
| 02 | `chapters/02/document_maitre.md` | S35-A088, section atomes critiques, ligne 119 | Record Mirror / Rafters : la critique rock conduit Morris vers Rob Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A089, section atomes critiques, ligne 121 | Eric's Liverpool : première scène de Morris et découverte d'Ian frontman | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A090, section atomes critiques, ligne 123 | Rafters / Fast Breeder : guerre de rang et naissance différée du manager Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A091, section atomes critiques, ligne 125 | "Living in the Ice Age" : écrire sans savoir, par intuition collective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A092, section atomes critiques, ligne 127 | Émotions non dites : Warsaw comme décharge générationnelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A093, section atomes critiques, ligne 129 | Middlesbrough Rock Garden : archive live et performance invisible à l'image | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A094, section atomes critiques, ligne 131 | Electric Circus / Rudolph Hess : provocation improvisée et futur piège mémoriel | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A097, section atomes critiques, ligne 133 | T. J. Davidson's : froid, piss tins et séparation Hook / Sumner | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A102, section atomes critiques, ligne 135 | Londres et le disque : deux objectifs DIY, Ian moteur mais démocratie réelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A087, section autres atomes utiles, ligne 302 | Strangeways : rencontre Hook / Sumner et sociologie ordinaire du groupe | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A098, section autres atomes utiles, ligne 304 | "Girlfriends" : concurrence entre groupe et vie affective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 02 | `chapters/02/document_maitre.md` | S35-A101, section autres atomes utiles, ligne 306 | Ivy Lane : verrouiller les portes, punir par les drums | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | mineur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 03 | `chapters/03/document_maitre.md` | S35-A091, section atomes critiques, ligne 130 | "Living in the Ice Age" : écrire sans savoir, par intuition collective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 03 | `chapters/03/document_maitre.md` | S35-A095, section atomes critiques, ligne 132 | Morris théorise la section rythmique : pont, moteur, cœur battant | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 03 | `chapters/03/document_maitre.md` | S35-A096, section atomes critiques, ligne 134 | "Fast dancey" et "jungly tom" : consignes pauvres, formes durables | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 03 | `chapters/03/document_maitre.md` | S35-A097, section atomes critiques, ligne 136 | T. J. Davidson's : froid, piss tins et séparation Hook / Sumner | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 03 | `chapters/03/document_maitre.md` | S35-A101, section autres atomes utiles, ligne 357 | Ivy Lane : verrouiller les portes, punir par les drums | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | mineur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 04 | `chapters/04/document_maitre.md` | S35-A089, section atomes critiques, ligne 84 | Eric's Liverpool : première scène de Morris et découverte d'Ian frontman | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 04 | `chapters/04/document_maitre.md` | S35-A091, section atomes critiques, ligne 86 | "Living in the Ice Age" : écrire sans savoir, par intuition collective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 05 | `chapters/05/document_maitre.md` | S35-A094, section atomes critiques, ligne 79 | Electric Circus / Rudolph Hess : provocation improvisée et futur piège mémoriel | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 05 | `chapters/05/document_maitre.md` | S35-A102, section atomes critiques, ligne 81 | Londres et le disque : deux objectifs DIY, Ian moteur mais démocratie réelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 06 | `chapters/06/document_maitre.md` | S35-A090, section atomes critiques, ligne 95 | Rafters / Fast Breeder : guerre de rang et naissance différée du manager Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 06 | `chapters/06/document_maitre.md` | S35-A095, section atomes critiques, ligne 97 | Morris théorise la section rythmique : pont, moteur, cœur battant | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 06 | `chapters/06/document_maitre.md` | S35-A096, section atomes critiques, ligne 99 | "Fast dancey" et "jungly tom" : consignes pauvres, formes durables | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 07 | `chapters/07/document_maitre.md` | S35-A095, section atomes critiques, ligne 95 | Morris théorise la section rythmique : pont, moteur, cœur battant | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 08 | `chapters/08/document_maitre.md` | S35-A086, section atomes critiques, ligne 96 | Drummer and Driver : Morris entre par la voiture autant que par la batterie | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 08 | `chapters/08/document_maitre.md` | S35-A093, section atomes critiques, ligne 98 | Middlesbrough Rock Garden : archive live et performance invisible à l'image | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 08 | `chapters/08/document_maitre.md` | S35-A102, section atomes critiques, ligne 100 | Londres et le disque : deux objectifs DIY, Ian moteur mais démocratie réelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 09 | `chapters/09/document_maitre.md` | S35-A088, section atomes critiques, ligne 66 | Record Mirror / Rafters : la critique rock conduit Morris vers Rob Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 09 | `chapters/09/document_maitre.md` | S35-A090, section atomes critiques, ligne 68 | Rafters / Fast Breeder : guerre de rang et naissance différée du manager Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 10 | `chapters/10/document_maitre.md` | S35-A099, section atomes critiques, ligne 85 | Rafters / Yachts : crise de Stephanie et vie de groupe sans filet | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 10 | `chapters/10/document_maitre.md` | S35-A098, section autres atomes utiles, ligne 226 | "Girlfriends" : concurrence entre groupe et vie affective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 11 | `chapters/11/document_maitre.md` | S35-A092, section atomes critiques, ligne 102 | Émotions non dites : Warsaw comme décharge générationnelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 11 | `chapters/11/document_maitre.md` | S35-A094, section atomes critiques, ligne 104 | Electric Circus / Rudolph Hess : provocation improvisée et futur piège mémoriel | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A089, section atomes critiques, ligne 87 | Eric's Liverpool : première scène de Morris et découverte d'Ian frontman | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A092, section atomes critiques, ligne 89 | Émotions non dites : Warsaw comme décharge générationnelle | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A099, section atomes critiques, ligne 91 | Rafters / Yachts : crise de Stephanie et vie de groupe sans filet | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A100, section atomes critiques, ligne 93 | Antidépresseurs, substances et humeur : Morris introduit une prudence clinique | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A098, section autres atomes utiles, ligne 216 | "Girlfriends" : concurrence entre groupe et vie affective | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 12 | `chapters/12/document_maitre.md` | S35-A101, section autres atomes utiles, ligne 218 | Ivy Lane : verrouiller les portes, punir par les drums | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | mineur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 13 | `chapters/13/document_maitre.md` | S35-A097, section atomes critiques, ligne 100 | T. J. Davidson's : froid, piss tins et séparation Hook / Sumner | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 14 | `chapters/14/document_maitre.md` | S35-A088, section atomes critiques, ligne 182 | Record Mirror / Rafters : la critique rock conduit Morris vers Rob Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 14 | `chapters/14/document_maitre.md` | S35-A090, section atomes critiques, ligne 184 | Rafters / Fast Breeder : guerre de rang et naissance différée du manager Gretton | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 14 | `chapters/14/document_maitre.md` | S35-A093, section atomes critiques, ligne 186 | Middlesbrough Rock Garden : archive live et performance invisible à l'image | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |
| 14 | `chapters/14/document_maitre.md` | S35-A094, section atomes critiques, ligne 188 | Electric Circus / Rudolph Hess : provocation improvisée et futur piège mémoriel | Vide : `Source :  ;` | S35 — Morris, Record Play Pause, 2019 | Champ atomique `source_id` absent, source portée par la métadonnée de fichier. | majeur | Corriger la provenance atomique ou son héritage dans une PR dédiée. |

# Analyse

## 1. Source absente dans l'atome d'origine

Hypothèse partiellement confirmée.

Dans `sources/morris_record_play_pause/source_part_06.md`, les blocs YAML des 17 atomes concernés ne contiennent pas de champ `source_id`. En ce sens, la source est absente du bloc atomique d'origine.

La source n'est toutefois pas absente du fichier d'origine : le même fichier porte en en-tête `source_id: S35` et `source_label: "S35 — Morris, Record Play Pause, 2019"`. Il faut donc distinguer l'absence dans l'atome lui-même et la présence au niveau de la source part.

## 2. Source présente dans l'atome mais perdue dans l'export

Hypothèse non démontrée.

L'audit ne trouve pas de `source_id` dans les blocs atomiques concernés. `exports/generated/atoms.json` ne contient pas non plus `data.source_id` pour ces 17 atomes. Il n'y a donc pas de preuve que le champ était présent dans l'atome puis perdu à l'export.

## 3. Source présente dans l'export mais perdue dans `tools/build_master_docs.py`

Hypothèse écartée pour les occurrences observées.

`exports/generated/atoms.json` ne contient pas `data.source_id` pour les atomes S35-A086 à S35-A102 concernés. `tools/build_master_docs.py` affiche la source à partir du champ `data.source_id`. Le générateur affiche donc un vide parce que l'export ne fournit pas le champ attendu.

## 4. Affichage vide lié à un cas ancien ou incomplet du schéma v2

Hypothèse probable.

Les atomes concernés sont regroupés dans une même passe documentaire : `sources/morris_record_play_pause/source_part_06.md`. Cette passe porte la source au niveau du fichier, mais pas dans chaque bloc atomique. Le cas ressemble donc à un héritage de métadonnée de source non propagé vers les atomes ou à un schéma atomique incomplet pour cette passe.

Cette hypothèse reste à confirmer dans une PR de correction ciblée, qui devra décider si la correction porte sur les données atomiques, sur l'héritage de métadonnées lors de l'export, ou sur une règle de génération.

## 5. Faux positif

Hypothèse non retenue.

Les 48 occurrences affichent réellement `Source :  ;` dans les documents maîtres. Le problème est visible dans les vues générées. La source S35 est retrouvable ailleurs, mais elle n'est pas affichée dans les entrées d'atomes concernées.

# Synthèse

- Nombre total d'occurrences : 48.
- Chapitres concernés : 14 chapitres, de `chapters/01/document_maitre.md` à `chapters/14/document_maitre.md`.
- Atomes concernés : 17 atomes uniques, tous issus de la série S35-A086 à S35-A102.
- Source retrouvée : S35 — Morris, Record Play Pause, 2019.
- Fichier source concerné : `sources/morris_record_play_pause/source_part_06.md`.
- Cause probable principale : source présente comme métadonnée de fichier, mais absente du bloc atomique et du champ `data.source_id` dans `exports/generated/atoms.json`.
- Gravité globale : majeure, car la défaillance touche des atomes souvent critiques et se propage dans tous les documents maîtres ; non bloquante, car la source est retrouvable sans ambiguïté au niveau du fichier source et de `exports/generated/sources.json`.
- Caractère bloquant pour la suite de M1 : non bloquant, mais une correction ciblée est recommandée avant d'élever le niveau de traçabilité des documents maîtres.

# Recommandations

Les recommandations sont limitées à la suite M1.

- Ouvrir une PR de correction ciblée après cet audit.
- Ne pas corriger manuellement les documents maîtres.
- Ne pas modifier manuellement les exports générés.
- Vérifier si la correction doit porter sur les blocs atomiques S35-A086 à S35-A102, sur l'héritage de `source_id` depuis la source part, ou sur une règle de génération.
- Régénérer les artefacts uniquement dans une PR dédiée si la correction retenue l'exige.
- Ajouter dans cette future PR une vérification que les documents maîtres n'affichent plus `Source :  ;` pour ces atomes.

Cette PR d'audit ne modifie pas les documents maîtres, les atomes, les exports ni `tools/build_master_docs.py`.

# Conclusion

La défaillance vient plutôt d'un problème de provenance dans les données atomiques exportées ou d'un héritage incomplet de métadonnées depuis le fichier source vers les atomes.

Elle ne semble pas venir directement de `tools/build_master_docs.py` : le générateur affiche le champ `data.source_id` qu'il reçoit, et ce champ est absent de `exports/generated/atoms.json` pour les atomes concernés.

Elle ne semble pas être une perte entre l'export et le document maître : la source n'est pas présente dans l'export atomique.

Une PR de correction ciblée devrait être ouverte ensuite pour restaurer ou propager `source_id: S35` sur les atomes S35-A086 à S35-A102 concernés, puis régénérer les artefacts avec les outils canoniques si le périmètre de cette future PR le prévoit.

Cette défaillance ne bloque pas la poursuite de M1. Elle doit toutefois être traitée avant de qualifier la traçabilité des documents maîtres au niveau élevé.
