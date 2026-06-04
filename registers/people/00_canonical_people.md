# Registre canonique des acteurs — `PERSON-`

> **Étape 9 — canonicalisation.** Identités canoniques des personnes, construites par `tools/build_people_canon.py` à partir de la couche provisoire `PERS-*` (`exports/generated/people.json`).
> **Gel additif** : chaque `PERS-*` est conservé tel quel et rabattu ici via `same_as` ; aucun id provisoire n'est renommé ni supprimé.
> **SSOT** : ce fichier est GÉNÉRÉ. Ne pas l'éditer à la main — modifier le générateur, puis `python3 tools/build_people_canon.py`. La sentinelle anti-drift (`tools/validate_people.py --check-drift`) rejoue le générateur et échoue sur toute divergence.
> **Schéma** : [`schemas/person_canonical.schema.json`](../../schemas/person_canonical.schema.json) (Draft 2020-12).

## Statistiques

| Indicateur | Valeur |
|------------|:------:|
| `PERSON-` canoniques | 167 |
| Liens `same_as` câblés (ids `PERS-*` rabattus) | 299 |
| `alt_names` (formes secondaires) | 25 |
| Renvois `ORG-` (hand-off) | 4 |
| Renvois concept (hand-off) | 1 |
| Items `a_arbitrer` | 4 |
| `categorie_a_arbitrer` (double appartenance) | 52 |

## Répartition par `categorie`

| Catégorie | Nb |
|-----------|:--:|
| entourage | 53 |
| industrie | 44 |
| auteur_secondaire | 29 |
| theoricien_mobilise | 14 |
| critique_journaliste | 12 |
| influence | 11 |
| membre | 4 |

---

# Identités canoniques

## PERSON-abby-fuoto — Abby Fuoto

```yaml
id: PERSON-abby-fuoto
type_unite: person
name: Abby Fuoto
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-002
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-aby-warburg — Aby Warburg

```yaml
id: PERSON-aby-warburg
type_unite: person
name: Aby Warburg
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S51
same_as:
  - PERS-S51-004
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-alan-erasmus — Alan Erasmus

```yaml
id: PERSON-alan-erasmus
type_unite: person
name: Alan Erasmus
categorie: industrie
role:
  - cofondateur Factory
  - organisateur
  - figure effacée du récit
  - acteur
  - cofondateur du dispositif Factory avec Tony Wilson
  - promoteur initial au Russell Club
sources:
  - S75
  - S76
  - S31
same_as:
  - PERS-S31-006
  - PERS-S75-024
  - PERS-S76-045
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-alan-hempsall — Alan Hempsall

```yaml
id: PERSON-alan-hempsall
type_unite: person
name: Alan Hempsall
categorie: entourage
role:
  - chanteur de Crispy Ambulance
  - substitut vocal ponctuel à Derby Hall
  - voix de substitution au Derby Hall de Bury
sources:
  - S75
  - S76
same_as:
  - PERS-S75-035
  - PERS-S76-080
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-alan-wise — Alan Wise

```yaml
id: PERSON-alan-wise
type_unite: person
name: Alan Wise
categorie: industrie
role:
  - promoteur local
  - gestionnaire des soirées au Russell Club selon S76
  - témoin du rôle visuel de Peter Saville
  - promoteur / acteur Factory Club
  - témoin de l’épilepsie de Curtis
  - lui-même sujet à des attaques de petit mal selon S76
sources:
  - S76
same_as:
  - PERS-S76-047
  - PERS-S76-054
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-alessandro-gnocchi — Alessandro Gnocchi

```yaml
id: PERSON-alessandro-gnocchi
type_unite: person
name: Alessandro Gnocchi
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S54
same_as:
  - PERS-S54-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-andrea-rabbito — Andrea Rabbito

```yaml
id: PERSON-andrea-rabbito
type_unite: person
name: Andrea Rabbito
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S52
same_as:
  - PERS-S52-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-andy-zero — Andy Zero

```yaml
id: PERSON-andy-zero
type_unite: person
name: Andy Zero
categorie: critique_journaliste
role:
  - acteur
sources:
  - S21
  - S77
same_as:
  - PERS-S21-003
  - PERS-S77-007
alt_names:
  - Andy Waide
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-annik-honore — Annik Honoré

```yaml
id: PERSON-annik-honore
type_unite: person
name: Annik Honoré
categorie: industrie
role:
  - proche
  - témoin
  - relation intime de Ian Curtis
  - figure de la crise biographique finale
  - journaliste/fanzine En Attendant
  - future cofondatrice liée à Factory Benelux / Les Disques du Crépuscule
  - médiatrice européenne
  - relation intime de Ian Curtis pendant la tournée européenne
sources:
  - S45
  - S75
  - S76
  - S52
  - S54
same_as:
  - PERS-010
  - PERS-S52-012
  - PERS-S54-007
  - PERS-S75-032
  - PERS-S76-063
  - PERS-S76-067
  - PERS-S76-070
alt_names:
  - Annick Honoré
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-anton-corbijn — Anton Corbijn

```yaml
id: PERSON-anton-corbijn
type_unite: person
name: Anton Corbijn
categorie: industrie
role:
  - acteur
sources:
  - S29
  - S52
  - S53
  - S78
same_as:
  - PERS-S29-011
  - PERS-S52-002
  - PERS-S53-005
  - PERS-S78-007
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-arthur-schopenhauer — Arthur Schopenhauer

```yaml
id: PERSON-arthur-schopenhauer
type_unite: person
name: Arthur Schopenhauer
categorie: influence
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-009
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-barbara-lloyd — Barbara Lloyd

```yaml
id: PERSON-barbara-lloyd
type_unite: person
name: Barbara Lloyd
categorie: entourage
role:
  - tante de Ian Curtis
  - témoin familial
sources:
  - S76
same_as:
  - PERS-S76-005
alt_names:
  - Aunt Barbara
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-benjamin-fraser — Benjamin Fraser

```yaml
id: PERSON-benjamin-fraser
type_unite: person
name: Benjamin Fraser
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bernard-pierre-wolff — Bernard Pierre Wolff

```yaml
id: PERSON-bernard-pierre-wolff
type_unite: person
name: Bernard Pierre Wolff
categorie: industrie
role:
  - photographe associé à la pochette de *Closer*
sources:
  - S76
same_as:
  - PERS-S76-079
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bernard-sumner — Bernard Sumner

```yaml
id: PERSON-bernard-sumner
type_unite: person
name: Bernard Sumner
categorie: membre
role:
  - musicien
  - guitariste
  - témoin
  - trajectoire sociale
sources:
  - S41
  - S45
  - S75
  - S52
  - S55
  - S58
same_as:
  - PERS-003
  - PERS-003-S75
  - PERS-S45-BERNARD-SUMNER-TABLETS
  - PERS-S52-006
  - PERS-S55-004
  - PERS-S58-003
alt_names:
  - Bernard Albrecht
  - Bernard Dicken
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bernie-binnick — Bernie Binnick

```yaml
id: PERSON-bernie-binnick
type_unite: person
name: Bernie Binnick
categorie: industrie
role:
  - exécutif américain lié au projet Grapevine/RCA
  - producteur de soul destiné à l’export britannique
