# Conventions de nommage

## Objet

Les conventions de nommage du repo sont désormais gelées.

Objectifs :

- cohérence ;
- stabilité ;
- lisibilité ;
- compatibilité des automatisations ;
- traçabilité documentaire.

Toute nouvelle ressource doit respecter ces conventions.

---

# 1. Sources

Format recommandé :

```text
SXXX_Auteur_TitreCourt_Annee.md
```

Exemples :

```text
S041_Hook_UnknownPleasures_2012.md
S045_Curtis_TouchingFromADistance_1995.md
```

Règles :

- pas d’espaces ;
- pas d’accents ;
- underscores uniquement ;
- année finale obligatoire si connue.

---

# 2. Atomes

Format :

```text
AT_CHXX_XXXXX
```

Exemple :

```text
AT_CH02_00034
```

Règles :

- identifiant unique ;
- stable ;
- jamais recyclé.

---

# 3. Citations

Format :

```text
CIT_CHXX_XXXX
```

---

# 4. Concepts

Format :

```text
CONCEPT-XXX
```

---

# 5. Mythes

Format :

```text
MYTH-XXX
```

---

# 6. Motifs

Format :

```text
MOTIF-XXX
```

---

# 7. Chronologie

Format :

```text
CHR-SXXX-XXX
```

---

# 8. Fichiers éditoriaux

Format recommandé :

```text
chapter_XX_master.md
```

Exemple :

```text
chapter_01_master.md
```

---

# 9. Doctrine importante

Les identifiants stabilisés ne doivent plus être modifiés.

Toute modification casse potentiellement :

- les graphes ;
- les liens ;
- les exports ;
- les prompts ;
- les automatisations.

---

# 10. Identité des lieux — forme canonique et réconciliation par équivalence

> Registre des lieux — étape 4 (Carte des lieux, 12b-1.c). Enrichissement
> **additif**, conforme à `SCHEMA_FREEZE_POLICY` (aucun renommage).
> Spécification détaillée : `docs/conventions/identifiants_lieux.md`.
>
> Note d'adaptation au dépôt : les lieux ne relèvent **pas** d'`atom.schema.yaml`
> (`type_unite` de l'atome n'a pas de valeur `lieu`) mais d'un schéma dédié
> `schemas/places.schema.yaml` (`type_unite: place`, champ de nom `label`),
> validé par `tools/validate_places.py`.

## 10.0. Convention de langage normatif

Les termes **DOIT**, **NE DOIT PAS**, **DEVRAIT** et **PEUT** s'entendent au sens
de la RFC 2119 : obligation, interdiction, recommandation et faculté. Ils
qualifient des règles vérifiables par l'outil de validation.

## 10.1. Problème traité

Trois conventions de nommage des identifiants `PLACE-*` coexistent dans le
corpus, héritées de passes de saisie successives :

| Convention | Exemple | Origine |
|---|---|---|
| Slug sémantique (v2) | `PLACE-TJ-DAVIDSONS` | Atomisation v2, source-agnostique |
| Positionnel | `PLACE-S83-001` | Saisie manuelle ancienne, index par source |
| *Scoping-source* | `PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET` | Saisie manuelle ancienne, source + qualificateur |

La déduplication ne fusionne que sur identifiant strictement identique. Un même
lieu physique portant plusieurs identifiants apparaît donc en plusieurs
exemplaires — concrètement, plusieurs punaises distinctes sur la couche
cartographique pour une seule adresse réelle. Le gel des schémas
(`SCHEMA_FREEZE_POLICY`) interdisant le renommage des identifiants stabilisés,
la réconciliation **DOIT** s'opérer par enrichissement additif et non par
migration d'identifiants.

## 10.2. Forme canonique

**10.2.1. Définition.** La forme canonique d'un lieu est `PLACE-<SLUG>`, où
`<SLUG>` est **source-agnostique** : il ne porte ni jeton de source (`S\d+`), ni
index positionnel, ni préfixe de provenance. Conforme au motif du schéma :
`^PLACE-[A-Z0-9][A-Z0-9-]*$`.

**10.2.2. Règle de slugification (déterministe).** Le `<SLUG>` est dérivé du nom
retenu du lieu (`label`) par application, dans l'ordre, des transformations
suivantes :

1. repli ASCII des caractères accentués (« é » → « e », « ô » → « o ») ;
2. passage en capitales ;
3. remplacement de toute séquence de caractères non alphanumériques par un tiret
   unique ;
