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
label: "Naissance de Ian Curtis"
date: "1956-07-15"
date_precision: jour
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
label: "Premier concert des Sex Pistols au Lesser Free Trade Hall"
date: "1976-06-04"
date_precision: jour
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
label: "Second concert des Sex Pistols au Lesser Free Trade Hall"
date: "1976-07-20"
date_precision: jour
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
label: "Premier concert de Warsaw à l'Electric Circus"
date: "1977-05-29"
date_precision: jour
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
label: "Premier concert sous le nom Joy Division (Pips)"
date: "1978-01-25"
date_precision: jour
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
label: "Arrivée de Stephen Morris (batteur)"
date: "1977-08"
date_precision: mois
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
label: "Sortie de A Factory Sample (FAC 2)"
date: "1979-01"
date_precision: mois
sources:
  - MASTER
  - S10
  - S41
membres_reconcilies:
  - CHR-1979-001
  - CHR-S41-1979-01-A-FACTORY-SAMPLE-RELEASE
  - CHR-S10-1978-006
```

---

## EVENT-SORTIE-UNKNOWN-PLEASURES — Sortie de l'album Unknown Pleasures (FACT 10)

```yaml
id: EVENT-SORTIE-UNKNOWN-PLEASURES
type_unite: chronology_event
categorie: jalon
label: "Sortie de l'album Unknown Pleasures (FACT 10)"
date: "1979-06-14"
date_precision: jour
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
label: "Dernier concert de Joy Division (Birmingham University)"
date: "1980-05-02"
date_precision: jour
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
label: "Mort de Ian Curtis"
date: "1980-05-18"
date_precision: jour
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
label: "Sortie posthume de l'album Closer"
date: "1980-07-18"
date_precision: jour
sources:
  - MASTER
  - S41
membres_reconcilies:
  - CHR-1980-004
  - CHR-S41-1980-CLOSER-RELEASE-POSTHUMOUS
```

---

## EVENT-PREMIERES-DEMOS-WARSAW-PENNINE-SOUND — Premières démos de Warsaw à Pennine Sound Studios

```yaml
id: EVENT-PREMIERES-DEMOS-WARSAW-PENNINE-SOUND
type_unite: chronology_event
categorie: jalon
label: "Premières démos de Warsaw à Pennine Sound Studios"
date: "1977-07-18"
date_precision: jour
sources:
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1977-07-18-WARSAW-DEMO-PENNINE
  - CHR-S75-1977-001
  - CHR-S76-1977-005
```

---

## EVENT-DERNIER-CONCERT-WARSAW-SWINGING-APPLE — Dernier concert sous le nom Warsaw (Swinging Apple, Liverpool)

```yaml
id: EVENT-DERNIER-CONCERT-WARSAW-SWINGING-APPLE
type_unite: chronology_event
categorie: jalon
label: "Dernier concert sous le nom Warsaw (Swinging Apple, Liverpool)"
date: "1977-12-31"
date_precision: jour
sources:
  - S41
  - S45
membres_reconcilies:
  - CHR-S41-TL2-1977-12-31-SWINGING-APPLE-LAST-WARSAW
  - CHR-S45-1977-12-31-SWINGING-APPLE
```

---

## EVENT-SESSIONS-RCA-ARROW-STUDIOS — Sessions de l'album avorté RCA / Arrow Studios

```yaml
id: EVENT-SESSIONS-RCA-ARROW-STUDIOS
type_unite: chronology_event
categorie: jalon
label: "Sessions de l'album avorté RCA / Arrow Studios"
date: "1978-05"
date_precision: mois
sources:
  - MASTER
  - S10
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-1978-001
  - CHR-S41-1978-05-ARROW-STUDIOS-RCA
  - CHR-S41-TL3-1978-05-03-04-ARROW-STUDIOS
  - CHR-S76-1978-005
  - CHR-S45-1978-04-RCA-ARROW
  - CHR-S75-1978-006
  - CHR-S10-1978-003
prudence_methodologique: >
  Périmètre retenu : sessions d'enregistrement à Arrow Studios pour RCA. Le contact RCA/Swan autour d'une reprise (CHR-S41-1978-05-RCA-SWAN-INTERZONE) et l'accord de management Gretton (CHR-S41-TL3-1978-05-GRETTON-MANAGER) sont des événements distincts, non fusionnés ici.