sources:
  - S45
  - S76
same_as:
  - PERS-S45-BERNIE-BINNICK
  - PERS-S76-036
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bob-auger — Bob Auger

```yaml
id: PERSON-bob-auger
type_unite: person
name: Bob Auger
categorie: industrie
role:
  - producteur
  - ingénieur / superviseur studio
  - ingénieur / acteur technique des sessions Arrow selon S76
sources:
  - S75
  - S76
same_as:
  - PERS-S75-020
  - PERS-S76-035
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bob-dickinson — Bob Dickinson

```yaml
id: PERSON-bob-dickinson
type_unite: person
name: Bob Dickinson
categorie: industrie
role:
  - journaliste local
  - DJ à Rafters
  - témoin du Stiff Test / Chiswick Challenge
sources:
  - S76
same_as:
  - PERS-S76-028
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-bob-jones — Bob Jones

```yaml
id: PERSON-bob-jones
type_unite: person
name: Bob Jones
categorie: industrie
role:
  - acteur
sources:
  - S84
same_as:
  - PERS-S84-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bob-krasnow — Bob Krasnow

```yaml
id: PERSON-bob-krasnow
type_unite: person
name: Bob Krasnow
categorie: industrie
role:
  - vice-président A&R Warner Brothers
  - "interlocuteur d'une occasion américaine manquée"
sources:
  - S75
same_as:
  - PERS-S75-034
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-bob-stanley — Bob Stanley

```yaml
id: PERSON-bob-stanley
type_unite: person
name: Bob Stanley
categorie: entourage
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-007
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-brion-gysin — Brion Gysin

```yaml
id: PERSON-brion-gysin
type_unite: person
name: Brion Gysin
categorie: influence
role:
  - acteur
sources:
  - S54
same_as:
  - PERS-S54-005
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-candy — Candy

```yaml
id: PERSON-candy
type_unite: person
name: Candy
categorie: entourage
role:
  - chien de Ian Curtis
  - élément domestique de la crise conjugale
sources:
  - S45
  - S76
same_as:
  - PERS-S45-CANDY
  - PERS-S76-076
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-carole-curtis — Carole Curtis

```yaml
id: PERSON-carole-curtis
type_unite: person
name: Carole Curtis
categorie: entourage
role:
  - sœur de Ian Curtis
  - témoin familial
  - mémoire familiale endeuillée
sources:
  - S76
same_as:
  - PERS-S76-004
  - PERS-S76-087
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-cath-carroll — Cath Carroll

```yaml
id: PERSON-cath-carroll
type_unite: person
name: Cath Carroll
categorie: critique_journaliste
role:
  - acteur
sources:
  - S21
  - S77
same_as:
  - PERS-S21-002
  - PERS-S77-006
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-charles-salem — Charles Salem

```yaml
id: PERSON-charles-salem
type_unite: person
name: Charles Salem
categorie: industrie
role:
  - acteur
sources:
  - S78
same_as:
  - PERS-S78-008
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-chris-ott — Chris Ott

```yaml
id: PERSON-chris-ott
type_unite: person
name: Chris Ott
categorie: auteur_secondaire
role:
  - critique
  - auteur
  - essayiste
sources:
  - S75
same_as:
  - PERS-013
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-christian-norberg-schulz — Christian Norberg-Schulz

```yaml
id: PERSON-christian-norberg-schulz
type_unite: person
name: Christian Norberg-Schulz
categorie: entourage
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-008
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-clinton-heylin — Clinton Heylin

```yaml
id: PERSON-clinton-heylin
type_unite: person
name: Clinton Heylin
categorie: critique_journaliste
role:
  - biographe musical
  - "témoin d'une interaction conflictuelle à Rare Records"
sources:
  - S76
same_as:
  - PERS-S76-013
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-colin-malcolm — Colin Malcolm

```yaml
id: PERSON-colin-malcolm
type_unite: person
name: Colin Malcolm
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-cosey-fanni-tutti — Cosey Fanni Tutti

```yaml
id: PERSON-cosey-fanni-tutti
type_unite: person
name: Cosey Fanni Tutti
categorie: entourage
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-004
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-daniel-odier — Daniel Odier

```yaml
id: PERSON-daniel-odier
type_unite: person
name: Daniel Odier
categorie: influence
role:
  - acteur
sources:
  - S54
same_as:
  - PERS-S54-008
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-dave-mccullough — Dave McCullough

```yaml
id: PERSON-dave-mccullough
type_unite: person
name: Dave McCullough
categorie: critique_journaliste
role:
  - journaliste musical pour Sounds
  - critique de Joy Division autour d’Unknown Pleasures et Stuff the Superstars
sources:
  - S76
same_as:
  - PERS-S76-062
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-dave-pils — Dave Pils

```yaml
id: PERSON-dave-pils
type_unite: person
name: Dave Pils
categorie: industrie
role:
  - roadie londonien / relais pratique pendant les sessions *Closer*
sources:
  - S76
same_as:
  - "PERS-S76-064#dave-pils"
  - PERS-S76-077
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-david-bowie — David Bowie

```yaml
id: PERSON-david-bowie
type_unite: person
name: David Bowie
categorie: influence
role:
  - artiste formateur pour Ian Curtis
  - figure glam et scénique pré-punk
sources:
  - S76
same_as:
  - PERS-S76-010
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-david-byrne — David Byrne

```yaml
id: PERSON-david-byrne
type_unite: person
name: David Byrne
categorie: influence
role:
  - acteur
sources:
  - S49
same_as:
  - PERS-S49-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-david-harvey — David Harvey

```yaml
id: PERSON-david-harvey
type_unite: person
name: David Harvey
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-008
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-david-haslam — David Haslam

```yaml
id: PERSON-david-haslam
type_unite: person
name: David Haslam
categorie: industrie
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-004
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-dean — Dean

```yaml
id: PERSON-dean
type_unite: person
name: Dean
categorie: entourage
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-DEAN-CHECK-INN
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-deborah-curtis — Deborah Curtis

```yaml
id: PERSON-deborah-curtis
type_unite: person
name: Deborah Curtis
categorie: auteur_secondaire
role:
  - témoin
  - proche
  - autrice
  - gardienne d’archive
  - future épouse de Ian Curtis
  - témoin intime central par S45
  - personnage biographique structurant dans S76
sources:
  - S45
  - S76
  - S52
same_as:
  - PERS-005
  - PERS-S45-DEBORAH-CURTIS-LOGISTIQUE-FORMATION
  - PERS-S45-DEBORAH-CURTIS-TEMOIN-POLITIQUE-DOMESTIQUE
  - PERS-S52-005
  - PERS-S76-009
