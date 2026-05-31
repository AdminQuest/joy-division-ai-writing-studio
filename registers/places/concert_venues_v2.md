# Lieux de concerts — extension du registre des lieux (étape 7a)

> Extension **additive** du registre des lieux (`PLACE-`), préalable à la
> réconciliation des concerts (étape 7b). Source des lieux :
> `docs/audits/audit_unitaire_concerts_12b-4.md` (PR #33) — venues des 88
> `concert_a_migrer` + composantes gig des 11 `a_scinder_concert`.
> Doctrine : identité **source-agnostique** `PLACE-<SLUG>` (NAMING §10,
> `docs/conventions/identifiants_lieux.md`). **Coordonnées DIFFÉRÉES** —
> identité sans lat/lng, géolocalisation par curation manuelle uniquement
> (jamais de géocodage auto au build), comme les lieux non encore localisés.
> Aucun `PLACE-` existant renommé ; les 3 venues déjà résolus (Electric
> Circus, Rafters, Stoneground/Mayflower) sont **réutilisés, non dupliqués**.

```yaml
id: PLACES-CONCERT-VENUES-V2
type_unite: registre_lieux
source_label: "Étape 7a — lieux de concerts (chronologie S41/S45/S75/S76)"
statut: integration_directe
```

```yaml
places:
  - id: PLACE-RUSSELL-CLUB
    label: "Russell Club (The Factory)"
    type: salle
    type_detail: club
    sources:
      - S41
      - S45
    usage: "Club de Royce Road, Hulme ; siège des soirées « The Factory » (Wilson/Erasmus) et venue récurrent de Joy Division."
  - id: PLACE-BAND-ON-THE-WALL
    label: "Band on the Wall"
    type: salle
    type_detail: salle_concert
    sources:
      - S41
      - S76
    usage: "Salle de Swan Street, Manchester ; concert de Joy Division (deal Factory annoncé)."
  - id: PLACE-KELLYS-MANCHESTER
    label: "Kelly's"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Club de Manchester ; concert Rock Against Racism de Joy Division."
  - id: PLACE-PIPERS-CYPRUS-TAVERN
    label: "Pipers (Cyprus Tavern)"
    type: salle
    type_detail: club
    sources:
      - S76
    usage: "Soirée « Pipers » au Cyprus Tavern, Princess Street, Manchester ; concert de Warsaw. Distinct du club « Pips » (PLACE-PIPS)."
  - id: PLACE-MANCHESTER-APOLLO
    label: "Manchester Apollo"
    type: salle
    type_detail: salle_concert
    sources:
      - S76
    usage: "Grande salle de Manchester ; concert de Joy Division (tournée nationale 1979)."
  - id: PLACE-OLDHAM-TOWER-CLUB
    label: "Oldham Tower Club"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Tower Club d'Oldham ; concert de Warsaw/Joy Division devant un public quasi nul."
  - id: PLACE-CHECK-INN-ALTRINCHAM
    label: "Check Inn, Altrincham"
    type: salle
    type_detail: club
    sources:
      - S41
      - S45
    usage: "Club d'Altrincham ; concert de Joy Division."
  - id: PLACE-BOWDON-VALE-YOUTH-CLUB
    label: "Bowdon Vale Youth Club"
    type: salle
    type_detail: youth_club
    sources:
      - S41
      - S76
    usage: "Youth club de la région d'Altrincham ; concert filmé par Malcolm Whitehead (« She's Lost Control »)."
  - id: PLACE-NEW-OSBOURNE-CLUB
    label: "New Osbourne Club"
    type: salle
    type_detail: club
    sources:
      - S45
    usage: "Club de Manchester ; concert bénéfice *City Fun*."
  - id: PLACE-SALFORD-TECHNICAL-COLLEGE
    label: "Salford Technical College"
    type: education
    type_detail: college_technique
    sources:
      - S41
      - S76
    usage: "Établissement de Salford ; concert de Warsaw (avec Drones / Slaughter & The Dogs / V2)."
    prudence_methodologique: >-
      Canonique sémantique de l'institution technique de Salford. Réconciliation
      (étape 7b-1) : PLACE-S83-004 (« Salford Technical School », facette S83 / rencontre
      Hannett 1977) porte désormais same_as vers ce canonique ; la mention joydiv « Salford
      College of Technology » désigne le même établissement. Variance de nom (School /
      College) conservée, statut S83 a_verifier inchangé.
  - id: PLACE-ERICS-LIVERPOOL
    label: "Eric's"
    type: salle
    type_detail: club
    sources:
      - S41
      - S76
    usage: "Club emblématique de Mathew Street, Liverpool ; concerts de Joy Division (dont avec les Rich Kids)."
  - id: PLACE-SWINGING-APPLE-LIVERPOOL
    label: "Swinging Apple, Liverpool"
    type: salle
    type_detail: club
    sources:
      - S41
      - S76
    usage: "Club de Liverpool ; dernier concert sous le nom Warsaw (réveillon 1977)."
    prudence_methodologique: >-
      VARIANTE DE NOM (un seul lieu) : « Swinging Apple » (S41) / « Spinning Apple » (S76) —
      orthographe à trancher à la curation ; non dédoublé.
  - id: PLACE-LIVERPOOL-EMPIRE
    label: "Liverpool Empire"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S76
    usage: "Théâtre de Liverpool ; concert de Lou Reed (1973) auquel assiste Ian Curtis — venue de concert d'un autre artiste, conservé comme lieu."
  - id: PLACE-QUEENS-HALL-LEEDS
    label: "Queen's Hall, Leeds"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S41
      - S45
      - S76
    usage: "Grande halle de Leeds ; hôte du Futurama Festival 1979 où joue Joy Division."
  - id: PLACE-LEEDS-UNIVERSITY
    label: "Leeds University"
    type: education
    type_detail: universite
    sources:
      - S41
    usage: "Université de Leeds ; concert de Joy Division (tournée Buzzcocks)."
  - id: PLACE-ROOTS-CLUB-LEEDS
    label: "Roots Club, Leeds"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Club de Leeds ; concert de Joy Division avec la Durutti Column."
  - id: PLACE-FAN-CLUB-LEEDS
    label: "F Club (Brannigan's), Leeds"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Le « F Club » au Brannigan's, Leeds ; concert de Joy Division."
  - id: PLACE-ROCK-GARDEN-MIDDLESBROUGH
    label: "Rock Garden, Middlesbrough"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Club de Middlesbrough ; concert de Warsaw promu par Bob Last."
  - id: PLACE-NEWCASTLE-TOWN-HALL
    label: "Newcastle Town Hall (annexe)"
    type: salle
    type_detail: salle_municipale
    sources:
      - S41
      - S76
    usage: "Annexe du Town Hall de Newcastle ; concert de Warsaw avec Penetration."
  - id: PLACE-CAIRD-HALL-DUNDEE
    label: "Caird Hall, Dundee"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S41
    usage: "Salle de Dundee ; concert de Joy Division (tournée Buzzcocks) où Ian s'effondre."
  - id: PLACE-ROYAL-STANDARD-BRADFORD
    label: "Royal Standard, Bradford"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Pub-venue de Bradford ; concert de Joy Division."
  - id: PLACE-COACH-HOUSE-HUDDERSFIELD
    label: "Coach House, Huddersfield"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Salle de Huddersfield ; concert de Joy Division devant un public minuscule."
  - id: PLACE-WAREHOUSE-PRESTON
    label: "The Warehouse, Preston"
    type: salle
    type_detail: club
    sources:
      - S76
    usage: "Club de Preston ; concert de Joy Division avec Section 25. Distinct de PLACE-WAREHOUSE-CHICAGO."
  - id: PLACE-WINTER-GARDENS-MALVERN
    label: "Winter Gardens, Malvern"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S76
    usage: "Salle de Malvern ; concert de Joy Division."
  - id: PLACE-THE-SQUAT-MANCHESTER
    label: "The Squat, Manchester"
    type: salle
    type_detail: lieu_alternatif
    sources:
      - S41
    usage: "Bâtiment universitaire désaffecté (Devas Street, Manchester) occupé ; plusieurs concerts de Warsaw (Stuff the Jubilee, Time's Up)."
  - id: PLACE-DERBY-HALL-BURY
    label: "Derby Hall, Bury"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S41
      - S75
      - S76
    usage: "Salle du complexe municipal de Bury ; avant-dernier concert (8 avril 1980), Curtis très affaibli."
    prudence_methodologique: >-
      VARIANTE DE NOM (un seul lieu) : « Derby Hall, Bury » (S75/S76) et « Bury Town Hall »
      (S41) désignent le même complexe — non dédoublé.
  - id: PLACE-AJANTA-THEATRE-DERBY
    label: "Ajanta Theatre, Derby"
    type: salle
    type_detail: salle_spectacle
    sources:
      - S41
    usage: "Cinéma-théâtre de Derby ; avant-dernier concert de Joy Division (19 avril 1980)."
  - id: PLACE-RAINBOW-THEATRE-LONDON
    label: "Rainbow Theatre, London"
    type: salle
    type_detail: salle_concert
    sources:
      - S41
      - S45
      - S75
      - S76
    usage: "Salle de Finsbury Park, Londres ; concerts de Joy Division (dont la crise de Curtis sous stroboscopes, 4 avril 1980)."
  - id: PLACE-ELECTRIC-BALLROOM-CAMDEN
    label: "Electric Ballroom, Camden"
    type: salle
    type_detail: salle_concert
    sources:
      - S41
      - S76
    usage: "Salle de Camden, Londres ; concerts de Joy Division."
  - id: PLACE-MOONLIGHT-CLUB-LONDON
    label: "Moonlight Club, West Hampstead"
    type: salle
    type_detail: club
    sources:
      - S76
    usage: "Club de West Hampstead, Londres ; mini-résidence de Joy Division (avril 1980)."
  - id: PLACE-YMCA-LONDON
    label: "YMCA, London"
    type: salle
    type_detail: salle_polyvalente
    sources:
      - S41
    usage: "Centre YMCA de Londres ; concerts de Joy Division."
    prudence_methodologique: >-
      DÉSAMBIGUÏSATION INCERTAINE (non tranchée) : les mentions « YMCA Prince of Wales
      Conference Centre » (2 août 1979) et « YMCA, Tottenham Court Road » (1979) pourraient
      désigner UN ou DEUX lieux distincts — regroupé provisoirement sous un seul PLACE- ; à
      scinder à la curation si confirmé distinct.
  - id: PLACE-BRUNEL-UNIVERSITY
    label: "Brunel University, Uxbridge"
    type: education
    type_detail: universite
    sources:
      - S41
    usage: "Université de Brunel, Uxbridge ; concert de Joy Division interrompu (crachats / coupure)."
  - id: PLACE-WALTHAMSTOW-YOUTH-CLUB
    label: "Walthamstow Youth Club"
    type: salle
    type_detail: youth_club
    sources:
      - S41
    usage: "Youth club de Walthamstow, Londres ; concert de Joy Division (interview d'Annik Honoré après)."
  - id: PLACE-ACKLAM-HALL-LONDON
    label: "Acklam Hall, London"
    type: salle
    type_detail: salle_concert
    sources:
      - S76
    usage: "Salle sous l'autoroute (Ladbroke Grove), Londres ; concert de Joy Division le lendemain de la naissance de Natalie."
  - id: PLACE-HIGH-WYCOMBE-TOWN-HALL
    label: "High Wycombe Town Hall"
    type: salle
    type_detail: salle_municipale
    sources:
      - S76
    usage: "Town Hall de High Wycombe ; concert de Joy Division avec Killing Joke."
  - id: PLACE-LOCARNO-BRISTOL
    label: "Locarno, Bristol"
    type: salle
    type_detail: salle_concert
    sources:
      - S41
    usage: "Salle de Bristol ; Joy Division fait la balance mais ne joue pas (éjection) — concert non tenu, lieu conservé."
  - id: PLACE-HOPE-AND-ANCHOR-LONDON
    label: "Hope & Anchor, Islington"
    type: salle
    type_detail: club
    sources:
      - S10
      - S41
      - S45
      - S75
      - S76
    usage: "Pub-venue d'Islington, Londres ; premier concert londonien (27 déc. 1978), suivi de la première crise de Curtis. Composante GIG des bundles a_scinder."
  - id: PLACE-NASHVILLE-ROOMS-LONDON
    label: "Nashville Rooms, London"
    type: salle
    type_detail: club
    sources:
      - S41
      - S76
    usage: "Pub-venue de West Kensington, Londres ; concert (13 août 1979) où Annik Honoré voit le groupe. Composante GIG des bundles a_scinder."
  - id: PLACE-MARQUEE-LONDON
    label: "Marquee Club, London"
    type: salle
    type_detail: club
    sources:
      - S41
    usage: "Club de Wardour Street, Londres ; concert de Joy Division en support de The Cure (4 mars 1979). Composante GIG d'un bundle a_scinder."
  - id: PLACE-PLAN-K-BRUSSELS
    label: "Plan K, Brussels"
    type: salle
    type_detail: club
    sources:
      - S41
      - S75
      - S76
    usage: "Espace culturel de Bruxelles ; concerts de Joy Division avec Cabaret Voltaire."
  - id: PLACE-LES-BAINS-DOUCHES-PARIS
    label: "Les Bains Douches, Paris"
    type: salle
    type_detail: club
    sources:
      - S41
      - S76
    usage: "Club parisien ; concert de Joy Division (longue setlist)."
  - id: PLACE-PARADISO-AMSTERDAM
    label: "Paradiso, Amsterdam"
    type: salle
    type_detail: salle_concert
    sources:
      - S76
    usage: "Salle d'Amsterdam ; concert de la tournée européenne (janvier 1980)."
  - id: PLACE-BASEMENT-COLOGNE
    label: "Basement, Cologne"
    type: salle
    type_detail: club
    sources:
      - S76
    usage: "Club underground de Cologne ; concert de la tournée européenne."
  - id: PLACE-EFFENAAR-EINDHOVEN
    label: "Effenaar, Eindhoven"
    type: salle
    type_detail: salle_concert
    sources:
      - S76
    usage: "Salle d'Eindhoven ; concert avec Minny Pops (tournée européenne)."
```

