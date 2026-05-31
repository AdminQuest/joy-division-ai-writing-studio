# S10 — Compléments au registre chronologique — Sumner, Salford, Warsaw, Factory

```yaml
id: CHRONO-S10-SUMNER-SALFORD-FORMATION-SOUND-V2
source_id: S10
source_label: "S10 — Sumner, Chapter and Verse, 2014/2015"
type_unite: registre_chronologie
statut: integration_directe
```

```yaml
events:
  - id: CHR-S10-1956-001
    same_as: EVENT-NAISSANCE-BERNARD-SUMNER
    date_precision: jour
    categorie: jalon
    date: 1956-01-04
    precision_date: jour
    event: "Naissance de Bernard Sumner à Crumpsall, Manchester, avant son enfance à Lower Broughton, Salford."
    type: naissance
    location: Crumpsall
    people:
      - Bernard Sumner
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A001

  - id: CHR-S10-1960S-001
    date_precision: intervalle
    date_debut: 1960
    date_fin: 1969
    categorie: jalon
    date: "années 1960"
    precision_date: decade
    event: "Bernard Sumner grandit à Alfred Street, Lower Broughton, dans une communauté ouvrière proche de sites industriels."
    type: contexte_social
    location: Alfred Street
    people:
      - Bernard Sumner
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A001
      - S10-A002

  - id: CHR-S10-1960S-002
    date_precision: intervalle
    date_debut: 1960
    date_fin: 1969
    categorie: jalon
    date: "années 1960"
    precision_date: decade
    event: "La famille de Sumner quitte Alfred Street pour un flat à Greengate ; Sumner découvre le confort domestique mais aussi la perte de sociabilité de rue."
    type: relogement
    location: Greengate
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A003

  - id: CHR-S10-1970S-001
    date_precision: circa
    categorie: jalon
    date: "début des années 1970"
    precision_date: periode
    event: "Clearance d’Alfred Street et dispersion de la communauté ouvrière de Lower Broughton."
    type: slum_clearance
    location: Alfred Street
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A004

  - id: CHR-S10-1970S-002
    same_as: EVENT-RENCONTRE-SUMNER-HOOK-SALFORD-GRAMMAR
    date_precision: circa
    categorie: jalon
    date: "début des années 1970"
    precision_date: periode
    event: "Bernard Sumner et Peter Hook se rencontrent à Salford Grammar School."
    type: rencontre
    location: Salford Grammar School
    people:
      - Bernard Sumner
      - Peter Hook
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A007

  - id: CHR-S10-1970-001
    date_precision: annee
    categorie: contexte
    date: 1970
    precision_date: annee
    event: "La mort de Jimi Hendrix pousse Sumner à réécouter son œuvre jusqu’au déclic musical."
    type: influence_musicale
    people:
      - Bernard Sumner
      - Jimi Hendrix
    sources:
      - S10
    certainty: medium
    related_atoms:
      - S10-A008

  - id: CHR-S10-1974-001
    date_precision: annee
    categorie: contexte
    date: 1974
    precision_date: annee
    event: "Sumner assiste à un concert de Lou Reed au Free Trade Hall."
    type: concert
    location: Free Trade Hall
    people:
      - Bernard Sumner
      - Lou Reed
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A010

  - id: CHR-S10-1976-001
    date_precision: jour
    same_as: EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER
    categorie: jalon
    date: 1976-06-04
    precision_date: jour
    event: "Bernard Sumner, Peter Hook, Terry Mason et d’autres assistent au concert des Sex Pistols au Lesser Free Trade Hall."
    type: concert_fondateur
    location: Lesser Free Trade Hall
    people:
      - Bernard Sumner
      - Peter Hook
      - Terry Mason
    organizations:
      - Sex Pistols
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A010
      - S10-A011

  - id: CHR-S10-1976-002
    date_precision: saison
    categorie: jalon
    date: "été 1976"
    precision_date: saison
    event: "Sumner et Hook commencent à apprendre guitare et basse et à composer ensemble à Alfred Street, avec un gramophone détourné en ampli."
    type: apprentissage_musical
    location: Alfred Street
    people:
      - Bernard Sumner
      - Peter Hook
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A012

  - id: CHR-S10-1976-003
    same_as: EVENT-RECRUTEMENT-IAN-CURTIS-CHANTEUR
    date_precision: circa
    categorie: jalon
    date: "fin 1976"
    precision_date: approx
    event: "Annonce déposée chez Virgin Records sur Lever Street pour recruter un chanteur ; Ian Curtis appelle et obtient le poste."
    type: recrutement
    location: Virgin Records Lever Street
    people:
      - Bernard Sumner
      - Ian Curtis
      - Peter Hook
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A013

  - id: CHR-S10-1977-001
    date_precision: jour
    same_as: EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS
    categorie: jalon
    date: 1977-05-29
    precision_date: jour
    event: "Premier concert de Warsaw / Stiff Kittens à l’Electric Circus, Manchester, en ouverture des Buzzcocks."
    type: concert
    location: Electric Circus
    organizations:
      - Buzzcocks
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A015

  - id: CHR-S10-1978-001
    date_precision: jour
    same_as: EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS
    categorie: jalon
    date: 1978-01-25
    precision_date: jour
    event: "Premier concert sous le nom Joy Division à Pips, Manchester."
    type: concert
    location: Pips
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A019

  - id: CHR-S10-1978-002
    date_precision: mois
    categorie: jalon
    date: "avril 1978"
    precision_date: mois
    event: "Concert à Rafters organisé par Stiff / Chiswick ; Rob Gretton voit Joy Division et propose de devenir leur manager."
    type: professionnalisation
    location: Rafters
    people:
      - Rob Gretton
      - Bernard Sumner
      - Ian Curtis
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A016

  - id: CHR-S10-1978-003
    same_as: EVENT-SESSIONS-RCA-ARROW-STUDIOS
    date_precision: annee
    categorie: jalon
    date: 1978
    precision_date: annee
    event: "Sessions RCA / Greendow Commercials, album avorté, overdubs imposés et récupération ultérieure des bandes par Gretton."
    type: session_studio
    location: Greendow Commercials studio
    people:
      - Richard Searling
      - Rob Gretton
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A018

  - id: CHR-S10-1978-004
    same_as: EVENT-ENREGISTREMENT-AN-IDEAL-FOR-LIVING
    date_precision: annee
    categorie: jalon
    date: 1978
    precision_date: annee
    event: "Enregistrement d’An Ideal for Living à Pennine Studios, Oldham, et choix de l’imagerie Hitler Youth / Bernard Albrecht."
    type: enregistrement_publication
    location: Pennine Studios Oldham
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A019

  - id: CHR-S10-1978-005
    same_as: EVENT-DEBUT-TELEVISION-GRANADA-SHADOWPLAY
    date_precision: jour
    categorie: jalon
    date: 1978-09-20
    precision_date: jour
    event: "Joy Division fait ses débuts télévisés sur Granada Reports avec Shadowplay."
    type: television
    location: Granada Television
    people:
      - Tony Wilson
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A017

  - id: CHR-S10-1978-006
    same_as: EVENT-SORTIE-A-FACTORY-SAMPLE
    date_precision: saison
    categorie: jalon
    date: "Noël 1978"
    precision_date: periode
    event: "Joy Division apparaît sur A Factory Sample avec Digital et Glass."
    type: publication
    organizations:
      - Factory Records
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A018

  - id: CHR-S10-1978-007
    a_scinder_etape_10: true
    date_precision: jour
    categorie: jalon
    date: 1978-12-27
    precision_date: jour
    event: "Concert au Hope and Anchor, Islington ; au retour, Curtis subit une crise épileptique et est conduit à l’hôpital de Luton."
    type: crise_biographique
    location: Hope and Anchor / Luton
    people:
      - Ian Curtis
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A024

  - id: CHR-S10-1979-001
    date_precision: mois
    categorie: jalon
    date: "janvier 1979"
    precision_date: mois
    event: "Diagnostic d’épilepsie de Curtis confirmé autour de la première Peel Session selon le cadrage de Sumner."
    type: diagnostic
    people:
      - Ian Curtis
    sources:
      - S10
    certainty: medium
    related_atoms:
      - S10-A024

  - id: CHR-S10-1979-002
    same_as: EVENT-SESSIONS-UNKNOWN-PLEASURES-STRAWBERRY
    date_precision: mois
    categorie: jalon
    date: "avril 1979"
    precision_date: mois
    event: "Joy Division entre à Strawberry Studios pour enregistrer Unknown Pleasures avec Martin Hannett."
    type: session_studio
    location: Strawberry Studios
    people:
      - Martin Hannett
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A020
      - S10-A021

  - id: CHR-S10-1980-001
    date_precision: annee
    categorie: jalon
    date: 1980
    precision_date: annee
    event: "Autour de Closer, Curtis exprime à Sumner le sentiment d’être entraîné dans un whirlpool et annonce brièvement à Gretton son désir de quitter le groupe pour Bournemouth."
    type: crise_finale
    people:
      - Ian Curtis
      - Rob Gretton
      - Bernard Sumner
    sources:
      - S10
    certainty: strong
    related_atoms:
      - S10-A025
```