alt_names:
  - Deborah Woodruff
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-derek-brandwood — Derek Brandwood

```yaml
id: PERSON-derek-brandwood
type_unite: person
name: Derek Brandwood
categorie: industrie
role:
  - responsable RCA nord
  - intermédiaire industrie musicale
  - représentant RCA nord de l’Angleterre
  - médiateur industriel des sessions RCA/Grapevine
  - témoin du potentiel et de l’échec RCA
sources:
  - S45
  - S75
  - S76
same_as:
  - PERS-S45-DEREK-BRANDWOOD
  - PERS-S75-017
  - PERS-S76-032
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-dik-verdult — Dik Verdult

```yaml
id: PERSON-dik-verdult
type_unite: person
name: Dik Verdult
categorie: industrie
role:
  - acteur
sources:
  - S84
same_as:
  - PERS-S84-005
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-domenico-morreale — Domenico Morreale

```yaml
id: PERSON-domenico-morreale
type_unite: person
name: Domenico Morreale
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S50
same_as:
  - PERS-S50-002
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-don-tonay — Don Tonay

```yaml
id: PERSON-don-tonay
type_unite: person
name: Don Tonay
categorie: entourage
role:
  - propriétaire du Russell Club
  - acteur des clubs de Moss Side et Hulme
sources:
  - S76
same_as:
  - PERS-S76-046
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-donald-johnson — Donald Johnson

```yaml
id: PERSON-donald-johnson
type_unite: person
name: Donald Johnson
categorie: entourage
role:
  - batteur de A Certain Ratio
  - figure citée dans la cartographie Newell Green / Wythenshawe
sources:
  - S76
same_as:
  - PERS-S76-039
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-doreen-curtis — Doreen Curtis

```yaml
id: PERSON-doreen-curtis
type_unite: person
name: Doreen Curtis
categorie: entourage
role:
  - mère de Ian Curtis
  - témoin familial central
sources:
  - S76
same_as:
  - PERS-S76-002
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-dr-david-holmes — Dr David Holmes

```yaml
id: PERSON-dr-david-holmes
type_unite: person
name: Dr David Holmes
categorie: entourage
role:
  - psychologue
  - musicien de la scène de l’époque
  - témoin interprétatif sur l’épilepsie et la performance
sources:
  - S76
same_as:
  - PERS-S76-055
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-eddie-garrity — Eddie Garrity

```yaml
id: PERSON-eddie-garrity
type_unite: person
name: Eddie Garrity
categorie: entourage
role:
  - chanteur lié à Ed Banger & The Nosebleeds
  - figure citée dans la cartographie Newell Green / Wythenshawe
sources:
  - S76
same_as:
  - PERS-S76-040
alt_names:
  - Ed Banger
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-eddy-oz-pa — Eddy

```yaml
id: PERSON-eddy-oz-pa
type_unite: person
name: Eddy
categorie: industrie
role:
  - acteur (à préciser)
sources:
  - S76
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: true
note: Composante individuelle de PERS-S76-052 « Oz PA / Eddy et Oz » ; nom incomplet, contrôle S76 requis.
```

## PERSON-emiliano-ilardi — Emiliano Ilardi

```yaml
id: PERSON-emiliano-ilardi
type_unite: person
name: Emiliano Ilardi
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S58
same_as:
  - PERS-S58-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-ernest-beard — Ernest Beard

```yaml
id: PERSON-ernest-beard
type_unite: person
name: Ernest Beard
categorie: entourage
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-ERNEST-BEARD
  - PERS-S45-ERNEST-BEARD-EPILEPSY
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-fabio-la-rocca — Fabio La Rocca

```yaml
id: PERSON-fabio-la-rocca
type_unite: person
name: Fabio La Rocca
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-francesca-ferrara — Francesca Ferrara

```yaml
id: PERSON-francesca-ferrara
type_unite: person
name: Francesca Ferrara
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S59
same_as:
  - PERS-S59-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-franco-berardi — Franco Berardi

```yaml
id: PERSON-franco-berardi
type_unite: person
name: Franco Berardi
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S29
  - S31
same_as:
  - PERS-S29-008
  - PERS-S31-002
alt_names:
  - Franco Berardi Bifo
  - Bifo
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-friedrich-nietzsche — Friedrich Nietzsche

```yaml
id: PERSON-friedrich-nietzsche
type_unite: person
name: Friedrich Nietzsche
categorie: influence
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-010
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-genesis-p-orridge — Genesis P-Orridge

```yaml
id: PERSON-genesis-p-orridge
type_unite: person
name: Genesis P-Orridge
categorie: entourage
role:
  - artiste Throbbing Gristle
  - témoin d’alerte autour de l’état de Curtis
sources:
  - S29
  - S76
same_as:
  - PERS-S29-003
  - PERS-S76-086
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-georg-simmel — Georg Simmel

```yaml
id: PERSON-georg-simmel
type_unite: person
name: Georg Simmel
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-007
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-georg-wilhelm-friedrich-hegel — Georg Wilhelm Friedrich Hegel

```yaml
id: PERSON-georg-wilhelm-friedrich-hegel
type_unite: person
name: Georg Wilhelm Friedrich Hegel
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S57
same_as:
  - PERS-S57-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-gillian-gilbert — Gillian Gilbert

```yaml
id: PERSON-gillian-gilbert
type_unite: person
name: Gillian Gilbert
categorie: entourage
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-GILLIAN-GILBERT-GOSHES
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-giuseppe-allegri — Giuseppe Allegri

```yaml
id: PERSON-giuseppe-allegri
type_unite: person
name: Giuseppe Allegri
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S31
same_as:
  - PERS-S31-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-grant-gee — Grant Gee

```yaml
id: PERSON-grant-gee
type_unite: person
name: Grant Gee
categorie: industrie
role:
  - acteur
sources:
  - S29
  - S34
  - S52
  - S78
  - S84
same_as:
  - PERS-S29-010
  - PERS-S34-003
  - PERS-S52-010
  - PERS-S78-010
  - PERS-S84-007
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-greil-marcus — Greil Marcus

```yaml
id: PERSON-greil-marcus
type_unite: person
name: Greil Marcus
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S31
same_as:
  - PERS-S31-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-henri-bergson — Henri Bergson

```yaml
id: PERSON-henri-bergson
type_unite: person
name: Henri Bergson
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-007
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-henri-lefebvre — Henri Lefebvre

```yaml
id: PERSON-henri-lefebvre
type_unite: person
name: Henri Lefebvre
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-006
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-hito-steyerl — Hito Steyerl

```yaml
id: PERSON-hito-steyerl
type_unite: person
name: Hito Steyerl
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S51
same_as:
  - PERS-S51-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-iain-gray — Iain Gray

