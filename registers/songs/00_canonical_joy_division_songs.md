# Registre canonique des chansons — Joy Division / Warsaw

```yaml
id: SONG-CANON-JOY-DIVISION
source_id: REGISTRY
source_label: "Registre canonique interne — chansons Joy Division / Warsaw"
type_unite: song_canon
statut: canonique_interne
scope: "Œuvre originale complète Joy Division / Warsaw, avec quelques démos, répétitions, BBC/Peel et inédits ; exclusion des reprises, chansons New Order hors corpus Joy Division et faux positifs issus des sources."
version: "2026-05-19"
```

## Règles de toilettage

Ce fichier sert de table de correspondance pour l’application `apps/song-register/`.

Règles :

- conserver uniquement les chansons originales Joy Division / Warsaw ;
- agréger les variantes live, BBC, Peel, démos, répétitions et paroles divergentes sous un titre canonique ;
- exclure les reprises, même jouées par Warsaw / Joy Division, sauf si un usage historiographique impose une mention contextuelle ;
- exclure les titres New Order qui ne sont pas des compositions Joy Division tardives ;
- conserver `Ceremony` et `In a Lonely Place` comme cas-limites Joy Division / New Order, car ils appartiennent au corpus terminal du groupe ;
- ne pas créer une entrée distincte pour `Chance` : variante / titre de travail rattaché à `Atmosphere` ;
- ne pas créer une entrée distincte pour `They Walked in Line` : variante rattachée à `Walked in Line`.

## Chansons canoniques

