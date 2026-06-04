# Registre sessions / répétitions — Joy Division / Warsaw

> **Lot** : C3A-9 — Construction du registre Sessions / Répétitions Joy Division
> **Sources pivots** : joydiv.org, S41 Hook, S45 Deborah Curtis, S75 Ott, S76 Middles/Reade, S88 Cashell
> **Date de consultation joydiv.org** : 4 juin 2026
> **Couverture** : 18 juillet 1977 → 1981
> **Total** : 26 entrées

## Doctrine

Ce registre documente la fabrication du son Joy Division : répétitions,
démos, sessions studio, sessions radio, sessions télévisées et lieux de
travail musical. Les concerts ordinaires restent dans le registre Concerts.

Les répétitions issues de bandes circulantes sont intégrées avec prudence :
joydiv.org les signale souvent comme datées ou localisées de manière
tentative. Elles sont donc marquées `probable` ou `conteste` lorsque la date,
le lieu ou le statut exact de l'enregistrement ne sont pas entièrement
stabilisés.

## Statistiques C3A-9

| Type | Entrées |
|------|---------|
| `demo` | 3 |
| `studio` | 10 |
| `radio` | 3 |
| `television` | 3 |
| `rehearsal` | 7 |

| Statut documentaire | Entrées |
|---------------------|---------|
| `etabli` | 19 |
| `probable` | 5 |
| `conteste` | 2 |

## Sessions