```yaml
id: PERSON-iain-gray
type_unite: person
name: Iain Gray
categorie: entourage
role:
  - ami de Ian Curtis
  - guitariste des répétitions embryonnaires pré-Warsaw
  - acteur périphérique rapidement effacé
sources:
  - S45
  - S76
same_as:
  - PERS-S45-IAIN-GRAY
  - PERS-S76-017
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-ian-curtis — Ian Curtis

```yaml
id: PERSON-ian-curtis
type_unite: person
name: Ian Curtis
categorie: membre
role:
  - chanteur
  - parolier
  - figure centrale
sources:
  - S41
  - S45
  - S29
  - S34
  - S49
  - S53
  - S54
  - S55
  - S56
  - S57
  - S59
same_as:
  - PERS-001
  - PERS-S29-002
  - PERS-S34-010
  - PERS-S45-IAN-CURTIS-VOTE-CONSERVATEUR
  - PERS-S49-002
  - PERS-S53-002
  - PERS-S54-002
  - PERS-S55-002
  - PERS-S56-002
  - PERS-S57-004
  - PERS-S59-002
alt_names:
  - Ian Kevin Curtis
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-ian-wood — Ian Wood

```yaml
id: PERSON-ian-wood
type_unite: person
name: Ian Wood
categorie: critique_journaliste
role:
  - journaliste local pour Sounds
  - inspecteur des impôts selon S76
  - observateur de Joy Division au Band On The Wall
sources:
  - S76
same_as:
  - PERS-S76-041
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-j-g-ballard — J. G. Ballard

```yaml
id: PERSON-j-g-ballard
type_unite: person
name: J. G. Ballard
categorie: influence
role:
  - acteur
sources:
  - S54
same_as:
  - PERS-S54-004
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-jacques-attali — Jacques Attali

```yaml
id: PERSON-jacques-attali
type_unite: person
name: Jacques Attali
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S60
same_as:
  - PERS-S60-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-jacques-derrida — Jacques Derrida

```yaml
id: PERSON-jacques-derrida
type_unite: person
name: Jacques Derrida
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-007
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-jane-jacobs — Jane Jacobs

```yaml
id: PERSON-jane-jacobs
type_unite: person
name: Jane Jacobs
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-009
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-jasmine — Jasmine

```yaml
id: PERSON-jasmine
type_unite: person
name: Jasmine
categorie: entourage
role:
  - acteur (à préciser)
sources:
  - S76
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: true
note: Composante individuelle de PERS-S76-064 « Dave Pils et Jasmine » ; nom incomplet, contrôle S76 requis.
```

## PERSON-jean-pierre-turmel — Jean-Pierre Turmel

```yaml
id: PERSON-jean-pierre-turmel
type_unite: person
name: Jean-Pierre Turmel
categorie: entourage
role:
  - auteur du texte de pochette de Licht und Blindheit
  - médiateur Sordide Sentimental
  - fondateur / animateur de Sordide Sentimental
  - médiateur français de Joy Division
  - acteur du disque-objet *Licht und Blindheit*
sources:
  - S75
  - S76
same_as:
  - PERS-S75-036
  - PERS-S76-066
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-jennifer-malvezzi — Jennifer Malvezzi

```yaml
id: PERSON-jennifer-malvezzi
type_unite: person
name: Jennifer Malvezzi
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S51
same_as:
  - PERS-S51-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-jeremey-deller — Jeremey Deller

```yaml
id: PERSON-jeremey-deller
type_unite: person
name: Jeremey Deller
categorie: entourage
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-008
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-jeremy-kerr — Jeremy Kerr

```yaml
id: PERSON-jeremy-kerr
type_unite: person
name: Jeremy Kerr
categorie: entourage
role:
  - membre de A Certain Ratio
  - témoin d’un concert de Joy Division au Band On The Wall
sources:
  - S76
same_as:
  - PERS-S76-042
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-john-anderson — John Anderson

```yaml
id: PERSON-john-anderson
type_unite: person
name: John Anderson
categorie: industrie
role:
  - producteur
  - responsable Grapevine
  - intermédiaire industriel
  - responsable de Grapevine Records
  - producteur / directeur de session associé aux sessions Arrow
  - acteur du projet RCA / Northern Soul
  - interlocuteur contractuel de Rob Gretton
sources:
  - S45
  - S75
  - S76
same_as:
  - PERS-S45-JOHN-ANDERSON
  - PERS-S75-019
  - PERS-S76-034
  - PERS-S76-044
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-john-brierley — John Brierley

```yaml
id: PERSON-john-brierley
type_unite: person
name: John Brierley
categorie: industrie
role:
  - ingénieur du son
  - producteur
sources:
  - S41
same_as:
  - PERS-012
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-john-curd — John Curd

```yaml
id: PERSON-john-curd
type_unite: person
name: John Curd
categorie: industrie
role:
  - promoteur du Lyceum selon S76
  - témoin indirect de la crise de Curtis
sources:
  - S76
same_as:
  - PERS-S76-075
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-john-peel — John Peel

```yaml
id: PERSON-john-peel
type_unite: person
name: John Peel
categorie: industrie
role:
  - DJ radio
  - médiateur national
  - animateur radio BBC
  - prescripteur national
  - réception critique de Joy Division
sources:
  - S75
  - S76
same_as:
  - PERS-S75-021
  - PERS-S76-057
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-john-the-postman — John The Postman

```yaml
id: PERSON-john-the-postman
type_unite: person
name: John The Postman
categorie: entourage
role:
  - figure de la scène mancunienne
  - performer punk local
  - témoin sensible des concerts Joy Division
sources:
  - S76
same_as:
  - PERS-S76-030
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-jon-savage — Jon Savage

```yaml
id: PERSON-jon-savage
type_unite: person
name: Jon Savage
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S52
  - S56
  - S77
  - S78
same_as:
  - PERS-S52-009
  - PERS-S56-003
  - PERS-S77-003
  - PERS-S78-004
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-kelvin-briggs — Kelvin Briggs

```yaml
id: PERSON-kelvin-briggs
type_unite: person
name: Kelvin Briggs
categorie: entourage
role:
  - ami de King’s School
  - témoin du cercle adolescent
  - témoin / best man au mariage de Curtis
sources:
  - S76
same_as:
  - PERS-S76-015
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-kevin-buckle — Kevin Buckle

```yaml
id: PERSON-kevin-buckle
type_unite: person
name: Kevin Buckle
categorie: entourage
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-002
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-kevin-cummins — Kevin Cummins

```yaml
id: PERSON-kevin-cummins
type_unite: person
name: Kevin Cummins
categorie: auteur_secondaire
role:
  - photographe
  - médiateur visuel
  - témoin de la scène mancunienne
  - témoin de l’Electric Circus
  - acteur fanzine / Negatives
  - producteur d’une part majeure de l’iconographie Joy Division
sources:
  - S75
  - S76
  - S53
  - S78
same_as:
  - PERS-S53-003
  - PERS-S75-023
  - PERS-S76-012
  - PERS-S76-023
  - PERS-S76-056
  - PERS-S78-006
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-kevin-curtis — Kevin Curtis

