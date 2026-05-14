# S45 — Relations stabilisées et entrées RAG — Annik, Apollo, Rainbow, effondrement conjugal

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A109-S45-A013
    source: S45-A109
    type: prolonge
    cible: S45-A013
    justification: >
      Annik Honoré reparaît comme figure relationnelle centrale, mais d’abord sous une forme dissimulée et domesticable.

  - id: REL-S45-A110-S45-A095
    source: S45-A110
    type: prolonge
    cible: S45-A095
    justification: >
      La no women policy se concrétise à l’Apollo par l’évacuation de Deborah de la loge où Annik est présente.

  - id: REL-S45-A111-CONCEPT-030
    source: S45-A111
    type: prolonge
    cible: CONCEPT-030
    justification: >
      Rob Gretton intervient dans une crise conjugale afin de maintenir une stabilité minimale autour de Curtis.

  - id: REL-S45-A112-CONCEPT-029
    source: S45-A112
    type: prolonge
    cible: CONCEPT-029
    justification: >
      Les signes sont relus après coup ; sur le moment, la maladie et la peur policière masquent la relation parallèle.

  - id: REL-S45-A113-CONCEPT-031
    source: S45-A113
    type: prolonge
    cible: CONCEPT-031
    justification: >
      La professionnalisation musicale se finance par le travail de nuit de Deborah et le soutien de ses parents.

  - id: REL-S45-A114-CONCEPT-032
    source: S45-A114
    type: prolonge
    cible: CONCEPT-032
    justification: >
      Les farces de tournée et la critique du Rainbow montrent que la relation Joy Division / Buzzcocks devient concurrentielle.

  - id: REL-S45-A115-S45-A108
    source: S45-A115
    type: prolonge
    cible: S45-A108
    justification: >
      Les rituels de langage ne suffisent plus à produire une parole réelle entre Ian et Deborah.

  - id: REL-S45-A116-MOTIF-025
    source: S45-A116
    type: prolonge
    cible: MOTIF-025
    justification: >
      Le fandom dévotionnel se transforme en relation transnationale active par radio, fanzine et rencontre.

  - id: REL-S45-A117-MYTH-005
    source: S45-A117
    type: nuance
    cible: MYTH-005
    justification: >
      Factory n’est pas seulement anti-business ; c’est aussi un théâtre social froid, image, violence et promesse de mobilité.

  - id: REL-S45-A118-CONCEPT-029
    source: S45-A118
    type: prolonge
    cible: CONCEPT-029
    justification: >
      La vérité conjugale est connue indirectement par le groupe avant d’être dite à Deborah.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A109
    source_id: S45
    atom_id: S45-A109
    title: "Annik nommée par périphrase"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - annik-honore
      - deborah-curtis
      - infidelity
      - tour
      - domestic-truth
    query_boost:
      - "chubby Belgian girl tour arranger"
      - "Annik Honoré tour arranger Deborah Curtis"
    use_for:
      - vérité conjugale différée
      - Annik comme figure dissimulée
    avoid_for:
      - causalité romantique unique

  - id: RAG-S45-A110
    source_id: S45
    atom_id: S45-A110
    title: "Apollo Manchester : Deborah face à Annik sans le savoir"
    chapters:
      - Chapitre 10
    tags:
      - apollo-manchester
      - annik-honore
      - dressing-room
      - deborah-curtis
      - humiliation
    query_boost:
      - "totally unaware of my husband's mistress"
      - "Apollo dressing room Annik Deborah Curtis"
    use_for:
      - scène de dépossession conjugale
      - no women policy concrète
    avoid_for:
      - triangle sentimental totalisant

  - id: RAG-S45-A113
    source_id: S45
    atom_id: S45-A113
    title: "Silklands et économie domestique d’épuisement"
    chapters:
      - Chapitre 6
      - Chapitre 10
    tags:
      - silklands
      - finances
      - domestic-economy
      - deborah-curtis
      - cigarettes
    query_boost:
      - "downward spiral of our financial situation"
      - "Silklands bar staff Deborah Curtis"
    use_for:
      - coût domestique de la professionnalisation
      - double travail de Deborah
    avoid_for:
      - grief conjugal isolé

  - id: RAG-S45-A114
    source_id: S45
    atom_id: S45-A114
    title: "Rainbow et Guildford : rivalité de tournée"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - rainbow-theatre
      - guildford
      - buzzcocks-tour
      - chris-bohn
      - sound
    query_boost:
      - "the spirit of resistance was there"
      - "Rainbow Theatre Buzzcocks Joy Division lousy sound"
    use_for:
      - rivalité Joy Division / Buzzcocks
      - support band menaçant
    avoid_for:
      - preuve technique de sabotage sans recoupement

  - id: RAG-S45-A116
    source_id: S45
    atom_id: S45-A116
    title: "Franck Essner et fandom transnational"
    chapters:
      - Chapitre 14
      - Chapitre 6
    tags:
      - franck-essner
      - transmission
      - paris
      - fanzine
      - fandom
    query_boost:
      - "Franck Essner Transmission fanzine"
      - "the band that wrote the song they loved so much"
    use_for:
      - internationalisation du fandom
      - rôle de Transmission comme vecteur
    avoid_for:
      - généralisation à toute la réception française

  - id: RAG-S45-A118
    source_id: S45
    atom_id: S45-A118
    title: "Our marriage was over and he hadn’t told me"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - marriage-collapse
      - deborah-curtis
      - epilepsy-association
      - band-filter
      - narrative-dispossession
    query_boost:
      - "Our marriage was over and he hadn't told me"
      - "Deborah Curtis marriage over Joy Division band blamed me"
    use_for:
      - dépossession narrative de Deborah
      - conclusion du chapitre These Days
    avoid_for:
      - vérité totale du groupe sans croisement
```
