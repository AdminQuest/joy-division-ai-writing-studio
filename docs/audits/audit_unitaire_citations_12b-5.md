# Audit unitaire — registre des citations (préalable à l'étape 8 — création `QUOTE-`)

> Audit **strictement diagnostic**, première brique de l'étape 8 (registre des
> citations). **Lecture seule** : aucune écriture de donnée, aucun identifiant
> `QUOTE-` créé, aucun renommage, aucun `same_as` posé, aucune arête `PERSON-`
> tirée. On inventorie la matière à canonicaliser et on chiffre les tensions de
> conception, **sans rien trancher**.
>
> Date : 31/05/2026.
> Périmètre : `registers/quotes/**/*.md` (registre dédié) ;
> `sources/*/citations_exactes.md` (atomisation par source) ;
> `registers/*_specialized_registers.md` (citations adossées aux registres
> spécialisés) ; `exports/generated/quotes.{json,csv}` et `quote_batches.*` ;
> `schemas/quote.schema.yaml` ; `apps/quote-register/` (UI).
> Doctrine appliquée comme grille de lecture : `docs/NAMING_CONVENTIONS.md` §10
> (forme canonique `<TYPE>-<SLUG>` source-agnostique, `same_as` déprécié→retenu,
> mono-valué, append-only), `docs/specs/cross_registres.md`,
> `docs/audits/audit_unitaire_concerts_12b-4.md` (modèle de l'audit préalable).
> **Modèle cible** (cadrage, non tranché ici) : type d'unité `quote`, identité
> `QUOTE-<slug>` sémantique et **source-agnostique** ; attribution → `PERSON-`
> **différée à l'étape 9** (on chiffre seulement la couverture) ; provenance /
> source comme attribut obligatoire. Le jeu d'identités `EVENT-` / `CONCERT-`
> reste **gelé** ; cet audit n'y touche pas.

---

## A. Localisation de la matière

| Élément | Chemin | État |
|---|---|---|
| Registre dédié | `registers/quotes/*.md` | **62** fichiers (1 consolidé + 61 par source) |
| Atomisation par source | `sources/*/citations_exactes.md` | **13** fichiers (sur **79** sources) |
| Citations adossées aux registres spécialisés | `registers/*_specialized_registers.md` | **31** fichiers |
| Lot historique (reliquat) | `registers/quotes/master_quotes.md` → `HIST-C1-IMPORT-001` | **70** lignes, `kind: quote_batch` |
| Schéma | `schemas/quote.schema.yaml` (`schema: quote`, v1.0) | présent |
| Exports | `exports/generated/quotes.{json,csv}` | **565** records `kind: quote` |
| Export du lot | `exports/generated/quote_batches.{json,csv}` | **1** record (le lot HIST) |
| Application dédiée | `apps/quote-register/` (`index.html`, `app.js`, `style.css`) | **présente et active** (charge `kind: quote` à chaud) |

Contrairement aux concerts (un reliquat joydiv.org compact + une chronologie),
la matière citation est **éclatée sur trois gisements imbriqués** : (1) un
**registre dédié** `registers/quotes/` (le plus volumineux) ; (2) une
**atomisation par source** `sources/*/citations_exactes.md` ; (3) des **citations
embarquées** dans les registres spécialisés. À cela s'ajoute (4) un **lot
historique** non atomisé (l'analogue du « reliquat joydiv » des concerts : un
import de travail figé, ici `00_Citations.xlsx`). L'app `quote-register` est, elle,
**bien présente et active** (différence notable avec l'app concerts retirée).

---

## B. Données « derrière la page » — les 565 records `kind: quote`

### B.1. Volumétrie et provenance par fichier-source

| Origine | Records | Remarque |
|---|---:|---|
| `registers/quotes/` | **309** | registre dédié (mais cf. §E — **partiellement** ingéré) |
| `registers/*_specialized_registers.md` | **140** | citations adossées (S53, S54, S78, S52, S77…) |
| `sources/*/citations_exactes.md` | **116** | atomisation par source (S45, S37, S29, S34…) |
| **Total exposé par la page** | **565** | `DynamicRegisters.loadRecords({ kinds: ['quote'] })` |

### B.2. Distribution par `source_id` — **38** sources distinctes

| Source | Records | Source | Records |
|---|---:|---|---:|
| **S76** (Middles & Reade, *Torn Apart*) | **195** | S53 / S54 (specialized) | 15 / 15 |
| **S45** (Deborah Curtis, *Touching from a Distance*) | **56** | S89 / S78 | 14 / 14 |
| **S71** (Claude Flowers) | 32 | S52 | 12 |
| **S75** (Chris Ott, *Unknown Pleasures*) | 21 | S72 (Reynolds) / S70 | 11 / 11 |
| S47 | 15 | S77 / S41 (Hook) *(cf. §E)* | 10 / **9** |

Une source domine massivement : **S76 = 195/565 ≈ 35 %**. Les trois premières
(S76 + S45 + S71) pèsent **283/565 ≈ 50 %**. La distribution est donc très
asymétrique — l'identité `QUOTE-` sera surtout éprouvée sur le sous-corpus
*Torn Apart*.

### B.3. Trois conventions d'identifiant legacy (à réconcilier vers `QUOTE-<slug>`)

| Convention | Exemple | Forme | Volume |
|---|---|---|---:|
| Source + ordinal `-Q` | `S45-Q001`, `S76-Q187` | `S\d+-Q\d+` | **557** |
| Source + ordinal `-CIT-` | `S37-CIT-001` | `S\d+-CIT-\d+` | **8** |
| Lot historique | `HIST-C1-001` | `HIST-C\d-\d+` | 70 *(dans le lot, non atomisé)* |

**Toutes** encodent la source dans l'ID (`S\d+`) et sont **positionnelles** :
aucune ne porte la forme cible. La forme `QUOTE-<slug>` est donc, comme `EVENT-`
et `CONCERT-`, **entièrement nouvelle** ; la migration se fera par `same_as`
**additif** (gel respecté). C'est la **3ᵉ famille de registre** à présenter la
même tripartition « slug sémantique cible vs identifiants positionnels/scopés
legacy » que les lieux (§10.1) et les concerts.

### B.4. Conformité au schéma déclaré — **faible**

`schemas/quote.schema.yaml` exige `id` + `source_id` + `citation_originale` +
`langue_originale` + `statut_verification`. Couverture réelle sur 565 :

| Champ requis | Couverture |
|---|---:|
| `source_id` | **565 / 565** (100 %) |
| `langue_originale` | 247 / 565 (44 %) |
| `citation_originale` | **121 / 565** (21 %) |
| `statut_verification` | 113 / 565 (20 %) |
| **Tous les requis simultanément** | **104 / 565 (18 %)** |

Seuls **18 %** des records satisfont le schéma déclaré. Le texte de la citation
est porté par **quatre champs concurrents** (`citation`, `citation_directe`,
`citation_originale`, `passage`, plus `quote`), le statut tantôt par une chaîne
tantôt par un **dictionnaire imbriqué** (65 records). La page compense ce
polymorphisme par des cascades de *fallback* (`app.js` : `data.citation_originale
|| data.citation_directe || data.quote || data.citation`). **Hétérogénéité de
schéma majeure** : à normaliser avant toute clé d'identité stable.

---

## C. Attribution (arête `PERSON-`, **différée étape 9** — couverture chiffrée)

### C.1. Couverture brute

| Mesure | Valeur |
|---|---:|
| Records portant un locuteur/auteur (`locuteur`/`auteur`/`auteur_cite`/`source_auteur`) | **290 / 565 (51 %)** |
| Records **sans** attribution explicite (anonymes / presse / narration nue) | **275 / 565 (49 %)** |
| Records normalisés vers un `PERSON-` | **0** |

### C.2. **Le champ d'attribution conflate trois choses distinctes**

Les valeurs d'attribution les plus fréquentes :

| Valeur | Occur. | Nature réelle |
|---|---:|---|
| **Middles & Reade** | 50 | **auteurs du livre S76** (narration, pas un locuteur cité) |
| Peter Hook | 23 | locuteur (membre) |
| Terry Mason | 18 | locuteur (entourage) |
| Annik Honoré | 14 | locuteur (entourage) |
| Ian Curtis | 12 | locuteur (membre) |
| Chris Ott / Tony Wilson / Claude Flowers / Paul Morley | 9/9/8/8 | mélange auteur ↔ locuteur |
| « Peter Hook **cité par** Chris Ott », « Bernard Sumner **cité par** Chris Ott » | — | **chaîne d'attribution** (locuteur ↔ rapporteur) |

Trois registres sémantiques sont écrasés dans un seul champ : **(a)** le
**locuteur** réel (membre/entourage), **(b)** l'**auteur de la source** (narrateur :
Middles & Reade pour les 195 quotes S76, Flowers, Ott…), **(c)** les **chaînes
« X cité par Y »** (27 records) où locuteur et rapporteur coexistent. Conséquence :
les **51 %** annoncés **surestiment** la couverture *locuteur* — une part notable
des « attributions » sont en fait l'**auteur du livre** (les ~50 « Middles & Reade »
ne sont pas des citations *de* Middles & Reade, mais la narration de *Torn Apart*).
La couverture *locuteur identifié* nette est **sensiblement inférieure à 51 %**.