```yaml
id: PERSON-kevin-curtis
type_unite: person
name: Kevin Curtis
categorie: entourage
role:
  - père de Ian Curtis
  - policier ferroviaire
  - ancien marin blessé pendant la guerre
sources:
  - S76
same_as:
  - PERS-S76-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-kevin-wood — Kevin Wood

```yaml
id: PERSON-kevin-wood
type_unite: person
name: Kevin Wood
categorie: entourage
role:
  - voisin de Barton Street
  - témoin de la découverte du corps de Ian Curtis
sources:
  - S76
same_as:
  - PERS-S76-084
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-larry-cassidy — Larry Cassidy

```yaml
id: PERSON-larry-cassidy
type_unite: person
name: Larry Cassidy
categorie: industrie
role:
  - chanteur de Section 25
  - témoin des crises de Curtis et de la scène Factory élargie
sources:
  - S76
same_as:
  - PERS-S76-083
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-lawrence-beedle — Lawrence Beedle

```yaml
id: PERSON-lawrence-beedle
type_unite: person
name: Lawrence Beedle
categorie: entourage
role:
  - acteur Music Force
  - acteur Rabid Records
  - témoin du lien Gretton/Rabid/Joy Division
sources:
  - S76
same_as:
  - PERS-S76-026
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-leonard-nevarez — Leonard Nevarez

```yaml
id: PERSON-leonard-nevarez
type_unite: person
name: Leonard Nevarez
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S78
same_as:
  - PERS-S78-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-lesley-gilbert — Lesley Gilbert

```yaml
id: PERSON-lesley-gilbert
type_unite: person
name: Lesley Gilbert
categorie: entourage
role:
  - compagne de Rob Gretton
  - salariée d’un cabinet d’avocats selon Terry Mason
sources:
  - S45
  - S76
same_as:
  - PERS-S45-LESLEY-GILBERT
  - PERS-S76-043
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-linda-barone — Linda Barone

```yaml
id: PERSON-linda-barone
type_unite: person
name: Linda Barone
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S56
same_as:
  - PERS-S56-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-lindsay-reade — Lindsay Reade

```yaml
id: PERSON-lindsay-reade
type_unite: person
name: Lindsay Reade
categorie: auteur_secondaire
role:
  - co-autrice de Torn Apart
  - "ancienne figure de l'entourage Factory"
  - médiatrice de témoignages intimes
sources:
  - S76
same_as:
  - PERS-S76-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-liz-naylor — Liz Naylor

```yaml
id: PERSON-liz-naylor
type_unite: person
name: Liz Naylor
categorie: critique_journaliste
role:
  - acteur
sources:
  - S21
  - S77
  - S78
same_as:
  - PERS-S21-001
  - PERS-S77-005
  - PERS-S78-002
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-lou-stoppard — Lou Stoppard

```yaml
id: PERSON-lou-stoppard
type_unite: person
name: Lou Stoppard
categorie: entourage
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-006
alt_names:
  - Adam Murray
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-lucy-toothpaste — Lucy Toothpaste

```yaml
id: PERSON-lucy-toothpaste
type_unite: person
name: Lucy Toothpaste
categorie: critique_journaliste
role:
  - acteur
sources:
  - S77
same_as:
  - PERS-S77-010
alt_names:
  - Lucy Whitman
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-malcolm-whitehead — Malcolm Whitehead

```yaml
id: PERSON-malcolm-whitehead
type_unite: person
name: Malcolm Whitehead
categorie: industrie
role:
  - acteur
sources:
  - S78
  - S84
same_as:
  - PERS-S78-009
  - PERS-S84-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-manolo-farci — Manolo Farci

```yaml
id: PERSON-manolo-farci
type_unite: person
name: Manolo Farci
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S49
same_as:
  - PERS-S49-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-marcel-proust — Marcel Proust

```yaml
id: PERSON-marcel-proust
type_unite: person
name: Marcel Proust
categorie: influence
role:
  - écrivain
  - référence possible pour le titre Unknown Pleasures
sources:
  - S75
same_as:
  - PERS-S75-031
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-mark-fisher — Mark Fisher

```yaml
id: PERSON-mark-fisher
type_unite: person
name: Mark Fisher
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-005
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-mark-leckey — Mark Leckey

```yaml
id: PERSON-mark-leckey
type_unite: person
name: Mark Leckey
categorie: entourage
role:
  - acteur
sources:
  - S51
same_as:
  - PERS-S51-002
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-mark-perry — Mark Perry

```yaml
id: PERSON-mark-perry
type_unite: person
name: Mark Perry
categorie: critique_journaliste
role:
  - acteur
sources:
  - S77
same_as:
  - PERS-S77-002
alt_names:
  - Mark P
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-mark-reeder — Mark Reeder

```yaml
id: PERSON-mark-reeder
type_unite: person
name: Mark Reeder
categorie: entourage
role:
  - témoin des sociabilités de disquaires
  - ami musical de Ian Curtis
  - témoin de Rare Records/Virgin
  - ami de Ian Curtis
  - témoin du changement de nom et de l’intérêt allemand de Curtis
  - témoin de la perception sociale de l’épilepsie
  - témoin ayant lui-même connu des crises
sources:
  - S76
same_as:
  - PERS-S76-011
  - PERS-S76-029
  - PERS-S76-053
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-marshall-berman — Marshall Berman

```yaml
id: PERSON-marshall-berman
type_unite: person
name: Marshall Berman
categorie: theoricien_mobilise
role:
  - acteur
sources:
  - S34
same_as:
  - PERS-S34-005
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-martin-hannett — Martin Hannett

```yaml
id: PERSON-martin-hannett
type_unite: person
name: Martin Hannett
categorie: industrie
role:
  - producteur
  - ingénieur sonore
  - expérimentateur
  - acteur Music Force
  - cofondateur Rabid Records
  - futur producteur de Joy Division
  - architecte sonore des sessions Cargo / Sordide
  - producteur de la première version Pennine de « Love Will Tear Us Apart » selon S76
  - producteur lié aux sessions de transition de janvier 1980
sources:
  - S41
  - S45
  - S34
  - S76
  - S31
  - S58
  - S59
same_as:
  - PERS-008
  - PERS-S31-004
  - PERS-S34-011
  - PERS-S45-MARTIN-HANNETT-UNKNOWN-PLEASURES
  - PERS-S58-006
  - PERS-S59-005
  - PERS-S76-024
  - PERS-S76-069
  - PERS-S76-072
alt_names:
  - James Martin Hannett
  - Martin Zero
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-martin-oneill — Martin O’Neill

```yaml
id: PERSON-martin-oneill
type_unite: person
name: Martin O’Neill
categorie: industrie
role:
  - photographe local
  - auteur de photographies iconiques du concert de Bowdon Vale
sources:
  - S76
same_as:
  - PERS-S76-059
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-martin-rushent — Martin Rushent

```yaml
id: PERSON-martin-rushent
type_unite: person
name: Martin Rushent
categorie: industrie
role:
  - producteur
  - entrepreneur de production
  - fondateur / acteur de Genetic Records
  - producteur potentiel alternatif pour Joy Division
