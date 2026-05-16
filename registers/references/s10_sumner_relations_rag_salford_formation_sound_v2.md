# S10 — Relations stabilisées et note RAG — Sumner, Salford, formation et son Joy Division

```yaml
id: REL-RAG-S10-SUMNER-SALFORD-FORMATION-SOUND-V2
source_id: S10
source_label: "S10 — Sumner, Chapter and Verse, 2014/2015"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S10-A001
  - S10-A002
  - S10-A003
  - S10-A004
  - S10-A005
  - S10-A006
  - S10-A007
  - S10-A008
  - S10-A009
  - S10-A010
  - S10-A011
  - S10-A012
  - S10-A013
  - S10-A014
  - S10-A015
  - S10-A016
  - S10-A017
  - S10-A018
  - S10-A019
  - S10-A020
  - S10-A021
  - S10-A022
  - S10-A023
  - S10-A024
  - S10-A025
chapitres:
  - Chapitre 1
  - Chapitre 2
  - Chapitre 3
  - Chapitre 4
  - Chapitre 5
  - Chapitre 9
  - Chapitre 10
chapitres_secondaires:
  - Chapitre 12
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S10. Il sert au RAG Studio pour articuler Salford, mémoire ouvrière, destruction urbaine, formation de Warsaw / Joy Division, punk, Factory, studio, composition collective et crise Curtis. S10 est une source primaire rétrospective : elle doit toujours être croisée avec S41, S45, S75, S76 et les sources secondaires.

## Relations stabilisées

```yaml
relations:
  - source: S10-A001
    type: prolonge
    cible: CONCEPT-SALFORD-COMMUNAUTE-OUVRIERE
    note: "Alfred Street est décrit comme communauté ouvrière vécue."

  - source: S10-A002
    type: prolonge
    cible: CONCEPT-PAYSAGE-INDUSTRIEL-SENSORIEL
    note: "L’industrie est mémorisée par odeurs, air, usines, prison et proximité de l’Irwell."

  - source: S10-A003
    type: relie
    cible: S20-A007
    note: "À croiser avec S20 sur relogement et perte de sociabilité dans les solutions de logement."

  - source: S10-A004
    type: cree
    cible: MOTIF-MORT-COMMUNAUTE-ALFRED-STREET
    note: "La clearance d’Alfred Street devient scène de destruction communautaire."

  - source: S10-A005
    type: cree
    cible: MOTIF-ORDSALL-STREETLIGHTS-MATRICE-SONORE
    note: "La scène des lampadaires au sodium fonde une mémoire du son froid et industriel."

  - source: S10-A006
    type: cree
    cible: CONCEPT-HUMILIATION-INSTITUTIONNELLE-CREATION
    note: "École et administration produisent l’impasse que la musique dépasse."

  - source: S10-A007
    type: relie
    cible: PERSONNE-PETER-HOOK
    note: "La rencontre avec Hook est située dans la sociabilité du fond de classe."

  - source: S10-A008
    type: prolonge
    cible: CONCEPT-SOCIABILITE-MUSICALE-ADOLESCENTE
    note: "Le youth club expose Sumner et Hook à des styles musicaux croisés."

  - source: S10-A009
    type: cree
    cible: CONCEPT-ESPACE-SONORE-MORRICONE
    note: "Morricone donne un modèle d’espace, silence et tension sonore."

  - source: S10-A010
    type: nuance
    cible: MYTH-LESSER-FREE-TRADE-HALL-EPIPHANIE-ABSOLUE
    note: "Sumner confirme l’impact du concert, mais en limite le récit miraculeux."

  - source: S10-A011
    type: cree
    cible: CONCEPT-PUNK-AUTORISATION-SOCIALE
    note: "Punk autorise les working-class misfits à créer sans virtuosité."

  - source: S10-A012
    type: prolonge
    cible: CONCEPT-BRICOLAGE-TECHNIQUE-SONORE
    note: "Le vieux gramophone amplifié matérialise le bricolage initial."

  - source: S10-A013
    type: prolonge
    cible: PERSONNE-IAN-CURTIS
    note: "Le recrutement de Curtis passe par Virgin Records et l’identification scène punk."

  - source: S10-A014
    type: prolonge
    cible: PERSONNE-STEPHEN-MORRIS
    note: "Morris stabilise la formation par technique, tempérament et disponibilité matérielle."

  - source: S10-A015
    type: prolonge
    cible: EVENT-WARSAW-ELECTRIC-CIRCUS-1977
    note: "Premier concert comme apprentissage scénique, non révélation totale."

  - source: S10-A016
    type: prolonge
    cible: PERSONNE-ROB-GRETTON
    note: "Gretton est médiateur de professionnalisation et d’intégration Factory."

  - source: S10-A017
    type: relie
    cible: ORG-GRANADA-TELEVISION
    note: "Granada Reports donne à Shadowplay une visibilité télévisuelle locale."

  - source: S10-A018
    type: prolonge
    cible: EVENT-RCA-SESSIONS-1978
    note: "Les RCA sessions deviennent contre-modèle industriel."

  - source: S10-A019
    type: nuance
    cible: MYTH-JOY-DIVISION-IMAGERIE-NAZIE-INTENTION-POLITIQUE
    note: "Sumner décrit la provocation comme naïve et punk, sans sympathie nazie revendiquée."

  - source: S10-A020
    type: prolonge
    cible: CONCEPT-STUDIO-COMME-INSTRUMENT
    note: "Hannett fait comprendre à Sumner le studio comme espace créatif."

  - source: S10-A021
    type: tension
    cible: CONCEPT-VERITE-LIVE-VERITE-STUDIO
    note: "Unknown Pleasures transfigure le groupe au prix d’un déplacement du son live."

  - source: S10-A022
    type: cree
    cible: CONCEPT-COMPOSITION-QUATRE-POLES-JOY-DIVISION
    note: "Le processus combine basse, batterie, arrangement et paroles / intuition de Curtis."

  - source: S10-A023
    type: prolonge
    cible: SONG-LOVE-WILL-TEAR-US-APART
    note: "Genèse collective, riff, arrangement, paroles et postérité."

  - source: S10-A024
    type: prolonge
    cible: CONCEPT-CURTIS-EPILEPSIE-SCENE
    note: "Luton, diagnostic, traitements lourds et menace des crises sur scène."

  - source: S10-A025
    type: prolonge
    cible: CONCEPT-CURTIS-PRESSION-CLOSER
    note: "Bournemouth et whirlpool comme signes de pression psychique avancée."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 1 : Salford, Alfred Street, Ordsall, clearance, communauté ouvrière, paysage industriel."
    - "Chapitre 2 : formation Sumner / Hook, punk, Sex Pistols, apprentissage autodidacte, recrutement Curtis."
    - "Chapitre 3 : Rob Gretton, Factory, RCA, An Ideal for Living, Hannett, Unknown Pleasures."
    - "Chapitre 4 : composition collective, Love Will Tear Us Apart, Curtis, épilepsie, Closer."
    - "Chapitre 9 : géographie émotionnelle de Salford / Manchester."
    - "Chapitre 10 : crise Curtis et mémoire de la fin."
  requetes_utiles:
    - "S10 Alfred Street Salford community clearance"
    - "S10 Ordsall streetlights Joy Division sound"
    - "S10 Lesser Free Trade Hall Sex Pistols punk myth"
    - "S10 gramophone amplifier Hook Sumner guitar bass"
    - "S10 Ian Curtis recruitment Virgin Records"
    - "S10 Rob Gretton Rafters Factory"
    - "S10 An Ideal for Living Hitler Youth Bernard Albrecht"
    - "S10 Hannett studio as instrument Unknown Pleasures"
    - "S10 Love Will Tear Us Apart riff arrangement lyrics"
    - "S10 Curtis epilepsy Luton Closer Bournemouth"
  exclusions:
    - "Ne pas utiliser S10 seul pour arbitrer un conflit de mémoire."
    - "Ne pas citer longuement le texte sous copyright."
    - "Ne pas confondre Sumner avec Hook, Curtis ou Deborah Curtis comme points de vue."
```
