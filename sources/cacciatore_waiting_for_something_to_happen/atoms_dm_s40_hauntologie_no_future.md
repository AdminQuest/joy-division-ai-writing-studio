# S40 — Atomes document maître — Cacciatore, « ...waiting for something to happen... », 2021

Ce fichier réinjecte S40 dans le flux effectivement lu par `tools/build_registers.py`, puis par `tools/build_master_docs.py`. Les fichiers JSON et les addenda demeurent utiles pour le RAG et la documentation de passe, mais les blocs YAML ci-dessous sont ceux qui alimentent les documents maîtres.

## S40-A001 — S40 comme article philosophico-esthétique, non source primaire

```yaml
id: S40-A001
type_unite: prudence_methodologique
titre: "S40 comme article philosophico-esthétique, non source primaire"
source_id: S40
resume: >
  S40 doit être utilisé comme source de réception et d’interprétation, non comme preuve historique première. Cacciatore propose une lecture philosophique et critique de la persistance de Joy Division ; il ne documente pas directement les faits de production du groupe.
role_argumentatif:
  - "Fixer le statut documentaire de S40 avant toute mobilisation théorique."
niveau_preuve:
  statut: source secondaire critique
  confiance: moyenne-forte comme interprétation ; faible comme preuve factuelle directe
importance:
  niveau: critique
risque_surinterpretation:
  niveau: élevé
  raison: "Risque de convertir S40 en clé totale ou en preuve historique."
motifs:
  - prudence anti-téléologique
  - séparation production-réception
concepts_derives:
  - hauntologie
  - réception posthume
relations:
  - type: garde_fou
    cible: REL-S40-001
usage_livre:
  - Chapitre 1
  - Chapitre 11
  - Chapitre 14
```

## S40-A002 — Le past inside the present : survivance spectrale du passé

```yaml
id: S40-A002
type_unite: concept_structurant
titre: "Le past inside the present : survivance spectrale du passé"
source_id: S40
resume: >
  Cacciatore évoque des « sampler viventi » obsédés par le past inside the present. Le passé Joy Division ne revient pas comme simple nostalgie ; il persiste dans le présent sous forme de spectres, de traces et de réactivations médiatiques.
role_argumentatif:
  - "Décrire la persistance du passé dans le présent comme structure de réception."
niveau_preuve:
  statut: source secondaire critique
  confiance: moyenne-forte
importance:
  niveau: majeure
risque_surinterpretation:
  niveau: moyen
  raison: "Ne pas confondre survivance spectrale et influence documentée."
motifs:
  - spectres
  - passé persistant
  - archive réactivée
concepts_derives:
  - past inside the present
  - survivance spectrale
relations:
  - type: prolonge
    cible: REL-S40-002
usage_livre:
  - Chapitre 14
```

## S40-A003 — No future et capitalisme globalisé : du cri punk à l’impossibilité contemporaine

```yaml
id: S40-A003
type_unite: concept_structurant
titre: "No future et capitalisme globalisé : du cri punk à l’impossibilité contemporaine"
source_id: S40
resume: >
  Le no future n’est plus seulement un mot d’ordre punk ; il devient, dans la lecture de Cacciatore, une impossibilité contemporaine d’ouvrir un monde possible. Cette lecture doit être maniée comme interprétation critique, non comme théorie explicite de Joy Division.
role_argumentatif:
  - "Relier le no future punk à une condition contemporaine où l’avenir cesse d’être opératoire."
niveau_preuve:
  statut: source secondaire critique
  confiance: moyenne-forte comme interprétation critique
importance:
  niveau: critique
risque_surinterpretation:
  niveau: moyen
  raison: "Éviter de faire du punk ou de Joy Division une théorie constituée du capitalisme globalisé."
motifs:
  - no future
  - futur fermé
concepts_derives:
  - capitalisme globalisé
  - impossibilité d’un monde possible
relations:
  - type: prolonge
    cible: REL-S40-003
usage_livre:
  - Chapitre 11
  - Chapitre 14
```

## S40-A004 — La lente cancellazione del futuro : diagnostic et risque de clôture

```yaml
id: S40-A004
type_unite: concept_critique
titre: "La lente cancellazione del futuro : diagnostic et risque de clôture"
source_id: S40
resume: >
  La perte du futur est un outil critique puissant, mais Cacciatore invite à ne pas figer l’avenir dans le seul registre de sa disparition. Cette prudence évite de transformer l’hauntologie en fatalisme narratif.
role_argumentatif:
  - "Introduire une prudence interne à la théorie du futur perdu."
niveau_preuve:
  statut: source secondaire critique
  confiance: moyenne-forte
importance:
  niveau: majeure
risque_surinterpretation:
  niveau: élevé
  raison: "La disparition du futur ne doit pas devenir une formule automatique."
motifs:
  - diagnostic critique
  - futur perdu
concepts_derives:
  - lente cancellazione del futuro
  - indétermination de l’avenir
relations:
  - type: nuance
    cible: REL-S40-007
usage_livre:
  - Chapitre 11
  - Chapitre 14
```

