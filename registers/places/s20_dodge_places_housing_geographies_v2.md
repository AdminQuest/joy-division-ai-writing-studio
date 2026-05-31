# S20 — Compléments au registre des lieux — géographies du logement mancunien

```yaml
id: PLACES-S20-HOUSING-GEOGRAPHIES-V2
source_id: S20
source_label: "S20 — Dodge, Mapping Manchester's housing problems, Manchester Geographies, s.d."
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-LITTLE-IRELAND
    lat: 53.4731
    lng: -2.2419
    geo_precision: quartier
    reference_croisee: ["wikidata:Q10567938"]
    prudence_methodologique: >-
      Quartier ouvrier irlandais disparu, démoli au XIXe siècle.
      Coordonnée = centroïde de la zone historique au confluent
      Medlock/Oxford Road (Wikidata P625 Q10567938).
    label: "Little Ireland"
    type: quartier
    type_detail: quartier_taudis_victorien
    sources:
      - S20-A002
      - S07
    usage: "Figure du logement ouvrier insalubre dans le Manchester industriel, située près du Medlock."
    prudence: "À traiter comme lieu social et sanitaire, non comme simple motif noir."

  - id: PLACE-ANGEL-MEADOW
    label: "Angel Meadow"
    type: quartier
    type_detail: quartier_taudis_victorien
    sources:
      - S20-A002
    usage: "Lieu emblématique du taudis victorien mancunien, utile pour la profondeur historique de l'insalubrité urbaine."

  - id: PLACE-VICTORIA-PARK-MANCHESTER
    lat: 53.456
    lng: -2.213
    geo_precision: quartier
    label: "Victoria Park"
    type: habitat
    type_detail: suburb_bourgeois
    sources:
      - S20-A003
    usage: "Exemple de ségrégation résidentielle bourgeoise au XIXe siècle."

  - id: PLACE-CHORLTONVILLE
    lat: 53.434
    lng: -2.279
    geo_precision: quartier
    reference_croisee: ["wikidata:Q5105186"]
    label: "Chorltonville"
    type: habitat
    type_detail: garden_suburb
    sources:
      - S20-A006
    usage: "Exemple de solution garden suburb à portée sociale limitée."

  - id: PLACE-WYTHENSHAWE
    lat: 53.392
    lng: -2.264
    geo_precision: quartier
    reference_croisee: ["wikidata:Q3570246"]
    label: "Wythenshawe"
    type: ville
    type_detail: ville_satellite
    sources:
      - S20-A007
      - S20-A008
    usage: "Grand espace de relogement municipal, pensé comme ville satellite et solution à la surdensité des inner neighbourhoods."
    prudence: "Ne pas présenter comme pur progrès : intégrer distance, équipements insuffisants et isolement."

  - id: PLACE-HULME
    label: "Hulme"
    type: quartier
    type_detail: quartier_inner_city
    sources:
      - S20-A008
      - S20-A010
      - S06
    usage: "Quartier central dans les politiques de dédensification, clearance et urban renewal."
    prudence: "Croiser S20 avec S06 pour l'expérience vécue de Hulme."

  - id: PLACE-HATTERSLEY
    lat: 53.444
    lng: -2.043
    geo_precision: quartier
    reference_croisee: ["wikidata:Q3128340"]
    label: "Hattersley"
    type: habitat
    type_detail: overspill_estate
    sources:
      - S20-A009
    usage: "Grand estate périphérique illustrant le déplacement de la pauvreté et le désancrage social."

  - id: PLACE-BESWICK
    lat: 53.4743
    lng: -2.20266
    geo_precision: quartier
    reference_croisee: ["wikidata:Q4897126"]
    label: "Beswick"
    type: quartier
    type_detail: quartier_inner_city
    sources:
      - S20-A010
      - S20-A011
    usage: "Quartier de clearance et d'expérimentation moderniste autour du Wellington Street estate."

  - id: PLACE-FORT-BESWICK
    lat: 53.47430
    lng: -2.20070
    geo_precision: quartier
    reference_croisee: ["wikidata:Q4897126"]
    prudence_methodologique: >-
      Wellington Street Estate (Fort Beswick). Source :
      https://personalpages.manchester.ac.uk/staff/m.dodge/Fort-Beswick-Been-Gone-and-Forgotten.pdf.
      Coordonnée du secteur Beswick, pas du bloc précis.
    label: "Fort Beswick"
    type: habitat
    type_detail: estate_moderniste
    sources:
      - S20-A011
      - S20-A013
    usage: "Nom péjoratif du Wellington Street estate, emblématique de l'échec des deck-access estates."

  - id: PLACE-WELLINGTON-STREET-ESTATE
    label: "Wellington Street estate"
    type: habitat
    type_detail: deck_access_estate
    sources:
      - S20-A011
      - S20-A013
    usage: "Cas détaillé d'urban renewal et de mégastructure à Beswick."

  - id: PLACE-STRETFORD-ROAD
    label: "Stretford Road"
    type: quartier
    type_detail: axe_urbain
    sources:
      - S20-A010
    usage: "Axe associé à la renewal de Hulme et à l'effacement du tissu urbain ancien."
```
