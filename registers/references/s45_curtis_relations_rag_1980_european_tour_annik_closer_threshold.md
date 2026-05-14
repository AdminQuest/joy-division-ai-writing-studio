# S45 — Relations stabilisées et entrées RAG — tournée européenne, Annik, foyer et seuil Closer

## Relations stabilisées

```yaml
relations:
  - id: REL-S45-A119-CONCEPT-033
    source: S45-A119
    type: prolonge
    cible: CONCEPT-033
    justification: >
      La séparation conjugale se formule d’abord en projet immobilier et en possible partage d’equity.

  - id: REL-S45-A120-CONCEPT-034
    source: S45-A120
    type: prolonge
    cible: CONCEPT-034
    justification: >
      La présence d’Annik sur la tournée européenne contredit la règle d’exclusion des wives and girlfriends.

  - id: REL-S45-A121-CONCEPT-035
    source: S45-A121
    type: prolonge
    cible: CONCEPT-035
    justification: >
      L’épisode Pernod / Bible / Revelation produit des lectures concurrentes sans intention stabilisable.

  - id: REL-S45-A122-CONCEPT-026
    source: S45-A122
    type: prolonge
    cible: CONCEPT-026
    justification: >
      La professionnalisation sous surveillance médicale échoue à produire un vrai repos ; le calendrier reprend la main.

  - id: REL-S45-A123-CONCEPT-029
    source: S45-A123
    type: prolonge
    cible: CONCEPT-029
    justification: >
      Le désamour devient parole explicite, mais sans résolution de la crise conjugale.

  - id: REL-S45-A124-MOTIF-038
    source: S45-A124
    type: prolonge
    cible: MOTIF-038
    justification: >
      Franck Essner passe du fandom transnational à l’intimité de Barton Street.

  - id: REL-S45-A125-CONCEPT-034
    source: S45-A125
    type: prolonge
    cible: CONCEPT-034
    justification: >
      La contradiction genrée devient économique : Deborah finance à crédit tandis que les frais d’Annik sont intégrés à la tournée.

  - id: REL-S45-A126-MOTIF-034
    source: S45-A126
    type: prolonge
    cible: MOTIF-034
    justification: >
      Le New Osbourne Club prolonge la loge comme espace de vérité cachée et d’exclusion de Deborah.

  - id: REL-S45-A127-CONCEPT-029
    source: S45-A127
    type: prolonge
    cible: CONCEPT-029
    justification: >
      La vérité conjugale différée devient preuve matérielle : nom et adresse d’Annik.

  - id: REL-S45-A128-S45-A127
    source: S45-A128
    type: prolonge
    cible: S45-A127
    justification: >
      La preuve écrite devient confrontation et aveu.

  - id: REL-S45-A129-CONCEPT-035
    source: S45-A129
    type: prolonge
    cible: CONCEPT-035
    justification: >
      Les pseudo-crises possibles doivent rester un symptôme indécidable, non un diagnostic de simulation.

  - id: REL-S45-A130-CONCEPT-033
    source: S45-A130
    type: prolonge
    cible: CONCEPT-033
    justification: >
      Facture d’électricité, alliance, Candy et vêtements de scène matérialisent la séparation non dite.

  - id: REL-S45-A131-CONCEPT-021
    source: S45-A131
    type: prolonge
    cible: CONCEPT-021
    justification: >
      La paternité empêchée transforme le double care en care triangulaire autour de Natalie.

  - id: REL-S45-A132-CONCEPT-036
    source: S45-A132
    type: prolonge
    cible: CONCEPT-036
    justification: >
      Les sessions de Closer deviennent un studio de dissociation domestique : Deborah exclue, Annik présente, femmes périphériques.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S45-A119
    source_id: S45
    atom_id: S45-A119
    title: "Barton Street à vendre : séparation matérielle avant séparation dite"
    chapters:
      - Chapitre 10
    tags:
      - barton-street
      - house-sale
      - equity
      - separation
      - deborah-curtis
    query_boost:
      - "he wasn’t intending to move into the flat with me"
      - "Barton Street sell the house equity Deborah Curtis"
    use_for:
      - séparation matérielle
      - rupture conjugale non dite
    avoid_for:
      - preuve juridique d’un plan conscient

  - id: RAG-S45-A120
    source_id: S45
    atom_id: S45-A120
    title: "Tournée européenne : Annik comme exception à la no women policy"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - european-tour
      - annik-honore
      - no-women-policy
      - deborah-curtis
      - touring
    query_boost:
      - "setting the scene for taking Annik on tour"
      - "Annik European tour Joy Division wives girlfriends"
    use_for:
      - contradiction genrée de tournée
      - crise conjugale et tournée
    avoid_for:
      - causalité romantique unique

  - id: RAG-S45-A121
    source_id: S45
    atom_id: S45-A121
    title: "Pernod, Bible et Revelation : scène à lectures concurrentes"
    chapters:
      - Chapitre 10
      - Chapitre 12
    tags:
      - bible
      - revelation
      - jezebel
      - pernod
      - self-harm
      - stephen-morris
    query_boost:
      - "The Bible was still open"
      - "Jezebel Revelation Ian Curtis Pernod"
    use_for:
      - scènes sensibles et herméneutique domestique
      - prudence sur intention suicidaire ou religieuse
    avoid_for:
      - prophétie religieuse
      - signe suicidaire univoque

  - id: RAG-S45-A127
    source_id: S45
    atom_id: S45-A127
    title: "Découverte de l’adresse d’Annik"
    chapters:
      - Chapitre 10
    tags:
      - annik-honore
      - delvino-road
      - notebooks
      - domestic-evidence
      - deborah-curtis
    query_boost:
      - "I found the name Annik Honoré and her address"
      - "Delvino Road London Annik Honore"
    use_for:
      - preuve domestique de l’infidélité
      - vérité conjugale différée
    avoid_for:
      - extension non sourcée de la relation

  - id: RAG-S45-A129
    source_id: S45
    atom_id: S45-A129
    title: "Pseudo-crises possibles : symptôme indécidable"
    chapters:
      - Chapitre 12
      - Chapitre 10
    tags:
      - pseudo-seizures
      - epilepsy
      - medical-caution
      - deborah-curtis
      - manipulation
    query_boost:
      - "Pseudo-seizures can be feigned either consciously or subconsciously"
      - "Ian Curtis pseudo seizures Deborah Curtis"
    use_for:
      - prudence médicale et probatoire
      - non-monocausalité
    avoid_for:
      - diagnostic de simulation

  - id: RAG-S45-A130
    source_id: S45
    atom_id: S45-A130
    title: "Red electricity bill, alliance et départ de Candy"
    chapters:
      - Chapitre 10
    tags:
      - red-electricity-bill
      - candy
      - wedding-ring
      - domestic-economy
      - deborah-curtis
    query_boost:
      - "red electricity bill came there was no money to pay for it"
      - "Candy farm Rochdale Deborah Curtis"
    use_for:
      - effondrement matériel du foyer
      - professionnalisation financée par le foyer
    avoid_for:
      - plainte financière isolée

  - id: RAG-S45-A132
    source_id: S45
    atom_id: S45-A132
    title: "Closer à Britannia Row : invitation formelle, exclusion pratique"
    chapters:
      - Chapitre 3
      - Chapitre 8
      - Chapitre 10
      - Chapitre 12
    tags:
      - closer
      - britannia-row
      - annik-honore
      - wives-girlfriends
      - studio
      - deborah-curtis
    query_boost:
      - "Annik managed to remain concealed for the first day"
      - "Closer Britannia Row £20 wives girlfriends"
    use_for:
      - studio comme dissociation domestique
      - contexte de Closer
    avoid_for:
      - causalité esthétique totale de la crise intime
```
