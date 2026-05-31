# Registre chronologique — identités canoniques d'événements (EVENT-)

> Brique d'identité (étape 6). Chaque entrée ci-dessous est un **jalon**
> canonique `EVENT-<SLUG>` : slug sémantique, source-agnostique, **sans date
> dans l'ID** (la date est un champ). Les identifiants legacy `CHR-…` qui
> désignent le même jalon portent `same_as: EVENT-…` dans leur fichier source
> (réconciliation additive, sans renommage — cf. cross_registres.md §1).
> `membres_reconcilies` liste ces legacy à titre de traçabilité.

---

## EVENT-NAISSANCE-IAN-CURTIS — Naissance de Ian Curtis

```yaml
id: EVENT-NAISSANCE-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
date: "1956-07-15"
date_precision: jour
event: >
  Naissance de Ian Curtis.
sources:
  - MASTER
  - S76
membres_reconcilies:
  - CHR-1956-001
  - CHR-S76-1956-001
```

---

## EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER — Premier concert des Sex Pistols au Lesser Free Trade Hall

```yaml
id: EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER
type_unite: chronology_event
categorie: jalon
date: "1976-06-04"
date_precision: jour
event: >
  Premier concert des Sex Pistols au Lesser Free Trade Hall.
sources:
  - MASTER
  - S10
  - S41
membres_reconcilies:
  - CHR-1976-001
  - CHR-S10-1976-001
  - CHR-S41-TL2-1976-06-04-LFTH
  - CHR-S41-1976-06-04-LESSER-FREE-TRADE-HALL
```

---

## EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-SECOND — Second concert des Sex Pistols au Lesser Free Trade Hall

```yaml
id: EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-SECOND
type_unite: chronology_event
categorie: jalon
date: "1976-07-20"
date_precision: jour
event: >
  Second concert des Sex Pistols au Lesser Free Trade Hall.
sources:
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1976-07-20-SECOND-PISTOLS-LFTH
  - CHR-S45-1976-07-20-SEX-PISTOLS
  - CHR-S75-1976-002
  - CHR-S76-1976-002
```

---

## EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS — Premier concert de Warsaw à l'Electric Circus

```yaml
id: EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS
type_unite: chronology_event
categorie: jalon
date: "1977-05-29"
date_precision: jour
event: >
  Premier concert de Warsaw à l'Electric Circus.
sources:
  - S10
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S10-1977-001
  - CHR-S41-TL2-1977-05-29-FIRST-WARSAW-GIG-REVIEW
  - CHR-S41-1977-05-29-WARSAW-FIRST-GIG-ELECTRIC-CIRCUS
  - CHR-S45-1977-05-29-WARSAW-ELECTRIC-CIRCUS
  - CHR-S76-1977-003
```

---

## EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS — Premier concert sous le nom Joy Division (Pips)

```yaml
id: EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS
type_unite: chronology_event
categorie: jalon
date: "1978-01-25"
date_precision: jour
event: >
  Premier concert sous le nom Joy Division (Pips).
sources:
  - S10
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S10-1978-001
  - CHR-S41-1978-01-PIPS-FIRST-JOY-DIVISION-GIG
  - CHR-S41-TL3-1978-01-25-PIPS-JOY-DIVISION
  - CHR-S45-1978-01-25-PIPS-FIRST-JD
  - CHR-S76-1978-001
```

---

## EVENT-ARRIVEE-STEPHEN-MORRIS — Arrivée de Stephen Morris (batteur)

```yaml
id: EVENT-ARRIVEE-STEPHEN-MORRIS
type_unite: chronology_event
categorie: jalon
date: "1977-08"
date_precision: mois
event: >
  Arrivée de Stephen Morris (batteur).
sources:
  - S41
  - S45
membres_reconcilies:
  - CHR-S41-1977-08-STEVE-MORRIS-JOINS
  - CHR-S45-1977-STEPHEN-MORRIS-RECRUTEMENT
prudence_methodologique: >
  S41 date l'arrivée à « 1977-08 » (mois), retenu comme date la plus précise ; S45 ne donne que « 1977 » (année). CHR-S35-P05-1977-ETE-001 (Morris voit l'annonce en vitrine de Jones's) est un candidat-membre à arbitrer.
```

---

## EVENT-SORTIE-A-FACTORY-SAMPLE — Sortie de A Factory Sample (FAC 2)

```yaml
id: EVENT-SORTIE-A-FACTORY-SAMPLE
type_unite: chronology_event
categorie: jalon
date: "1979-01"
date_precision: mois
event: >
  Sortie de A Factory Sample (FAC 2).
sources:
  - MASTER
  - S41
membres_reconcilies:
  - CHR-1979-001
  - CHR-S41-1979-01-A-FACTORY-SAMPLE-RELEASE
```

---

## EVENT-SORTIE-UNKNOWN-PLEASURES — Sortie de l'album Unknown Pleasures (FACT 10)

```yaml
id: EVENT-SORTIE-UNKNOWN-PLEASURES
type_unite: chronology_event
categorie: jalon
date: "1979-06-14"
date_precision: jour
event: >
  Sortie de l'album Unknown Pleasures (FACT 10).
sources:
  - MASTER
  - S41
  - S75
membres_reconcilies:
  - CHR-1979-002
  - CHR-S41-1979-06-UP-RELEASE-CRITICAL-ACCLAIM
  - CHR-S41-1979-06-14-UP-FACT10-RELEASE
  - CHR-S75-1979-006
prudence_methodologique: >
  S41 porte deux entrées de sortie (1979-06 « critical acclaim » et 1979-06-14 « FACT 10 release ») : duplication intra-source réconciliée. Lecture critique de S34 conservée distincte (reception_posthume).
```

---

## EVENT-DERNIER-CONCERT-BIRMINGHAM — Dernier concert de Joy Division (Birmingham University)

```yaml
id: EVENT-DERNIER-CONCERT-BIRMINGHAM
type_unite: chronology_event
categorie: jalon
date: "1980-05-02"
date_precision: jour
event: >
  Dernier concert de Joy Division (Birmingham University).
sources:
  - MASTER
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-1980-002
  - CHR-S41-1980-05-02-BIRMINGHAM-HIGH-HALL-LAST-GIG
  - CHR-S45-1980-05-02-BIRMINGHAM-FINAL-GIG
  - CHR-S75-1980-008
  - CHR-S76-1980-027
```

---

## EVENT-MORT-IAN-CURTIS — Mort de Ian Curtis

```yaml
id: EVENT-MORT-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
date: "1980-05-18"
date_precision: jour
event: >
  Mort de Ian Curtis.
sources:
  - MASTER
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-1980-003
  - CHR-S41-1980-05-18-CURTIS-SUICIDE
  - CHR-S75-1980-009
  - CHR-S76-1980-031
prudence_methodologique: >
  Les entrées adjacentes du 16-18 mai (derniers jours, dernier trajet, notification à Hook par la police, retour d'Annik Honoré) sont conservées comme jalons-facettes distincts, non fusionnés. CHR-S76-1980-031 (découverte du corps) est traité comme la consignation S76 du décès.
```

---

## EVENT-SORTIE-CLOSER — Sortie posthume de l'album Closer

```yaml
id: EVENT-SORTIE-CLOSER
type_unite: chronology_event
categorie: jalon
date: "1980-07-18"
date_precision: jour
event: >
  Sortie posthume de l'album Closer.
sources:
  - MASTER
  - S41
membres_reconcilies:
  - CHR-1980-004
  - CHR-S41-1980-CLOSER-RELEASE-POSTHUMOUS
```

---