sources:
  - S75
  - S76
same_as:
  - PERS-S75-022
  - PERS-S76-058
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-martin-x — Martin X

```yaml
id: PERSON-martin-x
type_unite: person
name: Martin X
categorie: entourage
role:
  - acteur
sources:
  - S21
same_as:
  - PERS-S21-004
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-martyn-atkins — Martyn Atkins

```yaml
id: PERSON-martyn-atkins
type_unite: person
name: Martyn Atkins
categorie: industrie
role:
  - acteur du design de *Closer*
  - médiateur de l’image Staglieno avec Peter Saville selon S76
sources:
  - S76
same_as:
  - PERS-S76-078
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-massimo-villani — Massimo Villani

```yaml
id: PERSON-massimo-villani
type_unite: person
name: Massimo Villani
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S57
same_as:
  - PERS-S57-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-matthew-worley — Matthew Worley

```yaml
id: PERSON-matthew-worley
type_unite: person
name: Matthew Worley
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S77
same_as:
  - PERS-S77-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-maurice-blanchot — Maurice Blanchot

```yaml
id: PERSON-maurice-blanchot
type_unite: person
name: Maurice Blanchot
categorie: influence
role:
  - acteur
sources:
  - S57
same_as:
  - PERS-S57-002
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-michael-goddard — Michael Goddard

```yaml
id: PERSON-michael-goddard
type_unite: person
name: Michael Goddard
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-001
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-michael-winterbottom — Michael Winterbottom

```yaml
id: PERSON-michael-winterbottom
type_unite: person
name: Michael Winterbottom
categorie: industrie
role:
  - acteur
sources:
  - S53
same_as:
  - PERS-S53-011
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-michel-isbecque — Michel Isbecque

```yaml
id: PERSON-michel-isbecque
type_unite: person
name: Michel Isbecque
categorie: industrie
role:
  - acteur
sources:
  - S84
same_as:
  - PERS-S84-004
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-mick-middles — Mick Middles

```yaml
id: PERSON-mick-middles
type_unite: person
name: Mick Middles
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-MICK-MIDDLES-BAND-ON-THE-WALL
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-mike-pickering — Mike Pickering

```yaml
id: PERSON-mike-pickering
type_unite: person
name: Mike Pickering
categorie: entourage
role:
  - supporter de Manchester City croisé par Gretton selon l’anecdote de Nottingham
  - futur acteur de la Haçienda et de la scène dance mancunienne
sources:
  - S76
same_as:
  - PERS-S76-038
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-natalie-curtis — Natalie Curtis

```yaml
id: PERSON-natalie-curtis
type_unite: person
name: Natalie Curtis
categorie: entourage
role:
  - proche
  - enfant de Ian Curtis
  - fille de Ian et Deborah Curtis
  - fille de Ian Curtis et Deborah Curtis
sources:
  - S45
  - S75
  - S76
same_as:
  - PERS-011
  - PERS-S45-NATALIE-CURTIS-BIRTH
  - PERS-S75-028
  - PERS-S76-061
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-neil-hargreaves — Neil Hargreaves

```yaml
id: PERSON-neil-hargreaves
type_unite: person
name: Neil Hargreaves
categorie: entourage
role:
  - acteur
sources:
  - S21
same_as:
  - PERS-S21-005
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-nick-cope — Nick Cope

```yaml
id: PERSON-nick-cope
type_unite: person
name: Nick Cope
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S84
same_as:
  - PERS-S84-008
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-nikolai-gogol — Nikolai Gogol

```yaml
id: PERSON-nikolai-gogol
type_unite: person
name: Nikolai Gogol
categorie: influence
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-012
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-orian-williams — Orian Williams

```yaml
id: PERSON-orian-williams
type_unite: person
name: Orian Williams
categorie: industrie
role:
  - acteur
sources:
  - S50
same_as:
  - PERS-S50-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-oz-oz-pa — Oz

```yaml
id: PERSON-oz-oz-pa
type_unite: person
name: Oz
categorie: industrie
role:
  - acteur (à préciser)
sources:
  - S76
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: true
note: Composante individuelle de PERS-S76-052 « Oz PA / Eddy et Oz » ; nom incomplet, contrôle S76 requis.
```

## PERSON-pam-wood — Pam Wood

```yaml
id: PERSON-pam-wood
type_unite: person
name: Pam Wood
categorie: entourage
role:
  - voisine de Barton Street
  - témoin périphérique de la découverte
sources:
  - S76
same_as:
  - PERS-S76-085
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-paolo-bertetti — Paolo Bertetti

```yaml
id: PERSON-paolo-bertetti
type_unite: person
name: Paolo Bertetti
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S50
same_as:
  - PERS-S50-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-paul-crosthwaite — Paul Crosthwaite

```yaml
id: PERSON-paul-crosthwaite
type_unite: person
name: Paul Crosthwaite
categorie: critique_journaliste
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-009
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-paul-hanley — Paul Hanley

```yaml
id: PERSON-paul-hanley
type_unite: person
name: Paul Hanley
categorie: entourage
role:
  - futur batteur de The Fall
  - témoin du concert de Bowdon Vale
sources:
  - S76
same_as:
  - PERS-S76-060
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-paul-heapy — Paul Heapy

```yaml
id: PERSON-paul-heapy
type_unite: person
name: Paul Heapy
categorie: entourage
role:
  - ami scolaire de Ian Curtis et Pete Johnson
sources:
  - S76
same_as:
  - PERS-S76-008
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-paul-morley — Paul Morley

```yaml
id: PERSON-paul-morley
type_unite: person
name: Paul Morley
categorie: auteur_secondaire
role:
  - journaliste
  - critique
  - témoin
  - critique musical
  - médiateur critique de Joy Division
  - journaliste NME
  - acteur de la première mythographie posthume de Joy Division
  - auteur de *Nothing*
sources:
  - S34
  - S45
  - S75
  - S76
  - S21
  - S77
  - S78
same_as:
  - PERS-014
  - PERS-S21-007
  - PERS-S34-012
  - PERS-S45-PAUL-MORLEY-1977
  - PERS-S45-PAUL-MORLEY-BAND-ON-THE-WALL
  - PERS-S75-037
  - PERS-S76-089
  - PERS-S77-008
  - PERS-S78-003
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-pennie-smith — Pennie Smith

```yaml
id: PERSON-pennie-smith
type_unite: person
name: Pennie Smith
categorie: industrie
role:
  - photographe
sources:
  - IMAGE-I-0004
same_as: []
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
note: "Identite ajoutee depuis le registre iconographique pour une photographie attribuee a Pennie Smith ; aucun PERS-* source existant au moment de l'ajout."
```

## PERSON-penny-rimbaud — Penny Rimbaud

```yaml
id: PERSON-penny-rimbaud
type_unite: person
name: Penny Rimbaud
categorie: entourage
role:
  - acteur
