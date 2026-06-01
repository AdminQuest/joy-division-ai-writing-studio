# Registre lieux — Venues de concerts (lot 3, étape 10)

Promotion en entrées `PLACE-` des salles de concerts géolocalisées (lot 3).
Coordonnées WGS84 curées (recoupées sources d'époque / Cinema Treasures /
Joy Division Central). `geo_precision` ∈ {exacte, rue, quartier, ville, region}.
Câblées aux fiches concerts via `place_id` (cf. registers/concerts/).

```yaml
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-9-30-CLUB-WASHINGTON
    label: "9:30 Club, Washington DC"
    type: salle
    lat: 38.89733
    lng: -77.0245
    geo_precision: exacte
    prudence_methodologique: "Original 9:30 Club, 930 F Street NW, Washington DC. Concert prévu, tournée américaine annulée."

  - id: PLACE-ACTIONSPACE-LONDON
    label: "Action Space, London"
    type: salle
    lat: 51.52131
    lng: -0.13052
    geo_precision: exacte
    prudence_methodologique: "Action Space, 16 Chenies Street, London WC1. Adresse issue d'un programme d'époque."

  - id: PLACE-AJANTA-THEATRE-DERBY
    label: "Ajanta Theatre, Derby"
    type: salle
    lat: 52.9189
    lng: -1.4769
    geo_precision: quartier
    prudence_methodologique: "Ancien cinéma ; localisation fine à confirmer par plan historique."

  - id: PLACE-AMERICAN-INDIAN-CENTER-SF
    label: "American Indian Center, San Francisco"
    type: salle
    lat: 37.76919
    lng: -122.42217
    geo_precision: exacte
    prudence_methodologique: "225 Valencia Street, San Francisco. Concert prévu, tournée américaine annulée."

  - id: PLACE-ASTORIA-EDINBURGH
    label: "Astoria, Edinburgh"
    type: salle
    lat: 55.9467
    lng: -3.2041
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; localisation approximée, adresse fine à documenter."

  - id: PLACE-BAND-ON-THE-WALL
    label: "Band on the Wall, Manchester"
    type: salle
    lat: 53.48514
    lng: -2.23488
    geo_precision: exacte
    prudence_methodologique: "25 Swan Street, Manchester. Salle toujours existante."

  - id: PLACE-BOLTON-INSTITUTE-OF-TECHNOLOGY
    label: "Bolton Institute of Technology"
    type: education
    lat: 53.5755
    lng: -2.4292
    geo_precision: quartier
    prudence_methodologique: "Bolton Institute / University of Bolton, Deane Road. Concert listé mais annulé. Coordonnée de campus."

  - id: PLACE-BOOKIES-DETROIT
    label: "Bookies Club, Detroit"
    type: salle
    lat: 42.4181
    lng: -83.0806
    geo_precision: rue
    prudence_methodologique: "Concert prévu, tournée américaine annulée. Adresse précise à confirmer."

  - id: PLACE-BOWDON-VALE-YOUTH-CLUB
    label: "Bowdon Vale Youth Club, Altrincham"
    type: salle
    lat: 53.3813
    lng: -2.3622
    geo_precision: quartier
    prudence_methodologique: "Adresse exacte non stabilisée."

  - id: PLACE-BRUNEL-UNIVERSITY
    label: "Brunel University, Uxbridge"
    type: education
    lat: 51.53285
    lng: -0.47275
    geo_precision: quartier
    prudence_methodologique: "Concert du 15 novembre 1978. Coordonnée de campus, salle exacte non précisée."

  - id: PLACE-CAIRD-HALL-DUNDEE
    label: "Caird Hall, Dundee"
    type: salle
    lat: 56.45961
    lng: -2.97055
    geo_precision: exacte
    prudence_methodologique: "City Square, Dundee. Salle municipale."

  - id: PLACE-CAPITOL-ABERDEEN
    label: "Capitol Theatre, Aberdeen"
    type: salle
    lat: 57.14577
    lng: -2.10531
    geo_precision: exacte
    prudence_methodologique: "Union Street, Aberdeen. Ancien cinéma / théâtre."

  - id: PLACE-CITY-HALL-CORK
    label: "Cork City Hall"
    type: salle
    lat: 51.89785
    lng: -8.46537
    geo_precision: exacte
    prudence_methodologique: "Anglesea Street, Cork."

  - id: PLACE-DUFFYS-MINNEAPOLIS
    label: "Duffy's, Minneapolis"
    type: salle
    lat: 44.9489
    lng: -93.2882
    geo_precision: rue
    prudence_methodologique: "Concert prévu, tournée américaine annulée. Adresse précise à confirmer."

  - id: PLACE-FAN-CLUB-LEEDS
    label: "The Fan Club, Leeds"
    type: salle
    lat: 53.7984
    lng: -1.5439
    geo_precision: quartier
    prudence_methodologique: "The Fan Club / Brannigan's, Leeds. Salle disparue ; localisation fine à vérifier."

  - id: PLACE-FLIPPERS-LOS-ANGELES
    label: "Flipper's Roller Boogie Palace, Los Angeles"
    type: salle
    lat: 34.0837
    lng: -118.3461
    geo_precision: quartier
    prudence_methodologique: "Concert prévu, tournée américaine annulée. Adresse exacte à confirmer."

  - id: PLACE-HIGH-WYCOMBE-TOWN-HALL
    label: "High Wycombe Town Hall"
    type: salle
    lat: 51.62861
    lng: -0.74902
    geo_precision: exacte
    prudence_methodologique: "Queen Victoria Road."

  - id: PLACE-HURRAH-NEW-YORK
    label: "Hurrah, New York"
    type: salle
    lat: 40.7648
    lng: -73.9761
    geo_precision: quartier
    prudence_methodologique: "Concert prévu, tournée américaine annulée. Localisation associée à West 62nd Street ; à confirmer."

  - id: PLACE-KELLYS-MANCHESTER
    label: "Kelly's, Manchester"
    type: salle
    lat: 53.4912
    lng: -2.2401
    geo_precision: rue
    prudence_methodologique: "Amber Street, Manchester. Club disparu."

  - id: PLACE-LANTAREN-ROTTERDAM
    label: "Club Lantaren, Rotterdam"
    type: salle
    lat: 51.91816
    lng: 4.47661
    geo_precision: exacte
    prudence_methodologique: "Gouvernestraat 133, Rotterdam. Concert européen du 16 janvier 1980."

  - id: PLACE-LEEDS-UNIVERSITY
    label: "University of Leeds"
    type: education
    lat: 53.8067
    lng: -1.555
    geo_precision: quartier
    prudence_methodologique: "Coordonnée de campus, salle exacte à préciser selon la date du concert."

  - id: PLACE-LIMIT-CLUB-SHEFFIELD
    label: "The Limit Club, Sheffield"
    type: salle
    lat: 53.3799
    lng: -1.4713
    geo_precision: rue
    prudence_methodologique: "Club disparu ; adresse à confirmer."

  - id: PLACE-LIVERPOOL-EMPIRE
    label: "Liverpool Empire Theatre"
    type: salle
    lat: 53.40854
    lng: -2.97841
    geo_precision: exacte
    prudence_methodologique: "Lime Street, Liverpool. Théâtre toujours existant. Aucune fiche concert correspondante dans le registre actuel."

  - id: PLACE-LOCARNO-BRISTOL
    label: "Locarno, Bristol"
    type: salle
    lat: 51.4572
    lng: -2.5928
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; localisation fine à vérifier."

  - id: PLACE-MANCHESTER-APOLLO
    label: "Manchester Apollo"
    type: salle
    lat: 53.46918
    lng: -2.22285
    geo_precision: exacte
    prudence_methodologique: "Stockport Road, Ardwick. Salle toujours existante. Fiches concerts sous « Apollo Theatre »."

  - id: PLACE-MOUNTFORD-HALL-LIVERPOOL
    label: "Mountford Hall, Liverpool"
    type: salle
    lat: 53.40555
    lng: -2.96691
    geo_precision: exacte
    prudence_methodologique: "Liverpool Guild of Students. Salle universitaire stable."

  - id: PLACE-NEW-THEATRE-OXFORD
    label: "New Theatre Oxford"
    type: salle
    lat: 51.75353
    lng: -1.26176
    geo_precision: exacte
    prudence_methodologique: "George Street. Théâtre toujours existant."

  - id: PLACE-NEWCASTLE-CITY-HALL
    label: "Newcastle City Hall"
    type: salle
    lat: 54.9777
    lng: -1.6136
    geo_precision: exacte
    prudence_methodologique: "Northumberland Road. Salle toujours existante."

  - id: PLACE-NEWCASTLE-GUILDHALL
    label: "Newcastle Guildhall"
    type: salle
    lat: 54.9698
    lng: -1.6108
    geo_precision: exacte
    prudence_methodologique: "Quayside. Bâtiment historique protégé. Fiches concerts sous « Guildhall » et « Guild Hall »."

  - id: PLACE-ODEON-BIRMINGHAM
    label: "Odeon, Birmingham"
    type: salle
    lat: 52.4799
    lng: -1.8982
    geo_precision: quartier
    prudence_methodologique: "New Street. Bâtiment démoli ou transformé ; localisation historique."

  - id: PLACE-ODEON-CANTERBURY
    label: "Odeon, Canterbury"
    type: salle
    lat: 51.2797
    lng: 1.0792
    geo_precision: quartier
    prudence_methodologique: "Adresse fine à confirmer."

  - id: PLACE-ODEON-EDINBURGH
    label: "Odeon, Edinburgh"
    type: salle
    lat: 55.9472
    lng: -3.204
    geo_precision: quartier
    prudence_methodologique: "Secteur Clerk Street. Localisation historique (Cinema Treasures #2322)."

  - id: PLACE-OLDHAM-TOWER-CLUB
    label: "Tower Club, Oldham"
    type: salle
    lat: 53.5409
    lng: -2.1113
    geo_precision: quartier
    prudence_methodologique: "Adresse précise à confirmer. Aucune fiche concert correspondante dans le registre actuel."

  - id: PLACE-OLYMPIA-DUBLIN
    label: "Olympia Theatre, Dublin"
    type: salle
    lat: 53.3443
    lng: -6.266
    geo_precision: exacte
    prudence_methodologique: "Dame Street. Théâtre toujours existant."

  - id: PLACE-PAARD-VAN-TROJE-THE-HAGUE
    label: "Paard van Troje, Den Haag"
    type: salle
    lat: 52.07864
    lng: 4.31333
    geo_precision: exacte
    prudence_methodologique: "Prinsegracht 12, Den Haag. Salle toujours existante."

  - id: PLACE-PAVILION-HEMEL-HEMPSTEAD
    label: "Pavilion, Hemel Hempstead"
    type: salle
    lat: 51.7524
    lng: -0.4725
    geo_precision: quartier
    prudence_methodologique: "Adresse fine à confirmer."

  - id: PLACE-PIPERS-CYPRUS-TAVERN
    label: "Piper's, Manchester"
    type: salle
    lat: 53.4804
    lng: -2.2396
    geo_precision: rue
    prudence_methodologique: "Spring Gardens, Manchester. Ne pas confondre avec Cyprus Tavern — Joy Division Central signale explicitement cette confusion."

  - id: PLACE-PLAYHOUSE-THEATRE-NOTTINGHAM
    label: "Nottingham Playhouse"
    type: salle
    lat: 52.95391
    lng: -1.15422
    geo_precision: exacte
    prudence_methodologique: "Wellington Circus. Théâtre stable."

  - id: PLACE-ROCK-GARDEN-MIDDLESBROUGH
    label: "Rock Garden, Middlesbrough"
    type: salle
    lat: 54.5763
    lng: -1.2354
    geo_precision: quartier
    prudence_methodologique: "Localisation fine à confirmer."

  - id: PLACE-ROYALTY-THEATRE-LONDON
    label: "Royalty Theatre, London"
    type: salle
    lat: 51.5116
    lng: -0.1282
    geo_precision: quartier
    prudence_methodologique: "Lieu disparu ou reconverti ; localisation historique à confirmer."

  - id: PLACE-RUSSELL-CLUB
    label: "Russell Club / Factory, Hulme"
    type: salle
    lat: 53.4677
    lng: -2.2561
    geo_precision: rue
    prudence_methodologique: "Royce Road, Hulme. Club démoli ; situé près de Royce Road / Clayburn Street. Lieu des Factory nights — « The Factory I » dans le registre des concerts (≠ The Factory II)."

  - id: PLACE-SCALA-CINEMA-LONDON
    label: "Scala, London"
    type: salle
    lat: 51.53084
    lng: -0.12036
    geo_precision: exacte
    prudence_methodologique: "275 Pentonville Road. Ancien cinéma, salle actuelle."

  - id: PLACE-SHEFFIELD-POLYTECHNIC
    label: "Sheffield Polytechnic"
    type: education
    lat: 53.3814
    lng: -1.4663
    geo_precision: quartier
    prudence_methodologique: "Sheffield Hallam University. Coordonnée de campus central."

  - id: PLACE-SOPHIA-GARDENS-CARDIFF
    label: "Sophia Gardens Pavilion, Cardiff"
    type: salle
    lat: 51.4861
    lng: -3.1912
    geo_precision: quartier
    prudence_methodologique: "Ancien pavillon démoli."

  - id: PLACE-SOUTHAMPTON-UNIVERSITY
    label: "University of Southampton"
    type: education
    lat: 50.9344
    lng: -1.3958
    geo_precision: quartier
    prudence_methodologique: "Highfield Campus. Salle exacte à préciser."

  - id: PLACE-ST-ANDREWS-UNIVERSITY
    label: "University of St Andrews"
    type: education
    lat: 56.3417
    lng: -2.7928
    geo_precision: quartier
    prudence_methodologique: "Coordonnée de campus, salle exacte à préciser."

  - id: PLACE-ST-GEORGES-HALL-BRADFORD
    label: "St George's Hall, Bradford"
    type: salle
    lat: 53.79343
    lng: -1.75276
    geo_precision: exacte
    prudence_methodologique: "Salle toujours existante."

  - id: PLACE-STARWOOD-LOS-ANGELES
    label: "The Starwood, Los Angeles"
    type: salle
    lat: 34.0902
    lng: -118.3853
    geo_precision: quartier
    prudence_methodologique: "West Hollywood. Concert prévu, tournée américaine annulée. Localisation historique à confirmer."

  - id: PLACE-STOCKPORT-COLLEGE
    label: "Stockport College"
    type: education
    lat: 53.4086
    lng: -2.1587
    geo_precision: quartier
    prudence_methodologique: "Site modernisé ; localisation approximée. Fiches concerts sous « Stockport Tech »."

  - id: PLACE-TIER-3-NEW-YORK
    label: "Tier 3, New York"
    type: salle
    lat: 40.7197
    lng: -74.0047
    geo_precision: quartier
    prudence_methodologique: "Concert prévu, tournée américaine annulée. Localisation associée à Tribeca ; à confirmer."

  - id: PLACE-TIFFANYS-LEICESTER
    label: "Tiffany's, Leicester"
    type: salle
    lat: 52.637
    lng: -1.1327
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; localisation fine à confirmer."

  - id: PLACE-TOP-RANK-READING
    label: "Top Rank, Reading"
    type: salle
    lat: 51.4562
    lng: -0.9711
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; adresse fine à confirmer."

  - id: PLACE-TOP-RANK-SHEFFIELD
    label: "Top Rank, Sheffield"
    type: salle
    lat: 53.381
    lng: -1.4682
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; adresse fine à confirmer."

  - id: PLACE-ULSTER-HALL-BELFAST
    label: "Ulster Hall, Belfast"
    type: salle
    lat: 54.59401
    lng: -5.93008
    geo_precision: exacte
    prudence_methodologique: "Bedford Street. Salle toujours existante."

  - id: PLACE-UNIVERSITY-OF-KENT
    label: "University of Kent, Canterbury"
    type: education
    lat: 51.2965
    lng: 1.0631
    geo_precision: quartier
    prudence_methodologique: "Coordonnée de campus, salle exacte à préciser."

  - id: PLACE-UNIVERSITY-OF-LONDON-UNION
    label: "University of London Union"
    type: education
    lat: 51.5221
    lng: -0.1307
    geo_precision: exacte
    prudence_methodologique: "Malet Street, London. Ancien ULU."

  - id: PLACE-WEST-RUNTON-PAVILION
    label: "West Runton Pavilion, Norfolk"
    type: salle
    lat: 52.9353
    lng: 1.2441
    geo_precision: quartier
    prudence_methodologique: "Salle disparue ; site approximatif."

  - id: PLACE-WINTER-GARDENS-MALVERN
    label: "Winter Gardens, Malvern"
    type: salle
    lat: 52.11125
    lng: -2.33037
    geo_precision: exacte
    prudence_methodologique: "Complexe culturel stabilisé."

  - id: PLACE-YMCA-LONDON
    label: "YMCA, London"
    type: salle
    lat: 51.5094
    lng: -0.1311
    geo_precision: quartier
    prudence_methodologique: "Adresse précise à établir selon l'événement."

  # Alias : même institution que PLACE-S83-004 (Salford Technical School).
  # Coordonnée portée par le canonique (S83). Concerts « Salford College of Technology ».
  - id: PLACE-SALFORD-TECHNICAL-COLLEGE
    label: "Salford Technical College"
    type: education
    same_as: PLACE-S83-004
```
