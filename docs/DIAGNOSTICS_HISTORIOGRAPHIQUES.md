# Diagnostics historiographiques

Le repo dispose désormais d’un moteur de diagnostics historiographiques.

Objectif :

- surveiller les dérives interprétatives ;
- détecter les atomes fragiles ;
- cartographier les mythes ;
- contrôler la densité théorique ;
- préparer un RAG historiographique.

---

# 1. Génération des exports

Toujours commencer par :

```bash
python tools/build_registers.py --strict
```

---

# 2. Génération des diagnostics

Lancer ensuite :

```bash
python tools/build_historiographical_diagnostics.py
```

Le fichier généré est :

```text
exports/generated/historiographical_diagnostics.json
```

---

# 3. Ce que le diagnostic détecte

## Atomes incomplets

Atomes sans champs v2 obligatoires.

---

## Atomes fragiles

Atomes marqués :

```text
fragile
hypothese
contesté
```

Ces atomes nécessitent une vigilance rédactionnelle.

---

## Mythes

Cartographie des atomes :

```text
type_unite: mythe
```

Permet de distinguer :

- reconstruction symbolique ;
- mémoire ;
- légende postérieure ;
- fait établi.

---

## Controverses

Cartographie des désaccords documentaires.

---

## Risques de surinterprétation

Repère les atomes :

```text
risque_surinterpretation:
  niveau: eleve | critique
```

Exemples typiques :

- lecture prophétique de Ian Curtis ;
- Manchester comme matrice absolue ;
- téléologie du post-punk.

---

## Densité théorique

Cartographie des atomes :

```text
nature_discursive:
  - theorique
```

Objectif :

- éviter les tunnels théoriques ;
- équilibrer narration et analyse.

---

## Motifs dominants

Détection automatique des motifs récurrents :

- spectralité ;
- ruine ;
- isolement ;
- fragmentation ;
- mémoire ouvrière ;
- froideur.

---

# 4. Usage stratégique

Les diagnostics ne servent pas seulement à vérifier.

Ils deviennent progressivement :

- un moteur éditorial ;
- un outil de supervision ;
- un système d’alerte historiographique.

Le repo évolue donc vers :

```text
un environnement de recherche assistée par IA
```

et non plus seulement un dépôt documentaire.