### C.3. Conséquence pour l'étape 9

L'arête `QUOTE- → attribué_à → PERSON-` exige d'abord de **séparer** locuteur,
rapporteur et auteur-de-source dans des champs distincts — un pré-traitement non
trivial **avant** toute liaison `PERSON-`. Le lot historique le signale déjà
crûment : **28 / 70** lignes y sont marquées « **à attribuer** » (cf. §F).

---

## D. Provenance, dates, verbatim/paraphrase

### D.1. Provenance — **forte**

| Mesure | Valeur |
|---|---:|
| Records avec `source_id` | **565 / 565 (100 %)** |
| Records avec page/pagination (`page_pdf`/`pages`/`page_print`/`passage`/…) | **565 / 565 (100 %)** |
| Records avec `source_year` (année d'édition) | **565 / 565 (100 %)** |

C'est le **point fort** du corpus citation (à l'inverse des concerts, bloqués par
les `PLACE-` manquants) : **toute** citation est sourcée et paginée. L'exigence de
provenance est **structurellement satisfaite** — sous réserve d'homogénéiser les
champs de page (au moins 6 variantes : `page_pdf`, `pages_pdf`, `pages`,
`page_print`, `pages_livre`, `passage`).

### D.2. Dates — **quasi inexistantes**

| Mesure | Valeur |
|---|---:|
| Records avec **date de la citation** (prononcée/publiée : `date`/`date_citation`/`date_propos`) | **0 / 565** |
| Records avec `source_year` (année du **livre**, pas de l'énonciation) | 565 / 565 |

**Aucune** citation ne porte la date à laquelle le propos a été **tenu** ; seule
l'année d'**édition de la source** est connue. Or `source_year` ≠ date
d'énonciation (un livre de 2006 cite un propos de 1979). La couverture
« date où la citation a été prononcée/publiée » est donc **≈ 0 %**. Si une date
est requise comme attribut `QUOTE-` (comme pour `CONCERT-`), elle est **à
reconstruire** intégralement.

### D.3. Verbatim vs paraphrase

| Catégorie | Volume | % |
|---|---:|---:|
| Texte **verbatim** présent (un des champs `citation*`/`passage`/`quote`) | **348 / 565** | **61 %** |
| **Sans** verbatim, `resume`/`usage_livre` seulement (paraphrase/usage) | **127** | 22 % |
| Reste (concept, terme analytique, fragment non textuel) | ~90 | 17 % |
| `statut` contenant explicitement `paraphrase_candidate` | 34 | — |

≈ **40 %** du corpus exposé **n'est pas une citation directe** (paraphrase, usage,
concept). Le lot historique l'accentue (cf. §F.2). **Tension de périmètre** : un
`QUOTE-` doit-il accueillir la paraphrase et le `reference_or_concept`, ou se
restreindre au verbatim ? Le `master_quotes.md` pose déjà la règle inverse :
« les entrées marquées comme concepts, titres, paraphrases […] **doivent rester
hors citation directe** ».

