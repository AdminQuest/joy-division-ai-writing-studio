# S45 — Relations stabilisées et entrées RAG — Factory, épilepsie, paroles, Natalie

Ce fichier consolide les relations et l’indexation RAG du passage atomisé dans `sources/curtis_touching_from_a_distance/source_part_1978_1979_factory_epilepsy_lyrics_natalie.md`.

---

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A061-CONCEPT-018
    source: S45-A061
    type: prolonge
    cible: CONCEPT-018
    justification: >
      La grossesse de Deborah révèle la politique affective implicite du groupe :
      relations tenues à distance et bonheur peu partageable.

  - id: REL-S45-A062-MYTH-002
    source: S45-A062
    type: nuance
    cible: MYTH-002
    justification: >
      Le témoignage de Sumner sur l’humour du groupe empêche de figer Joy Division
      dans une noirceur totale.

  - id: REL-S45-A063-CONCEPT-018
    source: S45-A063
    type: prolonge
    cible: CONCEPT-018
    justification: >
      Les « original girlies » donnent à voir une archive féminine minorée de la
      formation du groupe.

  - id: REL-S45-A064-MOTIF-025
    source: S45-A064
    type: prolonge
    cible: MOTIF-025
    justification: >
      Les « Goshes » constituent un noyau précoce de fandom incarné et genré.

  - id: REL-S45-A065-CONCEPT-004
    source: S45-A065
    type: requiert
    cible: CONCEPT-004
    justification: >
      L’épisode Stephanie est une scène privée sensible, dont l’intention ne peut
      pas être établie avec certitude.

  - id: REL-S45-A066-S45-A009
    source: S45-A066
    type: prolonge
    cible: S45-A009
    justification: >
      L’atome consolide le seuil *A Factory Sample* déjà identifié : Hannett, Saville,
      Wilson et silence informatif.

  - id: REL-S45-A067-MYTH-002
    source: S45-A067
    type: prépare
    cible: MYTH-002
    justification: >
      La demande d’autographe au Check Inn montre une canonisation micro-locale
      de Curtis avant la grande postérité.

  - id: REL-S45-A068-S45-A010
    source: S45-A068
    type: prolonge
    cible: S45-A010
    justification: >
      L’atome précise la première crise reconnue après le Hope and Anchor et son
      inscription hospitalière.

  - id: REL-S45-A069-CONCEPT-019
    source: S45-A069
    type: prolonge
    cible: CONCEPT-019
    justification: >
      Le diagnostic différé montre que l’épilepsie est aussi une affaire de foyer,
      d’attente médicale et d’observation domestique.

  - id: REL-S45-A070-MOTIF-026
    source: S45-A070
    type: prolonge
    cible: MOTIF-026
    justification: >
      Couverture NME, Peel session et accommodation de la maladie forment une
      double temporalité publique et domestique.

  - id: REL-S45-A071-CONCEPT-019
    source: S45-A071
    type: requiert
    cible: CONCEPT-019
    justification: >
      Diagnostic et traitements doivent être intégrés comme faisceau, non comme
      causalité unique.

  - id: REL-S45-A072-RISQUE-CAUSALITE-MEDICALE
    source: S45-A072
    type: alerte
    cible: RISQUE-CAUSALITE-MEDICALE
    justification: >
      La conviction de Sumner sur les comprimés est un témoignage fort, mais ne
      constitue pas une preuve médicale.

  - id: REL-S45-A073-CONCEPT-021
    source: S45-A073
    type: prolonge
    cible: CONCEPT-021
    justification: >
      Le rituel d’attente des crises installe Deborah dans une veille conjugale qui
      prépare la double charge domestique.

  - id: REL-S45-A074-CONCEPT-019
    source: S45-A074
    type: requiert
    cible: CONCEPT-019
    justification: >
      La danse de Curtis doit rester dans l’indécidable entre performance, symptôme,
      continuité gestuelle et réception rétrospective.

  - id: REL-S45-A075-S45-A011
    source: S45-A075
    type: prolonge
    cible: S45-A011
    justification: >
      Les carnets, papiers, sac plastique et citation Printed Noises renforcent la
      lecture des paroles comme matériau mobile.

  - id: REL-S45-A076-CONCEPT-020
    source: S45-A076
    type: prolonge
    cible: CONCEPT-020
    justification: >
      Morris et Sumner définissent Curtis comme catalyseur, non auteur total ni
      simple chanteur.

  - id: REL-S45-A077-CONCEPT-014
    source: S45-A077
    type: prolonge
    cible: CONCEPT-014
    justification: >
      L’abandon RCA devient libération éditoriale, rachat des masters et source
      potentielle de bootlegs.

  - id: REL-S45-A078-CONCEPT-006
    source: S45-A078
    type: prolonge
    cible: CONCEPT-006
    justification: >
      Hannett coordonne atmosphères, batterie et sons inhabituels pour stabiliser
      *Unknown Pleasures*.

  - id: REL-S45-A079-CONCEPT-018
    source: S45-A079
    type: prolonge
    cible: CONCEPT-018
    justification: >
      Le bannissement progressif des wives and girlfriends matérialise la politique
      affective et genrée du groupe.

  - id: REL-S45-A080-CONCEPT-021
    source: S45-A080
    type: prolonge
    cible: CONCEPT-021
    justification: >
      La naissance de Natalie transforme la maladie de Curtis en double charge de
      care pour Deborah.
