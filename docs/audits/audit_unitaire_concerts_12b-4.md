# Audit unitaire — registre des concerts (préalable à l'étape 7 — création `CONCERT-`)

> Audit **strictement diagnostic**, première brique de l'étape 7 (registre des
> concerts). **Lecture seule** : aucune écriture de donnée, aucun identifiant
> `CONCERT-` créé, aucun renommage, aucun `same_as` posé. On inventorie la
> matière à canonicaliser et on chiffre les tensions de conception, **sans rien
> trancher**.
>
> Date : 31/05/2026.
> Périmètre : `registers/chronology/**/*.md` (entrées `categorie:
> concert_a_migrer` et `a_scinder_etape_10: true`, posées en étape 6) ;
> `registers/concerts/` (reliquat joydiv.org) ; `exports/generated/concerts.*` ;
> `schemas/concert_v1.yaml`.
> Doctrine appliquée comme grille de lecture : `docs/specs/cross_registres.md`,
> `docs/NAMING_CONVENTIONS.md` §10, `docs/conventions/categories_chronologie.md`,
> `docs/audits/audit_unitaire_chronologie_12b-3.md` (socle EVENT- gelé).
> **Modèle cible** (cadrage, non tranché ici) : type d'unité `concert`, identité
> `CONCERT-<slug>` sémantique et **source-agnostique** (NAMING §10.2), référents
> `PLACE-` (étape 4) **+ date** comme attribut ; line-up / promoteurs / setlist
> **différés**. Le jeu d'identités `EVENT-` reste **gelé** (62, étape 6) ; cet
> audit n'y touche pas.

---

## A. Localisation de la matière

| Élément | Chemin | État |
|---|---|---|
| Gigs taggés en chronologie | `registers/chronology/*.md` — `categorie: concert_a_migrer` | **88** entrées |
| Bundles gig + jalon | `registers/chronology/*.md` — `a_scinder_etape_10: true` | **11** entrées |
| Reliquat « registre concerts » | `registers/concerts/00_canonical_concerts.md` | **196** entrées `JD-CONCERT-…` |
| Schéma du reliquat | `schemas/concert_v1.yaml` (+ `session_v1.yaml`) | présent |
| Exports du reliquat | `exports/generated/concerts.{json,csv}` | **197** records (cf. §D.4 — 1 parasite) |
| Source documentaire | `data/registre.json` → `REGISTRY-CONCERTS`, `REGISTRY-SESSIONS` | joydiv.org, T. Nuttall |
| Application dédiée | `apps/` | **absente** (cf. §D.3 — app retirée, données absorbées) |

