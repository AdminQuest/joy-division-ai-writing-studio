# S05 — Relations stabilisées et note RAG — maintien de l’ordre dans le Greater Manchester

```yaml
id: REL-RAG-S05-PUBLIC-ORDER-GREATER-MANCHESTER-V2
source_id: S05
source_label: "S05 — Jeffery, Tufail & Jackson, Policing and the Reproduction of Local Social Order, 2015"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S05-A001
  - S05-A002
  - S05-A003
  - S05-A004
  - S05-A005
  - S05-A006
  - S05-A007
  - S05-A008
  - S05-A009
  - S05-A010
  - S05-A011
  - S05-A012
  - S05-A013
chapitres:
  - Chapitre 1
chapitres_secondaires:
  - Chapitre 9
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S05. Il sert au RAG Studio pour articuler Manchester, police, ordre public, conflits politiques, racialisation, désindustrialisation, régénération et sécuritisation. S05 ne documente pas Joy Division directement ; il donne le cadre institutionnel et conflictuel dans lequel le Manchester de la fin des années 1970 et des années 1980 prend forme.

## Relations stabilisées

```yaml
relations:
  - source: S05-A001
    type: cree
    cible: CONCEPT-ORDRE-SOCIAL-LOCAL
    note: "La police est analysée comme institution de fabrication et reproduction de l’ordre social local."

  - source: S05-A001
    type: nuance
    cible: MYTH-POLICE-SIMPLE-REPRESSION
    note: "L’article insiste sur une fonction productive autant que répressive."

  - source: S05-A002
    type: cree
    cible: ORG-GREATER-MANCHESTER-POLICE
    note: "GMP est constituée en 1974 comme force métropolitaine dans un contexte de crise urbaine."

  - source: S05-A003
    type: prolonge
    cible: PERSONNE-JAMES-ANDERTON
    note: "Anderton structure le rapport entre conservatisme moral, police accountability et ordre local."

  - source: S05-A004
    type: cree
    cible: ORG-TACTICAL-AID-GROUP
    note: "La TAG est une force mobile et centralisée de maintien de l’ordre."

  - source: S05-A005
    type: prolonge
    cible: CONCEPT-ANTIFASCISME-MANCHESTER
    note: "Hyde et Bolton montrent le policing de la confrontation National Front / antifascistes."

  - source: S05-A006
    type: prolonge
    cible: EVENT-MOSS-SIDE-1981
    note: "Moss Side 1981 est situé dans les tensions racialisées de police-community relations."

  - source: S05-A007
    type: cree
    cible: EVENT-BATTLE-OF-BRITTAN-1985
    note: "La Battle of Brittan illustre l’affrontement entre contestation étudiante et GMP."

  - source: S05-A008
    type: prolonge
    cible: CONCEPT-POLICE-ACCOUNTABILITY-MANCHESTER
    note: "Le municipalisme de gauche tente de contester le pouvoir policier local."

  - source: S05-A009
    type: relie
    cible: PLACE-ORDSALL
    note: "Ordsall 1992 articule désindustrialisation, inner city, anti-police riot et gentrification."

  - source: S05-A010
    type: relie
    cible: PLACE-OLDHAM
    note: "Oldham 2001 est lu à travers racialisation, far right et discours de community cohesion."

  - source: S05-A011
    type: prolonge
    cible: CONCEPT-REGENERATION-SECURISEE
    note: "La régénération de Manchester suppose une sécuritisation de l’espace urbain attractif."

  - source: S05-A011
    type: relie
    cible: S02-A006
    note: "À croiser avec S02 sur la ville entrepreneuriale et la compétition territoriale."

  - source: S05-A012
    type: relie
    cible: PLACE-BARTON-MOSS
    note: "Barton Moss prolonge la question du maintien de l’ordre face aux protestations environnementales."

  - source: S05-A013
    type: prolonge
    cible: CONCEPT-MANCHESTER-CHAMP-DE-FORCES
    note: "Manchester doit être écrit comme champ de forces institutionnelles, urbaines et sociales."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 1 : contexte policier, politique et institutionnel de Manchester ; Anderton ; antifascisme ; Moss Side ; GMP."
    - "Chapitre 9 : ordre social local, géographie conflictuelle, police-community relations, sécuritisation."
    - "Chapitre 14 : arrière-plan de la ville régénérée, attractive et sécurisée."
  requetes_utiles:
    - "S05 Greater Manchester Police Anderton Tactical Aid Group"
    - "S05 National Front antifascism Hyde Bolton"
    - "S05 Moss Side 1981 racist policing"
    - "S05 Battle of Brittan police vigilantism"
    - "S05 Ordsall 1992 anti police riot deindustrialisation"
    - "S05 Oldham 2001 community cohesion far right"
    - "S05 regeneration securitisation Manchester policing"
  exclusions:
    - "Ne pas utiliser S05 comme source directe sur Joy Division."
    - "Ne pas citer les témoignages rapportés sans vérifier leur source secondaire d’origine."
    - "Ne pas réduire Anderton au folklore de God’s Cop."
    - "Ne pas confondre Moss Side, Ordsall, Oldham, Pendleton et Barton Moss."
```
