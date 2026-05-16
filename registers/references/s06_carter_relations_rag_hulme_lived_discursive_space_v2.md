# S06 — Relations stabilisées et note RAG — Hulme, espace vécu et espace discursif

```yaml
id: REL-RAG-S06-HULME-LIVED-DISCURSIVE-SPACE-V2
source_id: S06
source_label: "S06 — Carter, Youth, race and the inner-city estate, 2021/2023"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S06-A001
  - S06-A002
  - S06-A003
  - S06-A004
  - S06-A005
  - S06-A006
  - S06-A007
  - S06-A008
  - S06-A009
  - S06-A010
  - S06-A011
  - S06-A012
chapitres:
  - Chapitre 1
  - Chapitre 9
chapitres_secondaires:
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S06. Il sert au RAG Studio pour articuler Hulme, inner-city estate, jeunesse, race, stigmatisation territoriale, oral history et récits d’habitants. S06 ne documente pas Joy Division directement ; il protège l’écriture contre les clichés ruinistes et médiatiques de Hulme.

## Relations stabilisées

```yaml
relations:
  - source: S06-A001
    type: cree
    cible: CONCEPT-HULME-ESPACE-VECU-DISCURSIF
    note: "Hulme est un espace vécu par les habitants et construit par des discours publics."

  - source: S06-A001
    type: nuance
    cible: MYTH-HULME-PURE-RUINE-MODERNISTE
    note: "Le quartier ne doit pas être réduit à une image de ruine ou de crise."

  - source: S06-A002
    type: prolonge
    cible: PLACE-HULME-CRESCENTS
    note: "Les Crescents sont pris dans un récit de démolition et de renaissance familiale."

  - source: S06-A003
    type: cree
    cible: CONCEPT-INNER-CITY-CRISIS
    note: "Hulme est construit comme symptôme de l’inner-city crisis."

  - source: S06-A004
    type: cree
    cible: MOTIF-LEXIQUE-STIGMATISATION-HULME
    note: "Concrete jungle, ghetto et Bronx forment un lexique de territorial stigma."

  - source: S06-A005
    type: relie
    cible: CONCEPT-DECK-ACCESS-HOUSING
    note: "À croiser avec S20 sur les deck-access estates et les streets-in-the-sky."

  - source: S06-A006
    type: cree
    cible: CONCEPT-ORAL-HISTORY-HULME
    note: "Les témoignages contredisent et recomposent les discours publics sur Hulme."

  - source: S06-A007
    type: illustre
    cible: CONCEPT-TEMOIGNAGE-CONTRADICTOIRE
    note: "Jason et Conor montrent deux manières de négocier la réputation du quartier."

  - source: S06-A008
    type: prolonge
    cible: CONCEPT-REAPPROPRIATION-STIGMATE
    note: "Le terme ghetto est parfois retourné en marque d’appartenance communautaire."

  - source: S06-A009
    type: nuance
    cible: MYTH-HULME-GHETTO-SANS-COMMUNAUTE
    note: "Certains récits présentent Hulme comme bulle multiculturelle et espace d’acceptation."

  - source: S06-A010
    type: nuance
    cible: MYTH-HULME-UTOPIE-MULTICULTURELLE
    note: "Shaima rappelle la présence de racisme ordinaire et de différenciations internes."

  - source: S06-A011
    type: prolonge
    cible: CONCEPT-METHODE-CONTRE-ABSTRACTION-URBAINE
    note: "L’écriture doit éviter mythe, spectacle et abstraction."

  - source: S06-A012
    type: prolonge
    cible: CONCEPT-RECLAIMING-INNER-CITY-NARRATIVES
    note: "Les habitants reprennent les récits de l’inner city à leurs propres conditions."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 1 : Hulme comme espace vécu et discursif ; contre les clichés de ruine moderniste."
    - "Chapitre 9 : géographie émotionnelle ; témoignages ; race ; stigmatisation territoriale ; communauté vécue."
    - "Chapitre 14 : récupération et patrimonialisation du passé urbain, avec prudence."
  requetes_utiles:
    - "S06 Hulme inner-city estate lived discursive space"
    - "S06 Hulme concrete jungle ghetto Bronx"
    - "S06 Hulme Crescents demolition redevelopment"
    - "S06 Jason Conor oral history Hulme"
    - "S06 Shaima Hulme racism Asian community"
    - "S06 reclaiming narratives post-war inner city"
  exclusions:
    - "Ne pas utiliser S06 comme source directe sur Joy Division."
    - "Ne pas confondre Hulme et Moss Side."
    - "Ne pas reprendre concrete jungle, ghetto ou Bronx comme descriptions neutres."
    - "Ne pas homogénéiser les témoignages d’habitants."
```