```

---

## EVENT-DEBUT-TELEVISION-GRANADA-SHADOWPLAY — Débuts télévisés de Joy Division (Granada Reports, « Shadowplay »)

```yaml
id: EVENT-DEBUT-TELEVISION-GRANADA-SHADOWPLAY
type_unite: chronology_event
categorie: jalon
label: "Débuts télévisés de Joy Division (Granada Reports, « Shadowplay »)"
date: "1978-09-20"
date_precision: jour
sources:
  - S10
  - S41
  - S45
membres_reconcilies:
  - CHR-S10-1978-005
  - CHR-S41-1978-09-20-GRANADA-REPORTS-SHADOWPLAY
  - CHR-S41-TL3-1978-09-20-GRANADA-SHADOWPLAY
  - CHR-S45-1978-GRANADA-SHADOWPLAY
```

---

## EVENT-ENREGISTREMENT-A-FACTORY-SAMPLE-CARGO — Enregistrement de « Digital » et « Glass » (A Factory Sample, Cargo Studios)

```yaml
id: EVENT-ENREGISTREMENT-A-FACTORY-SAMPLE-CARGO
type_unite: chronology_event
categorie: jalon
label: "Enregistrement de « Digital » et « Glass » (A Factory Sample, Cargo Studios)"
date: "1978-10-11"
date_precision: jour
sources:
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-TL3-1978-10-11-CARGO-FACTORY-SAMPLE
  - CHR-S75-1978-007
  - CHR-S76-1978-016
```

---

## EVENT-COUVERTURE-NME-IAN-CURTIS — Ian Curtis en couverture du NME

```yaml
id: EVENT-COUVERTURE-NME-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Ian Curtis en couverture du NME"
date: "1979-01-13"
date_precision: jour
sources:
  - S45
  - S75
membres_reconcilies:
  - CHR-S45-1979-01-13-NME-COVER
  - CHR-S75-1979-001
```

---

## EVENT-DIAGNOSTIC-EPILEPSIE-IAN-CURTIS — Diagnostic d'épilepsie de Ian Curtis

```yaml
id: EVENT-DIAGNOSTIC-EPILEPSIE-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Diagnostic d'épilepsie de Ian Curtis"
date: "1979-01-23"
date_precision: jour
sources:
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S41-1979-01-23-EPILEPSY-DIAGNOSIS
  - CHR-S41-1979-01-23-CURTIS-EPILEPSY-DIAGNOSIS
  - CHR-S45-1979-01-23-SPECIALIST-EPILEPSY
  - CHR-S76-1979-004
```

---

## EVENT-PREMIERE-PEEL-SESSION — Première John Peel Session de Joy Division

```yaml
id: EVENT-PREMIERE-PEEL-SESSION
type_unite: chronology_event
categorie: jalon
label: "Première John Peel Session de Joy Division"
date: "1979-01-31"
date_precision: jour
sources:
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1979-01-31-FIRST-PEEL-SESSION
  - CHR-S75-1979-002
  - CHR-S76-1979-006
  - CHR-S45-1979-01-PEEL-SESSION-1
```

---

## EVENT-NAISSANCE-NATALIE-CURTIS — Naissance de Natalie Curtis

```yaml
id: EVENT-NAISSANCE-NATALIE-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Naissance de Natalie Curtis"
date: "1979-04-16"
date_precision: jour
sources:
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S41-1979-04-16-NATALIE-CURTIS-BORN
  - CHR-S45-1979-04-16-NATALIE-BIRTH
  - CHR-S76-1979-011
```

---

## EVENT-DEUXIEME-PEEL-SESSION — Deuxième John Peel Session de Joy Division

```yaml
id: EVENT-DEUXIEME-PEEL-SESSION
type_unite: chronology_event
categorie: jalon
label: "Deuxième John Peel Session de Joy Division"
date: "1979-11-26"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-11-26-SECOND-PEEL-SESSION
  - CHR-S41-1979-11-26-SECOND-PEEL-LWTUA
prudence_methodologique: >
  Deux entrées S41 (session ; « Love Will Tear Us Apart » y est enregistrée) — duplication intra-source réconciliée.
