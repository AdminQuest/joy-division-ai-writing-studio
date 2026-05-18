# Registres spécialisés — S35 — Morris, *Record Play Pause*, 2019 — part 02

```yaml
id: REG-S35-PART-02
source_id: S35
source_label: "S35 — Morris, Record Play Pause, 2019"
type_unite: registres_specialises
statut: verifie
passage_atomise: "PDF p. 24-50"
```

## 1. Concepts / motifs / mythes à compléter

```yaml
concepts_a_consolider:
  - id: CONCEPT-S35-009
    label: "humour autobiographique comme garde-fou historiographique"
    atoms: [S35-A021, S35-A025]
    chapters: [Chapitre 1, Chapitre 14]
    statut: candidat_stable
  - id: CONCEPT-S35-010
    label: "rythme par contrainte sociale"
    atoms: [S35-A022, S35-A023, S35-A032]
    chapters: [Chapitre 3]
    statut: candidat_stable
  - id: CONCEPT-S35-011
    label: "musique comme classement social"
    atoms: [S35-A031]
    chapters: [Chapitre 1, Chapitre 2, Chapitre 14]
    statut: candidat_stable
  - id: CONCEPT-S35-012
    label: "imaginaire de guerre non idéologique"
    atoms: [S35-A026]
    chapters: [Chapitre 5, Chapitre 11]
    statut: candidat_prudent

motifs_a_consolider:
  - id: MOTIF-S35-008
    label: "apprentissage par friction"
    atoms: [S35-A023, S35-A029, S35-A032]
    chapters: [Chapitre 3]
  - id: MOTIF-S35-009
    label: "pop matérielle et malentendu enfantin"
    atoms: [S35-A027, S35-A028]
    chapters: [Chapitre 1, Chapitre 3, Chapitre 14]
  - id: MOTIF-S35-010
    label: "style musical comme appartenance tribale"
    atoms: [S35-A031]
    chapters: [Chapitre 1, Chapitre 2, Chapitre 14]

mythes_a_nuancer:
  - id: MYTHE-S35-007
    label: "tout signe de guerre annonce une fascination politique"
    garde_fou: "S35-A026 montre d’abord une culture enfantine des objets, des vestiges et des décors militaires."
    atoms: [S35-A026]
  - id: MYTHE-S35-008
    label: "la batterie de Morris naît uniquement du krautrock"
    garde_fou: "La deuxième passe ajoute des médiations ordinaires : guitare ratée, percussion domestique, danse de salon, rythme subi."
    atoms: [S35-A029, S35-A030, S35-A032]
```

## 2. Citations candidates à contrôler

Aucune citation directe n’est intégrée comme vérifiée. Les passages ci-dessous sont à contrôler mot à mot sur l’édition retenue avant citation dans le manuscrit.

```yaml
citations_candidates:
  - id: QUOTE-S35-P02-001
    pages: "PDF p. 24"
    usage: "Poe / Wodehouse : double registre noirceur-humour"
    statut: a_verifier_avant_usage
  - id: QUOTE-S35-P02-002
    pages: "PDF p. 30"
    usage: "perte de connaissance et perception bidimensionnelle"
    statut: a_verifier_avant_usage
  - id: QUOTE-S35-P02-003
    pages: "PDF p. 41"
    usage: "guitare détruite par accordage"
    statut: a_verifier_avant_usage
  - id: QUOTE-S35-P02-004
    pages: "PDF p. 48"
    usage: "danse de salon et apprentissage des mesures"
    statut: a_verifier_avant_usage
  - id: QUOTE-S35-P02-005
    pages: "PDF p. 49-50"
    usage: "Beatles / Stones / Kinks comme appartenance tribale"
    statut: a_verifier_avant_usage
```

## 3. Chronologie limitée

```yaml
chronologie_a_croiser:
  - id: CHR-S35-P02-1967-001
    date: "1967-1968"
    label: "Morris situe ses pertes de connaissance d’enfance en Class 3 juniors"
    source_id: S35
    atoms: [S35-A024]
    statut: a_croiser_si_usage_factuel
  - id: CHR-S35-P02-1967-002
    date: "1967"
    label: "Morris évoque Jersey et la rencontre avec Jimmy Savile comme souvenir d’enfance"
    source_id: S35
    atoms: [S35-A025]
    statut: a_croiser_si_usage_factuel
  - id: CHR-S35-P02-1960S-001
    date: "années 1960"
    label: "Formation médiatique domestique par radio, télévision et premiers singles"
    source_id: S35
    atoms: [S35-A027, S35-A028]
    statut: contexte
```

## 4. Acteurs, lieux, organisations, chansons

```yaml
acteurs:
  - Stephen Morris
  - Clifford Morris
  - Hilda Morris
  - Amanda Morris
  - Edgar Allan Poe
  - P. G. Wodehouse
  - Jimmy Savile
  - Brian Epstein
  - Little Eva
  - Elvis Presley

lieux:
  - Macclesfield
  - Gawsworth Road
  - Christ Church Primary School
  - Parkside
  - Blackpool
  - Dinard
  - Jersey
  - Bouley Bay
  - Theatre Royal
  - Alex Brown School of Dancing
  - Alton Towers

organisations:
  - The Beatles
  - The Rolling Stones
  - The Kinks
  - Mods
  - Rockers

chansons:
  - "The Locomotion"
  - "Return to Sender"

objets_et_motifs:
  - radio domestique
  - télévision noir et blanc
  - premiers singles
  - guitare enfantine
  - baguettes disparues
  - danse de salon
  - parkas
  - badges
  - bunkers de Jersey
```

## 5. Usage par chapitre

```yaml
chapitres:
  Chapitre 1:
    atoms: [S35-A021, S35-A022, S35-A023, S35-A025, S35-A027, S35-A028, S35-A031]
    usage: "enfance provinciale, formation médiatique, pop comme socialisation"
  Chapitre 2:
    atoms: [S35-A031]
    usage: "préparer les scènes musicales comme tribus de signes avant le punk"
  Chapitre 3:
    atoms: [S35-A023, S35-A027, S35-A028, S35-A029, S35-A030, S35-A032]
    usage: "généalogie ordinaire de la batterie et du rythme"
  Chapitre 5:
    atoms: [S35-A026]
    usage: "prudence sur les signes militaires et l’imagerie de guerre"
  Chapitre 11:
    atoms: [S35-A026]
    usage: "guerre comme décor matériel de l’enfance britannique"
  Chapitre 12:
    atoms: [S35-A024]
    usage: "prudence analogique sur le corps et les malaises"
  Chapitre 14:
    atoms: [S35-A021, S35-A028, S35-A031]
    usage: "mémoire, objets pop, style et appartenance"
```
