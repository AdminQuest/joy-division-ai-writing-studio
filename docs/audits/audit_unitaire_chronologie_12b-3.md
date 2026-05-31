# Audit unitaire — registre chronologie (préalable à l'étape 6 — refonte)

> Audit **strictement diagnostic**, première brique de l'étape 6 (refonte de la
> chronologie, registre fondateur). **Lecture seule** : aucun renommage d'ID,
> aucune écriture de `same_as`, aucun changement de schéma, aucune édition de
> donnée. On inventorie l'existant et on remonte les arbitrages.
>
> Date : 31/05/2026.
> Périmètre : `registers/chronology/**/*.md` (lus comme le runtime
> `apps/lib/dynamic-registers.js`) + `apps/chronology-register/`.
> Doctrine : `docs/specs/cross_registres.md`, `docs/NAMING_CONVENTIONS.md` §10.
> Décisions de cadrage appliquées comme grille de lecture :
> **(a)** identifiant `EVENT-<SLUG>` sémantique, source-agnostique, **sans date dans l'ID** (la date est un champ) ;
> **(b)** la chronologie est réservée aux **événements-JALONS** ; la date d'un concert ordinaire reste un attribut, pas un `EVENT`.

---

## A. Localisation

| Élément | Chemin |
|---|---|
| Données | `registers/chronology/*.md` (62 fichiers Markdown, blocs YAML embarqués) |
| Application | `apps/chronology-register/` (`app.js`, `index.html`, `style.css`) |
| Chargement runtime | `apps/lib/dynamic-registers.js` — `loadRecords({ prefixes:['registers/chronology/', …], kinds:['chronology'] })` |
| Gabarit de référence | `registers/chronology/master_chronology.md` (`schema: chronology_template`) |

Le runtime n'a **aucun validateur dédié** (rien d'équivalent à
`tools/validate_places.py`). Le rendu est tolérant : `app.js` lit
`data.event || data.evenement`, `data.certainty || data.statut`, et trie par
`date.localeCompare(numeric)`. **Il ne lit pas `label`** (cf. §F).

---

## B. Inventaire général