```

---

## EVENT-FETE-FACTORY-NOUVEL-AN — Fête Factory du Nouvel An (Oldham Street)

```yaml
id: EVENT-FETE-FACTORY-NOUVEL-AN
type_unite: chronology_event
categorie: jalon
label: "Fête Factory du Nouvel An (Oldham Street)"
date: "1979-12-31"
date_precision: jour
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S41-1979-12-31-FACTORY-OFFICE-PARTY
  - CHR-S76-1979-026
prudence_methodologique: >
  Cadrages divergents du même soir : S41 le décrit comme une fête Factory où Gretton tente de vendre des parts ; S76 le présente comme le dernier réveillon de Ian Curtis.
```

---

## EVENT-OVERDOSE-PHENOBARBITAL-IAN-CURTIS — Overdose de phénobarbital de Ian Curtis

```yaml
id: EVENT-OVERDOSE-PHENOBARBITAL-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Overdose de phénobarbital de Ian Curtis"
date: "1980-04-07"
date_precision: jour
sources:
  - S45
  - S75
membres_reconcilies:
  - CHR-S45-1980-04-07-PHENOBARBITONE-OVERDOSE
  - CHR-S75-1980-006
```

---

## EVENT-CONCERT-DERBY-HALL-BURY — Concert du Derby Hall, Bury (interrompu, état critique de Curtis)

```yaml
id: EVENT-CONCERT-DERBY-HALL-BURY
type_unite: chronology_event
categorie: jalon
label: "Concert du Derby Hall, Bury (interrompu, état critique de Curtis)"
date: "1980-04-08"
date_precision: jour
sources:
  - MASTER
  - S45
membres_reconcilies:
  - CHR-1980-001
  - CHR-S45-1980-04-08-DERBY-HALL-BURY-RIOT
```

---

## EVENT-NAISSANCE-BERNARD-SUMNER — Naissance de Bernard Sumner

```yaml
id: EVENT-NAISSANCE-BERNARD-SUMNER
type_unite: chronology_event
categorie: jalon
label: "Naissance de Bernard Sumner"
date: "1956-01-04"
date_precision: jour
sources:
  - S10
membres_reconcilies:
  - CHR-S10-1956-001
```

---

## EVENT-NAISSANCE-PETER-HOOK — Naissance de Peter Hook

```yaml
id: EVENT-NAISSANCE-PETER-HOOK
type_unite: chronology_event
categorie: jalon
label: "Naissance de Peter Hook"
date: "1956-02-13"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1956-HOOK-BIRTH-SALFORD
```

---

## EVENT-RENCONTRE-SUMNER-HOOK-SALFORD-GRAMMAR — Rencontre de Bernard Sumner et Peter Hook (Salford Grammar School)

```yaml
id: EVENT-RENCONTRE-SUMNER-HOOK-SALFORD-GRAMMAR
type_unite: chronology_event
categorie: jalon
label: "Rencontre de Bernard Sumner et Peter Hook (Salford Grammar School)"
date: "1967"
date_precision: annee
sources:
  - S10
  - S41
membres_reconcilies:
  - CHR-S41-1967-SALFORD-GRAMMAR-MEETS-SUMNER
  - CHR-S10-1970S-002
prudence_methodologique: >
  Datation divergente : S41 « 1967 » ; S10 « début des années 1970 ».
```

---

## EVENT-MARIAGE-IAN-DEBORAH-CURTIS — Mariage de Ian Curtis et Deborah Woodruff

```yaml
id: EVENT-MARIAGE-IAN-DEBORAH-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Mariage de Ian Curtis et Deborah Woodruff"
date: "1975-08-23"
date_precision: jour
sources:
  - S76
membres_reconcilies:
  - CHR-S76-1975-001
```

---

## EVENT-RECRUTEMENT-IAN-CURTIS — Ian Curtis devient le chanteur du groupe

```yaml
id: EVENT-RECRUTEMENT-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Ian Curtis devient le chanteur du groupe"
date: "1976-12"
date_precision: mois
sources:
  - S10
  - S41
membres_reconcilies:
  - CHR-S41-1976-12-CURTIS-JOINS
  - CHR-S10-1976-003
prudence_methodologique: >
  S10 situe le recrutement via une annonce déposée chez Virgin (fin 1976).
```

---

## EVENT-CHANGEMENT-NOM-WARSAW-JOY-DIVISION — Changement de nom : Warsaw devient Joy Division

```yaml
id: EVENT-CHANGEMENT-NOM-WARSAW-JOY-DIVISION
type_unite: chronology_event
categorie: jalon
label: "Changement de nom : Warsaw devient Joy Division"
date: "1977-12"
date_precision: mois
sources:
  - S41
  - S45