### D.4. Doublons — **pas de clé naturelle de déduplication**

| Mesure | Valeur |
|---|---:|
| Records porteurs de verbatim ≥ 12 car. | 342 |
| Doublons **exacts** (texte normalisé identique) | **0 cluster** |
| Quasi-doublons (préfixe 25 car.) | **1** cluster (2 records) |
| Atomes (`related_atoms`) partagés par > 1 quote (signal `same_as` faible) | **73** atomes |

Résultat frappant et **opposé** aux concerts : il n'existe **aucune clé mécanique**
de dédup. Là où `lieu + date` donnait pour les concerts un ratio **88 → ~70
(1,26 : 1)** avec 15 clusters nets, les citations sont **textuellement uniques**
(traductions et formulations divergentes d'une source à l'autre). Le ratio
**entrées → identités est donc ≈ 1 : 1** au sens mécanique. Les vrais doublons
(même propos rapporté par deux livres avec un mot près) existent — les 73 atomes
partagés en sont l'indice — mais ils sont **non détectables par égalité de
chaîne** : tout `same_as` citation relèvera d'un **jugement sémantique**, pas d'un
*join*.

---

## E. Reliquat & angle mort de build — **~290 citations définies mais invisibles**

### E.1. Le registre dédié n'est ingéré qu'en partie

