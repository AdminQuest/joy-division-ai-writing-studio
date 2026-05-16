# Compléments aux registres spécialisés — S11 — HM Treasury, *Financial Statement and Budget Report 1987-88*, 1987

```yaml
source_id: S11
source_label: "S11 — HM Treasury, Financial Statement and Budget Report 1987-88, 1987"
type_unite: registres_specialises
statut: integration_directe
fiabilite: forte
```

## Citations / formulations candidates

```yaml
citations:
  - id: S11-Q001
    source_id: S11
    page_pdf: 5
    citation_originale: "defeat inflation and maintain a vigorous, enterprising economy"
    langue_originale: en
    statut_verification: a_reverifier
    usage: "Formule synthétique du récit économique officiel."
    related_atoms:
      - S11-A001
    prudence: "Citation courte à vérifier visuellement avant publication."

  - id: S11-Q002
    source_id: S11
    page_pdf: 8
    citation_originale: "The Medium Term Financial Strategy continues to provide the framework for the Government's economic policy"
    langue_originale: en
    statut_verification: a_reverifier
    usage: "Formule de cadrage de la MTFS."
    related_atoms:
      - S11-A002
    prudence: "Citation courte ; vérifier le texte exact avant insertion."

  - id: S11-Q003
    source_id: S11
    page_pdf: 51
    citation_originale: "reducing steadily the state's share of the nation's income"
    langue_originale: en
    statut_verification: a_reverifier
    usage: "Formule centrale sur la baisse relative de la dépense publique."
    related_atoms:
      - S11-A004
    prudence: "À citer avec référence au chapitre 5 et au tableau 5.1."
```

## Chronologie

```yaml
events:
  - id: CHR-S11-1987-001
    date: "1987-03-17"
    precision_date: jour
    event: "Présentation et impression du Financial Statement and Budget Report 1987-88 sur ordre de la Chambre des communes."
    type: publication_gouvernementale
    location: "London"
    people: []
    organizations:
      - HM Treasury
      - House of Commons
    sources:
      - S11
    certainty: strong
    related_atoms:
      - S11-A001

  - id: CHR-S11-1987-002
    date: "1987-03-17"
    precision_date: jour
    event: "Le budget 1987 annonce la réduction du basic rate of income tax de 29 % à 27 %."
    type: mesure_fiscale
    location: "United Kingdom"
    organizations:
      - HM Treasury
    sources:
      - S11
    certainty: strong
    related_atoms:
      - S11-A003

  - id: CHR-S11-1987-003
    date: "1987-1988"
    precision_date: exercice
    event: "Le FSBR fixe un PSBR prévisionnel proche de 1 % du PIB pour 1987-88."
    type: prevision_budgetaire
    location: "United Kingdom"
    organizations:
      - HM Treasury
    sources:
      - S11
    certainty: strong
    related_atoms:
      - S11-A005

  - id: CHR-S11-1987-004
    date: "1987"
    precision_date: annee
    event: "Le FSBR prévoit une croissance du PIB d’environ 3 % et une inflation autour de 4 % en fin d’année."
    type: prevision_macro
    location: "United Kingdom"
    organizations:
      - HM Treasury
    sources:
      - S11
    certainty: strong
    related_atoms:
      - S11-A006
```

## Acteurs

```yaml
people:
  - id: PERSONNE-S11-001
    name: "Nigel Lawson"
    role_in_s11: "Chancellor of the Exchequer présentant le Budget 1987, même si le document porte institutionnellement HM Treasury."
    related_atoms:
      - S11-A001
      - S11-A003
    prudence: "Le document est signé institutionnellement ; éviter de personnaliser excessivement."

  - id: PERSONNE-S11-002
    name: "Margaret Thatcher"
    role_in_s11: "Figure politique du cadre thatchérien dans lequel s’inscrit le FSBR."
    related_atoms:
      - S11-A001
      - S11-A004
      - S11-A005
    prudence: "S11 est un document Treasury ; Thatcher est le contexte politique, non l’autrice."
```

## Organisations

```yaml
organizations:
  - id: ORG-S11-001
    name: "HM Treasury"
    type: institution_gouvernementale
    role_in_s11: "Auteur institutionnel du FSBR 1987-88."
    related_atoms:
      - S11-A001
      - S11-A002

  - id: ORG-S11-002
    name: "House of Commons"
    type: parlement
    role_in_s11: "Institution ordonnant l’impression du document le 17 mars 1987."
    related_atoms:
      - S11-A001

  - id: ORG-S11-003
    name: "Her Majesty’s Stationery Office"
    type: editeur_public
    role_in_s11: "Éditeur officiel du document."
    related_atoms:
      - S11-A001

  - id: ORG-S11-004
    name: "Bank of England"
    type: banque_centrale
    role_in_s11: "Institution liée aux conditions monétaires, aux taux d’intérêt et aux agrégats monétaires."
    related_atoms:
      - S11-A002
```

## Lieux

```yaml
places:
  - id: PLACE-S11-001
    name: "United Kingdom"
    type: pays
    role_in_s11: "Échelle nationale des indicateurs macroéconomiques et budgétaires."
    related_atoms:
      - S11-A006
      - S11-A007
      - S11-A008

  - id: PLACE-S11-002
    name: "London"
    type: capitale
    role_in_s11: "Lieu institutionnel de publication et de présentation budgétaire."
    related_atoms:
      - S11-A001

  - id: PLACE-S11-003
    name: "Manchester / Salford"
    type: contrepoint_local
    role_in_s11: "Échelle locale à ne pas déduire directement du FSBR ; à croiser avec sources urbaines et culturelles."
    related_atoms:
      - S11-A010
```

## Chansons / albums

```yaml
songs_and_albums: []
```

S11 ne doit alimenter aucun registre chanson. Son usage est macro-contextuel.