```yaml
songs:
  - id: JD-SONG-001
    type_unite: song
    canonical_song: true
    song: "Atrocity Exhibition"
    slug: "atrocity-exhibition"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["live", "album", "rehearsal", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-002
    type_unite: song
    canonical_song: true
    song: "Isolation"
    slug: "isolation"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-003
    type_unite: song
    canonical_song: true
    song: "Passover"
    slug: "passover"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-004
    type_unite: song
    canonical_song: true
    song: "Colony"
    slug: "colony"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-005
    type_unite: song
    canonical_song: true
    song: "A Means to an End"
    slug: "a-means-to-an-end"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: ["Means to an End"]
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-006
    type_unite: song
    canonical_song: true
    song: "Heart and Soul"
    slug: "heart-and-soul"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-007
    type_unite: song
    canonical_song: true
    song: "Twenty Four Hours"
    slug: "twenty-four-hours"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: ["24 Hours", "Twenty-Four Hours"]
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-008
    type_unite: song
    canonical_song: true
    song: "The Eternal"
    slug: "the-eternal"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-009
    type_unite: song
    canonical_song: true
    song: "Decades"
    slug: "decades"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Closer"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-010
    type_unite: song
    canonical_song: true
    song: "Disorder"
    slug: "disorder"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-011
    type_unite: song
    canonical_song: true
    song: "Day of the Lords"
    slug: "day-of-the-lords"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-012
    type_unite: song
    canonical_song: true
    song: "Candidate"
    slug: "candidate"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-013
    type_unite: song
    canonical_song: true
    song: "Insight"
    slug: "insight"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-014
    type_unite: song
    canonical_song: true
    song: "New Dawn Fades"
    slug: "new-dawn-fades"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-015
    type_unite: song
    canonical_song: true
    song: "She’s Lost Control"
    slug: "shes-lost-control"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: ["She's Lost Control", "Shes Lost Control"]
    include_variants: ["album", "single", "live", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-016
    type_unite: song
    canonical_song: true
    song: "Shadowplay"
    slug: "shadowplay"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: ["Shadow Play"]
    include_variants: ["album", "live", "Granada", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-017
    type_unite: song
    canonical_song: true
    song: "Wilderness"
    slug: "wilderness"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-018
    type_unite: song
    canonical_song: true
    song: "Interzone"
    slug: "interzone"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "demo", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-019
    type_unite: song
    canonical_song: true
    song: "I Remember Nothing"
    slug: "i-remember-nothing"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Unknown Pleasures"]
    aliases: []
    include_variants: ["album", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-020
    type_unite: song
    canonical_song: true
    song: "Transmission"
    slug: "transmission"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["single", "Substance"]
    aliases: []
    include_variants: ["single", "live", "demo", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-021
    type_unite: song
    canonical_song: true
    song: "Novelty"
    slug: "novelty"
    category: "œuvre originale complète"
    period: "Warsaw / Joy Division"
    status: "canonique"
    albums: ["single", "Substance"]
    aliases: []
    include_variants: ["single", "live", "demo", "Warsaw", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-022
    type_unite: song
    canonical_song: true
    song: "Digital"
    slug: "digital"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["A Factory Sample", "Still", "Substance"]
    aliases: []
    include_variants: ["studio", "live", "BBC", "Peel", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-023
    type_unite: song
    canonical_song: true
    song: "Glass"
    slug: "glass"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["A Factory Sample", "Still", "Substance"]
    aliases: []
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-024
    type_unite: song
    canonical_song: true
    song: "Autosuggestion"
    slug: "autosuggestion"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Earcom 2", "Still", "Substance"]
    aliases: ["Auto-Suggestion"]
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-025
    type_unite: song
    canonical_song: true
    song: "From Safety to Where…"
    slug: "from-safety-to-where"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Earcom 2", "Substance"]
    aliases: ["From Safety to Where", "From Safety to Where...?", "From Safety To Where..."]
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-026
    type_unite: song
    canonical_song: true
    song: "Exercise One"
    slug: "exercise-one"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Peel Session", "Still", "Substance"]
    aliases: ["Exercise 1"]
    include_variants: ["Peel", "BBC", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-027
    type_unite: song
    canonical_song: true
    song: "The Sound of Music"
    slug: "the-sound-of-music"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Peel Session", "Still", "Substance"]
    aliases: ["Sound of Music"]
    include_variants: ["Peel", "BBC", "studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-028
    type_unite: song
    canonical_song: true
    song: "The Only Mistake"
    slug: "the-only-mistake"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Still"]
    aliases: ["Only Mistake"]
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-029
    type_unite: song
    canonical_song: true
    song: "Walked in Line"
    slug: "walked-in-line"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Still"]
    aliases: ["They Walked in Line", "They Walked In Line"]
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-030
    type_unite: song
    canonical_song: true
    song: "The Kill (Still)"
    slug: "the-kill"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Still"]
    aliases: ["The Kill", "Kill"]
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-051
    type_unite: song
    canonical_song: true
    song: "The Kill (Warsaw)"
    slug: "the-kill-warsaw"
    category: "Warsaw / pré-Joy Division"
    period: "Warsaw"
    status: "canonique distinct"
    albums: ["Warsaw / early corpus"]
    aliases: ["The Kill", "Kill"]
    include_variants: ["Warsaw", "manuscript", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-031
    type_unite: song
    canonical_song: true
    song: "Something Must Break"
    slug: "something-must-break"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Still", "Substance"]
    aliases: []
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-032
    type_unite: song
    canonical_song: true
    song: "Ice Age"
    slug: "ice-age"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Still", "Substance"]
    aliases: []
    include_variants: ["studio", "demo", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-033
    type_unite: song
    canonical_song: true
    song: "Dead Souls"
    slug: "dead-souls"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Licht und Blindheit", "Still", "Substance"]
    aliases: []
    include_variants: ["studio", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-034
    type_unite: song
    canonical_song: true
    song: "Atmosphere"
    slug: "atmosphere"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Licht und Blindheit", "Still", "Substance"]
    aliases: ["Chance"]
    include_variants: ["studio", "live", "demo", "Sordide Sentimental", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-035
    type_unite: song
    canonical_song: true
    song: "Love Will Tear Us Apart"
    slug: "love-will-tear-us-apart"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["single", "Substance"]
    aliases: ["Love Will Tear Us Apart Again"]
    include_variants: ["single", "Pennine", "Strawberry", "live", "BBC", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-036
    type_unite: song
    canonical_song: true
    song: "These Days"
    slug: "these-days"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["single", "Substance"]
    aliases: []
    include_variants: ["single", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-037
    type_unite: song
    canonical_song: true
    song: "Komakino"
    slug: "komakino"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Komakino", "Substance"]
    aliases: ["Komackino"]
    include_variants: ["single", "flexi", "live", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-038
    type_unite: song
    canonical_song: true
    song: "Incubation"
    slug: "incubation"
    category: "œuvre originale complète"
    period: "Joy Division"
    status: "canonique"
    albums: ["Komakino", "Substance"]
    aliases: []
    include_variants: ["single", "instrumental", "live"]
    exclude: false

  - id: JD-SONG-039
    type_unite: song
    canonical_song: true
    song: "As You Said"
    slug: "as-you-said"
    category: "inédit / instrumental"
    period: "Joy Division"
    status: "canonique"
    albums: ["Komakino", "Substance"]
    aliases: []
    include_variants: ["instrumental", "studio"]
    exclude: false

  - id: JD-SONG-040
    type_unite: song
    canonical_song: true
    song: "No Love Lost"
    slug: "no-love-lost"
    category: "Warsaw / pré-Joy Division"
    period: "Warsaw / Joy Division"
    status: "canonique"
    albums: ["An Ideal for Living"]
    aliases: ["No Love Lost"]
    include_variants: ["EP", "live", "Warsaw", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-041
    type_unite: song
    canonical_song: true
    song: "Leaders of Men"
    slug: "leaders-of-men"
    category: "Warsaw / pré-Joy Division"
    period: "Warsaw / Joy Division"
    status: "canonique"
    albums: ["An Ideal for Living"]
    aliases: []
    include_variants: ["EP", "live", "Warsaw", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-042
    type_unite: song
    canonical_song: true
    song: "Failures"
    slug: "failures"
    category: "Warsaw / pré-Joy Division"
    period: "Warsaw / Joy Division"
    status: "canonique"
    albums: ["An Ideal for Living"]
    aliases: []
    include_variants: ["EP", "live", "Warsaw", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-043
    type_unite: song
    canonical_song: true
    song: "Warsaw"
    slug: "warsaw"
    category: "Warsaw / pré-Joy Division"
    period: "Warsaw / Joy Division"
    status: "canonique"
    albums: ["An Ideal for Living", "Still"]
    aliases: []
    include_variants: ["EP", "live", "Warsaw", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-044
    type_unite: song
    canonical_song: true
    song: "The Drawback"
    slug: "the-drawback"
    category: "démo / répétition"
    period: "Warsaw"
    status: "canonique élargi"
    albums: ["Warsaw demos / bootleg corpus"]
    aliases: ["Drawback"]
    include_variants: ["demo", "Warsaw", "rehearsal"]
    exclude: false

  - id: JD-SONG-045
    type_unite: song
    canonical_song: true
    song: "Gutz"
    slug: "gutz"
    category: "démo / répétition"
    period: "Warsaw"
    status: "canonique élargi"
    albums: ["Warsaw demos / rehearsal corpus"]
    aliases: ["Guts"]
    include_variants: ["demo", "Warsaw", "rehearsal"]
    exclude: false

  - id: JD-SONG-046
    type_unite: song
    canonical_song: true
    song: "Inside the Line"
    slug: "inside-the-line"
    category: "démo / répétition"
    period: "Warsaw"
    status: "canonique élargi"
    albums: ["Warsaw demos / rehearsal corpus"]
    aliases: []
    include_variants: ["demo", "Warsaw", "rehearsal"]
    exclude: false

  - id: JD-SONG-047
    type_unite: song
    canonical_song: true
    song: "You’re No Good for Me"
    slug: "youre-no-good-for-me"
    category: "démo / répétition"
    period: "Warsaw"
    status: "canonique élargi"
    albums: ["Warsaw demos / rehearsal corpus"]
    aliases: ["You're No Good for Me", "Youre No Good for Me", "No Good for Me"]
    include_variants: ["demo", "Warsaw", "rehearsal"]
    exclude: false

  - id: JD-SONG-048
    type_unite: song
    canonical_song: true
    song: "At a Later Date"
    slug: "at-a-later-date"
    category: "Warsaw / live précoce"
    period: "Warsaw"
    status: "canonique élargi"
    albums: ["Short Circuit: Live at the Electric Circus"]
    aliases: []
    include_variants: ["live", "Warsaw", "Electric Circus"]
    exclude: false

  - id: JD-SONG-049
    type_unite: song
    canonical_song: true
    song: "Ceremony"
    slug: "ceremony"
    category: "terminal Joy Division / transition New Order"
    period: "Joy Division / New Order"
    status: "cas-limite inclus"
    albums: ["Still", "New Order single"]
    aliases: []
    include_variants: ["rehearsal", "live", "transition", "lyrics_divergence"]
    exclude: false

  - id: JD-SONG-050
    type_unite: song
    canonical_song: true
    song: "In a Lonely Place"
    slug: "in-a-lonely-place"
    category: "terminal Joy Division / transition New Order"
    period: "Joy Division / New Order"
    status: "cas-limite inclus"
    albums: ["New Order single", "Still / rehearsal corpus"]
    aliases: []
    include_variants: ["rehearsal", "transition", "lyrics_divergence"]
    exclude: false
```