4. suppression des tirets de tête et de fin ;
5. retrait des jetons de source et d'index (`S\d+`, suffixes positionnels).

**10.2.3. Désambiguïsation.** Un qualificateur (voie, ville) **NE DOIT PAS** être
ajouté par défaut. Il **PEUT** l'être uniquement lorsque deux lieux physiques
*distincts* partagent un même nom, et seulement dans la mesure strictement
nécessaire à les distinguer.

**10.2.4. Sélection du canonique en cas de candidats multiples.**

1. s'il existe déjà un slug v2 conforme à 10.2.2, il fait foi ;
2. à défaut, le slug est dérivé du nom le plus complet et le plus stable ;
3. en cas d'égalité, on retient la forme la moins ambiguë, et l'on consigne
   explicitement la règle de départage appliquée.

La forme canonique, une fois fixée, est elle-même gelée : elle relève dès lors de
`SCHEMA_FREEZE_POLICY`.

## 10.3. Sémantique du champ `same_as`

**10.3.1. Rôle.** `same_as` est un champ **optionnel** déclarant une relation
d'équivalence d'identité : « cet enregistrement désigne le même lieu physique
que l'identifiant cible ». Son ajout est un enrichissement rétrocompatible au
sens du gel ; il n'entraîne **aucun** renommage.

**10.3.2. Sens de l'arête.** Le champ `same_as` **DOIT** être porté par les
enregistrements *legacy* (formes positionnelle et *scoping-source*) et pointer
vers la forme **canonique**. Le sens est donc : *déprécié → retenu*.

**10.3.3. Mono-valué.** `same_as` est **MONO-VALUÉ** : une seule cible canonique
par enregistrement (chaîne, pas tableau). Une équivalence d'identité vers
plusieurs canoniques serait contradictoire : s'ils sont le même lieu, ils
**DOIVENT** être fusionnés ; sinon, ce ne sont pas des équivalents. Le
mono-valué garantit structurellement la convergence (INV-4).

**10.3.4. Append-only.** L'enregistrement canonique **NE DOIT PAS** être muté
pour enregistrer ses alias : la connaissance des alias est reconstruite à la
lecture (cf. 10.4). Cette règle protège l'enregistrement le plus référencé du
*churn* (dette D.1) et préserve la provenance : chaque enregistrement *legacy*
demeure auto-descriptif et porte lui-même son pointeur de réconciliation.

**10.3.5. Transitivité.** Une chaîne d'équivalences (`A same_as B`,
`B same_as C`) **DOIT** être résolue jusqu'à son point fixe — l'identifiant
canonique terminal. La résolution **DOIT** être déterministe et converger vers
un canonique unique.

> **Encadré — filiation « données liées »**
> Le champ `same_as` reprend la sémantique de `owl:sameAs` et de
> `schema.org/sameAs` : une équivalence d'identité orientée, et non une simple
> parenté thématique. Ce choix n'est pas cosmétique : la relation constitue le
> **premier type d'arête d'équivalence** du futur modèle cross-registres. La
> spécification de l'étape 5 **DOIT** la réutiliser telle quelle pour toutes les
> classes d'entités (personnes, organisations, concerts…) plutôt que
> d'introduire une convention concurrente. Elle alimentera directement le graphe
> de relations (étape 13) et pourra rattacher des entités externes lors de la
> veille Discogs (étape 14).

## 10.4. Comportement attendu du *loader*

Le *loader* (`apps/lib/dynamic-registers.js`) :

1. **DOIT** résoudre chaque enregistrement *legacy* vers son canonique au
   chargement (fusion à la lecture) ;
2. **DOIT** construire l'index inverse `canonique → [alias]`, sans stockage
   redondant de cette liste dans les données ;
3. **DOIT** faire opérer la déduplication cartographique sur l'**identité
   canonique** résolue, et non sur l'identifiant brut ;
4. **DEVRAIT** résoudre la transitivité par une structure d'union-recherche
   (*union-find*) ou équivalent, garantissant la convergence vers le point fixe.

## 10.5. Invariants vérifiés par le validateur

`tools/validate_places.py` (tests : `tools/test_validate_places.py`) :

