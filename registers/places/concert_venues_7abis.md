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
    lat: 51.52131
    lng: -0.13052
    geo_precision: exacte
    geo_source: "Action Space, 16 Chenies Street, London WC1"
    source_url: "https://archiveshub.jisc.ac.uk/mediaImages/bristoltheatrecollection_811/5/032/5032008.pdf"
    note_geo: "adresse issue d’un programme d’époque."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Action Space, 16 Chenies Street, London WC1. Source : https://archiveshub.jisc.ac.uk/mediaImages/bristoltheatrecollection_811/5/032/5032008.pdf. adresse issue d’un programme d’époque.
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
    lat: 55.94670
    lng: -3.20410
    geo_precision: site
    geo_source: "Astoria, Edinburgh"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "salle à documenter plus finement."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Astoria, Edinburgh. Source : https://www.joydiv.org/concerts.htm. salle à documenter plus finement.
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
    lat: 53.57550
    lng: -2.42920
    geo_precision: campus
    geo_source: "Bolton Institute of Technology / University of Bolton, Deane Road"
    source_url: "https://www.new-order.net/jd/gigs/"
    note_geo: "concert listé mais annulé."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Bolton Institute of Technology / University of Bolton, Deane Road. Source : https://www.new-order.net/jd/gigs/. concert listé mais annulé.
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
    lat: 57.14577
    lng: -2.10531
    geo_precision: exacte
    geo_source: "Capitol Theatre, Union Street, Aberdeen"
    source_url: "https://en.wikipedia.org/wiki/Capitol_Theatre,_Aberdeen"
    note_geo: "ancien cinéma/théâtre."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Capitol Theatre, Union Street, Aberdeen. Source : https://en.wikipedia.org/wiki/Capitol_Theatre,_Aberdeen. ancien cinéma/théâtre.
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
    lat: 51.89785
    lng: -8.46537
    geo_precision: exacte
    geo_source: "Cork City Hall, Anglesea Street, Cork"
    source_url: "https://en.wikipedia.org/wiki/Cork_City_Hall"
    note_geo: "bâtiment stable."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Cork City Hall, Anglesea Street, Cork. Source : https://en.wikipedia.org/wiki/Cork_City_Hall. bâtiment stable.
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
    lat: 53.827301
    lng: -3.054586
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
    lat: 51.91816
    lng: 4.47661
    geo_precision: exacte
    geo_source: "Club Lantaren, Gouvernestraat 133, Rotterdam"
    source_url: "https://www.enkiri.com/joy/gigs/ve_rotterdam_cl_la1.html"
    note_geo: "concert européen du 16 janvier 1980."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Club Lantaren, Gouvernestraat 133, Rotterdam. Source : https://www.enkiri.com/joy/gigs/ve_rotterdam_cl_la1.html. concert européen du 16 janvier 1980.
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
    lat: 53.37990
    lng: -1.47130
    geo_precision: rue
    geo_source: "The Limit Club, Sheffield"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "club disparu ; adresse à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — The Limit Club, Sheffield. Source : https://www.joydiv.org/concerts.htm. club disparu ; adresse à confirmer.
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
    lat: 53.40555
    lng: -2.96691
    geo_precision: exacte
    geo_source: "Mountford Hall, Liverpool Guild of Students"
    source_url: "https://www.liverpoolguild.org/venue-hire/mountford-hall"
    note_geo: "salle universitaire stable."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Mountford Hall, Liverpool Guild of Students. Source : https://www.liverpoolguild.org/venue-hire/mountford-hall. salle universitaire stable.
    label: "Mountford Hall (Liverpool University)"
    type: salle
    type_detail: salle_universitaire
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEW-THEATRE-OXFORD
    lat: 51.75353
    lng: -1.26176
    geo_precision: exacte
    geo_source: "New Theatre Oxford, George Street"
    source_url: "https://www.atgtickets.com/venues/new-theatre-oxford/"
    note_geo: "théâtre toujours existant."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — New Theatre Oxford, George Street. Source : https://www.atgtickets.com/venues/new-theatre-oxford/. théâtre toujours existant.
    label: "New Theatre, Oxford"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEWCASTLE-CITY-HALL
    lat: 54.97770
    lng: -1.61360
    geo_precision: exacte
    geo_source: "Newcastle City Hall, Northumberland Road"
    source_url: "https://www.o2cityhallnewcastle.co.uk/"
    note_geo: "salle toujours existante."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Newcastle City Hall, Northumberland Road. Source : https://www.o2cityhallnewcastle.co.uk/. salle toujours existante.
    label: "Newcastle City Hall"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-NEWCASTLE-GUILDHALL
    lat: 54.96980
    lng: -1.61080
    geo_precision: exacte
    geo_source: "Newcastle Guildhall, Quayside"
    source_url: "https://historicengland.org.uk/listing/the-list/list-entry/1024773"
    note_geo: "bâtiment historique."
    label: "Newcastle Guildhall"
    type: salle
    type_detail: salle_municipale
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
    prudence_methodologique: >-
      Regroupe les graphies joydiv « Guild Hall » et « Guildhall » (même lieu).
  - id: PLACE-ODEON-BIRMINGHAM
    lat: 52.47990
    lng: -1.89820
    geo_precision: site
    geo_source: "Odeon Birmingham, New Street"
    source_url: "https://cinematreasures.org/theaters/9137"
    note_geo: "localisation historique."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Odeon Birmingham, New Street. Source : https://cinematreasures.org/theaters/9137. localisation historique.
    label: "Odeon, Birmingham"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ODEON-CANTERBURY
    lat: 51.27970
    lng: 1.07920
    geo_precision: site
    geo_source: "Odeon Canterbury"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "adresse fine à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Odeon Canterbury. Source : https://www.joydiv.org/concerts.htm. adresse fine à confirmer.
    label: "Odeon, Canterbury"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ODEON-EDINBURGH
    lat: 55.94720
    lng: -3.20400
    geo_precision: site
    geo_source: "Odeon Edinburgh / Clerk Street area"
    source_url: "https://cinematreasures.org/theaters/2322"
    note_geo: "localisation historique."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Odeon Edinburgh / Clerk Street area. Source : https://cinematreasures.org/theaters/2322. localisation historique.
    label: "Odeon, Edinburgh"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-OLYMPIA-DUBLIN
    lat: 53.34430
    lng: -6.26600
    geo_precision: exacte
    geo_source: "Olympia Theatre, Dame Street, Dublin"
    source_url: "https://www.3olympia.ie/"
    note_geo: "théâtre toujours existant."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Olympia Theatre, Dame Street, Dublin. Source : https://www.3olympia.ie/. théâtre toujours existant.
    label: "Olympia Theatre, Dublin"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PAARD-VAN-TROJE-THE-HAGUE
    lat: 52.07864
    lng: 4.31333
    geo_precision: exacte
    geo_source: "Paard van Troje, Prinsegracht 12, Den Haag"
    source_url: "https://www.paard.nl/"
    note_geo: "salle toujours existante."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Paard van Troje, Prinsegracht 12, Den Haag. Source : https://www.paard.nl/. salle toujours existante.
    label: "Paard van Troje, The Hague"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PAVILION-HEMEL-HEMPSTEAD
    lat: 51.75240
    lng: -0.47250
    geo_precision: site
    geo_source: "Pavilion, Hemel Hempstead"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "adresse fine à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Pavilion, Hemel Hempstead. Source : https://www.joydiv.org/concerts.htm. adresse fine à confirmer.
    label: "Pavilion, Hemel Hempstead"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-PLAYHOUSE-THEATRE-NOTTINGHAM
    lat: 52.95391
    lng: -1.15422
    geo_precision: exacte
    geo_source: "Nottingham Playhouse, Wellington Circus"
    source_url: "https://nottinghamplayhouse.co.uk/"
    note_geo: "théâtre stable."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Nottingham Playhouse, Wellington Circus. Source : https://nottinghamplayhouse.co.uk/. théâtre stable.
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
    lat: 51.51160
    lng: -0.12820
    geo_precision: site
    geo_source: "Royalty Theatre, London"
    source_url: "https://cinematreasures.org/theaters/24986"
    note_geo: "lieu disparu / reconverti ; localisation historique à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Royalty Theatre, London. Source : https://cinematreasures.org/theaters/24986. lieu disparu / reconverti ; localisation historique à confirmer.
    label: "Royalty Theatre, London"
    type: salle
    type_detail: theatre
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SCALA-CINEMA-LONDON
    lat: 51.53084
    lng: -0.12036
    geo_precision: exacte
    geo_source: "Scala, 275 Pentonville Road, London"
    source_url: "https://scala.co.uk/"
    note_geo: "ancien cinéma, salle actuelle."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Scala, 275 Pentonville Road, London. Source : https://scala.co.uk/. ancien cinéma, salle actuelle.
    label: "Scala Cinema, London"
    type: salle
    type_detail: cinema_salle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SHEFFIELD-POLYTECHNIC
    lat: 53.38140
    lng: -1.46630
    geo_precision: campus
    geo_source: "Sheffield Polytechnic / Sheffield Hallam University"
    source_url: "https://www.shu.ac.uk/"
    note_geo: "campus central."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Sheffield Polytechnic / Sheffield Hallam University. Source : https://www.shu.ac.uk/. campus central.
    label: "Sheffield Polytechnic"
    type: education
    type_detail: polytechnique
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SOPHIA-GARDENS-CARDIFF
    lat: 51.48610
    lng: -3.19120
    geo_precision: site
    geo_source: "Sophia Gardens Pavilion, Cardiff"
    source_url: "https://en.wikipedia.org/wiki/Sophia_Gardens_Pavilion"
    note_geo: "ancien pavillon, démoli."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Sophia Gardens Pavilion, Cardiff. Source : https://en.wikipedia.org/wiki/Sophia_Gardens_Pavilion. ancien pavillon, démoli.
    label: "Sophia Gardens Pavilion, Cardiff"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-SOUTHAMPTON-UNIVERSITY
    lat: 50.93440
    lng: -1.39580
    geo_precision: campus
    geo_source: "University of Southampton, Highfield Campus"
    source_url: "https://www.southampton.ac.uk/about/our-campuses/highfield-campus.page"
    note_geo: "campus, salle exacte à préciser."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — University of Southampton, Highfield Campus. Source : https://www.southampton.ac.uk/about/our-campuses/highfield-campus.page. campus, salle exacte à préciser.
    label: "Southampton University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ST-ANDREWS-UNIVERSITY
    lat: 56.34170
    lng: -2.79280
    geo_precision: campus
    geo_source: "University of St Andrews"
    source_url: "https://www.st-andrews.ac.uk/"
    note_geo: "campus, salle exacte à préciser."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — University of St Andrews. Source : https://www.st-andrews.ac.uk/. campus, salle exacte à préciser.
    label: "St Andrews University"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-ST-GEORGES-HALL-BRADFORD
    lat: 53.79343
    lng: -1.75276
    geo_precision: exacte
    geo_source: "St George’s Hall, Bradford"
    source_url: "https://www.bradford-theatres.co.uk/venues/st-georges-hall"
    note_geo: "salle toujours existante."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — St George’s Hall, Bradford. Source : https://www.bradford-theatres.co.uk/venues/st-georges-hall. salle toujours existante.
    label: "St George's Hall, Bradford"
    type: salle
    type_detail: salle_spectacle
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-STOCKPORT-COLLEGE
    lat: 53.40860
    lng: -2.15870
    geo_precision: site
    geo_source: "Stockport College"
    source_url: "https://stockport.tscg.ac.uk/"
    note_geo: "établissement stable, site modernisé."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Stockport College. Source : https://stockport.tscg.ac.uk/. établissement stable, site modernisé.
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
    lat: 52.63700
    lng: -1.13270
    geo_precision: site
    geo_source: "Tiffany’s, Leicester"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "salle disparue ; localisation fine à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Tiffany’s, Leicester. Source : https://www.joydiv.org/concerts.htm. salle disparue ; localisation fine à confirmer.
    label: "Tiffany's, Leicester"
    type: salle
    type_detail: club
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TOP-RANK-READING
    lat: 51.45620
    lng: -0.97110
    geo_precision: site
    geo_source: "Top Rank, Reading"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "salle disparue ; adresse fine à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Top Rank, Reading. Source : https://www.joydiv.org/concerts.htm. salle disparue ; adresse fine à confirmer.
    label: "Top Rank, Reading"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-TOP-RANK-SHEFFIELD
    lat: 53.38100
    lng: -1.46820
    geo_precision: site
    geo_source: "Top Rank, Sheffield"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "salle disparue ; adresse fine à confirmer."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Top Rank, Sheffield. Source : https://www.joydiv.org/concerts.htm. salle disparue ; adresse fine à confirmer.
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
    lat: 54.59401
    lng: -5.93008
    geo_precision: exacte
    geo_source: "Ulster Hall, Bedford Street, Belfast"
    source_url: "https://www.ulsterhall.co.uk/"
    note_geo: "salle toujours existante."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — Ulster Hall, Bedford Street, Belfast. Source : https://www.ulsterhall.co.uk/. salle toujours existante.
    label: "Ulster Hall, Belfast"
    type: salle
    type_detail: salle_concert
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-UNIVERSITY-OF-KENT
    lat: 51.29650
    lng: 1.06310
    geo_precision: campus
    geo_source: "University of Kent, Canterbury"
    source_url: "https://www.kent.ac.uk/locations/canterbury"
    note_geo: "campus, salle exacte à préciser."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — University of Kent, Canterbury. Source : https://www.kent.ac.uk/locations/canterbury. campus, salle exacte à préciser.
    label: "University of Kent, Canterbury"
    type: education
    type_detail: universite
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-UNIVERSITY-OF-LONDON-UNION
    lat: 51.52210
    lng: -0.13070
    geo_precision: exacte
    geo_source: "University of London Union, Malet Street, London"
    source_url: "https://en.wikipedia.org/wiki/University_of_London_Union"
    note_geo: "ancien ULU."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — University of London Union, Malet Street, London. Source : https://en.wikipedia.org/wiki/University_of_London_Union. ancien ULU.
    label: "University of London Union (ULU)"
    type: education
    type_detail: union_etudiante
    sources:
      - joydiv
    usage: "Venue de concert de Joy Division (source joydiv.org)."
  - id: PLACE-WEST-RUNTON-PAVILION
    lat: 52.93530
    lng: 1.24410
    geo_precision: site
    geo_source: "West Runton Pavilion, Norfolk"
    source_url: "https://www.joydiv.org/concerts.htm"
    note_geo: "salle disparue ; site approximatif."
    prudence_methodologique: >-
      Géolocalisation C3A-6B — West Runton Pavilion, Norfolk. Source : https://www.joydiv.org/concerts.htm. salle disparue ; site approximatif.
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
