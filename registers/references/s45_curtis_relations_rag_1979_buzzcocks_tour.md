# S45 — Relations stabilisées et entrées RAG — tournée Buzzcocks, Futurama, Mountford Hall

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A102-CONCEPT-019
    source: S45-A102
    type: prolonge
    cible: CONCEPT-019
    justification: >
      Le passage confirme que l’état de Curtis dépend d’un faisceau : sommeil, travail, tournée, surveillance du groupe, traitement et fatigue.

  - id: REL-S45-A103-CONCEPT-023
    source: S45-A103
    type: nuance
    cible: CONCEPT-023
    justification: >
      Après le travail féminin effacé, la tournée révèle aussi une division matérielle du travail entre les membres masculins.

  - id: REL-S45-A104-CONCEPT-023
    source: S45-A104
    type: prolonge
    cible: CONCEPT-023
    justification: >
      Deborah corrige une mémoire secondaire qui attribue à tort une présence des épouses et compagnes à Futurama.

  - id: REL-S45-A105-CONCEPT-019
    source: S45-A105
    type: prolonge
    cible: CONCEPT-019
    justification: >
      La crise avant scène montre que la maladie n’est pas seulement domestique : elle intervient dans la logistique live.

  - id: REL-S45-A106-S45-A102
    source: S45-A106
    type: prolonge
    cible: S45-A102
    justification: >
      Mountford Hall donne sa première forme spectaculaire au seuil professionnel ouvert par la tournée Buzzcocks.

  - id: REL-S45-A107-S45-A098
    source: S45-A107
    type: prolonge
    cible: S45-A098
    justification: >
      La réception live contredit l’effort de résistance à la formule « Ian Curtis and Joy Division ».

  - id: REL-S45-A108-CONCEPT-018
    source: S45-A108
    type: prolonge
    cible: CONCEPT-018
    justification: >
      La politique affective du groupe trouve son envers domestique dans des rituels de langage et de sécurisation.

  - id: REL-S45-A108-RISQUE-PSYCHOLOGISATION
    source: S45-A108
    type: alerte
    cible: RISQUE-PSYCHOLOGISATION
    justification: >
      Le rituel téléphonique doit être décrit comme scène conjugale, non comme diagnostic.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A102
    source_id: S45
    atom_id: S45-A102
    title: "Buzzcocks tour : quitter le day job et collectiviser la maladie"
    chapters:
      - Chapitre 6
      - Chapitre 12
    tags:
      - buzzcocks-tour
      - day-job
      - epilepsy
      - professionalisation
      - group-care
    query_boost:
      - "give up the day job"
      - "Buzzcocks tour Ian Curtis day job"
      - "Joy Division September 1979 epilepsy fewer attacks"
    use_for:
      - professionnalisation de Joy Division
      - maladie collectivisée
      - articulation travail / tournée / santé
    avoid_for:
      - causalité médicale directe

  - id: RAG-S45-A104
    source_id: S45
    atom_id: S45-A104
    title: "Futurama ’79 : consécration live et correction de mémoire"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - futurama
      - leeds
      - ian-penman
      - mark-johnson
      - wives-girlfriends
    query_boost:
      - "Futurama 79 real stars of the night"
      - "Mark Johnson wives girlfriends Joy Division Futurama"
    use_for:
      - réception live
      - correction historiographique
      - absence des compagnes
    avoid_for:
      - citation non vérifiée sans source originale

  - id: RAG-S45-A106
    source_id: S45
    atom_id: S45-A106
    title: "Mountford Hall : Joy Division déborde le rôle de support band"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - mountford-hall
      - buzzcocks
      - penny-riley
      - live-reception
      - support-band
    query_boost:
      - "music to surrender to"
      - "Mountford Hall Joy Division Buzzcocks Penny Riley"
    use_for:
      - renversement hiérarchique live
      - support act conquérant
    avoid_for:
      - généralisation à toute la tournée sans recoupement

  - id: RAG-S45-A107
    source_id: S45
    atom_id: S45-A107
    title: "Curtis star malgré le collectif"
    chapters:
      - Chapitre 6
      - Chapitre 14
    tags:
      - ian-curtis
      - starification
      - body
      - live-performance
      - reception
    query_boost:
      - "Ian symbolizes Joy Division"
      - "Des Moines Ian Curtis symbolizes Joy Division"
    use_for:
      - starification corporelle
      - tension Curtis / collectif
    avoid_for:
      - réduction de Joy Division à Curtis

  - id: RAG-S45-A108
    source_id: S45
    atom_id: S45-A108
    title: "Rituels téléphoniques et langage conjugal"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - deborah-curtis
      - telephone
      - ritual
      - intimacy
      - psychologisation-risk
    query_boost:
      - "obsessive insurance against anything going wrong between us"
      - "Any deviation and Ian would begin the whole process again"
    use_for:
      - intimité conjugale
      - langage ritualisé
      - contrôle affectif
    avoid_for:
      - diagnostic psychologique rétrospectif
```
