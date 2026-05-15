# S41 — Relations stabilisées et entrées RAG — Moonlight, Rainbow, Bury, Derby, divorce

## Relations stabilisées

```yaml
relations:
  - id: REL-S41-A190-CONCEPT-147
    source: S41-A190
    type: prolonge
    cible: CONCEPT-147
    justification: >
      Les dates du Moonlight et du Rainbow sont prises dans l’horizon économique et symbolique de la tournée américaine.

  - id: REL-S41-A191-CONCEPT-148
    source: S41-A191
    type: prolonge
    cible: CONCEPT-148
    justification: >
      Le regard du Captain de Polydor signale une reconnaissance industrielle forte, sans bascule major immédiate.

  - id: REL-S41-A192-CONCEPT-139
    source: S41-A192
    type: prolonge
    cible: CONCEPT-139
    justification: >
      Le contraste entre le rig de Burnel et l’équipement de Hook rend visible le succès sans star-system ni moyens équivalents.

  - id: REL-S41-A193-CONCEPT-137
    source: S41-A193
    type: prolonge
    cible: CONCEPT-137
    justification: >
      La crise du Rainbow et l’insistance de Curtis à jouer ensuite prolongent la logique de continuation malgré danger.

  - id: REL-S41-A194-CONCEPT-149
    source: S41-A194
    type: prolonge
    cible: CONCEPT-149
    justification: >
      Hook formule explicitement que Bury aurait dû être annulé, tout en laissant incertaines les raisons du maintien.

  - id: REL-S41-A195-CONCEPT-133
    source: S41-A195
    type: prolonge
    cible: CONCEPT-133
    justification: >
      La gestion de Bury par guest list et improvisation prolonge les limites de l’économie Factory bricolée.

  - id: REL-S41-A196-CONCEPT-150
    source: S41-A196
    type: prolonge
    cible: CONCEPT-150
    justification: >
      Le sang de Twinny sur la chemise de Hook, lavé à l’eau salée par sa mère, fait rentrer la violence live dans la domesticité.

  - id: REL-S41-A197-CONCEPT-109
    source: S41-A197
    type: prolonge
    cible: CONCEPT-109
    justification: >
      Hook retenu physiquement en loge illustre une solidarité masculine violente que l’entourage doit contenir.

  - id: REL-S41-A198-CONCEPT-131
    source: S41-A198
    type: prolonge
    cible: CONCEPT-131
    justification: >
      Le refuge chez Tony et Lindsay Wilson suspend provisoirement la crise sans reconfigurer durablement le système.

  - id: REL-S41-A199-CONCEPT-151
    source: S41-A199
    type: prolonge
    cible: CONCEPT-151
    justification: >
      Factory II devient lieu où Deborah apprend des informations sur Annik et les sessions Closer.

  - id: REL-S41-A200-CONCEPT-152
    source: S41-A200
    type: prolonge
    cible: CONCEPT-152
    justification: >
      L’appel de Deborah à Annik et la mention du co-respondent déplacent la crise intime vers le registre juridique.
```

## Entrées RAG candidates