## Titres explicitement exclus du menu

```yaml
songs:
  - id: JD-SONG-EXCL-001
    type_unite: song
    canonical_song: false
    song: "Blue Monday"
    exclude: true
    exclusion_reason: "New Order, hors corpus Joy Division original."

  - id: JD-SONG-EXCL-002
    type_unite: song
    canonical_song: false
    song: "Boredom"
    exclude: true
    exclusion_reason: "Buzzcocks ; titre contextuel, pas chanson Joy Division / Warsaw."

  - id: JD-SONG-EXCL-003
    type_unite: song
    canonical_song: false
    song: "Love Battery"
    exclude: true
    exclusion_reason: "Buzzcocks ; titre contextuel, pas chanson Joy Division / Warsaw."

  - id: JD-SONG-EXCL-004
    type_unite: song
    canonical_song: false
    song: "Louie Louie"
    exclude: true
    exclusion_reason: "Reprise / rituel Jon the Postman ; pas œuvre originale Joy Division."

  - id: JD-SONG-EXCL-005
    type_unite: song
    canonical_song: false
    song: "Sister Ray"
    exclude: true
    exclusion_reason: "Reprise du Velvet Underground ; ne doit pas figurer comme œuvre originale Joy Division."

  - id: JD-SONG-EXCL-006
    type_unite: song
    canonical_song: false
    song: "The Passenger"
    exclude: true
    exclusion_reason: "Reprise d’Iggy Pop ; contexte live seulement."
```