Trois gisements **disjoints** coexistent donc : (1) les gigs **attribués par
source** noyés dans la chronologie (S41/S45/S75/S76), produits par la refonte de
l'étape 6 ; (2) un **registre concerts complet** issu de joydiv.org, à
identifiants `JD-CONCERT-YYYYMMDD-NNN` (date-dans-l'ID, lieux en texte libre),
sans app ni couche d'identité ; (3) le socle **`EVENT-` gelé** dont 11 entrées
chronologie restent à scinder. L'étape 7 doit les réconcilier sous une forme
canonique unique `CONCERT-<slug>`.

---

## B. Inventaire — les 88 `concert_a_migrer`

### B.1. Volumétrie et provenance

| Source | Entrées | Forme d'ID |
|---|---:|---|
| **S41** (Hook) | 47 | `CHR-S41-[TLn-]YYYY[-MM[-DD]]-SLUG` (date + slug) |
| **S76** (Torn Apart) | 28 | `CHR-S76-YYYY-NNN` (année + positionnel) |
| **S45** (Curtis) | 6 | `CHR-S45-YYYY[-MM[-DD]]-SLUG` |
| **S75** (Ott) | 4 | `CHR-S75-YYYY-NNN` |
| **Total** | **88** | — |

Aucune entrée ne porte la forme cible : **toutes** encodent au moins l'année dans
l'ID, la plupart le mois ou le jour, et toutes sont **source-scopées**. La forme
`CONCERT-<slug>` est donc, comme l'`EVENT-` de l'étape 6, **entièrement
nouvelle** ; la migration se fera par `same_as` **additif** (gel respecté).

### B.2. Distribution des dates (précision)

| `date_precision` | Nombre |
|---|---:|
| `jour` | **68** |
| `mois` | 9 |
| `intervalle` | 6 (résidences multi-soirs : Moonlight, Rainbow×2 soirs, Squat…) |
| `annee` | 2 |
| `circa` | 2 |
| `saison` | 1 |
| **Dates non datées au jour (incertaines)** | **20** (mois + intervalle + annee + circa + saison) |

77 % des gigs sont datés au jour — base solide pour la clé d'identité
`lieu + date`. Les 20 entrées non-jour exigeront soit un affinage de date, soit
une clé d'identité tolérante (date partielle).

### B.3. Couverture des lieux — **point critique**

| Mesure | Valeur |
|---|---:|
| Lieux (venues) distincts mentionnés par les 88 entrées | **47** |
| Venues résolvant déjà vers un `PLACE-` existant | **3** (Electric Circus, Rafters, Mayflower/Belle Vue) |
| Entrées couvertes par ces 3 `PLACE-` | 13 / 88 |
| **Venues SANS `PLACE-` (à créer en étape 4)** | **≈ 43 / 47 (≈ 91 %)** |
| Entrées dont le venue n'a pas encore de `PLACE-` | ≈ 74 / 88 |

Le registre `PLACE-` compte 83 identifiants, dont **24** de type salle/studio/
répétition — mais l'essentiel sont des **studios** (Strawberry, Cargo, Britannia
Row, T.J. Davidson's…) et des **salles non-JD** ; seules **3** salles de concert
JD y figurent. La quasi-totalité des venues de tournée (Plan K, Moonlight Club,
Rainbow Theatre, Bowdon Vale, Russell Club/Factory, Eric's, Les Bains Douches,
Paradiso, Effenaar…) sont **en texte libre, sans `PLACE-`**. **Le maillage
`CONCERT- → a_pour_lieu → PLACE-` est donc majoritairement non câblable en
l'état** : l'étape 7 est bloquée par un lot de création `PLACE-` (étape 4).

### B.4. Lieux récurrents (≥ 2 gigs au même lieu)

| Venue | Gigs | `PLACE-` ? |
|---|---:|---|
| Rafters | 6 | ✓ existant |
| Russell Club (Factory) | 6 | à créer |
| Electric Circus | 5 | ✓ existant |
| Plan K, Brussels | 4 | à créer |
| Rainbow Theatre, London | 4 | à créer |
| Bowdon Vale Youth Club | 4 | à créer |
| Futurama / Queen's Hall, Leeds | 3 | à créer |
| Derby/Town Hall, Bury | 3 | à créer |
| + 14 venues à 2 gigs (Squat, Middlesbrough, Eric's, Brunel, Band on the Wall, Moonlight, Bains Douches, Electric Ballroom, Check Inn, Salford Tech, Newcastle, Swinging Apple, YMCA, Mayflower) | 2 | 1 ✓ / 13 à créer |

**22 venues sur 47 reçoivent ≥ 2 gigs.** C'est la donnée structurante pour
l'arbitrage du slug (cf. §F.1) : un même lieu portant plusieurs concerts impose
de désambiguïser les slugs **autrement que par le seul lieu**.

### B.5. Doublons inter-sources — candidats `same_as` (ratio entrées → identités)

Regroupement par `lieu + date` (clé jour, sinon mois) :

| Mesure | Valeur |
|---|---:|
| Identités-gig distinctes estimées | **≈ 70** |
| **Ratio entrées → identités** | **88 → 70 ≈ 1,26 : 1** |
| Clusters multi-entrées (« même gig, plusieurs sources ») | **15** |
| Entrées absorbées par ces clusters | 33 |

Les 15 clusters `same_as` candidats :

| Date | Lieu | Entrées |
|---|---|---|
| 1976-12-09 | Electric Circus | S41-…-HATE-COAT · S76-1976-003 |
| 1977-06 | The Squat | S41-…-SQUAT-STUFF · S41-TL2-…-SEQUENCE *(intra-S41)* |
| 1977-09-14 | Rock Garden, Middlesbrough | S41-…-BOB-LAST · S41-TL2-…-TAPE *(intra-S41)* |
| 1977-10-02 | Electric Circus | S45-…-SHORT-CIRCUIT · S76-1977-006 |
| 1977-12-31 | Swinging/Spinning Apple | S41-…-SWINGING-APPLE · S76-1977-011 |
| 1978-04-14 | Rafters (Stiff/Chiswick) | S41-…-STIFF-CHISWICK · S75-1978-005 |
| 1978-05-20 | Mayflower / Belle Vue | S41-…-MAYFLOWER · S41-TL3-…-MAYFLOWER *(intra-S41)* |
| 1978-06-09 | Russell Club (Factory) | S41-…-FIRST-FACTORY · S41-TL3-…-FACTORY *(intra-S41)* |
| 1978-07-15 | Eric's, Liverpool | S41-TL3-…-RICH-KIDS · S76-1978-018 |
| 1979-03-14 | Bowdon Vale Youth Club | S41-…-WHITEHEAD · S41-…-WHITEHEAD-FILM · S76-1979-009 |
| 1979-09-08 | Futurama, Leeds | S41-…-FUTURAMA · S76-1979-017 |
| 1979-10-16 | Plan K, Brussels | S41-…-PLAN-K · S41-…-PLAN-K-TIMELINE · S75-1979-011 |
| 1979-11-09 | Rainbow Theatre | S41-…-RAINBOW · S76-1979-023 |
| 1979-12-18 | Les Bains Douches, Paris | S41-…-BAINS-DOUCHES · S76-1979-025 |
| 1980-04-08 | Derby Hall, Bury | S41-…-BURY · S75-1980-007 · S76-1980-024 |

Note : 4 de ces 15 clusters sont des **duplications intra-S41** (narratif vs
timeline TL2/TL3), à réconcilier comme en étape 6. **Piège à éviter** (analogue
au Lesser Free Trade Hall de l'audit chronologie) : les **3 gigs distincts à
l'Electric Circus** (1976-12-09 / 1977-05-29 *(déjà EVENT-)* / 1977-10-02) ne
doivent **pas** être fusionnés ; deux soirées au même venue (Moonlight 02→04
avril, Rainbow 09+10 nov.) sont **des concerts distincts**, non des doublons.

---

## C. Inventaire — les 11 bundles `a_scinder_etape_10`

Chaque bundle énonce, dans une seule entrée, **un gig** ET **un fait-jalon**. La
composante jalon a été canonicalisée en étape 6 ; la composante **gig** reste à
extraire vers `CONCERT-`. Vérification du **gel EVENT-** :

| Entrée | Date | Composante GIG (→ `CONCERT-`) | Composante jalon — `same_as` | EVENT- gelé ? |
|---|---|---|---|:--:|
| CHR-S10-1978-007 | 1978-12-27 | Hope & Anchor, London | `EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS` | ✓ |
| CHR-S45-1978-12-27-…-FIRST-FIT | 1978-12-27 | Hope & Anchor, London | `EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS` | ✓ |
| CHR-S75-1978-008 | 1978-12-27 | Hope & Anchor, London | `EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS` | ✓ |
| CHR-S76-1978-019 | 1978-12-27 | Hope & Anchor, London | `EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS` | ✓ |
| CHR-S41-TL3-1978-12-27-HOPE-ANCHOR-REVIEW | 1978-12-27 | Hope & Anchor, London | **— (aucun `same_as`)** | ⚠ cf. §F.4 |
| CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE | 1979-03-04 | Marquee, London | `EVENT-DEMOS-GENETIC-EDEN-STUDIOS` | ✓ |
| CHR-S41-1979-08-13-NASHVILLE-ANNIK | 1979-08-13 | Nashville Rooms, London | `EVENT-RENCONTRE-ANNIK-HONORE` | ✓ |
| CHR-S41-1979-08-13-…-ATMOSPHERE | 1979-08-13 | Nashville Rooms, London | `EVENT-RENCONTRE-ANNIK-HONORE` | ✓ |
| CHR-S76-1979-019 | 1979-08-13 | Nashville Rooms, London | `EVENT-RENCONTRE-ANNIK-HONORE` | ✓ |
| CHR-S41-1980-04-04-RAINBOW-FIT-… | 1980-04-04 | Rainbow Theatre, London | `EVENT-CRISE-RAINBOW-THEATRE` | ✓ |
| CHR-S75-1980-005 | 1980-04-04 | Rainbow Theatre, London | `EVENT-CRISE-RAINBOW-THEATRE` | ✓ |

**Composante jalon : confirmée gelée.** Les 11 bundles renvoient à **4** `EVENT-`
canoniques, tous présents dans le jeu gelé de 62 (`events_canonical.md`) :
`EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS`, `EVENT-DEMOS-GENETIC-EDEN-STUDIOS`,
`EVENT-RENCONTRE-ANNIK-HONORE`, `EVENT-CRISE-RAINBOW-THEATRE`.

**Composante gig : 4 concerts distincts** à fonder en `CONCERT-` —
Hope & Anchor (1978-12-27, 5 entrées), Nashville Rooms (1979-08-13, 3 entrées),
Rainbow Theatre (1980-04-04, 2 entrées), Marquee (1979-03-04, 1 entrée). **Aucun
de ces 4 venues n'a de `PLACE-`** → 4 créations `PLACE-` supplémentaires.
Les 11 bundles se réduisent donc à **4 identités-gig**.

> ⚠ **Anomalie** : `CHR-S41-TL3-1978-12-27-HOPE-ANCHOR-REVIEW` est taggé
> `a_scinder_etape_10` mais **ne porte aucun `same_as`** vers
> `EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS` (contrairement aux 4 autres
> entrées Hope & Anchor). Sa composante non-gig est la **critique Sounds** de
> Nick Tester, pas la crise — d'où l'absence de réconciliation. À arbitrer
> (cf. §F.4). Constat seulement ; rien n'est corrigé ici.

---

## D. Reliquat — registre joydiv.org (`00_canonical_concerts.md`)

### D.1. Volumétrie

| Mesure | Valeur |
|---|---:|
| Entrées `JD-CONCERT-…` | **196** |
| Statut `confirme` | 151 |
| Statut `annule` | 40 (dont 13 = tournée US annulée) |
| Statut `tv` | 3 |
| Statut `douteux` | 2 |
| Couples (lieu, ville) distincts | **136** |
| Entrées avec `nom_tournee` | 48 (Buzzcocks 25 · European tour Jan-1980 10 · US tour annulée 13) |
| Entrées avec `setlist` | **0** |

Couverture annoncée : 29 mai 1977 → 2 mai 1980 + tournée US annulée. C'est le
gisement **le plus complet et le plus homogène** (un seul schéma, une seule
source). Les venues récurrents y confirment §B.4 : Eric's (10), The Factory (9),
Rafters (7), Band on the Wall (7), Electric Circus (4), Apollo (4)…

### D.2. Forme d'ID non conforme au modèle cible

`JD-CONCERT-YYYYMMDD-NNN` **encode la date** (contraire au cadrage `CONCERT-<slug>`
+ date-attribut) et **ne référence aucun `PLACE-`** : `lieu`/`ville`/`pays` sont
en **texte libre**. C'est une 4ᵉ convention d'identifiant à réconcilier, comme
les 6 conventions de la chronologie. La migration se fera par `same_as` additif.

### D.3. App retirée, données et exports résiduels

Aucun dossier `apps/concerts-register/` (alors qu'existent `chronology-register`,
`song-register`, `places-register`…). `apps/lib/dynamic-registers.js` **ne charge
aucun** `kind: concert`. Le registre n'est donc **plus exposé par le runtime** —
l'app a été **retirée ou jamais portée** —, mais la donnée et l'export
persistent : `tools/build_registers.py` (l. 287-288, 626-676) classe encore
`JD-CONCERT-*` en `kind: concert` et **régénère** `concerts.{json,csv}`. Reliquat
**vivant côté build, mort côté UI**.

### D.4. Anomalie d'export — parasite d'en-tête

`exports/generated/concerts.json` contient **197** records pour **196** entrées
réelles : le 197ᵉ est l'identifiant-**gabarit** `JD-CONCERT-YYYYMMDD-NNN`, copié
depuis l'exemple de `registers/concerts/README.md` et **ingéré comme un vrai
concert** par le build (même classe de bug que les « parasites d'en-tête » de
l'audit lieux). Constat ; correctif hors périmètre.

### D.5. Adjacence — registre `sessions`

`registers/sessions/00_canonical_sessions.md` (+ `schemas/session_v1.yaml`,
`REGISTRY-SESSIONS`) est un reliquat **jumeau** (même source joydiv.org, démos /
Peel / répétitions). **Hors périmètre concerts**, signalé pour cohérence : sa
réconciliation relèvera d'une étape sœur (frontière concert ↔ session à tenir).

---

## E. Setlists & arête vers `SONG-`

- **Reliquat joydiv** : champ `setlist` prévu au schéma mais **jamais renseigné**
  (0/196).
- **Chronologie** : **1** entrée porte un champ structuré ; en revanche plusieurs
  `evenement`/`event` **décrivent en prose** une setlist (« longue setlist » au
  Plan K et aux Bains Douches, « Atmosphere ouvre le set » au Nashville, « She's
  Lost Control » filmée à Bowdon Vale…).

→ La matière setlist existe mais **non structurée**. Conforme au cadrage
(line-up / setlist **différés**), l'arête `CONCERT- → SONG-` n'est pas encore
outillable : à traiter dans une passe ultérieure, après création du registre cible.

---

## F. Tensions de conception (à informer, **non tranchées**)

### F.1. Date-dans-le-slug **ou non**, vu les lieux récurrents

C'est la tension centrale. 22 venues sur 47 portent ≥ 2 gigs (Rafters 6,
Russell Club 6, Plan K 4, Rainbow 4, Bowdon Vale 4…). Un slug fondé sur le **seul
lieu** (`CONCERT-PLAN-K`) **collisionne** dès le 2ᵉ concert. Trois stratégies,
chacune avec un coût :

- **(a) Lieu + date** (`CONCERT-PLAN-K-1979-10-16`) : désambiguïse trivialement,
  mais **réintroduit la date dans l'ID** — exactement ce que la doctrine `EVENT-`
  a banni (NAMING §10.2, audit chronologie décision (a)). Cohérence transversale
  ⇒ contre.
- **(b) Lieu + ordinal** (`CONCERT-PLAN-K-1` / `-2`) : sans date, mais l'ordinal
  est **fragile** (une date intercalée découverte plus tard renumérote tout) et
  peu sémantique.
- **(c) Lieu + descripteur sémantique** (tournée, tête d'affiche, festival,
  nom d'événement) : `CONCERT-PLAN-K-ATMOSPHERE` (?), `CONCERT-FUTURAMA-1979`,
  `CONCERT-STIFF-CHISWICK-RAFTERS`, `CONCERT-MOONLIGHT-RESIDENCE`… Le plus
  conforme à l'esprit `EVENT-`, mais **tous les gigs n'ont pas de descripteur
  distinctif** (cf. §F.2) → schéma de slug **hybride**, donc règle de
  désambiguïsation à spécifier précisément.

**Tension** : le modèle cible dit « identité = `PLACE-` + date », mais l'ID doit
rester sans date. Il faut donc **distinguer l'attribut date (porté, obligatoire)
de la clé de slug** — et décider de la stratégie de collision (a/b/c) **avant**
toute création.

### F.2. Descripteurs distinctifs réellement disponibles

Utilisables comme slug sémantique **sans date** : tournées (**Buzzcocks** 25 gigs,
**European tour Jan-1980** 10, **US tour annulée** 13 — d'après joydiv) ;
festivals (**Futurama** '79) ; événements nommés (**Stiff Test / Chiswick
Challenge**, **Stuff the Jubilee**, **Short Circuit** closing, **Rock Against
Racism** chez Kelly's, **soirées Factory** au Russell Club) ; têtes
d'affiche/support (support **Heartbreakers**, **Rezillos/Undertones**, support de
**The Cure** au Marquee). Mais **la majorité des gigs ordinaires n'ont aucun
descripteur** → un slug purement sémantique ne couvre pas tout le corpus.

### F.3. Lieux manquants — dépendance bloquante à l'étape 4

≈ **43 venues sur 47** (et les 4 venues des bundles) **n'ont pas de `PLACE-`**.
Sans eux, l'arête `a_pour_lieu` est vide pour ~74 des 88 gigs et pour les 4
bundles. **Tension de séquençage** : l'étape 7 présuppose un **lot de création
`PLACE-`** (salles de concert UK + venues européens), qui relève de l'étape 4 et
n'a pas été fait. À arbitrer : créer les `PLACE-` d'abord, ou créer les `CONCERT-`
avec un `a_pour_lieu` en texte libre provisoire (dette de maillage) ?

### F.4. Doublons & granularité d'identité

- **Ratio 88 → ~70** (chronologie seule) ; mais le **reliquat joydiv (196)** est
  un sur-ensemble quasi complet : l'identité-gig réelle est probablement portée
  par joydiv, la chronologie n'ajoutant que des **facettes attribuées** (S41/S45/
  S75/S76). **Tension** : qui est le porteur canonique du `CONCERT-` — joydiv
  (complétude) ou la chronologie (traçabilité de source) ? Le `same_as` doit-il
  pointer chronologie → joydiv → `CONCERT-`, ou tout legacy → `CONCERT-` ?
- **15 clusters internes** à la chronologie (dont 4 dup intra-S41) à réconcilier.
- **Anti-fusion** : 3 gigs Electric Circus, résidences multi-soirs (Moonlight,
  Rainbow) = concerts **distincts** — ne pas sur-fusionner sur le seul lieu.
- **`CHR-S41-TL3-1978-12-27-HOPE-ANCHOR-REVIEW`** (§C) : taggé `a_scinder` mais
  **sans `same_as`** ; sa composante non-gig (critique Sounds) n'est pas un
  `EVENT-`. À arbitrer : sa part gig fusionne-t-elle avec le `CONCERT-` Hope &
  Anchor du 27/12 (oui, vraisemblablement), et sa part critique devient-elle un
  atome de réception ou reste-t-elle un `jalon` nu ?

### F.5. Frontière concert / non-concert

À tenir au moment de la migration : gigs **annulés** (40 chez joydiv) et
**reportés** — un `CONCERT-` annulé est-il une identité de concert (statut
`annule`) ou exclu ? Passages **TV** (3 chez joydiv ; *Something Else*, *Granada*
en chronologie) — `CONCERT-` ou registre captations ? Concert **« joué devant
personne »** (Oldham Tower, Coach House Huddersfield) = concert ordinaire. Concert
**non joué** (soundcheck puis éjection au Locarno, Bristol) — exclure. Concerts
**d'autres artistes** assistés par le groupe (Lou Reed à Liverpool Empire, déjà
classé) — **pas** des `CONCERT-` Joy Division (relèvent de `contexte`).

---

## G. Synthèse — chiffres clés

| Axe | Valeur |
|---|---|
| Matière chronologie | **88** `concert_a_migrer` + **11** `a_scinder_etape_10` |
| Reliquat joydiv | **196** `JD-CONCERT-` (151 confirmés / 40 annulés / 3 TV / 2 douteux) ; **0** setlist ; **app retirée**, export résiduel (+1 parasite) |
| Lieux distincts (chronologie) | **47** venues |
| Couverture `PLACE-` | **3 / 47** venues (≈ 9 %) ⇒ **≈ 43 `PLACE-` à créer** + 4 pour les bundles |
| Dates | 68 jour / 9 mois / 6 intervalle / 2 année / 2 circa / 1 saison ⇒ **20 dates non-jour** (incertaines) |
| Ratio entrées → identités (chronologie) | **88 → ~70 ≈ 1,26 : 1** ; **15 clusters** `same_as` candidats (33 entrées) |
| Bundles | 11 → **4 identités-gig** ; composante jalon **gelée** (4 `EVENT-` vérifiés) ; **1** entrée sans `same_as` (anomalie §C/F.4) |
| Gel `EVENT-` | **intact** — aucun des 62 `EVENT-` touché par cet audit |
| Tensions majeures | date-dans-slug vs lieux récurrents (§F.1) ; ~43 `PLACE-` manquants bloquants (§F.3) ; porteur canonique joydiv vs chronologie (§F.4) |

---

## Décisions à arbitrer

*(rien n'est tranché ici — à valider avant toute écriture)*

1. **Stratégie de slug `CONCERT-`** face aux 22 lieux récurrents : descripteur
   sémantique (c) par défaut + repli ordinal (b) pour les gigs nus, **jamais**
   date-dans-l'ID (a) ? Spécifier la règle de désambiguïsation déterministe
   (extension de NAMING §10.2.3 au type `concert`).
2. **Séquençage `PLACE-`** : créer le lot de ~43 (+4) `PLACE-` venues **avant**
   les `CONCERT-`, ou tolérer un `a_pour_lieu` provisoire en texte libre ?
3. **Porteur canonique** : le `CONCERT-` est-il ancré sur le reliquat joydiv
   (complet) avec `same_as` des facettes chronologie, ou l'inverse ? Sort du
   reliquat `JD-CONCERT-` (déprécié par `same_as` ? conservé ? son export et son
   parasite §D.4 nettoyés ?).
4. **Périmètre** : les statuts `annule` (40) / `tv` (3) / `douteux` (2) entrent-ils
   dans `CONCERT-` (avec attribut statut) ou sont-ils exclus / relocalisés ?
5. **Bundle sans `same_as`** (`…HOPE-ANCHOR-REVIEW`, §C/F.4) : rattacher sa part
   gig au `CONCERT-` Hope & Anchor 1978-12-27 ; statut de la part critique.
6. **Registre `sessions`** (§D.5) : réconcilié en parallèle, et frontière
   concert ↔ session (Peel sessions, démos jouées live) à formaliser.
7. **Setlists** (§E) : différées (cadrage) — confirmer, et planifier la
   structuration prose → `SONG-` en passe ultérieure.