`registers/quotes/` **définit 588** identifiants `-Q` distincts, mais seuls
**309** records en proviennent dans l'export. En croisant **tout** le dépôt
(registre + sources) :

| Mesure | Valeur |
|---|---:|
| Identifiants `-Q` **définis** (registers/quotes + sources) | **707** |
| Identifiants `-Q` **ingérés** (dans `quotes.json`) | 557 |
| **Définis mais ABSENTS de la page** | **≈ 290** |

Décomposition des absents par source : **S41 (Peter Hook) = 214**,
**S45 (Curtis) = 52**, puis S26 (7), S22 (5), S12 (4)…

### E.2. Cause — les listes `quotes:` de 1er niveau ne sont pas éclatées

Vingt-quatre fichiers (dont **les 20 fichiers `s41_hook_quotes_*`**) structurent
leurs citations sous une **liste YAML de 1er niveau** `quotes: [ {id: S41-Q114, …}, … ]`.
Le build (et l'`inferKind` dynamique, cf. note `apps/lib/dynamic-registers.js:8`)
n'**éclate pas** ces listes en records individuels : le fichier entier est lu
comme un bloc dont l'`id` racine est absent → les ~290 citations qu'il contient
**ne sont jamais exposées**. Vérification ciblée : **223** `S41-Q…` (Hook) sont
définis dans le registre, **9** seulement atteignent la page (**214 invisibles**).

> ⚠ **Conséquence d'audit** : la « matière derrière la page » (565) **sous-estime**
> le corpus réel. La quasi-totalité des citations de **Peter Hook** (*Unknown
> Pleasures: Inside Joy Division*, S41) — un témoin de premier plan — et la moitié
> du complément **Curtis** (S45) sont **hors registre exposé**. C'est la même
> classe de bug que les « parasites d'en-tête » des audits lieux/concerts, mais
> en **soustraction** : non pas un faux record en trop, mais **~290 vrais records
> manquants**. Constat seulement ; correctif hors périmètre.

### E.3. Lot historique `HIST-C1-IMPORT-001` — le reliquat à part

C'est l'analogue du reliquat joydiv des concerts : un **import figé** de
`00_Citations.xlsx` (70 lignes, chapitre 1), classé `kind: quote_batch` et **non
atomisé** en records `quote`. Il porte sa **propre typologie** (colonne *Type*) et
son propre statut consolidé (`candidate` / `verified_candidate` /
`reference_or_concept`). Il **ne passe pas** par le schéma `quote` et n'est **pas
exposé** par la page citations (seulement par `quote_batches.*`). Sa
réconciliation vers `QUOTE-` est une **passe distincte** (dé-tableautage,
attribution des 28 « à attribuer », tri verbatim/concept).

---

## F. Le lot historique en détail (70 lignes) — typologie et attribution

| Axe | Répartition |
|---|---|
| **Type** | verbatim **8** · paraphrase (toutes formes) **~37** · titre d'œuvre/chanson **7** · concept/terme analytique **~15** · divers (argot, surnom, rubrique) **3** |
| **Attribution** | source connue **42** · **« à attribuer » 28** |
| **Statut** | `candidate` 45 · `reference_or_concept` 20 · `verified_candidate` 5 |

Le lot confirme en miniature les tensions globales : **majorité non-verbatim**
(8 verbatim sur 70), **40 % non attribués**, et une part importante (**20**) de
`reference_or_concept` que la doctrine du registre exclut explicitement de la
citation directe. Exemples de fragments sans clé courte naturelle : « khazi »,
« honnête », « bourgeois », « son Manchester », « Pam ponders ».

---

## G. Doctrine de slug — pourquoi une citation n'a **pas** de clé naturelle

`NAMING_CONVENTIONS.md` §10.2.2 dérive le slug d'un **`label`** (nom retenu du
lieu) par slugification déterministe. Un lieu a un nom court ; un concert a un
couple lieu+événement. **Une citation n'a ni l'un ni l'autre** :