| Mesure | Valeur |
|---|---:|
| Fichiers de données | 62 |
| Entrées-événements (lignes `id:` d'événement) | **500** |
| En-têtes d'unité v2 (`CHRONO-…-V2`, non-événements) | 8 |
| Identifiants d'événement distincts (après dédup par chaîne) | 500 (aucune collision exacte) |

### Manuelles anciennes vs atomisées v2

| Famille | Fichiers | Événements | Forme d'ID | Champ-texte / atomes | Précision |
|---|---:|---:|---|---|---|
| **Atomisées v2** (`*_v2.md` : S02, S05, S06, S10×2, S12, S20, S69) | 8 | **80** | `CHR-Sxx-NNN` (positionnel, source-scopé) + en-tête `CHRONO-…-V2` | `event` / `related_atoms` | `precision_date` présent |
| **Maître** (`master_chronology.md`) | 1 | 10 | `CHR-YYYY-NNN` (**source-agnostique**, année+positionnel) | `event` / `related_atoms` | `precision_date` présent |
| **S76 — Torn Apart** | 17 | 101 | `CHR-S76-YYYY-NNN` (année+positionnel) | `event` / `related_atoms` | `precision_date` (vocab libre, cf. §D) |
| **S75 — Ott** | 3 | 31 | `CHR-S75-YYYY-NNN` | `event` / `related_atoms` | `precision_date` présent |
| **S34 — Fraser & Fuoto** | 1 | 6 | `CHR-S34-YYYY-NNN` (`type_unite: chronology_event`) | `event` / `related_atoms` | `precision_date` présent |
| **S29 — Goddard** | 1 | 4 | `CHR-S29-YYYY-NNN` (`chronology_event`) | `event` / `related_atoms` | `precision_date` présent |
| **S35 — Morris** | 3 | 17 | `CHR-S35-Pnn-YYYY-NNN` (part+année+positionnel) | **`label`** / **`atoms`** | **absent** |
| **S41 — Hook** | 19 | **182** | `CHR-S41-[TLn-]YYYY[-MM[-DD]]-SLUG` (**date encodée + slug**) | **`evenement`** / **`atomes_lies`** | **absent** |
| **S45 — Curtis** | 9 | 69 | `CHR-S45-YYYY[-MM[-DD]]-SLUG` (**date encodée + slug**) | **`evenement`** / **`atomes_lies`** | **absent** |

Lecture : la moitié du volume (S41+S45 = 251 entrées, 50 %) suit une convention
**date-dans-l'ID + champs francophones minimaux** ; l'autre moitié se répartit
entre la convention v2 propre, le maître source-agnostique, et trois variantes
positionnelles (S76/S75/S34/S29/S35).

---

## C. Identifiants

### C.1. Combien de conventions coexistent ? — **six**

| # | Convention | Exemple | Familles | Date dans l'ID ? | Source dans l'ID ? |
|---|---|---|---|---|---|
| 1 | Source-agnostique année+positionnel | `CHR-1980-003` | maître | **oui (année)** | non |
| 2 | v2 positionnel source-scopé | `CHR-S02-001` | S02,S05,S06,S10,S12,S20,S69 | non | oui |
| 3 | Source-scopé année+positionnel | `CHR-S76-1956-001` | S76, S75, S34, S29 | **oui (année)** | oui |
| 4 | Source-scopé part+année+positionnel | `CHR-S35-P03-1969-001` | S35 | **oui (année)** | oui |
| 5 | Source-scopé **date complète + slug** | `CHR-S41-1977-05-29-WARSAW-FIRST-GIG-ELECTRIC-CIRCUS` | S41, S45 | **oui (jusqu'au jour)** | oui |
| 6 | En-tête d'unité v2 (espace de noms `CHRONO-`) | `CHRONO-S02-…-V2` | 8 v2 | non | oui |

À quoi s'ajoute le préfixe `TL` (timeline) interne à S41 (`CHR-S41-TL2-…`,
`CHR-S41-TL3-…`, 33 ID) — sous-convention de la convention 5.

### C.2. IDs encodant une date — non conformes à la décision (a)

| Granularité encodée dans l'ID | Nombre |
|---|---:|
| Jour (`…-YYYY-MM-DD-…`) | 95 |
| Mois (`…-YYYY-MM-…`) | 67 |
| Au moins l'année | **454 / 500** |
| Aucune date dans l'ID | 46 (v2 positionnels S02/S05/S06/S20/S69 + le singleton `…-VOTE-CONSERVATEUR`) |

> Constat structurant : **454 ID sur 500 (91 %) encodent au moins l'année**, et
> 162 encodent le mois ou le jour. La décision (a) impose un ID **sans date**.
> Aucune des six conventions n'est conforme : même la plus propre (v2) reste
> source-scopée et positionnelle, sans slug sémantique. Le futur `EVENT-<SLUG>`
> est donc une **forme canonique entièrement nouvelle** ; la migration se fera,
> comme pour les lieux, par **`same_as` additif sans renommage** (gel des schémas,
> `cross_registres.md` §2.2).

### C.3. Doublons & quasi-doublons (mêmes événements sous IDs différents)

La chronologie est **partitionnée par source** : S41, S45, S75, S76 et le maître
narrent chacun la même histoire du groupe. Le même fait réel apparaît donc sous
plusieurs ID source-scopés → **candidats `same_as`**. Le runtime ne fusionnant
sur rien, ces entrées produisent aujourd'hui des doublons d'affichage.

Clusters confirmés (par recoupement date + texte) :

| Cluster (fait réel) | Date | IDs concernés | Sources |
|---|---|---|---|
| Naissance de Ian Curtis | 1956-07-15 | `CHR-1956-001` · `CHR-S76-1956-001` | maître, S76 |
| **Premier concert Warsaw, Electric Circus** | 1977-05-29 | `CHR-S41-1977-05-29-WARSAW-FIRST-GIG-ELECTRIC-CIRCUS` · `CHR-S41-TL2-1977-05-29-FIRST-WARSAW-GIG-REVIEW` · `CHR-S45-1977-05-29-WARSAW-ELECTRIC-CIRCUS` · (S10 v2, S76 p03) | S41 (×2 !), S45, S10, S76 |
| Dernier concert, Birmingham High Hall | 1980-05-02 | `CHR-1980-002` · `CHR-S41-1980-05-02-BIRMINGHAM-HIGH-HALL-LAST-GIG` · `CHR-S45-1980-05-02-BIRMINGHAM-FINAL-GIG` · (S75, S76 p17) | maître, S41, S45, S75, S76 |
| Mort de Ian Curtis | 1980-05-18 | `CHR-1980-003` · `CHR-S41-1980-05-18-CURTIS-SUICIDE` · (S75, S76 p17) | maître, S41, S75, S76 |
| Sortie *Unknown Pleasures* (FACT 10) | 1979-06-14 | `CHR-1979-002` · `CHR-S41-1979-06-14-UP-FACT10-RELEASE` · (S75) | maître, S41, S75 |
| Sortie *Closer* (posthume) | 1980-07-18 | `CHR-1980-004` · `CHR-S41-1980-CLOSER-RELEASE-POSTHUMOUS` · (S45) | maître, S41, S45 |
| Arrivée de Stephen Morris | 1977-08 / 1977 | `CHR-S41-1977-08-STEVE-MORRIS-JOINS` · `CHR-S45-1977-STEPHEN-MORRIS-RECRUTEMENT` | S41, S45 — **dates divergentes** (cf. §F) |

**Quasi-doublon à NE PAS fusionner** (piège, analogue à `FREE-TRADE-HALL` vs
`LESSER-FREE-TRADE-HALL` de l'audit lieux) :

- Concert Sex Pistols au Lesser Free Trade Hall — **deux gigs distincts** :
  - `CHR-1976-001` (maître) = **4 juin 1976** (1er concert, daté `1976-06-04`) ;
  - `CHR-S45-1976-07-20-SEX-PISTOLS` + `CHR-S75-1976-002` = **20 juillet 1976**
    (2e concert, « second concert » explicite chez Ott).
  → S45 et S75 sont `same_as` **entre eux** (même 2e gig) ; ni l'un ni l'autre
    n'est `same_as` du maître. Le maître datant `1976-06-04` (1er gig) reste distinct.

**Duplication intra-source (S41)** : les fichiers `…timeline_two…` (TL2) et
`…timeline_three…` (TL3) ré-énoncent des événements déjà présents dans les
fichiers narratifs S41 (ex. premier concert Warsaw : TL2 *et*
`…warsaw_first_gigs…`). Doublons **à l'intérieur d'une même source** → à
réconcilier aussi.

### C.4. Mapping proposé vers `EVENT-<SLUG>` — **proposition, non appliquée**

Dérivation selon `NAMING_CONVENTIONS` §10.2.2 (repli ASCII, capitales,
non-alphanum → tiret, retrait des jetons de source/index/date) :

| Fait réel | Slug canonique proposé | Date (champ) | `same_as` à poser (legacy → canonique) |
|---|---|---|---|
| Naissance Ian Curtis | `EVENT-NAISSANCE-IAN-CURTIS` | 1956-07-15 | `CHR-1956-001`, `CHR-S76-1956-001` |
| Premier concert Warsaw, Electric Circus | `EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS` | 1977-05-29 | les 4-5 ID du cluster |
| Dernier concert, Birmingham | `EVENT-DERNIER-CONCERT-BIRMINGHAM` | 1980-05-02 | les ~5 ID du cluster |
| Mort de Ian Curtis | `EVENT-MORT-IAN-CURTIS` | 1980-05-18 | les ~4 ID du cluster |
| Sortie *Unknown Pleasures* | `EVENT-SORTIE-UNKNOWN-PLEASURES` | 1979-06-14 | les 3 ID du cluster |
| Sortie *Closer* | `EVENT-SORTIE-CLOSER` | 1980-07-18 | les 3 ID du cluster |
| 2e concert Sex Pistols, Lesser FTH | `EVENT-SEX-PISTOLS-LESSER-FTH-1976-07-20` (*) | 1976-07-20 | `CHR-S45-1976-07-20-SEX-PISTOLS`, `CHR-S75-1976-002` |

(*) qualificateur de désambiguïsation **à arbitrer** (cf. §Décisions — slugs ambigus).

---

## D. Dates

### D.1. Formats en présence

Deux registres de notation **cohabitent** : ISO (`YYYY`, `YYYY-MM`,
`YYYY-MM-DD`, intervalles `YYYY-MM-DD/YYYY-MM-DD`) et **prose française**
(`30 juillet 1977`, `janvier 1979`, `été 1977`, `années 1960`,
`seconde moitié du XXe siècle`). Le tri runtime (`localeCompare` numérique sur la
chaîne) mêle donc des clés ISO et des clés prose → ordre non fiable pour les
entrées prose.

### D.2. Distribution par précision (500 entrées, normalisée d'après la valeur `date:`)

| Catégorie | Nombre | Détail |
|---|---:|---|
| `jour` | **212** | 210 ISO `YYYY-MM-DD` + 2 prose (`30 juillet 1977`, `26 mai 1977`) |
| `annee` | **134** | `YYYY` |
| `mois` | **107** | 103 ISO `YYYY-MM` + 4 prose (`janvier 1979`, `avril 1978`…) |
| `intervalle` | **34** | 32 plages `…/…` (ex. `1980-05-17/1980-05-18`) + 2 `YYYY-YYYY` (`1881-1886`, `2013-2014`) |
| `circa` (décennie/vague) | **10** | `années 1960` (×2), `début des années 1970`, `milieu des années 1960`, `années 1990`, `années 2010`, `fin 1976`, `seconde moitié du XXe siècle`, `à préciser` |
| `saison` | **3** | `été 1977`, `été 1976`, `Noël 1978` |

> Note : la catégorie `circa` ci-dessus regroupe décennies + formulations vagues
> (la grille de cadrage à 6 termes n'a pas de bucket « décennie » distinct — **à
> arbitrer** si l'on veut le créer).

### D.3. Vocabulaire `precision_date` déclaré — incohérent et à normaliser

Le champ `precision_date` n'existe que sur **233 / 500 entrées** (les familles à
champs anglais). Il est **absent de S41, S45 (251 entrées) et S35 (17)** — pour
elles la précision n'est lisible que dans la chaîne `date:`. Là où il existe, il
compte **~40 valeurs distinctes**, mélangeant :

- termes FR : `annee` (59), `mois` (5), `periode` (5), `saison` (1), `decade` (5) ;
- termes EN : `exact` (79), `year` (5), `month` (4), `approximate` (18), `approx` (3), `range` (5), `spring`/`summer` ;
- **texte libre** (intégralement dans S76) : `overnight_session`, `during_Closer_sessions`,
  `before_Britannia_Row_sessions`, `after_1978-05-05`, `exact_or_same_night_after_gig`,
  `same_sequence_as_Gretton_rehearsal_entry`, `inferred_or_to_verify`, etc.

→ Aucun vocabulaire contrôlé. La refonte devra mapper vers un jeu fermé
(proposé : `jour | mois | saison | annee | circa | intervalle`).

### D.4. Cas problématiques

- **Date manquante / placeholder** : `s45_curtis_chronology_vote_conservateur.md`
  porte `date: à préciser` (entrée non datable en l'état).
- **Statuts « datation à préciser »** : ~20 entrées (surtout S45, S41) signalent
  en `statut`/`notes` que la date est incertaine — non bloquant mais à tracer.
- **Dates impossibles / intervalles incohérents** : **aucun** intervalle inversé
  détecté (18 plages au jour vérifiées, début ≤ fin). RAS sur ce point.
- **Dates hors période du groupe** (légitimes mais à classer, cf. §E) :
  `1881-1886` (S20, histoire du logement), `1962/1966` (S41, enfance Hook en
  Jamaïque), `2007` / `2017` / `années 1990` / `années 2010` / `2013-2014`
  (S29/S34 — réception critique posthume).

---

## E. Frontière jalon / date ordinaire

Application de la décision (b) : seuls les **jalons** ont vocation à devenir
`EVENT-`. Trois classes ressortent.

### E.1. JALONS (légitimes en chronologie)

Naissance/mort de Curtis ; formation et changements de nom (Stiff Kittens →
Warsaw → Joy Division) ; arrivée de Morris ; signature Factory ; sorties
discographiques (*A Factory Sample*, *Unknown Pleasures*, *Closer*, singles) ;
**premier** et **dernier** concert ; premier *fit* documenté ; suicide et
funérailles. Ce sont les ancres temporelles du graphe.

### E.2. Dates de concert ordinaires — candidates à **NE PAS** devenir `EVENT`

S41 et S45 contiennent une **dense liste de concerts datés** (Rafters,
Newcastle, le Squat, Eric's Liverpool, Middlesbrough Rock Garden, Salford
Technical College…). Exemples typiques :

- `CHR-S41-1977-05-31-RAFTERS-HEARTBREAKERS`
- `CHR-S41-1977-06-06-NEWCASTLE-SLEEPING-BAG`
- `CHR-S41-1977-08-27-ERICS-LIVERPOOL`
- `CHR-S41-1977-09-14-MIDDLESBROUGH-BOB-LAST`
- `CHR-S45-1977-08-10-BROTHERDALE-PANIK`

Ce sont des **dates de concert routinières** : leur place naturelle est le
**futur registre concerts (`CONCERT-`, étape 10)**, où la date sera un attribut
(`a_pour_date`). Elles ne devraient pas être promues en `EVENT-` individuels.
Volume indicatif : la majorité des 95 ID à granularité « jour » de S41/S45 sont
des gigs → **plusieurs dizaines d'entrées limites**.

### E.3. « Événements » de réception / lecture critique — statut à arbitrer

S29 (Goddard) et S34 (Fraser & Fuoto) encodent comme « événements » des
**interprétations critiques** (`certainty: interpretation_critique`),
ex. `CHR-S29-2017-001` (mort de Mark Fisher), `CHR-S34-2007-001` (documentaire
Grant Gee), `CHR-S34-1979-001` (*Unknown Pleasures* « comme forme spatiale »).
Ce ne sont **ni des jalons biographiques, ni des concerts** : repères de
réception posthume / lecture savante. À arbitrer : restent-ils dans la
chronologie, ou relèvent-ils d'un registre concepts/réception (étape 11) ?

---

## F. Qualité

### F.1. Contradictions version manuelle ↔ v2 (ou inter-sources) d'un même événement

- **Arrivée de Stephen Morris** : S41 date `1977-08` ; S45 date `1977`
  (bare year). Même fait, **précision/datation divergente** — à trancher à la
  réconciliation `same_as`.
- **Concert Sex Pistols au Lesser FTH** : risque de **fusion erronée** entre le
  4 juin (maître) et le 20 juillet (S45/S75) — cf. §C.3. À garder distincts.
- **Naissance Ian Curtis** : maître situe à *Old Trafford* ; S76 à *Basford
  House, Old Trafford* — pas une contradiction, mais granularité de lieu à
  unifier au moment du lien `a_pour_lieu`.
- Plusieurs entrées portent des `contradictions:` explicites internes (champ du
  gabarit), ex. `CHR-S76-1972-001` (« témoignage unique… date exacte à
  recouper ») — traçabilité présente, à exploiter.

### F.2. Champs manquants / hétérogènes

| Champ | Présent sur … / 500 | Familles déficientes |
|---|---:|---|
| `precision_date` | 233 | absent de **S41, S45, S35** (268 entrées) |
| `location` | 216 | absent de S41, S45, S35 (référents de lieu noyés dans le texte) |
| `people` | 182 | absent de S41, S45, S35 |
| `type` | 223 | absent de S41, S45, S35 |
| champ-texte | 500 | mais **3 noms** : `event` / `evenement` / `label` |
| atomes | 500 | **3 noms** : `related_atoms` / `atomes_lies` / `atoms` |
| certitude | 500 | **2 noms** : `certainty` / `statut` (et `statut` mêle datation + certitude) |

**Bug de rendu** : `app.js` lit `event||evenement` mais **pas `label`** → les
**17 entrées S35** s'affichent avec un texte d'événement vide. De même, le filtre
de recherche et l'export CSV ignorent `label`. (Constat ; correctif hors
périmètre de cet audit.)

`certainty` détourné : S29/S34 y mettent des valeurs non prévues par le gabarit
(`interpretation_critique`, `source_secondaire`) au lieu de `strong|medium|weak`.

---

## G. Cross-readiness (préparation au maillage `liens`)

### G.1. Champs de liaison — **absents partout**

| Champ | Occurrences |
|---|---:|
| `same_as` | **0** |
| `liens` | **0** |
| `reference_croisee` | **0** |

Aucune infrastructure de liaison n'est encore posée — conforme à
`cross_registres.md` (spécification de conception, implémentation par les
refontes). La couche d'identité (`same_as`) **et** la couche de relation
(`liens`) sont à câbler par cette refonte de l'étape 6. Selon la règle de
direction (§3.3 de la spec), l'`EVENT` est un **nœud fondateur** : peu/pas de
liens sortants ; ce sont les concerts/sessions qui pointeront vers lui
(`a_pour_date` → `ancre`).

### G.2. Références implicites en texte libre (futurs liens)

Les entités qui deviendront des cibles `<TYPE>-<SLUG>` sont aujourd'hui en
**texte libre** :

- **Lieux** (`location`, 216 occ. + nombreuses mentions noyées dans `event`/
  `evenement` pour S41/S45) : « Electric Circus », « Rafters », « Strawberry
  Studios », « Britannia Row »… → futurs `PLACE-` (`a_pour_lieu`, ét. 10).
- **Personnes** (`people`, 182 occ.) : « Ian Curtis », « Martin Hannett »,
  « Rob Gretton », « Tony Wilson »… → futurs `PERSON-` (ét. 8).
- **Organisations** (dans le texte) : « Factory Records », « RCA », « Granada
  Television »… → futurs `ORG-` (ét. 9).
- **Chansons** (`songs`, 22 occ.) : « Shadowplay », « Transmission », « Dead
  Souls »… → futurs `SONG-`.

Ces mentions sont exploitables comme amorces de liens, mais **non normalisées**
(libellés libres, accents, variantes) : leur résolution vers des identifiants
canoniques est un chantier de la refonte / du maillage (ét. 11).

---

## H. Synthèse

| Axe | État |
|---|---|
| Volume | 500 événements, 62 fichiers |
| Conventions d'ID | **6** coexistantes ; **91 % encodent une date** ⇒ toutes non conformes à la décision (a) |
| Doublons inter-sources | ≥ 7 clusters `same_as` confirmés + duplication intra-S41 (timelines) |
| Dates | 2 systèmes de notation (ISO / prose FR) ; `precision_date` absent sur 268 entrées, ~40 valeurs ailleurs |
| Jalon vs concert | dizaines de gigs S41/S45 = dates ordinaires (→ registre concerts, ét. 10) |
| Cross-readiness | `same_as`/`liens`/`reference_croisee` **= 0** ; références entièrement en texte libre |

---

## Décisions à arbitrer

*(rien n'est tranché ici — à valider avant toute écriture)*

### 1. Doublons à réconcilier par `same_as`

- Valider les **7 clusters** du §C.3 (naissance Curtis ; 1er concert Warsaw ;
  dernier concert Birmingham ; mort de Curtis ; sorties *UP* et *Closer* ;
  arrivée de Morris) comme arêtes `same_as` vers les slugs `EVENT-` proposés
  (§C.4).
- Trancher la **duplication intra-S41** (fichiers `timeline_two`/`timeline_three`
  vs fichiers narratifs) : `same_as` interne, ou choix d'un porteur canonique ?
- **Arrivée de Morris** : retenir `1977-08` (S41) ou `1977` (S45) comme date du
  fait fusionné ?

### 2. Entrées limites jalon / concert

- Confirmer la règle (b) : les **gigs ordinaires** S41/S45 (Rafters, Newcastle,
  Eric's, Middlesbrough…) **ne deviennent pas** des `EVENT-` et sont réservés au
  futur registre `CONCERT-` (étape 10). Quels gigs font exception (= jalons) :
  uniquement 1er et dernier concert, ou aussi les nuits Factory fondatrices ?
- Statut des **« événements » de réception critique** S29/S34 (docu Grant Gee
  2007, mort de Fisher 2017, lectures de *UP*) : maintenus en chronologie, ou
  déplacés vers concepts/réception (étape 11) ?

### 3. Slugs ambigus

- **« ELECTRIC-CIRCUS »** désigne **trois** événements distincts (1976-12-09
  « hate coat » ; 1977-05-29 premier concert Warsaw ; 1977-10-02 nuit de clôture
  *Short Circuit*). Le slug doit encoder **l'événement**, pas le lieu : quelle
  forme retenir (`EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS` vs un slug plus
  court) ?
- **Sex Pistols au Lesser Free Trade Hall** : deux gigs (4 juin / 20 juillet
  1976). Quelle stratégie de désambiguïsation des slugs — suffixe de date
  (`-1976-06-04` / `-1976-07-20`, mais cela réintroduit une date dans l'ID,
  contraire à (a)), suffixe ordinal (`-1`/`-2`), ou qualificateur sémantique ?
- **Catégorie de précision « décennie »** : la grille à 6 termes (`jour, mois,
  saison, annee, circa, intervalle`) n'a pas de bucket dédié aux 10 entrées de
  type décennie/vague. Les ranger en `circa`, ou créer un 7e terme `decennie` ?

---

# ANNEXE — État post-canonicalisation (brique d'identité, étape 6)

> Mise à jour : 31/05/2026. Cette annexe consigne l'**implémentation** de la
> brique d'identité (au-delà du diagnostic lecture-seule ci-dessus). Travail
> **strictement additif**, conforme au gel : aucun ID legacy renommé, aucune
> donnée existante réécrite ; seuls des champs optionnels sont ajoutés.
> Outil : `tools/canonicalize_chronology.py` (phases `classification`, `canon`,
> `precision`, `check`, `report`). Décisions de cadrage validées appliquées.

## I.1. Classification (`categorie`) — 500 entrées

| Catégorie | Nombre | Traitement |
|---|---:|---|
| `jalon` | 378 | reçoit (si réconcilié) un `EVENT-` canonique ; cœur de la chronologie |
| `concert_a_migrer` | 76 | conservé, ID legacy gardé, **non** promu — migrera vers `CONCERT-` (étape 10) |
| `reception_posthume` | 46 | conservé, étiqueté — relocalisation différée (étape 11) |

Règles : sources interprétatives (S29, S34) et tout événement postérieur à 1980
→ `reception_posthume` ; spine maître + formation/discographie/line-up/décès +
concerts premier/dernier/significatifs → `jalon` ; gigs ordinaires → `concert_a_migrer`.

## I.2. Canonicalisation `EVENT-<SLUG>` — 11 jalons, 39 arêtes `same_as`

Fichier : `registers/chronology/events_canonical.md`. Slugs sémantiques,
source-agnostiques, **sans date dans l'ID**. Chaque legacy d'un cluster porte
`same_as: EVENT-…` (append-only) dans son fichier source.

| `EVENT-` canonique | Date | `same_as` |
|---|---|---:|
| `EVENT-NAISSANCE-IAN-CURTIS` | 1956-07-15 | 2 |
| `EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER` | 1976-06-04 | 4 |
| `EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-SECOND` | 1976-07-20 | 4 |
| `EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS` | 1977-05-29 | 5 |
| `EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS` | 1978-01-25 | 5 |
| `EVENT-ARRIVEE-STEPHEN-MORRIS` | 1977-08 | 2 |
| `EVENT-SORTIE-A-FACTORY-SAMPLE` | 1979-01 | 2 |
| `EVENT-SORTIE-UNKNOWN-PLEASURES` | 1979-06-14 | 4 |
| `EVENT-DERNIER-CONCERT-BIRMINGHAM` | 1980-05-02 | 5 |
| `EVENT-MORT-IAN-CURTIS` | 1980-05-18 | 4 |
| `EVENT-SORTIE-CLOSER` | 1980-07-18 | 2 |

- Les **deux** concerts Sex Pistols (4 juin / 20 juillet 1976) sont désambiguïsés
  par qualificateur **ordinal** (`-PREMIER` / `-SECOND`), jamais par date — ils
  ne sont **pas** fusionnés.
- La **duplication intra-S41** (fichiers `timeline` vs narratifs) est réconciliée
  par `same_as` pour les jalons concernés (ex. premier concert Warsaw : 2 entrées
  S41 collapsées). **Dette signalée** (non traitée ici) : à terme, une timeline
  devrait être une *vue dérivée* et non un doublon stocké.
- `EVENT-` canonique reconnu comme kind `chronology` (build + loader). Le préfixe
  legacy source-scopé `EVENT-S\d+-` est **exclu** (cf. I.4).

## I.3. `date_precision` — 500 entrées

| Précision | Nombre |
|---|---:|
| `jour` | 206 |
| `annee` | 117 |
| `mois` | 89 |
| `circa` | 43 |
| `intervalle` | 38 (champs `date_debut` / `date_fin`) |
| `saison` | 7 |

Inférée honnêtement de la donnée existante, **jamais plus précise que la source** :
une date ISO complète dont la source porte `approximate` est rangée en `circa`
(pas `jour`). Les décennies pleines (« années 1960 ») deviennent un `intervalle`
borné (1960/1969) ; les décennies partielles (« début des années 1970 ») restent
`circa`. Décision retenue : **pas de 7e terme « décennie »** — absorbé par `circa`
ou `intervalle`. Le placeholder unique « à préciser » → `circa`, sans valeur inventée.

## I.4. Découverte — préfixe legacy `EVENT-S41-` non canonique (hors périmètre)

Quatre entrées **pré-existantes** squattent le namespace `EVENT-` sous forme
**source-scopée + date-encodée**, dans le **registre des chansons** (et non la
chronologie) : `EVENT-S41-M5-VAN-ACCIDENT-1979`,
`EVENT-S41-FACTORY-OFFICE-PARTY-1979-12-31`, `EVENT-S41-WILSON-REFUGE-AFTER-BURY`,
`EVENT-S41-DEBBIE-ANNIK-CO-RESPONDENT-CALL` (`registers/songs/s41_*`). Elles ont
une forme de fiche-chanson (`titre`/`usage`, sans `date`/`event`). Laissées **en
l'état** (registre chansons = refonte distincte) et **exclues** de la
reconnaissance `EVENT-`→chronologie via le motif `EVENT-S\d+-`. **À arbitrer** :
réconciliation ultérieure vers des `EVENT-<SLUG>` canoniques.

## I.5. Chaîne de cohérence

- `tools/canonicalize_chronology.py --phase check` : 39 `same_as` résolus,
  **0** cible manquante, **0** date impossible, **0** intervalle inversé.
- `tools/build_registers.py --strict` : **errors = 0** (chronology = 488 ;
  +11 canoniques ; entrée S75 récupérée).
- Sentinelle anti-drift (`tools/check_generated_sync.py`) : **OK** (exports
  régénérés ; churn d'horodatage écarté).

## I.6. Cas FLAGGÉS — à arbitrer (ne pas trancher unilatéralement)

`categorie` est renseignée partout par la règle ; les cas ci-dessous sont
remontés pour validation (heuristique de confiance moindre).

- **`context_urbain` (20)** — registres urbains/sociaux v2 (S02, S05, S06, S12,
  S20) : ni jalon du groupe, ni concert, ni réception posthume. Classés `jalon`
  par défaut faute de 4e catégorie. **Arbitrage** : créer une catégorie
  `contexte` ? les déplacer en étape 11 ?
- **`perf_mixte` (33)** — l'entrée mentionne une performance **mais** porte aussi
  un fait non-scénique (crise, accident, session, presse, « assiste à »…) :
  classées `jalon` (à confirmer entrée par entrée pour d'éventuelles bascules
  vers `concert_a_migrer`).
- **`jalon_concert_significatif` (10)** — gig retenu comme `jalon` car proche d'un
  mot-clé de significativité (dernier concert Warsaw au Swinging Apple,
  Eric's premier concert avec Morris, Pips after-gap, Derby Ajanta avant-dernier,
  3e concert Pistols à l'Electric Circus…). **Arbitrage** : lesquels sont de
  vrais jalons vs des gigs ordinaires à migrer ?

Liste exhaustive des identifiants flaggés : `python3 tools/canonicalize_chronology.py --phase report`.
