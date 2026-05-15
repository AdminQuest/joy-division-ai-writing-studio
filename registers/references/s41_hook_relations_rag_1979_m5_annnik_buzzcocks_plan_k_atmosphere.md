# S41 — Relations stabilisées et entrées RAG — M5, Annik, Buzzcocks tour, Plan K, « Atmosphere »

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A132-CONCEPT-108
    source: S41-A132
    type: prolonge
    cible: CONCEPT-108
    justification: >
      L’accident du van met fin au rôle de Hook comme chauffeur principal et transforme la logistique de tournée.

  - id: REL-S41-A133-CONCEPT-105
    source: S41-A133
    type: prolonge
    cible: CONCEPT-105
    justification: >
      Le souvenir de Hook sur Annik et l’entretien En Attendant est corrigé par une archive sonore, ce qui impose une prudence méthodologique.

  - id: REL-S41-A134-CONCEPT-106
    source: S41-A134
    type: prolonge
    cible: CONCEPT-106
    justification: >
      Hook pluralise Curtis contre la figure unique du martyr littéraire ou du pur chanteur tragique.

  - id: REL-S41-A135-CONCEPT-104
    source: S41-A135
    type: prolonge
    cible: CONCEPT-104
    justification: >
      Le groupe bénéficie de l’énergie scénique de Curtis tandis que le foyer en reçoit le contrecoup domestique et médical.

  - id: REL-S41-A136-CONCEPT-107
    source: S41-A136
    type: prolonge
    cible: CONCEPT-107
    justification: >
      Les crises et la sensibilité aux flashes conduisent à une adaptation lumineuse qui devient signature visuelle.

  - id: REL-S41-A137-CONCEPT-091
    source: S41-A137
    type: prolonge
    cible: CONCEPT-091
    justification: >
      Après une crise grave, le groupe accepte la parole rassurante de Curtis et poursuit la tournée.

  - id: REL-S41-A138-CONCEPT-108
    source: S41-A138
    type: prolonge
    cible: CONCEPT-108
    justification: >
      La tournée Buzzcocks fait passer Joy Division au statut professionnel, mais dans une économie très pauvre.

  - id: REL-S41-A139-CONCEPT-109
    source: S41-A139
    type: prolonge
    cible: CONCEPT-109
    justification: >
      La nuit de Glasgow illustre la masculinité de tournée : alcool, défi obscène, destruction et risque policier.

  - id: REL-S41-A140-CONCEPT-109
    source: S41-A140
    type: prolonge
    cible: CONCEPT-109
    justification: >
      La farce de Dundee prolonge la culture interne brutale et potache de tournée.

  - id: REL-S41-A141-CONCEPT-110
    source: S41-A141
    type: prolonge
    cible: CONCEPT-110
    justification: >
      Plan K associe seuil européen, avant-garde internationale et désordre de tournée pauvre.

  - id: REL-S41-A142-CONCEPT-111
    source: S41-A142
    type: prolonge
    cible: CONCEPT-111
    justification: >
      « Atmosphere » apparaît d’abord dans un circuit limité avant de devenir morceau canonique et funéraire.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A132
    source_id: S41
    atom_id: S41-A132
    title: "M5 : accident du van et fin du bassiste-chauffeur"
    chapters:
      - Chapitre 6
      - Chapitre 10
    tags:
      - m5
      - van-accident
      - bass-cab
      - touring-logistics
      - peter-hook
    query_boost:
      - "No more driving the van for me"
      - "forty-foot lorry bass cab motorway Joy Division"
    use_for:
      - logistique de tournée
      - professionnalisation pauvre
    avoid_for:
      - causalité unique de l’alcoolisme

  - id: RAG-S41-A133
    source_id: S41
    atom_id: S41-A133
    title: "Annik Honoré et mémoire corrigée par archive"
    chapters:
      - Chapitre 10
      - Chapitre 12
      - Chapitre 14
    tags:
      - annik-honore
      - en-attendant
      - dave-pils
      - control
      - memory
    query_boost:
      - "You shouldn’t trust a word I say"
      - "Annik En Attendant Dave Pils tape Hooky"
    use_for:
      - méthode critique des mémoires
      - relation Annik / Ian à croiser
    avoid_for:
      - psychologisation non croisée

  - id: RAG-S41-A134
    source_id: S41
    atom_id: S41-A134
    title: "Ian Curtis non sacralisé : one of the lads"
    chapters:
      - Chapitre 10
      - Chapitre 12
      - Chapitre 14
    tags:
      - ian-curtis
      - myth
      - one-of-the-lads
      - deification
      - people-pleaser
    query_boost:
      - "He was our mate"
      - "deification of Ian one of the lads"
    use_for:
      - démythification de Curtis
      - pluralité des Ian
    avoid_for:
      - contre-mythe viriliste

  - id: RAG-S41-A136
    source_id: S41
    atom_id: S41-A136
    title: "Crises sur scène et washes de lumière"
    chapters:
      - Chapitre 12
      - Chapitre 14
    tags:
      - epilepsy
      - lighting
      - washes
      - ian-curtis-dance
      - stagecraft
    query_boost:
      - "yet another of those things that unintentionally ended up defining us"
      - "Rob lighting men flashes Ian fit washes"
    use_for:
      - scénographie par contrainte médicale
      - santé et performance
    avoid_for:
      - romantisation des crises

  - id: RAG-S41-A137
    source_id: S41
    atom_id: S41-A137
    title: "Leeds : crise grave et consentement commode"
    chapters:
      - Chapitre 12
    tags:
      - leeds
      - seizure
      - epilepsy
      - buzzcocks-tour
      - responsibility
    query_boost:
      - "Because he said he was all right that’s why"
      - "holding his tongue Leeds seizure"
    use_for:
      - responsabilité collective
      - poursuite de tournée malgré crise
    avoid_for:
      - procès rétrospectif simpliste

  - id: RAG-S41-A138
    source_id: S41
    atom_id: S41-A138
    title: "Buzzcocks tour : professionnalisation pauvre"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - buzzcocks
      - tour
      - professional-musicians
      - lobster-thermidor
      - rough-cousins
    query_boost:
      - "We were professional musicians"
      - "rough cousins lobster thermidor Buzzcocks Joy Division"
    use_for:
      - économie de tournée
      - renversement de hiérarchie punk
    avoid_for:
      - supériorité scénique non croisée

  - id: RAG-S41-A141
    source_id: S41
    atom_id: S41-A141
    title: "Plan K Bruxelles : avant-garde et potacherie"
    chapters:
      - Chapitre 6
      - Chapitre 11
      - Chapitre 14
    tags:
      - plan-k
      - brussels
      - william-burroughs
      - cabaret-voltaire
      - europe
    query_boost:
      - "Fuck off kid William Burroughs Joy Division Plan K"
      - "Plan K Brussels youth hostel horse meat"
    use_for:
      - première Europe
      - avant-garde désacralisée
    avoid_for:
      - réduction à l’anecdote scatologique

  - id: RAG-S41-A142
    source_id: S41
    atom_id: S41-A142
    title: "Atmosphere / Licht und Blindheit : circuit limité et postérité funéraire"
    chapters:
      - Chapitre 4
      - Chapitre 8
      - Chapitre 12
      - Chapitre 14
    tags:
      - atmosphere
      - licht-und-blindheit
      - sordide-sentimental
      - limited-edition
      - funeral
    query_boost:
      - "Who puts one of their best songs on a limited-edition single available only in France"
      - "Atmosphere death march funerals Peter Hook"
    use_for:
      - Sordide Sentimental
      - canonisation posthume
    avoid_for:
      - lecture exclusivement funéraire
```
