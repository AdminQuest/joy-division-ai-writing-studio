# M2.10.3 - Retour de campagne sources longues

## 1. Objet du retour de campagne

Ce document restitue une campagne courte d'observation du prototype
`tools/m2_integrate_source.py`.

Objectif :

- executer le prototype sur des situations representatives du corpus Joy
  Division ;
- observer les decisions, bloquants, reserves et informations produits ;
- identifier les faux positifs et faux negatifs reels ;
- decider de l'avenir immediat du prototype.

Perimetre :

- pre-validation de sources longues ;
- lecture de `data/registre.json` ;
- sortie CLI en lecture seule ;
- observation qualitative.

Limites :

- aucune source canonique n'a ete creee ;
- aucun `Sxx` n'a ete attribue ;
- aucun dossier source n'a ete cree ;
- aucun atome, citation ou relation n'a ete genere ;
- aucune modification du prototype n'a ete effectuee.

Les executions ont ete realisees depuis la branche
`docs/m2-retour-campagne-sources-longues`.

## 2. Resultats detailles

### Cas A - Source reellement nouvelle

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `This Searing Light, the Sun and Everything Else: Joy Division: The Oral History` |
| `--author` | `Jon Savage` |
| `--type` | `livre` |
| `--year` | `2019` |
| `--reference` | `SAVAGE, Jon, This Searing Light, the Sun and Everything Else: Joy Division: The Oral History, London, Faber & Faber, 2019.` |

La source choisie ne correspond a aucune entree canonique titre/auteur dans
`data/registre.json`.

#### Decision

`pre-validee`

#### Bloquants

Aucun.

#### Reserves

Aucune.

#### Informations

- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/jon_savage_this_searing_light_the_sun_and_everything_else_joy_division_the_oral/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

Le resultat est utile. Le prototype reconnait une source absente du registre et
produit une proposition lisible sans bloquer ni ajouter de reserve artificielle.

La proposition de dossier source est comprehensible, mais elle est tronquee a la
limite du slug. Cette troncature ne bloque pas l'observation ; elle rappelle que
le dossier reste une proposition non attribuee.

### Cas B - Source deja presente

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures` |
| `--author` | `Mark Fisher` |
| `--type` | `livre` |
| `--year` | `2014` |
| `--reference` | `FISHER, Mark, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures, Winchester (UK) ; Washington (US), Zero Books, 2014, ISBN 978-1-78099-226-6.` |

Source canonique observee : `S90`.

#### Decision

`non pre-validee`

#### Bloquants

- `source deja presente de facon certaine: S90 - Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures (2014)`

#### Reserves

Aucune.

#### Informations

- `Sxx existant: S90`
- `dossier source probable: sources/fisher_ghosts_of_my_life/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

La detection est bonne. Le prototype bloque la source deja canonisee, indique le
bon `Sxx` et reprend le dossier source canonique existant.

Le diagnostic est actionnable : l'utilisateur comprend qu'il ne faut pas creer
un nouveau `Sxx`.

### Cas C - Reedition

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `Retromania: Pop Culture's Addiction to Its Own Past` |
| `--author` | `Simon Reynolds` |
| `--type` | `livre` |
| `--year` | `2012` |
| `--reference` | `REYNOLDS, Simon, Retromania: Pop Culture's Addiction to Its Own Past, Faber paperback edition, 2012.` |
| `--edition` | `Faber paperback 2012` |

Source proche attendue : `S91`, annee `2011`.

#### Decision

`pre-validee avec reserve`

#### Bloquants

Aucun.

#### Reserves

- `source proche detectee : autre edition ou reedition possible (S91 - Retromania: Pop Culture's Addiction to Its Own Past (2011))`

#### Informations

- `edition fournie: Faber paperback 2012`
- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/simon_reynolds_retromania_pop_culture_s_addiction_to_its_own_past/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

Le comportement est conforme au besoin d'observation. Le prototype ne bloque pas
la reedition, mais signale explicitement l'arbitrage humain a effectuer.

La reserve est utile : elle distingue une creation probable d'un cas a rattacher
eventuellement a `S91`.

### Cas D - Traduction ou variante linguistique

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `Rip It Up and Start Again: Postpunk 1978–1984` |
| `--author` | `Simon Reynolds` |
| `--type` | `livre` |
| `--year` | `2007` |
| `--reference` | `REYNOLDS, Simon, Rip It Up and Start Again: Postpunk 1978-1984, edition francaise, Paris, Editions Allia, 2007.` |
| `--edition` | `edition francaise Editions Allia 2007` |

Source proche attendue : `S72`, annee `2005/2006`.

#### Decision

`pre-validee avec reserve`

#### Bloquants

Aucun.

#### Reserves

- `source proche detectee : autre edition ou reedition possible (S72 - Rip It Up and Start Again: Postpunk 1978–1984 (2005/2006))`

#### Informations

- `edition fournie: edition francaise Editions Allia 2007`
- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/simon_reynolds_rip_it_up_and_start_again_postpunk_19781984/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

