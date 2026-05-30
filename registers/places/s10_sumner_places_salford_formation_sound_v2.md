# S10 — Compléments au registre des lieux — Salford, Manchester, Factory et studio

```yaml
id: PLACES-S10-SUMNER-SALFORD-FORMATION-SOUND-V2
source_id: S10
source_label: "S10 — Sumner, Chapter and Verse, 2014/2015"
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-ALFRED-STREET
    label: "Alfred Street"
    type: quartier
    type_detail: rue_ouvriere
    sources:
      - S10-A001
      - S10-A004
    usage_s10: "Rue d’enfance de Bernard Sumner à Lower Broughton ; communauté ouvrière détruite par clearance."
    prudence: "Ne pas idéaliser la communauté ; intégrer violence, pauvreté, toxicité industrielle et destruction."

  - id: PLACE-LOWER-BROUGHTON
    label: "Lower Broughton"
    type: quartier
    type_detail: quartier_salford
    sources:
      - S10-A001
      - S10-A002
    usage_s10: "Quartier d’enfance de Sumner, marqué par industries, prison, Irwell et sociabilité ouvrière."

  - id: PLACE-WHEATHILL-CHEMICAL-WORKS
    label: "Wheathill Chemical Works"
    type: industrie
    type_detail: site_industriel
    sources:
      - S10-A002
    usage_s10: "Usine chimique au bout d’Alfred Street, mémorisée par Sumner comme source d’odeurs et de toxicité."

  - id: PLACE-ORDSALL
    label: "Ordsall"
    type: quartier
    type_detail: quartier_salford
    sources:
      - S10-A005
    usage_s10: "Lieu de la scène nocturne des lampadaires au sodium que Sumner associe au son de Joy Division."

  - id: PLACE-GREENGATE
    label: "Greengate"
    type: habitat
    type_detail: tower_block_relogement
    sources:
      - S10-A003
    usage_s10: "Lieu du relogement familial de Sumner en tower block ; confort matériel mais perte de rue et de communauté."

  - id: PLACE-SALFORD-GRAMMAR-SCHOOL
    lat: 53.488
    lng: -2.298
    geo_precision: rue
    prudence_methodologique: >-
      Établissement nommé = bâtiment (granularité rue) ; coordonnée approximative
      à l'échelle de Salford, bâtiment précis non confirmé.
    label: "Salford Grammar School"
    type: education
    type_detail: ecole
    sources:
      - S10-A007
    usage_s10: "Lieu de rencontre de Bernard Sumner, Peter Hook, Terry Mason et autres membres de leur sociabilité adolescente."

  - id: PLACE-NORTH-SALFORD-YOUTH-CLUB
    label: "North Salford Youth Club"
    type: salle
    type_detail: youth_club
    sources:
      - S10-A008
    usage_s10: "Lieu d’exposition à soul, ska, rock, Led Zeppelin, Santana, Stones et Black Sabbath."

  - id: PLACE-LESSER-FREE-TRADE-HALL
    lat: 53.4779
    lng: -2.247
    geo_precision: exacte
    prudence_methodologique: >-
      Petite salle AU SEIN du Free Trade Hall — distincte du grand hall (PLACE-FREE-TRADE-HALL) ; même bâtiment, point partagé.
    label: "Lesser Free Trade Hall"
    type: salle
    type_detail: salle_concert
    sources:
      - S10-A010
    usage_s10: "Lieu du concert des Sex Pistols du 4 juin 1976, décisif mais non miraculeux selon Sumner."

  - id: PLACE-VIRGIN-RECORDS-LEVER-STREET
    label: "Virgin Records, Lever Street"
    type: commerce
    type_detail: disquaire_hub_punk
    sources:
      - S10-A013
    usage_s10: "Lieu où Sumner et Hook déposent l’annonce pour recruter un chanteur."

  - id: PLACE-GREY-MARE
    label: "Grey Mare"
    type: studio
    type_detail: lieu_repetition
    sources:
      - S10-A014
    usage_s10: "Salle de répétition au-dessus d’un pub de Weaste, associée aux débuts avec Curtis."

  - id: PLACE-ELECTRIC-CIRCUS
    lat: 53.493
    lng: -2.221
    geo_precision: rue
    prudence_methodologique: >-
      Collyhurst ; salle fermée en 1977, démolie.
    label: "Electric Circus"
    type: salle
    type_detail: salle_concert
    sources:
      - S10-A015
    usage_s10: "Lieu du premier concert de Warsaw / Stiff Kittens le 29 mai 1977."

  - id: PLACE-RAFTERS-MANCHESTER
    label: "Rafters"
    type: salle
    type_detail: salle_concert
    sources:
      - S10-A016
    usage_s10: "Lieu du concert d’avril 1978 qui déclenche la rencontre avec Rob Gretton."

  - id: PLACE-TJ-DAVIDSONS
    lat: 53.474
    lng: -2.249
    geo_precision: rue
    prudence_methodologique: >-
      Entrepôt de répétition, Little Peter Street ; bâtiment d'origine disparu.
    label: "TJ Davidson’s"
    type: studio
    type_detail: lieu_repetition
    sources:
      - S10-A016
      - S10-A017
    usage_s10: "Lieu de répétition central, proche du futur Haçienda, associé à Gretton et aux photographies de Curtis."

  - id: PLACE-GREENDOW-COMMERCIALS-STUDIO
    label: "Greendow Commercials studio"
    type: studio
    type_detail: studio
    sources:
      - S10-A018
    usage_s10: "Studio commercial où se déroulent les sessions RCA / album avorté."

  - id: PLACE-PENNINE-STUDIOS-OLDHAM
    label: "Pennine Studios, Oldham"
    type: studio
    type_detail: studio
    sources:
      - S10-A019
    usage_s10: "Studio de l’enregistrement d’An Ideal for Living."

  - id: PLACE-STRAWBERRY-STUDIOS
    lat: 53.4084
    lng: -2.157
    geo_precision: exacte
    reference_croisee: ["wikidata:Q7622496"]
    prudence_methodologique: >-
      Studio fermé en 1993 ; bâtiment conservé (Stockport).
    label: "Strawberry Studios"
    type: studio
    type_detail: studio
    sources:
      - S10-A020
      - S10-A021
    usage_s10: "Studio de Stockport où Sumner découvre avec Hannett le studio comme instrument."

  - id: PLACE-LUTON-HOSPITAL
    label: "Hôpital de Luton"
    type: sante
    type_detail: hopital
    sources:
      - S10-A024
    usage_s10: "Lieu de prise en charge après la crise épileptique de Curtis au retour du Hope and Anchor."
```
