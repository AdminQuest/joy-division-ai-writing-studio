# S41 — Relations stabilisées et entrées RAG — Timeline Three, année 1978

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A093-CONCEPT-082
    source: S41-A093
    type: prolonge
    cible: CONCEPT-082
    justification: >
      La Timeline Three verrouille 1978 comme année de bascule documentaire, entre nom, Factory, sessions, télévision, tournées et seuil médical.

  - id: REL-S41-A094-CONCEPT-083
    source: S41-A094
    type: prolonge
    cible: CONCEPT-083
    justification: >
      M24J confirme que Factory précède le label sous forme de projet de management et de club local.

  - id: REL-S41-A095-CONCEPT-084
    source: S41-A095
    type: prolonge
    cible: CONCEPT-084
    justification: >
      Les entrées Arrow, *An Ideal for Living*, *Short Circuit* et *A Factory Sample* distinguent sessions, sorties et rééditions.

  - id: REL-S41-A096-CONCEPT-050
    source: S41-A096
    type: prolonge
    cible: CONCEPT-050
    justification: >
      Les dates avec Rich Kids et Durutti Column inscrivent Joy Division dans une sociabilité de plateau plus large.

  - id: REL-S41-A097-CONCEPT-085
    source: S41-A097
    type: prolonge
    cible: CONCEPT-085
    justification: >
      Suicide fonctionne comme horizon minimal et avant-gardiste, surtout pour Curtis et Morris.

  - id: REL-S41-A098-CONCEPT-086
    source: S41-A098
    type: prolonge
    cible: CONCEPT-086
    justification: >
      Le concert de Bradford transforme la controverse politique en danger scénique possible.

  - id: REL-S41-A099-CONCEPT-087
    source: S41-A099
    type: prolonge
    cible: CONCEPT-087
    justification: >
      Granada Reports impose au groupe un problème d’image, que le montage tente de compenser.

  - id: REL-S41-A100-CONCEPT-088
    source: S41-A100
    type: prolonge
    cible: CONCEPT-088
    justification: >
      La date Rock Against Racism nuance l’accumulation des signes nazis sans l’effacer.

  - id: REL-S41-A101-CONCEPT-079
    source: S41-A101
    type: consolide
    cible: CONCEPT-079
    justification: >
      Les témoignages de Brunel et Bristol consolident la violence corporelle et contractuelle de la tournée 1978.

  - id: REL-S41-A102-CONCEPT-089
    source: S41-A102
    type: prolonge
    cible: CONCEPT-089
    justification: >
      La review du Check Inn situe Joy Division par comparaison avec The Fall et Buzzcocks.

  - id: REL-S41-A103-CONCEPT-080
    source: S41-A103
    type: consolide
    cible: CONCEPT-080
    justification: >
      La review de Nick Tester confirme la désacralisation du premier Londres.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A093
    source_id: S41
    atom_id: S41-A093
    title: "Timeline Three : armature documentaire de 1978"
    chapters:
      - Chapitre 6
      - Chapitre 8
    tags:
      - timeline-three
      - 1978
      - factory
      - joy-division
      - chronology
    query_boost:
      - "TIMELINE THREE JANUARY 1978 DECEMBER 1978"
      - "Pips Stiff Chiswick Arrow Factory Hope Anchor 1978"
    use_for:
      - contrôle chronologique 1978
      - bornage discographique et live
    avoid_for:
      - causalité narrative autonome

  - id: RAG-S41-A095
    source_id: S41
    atom_id: S41-A095
    title: "Arrow, An Ideal, Short Circuit, Cargo : verrous 1978"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - arrow-studios
      - an-ideal-for-living
      - short-circuit
      - a-factory-sample
      - tracklist
    query_boost:
      - "The unreleased-album sessions Arrow Studios Manchester"
      - "An Ideal seven-inch Short Circuit A Factory Sample 1978 timeline"
    use_for:
      - sessionographie
      - dates de sortie
      - tracklists
    avoid_for:
      - analyse esthétique autonome

  - id: RAG-S41-A097
    source_id: S41
    atom_id: S41-A097
    title: "Suicide au Russell Club : avant-garde minimale"
    chapters:
      - Chapitre 3
      - Chapitre 6
    tags:
      - suicide
      - russell-club
      - factory
      - ian-curtis
      - stephen-morris
    query_boost:
      - "all their songs sound like intros"
      - "Joy Division Suicide Russell Club 28 July 1978"
    use_for:
      - influences live
      - avant-garde minimale
    avoid_for:
      - causalité unique

  - id: RAG-S41-A098
    source_id: S41
    atom_id: S41-A098
    title: "Bradford : public National Front et réception dangereuse"
    chapters:
      - Chapitre 5
      - Chapitre 6
      - Chapitre 11
    tags:
      - bradford
      - royal-standard
      - national-front
      - nazi-controversy
      - live-danger
    query_boost:
      - "We had to pretend to be Nazis to get out alive"
      - "Royal Standard Bradford National Front Joy Division"
    use_for:
      - controverse nazie en situation live
      - réception politique dangereuse
    avoid_for:
      - littéralisation non croisée

  - id: RAG-S41-A099
    source_id: S41
    atom_id: S41-A099
    title: "Granada Reports : Shadowplay et World in Action"
    chapters:
      - Chapitre 5
      - Chapitre 14
    tags:
      - granada-reports
      - shadowplay
      - world-in-action
      - curtis-dancing
      - television
    query_boost:
      - "they thought we were boring to look at"
      - "Shadowplay World in Action offcuts Granada Reports"
    use_for:
      - télévision et image scénique
      - naissance médiatisée du geste Curtis
    avoid_for:
      - causalité directe sur la danse

  - id: RAG-S41-A100
    source_id: S41
    atom_id: S41-A100
    title: "Rock Against Racism et Factory FAC 3"
    chapters:
      - Chapitre 5
      - Chapitre 6
      - Chapitre 14
    tags:
      - rock-against-racism
      - kellys
      - cabaret-voltaire
      - fac-3
      - factory
    query_boost:
      - "This was in aid of a great cause We were proud to support it"
      - "Joy Division Rock Against Racism Kelly's Cabaret Voltaire FAC 3"
    use_for:
      - contrepoint antifasciste
      - montée Factory
    avoid_for:
      - absolution totale de la controverse

  - id: RAG-S41-A101
    source_id: S41
    atom_id: S41-A101
    title: "Brunel et Bristol : violence de tournée corroborée"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - brunel
      - bristol-locarno
      - spitting
      - mickey-bradley
      - tour
    query_boost:
      - "I see you are not educated down south"
      - "Locarno Bristol No room on the bill for Joy Division"
    use_for:
      - corroboration externe de tournée
      - violence live et éviction
    avoid_for:
      - preuve exhaustive

  - id: RAG-S41-A103
    source_id: S41
    atom_id: S41-A103
    title: "Hope & Anchor : review Sounds et anti-consécration"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - hope-and-anchor
      - sounds
      - nick-tester
      - london
      - poise-than-pose
    query_boost:
      - "poise than pose"
      - "Joy Division were grim but I grinned Nick Tester"
    use_for:
      - réception londonienne négative
      - anti-consécration
    avoid_for:
      - verdict définitif sur le groupe
```