Le prototype detecte la proximite lorsque le titre reste proche du titre
canonique et que l'auteur correspond. Le cas est utile : il force un arbitrage
sur la relation entre edition francaise, variante linguistique et source
canonique `S72`.

Limite observee : ce cas ne demontre pas que le prototype saurait reconnaitre un
titre entierement traduit. La detection repose ici sur la proximite forte du
titre et sur l'auteur.

### Cas E - Metadonnees imparfaites

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `From Joy Division` |
| `--author` | `Middles` |
| `--type` | `livre` |
| `--year` | `1996` |
| `--reference` | `MIDDLES, From Joy Division, 1996.` |

Source proche attendue : `S74`, `Mick Middles`, `From Joy Division to New Order`.

#### Decision

`pre-validee`

#### Bloquants

Aucun.

#### Reserves

Aucune.

#### Informations

- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/middles_from_joy_division/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

Ce cas revele une faiblesse. La source candidate ressemble fortement a `S74`,
mais le prototype ne signale aucune reserve.

Le comportement est donc trop permissif pour des metadonnees imparfaites :
l'utilisateur pourrait croire qu'une nouvelle source est probable alors qu'un
rattachement ou une verification contre `S74` devrait etre signale.

Ce cas constitue le faux negatif le plus important de la campagne.

### Cas F - Titre court ou generique

#### Entree

| Parametre | Valeur |
| --- | --- |
| `--title` | `Joy Division` |
| `--author` | `Unknown Author` |
| `--type` | `livre` |
| `--year` | `2026` |
| `--reference` | `Unknown Author, Joy Division, reference de test pour observation, 2026.` |

Sources proches attendues possibles : `S09`, `S47`, `S68`.

#### Decision

`pre-validee avec reserve`

#### Bloquants

Aucun.

#### Reserves

- `source proche detectee : variante de titre (S09 - Joy Division (2010))`
- `source proche detectee : variante de titre (S47 - Joy Division (1984))`
- `source proche detectee : variante de titre (S68 - Joy Division (1988))`

#### Informations

- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/unknown_author_joy_division/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse

Le prototype reagit correctement a un titre tres generique. Les reserves sont
nombreuses, mais elles sont utiles : un titre `Joy Division` ne doit pas etre
accepte silencieusement sans verification humaine.

Ce cas peut etre vu comme un faux positif si la source etait reellement
distincte, mais il est acceptable : le risque documentaire d'un doublon est
eleve.

### Cas G - Critique ou recension

Deux executions ont ete faites pour observer deux situations differentes.

#### Entree G1 - Recension deja canonisee

| Parametre | Valeur |
| --- | --- |
| `--title` | `Retromania: Pop Culture's Addiction to Its Own Past (Book Review)` |
| `--author` | `James Weissinger` |
| `--type` | `article` |
| `--year` | `2012` |
| `--reference` | `WEISSINGER, James, Retromania: Pop Culture's Addiction to Its Own Past (Book Review), 2012.` |

Source canonique observee : `S94`.

#### Decision G1

`non pre-validee`

#### Bloquants G1

- `source deja presente de facon certaine: S94 - Retromania: Pop Culture's Addiction to Its Own Past (Book Review) (2012)`

#### Reserves G1

Aucune.

#### Informations G1

- `Sxx existant: S94`
- `dossier source probable: sources/james_weissinger_retromania_pop_culture_s_addiction_to_its_own_past_book_review/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse G1

Le prototype detecte correctement la recension deja canonisee. Il ne cherche pas
a evaluer la relation critique/source primaire, car la detection de doublon
certain suffit a bloquer.

#### Entree G2 - Recension avec titre abrege

| Parametre | Valeur |
| --- | --- |
| `--title` | `Retromania: Pop Culture's Addiction to Its Own Past` |
| `--author` | `James Weissinger` |
| `--type` | `article` |
| `--year` | `2012` |
| `--reference` | `WEISSINGER, James, Retromania: Pop Culture's Addiction to Its Own Past (Book Review), 2012.` |

Sources proches attendues : `S91` et `S94`.

#### Decision G2

`pre-validee avec reserve`

#### Bloquants G2

Aucun.

#### Reserves G2

- `source proche detectee : variante de titre (S91 - Retromania: Pop Culture's Addiction to Its Own Past (2011))`
- `source proche detectee : titre proche (S94 - Retromania: Pop Culture's Addiction to Its Own Past (Book Review) (2012))`

#### Informations G2

- `nouveau Sxx probablement requis: S95`
- `dossier source probable: sources/james_weissinger_retromania_pop_culture_s_addiction_to_its_own_past/`
- `lecture seule: aucun fichier cree ou modifie`

#### Analyse G2

Le prototype rapproche correctement la recension de la source primaire `S91` et
de la recension deja canonisee `S94`. Le diagnostic est utile, mais il laisse a
l'humain le soin de comprendre que le candidat est probablement une variante de
`S94`, pas une nouvelle source primaire.