sources:
  - S77
same_as:
  - PERS-S77-009
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-pete-johnson — Pete Johnson

```yaml
id: PERSON-pete-johnson
type_unite: person
name: Pete Johnson
categorie: entourage
role:
  - "ami d'enfance de Ian Curtis"
  - témoin scolaire et adolescent
sources:
  - S76
same_as:
  - PERS-S76-006
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-pete-shelley — Pete Shelley

```yaml
id: PERSON-pete-shelley
type_unite: person
name: Pete Shelley
categorie: entourage
role:
  - acteur
sources:
  - S54
same_as:
  - PERS-S54-009
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-peter-hook — Peter Hook

```yaml
id: PERSON-peter-hook
type_unite: person
name: Peter Hook
categorie: membre
role:
  - musicien
  - bassiste
  - témoin
  - mémorialiste
sources:
  - S41
  - S52
  - S54
  - S55
  - S58
  - S59
same_as:
  - PERS-002
  - PERS-S52-007
  - PERS-S54-006
  - PERS-S55-003
  - PERS-S58-002
  - PERS-S59-003
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-peter-saville — Peter Saville

```yaml
id: PERSON-peter-saville
type_unite: person
name: Peter Saville
categorie: industrie
role:
  - designer
  - directeur artistique
  - designer graphique
  - "auteur de la pochette d'Unknown Pleasures"
  - étudiant à Manchester Polytechnic
  - acteur de l’image Factory
sources:
  - S41
  - S75
  - S76
  - S31
  - S53
  - S59
  - S60
same_as:
  - PERS-009
  - PERS-S31-008
  - PERS-S53-004
  - PERS-S59-004
  - PERS-S60-002
  - PERS-S75-029
  - PERS-S76-049
alt_names:
  - Peter Andrew Saville
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-raf-simons — Raf Simons

```yaml
id: PERSON-raf-simons
type_unite: person
name: Raf Simons
categorie: industrie
role:
  - acteur
sources:
  - S60
  - S85
same_as:
  - PERS-S60-004
  - PERS-S85-005
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-raffaele-federici — Raffaele Federici

```yaml
id: PERSON-raffaele-federici
type_unite: person
name: Raffaele Federici
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S60
same_as:
  - PERS-S60-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-richard-boon — Richard Boon

```yaml
id: PERSON-richard-boon
type_unite: person
name: Richard Boon
categorie: industrie
role:
  - manager de Buzzcocks
  - interlocuteur précoce de Curtis
  - médiateur de scène
sources:
  - S76
  - S84
same_as:
  - PERS-S76-019
  - PERS-S84-002
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-richard-searling — Richard Searling

```yaml
id: PERSON-richard-searling
type_unite: person
name: Richard Searling
categorie: industrie
role:
  - DJ northern soul
  - producteur associé
  - assistant de Derek Brandwood
  - intermédiaire du projet RCA/Grapevine
sources:
  - S45
  - S75
  - S76
same_as:
  - PERS-S45-RICHARD-SEARLING
  - PERS-S75-018
  - PERS-S76-033
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-rob-gretton — Rob Gretton

```yaml
id: PERSON-rob-gretton
type_unite: person
name: Rob Gretton
categorie: industrie
role:
  - manager
  - stratège
  - médiateur
  - manager de Joy Division
  - "gardien de l'image et des objets Factory"
  - futur manager de Joy Division
  - DJ à Rafters
  - auteur du fanzine Manchester Rains
  - producteur lié à The Panik
  - figure des réseaux Wythenshawe / Newell Green / Manchester City
sources:
  - S41
  - S45
  - S75
  - S76
  - S31
  - S58
same_as:
  - PERS-006
  - PERS-S31-007
  - PERS-S45-ROB-GRETTON-GARDIEN
  - PERS-S58-005
  - PERS-S75-030
  - PERS-S76-027
  - PERS-S76-037
alt_names:
  - Robert Leo Gretton
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-roger-eagle — Roger Eagle

```yaml
id: PERSON-roger-eagle
type_unite: person
name: Roger Eagle
categorie: industrie
role:
  - DJ et promoteur
  - figure Twisted Wheel / Eric’s
  - initiateur possible d’un projet de label Manchester-Liverpool
sources:
  - S76
same_as:
  - PERS-S76-048
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-sam-riley — Sam Riley

```yaml
id: PERSON-sam-riley
type_unite: person
name: Sam Riley
categorie: entourage
role:
  - acteur
sources:
  - S52
same_as:
  - PERS-S52-003
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-samantha-morton — Samantha Morton

```yaml
id: PERSON-samantha-morton
type_unite: person
name: Samantha Morton
categorie: entourage
role:
  - acteur
sources:
  - S52
same_as:
  - PERS-S52-004
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-simon-reynolds — Simon Reynolds

```yaml
id: PERSON-simon-reynolds
type_unite: person
name: Simon Reynolds
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S29
same_as:
  - PERS-S29-006
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-simon-topping — Simon Topping

```yaml
id: PERSON-simon-topping
type_unite: person
name: Simon Topping
categorie: entourage
role:
  - chanteur / membre associé à A Certain Ratio
  - voix de substitution au Derby Hall de Bury
sources:
  - S76
same_as:
  - PERS-S76-081
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-stephanie — Stephanie

```yaml
id: PERSON-stephanie
type_unite: person
name: Stephanie
categorie: entourage
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-STEPHANIE-MORRIS
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: true
```

## PERSON-stephen-morris — Stephen Morris

```yaml
id: PERSON-stephen-morris
type_unite: person
name: Stephen Morris
categorie: membre
role:
  - musicien
  - batteur
  - témoin
  - catalyseur formel
  - batteur de Joy Division
  - opérateur rythmique du son Hannett
  - stabilisateur rythmique du groupe
sources:
  - S41
  - S45
  - S75
  - S76
  - S52
  - S55
same_as:
  - PERS-004
  - PERS-004-S75
  - PERS-S45-STEPHEN-MORRIS
  - PERS-S52-008
  - PERS-S55-005
  - PERS-S75-026
  - PERS-S76-021
alt_names:
  - Stephen Paul David Morris
  - Steve Morris
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-steve-brotherdale — Steve Brotherdale

```yaml
id: PERSON-steve-brotherdale
type_unite: person
name: Steve Brotherdale
categorie: entourage
role:
  - musicien
  - batteur transitoire
  - batteur transitoire de Warsaw
  - acteur de la scène mancunienne
sources:
  - S45
  - S75
  - S76
same_as:
  - PERS-015
  - PERS-S45-STEVE-BROTHERDALE
  - PERS-S76-020
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-steve-burke — Steve Burke