```yaml
rag_index:
  - id: RAG-S41-A190
    source_id: S41
    atom_id: S41-A190
    title: "Moonlight / Rainbow : concerts de financement sous crise"
    chapters: [Chapitre 6, Chapitre 8, Chapitre 12]
    tags: [moonlight-club, rainbow-theatre, america-tour, april-1980, funds]
    query_boost:
      - "With the American tour due to begin on 21 May"
      - "Moonlight Club Rainbow Theatre American tour funds Joy Division"
    use_for: [préparation de l’Amérique, concerts sous pression médicale]
    avoid_for: [réduction économiciste]

  - id: RAG-S41-A191
    source_id: S41
    atom_id: S41-A191
    title: "Moonlight : Polydor et reconnaissance industrielle"
    chapters: [Chapitre 6, Chapitre 8, Chapitre 14]
    tags: [polydor, captain, moonlight-club, independent-group, industry]
    query_boost:
      - "the first independent group I’d seen who could take on the world"
      - "Captain Polydor Moonlight Joy Division independent group world"
    use_for: [réception industrielle, aura live pré-américaine]
    avoid_for: [trajectoire major contrefactuelle]

  - id: RAG-S41-A192
    source_id: S41
    atom_id: S41-A192
    title: "Rainbow : Burnel, Stranglers crew et hiérarchie matérielle"
    chapters: [Chapitre 3, Chapitre 6]
    tags: [rainbow-theatre, jean-jacques-burnel, stranglers, bass-rig, soundcheck]
    query_boost:
      - "Jean-Jacques Burnel’s set-up"
      - "Stranglers crew Rainbow Theatre Hook bass rig sound-check"
    use_for: [hiérarchie matérielle live, basse et équipement]
    avoid_for: [anecdote matériel isolée]

  - id: RAG-S41-A193
    source_id: S41
    atom_id: S41-A193
    title: "Rainbow / Moonlight : crise et parole tenue"
    chapters: [Chapitre 12, Chapitre 6]
    tags: [rainbow-fit, moonlight, ian-curtis, man-of-his-word, epilepsy]
    query_boost:
      - "No mate no you’re not fucking going on again tonight"
      - "Rainbow fit Moonlight man of his word Ian Curtis"
    use_for: [sujet malade et agent, continuation malgré danger]
    avoid_for: [héroïsation du sacrifice]

  - id: RAG-S41-A194
    source_id: S41
    atom_id: S41-A194
    title: "Bury Town Hall : concert qui aurait dû être annulé"
    chapters: [Chapitre 12, Chapitre 6]
    tags: [bury-town-hall, cancelled, america-tour, rob-gretton, health]
    query_boost:
      - "We should have cancelled of course"
      - "Bury Town Hall should have cancelled American tour money penalties"
    use_for: [annulation impensée, culpabilité rétrospective]
    avoid_for: [preuve d’indifférence pure]

  - id: RAG-S41-A195
    source_id: S41
    atom_id: S41-A195
    title: "Bury riot : guest list et débordement"
    chapters: [Chapitre 6, Chapitre 12, Chapitre 14]
    tags: [bury-riot, guest-list, rob-gretton, factory, troublemakers]
    query_boost:
      - "the crowd were getting more and more rowdy"
      - "Bury guest list Rob troublemakers crowd rowdy"
    use_for: [gestion Factory sous contrainte, violence de salle]
    avoid_for: [responsabilité unique de Rob]

  - id: RAG-S41-A196
    source_id: S41
    atom_id: S41-A196
    title: "Twinny ensanglanté : chemise de Hook et eau salée"
    chapters: [Chapitre 6, Chapitre 12]
    tags: [twinny, blood, salt-water, shirt, bury]
    query_boost:
      - "his mum got the blood out by washing it in a bath of salt water"
      - "Twinny blood shirt salt water Hook Bury"
    use_for: [violence qui rentre à la maison, domesticité du live]
    avoid_for: [folklorisation du sang]

  - id: RAG-S41-A197
    source_id: S41
    atom_id: S41-A197
    title: "Hook retenu en loge : solidarité violente contenue"
    chapters: [Chapitre 6, Chapitre 12]
    tags: [hook-restrained, tony-wilson, lindsay, iris, section-25, bury]
    query_boost:
      - "we could have them if we all stuck together"
      - "Tony Lindsay Iris Paul Section 25 held Hook dressing room"
    use_for: [masculinité de tournée, violence contenue]
    avoid_for: [héroïsation de la riposte]

  - id: RAG-S41-A198
    source_id: S41
    atom_id: S41-A198
    title: "Tony et Lindsay Wilson : refuge après Bury"
    chapters: [Chapitre 12, Chapitre 14]
    tags: [tony-wilson, lindsay-wilson, refuge, records, dope, bury]
    query_boost:
      - "spent a few days listening to records and smoking dope"
      - "Ian stayed with Tony and Lindsay Wilson after Bury"
    use_for: [soin informel après crise, refuge temporaire]
    avoid_for: [protection durable surestimée]

  - id: RAG-S41-A199
    source_id: S41
    atom_id: S41-A199
    title: "Factory II : Debbie apprend Annik"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [factory-ii, deborah-curtis, annik, closer, natalie-birthday]
    query_boost:
      - "learned more about Ian’s relationship with Annik"
      - "Factory II Debbie Annik Closer living arrangements Natalie birthday"
    use_for: [concert comme révélation domestique, crise conjugale]
    avoid_for: [jugement moral]

  - id: RAG-S41-A200
    source_id: S41
    atom_id: S41-A200
    title: "Derby et divorce : Annik co-respondent"
    chapters: [Chapitre 10, Chapitre 12]
    tags: [derby-ajanta, annik, deborah, co-respondent, divorce, rusholme]
    query_boost:
      - "she planned to divorce Ian and would be naming Annik as co-respondent"
      - "Derby Ajanta Rusholme Belgian embassy co-respondent"
    use_for: [domesticité judiciarisée, crise intime rendue publique]
    avoid_for: [cause unique du suicide]
```