## 3. Faux positifs observes

| Cas | Cause | Gravite | Impact | Appreciation |
| --- | --- | --- | --- | --- |
| Cas F | Titre tres generique `Joy Division` rapproche de `S09`, `S47` et `S68`. | Faible | Reserve supplementaire a examiner. | Acceptable. |
| Cas G2 | Recension abregee rapprochee aussi de la source primaire `S91`. | Faible a moyenne | L'utilisateur doit distinguer recension et source primaire. | Acceptable. |

Ces faux positifs ou quasi-faux positifs sont preferables a une acceptation
silencieuse. Ils augmentent le cout de lecture, mais reduisent le risque de
doublon documentaire.

## 4. Faux negatifs observes

| Cas | Cause | Gravite | Impact | Appreciation |
| --- | --- | --- | --- | --- |
| Cas E | Titre abrege `From Joy Division` et auteur incomplet `Middles` non rapproches de `S74`. | Moyenne a forte | Le prototype propose une source nouvelle probable alors qu'une source canonique proche existe. | Problematique. |

Le cas E montre que les metadonnees imparfaites restent le point fragile du
prototype.

## 5. Qualite des diagnostics

La lisibilite generale est bonne :

- les decisions sont explicites ;
- les bloquants sont separes des reserves ;
- les informations rappellent toujours la lecture seule ;
- les sources proches sont nommees avec `Sxx`, titre et annee.

L'utilite est bonne pour :

- source deja presente ;
- reedition ;
- variante proche ;
- titre generique ;
- critique ou recension proche.

Le caractere actionnable est insuffisant dans le cas des metadonnees
imparfaites. Le prototype ne signale pas toujours une proximite lorsqu'un titre
est abrege.

## 6. Qualite des propositions

### Sxx proposes

Le `Sxx` probable affiche est `S95` pour les nouvelles sources candidates,
coherent avec l'etat courant du registre observe pendant la campagne.

La formulation `probable, non attribue` reste claire.

### Dossiers sources proposes

Les dossiers sources proposes sont lisibles et deterministes.

Points observes :

- le dossier canonique `sources/fisher_ghosts_of_my_life/` est bien repris pour
  `S90` ;
- les nouveaux dossiers probables sont comprehensibles ;
- les titres longs produisent des slugs tronques, comme dans le cas A ;
- les caracteres typographiques comme le tiret long peuvent disparaitre dans le
  slug, comme dans le cas D.

Ces limites sont acceptables pour une proposition preparatoire.

### Reserves

Les reserves sont utiles dans les cas C, D, F et G2.

Elles remplissent leur role : signaler un arbitrage humain sans bloquer
automatiquement.

### Informations

Les informations sont stables et utiles :

- edition fournie ;
- `Sxx` existant ou probable ;
- dossier source probable ;
- rappel de lecture seule.

## 7. Enseignements

Ce qui fonctionne :

- detection d'une source deja canonisee ;
- detection d'une reedition probable ;
- detection d'une variante proche lorsque titre et auteur restent fortement
  comparables ;
- reserves utiles sur titres generiques ;
- detection de recension proche lorsqu'une variante du titre est fournie ;
- sortie deterministe et relisible.

Ce qui surprend :

- un titre incomplet mais tres suggestif peut passer sans reserve ;
- une recension abregee remonte a la fois la source primaire et la recension
  deja canonisee, ce qui est utile mais demande une lecture attentive.

Ce qui reste fragile :

- titres abreges ;
- auteurs incomplets ;
- traductions dont le titre serait completement traduit ;
- distinction fine entre source primaire, recension et variante de recension.

## 8. Limites observees

Limites reellement constatees pendant la campagne :

- le prototype ne detecte pas `S74` avec le titre abrege `From Joy Division` et
  l'auteur incomplet `Middles` ;
- les slugs de dossiers longs sont tronques ;
- les slugs ne conservent pas toujours visiblement les separateurs
  typographiques ;
- les reserves peuvent melanger source primaire et recension dans le cas d'un
  titre abrege ;
- la reconnaissance d'une traduction n'a ete observee que lorsque le titre reste
  proche du titre canonique.

## 9. Decision

```text
amelioration
```

## 10. Justification

Le prototype apporte une valeur documentaire reelle et doit etre conserve.

Il detecte correctement :

- les sources deja presentes ;
- les reeditions probables ;
- les variantes proches ;
- les titres generiques a risque ;
- les recensions proches.

Cependant, la campagne a observe un faux negatif problematique sur les
metadonnees imparfaites. Le cas `From Joy Division` / `Middles` aurait du
produire au moins une reserve vers `S74`.

La decision retenue est donc `amelioration`, et non `stabilisation`.

L'extension fonctionnelle n'est pas justifiee a ce stade : le prototype doit
d'abord mieux signaler les proximites faibles mais documentaires, notamment sur
titres abreges et auteurs incomplets.
