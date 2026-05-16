# S02 — Relations stabilisées et note RAG — Manchester, shrinking city, renouveau urbain

```yaml
id: REL-RAG-S02-MANCHESTER-SHRINKING-CITY-V2
source_id: S02
source_label: "S02 — Sueur, Villes du futur, futur des villes, 2011"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S02-A001
  - S02-A002
  - S02-A003
  - S02-A004
  - S02-A005
  - S02-A006
  - S02-A007
  - S02-A008
  - S02-A009
  - S02-A010
chapitres:
  - Chapitre 1
  - Chapitre 9
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S02. Il sert au RAG Studio comme carte de cadrage urbain : Manchester shrinking city, désindustrialisation, recomposition métropolitaine, politiques de régénération, cultures urbaines et limites sociales du modèle.

## Relations stabilisées

```yaml
relations:
  - source: S02-A001
    type: cree
    cible: CONCEPT-SHRINKING-CITY-MANCHESTER
    note: "Manchester est cadrée comme ville industrielle en contraction."

  - source: S02-A001
    type: prolonge
    cible: CHAPITRE-1
    note: "Cadrage urbain initial du Manchester de Joy Division."

  - source: S02-A002
    type: prolonge
    cible: CONCEPT-DESINDUSTRIALISATION-MANCHESTER
    note: "Le rétrécissement urbain est lié à la perte de base industrielle et d’emploi."

  - source: S02-A002
    type: relie
    cible: S01
    note: "À croiser avec Blakeley & Evans pour East Manchester et la base économique."

  - source: S02-A002
    type: relie
    cible: S04
    note: "À croiser avec Kidd pour l’histoire urbaine de Manchester."

  - source: S02-A003
    type: cree
    cible: RULE-DISTINGUER-CITY-GREATER-MANCHESTER
    note: "Tout usage statistique ou géographique doit préciser l’échelle."

  - source: S02-A004
    type: prolonge
    cible: CONCEPT-VILLE-RETRECIE-SYSTEME
    note: "La shrinking city désigne un système urbain déséquilibré, non une simple baisse de population."

  - source: S02-A005
    type: prolonge
    cible: CONCEPT-REGENERATION-URBAINE
    note: "La régénération est une réponse politique à la contraction urbaine."

  - source: S02-A006
    type: cree
    cible: CONCEPT-VILLE-ENTREPRENEURIALE-MANCHESTER
    note: "La relance mancunienne s’appuie sur partenariats, marketing et compétition métropolitaine."

  - source: S02-A007
    type: nuance
    cible: EVENT-IRA-1996-MANCHESTER
    note: "L’attentat accélère la recomposition du centre-ville sans constituer une cause unique."

  - source: S02-A008
    type: relie
    cible: PLACE-HULME
    note: "Hulme est un laboratoire urbain à croiser avec les sources spécialisées."

  - source: S02-A009
    type: prolonge
    cible: CONCEPT-REGENERATION-SYMBOLIQUE
    note: "La culture populaire participe à la transformation de l’image de Manchester."

  - source: S02-A009
    type: relie
    cible: S69-A029
    note: "À croiser avec le documentaire Grant Gee comme récit de mémoire urbaine."

  - source: S02-A010
    type: nuance
    cible: MYTH-MANCHESTER-RENAISSANCE-HOMOGENE
    note: "La régénération n’efface pas les inégalités ni les fractures héritées de la désindustrialisation."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 1 : cadre urbain de Manchester avant et autour de la formation de Joy Division."
    - "Chapitre 9 : mémoire urbaine, shrinking city, régénération et récit de la ville."
    - "Chapitre 14 : patrimonialisation culturelle et conversion de l’image post-industrielle en ressource symbolique."
  requetes_utiles:
    - "S02 Manchester shrinking city désindustrialisation"
    - "S02 Manchester régénération urbaine ville entrepreneuriale"
    - "S02 Greater Manchester échelle urbaine prudence"
    - "S02 Hulme renouvellement urbain"
    - "S02 Factory Records Hacienda régénération symbolique Manchester"
  exclusions:
    - "Ne pas utiliser S02 pour établir les faits internes de Joy Division."
    - "Ne pas atomiser le reste du rapport sauf besoin spécifique sur les villes du futur."
    - "Ne pas citer les chiffres sans recoupement par sources urbaines spécialisées."
```