```yaml
id: PERSON-steve-burke
type_unite: person
name: Steve Burke
categorie: critique_journaliste
role:
  - témoin de l’Electric Circus
  - acteur fanzine / scène mancunienne
sources:
  - S76
same_as:
  - PERS-S76-018
alt_names:
  - Steve Shy
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-steve-harley — Steve Harley

```yaml
id: PERSON-steve-harley
type_unite: person
name: Steve Harley
categorie: critique_journaliste
role:
  - musicien, Cockney Rebel
  - intervenant critique lors de *Something Else*
sources:
  - S76
same_as:
  - PERS-S76-065
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-steven-morrissey — Steven Morrissey

```yaml
id: PERSON-steven-morrissey
type_unite: person
name: Steven Morrissey
categorie: critique_journaliste
role:
  - jeune observateur de la scène glam/punk mancunienne
  - futur chanteur de The Smiths
  - critique ultérieur de Joy Division et New Order
sources:
  - S76
same_as:
  - PERS-S76-031
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-stuart-orme — Stuart Orme

```yaml
id: PERSON-stuart-orme
type_unite: person
name: Stuart Orme
categorie: industrie
role:
  - acteur
sources:
  - S84
same_as:
  - PERS-S84-006
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-sue-barlow — Sue Barlow

```yaml
id: PERSON-sue-barlow
type_unite: person
name: Sue Barlow
categorie: entourage
role:
  - acteur
sources:
  - S45
same_as:
  - PERS-S45-SUE-BARLOW
  - PERS-S45-SUE-BARLOW-GIRLIES
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-terry-mason — Terry Mason

```yaml
id: PERSON-terry-mason
type_unite: person
name: Terry Mason
categorie: industrie
role:
  - ami de Bernard Sumner et Peter Hook
  - premier organisateur / manager informel de Warsaw
  - témoin direct des débuts
  - témoin logistique et ancien manager
  - acteur du retrait de Curtis lors des crises
  - observateur de Preston, Lyceum et Candy
sources:
  - S45
  - S76
same_as:
  - PERS-S45-TERRY-MASON
  - PERS-S76-016
  - PERS-S76-074
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-tom-hingley — Tom Hingley

```yaml
id: PERSON-tom-hingley
type_unite: person
name: Tom Hingley
categorie: entourage
role:
  - acteur
sources:
  - S85
same_as:
  - PERS-S85-003
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-tony-davidson — Tony Davidson

```yaml
id: PERSON-tony-davidson
type_unite: person
name: Tony Davidson
categorie: industrie
role:
  - propriétaire / acteur local
  - "fournisseur d'espace de répétition"
  - propriétaire de T. J. Davidson’s
  - entrepreneur de répétition et label TJM Records
sources:
  - S75
  - S76
same_as:
  - PERS-S75-025
  - PERS-S76-051
alt_names:
  - T.J. Davidson
  - T. J. Davidson
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-tony-drayton — Tony Drayton

```yaml
id: PERSON-tony-drayton
type_unite: person
name: Tony Drayton
categorie: entourage
role:
  - acteur
sources:
  - S77
same_as:
  - PERS-S77-004
alt_names:
  - Tony D
  - Tony Puppy
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-tony-nuttall — Tony Nuttall

```yaml
id: PERSON-tony-nuttall
type_unite: person
name: Tony Nuttall
categorie: entourage
role:
  - "ami d'enfance de Ian Curtis"
  - compagnon de speedway et de sociabilité locale
sources:
  - S45
  - S76
same_as:
  - PERS-S45-TONY-NUTTALL-RUPTURE-POLITIQUE
  - PERS-S76-007
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-tony-wilson — Tony Wilson

```yaml
id: PERSON-tony-wilson
type_unite: person
name: Tony Wilson
categorie: industrie
role:
  - journaliste
  - entrepreneur culturel
  - fondateur Factory
  - médiateur
  - présentateur Granada TV
  - futur cofondateur de Factory Records
  - témoin du dernier Electric Circus
  - cofondateur Factory
  - promoteur du Factory Club
  - initiateur de *The Factory Sample*
  - témoin du Lyceum
  - médiateur vocal indirect pour « Love Will Tear Us Apart » via Sinatra
sources:
  - S41
  - S45
  - S34
  - S76
  - S21
  - S31
  - S52
  - S53
  - S58
  - S78
same_as:
  - PERS-007
  - PERS-S21-006
  - PERS-S31-005
  - PERS-S34-004
  - PERS-S45-TONY-WILSON-GRANADA
  - PERS-S52-011
  - PERS-S53-006
  - PERS-S58-004
  - PERS-S76-022
  - PERS-S76-050
  - PERS-S76-073
  - PERS-S78-005
alt_names:
  - Anthony Howard Wilson
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-tosh-ryan — Tosh Ryan

```yaml
id: PERSON-tosh-ryan
type_unite: person
name: Tosh Ryan
categorie: entourage
role:
  - acteur Music Force
  - cofondateur Rabid Records
  - témoin de Hannett
sources:
  - S76
same_as:
  - PERS-S76-025
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-vince-staples — Vince Staples

```yaml
id: PERSON-vince-staples
type_unite: person
name: Vince Staples
categorie: entourage
role:
  - acteur
sources:
  - S60
same_as:
  - PERS-S60-005
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-vincent-moon — Vincent Moon

```yaml
id: PERSON-vincent-moon
type_unite: person
name: Vincent Moon
categorie: industrie
role:
  - acteur
sources:
  - S50
same_as:
  - PERS-S50-005
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-vincenzo-romania — Vincenzo Romania

```yaml
id: PERSON-vincenzo-romania
type_unite: person
name: Vincenzo Romania
categorie: auteur_secondaire
role:
  - acteur
sources:
  - S55
same_as:
  - PERS-S55-001
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-vini-reilly — Vini Reilly

```yaml
id: PERSON-vini-reilly
type_unite: person
name: Vini Reilly
categorie: entourage
role:
  - musicien de The Durutti Column
  - "témoin technique de l'usage du delay"
  - musicien
  - futur membre / centre de Durutti Column
  - témoin pré-Warsaw
  - musicien Durutti Column
  - témoin rétrospectif de la mort de Curtis
sources:
  - S75
  - S76
same_as:
  - PERS-S75-027
  - PERS-S76-014
  - PERS-S76-088
alt_names: []
categorie_a_arbitrer: true
a_arbitrer: false
```

## PERSON-warren-jackson — Warren Jackson

```yaml
id: PERSON-warren-jackson
type_unite: person
name: Warren Jackson
categorie: industrie
role:
  - acteur
sources:
  - S50
same_as:
  - PERS-S50-004
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

## PERSON-william-s-burroughs — William S. Burroughs

```yaml
id: PERSON-william-s-burroughs
type_unite: person
name: William S. Burroughs
categorie: influence
role:
  - écrivain
  - "figure d'admiration pour Ian Curtis"
sources:
  - S75
  - S54
  - S56
same_as:
  - PERS-S54-003
  - PERS-S56-004
  - PERS-S75-033
alt_names: []
categorie_a_arbitrer: false
a_arbitrer: false
```

