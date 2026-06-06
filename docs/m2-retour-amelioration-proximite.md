# M2.10.4 - Retour d'amelioration de proximite des sources longues

## 1. Objet

Ce document restitue l'amelioration ciblee de la detection de proximite dans
`tools/m2_integrate_source.py`.

Le retour de campagne M2.10.3 avait observe un faux negatif :

```text
titre  : From Joy Division
auteur : Middles
annee  : 1996
```

Cette entree n'etait pas rapprochee de :

```text
S74 - Mick Middles - From Joy Division to New Order (1996)
```

L'objectif de M2.10.4 est de mieux signaler les proximites faibles mais
documentaires, sans transformer ces indices en doublons certains.

## 2. Modification realisee

La detection distingue maintenant :

- auteur certain ;
- auteur proche ;
- titre partiel significatif ;
- doublon certain ;
- proximite documentaire.

Un auteur patronymique seul comme `Middles` n'est pas une preuve de doublon.
Il peut cependant contribuer a une reserve lorsqu'il est combine a un titre
partiel significatif.

Un titre abrege comme `From Joy Division` peut etre rapproche de
`From Joy Division to New Order` si la partie commune est suffisamment longue et
documentairement significative.

Aucune dependance externe, logique IA ou similarite opaque n'a ete introduite.

## 3. Cas testes

### Cas S74 - auteur partiel et titre abrege

Entree :

```text
--title From Joy Division
--author Middles
--type livre
--year 1996
--reference MIDDLES, From Joy Division, 1996.
```

Resultat avant amelioration :

```text
Decision : pre-validee
Reserves : aucun
```

Resultat apres amelioration :

```text
Decision : pre-validee avec reserve
Reserves :
- source proche detectee : metadonnees partielles possibles (S74 - Mick Middles - From Joy Division to New Order (1996))
```

Analyse :

Le faux negatif principal est corrige. Le prototype ne bloque pas la proposition
et conserve l'arbitrage humain.

### Cas auteur patronymique seul

Entree testee :

```text
--title From Joy Division to New Order
--author Middles
--year 1996
```

Resultat observe :

```text
Decision : pre-validee avec reserve
```

Analyse :

Le patronyme seul est traite comme un indice faible. Il ne produit pas de
doublon certain, meme lorsque le titre est exact.

### Cas titre abrege seul

Entree testee :

```text
--title From Joy Division
--author Mick Middles
--year 1996
```

Resultat observe :

```text
Decision : pre-validee avec reserve
```

Analyse :

Le titre partiel significatif suffit a produire une reserve lorsqu'il est
combine a un auteur proche.

### Cas S90 - source deja presente

Entree :

```text
Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures
Mark Fisher
2014
```

Resultat observe :

```text
Decision : non pre-validee
Bloquant : source deja presente de facon certaine: S90
```

Analyse :

Pas de regression. Le doublon certain reste bloquant.

### Cas S91 - reedition

Entree :

```text
Retromania: Pop Culture's Addiction to Its Own Past
Simon Reynolds
2012
```

Resultat observe :

```text
Decision : pre-validee avec reserve
Reserve : autre edition ou reedition possible (S91)
```

Analyse :

Pas de regression. La reedition reste soumise a reserve.

### Cas S72 - variante linguistique ou edition

Entree :

```text
Rip It Up and Start Again: Postpunk 1978-1984
Simon Reynolds
2007
```

Resultat observe :

```text
Decision : pre-validee avec reserve
Reserve : autre edition ou reedition possible (S72)
```

Analyse :

Pas de regression. Le rapprochement vers `S72` reste conserve.

### Cas S94 - recension deja canonisee

Entree :

```text
Retromania: Pop Culture's Addiction to Its Own Past (Book Review)
James Weissinger
2012
```

Resultat observe :

```text
Decision : non pre-validee
Bloquant : source deja presente de facon certaine: S94
```

Analyse :

Pas de regression. La recension deja canonisee reste detectee comme source
presente.

### Cas titre generique

Entree :

```text
Joy Division
Unknown Author
2026
```

Resultat observe :

```text
Decision : pre-validee avec reserve
Reserves :
- S09
- S47
- S68
```

Analyse :

Pas de regression. Le titre generique reste soumis a reserve et n'est pas
transforme en doublon certain.

## 4. Faux positifs observes

Aucun nouveau faux positif bloquant n'a ete observe.

Le titre generique `Joy Division` continue a produire plusieurs reserves. Ce
comportement etait deja attendu et reste acceptable : il augmente le cout de
lecture, mais il evite une acceptation silencieuse sur un titre a fort risque de
doublon.

## 5. Faux negatifs restants

Le faux negatif `From Joy Division` / `Middles` vers `S74` est corrige.

Faux negatifs encore possibles :

- titre tres court ;
- titre entierement traduit ;
- auteur tres incomplet de moins de cinq caracteres ;
- source proche uniquement par reference bibliographique partielle.

Ces limites n'ont pas ete corrigees dans M2.10.4 afin de conserver une logique
simple, deterministe et explicable.

## 6. Decision

L'amelioration est jugee acceptable pour le perimetre M2.10.4.

Le prototype reste :

- en lecture seule ;
- preparatoire ;
- soumis a validation humaine ;
- sans attribution automatique de `Sxx`.

La prochaine decision peut revenir a une stabilisation documentaire si aucune
nouvelle campagne n'observe de faux negatif majeur.
