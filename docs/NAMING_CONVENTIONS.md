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
