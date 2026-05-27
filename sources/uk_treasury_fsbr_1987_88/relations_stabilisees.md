# Relations stabilisées — S11 — HM Treasury, *Financial Statement and Budget Report 1987-88*, 1987

```yaml
source_id: S11
source_label: "S11 — HM Treasury, Financial Statement and Budget Report 1987-88, 1987"
type_unite: relations_stabilisees
statut: integration_directe
fiabilite: forte
atomes_source:
  - S11-A001
  - S11-A002
  - S11-A003
  - S11-A004
  - S11-A005
  - S11-A006
  - S11-A007
  - S11-A008
  - S11-A009
  - S11-A010
```

## REL-S11-001 — MTFS → désinflation → discipline budgétaire

```yaml
id: REL-S11-001
source_id: S11
relation_type: doctrine_macro
de:
  - Medium Term Financial Strategy
  - M0
  - money GDP
vers:
  - désinflation
  - PSBR bas
  - discipline budgétaire
atomes:
  - S11-A001
  - S11-A002
  - S11-A005
chapitres:
  - Chapitre 1
stabilite: forte
```

Le FSBR articule la stratégie économique autour de la désinflation et du contrôle nominal. La réduction du PSBR et la trajectoire de la dépense publique sont présentées comme conditions d’un environnement monétaire stable.

## REL-S11-002 — baisse fiscale → récit de l’entreprise

```yaml
id: REL-S11-002
source_id: S11
relation_type: discours_fiscal
de:
  - baisse de l’impôt sur le revenu
  - personal allowances
  - profit-related pay
vers:
  - motivation
  - entreprise
  - efficacité
  - emploi
atomes:
  - S11-A003
chapitres:
  - Chapitre 1
stabilite: forte
```

La baisse fiscale n’est pas seulement comptable. Dans le FSBR, elle appartient au récit de l’entreprise : réduire l’impôt, alléger les charges et encourager la motivation individuelle.

## REL-S11-003 — dépense publique → baisse de la part de l’État

```yaml
id: REL-S11-003
source_id: S11
relation_type: transformation_etat
de:
  - public expenditure
  - general government expenditure
vers:
  - réduction de la part de l’État
  - baisse fiscale
  - efficacité
atomes:
  - S11-A004
  - S11-A005
chapitres:
  - Chapitre 1
stabilite: forte
```

Le document présente la baisse relative de la dépense publique comme un objectif politique durable. La réduction de la part de l’État dans le revenu national devient un marqueur du thatchérisme tardif.

## REL-S11-004 — privatisation → PSBR → retrait de l’État producteur

```yaml
id: REL-S11-004
source_id: S11
relation_type: finances_publiques
de:
  - privatisation proceeds
  - public corporations
vers:
  - PSBR
  - retrait de l’État producteur
  - cadrage budgétaire
atomes:
  - S11-A005
chapitres:
  - Chapitre 1
stabilite: forte
prudence: "Ne pas confondre produit de privatisation et amélioration structurelle locale."
```

Les privatisations entrent dans la construction du solde public. Elles portent aussi une signification politique : le retrait de l’État producteur et la reconfiguration du secteur public.

## REL-S11-005 — reprise officielle → tension avec récits culturels du déclin

```yaml
id: REL-S11-005
source_id: S11
relation_type: tension_historiographique
de:
  - croissance officielle
  - inflation basse
  - baisse du chômage
vers:
  - récits culturels du déclin
  - Manchester post-industrielle
  - mémoire post-punk
atomes:
  - S11-A006
  - S11-A007
  - S11-A010
chapitres:
  - Chapitre 1
  - Chapitre 14
stabilite: forte
```

S11 permet de faire apparaître une tension d’écriture : en 1987, le gouvernement affirme la stabilisation de l’économie, alors que les récits culturels du Nord industriel restent marqués par le déclassement, la perte et la mémoire de la crise.

## REL-S11-006 — compétitivité nationale → expérience locale non déductible

```yaml
id: REL-S11-006
source_id: S11
relation_type: prudence_echelle
de:
  - manufacturing output
  - productivity
  - competitiveness
vers:
  - non-extrapolation locale
  - Manchester / Salford
atomes:
  - S11-A008
  - S11-A010
chapitres:
  - Chapitre 1
stabilite: forte
prudence: "Les données nationales ne prouvent pas l’expérience locale de Manchester."
```

La compétitivité manufacturière nationale ne permet pas de déduire automatiquement la condition locale des anciens bassins industriels. S11 sert de contrepoint macro, non de source locale.

## REL-S11-007 — local authorities → cadrage financier national des collectivités

```yaml
id: REL-S11-007
source_id: S11
relation_type: finances_locales
de:
  - local authorities
  - rates
  - grants
  - borrowing
vers:
  - cadrage national des collectivités
  - contrôle de la dépense publique
atomes:
  - S11-A009
chapitres:
  - Chapitre 1
stabilite: forte
```

Le FSBR intègre les collectivités locales dans l’agrégat public. Il les pense à travers dépense, recettes, subventions, rates et borrowing, ce qui permet d’éclairer le contexte national de contrainte financière locale.

## REL-S11-008 — FSBR officiel → contrepoint, non réfutation

```yaml
id: REL-S11-008
source_id: S11
relation_type: methode_historiographique
de:
  - FSBR 1987-88
  - récit officiel
vers:
  - contrepoint macroéconomique
  - sources urbaines et culturelles
atomes:
  - S11-A010
chapitres:
  - Chapitre 1
  - Chapitre 14
stabilite: forte
```

S11 ne réfute pas S15, S20, S06 ou les témoignages musicaux. Il ajoute un niveau : la langue officielle d’un gouvernement qui raconte une économie rétablie, au moment où la mémoire culturelle continue de travailler le déclin.