## S40-A005 — L’attente sans horizon stable : structure temporelle du titre

```yaml
id: S40-A005
type_unite: motif_majeur
titre: "L’attente sans horizon stable : structure temporelle du titre"
source_id: S40
resume: >
  L’attente n’est pas ici espérance ; elle est suspension, veille, impossibilité de voir venir l’avenir. Cette structure temporelle donne sa force au titre de l’article : « ...waiting for something to happen... ».
role_argumentatif:
  - "Faire de l’attente le nœud temporel de S40."
niveau_preuve:
  statut: lecture critique du passage
  confiance: forte
importance:
  niveau: critique
risque_surinterpretation:
  niveau: moyen
  raison: "Ne pas réduire toutes les chansons de Joy Division à l’attente."
motifs:
  - waiting
  - suspension
  - avenir invisible
concepts_derives:
  - attente sans horizon stable
  - horizon d’attente
relations:
  - type: structure
    cible: REL-S40-004
usage_livre:
  - Chapitre 11
```

## S40-A006 — Joy Division et les spectres : corpus clos, présence persistante

```yaml
id: S40-A006
type_unite: lecture_reception
titre: "Joy Division et les spectres : corpus clos, présence persistante"
source_id: S40
resume: >
  Joy Division devient un objet spectral parce que son corpus clos continue d’agir dans le présent comme trace, symptôme et appel d’un futur non accompli. Cette survivance doit être distinguée d’une influence directe documentée.
role_argumentatif:
  - "Définir Joy Division comme objet de survivance plus que comme nostalgie simple."
niveau_preuve:
  statut: source secondaire critique
  confiance: moyenne-forte
importance:
  niveau: critique
risque_surinterpretation:
  niveau: moyen
  raison: "Ne pas confondre spectre et fait d’influence directe."
motifs:
  - revenance
  - héritage spectral
  - présence après-coup
concepts_derives:
  - spectres
  - corpus clos
  - présence posthume
relations:
  - type: prolonge
    cible: REL-S40-005
usage_livre:
  - Chapitre 14
```

## S40-A007 — Futur perdu : outil de réception, non preuve historique

```yaml
id: S40-A007
type_unite: prudence_conceptuelle
titre: "Futur perdu : outil de réception, non preuve historique"
source_id: S40
resume: >
  Le futur perdu permet de lire la résonance contemporaine de Joy Division ; il ne prouve pas que le groupe aurait consciemment théorisé cette condition. Le concept doit rester un outil de réception, non une causalité historique.
role_argumentatif:
  - "Empêcher la conversion du concept de futur perdu en causalité historique."
niveau_preuve:
  statut: garde-fou méthodologique
  confiance: forte
importance:
  niveau: majeure
risque_surinterpretation:
  niveau: élevé
  raison: "Risque d’attribuer le futur perdu directement à Curtis ou au groupe."
motifs:
  - futur perdu
  - prudence anti-anachronique
concepts_derives:
  - réception posthume
  - non-accomplissement
relations:
  - type: garde_fou
    cible: REL-S40-006
usage_livre:
  - Chapitre 1
  - Chapitre 11
  - Chapitre 14
```

## S40-A008 — Garde-fou : l’hauntologie ne doit pas devenir une téléologie Joy Division

```yaml
id: S40-A008
type_unite: prudence_methodologique
titre: "Garde-fou : l’hauntologie ne doit pas devenir une téléologie Joy Division"
source_id: S40
resume: >
  L’hauntologie doit ouvrir une analyse des temporalités, non enfermer Joy Division dans une prophétie rétrospective. S40 contient donc un garde-fou contre les lectures qui feraient du groupe un annonciateur direct de Fisher, Derrida ou Bifo.
role_argumentatif:
  - "Prévenir la lecture prophétique de Joy Division."
niveau_preuve:
  statut: règle d’usage historiographique
  confiance: forte
importance:
  niveau: critique
risque_surinterpretation:
  niveau: très élevé
  raison: "L’hauntologie devient dangereuse si elle fonctionne comme clé totale."
motifs:
  - anti-prophétie
  - anti-mythe
  - médiation critique
concepts_derives:
  - hauntologie
  - téléologie
relations:
  - type: garde_fou
    cible: REL-S40-007
usage_livre:
  - Chapitre 1
  - Chapitre 11
  - Chapitre 14
```