membres_reconcilies:
  - CHR-S41-1977-JOY-DIVISION-NAME-STABILIZED
  - CHR-S45-1978-01-AN-IDEAL-NAME-CHANGE
  - CHR-S41-1977-WARSAW-PAKT-NAME-COLLISION
prudence_methodologique: >
  La collision avec « Warsaw Pakt » (CHR-S41-1977-WARSAW-PAKT-NAME-COLLISION) est la cause documentée du changement.
```

---

## EVENT-INSTALLATION-TJ-DAVIDSONS — Installation du groupe à T. J. Davidson's (local de répétition)

```yaml
id: EVENT-INSTALLATION-TJ-DAVIDSONS
type_unite: chronology_event
categorie: jalon
label: "Installation du groupe à T. J. Davidson's (local de répétition)"
date: "1977"
date_precision: annee
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S41-1977-TJ-DAVIDSONS-PRACTICE-ROOM
  - CHR-S76-1978-017
```

---

## EVENT-DEPART-TONY-TABAC — Départ de Tony Tabac (batterie)

```yaml
id: EVENT-DEPART-TONY-TABAC
type_unite: chronology_event
categorie: jalon
label: "Départ de Tony Tabac (batterie)"
date: "1977-06-25"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1977-06-25-TONY-TABAC-LAST-GIG
```

---

## EVENT-ENREGISTREMENT-AN-IDEAL-FOR-LIVING — Enregistrement de l'EP An Ideal for Living (Pennine Sound)

```yaml
id: EVENT-ENREGISTREMENT-AN-IDEAL-FOR-LIVING
type_unite: chronology_event
categorie: jalon
label: "Enregistrement de l'EP An Ideal for Living (Pennine Sound)"
date: "1977-12"
date_precision: mois
sources:
  - S10
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S41-1977-PENNINE-AN-IDEAL-SESSION
  - CHR-S45-1977-12-PENNINE-AN-IDEAL
  - CHR-S41-TL2-1977-12-14-AN-IDEAL-SESSIONS
  - CHR-S76-1977-010
  - CHR-S10-1978-004
```

---

## EVENT-SORTIE-AN-IDEAL-FOR-LIVING-7-POUCES — Sortie de An Ideal for Living, 7 pouces original (Enigma PSS 139)

```yaml
id: EVENT-SORTIE-AN-IDEAL-FOR-LIVING-7-POUCES
type_unite: chronology_event
categorie: jalon
label: "Sortie de An Ideal for Living, 7 pouces original (Enigma PSS 139)"
date: "1978-06-03"
date_precision: jour
sources:
  - S41
  - S75
membres_reconcilies:
  - CHR-S41-TL3-1978-06-03-AN-IDEAL-SEVEN-INCH
  - CHR-S75-1978-003
```

---

## EVENT-REEDITION-AN-IDEAL-FOR-LIVING-12-POUCES — Réédition de An Ideal for Living en 12 pouces (Anonymous ANON1)

```yaml
id: EVENT-REEDITION-AN-IDEAL-FOR-LIVING-12-POUCES
type_unite: chronology_event
categorie: jalon
label: "Réédition de An Ideal for Living en 12 pouces (Anonymous ANON1)"
date: "1978-10-10"
date_precision: jour
sources:
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-TL3-1978-10-10-AN-IDEAL-TWELVE-INCH
  - CHR-S41-1978-06-AIL-12-INCH-RABID
  - CHR-S75-1978-004
  - CHR-S76-1978-010
```

---

## EVENT-ENREGISTREMENT-SHORT-CIRCUIT-ELECTRIC-CIRCUS — Captation pour Short Circuit (dernière soirée de l'Electric Circus)

```yaml
id: EVENT-ENREGISTREMENT-SHORT-CIRCUIT-ELECTRIC-CIRCUS
type_unite: chronology_event
categorie: jalon
label: "Captation pour Short Circuit (dernière soirée de l'Electric Circus)"
date: "1977-10-02"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1977-10-02-ELECTRIC-CIRCUS-SHORT-CIRCUIT
  - CHR-S41-TL2-1977-10-02-SHORT-CIRCUIT-COLD-ENTRY
