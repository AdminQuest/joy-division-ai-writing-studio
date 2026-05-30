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

# 10. Lieux (registre des lieux — étape 12b-1.c)

Forme canonique **gelée** :

```text
PLACE-<SLUG>
```

où `<SLUG>` est **source-agnostique** : il décrit le lieu physique, jamais la
source qui le documente. Un même lieu attesté par plusieurs sources porte **un
seul** identifiant canonique.

### Règle de canonicalisation (déterministe)

Le slug se dérive du nom canonique du lieu :

1. translittération ASCII (accents retirés : *Haçienda* → `HACIENDA`) ;
2. apostrophes et ponctuation supprimées (*King's School* → `KINGS-SCHOOL`) ;
3. espaces et séparateurs → tiret unique ; mise en MAJUSCULES ;
4. pas de préfixe de source (`S35`, `S41`…) ni de compteur positionnel
   (`-001`) dans un identifiant canonique.

Conforme au motif du schéma : `^PLACE-[A-Z0-9][A-Z0-9-]*$`.

### Formes legacy tolérées (gel = pas de renommage)

Antérieures à la règle, **conservées telles quelles** (le gel interdit le
renommage des identifiants stabilisés) :

- scoping-source : `PLACE-S41-TJ-DAVIDSONS-LITTLE-PETER-STREET` ;
- positionnel : `PLACE-S83-001`.

Elles restent valides et référençables. On **ne les renomme pas** ; on les
rattache au canonique par une arête d'équivalence (ci-dessous).

### `same_as` — arête d'équivalence (cross-ready, étape 5)

Quand un enregistrement legacy décrit le **même lieu physique** qu'un
identifiant canonique, il porte :

```yaml
same_as: PLACE-<SLUG-CANONIQUE>
```

Règles (imposées par `tools/validate_places.py`, résolues par
`apps/lib/dynamic-registers.js`) :

- **append-only** : `same_as` est porté par le legacy ; le canonique n'est
  jamais muté et ne porte pas de `same_as` (il est son propre point fixe) ;
- **cible existante** : la cible est un identifiant de lieu présent ;
- **absence de cycle** ; le loader résout la **clôture transitive** (union-find)
  et fusionne la composante sur son canonique ;
- les enrichissements transversaux (coordonnées, futurs liens concerts/maillage)
  s'attachent **au canonique**, après réconciliation.

`same_as` est l'arête d'équivalence inter-registres de référence : la
spécification cross-registres (étape 5) la reprend telle quelle.

Spécification détaillée : `docs/conventions/identifiants_lieux.md`.