- le **texte** est trop long et instable (traductions multiples : 116 `en`,
  105 `it`, 20 « anglais », 6 `fr` — la même citation existe en plusieurs
  langues/formulations) pour servir de slug ;
- **49 %** des citations sont **anonymes** → pas de locuteur pour amorcer le slug ;
- une part notable sont des **fragments** (« khazi », « self-inflicted wound »,
  « moral Chernobyl ») sans thème distinctif ;
- l'absence de **clé courte naturelle** impose un slug **composite** et
  **construit** — typiquement `locuteur + thème/occasion` (ex. hypothétique
  `QUOTE-HANNETT-TOILET-SOUND`, `QUOTE-ANDERTON-SELF-INFLICTED-WOUND`) — donc une
  **doctrine de slug nouvelle**, non couverte par §10.2.2.

---

## H. Synthèse — chiffres clés

| Axe | Valeur |
|---|---|
| Citations « derrière la page » | **565** records `kind: quote` (38 sources ; S76 ≈ 35 %) |
| Corpus réel défini (registre + sources) | **707** identifiants `-Q` ⇒ **~290 définis mais invisibles** (214 Hook S41, 52 Curtis S45 — listes `quotes:` non éclatées) |
| Reliquat historique | **70** lignes `HIST-` (`quote_batch`), non atomisé, typologie propre |
| Conventions d'ID legacy | **3** (`S\d+-Q\d+` ×557, `S\d+-CIT-` ×8, `HIST-` ×70) — forme `QUOTE-<slug>` **nouvelle** |
| Conformité schéma `quote` | **104 / 565 (18 %)** ; texte sous 4+ champs concurrents ; statut parfois dict |
| **Attribution** (couverture brute) | **290 / 565 (51 %)** — **surestimée** (auteur-de-source vs locuteur conflatés ; 27 « cité par ») ; **0** `PERSON-` ; 28/70 « à attribuer » dans le lot |
| **Provenance** | **565 / 565 (100 %)** sourcées + paginées (point fort) ; 6 variantes de champ page |
| **Dates** d'énonciation | **0 / 565** (seule l'année d'édition est connue) |
| **Verbatim vs paraphrase** | **~61 % verbatim** / ~40 % paraphrase·usage·concept (lot historique : 8 verbatim / 70) |
| **Doublons** | **0** doublon exact ; ratio entrées→identités **≈ 1 : 1** mécanique ; same_as = **jugement sémantique** (73 atomes partagés comme seul signal faible) |
| Gel `EVENT-` / `CONCERT-` | **intact** — aucun touché par cet audit |

---

## I. Tensions de conception (à informer, **non tranchées**)