```

---

## EVENT-SORTIE-SHORT-CIRCUIT-LIVE — Sortie de Short Circuit – Live at the Electric Circus

```yaml
id: EVENT-SORTIE-SHORT-CIRCUIT-LIVE
type_unite: chronology_event
categorie: jalon
label: "Sortie de Short Circuit – Live at the Electric Circus"
date: "1978-06-09"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-TL3-1978-06-09-SHORT-CIRCUIT
```

---

## EVENT-ROB-GRETTON-DEVIENT-MANAGER — Rob Gretton devient le manager de Joy Division

```yaml
id: EVENT-ROB-GRETTON-DEVIENT-MANAGER
type_unite: chronology_event
categorie: jalon
label: "Rob Gretton devient le manager de Joy Division"
date: "1978-05"
date_precision: mois
sources:
  - S41
  - S45
  - S76
membres_reconcilies:
  - CHR-S41-TL3-1978-05-GRETTON-MANAGER
  - CHR-S45-1978-GRETTON-MANAGER
  - CHR-S76-1978-007
```

---

## EVENT-PREMIERE-SOIREE-FACTORY — Première soirée Factory (Russell Club)

```yaml
id: EVENT-PREMIERE-SOIREE-FACTORY
type_unite: chronology_event
categorie: jalon
label: "Première soirée Factory (Russell Club)"
date: "1978-05-19"
date_precision: jour
sources:
  - S76
membres_reconcilies:
  - CHR-S76-1978-013
```

---

## EVENT-SESSION-PICCADILLY-RADIO — Session Piccadilly Radio

```yaml
id: EVENT-SESSION-PICCADILLY-RADIO
type_unite: chronology_event
categorie: jalon
label: "Session Piccadilly Radio"
date: "1979-06-04"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-06-04-PICCADILLY-RADIO
  - CHR-S41-1979-06-PICCADILLY-RADIO-CHANCE-ATROCITY
```

---

## EVENT-TELEVISION-WHATS-ON-SHES-LOST-CONTROL — Enregistrement télévisé « She's Lost Control » (What's On / Granada)

```yaml
id: EVENT-TELEVISION-WHATS-ON-SHES-LOST-CONTROL
type_unite: chronology_event
categorie: jalon
label: "Enregistrement télévisé « She's Lost Control » (What's On / Granada)"
date: "1979"
date_precision: annee
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-GRANADA-WHATS-ON-SLC
```

---

## EVENT-PERFORMANCE-BBC2-SOMETHING-ELSE — Performance BBC2 « Something Else » (« Transmission » / « She's Lost Control »)

```yaml
id: EVENT-PERFORMANCE-BBC2-SOMETHING-ELSE
type_unite: chronology_event
categorie: jalon
label: "Performance BBC2 « Something Else » (« Transmission » / « She's Lost Control »)"
date: "1979-09"
date_precision: mois
sources:
  - S75
  - S76
membres_reconcilies:
  - CHR-S76-1979-016
  - CHR-S75-1979-010
prudence_methodologique: >
  Diffusion le 15 septembre 1979 (S76).
```

---

## EVENT-SESSIONS-UNKNOWN-PLEASURES-STRAWBERRY — Sessions d'enregistrement de Unknown Pleasures (Strawberry Studios)

```yaml
id: EVENT-SESSIONS-UNKNOWN-PLEASURES-STRAWBERRY
type_unite: chronology_event
categorie: jalon
label: "Sessions d'enregistrement de Unknown Pleasures (Strawberry Studios)"
date: "1979-04"
date_precision: mois
sources:
  - S10
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1979-03-31-05-02-UP-STRAWBERRY
  - CHR-S41-1979-04-STRAWBERRY-UP-SESSIONS
  - CHR-S45-1979-04-UNKNOWN-PLEASURES-STRAWBERRY
  - CHR-S75-1979-004
  - CHR-S76-1979-010
  - CHR-S10-1979-002
```

---

## EVENT-SESSIONS-TRANSMISSION — Sessions d'enregistrement de « Transmission »

```yaml
id: EVENT-SESSIONS-TRANSMISSION
type_unite: chronology_event
categorie: jalon
label: "Sessions d'enregistrement de « Transmission »"
date: "1979-07"
date_precision: mois
sources:
  - S41
  - S75