```yaml
- id: JD-SESSION-19770718-001
  numero: 1
  label: "Warsaw demo"
  date: 1977-07-18
  type_session: demo
  studio: "Pennine Sound Studios"
  lieu: "Pennine Sound Studios"
  place_id: PLACE-PENNINE-STUDIOS-OLDHAM
  ville: "Oldham"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Steve Brotherdale"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Warsaw"
  titres:
    - "Inside the Line"
    - "Gutz"
    - "At a Later Date"
    - "The Kill"
    - "You're No Good for Me"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  atomes_lies:
    - S41-A034
    - S41-A035
  relations:
    chronology:
      - CHR-S41-1977-07-18-WARSAW-DEMO-PENNINE
    places:
      - PLACE-PENNINE-STUDIOS-OLDHAM
    people:
      - PERSON-ian-curtis
      - PERSON-bernard-sumner
      - PERSON-peter-hook
  notes: "Première démo Warsaw, enregistrée avec Steve Brotherdale à la batterie."

- id: JD-SESSION-19770900-001
  numero: 2
  label: "Répétition Warsaw août/septembre 1977"
  date: "1977-09-00"
  type_session: rehearsal
  studio: "Lieu non documenté"
  lieu: "Lieu non documenté"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Warsaw"
  titres:
    - "Reaction"
    - "Inside the Line"
    - "Leaders of Men"
    - "Novelty"
    - "The Kill"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: probable
  relations:
    chronology:
      - EVENT-ARRIVEE-STEPHEN-MORRIS
    people:
      - PERSON-ian-curtis
      - PERSON-bernard-sumner
      - PERSON-peter-hook
      - PERSON-stephen-morris
  notes: "joydiv.org date cette bande de façon tentative à août/septembre 1977, avec le 14 septembre 1977 comme hypothèse la plus probable. Le lieu n'est pas stabilisé."

- id: JD-SESSION-19771100-001
  numero: 3
  label: "Répétition Warsaw T.J. Davidson's, automne 1977"
  date: "1977-11-00"
  type_session: rehearsal
  studio: "T.J. Davidson's Rehearsal Room"
  lieu: "T.J. Davidson's Rehearsal Room"
  place_id: PLACE-TJ-DAVIDSONS
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Warsaw"
  titres:
    - "At a Later Date"
    - "Ice Age"
    - "Inside the Line"
    - "Warsaw"
    - "Failures"
    - "No Love Lost"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S76
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: probable
  relations:
    chronology:
      - EVENT-INSTALLATION-TJ-DAVIDSONS
    places:
      - PLACE-TJ-DAVIDSONS
    people:
      - PERSON-ian-curtis
      - PERSON-bernard-sumner
      - PERSON-peter-hook
      - PERSON-stephen-morris
      - PERSON-tony-davidson
  notes: "joydiv.org propose octobre/novembre 1977 et localise la bande comme supposée à T.J. Davidson's. Le statut reste probable."

- id: JD-SESSION-19771200-001
  numero: 4
  label: "An Ideal for Living"
  date: "1977-12-00"
  type_session: demo
  studio: "Pennine Sound Studios"
  lieu: "Pennine Sound Studios"
  place_id: PLACE-PENNINE-STUDIOS-OLDHAM
  ville: "Oldham"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Warsaw"
  titres:
    - "Warsaw"
    - "No Love Lost"
    - "Leaders of Men"
    - "Failures (Of The Modern Man)"
  premiere_sortie_officielle:
    titre: "An Ideal for Living"
    format: "EP"
    label: "Enigma Records"
    annee: "1978"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S45
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    places:
      - PLACE-PENNINE-STUDIOS-OLDHAM
  notes: "EP auto-produit, enregistré en décembre 1977. Le jour exact reste inconnu."

- id: JD-SESSION-19780100-001
  numero: 5
  label: "Répétition T.J. Davidson's — Pictures in My Mind"
  date: "1978-01-00"
  type_session: rehearsal
  studio: "T.J. Davidson's Rehearsal Room"
  lieu: "T.J. Davidson's Rehearsal Room"
  place_id: PLACE-TJ-DAVIDSONS
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Pictures in My Mind"
    - "Shadowplay"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S76
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: probable
  relations:
    chronology:
      - EVENT-INSTALLATION-TJ-DAVIDSONS
    places:
      - PLACE-TJ-DAVIDSONS
  notes: "Répétition datée tentativement de janvier 1978 par joydiv.org. Elle documente le passage entre le répertoire Warsaw et Joy Division."

- id: JD-SESSION-19780503-001
  numero: 6
  label: "RCA sessions (album inédit)"
  date: 1978-05-03
  type_session: studio
  studio: "Arrow Studios"
  lieu: "Arrow Studios"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "John Anderson, Bob Auger, Richard Searling"
  ingenieur_son: "Bob Auger"
  ere: "Joy Division"
  titres:
    - "The Drawback"
    - "Leaders of Men"
    - "Walked in Line"
    - "Failures"
    - "Novelty"
    - "No Love Lost"
    - "Transmission"
    - "Ice Age"
    - "Interzone"
    - "Warsaw"
    - "Shadowplay"
  premiere_sortie_officielle:
    titre: "Warsaw"
    format: "compilation retrospective"
    label: "Movieplay Gold"
    annee: "1994"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S45
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  chronologie_id: "CHR-1978-001"
  relations:
    chronology:
      - EVENT-SESSIONS-RCA-ARROW-STUDIOS
      - CHR-1978-001
    people:
      - PERSON-john-anderson
      - PERSON-bob-auger
      - PERSON-richard-searling
  notes: "Sessions des 3-4 mai 1978 pour l'album RCA avorté. Publication ultérieure contestée par les ayants droit."

- id: JD-SESSION-19780920-001
  numero: 7
  label: "Granada Reports — Shadowplay"
  date: 1978-09-20
  type_session: television
  studio: "Granada TV"
  lieu: "Granada TV"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Tony Wilson"]
  producteur: "Tony Wilson / Granada TV"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Shadowplay"
  premiere_sortie_officielle:
    titre: "Substance"
    format: "video / compilation"
    label: "Factory"
    annee: "1988"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S45
  urls:
    - "https://www.joydiv.org/jdtv.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-DEBUT-TELEVISION-GRANADA-SHADOWPLAY
    people:
      - PERSON-tony-wilson
  notes: "Première apparition télévisée de Joy Division, présentée par Tony Wilson sur Granada Reports."

- id: JD-SESSION-19781011-001
  numero: 8
  label: "A Factory Sample"
  date: 1978-10-11
  type_session: studio
  studio: "Cargo Studios"
  lieu: "Cargo Studios"
  place_id: PLACE-CARGO-STUDIOS
  ville: "Rochdale"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Digital"
    - "Glass"
  premiere_sortie_officielle:
    titre: "A Factory Sample"
    format: "EP double 7 pouces"
    label: "Factory Records (FAC 2)"
    annee: "1978"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-ENREGISTREMENT-A-FACTORY-SAMPLE-CARGO
    places:
      - PLACE-CARGO-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Première collaboration studio avec Martin Hannett."

- id: JD-SESSION-19790131-001
  numero: 9
  label: "John Peel Session 1"
  date: 1979-01-31
  type_session: radio
  studio: "BBC Studios Maida Vale"
  lieu: "BBC Studios Maida Vale"
  place_id: PLACE-MAIDA-VALE-STUDIOS
  ville: "London"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Bob Sargeant"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Exercise One"
    - "Insight"
    - "Transmission"
    - "She's Lost Control"
  premiere_sortie_officielle:
    titre: "The Peel Sessions"
    format: "EP 12 pouces"
    label: "Strange Fruit Records"
    annee: "1986"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-PREMIERE-PEEL-SESSION
    places:
      - PLACE-MAIDA-VALE-STUDIOS
    people:
      - PERSON-john-peel
  notes: "Première Peel Session, diffusée le 14 février 1979."

- id: JD-SESSION-19790300-001
  numero: 10
  label: "Répétition dite Bedge tape"
  date: "1979-03-00"
  type_session: rehearsal
  studio: "Lieu incertain"
  lieu: "Band on the Wall ou Eric's selon cassette, mais probablement répétition"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "No Love Lost"
    - "Leaders of Men"
    - "Day of the Lords"
    - "Shadowplay"
    - "Ice Age"
    - "New Dawn Fades"
    - "Digital"
    - "Insight"
    - "The Kill"
    - "Transmission"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: conteste
  relations: {}
  notes: "joydiv.org indique que la cassette porte une attribution live possible, mais que le contenu sonne comme une répétition. Aucun lieu canonique ne doit être créé sans validation."

- id: JD-SESSION-19790304-001
  numero: 11
  label: "Genetic Demos"
  date: 1979-03-04
  type_session: demo
  studio: "Eden Studios"
  lieu: "Eden Studios"
  ville: "London"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Rushent"]
  producteur: "Martin Rushent"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Glass"
    - "Transmission"
    - "Ice Age"
    - "Insight"
    - "Digital"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    people:
      - PERSON-martin-rushent
  notes: "Démos pour Genetic Records / Martin Rushent, sans concrétisation contractuelle."

- id: JD-SESSION-19790400-001
  numero: 12
  label: "Unknown Pleasures sessions"
  date: "1979-04-00"
  type_session: studio
  studio: "Strawberry Studios"
  lieu: "Strawberry Studios"
  place_id: PLACE-STRAWBERRY-STUDIOS
  ville: "Stockport"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Disorder"
    - "Day of the Lords"
    - "Candidate"
    - "Insight"
    - "New Dawn Fades"
    - "She's Lost Control"
    - "Shadowplay"
    - "Wilderness"
    - "Interzone"
    - "I Remember Nothing"
    - "Auto-Suggestion"
    - "From Safety to Where?"
    - "Exercise One"
    - "The Only Mistake"
    - "Walked in Line"
    - "The Kill"
  premiere_sortie_officielle:
    titre: "Unknown Pleasures"
    format: "album"
    label: "Factory Records (FACT 10)"
    annee: "1979"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S10
    - S41
    - S45
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSIONS-UNKNOWN-PLEASURES-STRAWBERRY
    places:
      - PLACE-STRAWBERRY-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Session principale d'avril 1979, avec prises album et titres destinés à des compilations ultérieures."

- id: JD-SESSION-19790604-001
  numero: 13
  label: "Piccadilly Radio Session"
  date: 1979-06-04
  type_session: radio
  studio: "Pennine Sound Studios"
  lieu: "Pennine Sound Studios"
  place_id: PLACE-PENNINE-STUDIOS-OLDHAM
  ville: "Oldham"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Stuart James"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "These Days"
    - "Candidate"
    - "The Only Mistake"
    - "Chance"
    - "Atrocity Exhibition"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSION-PICCADILLY-RADIO
    places:
      - PLACE-PENNINE-STUDIOS-OLDHAM
  notes: "Session pour Piccadilly Radio Manchester. « Chance » est le titre de travail d'Atmosphere."

- id: JD-SESSION-19790700-001
  numero: 14
  label: "Transmission sessions 1"
  date: "1979-07-00"
  type_session: studio
  studio: "Central Sound Studios"
  lieu: "Central Sound Studios"
  place_id: PLACE-CENTRAL-SOUND-STUDIOS
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Transmission"
    - "Novelty"
    - "Dead Souls"
    - "Something Must Break"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSIONS-TRANSMISSION
    places:
      - PLACE-CENTRAL-SOUND-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Première tentative de juillet 1979 pour Transmission, non retenue pour le single."

- id: JD-SESSION-19790719-001
  numero: 15
  label: "What's On — She's Lost Control"
  date: 1979-07-19
  type_session: television
  studio: "Granada TV"
  lieu: "Granada TV"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Granada TV"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "She's Lost Control"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
  urls:
    - "https://www.joydiv.org/jdtv.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-TELEVISION-WHATS-ON-SHES-LOST-CONTROL
  notes: "joydiv.org distingue la date d'archive Granada du 19 juillet 1979 et la page publique What's On du 20 juillet 1979. La performance est coupée par les crédits de fin."

- id: JD-SESSION-19790728-001
  numero: 16
  label: "Transmission sessions 2"
  date: 1979-07-28
  type_session: studio
  studio: "Strawberry Studios"
  lieu: "Strawberry Studios"
  place_id: PLACE-STRAWBERRY-STUDIOS
  ville: "Stockport"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Transmission"
    - "Novelty"
  premiere_sortie_officielle:
    titre: "Transmission"
    format: "single 7 pouces"
    label: "Factory Records (FAC 13)"
    annee: "1979"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSIONS-TRANSMISSION
    places:
      - PLACE-STRAWBERRY-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Plage de travail du 28 juillet au 4 août 1979 ; version finale du single Transmission."

- id: JD-SESSION-19790901-001
  numero: 17
  label: "Something Else — BBC2"
  date: 1979-09-01
  type_session: television
  studio: "BBC2 / Oxford Road"
  lieu: "BBC2 / Oxford Road"
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Tony Wilson", "Steve Harley"]
  producteur: "BBC2"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "She's Lost Control"
    - "Transmission"
  premiere_sortie_officielle:
    titre: "Substance"
    format: "video / compilation"
    label: "Factory"
    annee: "1988"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/jdtv.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-PERFORMANCE-BBC2-SOMETHING-ELSE
      - CHR-S76-1979-016
    people:
      - PERSON-tony-wilson
      - PERSON-stephen-morris
  notes: "Enregistré le 1er septembre 1979 et diffusé le 15 septembre 1979 selon joydiv.org et S76."

- id: JD-SESSION-19791000-001
  numero: 18
  label: "Sordide Sentimental session"
  date: "1979-10-00"
  type_session: studio
  studio: "Cargo Studios"
  lieu: "Cargo Studios"
  place_id: PLACE-CARGO-STUDIOS
  ville: "Rochdale"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Atmosphere"
    - "Dead Souls"
    - "Ice Age"
  premiere_sortie_officielle:
    titre: "Licht und Blindheit"
    format: "single 7 pouces"
    label: "Sordide Sentimental (SS33002)"
    annee: "1980"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSIONS-LICHT-UND-BLINDHEIT
    places:
      - PLACE-CARGO-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Plage octobre-novembre 1979 pour Atmosphere / Dead Souls, associée au single Sordide Sentimental."

- id: JD-SESSION-19791100-001
  numero: 19
  label: "Répétition T.J. Davidson's — From Night to Day / A Means to an End"
  date: "1979-11-00"
  type_session: rehearsal
  studio: "T.J. Davidson's Rehearsal Room"
  lieu: "T.J. Davidson's Rehearsal Room"
  place_id: PLACE-TJ-DAVIDSONS
  ville: "Manchester"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Untitled / Instrumental jam"
    - "From Night to Day"
    - "A Means to an End"
  premiere_sortie_officielle: {}
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S76
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: probable
  relations:
    places:
      - PLACE-TJ-DAVIDSONS
  notes: "Répétition datée tentativement de novembre/décembre 1979, utile pour documenter l'émergence de A Means to an End."

- id: JD-SESSION-19791126-001
  numero: 20
  label: "John Peel Session 2"
  date: 1979-11-26
  type_session: radio
  studio: "BBC Studios Maida Vale"
  lieu: "BBC Studios Maida Vale"
  place_id: PLACE-MAIDA-VALE-STUDIOS
  ville: "London"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Tony Wilson"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "The Sound of Music"
    - "Twenty Four Hours"
    - "Colony"
    - "Love Will Tear Us Apart"
  premiere_sortie_officielle:
    titre: "The Peel Sessions"
    format: "EP 12 pouces"
    label: "Strange Fruit Records"
    annee: "1987"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-DEUXIEME-PEEL-SESSION
    places:
      - PLACE-MAIDA-VALE-STUDIOS
    people:
      - PERSON-john-peel
  notes: "Deuxième Peel Session, diffusée le 10 décembre 1979. Tony Wilson est le producteur BBC, homonyme du Tony Wilson Factory."

- id: JD-SESSION-19800108-001
  numero: 21
  label: "Love Will Tear Us Apart session 1"
  date: 1980-01-08
  type_session: studio
  studio: "Pennine Sound Studios"
  lieu: "Pennine Sound Studios"
  place_id: PLACE-PENNINE-STUDIOS-OLDHAM
  ville: "Oldham"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "These Days"
    - "The Sound of Music"
    - "Love Will Tear Us Apart"
  premiere_sortie_officielle:
    titre: "Love Will Tear Us Apart"
    format: "single"
    label: "Factory Records (FAC 23)"
    annee: "1980"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-ENREGISTREMENT-LOVE-WILL-TEAR-US-APART
    places:
      - PLACE-PENNINE-STUDIOS-OLDHAM
    people:
      - PERSON-martin-hannett
  notes: "Version rapide de Love Will Tear Us Apart, non retenue comme face A."

- id: JD-SESSION-19800300-001
  numero: 22
  label: "Love Will Tear Us Apart session 2"
  date: "1980-03-00"
  type_session: studio
  studio: "Strawberry Studios"
  lieu: "Strawberry Studios"
  place_id: PLACE-STRAWBERRY-STUDIOS
  ville: "Stockport"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Love Will Tear Us Apart"
    - "She's Lost Control"
  premiere_sortie_officielle:
    titre: "Love Will Tear Us Apart"
    format: "single"
    label: "Factory Records (FAC 23)"
    annee: "1980"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S41
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-ENREGISTREMENT-LOVE-WILL-TEAR-US-APART
    places:
      - PLACE-STRAWBERRY-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Version définitive du single, sortie posthume en juin 1980."

- id: JD-SESSION-19800318-001
  numero: 23
  label: "Closer sessions"
  date: 1980-03-18
  type_session: studio
  studio: "Britannia Row Studios"
  lieu: "Britannia Row Studios"
  place_id: PLACE-BRITANNIA-ROW-STUDIOS
  ville: "Islington London"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett", "Jon Caffery"]
  producteur: "Martin Hannett"
  ingenieur_son: "Jon Caffery"
  ere: "Joy Division"
  titres:
    - "Atrocity Exhibition"
    - "Isolation"
    - "Passover"
    - "Colony"
    - "A Means to an End"
    - "Heart and Soul"
    - "Twenty Four Hours"
    - "The Eternal"
    - "Decades"
    - "Komakino"
    - "Incubation"
    - "As You Said"
    - "Love Will Tear Us Apart"
  premiere_sortie_officielle:
    titre: "Closer"
    format: "album"
    label: "Factory Records (FACT 25)"
    annee: "1980"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S10
    - S41
    - S45
    - S75
    - S76
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    chronology:
      - EVENT-SESSIONS-CLOSER-BRITANNIA-ROW
    places:
      - PLACE-BRITANNIA-ROW-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Plage du 18 au 30 mars 1980. Session centrale de Closer, avec moyens londoniens accrus et ingénierie de Jon Caffery."

- id: JD-SESSION-19800000-001
  numero: 24
  label: "Rehearsal room session / Graveyard Studio"
  date: "1980-00-00"
  type_session: rehearsal
  studio: "Graveyard Studio / rehearsal room"
  lieu: "Graveyard Studio / rehearsal room"
  place_id: PLACE-GRAVEYARD-STUDIO
  ville: "Manchester / Prestwich"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "Ceremony"
    - "In a Lonely Place"
  premiere_sortie_officielle:
    titre: "Heart And Soul"
    format: "coffret"
    label: "London Records"
    annee: "1997"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S10
    - S88
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: conteste
  relations:
    places:
      - PLACE-GRAVEYARD-STUDIO
  notes: "joydiv.org conserve l'entrée pour complétude mais signale que l'attribution Graveyard / rehearsal room est discutée et que les prises peuvent provenir de répétitions distinctes."

- id: JD-SESSION-19800514-001
  numero: 25
  label: "In a Lonely Place rehearsal takes"
  date: 1980-05-14
  type_session: rehearsal
  studio: "Pinky's Rehearsal Room / attribution à confirmer"
  lieu: "Pinky's Rehearsal Room / attribution à confirmer"
  ville: "Salford"
  participants: ["Ian Curtis", "Bernard Sumner", "Peter Hook", "Stephen Morris"]
  producteur: "Inconnu"
  ingenieur_son: "Inconnu"
  ere: "Joy Division"
  titres:
    - "In a Lonely Place"
  premiere_sortie_officielle:
    titre: "Ceremony / In A Lonely Place"
    format: "Record Store Day 12 pouces"
    label: "Rhino / Factory"
    annee: "2011"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
    - S88
  urls:
    - "https://www.joydiv.org/rehearsals.htm"
  statut_documentaire: probable
  relations: {}
  notes: "joydiv.org donne le 14 mai 1980 comme hypothèse la plus probable pour plusieurs prises de In a Lonely Place. Le lieu reste à confirmer ; aucune relation place n'est créée."

- id: JD-SESSION-19810000-001
  numero: 26
  label: "Still session"
  date: "1981-00-00"
  type_session: studio
  studio: "Britannia Row Studios"
  lieu: "Britannia Row Studios"
  place_id: PLACE-BRITANNIA-ROW-STUDIOS
  ville: "Islington London"
  participants: ["Bernard Sumner", "Peter Hook", "Stephen Morris", "Martin Hannett"]
  producteur: "Martin Hannett"
  ingenieur_son: "Inconnu"
  ere: "Post-Joy Division"
  titres:
    - "The Only Mistake"
    - "Walked in Line"
    - "The Kill"
  premiere_sortie_officielle:
    titre: "Still"
    format: "double album"
    label: "Factory Records (FACT 40)"
    annee: "1981"
  source: joydiv.org
  sources:
    - REGISTRY-SESSIONS
  urls:
    - "https://www.joydiv.org/sessions.htm"
  statut_documentaire: etabli
  relations:
    places:
      - PLACE-BRITANNIA-ROW-STUDIOS
    people:
      - PERSON-martin-hannett
  notes: "Session posthume de travail sur bandes pour Still. Elle est conservée car joydiv.org l'intègre au corpus des sessions."
```
