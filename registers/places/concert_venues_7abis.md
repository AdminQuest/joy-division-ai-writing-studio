# Lieux de concerts (suite) — venues joydiv débloqués (étape 7a-bis)

> Complète l'étape 7a : crée les `PLACE-` des venues joydiv encore bloqués en
> 7b-1 (hors des 47 venues de la chronologie). Identités source-agnostiques
> `PLACE-<SLUG>`, **coordonnées différées** (curation manuelle, jamais de
> géocodage auto). Réconciliation : Free Trade Hall réutilise le `PLACE-` existant ;
> graphies variantes regroupées en un seul `PLACE-`. **Résidu non créé** (non
> identifiable / tournée US-Canada annulée jamais jouée) : voir le rapport 7a-bis.
> Additif ; aucun `PLACE-` existant renommé ; gel EVENT- intact.

```yaml
places:
  - id: PLACE-ACTIONSPACE-LONDON
    label: "Actionspace, London"
    type: salle
    type_detail: espace_alternatif
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ALBERT-HALL-STIRLING
    label: "Albert Hall, Stirling"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 56.11815
    lng: -3.94186
    geo_precision: exacte
    prudence_methodologique: >-
      24 Dumbarton Road ; Historic Environment Scotland LB41099. Source: trove.scot
  - id: PLACE-ASSEMBLY-ROOMS-DERBY
    label: "Assembly Rooms, Derby"
    type: salle
    type_detail: salle_municipale
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 52.92331
    lng: -1.47619
    geo_precision: exacte
    prudence_methodologique: >-
      batiment demoli/transforme ; localisation historique fiable. Source: commons.wikimedia.org
  - id: PLACE-ASTORIA-EDINBURGH
    label: "The Astoria, Edinburgh"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-BANGOR-UNIVERSITY
    label: "Bangor University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.2289
    lng: -4.1269
    geo_precision: quartier
    prudence_methodologique: >-
      campus historique, pas d'une salle precise. Source: bangor.ac.uk
  - id: PLACE-BIRMINGHAM-UNIVERSITY
    label: "University of Birmingham (High Hall)"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 52.45029
    lng: -1.93
    geo_precision: exacte
    prudence_methodologique: >-
      High Hall devenu Chamberlain Hall ; coordonnee calee sur The Vale. Source: enkiri.com
  - id: PLACE-BOLTON-INSTITUTE-OF-TECHNOLOGY
    label: "Bolton Institute of Technology"
    type: education
    type_detail: institut_technique
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-BRADFORD-UNIVERSITY
    label: "Bradford University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.79147
    lng: -1.76607
    geo_precision: quartier
    prudence_methodologique: >-
      coordonnee du campus central/Richmond Building. Source: bradford.ac.uk
  - id: PLACE-CAPITOL-ABERDEEN
    label: "Capitol, Aberdeen"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-CARDIFF-UNIVERSITY
    label: "Cardiff University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 51.48839
    lng: -3.1775
    geo_precision: exacte
    prudence_methodologique: >-
      Cardiff Students' Union, Park Place / Senghennydd Road. Source: cardiff.ac.uk
  - id: PLACE-CITY-HALL-CORK
    label: "City Hall, Cork"
    type: salle
    type_detail: salle_municipale
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-CITY-HALL-HULL
    label: "City Hall, Hull"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.74368
    lng: -0.33979
    geo_precision: exacte
    prudence_methodologique: >-
      batiment liste, Queen Victoria Square, HU1 3RQ. Source: historicengland.org.uk
  - id: PLACE-CIVIC-HALL-GUILDFORD
    label: "Civic Hall, Guildford"
    type: salle
    type_detail: salle_municipale
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 51.23946
    lng: -0.56491
    geo_precision: exacte
    prudence_methodologique: >-
      ancien batiment demoli ; coordonnee du site historique/G Live. Source: setlist.fm
  - id: PLACE-CLUB-VERA-GRONINGEN
    label: "Club Vera, Groningen"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.21703
    lng: 6.57011
    geo_precision: exacte
    prudence_methodologique: >-
      Oosterstraat 44, Groningen ; salle existante. Source: visitgroningen.nl
    reference_croisee:
      - "wikidata:Q17389445"
  - id: PLACE-COATHAM-BOWL-REDCAR
    label: "Coatham Bowl, Redcar"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 54.62083
    lng: -1.08083
    geo_precision: exacte
    prudence_methodologique: >-
      batiment demoli 2014 ; coordonnee approximative secteur Majuba Road. Source: redcar-cleveland.gov.uk
  - id: PLACE-COLSTON-HALL-BRISTOL
    label: "Colston Hall, Bristol"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 51.454
    lng: -2.598
    geo_precision: exacte
    prudence_methodologique: >-
      renommee Bristol Beacon. Source: historicengland.org.uk
    reference_croisee:
      - "wikidata:Q5149374"
  - id: PLACE-DE-MONTFORT-HALL-LEICESTER
    label: "De Montfort Hall, Leicester"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 52.6243
    lng: -1.1216
    geo_precision: exacte
    prudence_methodologique: >-
      batiment stable, Granville Road, LE1 7RU. Source: demontforthall.co.uk
  - id: PLACE-DOORNROOSJE-NIJMEGEN
    label: "Doornroosje, Nijmegen"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 51.83095
    lng: 5.86025
    geo_precision: exacte
    prudence_methodologique: >-
      emplacement d'epoque, Groenewoudseweg 322 ; demenage en 2014. Source: podiuminfo.nl
    reference_croisee:
      - "wikidata:Q2180529"
  - id: PLACE-GOOD-MOOD-HALIFAX
    label: "Good Mood, Halifax"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-IMPERIAL-HOTEL-BLACKPOOL
    label: "Imperial Hotel, Blackpool"
    type: salle
    type_detail: salle_hotel
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.82
    lng: -3.053
    geo_precision: exacte
    prudence_methodologique: >-
      North Promenade FY1 2HB ; hotel toujours existant. Source: imperialhotelblackpool.co.uk
  - id: PLACE-KANT-KINO-BERLIN
    label: "Kant Kino, Berlin"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 52.5069
    lng: 13.30834
    geo_precision: exacte
    prudence_methodologique: >-
      Kantstrasse 54, 10627 Berlin ; salle existante. Source: yorck.de
    reference_croisee:
      - "wikidata:Q42297621"
  - id: PLACE-KING-GEORGES-HALL-BLACKBURN
    label: "King George's Hall, Blackburn"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.74893
    lng: -2.48597
    geo_precision: exacte
    prudence_methodologique: >-
      Regroupe les graphies « King George's Hall » et « King Georges Hall » (même lieu).
      Coordonnees: batiment stable, Northgate, BB2 1AA. Source: visitlancashire.com
  - id: PLACE-KING-KONG-ANTWERPEN
    label: "King Kong, Antwerp"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-LANCASTER-UNIVERSITY
    label: "Lancaster University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 54.00617
    lng: -2.78466
    geo_precision: quartier
    prudence_methodologique: >-
      campus Bailrigg, pas d'une salle precise. Source: lancaster.ac.uk
  - id: PLACE-LANTAREN-ROTTERDAM
    label: "Lantaren, Rotterdam"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-LEIGH-FESTIVAL
    label: "Leigh Open Air Festival (Zoo/Factory)"
    type: salle
    type_detail: festival
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-LIMIT-CLUB-SHEFFIELD
    label: "Limit Club, Sheffield"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-LOUGHBOROUGH-UNIVERSITY
    label: "Loughborough University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 52.7648
    lng: -1.228
    geo_precision: quartier
    prudence_methodologique: >-
      campus etendu ; point central acceptable. Source: lboro.ac.uk
  - id: PLACE-LYCEUM-LONDON
    label: "The Lyceum, London"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 51.51154
    lng: -0.12008
    geo_precision: exacte
    prudence_methodologique: >-
      21 Wellington Street ; batiment stable. Source: latlong.net
  - id: PLACE-MANCHESTER-POLYTECHNIC
    label: "Manchester Polytechnic"
    type: education
    type_detail: polytechnique
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    lat: 53.47053
    lng: -2.23872
    geo_precision: quartier
    prudence_methodologique: >-
      ancien Manchester Polytechnic ; campus All Saints. Source: mmu.ac.uk
  - id: PLACE-METRO-PLYMOUTH
    label: "Metro, Plymouth"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-MOUNTFORD-HALL-LIVERPOOL
    label: "Mountford Hall (Liverpool University)"
    type: salle
    type_detail: salle_universitaire
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEW-THEATRE-OXFORD
    label: "New Theatre, Oxford"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEWCASTLE-CITY-HALL
    label: "Newcastle City Hall"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEWCASTLE-GUILDHALL
    label: "Newcastle Guildhall"
    type: salle
    type_detail: salle_municipale
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    prudence_methodologique: >-
      Regroupe les graphies joydiv « Guild Hall » et « Guildhall » (même lieu).
  - id: PLACE-ODEON-BIRMINGHAM
    label: "Odeon, Birmingham"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ODEON-CANTERBURY
    label: "Odeon, Canterbury"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ODEON-EDINBURGH
    label: "Odeon, Edinburgh"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-OLYMPIA-DUBLIN
    label: "Olympia Theatre, Dublin"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PAARD-VAN-TROJE-THE-HAGUE
    label: "Paard van Troje, The Hague"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PAVILION-HEMEL-HEMPSTEAD
    label: "Pavilion, Hemel Hempstead"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PLAYHOUSE-THEATRE-NOTTINGHAM
    label: "Playhouse Theatre, Nottingham"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-REVOLUTION-CLUB-YORK
    label: "Revolution Club, York"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ROMULUS-CLUB-BIRMINGHAM
    label: "Romulus Club, Birmingham"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ROYALTY-THEATRE-LONDON
    label: "Royalty Theatre, London"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SCALA-CINEMA-LONDON
    label: "Scala Cinema, London"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SHEFFIELD-POLYTECHNIC
    label: "Sheffield Polytechnic"
    type: education
    type_detail: polytechnique
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SOPHIA-GARDENS-CARDIFF
    label: "Sophia Gardens Pavilion, Cardiff"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SOUTHAMPTON-UNIVERSITY
    label: "Southampton University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ST-ANDREWS-UNIVERSITY
    label: "St Andrews University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ST-GEORGES-HALL-BRADFORD
    label: "St George's Hall, Bradford"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-STOCKPORT-COLLEGE
    label: "Stockport College of Technology"
    type: education
    type_detail: college_technique
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-THE-VENUE-MANCHESTER
    label: "The Venue, Manchester"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TIFFANYS-LEICESTER
    label: "Tiffany's, Leicester"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TOP-RANK-READING
    label: "Top Rank, Reading"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TOP-RANK-SHEFFIELD
    label: "Top Rank, Sheffield"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TRINITY-HALL-BRISTOL
    label: "Trinity Hall, Bristol"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ULSTER-HALL-BELFAST
    label: "Ulster Hall, Belfast"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-UNIVERSITY-OF-KENT
    label: "University of Kent, Canterbury"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-UNIVERSITY-OF-LONDON-UNION
    label: "University of London Union (ULU)"
    type: education
    type_detail: union_etudiante
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-WEST-RUNTON-PAVILION
    label: "West Runton Pavilion"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-WYTHENSHAWE-COLLEGE
    label: "Wythenshawe College, Manchester"
    type: education
    type_detail: college
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
```