membres_reconcilies:
  - CHR-S41-1979-07-CENTRAL-SOUND-TRANSMISSION
  - CHR-S41-1979-07-01-CENTRAL-SOUND-TRANSMISSION
  - CHR-S75-1979-009
  - CHR-S41-1979-07-28-08-04-STRAWBERRY-TRANSMISSION
prudence_methodologique: >
  Deux studios : sessions Central Sound puis version single à Strawberry.
```

---

## EVENT-SESSIONS-LICHT-UND-BLINDHEIT — Sessions « Atmosphere » / « Dead Souls » (Licht und Blindheit, Cargo Studios)

```yaml
id: EVENT-SESSIONS-LICHT-UND-BLINDHEIT
type_unite: chronology_event
categorie: jalon
label: "Sessions « Atmosphere » / « Dead Souls » (Licht und Blindheit, Cargo Studios)"
date_debut: 1979-10
date_fin: 1979-11
date_precision: intervalle
sources:
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1979-10-ATMOSPHERE-LICHT-UND-BLINDHEIT
  - CHR-S41-1979-10-11-CARGO-SORDIDE-ATMOSPHERE
  - CHR-S75-1979-012
  - CHR-S76-1979-024
```

---

## EVENT-SESSIONS-CLOSER-BRITANNIA-ROW — Sessions d'enregistrement de Closer (Britannia Row Studios)

```yaml
id: EVENT-SESSIONS-CLOSER-BRITANNIA-ROW
type_unite: chronology_event
categorie: jalon
label: "Sessions d'enregistrement de Closer (Britannia Row Studios)"
date: "1980-03"
date_precision: mois
sources:
  - S10
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1980-CLOSER-BRITANNIA-ROW-SESSIONS
  - CHR-S45-1980-03-CLOSER-BRITANNIA-ROW
  - CHR-S75-1980-004
  - CHR-S10-1980-002
  - CHR-S76-1980-016
```

---

## EVENT-TOURNEE-BUZZCOCKS — Tournée britannique des Buzzcocks (Joy Division en première partie)

```yaml
id: EVENT-TOURNEE-BUZZCOCKS
type_unite: chronology_event
categorie: jalon
label: "Tournée britannique des Buzzcocks (Joy Division en première partie)"
date: "1979"
date_precision: annee
sources:
  - S41
  - S45
membres_reconcilies:
  - CHR-S45-1979-08-BUZZCOCKS-TOUR-DAY-JOB
  - CHR-S41-1979-BUZZCOCKS-TOUR-PROFESSIONAL
  - CHR-S45-1979-MOUNTFORD-HALL-BUZZCOCKS
```

---

## EVENT-TOURNEE-EUROPEENNE-1980 — Tournée européenne de Joy Division

```yaml
id: EVENT-TOURNEE-EUROPEENNE-1980
type_unite: chronology_event
categorie: jalon
label: "Tournée européenne de Joy Division"
date: "1980-01"
date_precision: mois
sources:
  - S41
  - S45
  - S75
membres_reconcilies:
  - CHR-S41-1980-01-EUROPEAN-TOUR-ANNIK
  - CHR-S45-1980-01-EUROPEAN-TOUR-DEPART
  - CHR-S75-1980-002
```

---

## EVENT-TENTATIVE-SUICIDE-RETOUR-EUROPE — Tentative de suicide au retour de la tournée européenne (Pernod / couteau)

```yaml
id: EVENT-TENTATIVE-SUICIDE-RETOUR-EUROPE
type_unite: chronology_event
categorie: jalon
label: "Tentative de suicide au retour de la tournée européenne (Pernod / couteau)"
date: "1980-01"
date_precision: mois
sources:
  - S41
  - S45
  - S75
membres_reconcilies:
  - CHR-S41-1980-POST-EUROPE-PERNOD-KNIFE
  - CHR-S45-1980-01-RETURN-PERNOD-BIBLE
  - CHR-S75-1980-003
prudence_methodologique: >
  Datation divergente : S41/S45 « janvier 1980 » ; S75 « février 1980 ».
