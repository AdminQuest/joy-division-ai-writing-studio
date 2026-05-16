# S20 — Compléments au registre des lieux — géographies du logement mancunien

```yaml
id: PLACES-S20-HOUSING-GEOGRAPHIES-V2
source_id: S20
source_label: "S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-LITTLE-IRELAND
    label: "Little Ireland"
    type: quartier_taudis_victorien
    sources:
      - S20-A002
      - S07
    usage: "Figure du logement ouvrier insalubre dans le Manchester industriel, située près du Medlock."
    prudence: "À traiter comme lieu social et sanitaire, non comme simple motif noir."

  - id: PLACE-ANGEL-MEADOW
    label: "Angel Meadow"
    type: quartier_taudis_victorien
    sources:
      - S20-A002
    usage: "Lieu emblématique du taudis victorien mancunien, utile pour la profondeur historique de l’insalubrité urbaine."

  - id: PLACE-VICTORIA-PARK-MANCHESTER
    label: "Victoria Park"
    type: suburb_bourgeois
    sources:
      - S20-A003
    usage: "Exemple de ségrégation résidentielle bourgeoise au XIXe siècle."

  - id: PLACE-CHORLTONVILLE
    label: "Chorltonville"
    type: garden_suburb
    sources:
      - S20-A006
    usage: "Exemple de solution garden suburb à portée sociale limitée."

  - id: PLACE-WYTHENSHAWE
    label: "Wythenshawe"
    type: ville_satellite
    sources:
      - S20-A007
      - S20-A008
    usage: "Grand espace de relogement municipal, pensé comme ville satellite et solution à la surdensité des inner neighbourhoods."
    prudence: "Ne pas présenter comme pur progrès : intégrer distance, équipements insuffisants et isolement."

  - id: PLACE-HULME
    label: "Hulme"
    type: quartier_inner_city
    sources:
      - S20-A008
      - S20-A010
      - S06
    usage: "Quartier central dans les politiques de dédensification, clearance et urban renewal."
    prudence: "Croiser S20 avec S06 pour l’expérience vécue de Hulme."

  - id: PLACE-HATTERSLEY
    label: "Hattersley"
    type: overspill_estate
    sources:
      - S20-A009
    usage: "Grand estate périphérique illustrant le déplacement de la pauvreté et le désancrage social."

  - id: PLACE-BESWICK
    label: "Beswick"
    type: quartier_inner_city
    sources:
      - S20-A010
      - S20-A011
    usage: "Quartier de clearance et d’expérimentation moderniste autour du Wellington Street estate."

  - id: PLACE-FORT-BESWICK
    label: "Fort Beswick"
    type: estate_moderniste
    sources:
      - S20-A011
      - S20-A013
    usage: "Nom péjoratif du Wellington Street estate, emblématique de l’échec des deck-access estates."

  - id: PLACE-WELLINGTON-STREET-ESTATE
    label: "Wellington Street estate"
    type: deck_access_estate
    sources:
      - S20-A011
      - S20-A013
    usage: "Cas détaillé d’urban renewal et de mégastructure à Beswick."

  - id: PLACE-STRETFORD-ROAD
    label: "Stretford Road"
    type: axe_urbain
    sources:
      - S20-A010
    usage: "Axe associé à la renewal de Hulme et à l’effacement du tissu urbain ancien."
```
