# M2.10 - CLI d'integration documentaire de source longue

## Objectif

`tools/m2_integrate_source.py` prepare un diagnostic local pour une source
longue candidate.

La question traitee est :

```text
Cette source peut-elle etre integree proprement dans le corpus ?
```

Le prototype produit un diagnostic et une proposition. Il ne realise aucune
integration effective.

## Perimetre

Le prototype applique le contrat M2.3 :

- qualification minimale d'une source candidate ;
- comparaison avec `data/registre.json` ;
- detection d'une source deja presente ;
- detection d'une source proche ;
- proposition d'un `Sxx` probable si la source semble nouvelle ;
- proposition d'un dossier source probable ;
- classification en `bloquant`, `reserve` et `information`.

Le prototype reste en lecture seule.

Il ne cree pas :

- source canonique ;
- entree dans `data/registre.json` ;
- dossier `sources/<slug>/` ;
- atomes ;
- citations ;
- relations ;
- branche ;
- Pull Request.

## Parametres

Parametres obligatoires :

| Parametre | Role |
| --- | --- |
| `--title` | Titre de la source candidate. |
| `--author` | Auteur, autrice ou responsable documentaire. |
| `--type` | Type documentaire M2.3. |
| `--year` | Annee ou date principale. |
| `--reference` | Reference complete ou description bibliographique equivalente. |

Parametres facultatifs :

| Parametre | Role |
| --- | --- |
| `--url` | URL utile a l'identification. |
| `--edition` | Edition, version ou tirage consulte. |
| `--publication` | Revue, fanzine, archive ou support parent. |
| `--pages-useful` | Pages utiles ou pagination traitee. |
| `--section-useful` | Section, chapitre ou partie utile. |

Types autorises :

- `livre`
- `article`
- `interview`
- `fanzine`
- `archive`
- `memoire`
- `these`
- `dossier documentaire`

L'alias CLI `dossier_documentaire` est accepte et normalise en
`dossier documentaire`.

## Exemples

### Source nouvelle

```bash
python3 tools/m2_integrate_source.py \
  --title "M2 Integration Prototype Source" \
  --author "Prototype Author" \
  --type livre \
  --year 2026 \
  --reference "Prototype Author, M2 Integration Prototype Source, Test Press, 2026."
```

Resultat attendu :

- decision `pre-validee` ;
- aucun bloquant ;
- aucun reserve ;
- nouveau `Sxx` probable ;
- dossier source probable.

### Source deja presente

```bash
python3 tools/m2_integrate_source.py \
  --title "Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures" \
  --author "Mark Fisher" \
  --type livre \
  --year 2014 \
  --reference "FISHER, Mark, Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures, Winchester (UK) ; Washington (US), Zero Books, 2014, ISBN 978-1-78099-226-6."
```

Resultat attendu :

- decision `non pre-validee` ;
- bloquant `source deja presente de facon certaine` ;
- `Sxx` existant affiche.

### Source proche

```bash
python3 tools/m2_integrate_source.py \
  --title "Retromania: Pop Culture's Addiction to Its Own Past" \
  --author "Simon Reynolds" \
  --type livre \
  --year 2012 \
  --reference "REYNOLDS, Simon, Retromania: Pop Culture's Addiction to Its Own Past, Faber paperback edition, 2012." \
  --edition "Faber paperback 2012"
```

Resultat attendu :

- decision `pre-validee avec reserve` ;
- reserve signalant une autre edition ou reedition possible ;
- aucun bloquant.

### Type invalide

```bash
python3 tools/m2_integrate_source.py \
  --title "M2 Integration Prototype Source" \
  --author "Prototype Author" \
  --type blog \
  --year 2026 \
  --reference "Prototype Author, M2 Integration Prototype Source, Test Press, 2026."
```

Resultat attendu :

- decision `non pre-validee` ;
- bloquant `type documentaire inconnu`.

## Sortie

La sortie contient :

- decision ;
- bloquants ;
- reserves ;
- informations ;
- proposition.

La proposition affiche :

- type documentaire ;
- source probable ;
- `Sxx` existant ou probable ;
- dossier source probable ;
- fichiers potentiellement concernes ;
- metadonnees candidates.

Les fichiers potentiellement concernes sont informatifs. Le prototype ne les
modifie pas.

## Limites

Le prototype ne juge pas :

- la qualite historiographique de la source ;
- la suffisance de la source pour une atomisation ;
- les droits de reproduction ;
- la validite d'une citation ;
- la pertinence d'une relation documentaire ;
- la decision d'ajouter un `Sxx`.

Les detections de proximite sont heuristiques. Une reserve indique un arbitrage
humain necessaire, pas une decision automatique.

## Lien avec M2.3

M2.3 decrit le flux complet :

```text
source longue
  ->
source canonique
  ->
dossier source
  ->
propositions documentaires
  ->
pre-validation
  ->
controles
  ->
PR
  ->
validation humaine
```

Ce prototype ne couvre que la premiere pre-validation :

- la source semble-t-elle nouvelle ?
- existe-t-elle deja ?
- est-elle proche d'une source canonique ?
- peut-on proposer un dossier source probable ?

L'integration effective reste hors perimetre.
