# Registre des concerts — identités canoniques CONCERT- (étape 7b-1)

> Colonne vertébrale du registre des concerts, fondée sur la source joydiv.org
> (`00_canonical_concerts.md`, Tony Nuttall). Identité **source-agnostique**
> `CONCERT-AAAAMMJJ-LIEU` (date dans le slug + `date`/`date_precision` en champ ;
> `lieu` → réf `PLACE-` de l'étape 7a). Les entrées legacy `JD-CONCERT-` restent
> en source et se réconcilient par `same_as` (porté côté legacy) ; chaque
> canonique porte `membres_reconcilies`. Additif, gel EVENT- intact.
>
> Périmètre 7b-1 : concerts joydiv **confirmés + annulés** dont le lieu résout
> vers un `PLACE-` existant. **Exclus** : 3 passages TV (hors périmètre).
> **Flaggés, non créés** : 2 douteux ; concerts dont le venue n'a pas encore de
> `PLACE-` (lot de création de lieux différé). Les 88 `concert_a_migrer`, les 4
> bundles et le renommage `a_scinder` relèvent de 7b-2.


## 1977

```yaml
- id: CONCERT-19770529-ELECTRIC-CIRCUS
  type_unite: concert
  label: "Warsaw — Electric Circus, Manchester (1977-05-29)"
  date: "1977-05-29"
  date_precision: jour
  lieu: PLACE-ELECTRIC-CIRCUS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770529-001
- id: CONCERT-19770531-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Warsaw — Rafters, Manchester (1977-05-31)"
  date: "1977-05-31"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770531-001
- id: CONCERT-19770603-THE-SQUAT-MANCHESTER
  type_unite: concert
  label: "Warsaw — The Squat, Manchester (1977-06-03)"
  date: "1977-06-03"
  date_precision: jour
  lieu: PLACE-THE-SQUAT-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770603-001
- id: CONCERT-19770616-THE-SQUAT-MANCHESTER
  type_unite: concert
  label: "Warsaw — The Squat, Manchester (1977-06-16)"
  date: "1977-06-16"
  date_precision: jour
  lieu: PLACE-THE-SQUAT-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770616-001
- id: CONCERT-19770625-THE-SQUAT-MANCHESTER
  type_unite: concert
  label: "Warsaw — The Squat, Manchester (1977-06-25)"
  date: "1977-06-25"
  date_precision: jour
  lieu: PLACE-THE-SQUAT-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770625-001
- id: CONCERT-19770630-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Warsaw — Rafters, Manchester (1977-06-30)"
  date: "1977-06-30"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770630-001
- id: CONCERT-19770914-ROCK-GARDEN-MIDDLESBROUGH
  type_unite: concert
  label: "Warsaw — Rock Garden, Middlesbrough (1977-09-14)"
  date: "1977-09-14"
  date_precision: jour
  lieu: PLACE-ROCK-GARDEN-MIDDLESBROUGH
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770914-001
- id: CONCERT-19770924-ELECTRIC-CIRCUS
  type_unite: concert
  label: "Warsaw — Electric Circus, Manchester (1977-09-24)"
  date: "1977-09-24"
  date_precision: jour
  lieu: PLACE-ELECTRIC-CIRCUS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19770924-001
- id: CONCERT-19771002-ELECTRIC-CIRCUS
  type_unite: concert
  label: "Warsaw — Electric Circus, Manchester (1977-10-02)"
  date: "1977-10-02"
  date_precision: jour
  lieu: PLACE-ELECTRIC-CIRCUS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771002-001
- id: CONCERT-19771007-SALFORD-TECHNICAL-COLLEGE
  type_unite: concert
  label: "Warsaw — Salford College of Technology, Salford (1977-10-07)"
  date: "1977-10-07"
  date_precision: jour
  lieu: PLACE-SALFORD-TECHNICAL-COLLEGE
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771007-001
- id: CONCERT-19771013-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Warsaw — Rafters, Manchester (1977-10-13)"
  date: "1977-10-13"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771013-001
- id: CONCERT-19771019-PIPERS-CYPRUS-TAVERN
  type_unite: concert
  label: "Warsaw — Pipers, Manchester (1977-10-19)"
  date: "1977-10-19"
  date_precision: jour
  lieu: PLACE-PIPERS-CYPRUS-TAVERN
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771019-001
- id: CONCERT-19771124-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Warsaw — Rafters, Manchester (1977-11-24)"
  date: "1977-11-24"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771124-001
- id: CONCERT-19771200-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Warsaw — Rafters, Manchester (1977-12)"
  date: "1977-12"
  date_precision: mois
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771200-001
- id: CONCERT-19771231-SWINGING-APPLE-LIVERPOOL
  type_unite: concert
  label: "Warsaw — The Swingin' Apple, Liverpool (1977-12-31)"
  date: "1977-12-31"
  date_precision: jour
  lieu: PLACE-SWINGING-APPLE-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19771231-001
```

## 1978

```yaml
- id: CONCERT-19780125-PIPS
  type_unite: concert
  label: "Joy Division — Pips Disco, Manchester (1978-01-25)"
  date: "1978-01-25"
  date_precision: jour
  lieu: PLACE-PIPS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780125-001
- id: CONCERT-19780328-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Joy Division — Rafters, Manchester (1978-03-28)"
  date: "1978-03-28"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780328-001
- id: CONCERT-19780414-RAFTERS-MANCHESTER
  type_unite: concert
  label: "Joy Division — Rafters, Manchester (1978-04-14)"
  date: "1978-04-14"
  date_precision: jour
  lieu: PLACE-RAFTERS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780414-001
- id: CONCERT-19780520-STONEGROUND-MAYFLOWER
  type_unite: concert
  label: "Joy Division — The Mayflower Club, Manchester (1978-05-20)"
  date: "1978-05-20"
  date_precision: jour
  lieu: PLACE-STONEGROUND-MAYFLOWER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780520-001
- id: CONCERT-19780600-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1978-06)"
  date: "1978-06"
  date_precision: mois
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780600-001
- id: CONCERT-19780609-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I (Russell Club), Manchester (1978-06-09)"
  date: "1978-06-09"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780609-001
- id: CONCERT-19780713-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1978-07-13)"
  date: "1978-07-13"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780713-001
- id: CONCERT-19780715-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1978-07-15)"
  date: "1978-07-15"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780715-001
- id: CONCERT-19780727-ROOTS-CLUB-LEEDS
  type_unite: concert
  label: "Joy Division — Roots Club, Leeds (1978-07-27)"
  date: "1978-07-27"
  date_precision: jour
  lieu: PLACE-ROOTS-CLUB-LEEDS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780727-001
- id: CONCERT-19780728-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1978-07-28)"
  date: "1978-07-28"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780728-001
- id: CONCERT-19780820-ROYAL-STANDARD-BRADFORD
  type_unite: concert
  label: "Joy Division — Royal Standard, Bradford (1978-08-20)"
  date: "1978-08-20"
  date_precision: jour
  lieu: PLACE-ROYAL-STANDARD-BRADFORD
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780820-001
- id: CONCERT-19780829-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1978-08-29)"
  date: "1978-08-29"
  date_precision: jour
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780829-001
- id: CONCERT-19780904-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1978-09-04)"
  date: "1978-09-04"
  date_precision: jour
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780904-001
- id: CONCERT-19780909-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1978-09-09)"
  date: "1978-09-09"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780909-001
- id: CONCERT-19780910-ROYAL-STANDARD-BRADFORD
  type_unite: concert
  label: "Joy Division — Royal Standard, Bradford (1978-09-10)"
  date: "1978-09-10"
  date_precision: jour
  lieu: PLACE-ROYAL-STANDARD-BRADFORD
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780910-001
- id: CONCERT-19780922-COACH-HOUSE-HUDDERSFIELD
  type_unite: concert
  label: "Joy Division — Coach House, Huddersfield (1978-09-22)"
  date: "1978-09-22"
  date_precision: jour
  lieu: PLACE-COACH-HOUSE-HUDDERSFIELD
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780922-001
- id: CONCERT-19780926-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1978-09-26)"
  date: "1978-09-26"
  date_precision: jour
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19780926-001
- id: CONCERT-19781012-KELLYS-MANCHESTER
  type_unite: concert
  label: "Joy Division — Kelly's, Manchester (1978-10-12)"
  date: "1978-10-12"
  date_precision: jour
  lieu: PLACE-KELLYS-MANCHESTER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781012-001
- id: CONCERT-19781020-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1978-10-20)"
  date: "1978-10-20"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781020-001
- id: CONCERT-19781024-FAN-CLUB-LEEDS
  type_unite: concert
  label: "Joy Division — The Fan Club, Leeds (1978-10-24)"
  date: "1978-10-24"
  date_precision: jour
  lieu: PLACE-FAN-CLUB-LEEDS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781024-001
- id: CONCERT-19781026-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1978-10-26)"
  date: "1978-10-26"
  date_precision: jour
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781026-001
- id: CONCERT-19781027-MANCHESTER-APOLLO
  type_unite: concert
  label: "Joy Division — Apollo Theatre, Manchester (1978-10-27)"
  date: "1978-10-27"
  date_precision: jour
  lieu: PLACE-MANCHESTER-APOLLO
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781027-001
- id: CONCERT-19781104-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1978-11-04)"
  date: "1978-11-04"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781104-001
- id: CONCERT-19781112-MANCHESTER-APOLLO
  type_unite: concert
  label: "Joy Division — Apollo Theatre, Manchester (1978-11-12)"
  date: "1978-11-12"
  date_precision: jour
  lieu: PLACE-MANCHESTER-APOLLO
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781112-001
- id: CONCERT-19781115-BRUNEL-UNIVERSITY
  type_unite: concert
  label: "Joy Division — Brunel University, Uxbridge (1978-11-15)"
  date: "1978-11-15"
  date_precision: jour
  lieu: PLACE-BRUNEL-UNIVERSITY
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781115-001
- id: CONCERT-19781119-LOCARNO-BRISTOL
  type_unite: concert
  label: "[annulé] Joy Division — Locarno, Bristol (1978-11-19)"
  date: "1978-11-19"
  date_precision: jour
  lieu: PLACE-LOCARNO-BRISTOL
  statut: annulé
  membres_reconcilies:
    - JD-CONCERT-19781119-A01
- id: CONCERT-19781120-CHECK-INN-ALTRINCHAM
  type_unite: concert
  label: "Joy Division — Check Inn Club, Altrincham (1978-11-20)"
  date: "1978-11-20"
  date_precision: jour
  lieu: PLACE-CHECK-INN-ALTRINCHAM
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781120-001
- id: CONCERT-19781201-SALFORD-TECHNICAL-COLLEGE
  type_unite: concert
  label: "Joy Division — Salford College of Technology, Salford (1978-12-01)"
  date: "1978-12-01"
  date_precision: jour
  lieu: PLACE-SALFORD-TECHNICAL-COLLEGE
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781201-001
- id: CONCERT-19781227-HOPE-AND-ANCHOR-LONDON
  type_unite: concert
  label: "Joy Division — Hope and Anchor, London (1978-12-27)"
  date: "1978-12-27"
  date_precision: jour
  lieu: PLACE-HOPE-AND-ANCHOR-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19781227-001
    - CHR-S10-1978-007
    - CHR-S41-TL3-1978-12-27-HOPE-ANCHOR-REVIEW
    - CHR-S45-1978-12-27-HOPE-AND-ANCHOR-FIRST-FIT
    - CHR-S75-1978-008
    - CHR-S76-1978-019
```

## 1979

```yaml
- id: CONCERT-19790126-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-01-26)"
  date: "1979-01-26"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790126-001
- id: CONCERT-19790216-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1979-02-16)"
  date: "1979-02-16"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790216-001
- id: CONCERT-19790301-HOPE-AND-ANCHOR-LONDON
  type_unite: concert
  label: "Joy Division — Hope and Anchor, London (1979-03-01)"
  date: "1979-03-01"
  date_precision: jour
  lieu: PLACE-HOPE-AND-ANCHOR-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790301-001
- id: CONCERT-19790304-MARQUEE-LONDON
  type_unite: concert
  label: "Joy Division — Marquee, London (1979-03-04)"
  date: "1979-03-04"
  date_precision: jour
  lieu: PLACE-MARQUEE-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790304-001
    - CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE
- id: CONCERT-19790313-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1979-03-13)"
  date: "1979-03-13"
  date_precision: jour
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790313-001
- id: CONCERT-19790314-BOWDON-VALE-YOUTH-CLUB
  type_unite: concert
  label: "Joy Division — Bowdon Vale Youth Club, Altrincham (1979-03-14)"
  date: "1979-03-14"
  date_precision: jour
  lieu: PLACE-BOWDON-VALE-YOUTH-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790314-001
- id: CONCERT-19790330-WALTHAMSTOW-YOUTH-CLUB
  type_unite: concert
  label: "Joy Division — Youth Centre Walthamstow, London (1979-03-30)"
  date: "1979-03-30"
  date_precision: jour
  lieu: PLACE-WALTHAMSTOW-YOUTH-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790330-001
- id: CONCERT-19790503-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1979-05-03)"
  date: "1979-05-03"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790503-001
- id: CONCERT-19790511-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-05-11)"
  date: "1979-05-11"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790511-001
- id: CONCERT-19790517-ACKLAM-HALL-LONDON
  type_unite: concert
  label: "Joy Division — Acklam Hall, London (1979-05-17)"
  date: "1979-05-17"
  date_precision: jour
  lieu: PLACE-ACKLAM-HALL-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790517-001
- id: CONCERT-19790523-BOWDON-VALE-YOUTH-CLUB
  type_unite: concert
  label: "Joy Division — Bowdon Vale Youth Club, Altrincham (1979-05-23)"
  date: "1979-05-23"
  date_precision: jour
  lieu: PLACE-BOWDON-VALE-YOUTH-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790523-001
- id: CONCERT-19790600-BAND-ON-THE-WALL
  type_unite: concert
  label: "Joy Division — Band on the Wall, Manchester (1979-06)"
  date: "1979-06"
  date_precision: mois
  lieu: PLACE-BAND-ON-THE-WALL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790600-001
- id: CONCERT-19790607-FAN-CLUB-LEEDS
  type_unite: concert
  label: "Joy Division — The Fan Club, Leeds (1979-06-07)"
  date: "1979-06-07"
  date_precision: jour
  lieu: PLACE-FAN-CLUB-LEEDS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790607-001
- id: CONCERT-19790613-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-06-13)"
  date: "1979-06-13"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790613-001
- id: CONCERT-19790628-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-06-28)"
  date: "1979-06-28"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790628-001
- id: CONCERT-19790711-ROOTS-CLUB-LEEDS
  type_unite: concert
  label: "Joy Division — Roots Club, Leeds (1979-07-11)"
  date: "1979-07-11"
  date_precision: jour
  lieu: PLACE-ROOTS-CLUB-LEEDS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790711-001
- id: CONCERT-19790713-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-07-13)"
  date: "1979-07-13"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790713-001
- id: CONCERT-19790728-STONEGROUND-MAYFLOWER
  type_unite: concert
  label: "Joy Division — The Mayflower Club, Manchester (1979-07-28)"
  date: "1979-07-28"
  date_precision: jour
  lieu: PLACE-STONEGROUND-MAYFLOWER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790728-001
- id: CONCERT-19790802-YMCA-LONDON
  type_unite: concert
  label: "Joy Division — YMCA, London (1979-08-02)"
  date: "1979-08-02"
  date_precision: jour
  lieu: PLACE-YMCA-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790802-001
- id: CONCERT-19790811-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1979-08-11)"
  date: "1979-08-11"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790811-001
- id: CONCERT-19790813-NASHVILLE-ROOMS-LONDON
  type_unite: concert
  label: "Joy Division — Nashville Rooms, London (1979-08-13)"
  date: "1979-08-13"
  date_precision: jour
  lieu: PLACE-NASHVILLE-ROOMS-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790813-001
    - CHR-S41-1979-08-13-NASHVILLE-ANNIK
    - CHR-S41-1979-08-13-NASHVILLE-ANNIK-ATMOSPHERE
    - CHR-S76-1979-019
- id: CONCERT-19790822-WALTHAMSTOW-YOUTH-CLUB
  type_unite: concert
  label: "Joy Division — Youth Centre Walthamstow, London (1979-08-22)"
  date: "1979-08-22"
  date_precision: jour
  lieu: PLACE-WALTHAMSTOW-YOUTH-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790822-001
- id: CONCERT-19790831-ELECTRIC-BALLROOM-CAMDEN
  type_unite: concert
  label: "Joy Division — The Electric Ballroom, London (1979-08-31)"
  date: "1979-08-31"
  date_precision: jour
  lieu: PLACE-ELECTRIC-BALLROOM-CAMDEN
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790831-001
- id: CONCERT-19790908-QUEENS-HALL-LEEDS
  type_unite: concert
  label: "Joy Division — Futurama One Festival, Leeds (1979-09-08)"
  date: "1979-09-08"
  date_precision: jour
  lieu: PLACE-QUEENS-HALL-LEEDS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790908-001
- id: CONCERT-19790914-ROCK-GARDEN-MIDDLESBROUGH
  type_unite: concert
  label: "Joy Division — Rock Garden, Middlesbrough (1979-09-14)"
  date: "1979-09-14"
  date_precision: jour
  lieu: PLACE-ROCK-GARDEN-MIDDLESBROUGH
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790914-001
- id: CONCERT-19790922-NASHVILLE-ROOMS-LONDON
  type_unite: concert
  label: "Joy Division — Nashville Rooms, London (1979-09-22)"
  date: "1979-09-22"
  date_precision: jour
  lieu: PLACE-NASHVILLE-ROOMS-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790922-001
- id: CONCERT-19790928-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1979-09-28)"
  date: "1979-09-28"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790928-001
- id: CONCERT-19790929-STONEGROUND-MAYFLOWER
  type_unite: concert
  label: "Joy Division — The Mayflower, Manchester (1979-09-29)"
  date: "1979-09-29"
  date_precision: jour
  lieu: PLACE-STONEGROUND-MAYFLOWER
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19790929-001
- id: CONCERT-19791003-LEEDS-UNIVERSITY
  type_unite: concert
  label: "Joy Division — Leeds University, Leeds (1979-10-03)"
  date: "1979-10-03"
  date_precision: jour
  lieu: PLACE-LEEDS-UNIVERSITY
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791003-001
- id: CONCERT-19791005-MANCHESTER-APOLLO
  type_unite: concert
  label: "Joy Division — Apollo, Glasgow (1979-10-05)"
  date: "1979-10-05"
  date_precision: jour
  lieu: PLACE-MANCHESTER-APOLLO
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791005-001
- id: CONCERT-19791008-CAIRD-HALL-DUNDEE
  type_unite: concert
  label: "Joy Division — Caird Hall, Dundee (1979-10-08)"
  date: "1979-10-08"
  date_precision: jour
  lieu: PLACE-CAIRD-HALL-DUNDEE
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791008-001
- id: CONCERT-19791010-KELLYS-MANCHESTER
  type_unite: concert
  label: "[annulé] Joy Division — Kelly's, Portrush (1979-10-10)"
  date: "1979-10-10"
  date_precision: jour
  lieu: PLACE-KELLYS-MANCHESTER
  statut: annulé
  membres_reconcilies:
    - JD-CONCERT-19791010-A01
- id: CONCERT-19791016-PLAN-K-BRUSSELS
  type_unite: concert
  label: "Joy Division — Plan K, Brussels (1979-10-16)"
  date: "1979-10-16"
  date_precision: jour
  lieu: PLACE-PLAN-K-BRUSSELS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19791016-001
- id: CONCERT-19791026-ELECTRIC-BALLROOM-CAMDEN
  type_unite: concert
  label: "Joy Division — Electric Ballroom, London (1979-10-26)"
  date: "1979-10-26"
  date_precision: jour
  lieu: PLACE-ELECTRIC-BALLROOM-CAMDEN
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19791026-001
- id: CONCERT-19791027-MANCHESTER-APOLLO
  type_unite: concert
  label: "Joy Division — Apollo Theatre, Manchester (1979-10-27)"
  date: "1979-10-27"
  date_precision: jour
  lieu: PLACE-MANCHESTER-APOLLO
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791027-001
- id: CONCERT-19791028-MANCHESTER-APOLLO
  type_unite: concert
  label: "Joy Division — Apollo Theatre, Manchester (1979-10-28)"
  date: "1979-10-28"
  date_precision: jour
  lieu: PLACE-MANCHESTER-APOLLO
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791028-001
- id: CONCERT-19791102-WINTER-GARDENS-MALVERN
  type_unite: concert
  label: "Joy Division — Winter Gardens, Bournemouth (1979-11-02)"
  date: "1979-11-02"
  date_precision: jour
  lieu: PLACE-WINTER-GARDENS-MALVERN
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791102-001
- id: CONCERT-19791108-MARQUEE-LONDON
  type_unite: concert
  label: "[annulé] Joy Division — Marquee Club, London (1979-11-08)"
  date: "1979-11-08"
  date_precision: jour
  lieu: PLACE-MARQUEE-LONDON
  statut: annulé
  membres_reconcilies:
    - JD-CONCERT-19791108-A01
- id: CONCERT-19791109-RAINBOW-THEATRE-LONDON
  type_unite: concert
  label: "Joy Division — The Rainbow Theatre, London (1979-11-09)"
  date: "1979-11-09"
  date_precision: jour
  lieu: PLACE-RAINBOW-THEATRE-LONDON
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791109-001
- id: CONCERT-19791110-RAINBOW-THEATRE-LONDON
  type_unite: concert
  label: "Joy Division — The Rainbow Theatre, London (1979-11-10)"
  date: "1979-11-10"
  date_precision: jour
  lieu: PLACE-RAINBOW-THEATRE-LONDON
  statut: confirmé
  nom_tournee: "Buzzcocks tour"
  membres_reconcilies:
    - JD-CONCERT-19791110-001
- id: CONCERT-19791208-ERICS-LIVERPOOL
  type_unite: concert
  label: "Joy Division — Eric's, Liverpool (1979-12-08)"
  date: "1979-12-08"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19791208-001
- id: CONCERT-19791218-LES-BAINS-DOUCHES-PARIS
  type_unite: concert
  label: "Joy Division — Les Bains Douches, Paris (1979-12-18)"
  date: "1979-12-18"
  date_precision: jour
  lieu: PLACE-LES-BAINS-DOUCHES-PARIS
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19791218-001
- id: CONCERT-19791231-WAREHOUSE-PRESTON
  type_unite: concert
  label: "Joy Division — Warehouse, Manchester (1979-12-31)"
  date: "1979-12-31"
  date_precision: jour
  lieu: PLACE-WAREHOUSE-PRESTON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19791231-001
```

## 1980

```yaml
- id: CONCERT-19800111-PARADISO-AMSTERDAM
  type_unite: concert
  label: "Joy Division — Paradiso, Amsterdam (1980-01-11)"
  date: "1980-01-11"
  date_precision: jour
  lieu: PLACE-PARADISO-AMSTERDAM
  statut: confirmé
  nom_tournee: "European tour January 1980"
  membres_reconcilies:
    - JD-CONCERT-19800111-001
- id: CONCERT-19800115-BASEMENT-COLOGNE
  type_unite: concert
  label: "Joy Division — The Basement, Cologne (1980-01-15)"
  date: "1980-01-15"
  date_precision: jour
  lieu: PLACE-BASEMENT-COLOGNE
  statut: confirmé
  nom_tournee: "European tour January 1980"
  membres_reconcilies:
    - JD-CONCERT-19800115-001
- id: CONCERT-19800117-PLAN-K-BRUSSELS
  type_unite: concert
  label: "Joy Division — Plan K, Brussels (1980-01-17)"
  date: "1980-01-17"
  date_precision: jour
  lieu: PLACE-PLAN-K-BRUSSELS
  statut: confirmé
  nom_tournee: "European tour January 1980"
  membres_reconcilies:
    - JD-CONCERT-19800117-001
- id: CONCERT-19800118-EFFENAAR-EINDHOVEN
  type_unite: concert
  label: "Joy Division — Effenaar, Eindhoven (1980-01-18)"
  date: "1980-01-18"
  date_precision: jour
  lieu: PLACE-EFFENAAR-EINDHOVEN
  statut: confirmé
  nom_tournee: "European tour January 1980"
  membres_reconcilies:
    - JD-CONCERT-19800118-001
- id: CONCERT-19800207-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory II, Manchester (1980-02-07)"
  date: "1980-02-07"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800207-001
- id: CONCERT-19800220-DERBY-HALL-BURY
  type_unite: concert
  label: "Joy Division — Town Hall, High Wycombe (1980-02-20)"
  date: "1980-02-20"
  date_precision: jour
  lieu: PLACE-DERBY-HALL-BURY
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800220-001
- id: CONCERT-19800228-WAREHOUSE-PRESTON
  type_unite: concert
  label: "Joy Division — The Warehouse, Preston (1980-02-28)"
  date: "1980-02-28"
  date_precision: jour
  lieu: PLACE-WAREHOUSE-PRESTON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800228-001
- id: CONCERT-19800402-MOONLIGHT-CLUB-LONDON
  type_unite: concert
  label: "Joy Division — The Moonlight Club, London (1980-04-02)"
  date: "1980-04-02"
  date_precision: jour
  lieu: PLACE-MOONLIGHT-CLUB-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800402-001
- id: CONCERT-19800403-MOONLIGHT-CLUB-LONDON
  type_unite: concert
  label: "Joy Division — The Moonlight Club, London (1980-04-03)"
  date: "1980-04-03"
  date_precision: jour
  lieu: PLACE-MOONLIGHT-CLUB-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800403-001
- id: CONCERT-19800404-MOONLIGHT-CLUB-LONDON
  type_unite: concert
  label: "Joy Division — The Moonlight Club, London (1980-04-04)"
  date: "1980-04-04"
  date_precision: jour
  lieu: PLACE-MOONLIGHT-CLUB-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800404-002
- id: CONCERT-19800404-RAINBOW-THEATRE-LONDON
  type_unite: concert
  label: "Joy Division — Rainbow Theatre, London (1980-04-04)"
  date: "1980-04-04"
  date_precision: jour
  lieu: PLACE-RAINBOW-THEATRE-LONDON
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800404-001
    - CHR-S41-1980-04-04-RAINBOW-FIT-MOONLIGHT-INSISTENCE
    - CHR-S75-1980-005
- id: CONCERT-19800405-WINTER-GARDENS-MALVERN
  type_unite: concert
  label: "Joy Division — Winter Gardens, Malvern (1980-04-05)"
  date: "1980-04-05"
  date_precision: jour
  lieu: PLACE-WINTER-GARDENS-MALVERN
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800405-001
- id: CONCERT-19800408-DERBY-HALL-BURY
  type_unite: concert
  label: "Joy Division — Derby Hall, Bury (1980-04-08)"
  date: "1980-04-08"
  date_precision: jour
  lieu: PLACE-DERBY-HALL-BURY
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800408-001
- id: CONCERT-19800411-RUSSELL-CLUB
  type_unite: concert
  label: "Joy Division — The Factory I, Manchester (1980-04-11)"
  date: "1980-04-11"
  date_precision: jour
  lieu: PLACE-RUSSELL-CLUB
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800411-001
- id: CONCERT-19800419-AJANTA-THEATRE-DERBY
  type_unite: concert
  label: "Joy Division — Ajanta Theatre, Derby (1980-04-19)"
  date: "1980-04-19"
  date_precision: jour
  lieu: PLACE-AJANTA-THEATRE-DERBY
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800419-001
- id: CONCERT-19800426-ROCK-GARDEN-MIDDLESBROUGH
  type_unite: concert
  label: "Joy Division — Rock Garden, Middlesbrough (1980-04-26)"
  date: "1980-04-26"
  date_precision: jour
  lieu: PLACE-ROCK-GARDEN-MIDDLESBROUGH
  statut: confirmé
  membres_reconcilies:
    - JD-CONCERT-19800426-001
- id: CONCERT-19800503-ERICS-LIVERPOOL
  type_unite: concert
  label: "[annulé] Joy Division — Eric's, Liverpool (1980-05-03)"
  date: "1980-05-03"
  date_precision: jour
  lieu: PLACE-ERICS-LIVERPOOL
  statut: annulé
  membres_reconcilies:
    - JD-CONCERT-19800503-A01
```