```

---

## EVENT-SEANCE-PHOTO-CUMMINS-PRINCESS-PARKWAY — Séance photo de Kevin Cummins (Princess Parkway)

```yaml
id: EVENT-SEANCE-PHOTO-CUMMINS-PRINCESS-PARKWAY
type_unite: chronology_event
categorie: jalon
label: "Séance photo de Kevin Cummins (Princess Parkway)"
date: "1979-01-06"
date_precision: jour
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-01-06-CUMMINS-PRINCESS-PARKWAY
```

---

## EVENT-SEANCE-PHOTO-CORBIJN — Première séance photo d'Anton Corbijn

```yaml
id: EVENT-SEANCE-PHOTO-CORBIJN
type_unite: chronology_event
categorie: jalon
label: "Première séance photo d'Anton Corbijn"
date: "1979-11"
date_precision: mois
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-11-CORBIJN-PHOTO-SESSION
```

---

## EVENT-POCHETTE-CLOSER-STAGLIENO — Conception de la pochette de Closer (photographie de Staglieno, Saville)

```yaml
id: EVENT-POCHETTE-CLOSER-STAGLIENO
type_unite: chronology_event
categorie: jalon
label: "Conception de la pochette de Closer (photographie de Staglieno, Saville)"
date: "1980-03"
date_precision: mois
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S76-1980-019
  - CHR-S41-1980-SAVILLE-STAGLIENO-CLOSER-LWTUA
```

---

## EVENT-TOURNAGE-VIDEO-LOVE-WILL-TEAR-US-APART — Tournage de la vidéo « Love Will Tear Us Apart » (T. J. Davidson's)

```yaml
id: EVENT-TOURNAGE-VIDEO-LOVE-WILL-TEAR-US-APART
type_unite: chronology_event
categorie: jalon
label: "Tournage de la vidéo « Love Will Tear Us Apart » (T. J. Davidson's)"
date: "1980-04"
date_precision: mois
sources:
  - S41
  - S45
membres_reconcilies:
  - CHR-S45-1980-04-25-LWTUA-VIDEO
  - CHR-S41-1980-04-MAY-LWTUA-VIDEO-TJ-DAVIDSONS
```

---

## EVENT-FUNERAILLES-IAN-CURTIS — Funérailles et crémation de Ian Curtis

```yaml
id: EVENT-FUNERAILLES-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Funérailles et crémation de Ian Curtis"
date: "1980-05"
date_precision: mois
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S41-1980-05-FUNERAL-AND-WAKE
  - CHR-S76-1980-033
prudence_methodologique: >
  Crémation le 23 mai 1980 (S76) ; wake Factory à Palatine Road.
```

---

## EVENT-SORTIE-FAC13-TRANSMISSION — Sortie du single « Transmission » / « Novelty » (FAC 13)

```yaml
id: EVENT-SORTIE-FAC13-TRANSMISSION
type_unite: chronology_event
categorie: jalon
label: "Sortie du single « Transmission » / « Novelty » (FAC 13)"
date: "1979-10"
date_precision: mois
sources:
  - S41
membres_reconcilies:
  - CHR-S41-1979-10-EARCOM-FAC13-SORDIDE-BUZZCOCKS
prudence_methodologique: >
  Seule mention legacy : une entrée-résumé d'octobre 1979 (CHR-S41-1979-10-EARCOM-FAC13-SORDIDE-BUZZCOCKS) couvrant aussi Earcom 2, Sordide Sentimental et le début de tournée Buzzcocks ; rattachée ici à FAC 13 comme sortie dominante (membership mince).
```

---

## EVENT-SORTIE-EARCOM-2 — Parution de « Autosuggestion » / « From Safety to Where…? » sur Earcom 2

```yaml
id: EVENT-SORTIE-EARCOM-2
type_unite: chronology_event
categorie: jalon
label: "Parution de « Autosuggestion » / « From Safety to Where…? » sur Earcom 2"
date: "1979-10"
date_precision: mois
sources:
  - S75
membres_reconcilies:
  - CHR-S75-1979-007
```

---

## EVENT-ENREGISTREMENT-LOVE-WILL-TEAR-US-APART — Enregistrement et mixage de « Love Will Tear Us Apart »

```yaml
id: EVENT-ENREGISTREMENT-LOVE-WILL-TEAR-US-APART
type_unite: chronology_event
categorie: jalon
label: "Enregistrement et mixage de « Love Will Tear Us Apart »"
date_debut: 1980-01
date_fin: 1980-03
date_precision: intervalle
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S41-1980-LWTUA-PENNINE-STRAWBERRY-MIX
  - CHR-S76-1980-002
  - CHR-S76-1980-013