| Code | Invariant | Sévérité |
|---|---|---|
| INV-1 | Toute valeur de `same_as` résout vers un identifiant `PLACE-*` existant. | Erreur |
| INV-2 | Le graphe des relations `same_as` ne contient aucun cycle. | Erreur |
| INV-3 | Un lieu canonique est un point fixe : il ne porte aucun `same_as` sortant. | Erreur |
| INV-4 | Toute chaîne d'équivalences converge vers un canonique unique (pas de divergence vers deux canoniques). | Erreur |
| INV-5 | Tout identifiant `PLACE-*` référencé par un autre registre est soit canonique, soit résoluble vers un canonique. | Avertissement (TODO) |
| INV-6 | Deux lieux canoniques distincts ne partagent pas des coordonnées identiques sans justification consignée (`prudence_methodologique`). | Avertissement |

INV-1 à INV-4 garantissent l'intégrité du mécanisme et interdisent tout
contournement silencieux du gel ; ils sont vérifiés de façon explicite et
défensive (le mono-valué de 10.3.3 rend INV-4 structurellement satisfait, mais
le garde subsiste contre une donnée mal formée). INV-5 protège la propriété
*cross-ready* en amont des étapes 10 et 11 ; son balayage cross-registres n'est
pas implémenté dans ce validateur (résolu au runtime par le loader) et reste un
TODO explicite. INV-6 sert de filet contre les doublons physiques non encore
réconciliés.

## 10.6. Exemple traité — studio T.J. Davidson

| Identifiant | Convention | Rôle |
|---|---|---|
| `PLACE-TJ-DAVIDSONS` | slug v2 | **Canonique** |
| `PLACE-S83-001` | positionnel | Alias → `PLACE-TJ-DAVIDSONS` |
| `PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET` | *scoping-source* | Alias → `PLACE-TJ-DAVIDSONS` |

Enregistrement canonique (la coordonnée s'attache **ici**, après réconciliation) :

```yaml
id: PLACE-TJ-DAVIDSONS
type_unite: place
label: "TJ Davidson's"
lat: 53.474
lng: -2.249
geo_precision: rue                 # exacte | rue | quartier | ville (granularité)
reference_croisee: ["wikidata:Q…"] # tableau, identifiants préfixés par autorité
prudence_methodologique: >-        # axe confiance/incertitude
  Entrepôt de répétition, Little Peter Street ; bâtiment d'origine disparu.
```

Enregistrement *legacy* (identifiant gelé, simple ajout de `same_as`) :

```yaml
id: PLACE-S83-001
type_unite: place
same_as: PLACE-TJ-DAVIDSONS   # équivalence d'identité ; aucun renommage (gel respecté)
```

> Les coordonnées ne sont **jamais devinées par géocodage automatique**. Elles
> sont saisies manuellement ou recoupées depuis Wikidata (propriété P625,
> licence CC0 — stockable sans attribution), accompagnées de leur provenance
> (`reference_croisee`), de leur granularité (`geo_precision`) et, le cas
> échéant, d'une note `prudence_methodologique` (lieu démoli, localisation
> approximative). **Granularité et confiance sont deux axes distincts** :
> `geo_precision` ne porte pas de valeur « approximative » — l'incertitude se
> documente dans `prudence_methodologique`.

## 10.7. Articulation avec la doctrine existante

1. **`SCHEMA_FREEZE_POLICY`.** Dispositif relevant exclusivement de la catégorie
   autorisée « ajout prudent de champ optionnel / enrichissement
   rétrocompatible ». Aucun identifiant n'est renommé.
2. **`NAMING_CONVENTIONS`.** La présente section fixe la forme canonique et sa
   règle de dérivation déterministe.
3. **Spécification cross-registres (étape 5).** La sémantique de `same_as`
   arrêtée ici constitue une décision de spécification anticipée, à reprendre
   sans modification par l'étape 5.
4. **Schéma (`schemas/places.schema.yaml`).** `same_as` y est déclaré comme
   propriété optionnelle (chaîne, motif `PLACE-*`) ; `geo_precision`,
   `reference_croisee`, `prudence_methodologique` y sont des champs optionnels.

### Conclusion intermédiaire

La réconciliation des identifiants de lieux est traitée par **équivalence
additive** et non par migration : la forme canonique source-agnostique fait foi,
les identifiants hérités demeurent gelés et portent un pointeur `same_as` vers le
canonique, et la fusion s'opère à la lecture. Ce dispositif satisfait
simultanément le gel des schémas, l'exigence d'« un lieu physique = une entité
cartographique » et la propriété *cross-ready* requise par les étapes avales. Les
invariants de validation garantissent qu'aucune dérive ne pourra contourner le
gel de manière silencieuse.