### I.1. Doctrine de slug d'une citation
Aucune clé courte naturelle (≠ `PLACE-`/`CONCERT-`). Le slug devra être
**composite et construit** (`locuteur + thème/occasion`), mais **49 %** des
citations sont **anonymes** et beaucoup sont des **fragments** sans thème
distinctif. §10.2.2 (slug dérivé d'un `label`) **ne s'applique pas** : il faut
**spécifier une règle de slug propre au type `quote`**, avec stratégie de repli
pour les anonymes (thème seul ? source + ordinal ?) et de désambiguïsation
(plusieurs citations d'un même locuteur sur un même thème).

### I.2. Attribution différée mais champ à dénormaliser d'abord
La couverture **51 %** est **gonflée** : le champ mélange locuteur, auteur-de-source
et chaînes « cité par ». **Avant** l'arête `PERSON-` (étape 9), il faut séparer
ces trois rôles — sinon les 195 quotes S76 se rattacheraient à « Middles & Reade »
(les auteurs) plutôt qu'à leurs locuteurs réels. Tension : l'étape 8 doit-elle
déjà **dénormaliser l'attribution** (champ `locuteur` distinct de `source_auteur`),
ou geler l'état et tout reporter à l'étape 9 ?

### I.3. Exigence de provenance — satisfaite, mais date manquante
Provenance **100 %** (force du corpus) — mais **date d'énonciation 0 %** et
**6 champs de page** concurrents. Tension : si `QUOTE-` exige une date-attribut
(symétrie avec `CONCERT-`), elle est **à reconstruire** ; sinon, acter que la
provenance se limite à `source + page` et que la datation est facultative.

### I.4. Doublons — pas de clé, ratio ≈ 1 : 1
Aucun *join* mécanique (0 doublon exact). Le `same_as` citation relève du
**jugement éditorial** (même propos, formulations/langues divergentes). Tension :
faut-il un même_propos canonique (regroupant les variantes de traduction/source)
**au-dessus** des `QUOTE-` par-source, ou chaque variante est-elle un `QUOTE-`
distinct relié par `same_as` ? Et quel porteur canonique (la formulation
originale ? la plus citée ?) ?

### I.5. Données existantes vs citations-sources — corpus sous-estimé
La page (565) **n'expose pas** ~290 citations définies (214 Hook, 52 Curtis) à
cause des listes `quotes:` non éclatées (§E), ni les 70 lignes du lot historique.
Tension de **complétude et de porteur** : l'étape 8 doit-elle d'abord **réparer
l'ingestion** (éclatement des listes `quotes:`) pour voir tout le corpus, choisir
entre registre dédié / atomisation source / specialized comme **gisement
canonique**, et statuer sur le sort du **lot historique** (atomiser vers `QUOTE-`
ou laisser en `quote_batch`) ?

### I.6. Verbatim vs paraphrase/concept dans le périmètre `QUOTE-`
≈ 40 % du corpus n'est pas du verbatim. La doctrine `master_quotes` exclut
concepts/titres/paraphrases de la citation directe. Tension de **frontière** :
`QUOTE-` = verbatim **strict** (et les paraphrases/concepts relèvent de `CONCEPT-`
/ `MOTIF-` / atomes) ? ou `QUOTE-` accueille un attribut `type` (verbatim /
paraphrase / reference) ?

---

## Décisions à arbitrer

*(rien n'est tranché ici — à valider avant toute écriture)*

1. **Doctrine de slug `QUOTE-`** : règle composite `locuteur + thème` + repli pour
   les ~49 % d'anonymes et les fragments ; désambiguïsation déterministe.
   Extension dédiée de NAMING §10 au type `quote`.
2. **Attribution** : dénormaliser `locuteur` ↔ `source_auteur` ↔ « cité par » dès
   l'étape 8, ou tout différer à l'étape 9 ? (impact direct sur la justesse de
   l'arête `PERSON-`).
3. **Date** : attribut obligatoire (à reconstruire, 0 % actuel) ou facultatif ?
4. **Gisement canonique** : registre dédié `registers/quotes/` vs
   `citations_exactes` vs specialized — lequel porte le `QUOTE-`, et `same_as`
   dans quel sens ?
5. **Angle mort d'ingestion** (§E) : réparer l'éclatement des listes `quotes:`
   (≈ 290 records, dont **214 Hook**) **avant** la canonicalisation, sous peine de
   fonder le registre sur un corpus amputé.
6. **Lot historique** (70 lignes `HIST-`) : atomiser vers `QUOTE-` (avec les
   28 « à attribuer ») ou conserver en `quote_batch` ?
7. **Frontière verbatim / paraphrase / concept** : périmètre strict du `QUOTE-`
   et renvoi des non-verbatim vers `CONCEPT-`/`MOTIF-`/atomes.
8. **Homogénéisation de schéma** : champ unique de texte, champ unique de page,
   statut non-imbriqué — préalable à toute clé d'identité (18 % de conformité
   actuelle).