prudence_methodologique: >
  Version Pennine initiale (janvier) puis reprise et mix à Strawberry (mars) ; le tournage vidéo est un événement distinct.
```

---

## EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS — Première crise épileptique majeure de Ian Curtis (retour du Hope & Anchor)

```yaml
id: EVENT-PREMIERE-CRISE-EPILEPTIQUE-IAN-CURTIS
type_unite: chronology_event
categorie: jalon
label: "Première crise épileptique majeure de Ian Curtis (retour du Hope & Anchor)"
date: "1978-12-27"
date_precision: jour
sources:
  - MASTER
  - S10
  - S41
  - S45
  - S75
  - S76
membres_reconcilies:
  - CHR-1978-002
  - CHR-S41-1978-12-M1-LUTON-FIRST-FIT
  - CHR-S45-1978-12-27-HOPE-AND-ANCHOR-FIRST-FIT
  - CHR-S75-1978-008
  - CHR-S76-1978-019
  - CHR-S10-1978-007
prudence_methodologique: >
  Composante non-concert du bundle du 27/12/1978 ; la composante concert (premier concert londonien) reste résiduelle, taguée a_scinder_concert.
```

---

## EVENT-RENCONTRE-ANNIK-HONORE — Entrée d'Annik Honoré dans l'entourage de Joy Division (Nashville Rooms)

```yaml
id: EVENT-RENCONTRE-ANNIK-HONORE
type_unite: chronology_event
categorie: jalon
label: "Entrée d'Annik Honoré dans l'entourage de Joy Division (Nashville Rooms)"
date: "1979-08-13"
date_precision: jour
sources:
  - S41
  - S76
membres_reconcilies:
  - CHR-S41-1979-08-13-NASHVILLE-ANNIK
  - CHR-S41-1979-08-13-NASHVILLE-ANNIK-ATMOSPHERE
  - CHR-S76-1979-019
prudence_methodologique: >
  Composante non-concert du bundle du 13/08/1979 ; la composante concert reste résiduelle, taguée a_scinder_concert.
```

---

## EVENT-CRISE-RAINBOW-THEATRE — Crise de Ian Curtis au Rainbow Theatre (stroboscopes)

```yaml
id: EVENT-CRISE-RAINBOW-THEATRE
type_unite: chronology_event
categorie: jalon
label: "Crise de Ian Curtis au Rainbow Theatre (stroboscopes)"
date: "1980-04-04"
date_precision: jour
sources:
  - S41
  - S75
membres_reconcilies:
  - CHR-S41-1980-04-04-RAINBOW-FIT-MOONLIGHT-INSISTENCE
  - CHR-S75-1980-005
prudence_methodologique: >
  Composante non-concert du bundle du 04/04/1980 ; la composante concert reste résiduelle, taguée a_scinder_concert.
```

---

## EVENT-DEMOS-GENETIC-EDEN-STUDIOS — Démos pour Genetic à Eden Studios (Martin Rushent)

```yaml
id: EVENT-DEMOS-GENETIC-EDEN-STUDIOS
type_unite: chronology_event
categorie: jalon
label: "Démos pour Genetic à Eden Studios (Martin Rushent)"
date: "1979-03-04"
date_precision: jour
sources:
  - S41
  - S75
  - S76
membres_reconcilies:
  - CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE
  - CHR-S75-1979-003
  - CHR-S76-1979-007
  - CHR-S41-1979-EDEN-STUDIOS-RUSHENT-DEMOS
prudence_methodologique: >
  Composante non-concert du bundle du 04/03/1979 ; la composante concert (gig au Marquee, CHR-S41-1979-03-04-EDEN-GENETIC-MARQUEE) reste résiduelle, taguée a_scinder_concert.
```

---

## EVENT-GENESE-DUO-SUMNER-HOOK — Bernard Sumner et Peter Hook commencent à jouer ensemble (genèse du groupe)

```yaml
id: EVENT-GENESE-DUO-SUMNER-HOOK
type_unite: chronology_event
categorie: jalon
label: "Bernard Sumner et Peter Hook commencent à jouer ensemble (genèse du groupe)"
date: "1976"
date_precision: annee
sources:
  - S10
membres_reconcilies:
  - CHR-S10-1976-002
```

---
