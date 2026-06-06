# M2.10 - Retour d'usage V1 du prototype d'integration de source longue

## 1. Objet du retour d'usage

Ce document evalue le comportement reel du prototype
`tools/m2_integrate_source.py`.

Le prototype a ete developpe pour tester le premier flux M2.3 en lecture seule.
Il ne cree pas de source canonique, ne modifie pas `data/registre.json`, ne cree
pas de dossier `sources/<slug>/`, ne genere pas d'atomes, de citations ou de
relations, et n'ouvre pas de PR.

Question evaluee :

```text
Cette source peut-elle etre integree proprement dans le corpus ?
```

Le prototype produit :

- un diagnostic ;
- une decision de pre-validation ;
- une proposition de `Sxx` existant ou probable ;
- un dossier source probable ;
- une liste de fichiers potentiellement concernes.

## 2. Cas d'essai realises

Les essais ci-dessous ont ete executes sur l'etat courant du depot.

### Cas conforme

Commande :

```bash
python3 tools/m2_integrate_source.py --title "M2 Integration Prototype Source" --author "Prototype Author" --type livre --year 2026 --reference "Prototype Author, M2 Integration Prototype Source, Test Press, 2026."
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| decision | `pre-validee` |
| bloquants | aucun |
| reserves | aucune |
| Sxx probable | `S95` |
| dossier source probable | `sources/prototype_author_m2_integration_prototype_source/` |

Lecture :

Le prototype reconnait une source nouvelle identifiable, propose un prochain
`Sxx` probable et un dossier source probable, sans creer aucun fichier.

### Source deja presente

Commande :

```bash
python3 tools/m2_integrate_source.py --title "Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures" --author "Mark Fisher" --type livre --year 2014 --reference "FISHER, Mark, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures, Winchester (UK) ; Washington (US), Zero Books, 2014, ISBN 978-1-78099-226-6."
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| decision | `non pre-validee` |
| bloquant | `source deja presente de facon certaine: S90 - Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures (2014)` |
| Sxx existant | `S90` |
| reserves | aucune |

Lecture :

Le prototype bloque une source deja canonique. Il identifie le `Sxx` existant et
ne propose pas de creation effective.

### Source proche

Commande :

```bash
python3 tools/m2_integrate_source.py --title "Retromania: Pop Culture's Addiction to Its Own Past" --author "Simon Reynolds" --type livre --year 2012 --reference "REYNOLDS, Simon, Retromania: Pop Culture's Addiction to Its Own Past, Faber paperback edition, 2012." --edition "Faber paperback 2012"
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| decision | `pre-validee avec reserve` |
| bloquants | aucun |
| reserve | `source proche detectee : autre edition ou reedition possible (S91 - Retromania: Pop Culture's Addiction to Its Own Past (2011))` |
| Sxx probable | `S95` |
| dossier source probable | `sources/simon_reynolds_retromania_pop_culture_s_addiction_to_its_own_past/` |

Lecture :

Le prototype ne bloque pas automatiquement une autre edition possible. Il expose
la proximite comme reserve, ce qui correspond au contrat M2.3 : l'humain doit
decider s'il s'agit d'une nouvelle source, d'une edition a rattacher ou d'une
mise a jour de `S91`.

### Type invalide

Commande :

```bash
python3 tools/m2_integrate_source.py --title "M2 Integration Prototype Source" --author "Prototype Author" --type blog --year 2026 --reference "Prototype Author, M2 Integration Prototype Source, Test Press, 2026."
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| decision | `non pre-validee` |
| bloquant | `type documentaire inconnu: blog` |
| reserves | aucune |

Lecture :

Le prototype limite bien les types au vocabulaire M2.3 :

- `livre`
- `article`
- `interview`
- `fanzine`
- `archive`
- `memoire`
- `these`
- `dossier documentaire`

## 3. Valeur documentaire reelle

Le prototype apporte une valeur documentaire par rapport a une integration
manuelle immediate.

Gains observes :

- verification rapide contre `data/registre.json` ;
- detection d'une source deja presente ;
- detection d'une edition ou reedition proche ;
- proposition d'un prochain `Sxx` probable sans attribution effective ;
- proposition d'un dossier source probable ;
- classification claire en `bloquant`, `reserve` et `information` ;
- sortie deterministe et relisible.

Risques evites :

- creation d'un doublon `Sxx` ;
- confusion entre source canonique et dossier source ;
- ouverture trop rapide d'une integration documentaire large ;
- traitement d'un type hors contrat M2.3.

## 4. Limites observees

Limites reelles du prototype V1 :

- la detection de source proche reste heuristique ;
- le prochain `Sxx` est seulement probable et peut changer si le registre evolue ;
- le dossier source probable est derive automatiquement du titre et de l'auteur ;
- le prototype ne juge pas la qualite historiographique de la source ;
- le prototype ne decide pas si une autre edition doit devenir un nouveau `Sxx` ;
- le prototype ne prepare pas encore d'atomes, citations, relations ou patchs ;
- le prototype ne verifie pas les droits ou la disponibilite effective du fichier source.

Ces limites sont coherentes avec le perimetre : diagnostic preparatoire en
lecture seule.

## 5. Decision d'usage

Le prototype repond-il au besoin initial ?

Oui, pour une premiere pre-validation M2.3 limitee.

Il permet de determiner si une source candidate est :

- nouvelle et pre-validable ;
- deja presente et donc bloquante ;
- proche d'une source existante et donc a arbitrer ;
- hors vocabulaire M2.3.

Il ne suffit pas encore a piloter une integration documentaire complete.

## 6. Recommandation

Conserver le prototype comme premier outil de diagnostic M2.3.

Suite recommandee :

- ne pas etendre immediatement vers la generation d'atomes ;
- utiliser le prototype sur quelques sources longues reelles ;
- documenter les faux positifs et faux negatifs de proximite ;
- renforcer ensuite, si necessaire, la detection des editions, traductions et
  reeditions.

La prochaine evolution doit rester preparatoire et lecture seule tant que les
cas d'usage reels n'ont pas ete suffisamment observes.