```

---

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A066
    source_id: S45
    atom_id: S45-A066
    title: A Factory Sample comme seuil Factory
    chapters:
      - Chapitre 3
      - Chapitre 5
      - Chapitre 6
    tags:
      - a-factory-sample
      - martin-hannett
      - peter-saville
      - digital
      - glass
      - factory
      - cold-sound
    query_boost:
      - "A Factory Sample much cleaner and colder sound"
      - "Digital Glass Martin Hannett Peter Saville Deborah Curtis"
      - "Joy Division left almost blank Factory Sample"
    use_for:
      - analyser le proto-système Factory
      - relier son froid et minimalisme graphique
      - préparer Unknown Pleasures
    avoid_for:
      - Factory déjà système clos

  - id: RAG-S45-A068
    source_id: S45
    atom_id: S45-A068
    title: Hope and Anchor et première crise reconnue
    chapters:
      - Chapitre 12
    tags:
      - hope-and-anchor
      - epilepsy
      - first-fit
      - luton-and-dunstable
      - phenobarbitone
      - health
    query_boost:
      - "Hope and Anchor first recognizable epileptic fit"
      - "I've had some kind of fit Deborah Curtis"
      - "Luton and Dunstable Hospital Ian Curtis"
    use_for:
      - dater la rupture médicale
      - articuler tournée, fatigue et maladie
      - éviter la téléologie morbide
    avoid_for:
      - cause unique de la mort
      - scène prophétique

  - id: RAG-S45-A071
    source_id: S45
    atom_id: S45-A071
    title: Diagnostic du 23 janvier 1979 et traitements
    chapters:
      - Chapitre 12
    tags:
      - epilepsy
      - phenytoin-sodium
      - phenobarbitone
      - diagnosis
      - macclesfield-hospital
      - side-effects
    query_boost:
      - "Ian was now EPILEPTIC"
      - "Phenytoin Sodium Phenobarbitone Ian Curtis"
      - "23 January 1979 Macclesfield District and General Hospital"
    use_for:
      - traiter la nomination médicale
      - cadrer les effets secondaires possibles
      - distinguer médicament et causalité
    avoid_for:
      - preuve médicale définitive

  - id: RAG-S45-A075
    source_id: S45
    atom_id: S45-A075
    title: Paroles ouvertes, carnets et sac plastique
    chapters:
      - Chapitre 4
    tags:
      - lyrics
      - notebooks
      - plastic-bag
      - printed-noises
      - anti-confessional
      - songwriting
    query_boost:
      - "We haven't got a message really lyrics are open to interpretation"
      - "Ian carried a plastic bag notebooks lyrics"
      - "Printed Noises Joy Division lyrics multidimensional"
    use_for:
      - contrer lecture journal intime
      - expliquer paroles comme matériau mobile
      - articuler écriture et musique collective
    avoid_for:
      - paroles comme suicide note
      - intention transparente

  - id: RAG-S45-A077
    source_id: S45
    atom_id: S45-A077
    title: Abandon RCA, masters et bootlegs
    chapters:
      - Chapitre 8
      - Chapitre bootlegs
    tags:
      - rca
      - master-tapes
      - bootlegs
      - richard-searling
      - rob-gretton
      - publishing
    query_boost:
      - "master tapes were handed over in return for £1,500"
      - "RCA bootlegs cassette copy not original master Deborah Curtis"
      - "Joy Division publishing contract never signed RCA"
    use_for:
      - documenter l’anti-récit RCA
      - alimenter le registre bootlegs
      - expliquer liberté éditoriale
    avoid_for:
      - origine définitive des bootlegs sans vérification sonore

  - id: RAG-S45-A078
    source_id: S45
    atom_id: S45-A078
    title: Unknown Pleasures et Hannett catalyseur sonore
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - unknown-pleasures
      - martin-hannett
      - strawberry-studios
      - drums
      - glass-smashing
      - hand-clapping
      - factory
    query_boost:
      - "the catalyst Joy Division badly needed"
      - "Unknown Pleasures Strawberry Studios glass-smashing hand-clapping"
      - "Hannett drums integral part of the music Deborah Curtis"
    use_for:
      - analyser Hannett comme catalyseur
      - articuler studio et atmosphère
      - préparer lecture d’Unknown Pleasures
    avoid_for:
      - Hannett seul auteur du son

  - id: RAG-S45-A080
    source_id: S45
    atom_id: S45-A080
    title: Naissance de Natalie et double care domestique
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - natalie-curtis
      - birth
      - fatherhood
      - epilepsy
      - domestic-care
      - deborah-curtis
    query_boost:
      - "I can't imagine there being another person here with us"
      - "Natalie birth Ian Curtis afraid fit dropped baby"
      - "Deborah look after both Ian and Natalie single-handedly"
    use_for:
      - analyser paternité empêchée
      - documenter double charge domestique
      - relier maladie et foyer
    avoid_for:
      - moralisation de l’incapacité paternelle
```
