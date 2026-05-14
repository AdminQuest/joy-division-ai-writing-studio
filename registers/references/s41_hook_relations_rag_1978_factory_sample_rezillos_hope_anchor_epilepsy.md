# S41 — Relations stabilisées et entrées RAG — Factory Sample, tournée Rezillos/Undertones, Hope & Anchor, épilepsie

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A079-CONCEPT-076
    source: S41-A079
    type: prolonge
    cible: CONCEPT-076
    justification: >
      A Factory Sample fonctionne comme pacte de confiance avec Factory mais sans deal clair sur argent ou droits.

  - id: REL-S41-A080-CONCEPT-075
    source: S41-A080
    type: prolonge
    cible: CONCEPT-075
    justification: >
      Wilson légitime Joy Division par une relation culturelle et télévisuelle où Curtis devient son interlocuteur principal.

  - id: REL-S41-A081-CONCEPT-077
    source: S41-A081
    type: prolonge
    cible: CONCEPT-077
    justification: >
      Cargo Studios et John Brierley fournissent l’infrastructure technique qui rend possible la première réussite Hannett.

  - id: REL-S41-A082-CONCEPT-077
    source: S41-A082
    type: prolonge
    cible: CONCEPT-077
    justification: >
      Hannett exploite l’espace du groupe et sa naïveté technique comme matériau de production.

  - id: REL-S41-A083-S41-A079
    source: S41-A083
    type: prolonge
    cible: S41-A079
    justification: >
      « Digital » et « Glass » concrétisent le pacte Factory par une session qui donne au groupe son meilleur enregistrement jusque-là.

  - id: REL-S41-A084-CONCEPT-076
    source: S41-A084
    type: prolonge
    cible: CONCEPT-076
    justification: >
      L’objet Factory se fabrique par travail manuel et confiance, plus que par contrat industriel formalisé.

  - id: REL-S41-A085-CONCEPT-078
    source: S41-A085
    type: prolonge
    cible: CONCEPT-078
    justification: >
      Les lieux de concerts punk recoupent des zones de prostitution et de surveillance policière, rendant le Transit suspect.

  - id: REL-S41-A086-CONCEPT-071
    source: S41-A086
    type: prolonge
    cible: CONCEPT-071
    justification: >
      La tournée Rezillos / Undertones manifeste la professionnalisation concrète : dormir hors domicile, circuler, accepter des plateaux inadéquats.

  - id: REL-S41-A087-CONCEPT-079
    source: S41-A087
    type: prolonge
    cible: CONCEPT-079
    justification: >
      Brunel montre le concert comme interaction corporelle violente : crachats, coups, instrument défensif et arrêt du set.

  - id: REL-S41-A088-CONCEPT-079
    source: S41-A088
    type: prolonge
    cible: CONCEPT-079
    justification: >
      Le souvenir des Buzzcocks contextualise le crachat comme norme punk mais aussi comme limite corporelle.

  - id: REL-S41-A089-CONCEPT-074
    source: S41-A089
    type: prolonge
    cible: CONCEPT-074
    justification: >
      L’éviction de Bristol révèle la fragilité de la tournée et l’absence de protections contractuelles suffisantes.

  - id: REL-S41-A090-CONCEPT-080
    source: S41-A090
    type: prolonge
    cible: CONCEPT-080
    justification: >
      Le premier concert londonien n’est pas une consécration, mais un sous-sol froid, une mauvaise critique et une perte d’argent.

  - id: REL-S41-A091-CONCEPT-081
    source: S41-A091
    type: prolonge
    cible: CONCEPT-081
    justification: >
      La crise sur l’autoroute après le Hope & Anchor marque, pour Hook, le basculement vers une lecture médicale de Curtis.

  - id: REL-S41-A092-S41-A091
    source: S41-A092
    type: consolide
    cible: S41-A091
    justification: >
      Le diagnostic officiel de janvier 1979 verrouille la séquence médicale ouverte par la crise de l’autoroute.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A079
    source_id: S41
    atom_id: S41-A079
    title: "A Factory Sample : confiance sans contrat"
    chapters:
      - Chapitre 8
      - Chapitre 6
    tags:
      - a-factory-sample
      - digital
      - factory
      - contract
      - tony-wilson
    query_boost:
      - "Money never came into it"
      - "Digital Factory Sample limited 5000 copies"
    use_for:
      - idéalisme contractuel Factory
      - économie du sampler
    avoid_for:
      - jugement commercial anachronique

  - id: RAG-S41-A081
    source_id: S41
    atom_id: S41-A081
    title: "Cargo Studios : Brierley, Hannett et infrastructure sonore"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - cargo-studios
      - john-brierley
      - martin-hannett
      - digital
      - glass
    query_boost:
      - "the most famous punk studio in the North"
      - "Cargo Studios John Brierley Hannett Digital Glass"
    use_for:
      - infrastructure sonore Factory
      - studio local post-punk
    avoid_for:
      - décor studio sans fonction technique

  - id: RAG-S41-A083
    source_id: S41
    atom_id: S41-A083
    title: "Digital et Glass : première réussite Hannett"
    chapters:
      - Chapitre 3
      - Chapitre 8
    tags:
      - digital
      - glass
      - hannett
      - cargo
      - bass
    query_boost:
      - "easily our best recording up to that point"
      - "Digital bass is kicking it"
    use_for:
      - première réussite Hannett
      - ego instrumental de Hook
    avoid_for:
      - lecture uniquement depuis conflits ultérieurs

  - id: RAG-S41-A085
    source_id: S41
    atom_id: S41-A085
    title: "Transit bleu et Yorkshire Ripper"
    chapters:
      - Chapitre 6
      - Chapitre 13
    tags:
      - blue-transit
      - yorkshire-ripper
      - red-light-districts
      - police
      - gigs
    query_boost:
      - "you can consider yourself under investigation"
      - "blue transit red-light districts Joy Division Yorkshire Ripper"
    use_for:
      - géographie policière des gigs
      - marginalité urbaine des lieux live
    avoid_for:
      - sociologie policière générale

  - id: RAG-S41-A087
    source_id: S41
    atom_id: S41-A087
    title: "Brunel : crachats et basse comme arme"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - brunel
      - spitting
      - bass-as-weapon
      - ian-curtis
      - rezillos-tour
    query_boost:
      - "I started twatting them with my bass"
      - "Brunel spitting Ian Curtis Hondo bass"
    use_for:
      - violence corporelle live
      - protection physique du chanteur
    avoid_for:
      - folklore punk comique

  - id: RAG-S41-A090
    source_id: S41
    atom_id: S41-A090
    title: "Hope & Anchor : premier Londres désacralisé"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - hope-and-anchor
      - london
      - first-london-gig
      - bad-review
      - loss
    query_boost:
      - "Joy Division were grim but I grinned"
      - "Hope & Anchor first London gig Joy Division lost a quid"
    use_for:
      - anti-consécration londonienne
      - économie pauvre du live
    avoid_for:
      - reconnaissance nationale

  - id: RAG-S41-A091
    source_id: S41
    atom_id: S41-A091
    title: "M1 / Luton : première crise révélée"
    chapters:
      - Chapitre 12
      - Chapitre 6
    tags:
      - epilepsy
      - first-fit
      - hope-and-anchor
      - luton-and-dunstable
      - m1
    query_boost:
      - "There’s something wrong with Ian"
      - "Luton and Dunstable Hospital first fit Ian Curtis"
    use_for:
      - seuil médical post-Hope & Anchor
      - bascule vers épilepsie
    avoid_for:
      - relecture médicale totale du passé

  - id: RAG-S41-A092
    source_id: S41
    atom_id: S41-A092
    title: "Diagnostic d’épilepsie, 23 janvier 1979"
    chapters:
      - Chapitre 12
    tags:
      - epilepsy-diagnosis
      - macclesfield
      - january-1979
      - timeline-three
    query_boost:
      - "officially diagnosed with epilepsy"
      - "23 January 1979 Macclesfield District and General Hospital epilepsy"
    use_for:
      - chronologie médicale
      - verrouillage clinique
    avoid_for:
      - diagnostic rétroactif généralisé
```
