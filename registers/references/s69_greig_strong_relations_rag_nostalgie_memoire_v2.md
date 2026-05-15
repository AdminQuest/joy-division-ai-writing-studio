# S69 — Relations stabilisées et note RAG — nostalgie, mémoire, patrimonialisation

```yaml
id: REL-RAG-S69-NOSTALGIE-MEMOIRE-V2
source_id: S69
source_label: "S69 — Greig & Strong, But We Remember When We Were Young, 2014"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S69-A021
  - S69-A022
  - S69-A023
  - S69-A024
  - S69-A025
  - S69-A026
  - S69-A027
  - S69-A028
  - S69-A029
  - S69-A030
  - S69-A031
  - S69-A032
  - S69-A033
  - S69-A034
chapitres:
  - Chapitre 9
  - Chapitre 12
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S69. Il sert au RAG Studio comme carte relationnelle : mémoire post-2000, ordres de nostalgie, témoins d’autorité, commerce de la mémoire, controverses d’authenticité, publics tardifs.

## Relations stabilisées

```yaml
relations:
  - source: S69-A021
    type: prolonge
    cible: CONCEPT-MEMOIRE-CULTURELLE
    note: "Joy Division devient un objet de travail mémoriel intensifié après 2000."

  - source: S69-A021
    type: prépare
    cible: CHAPITRE-14
    note: "Atome d’ouverture pour la postérité contemporaine du groupe."

  - source: S69-A022
    type: nuance
    cible: MYTH-JOY-DIVISION-MYSTERE
    note: "Le mystère du groupe est aussi produit par le déficit documentaire initial."

  - source: S69-A023
    type: cree
    cible: CONCEPT-NOSTALGIE-HUMEUR
    note: "Nostalgie comme expérience vécue de perte par les témoins."

  - source: S69-A023
    type: cree
    cible: CONCEPT-NOSTALGIE-MODE
    note: "Nostalgie comme stylisation du passé."

  - source: S69-A023
    type: cree
    cible: CONCEPT-NOSTALGIE-ERSATZ
    note: "Nostalgie sans mémoire directe, activée par les publics tardifs."

  - source: S69-A024
    type: prolonge
    cible: CONCEPT-SOCIETE-AMNESIQUE
    note: "La culture médiatisée accroît le marché des représentations du passé."

  - source: S69-A024
    type: prolonge
    cible: CONCEPT-COMMERCE-MEMOIRE
    note: "Les objets Joy Division circulent comme marchandises mémorielles."

  - source: S69-A025
    type: nuance
    cible: MYTH-NOSTALGIE-REACTIONNAIRE
    note: "La nostalgie peut aussi être ressource, stratégie culturelle ou dialogue avec le passé."

  - source: S69-A026
    type: cree
    cible: CONCEPT-TEMOIN-AUTORITE
    note: "Les témoins comblent les lacunes et revendiquent la compétence du récit."

  - source: S69-A027
    type: nuance
    cible: S45
    note: "Deborah Curtis est relue comme reprise d’histoire, non comme nostalgie conjugale."

  - source: S69-A028
    type: nuance
    cible: MEDIUM-CONTROL-2007
    note: "Control convertit le récit de Deborah Curtis en iconographie tragique."

  - source: S69-A029
    type: prolonge
    cible: CONCEPT-MEMOIRE-URBAINE
    note: "Le documentaire de Grant Gee articule Joy Division au récit de transformation de Manchester."

  - source: S69-A030
    type: prolonge
    cible: CONCEPT-LEGITIMITE-MEMORIELLE
    note: "La légitimité du récit dépend de l’association au groupe."

  - source: S69-A031
    type: tension
    cible: CONCEPT-AUTHENTICITE-ALTERNATIVE
    note: "La trace commerciale fragilise l’autorité dans la culture alternative."

  - source: S69-A032
    type: illustre
    cible: CONCEPT-NOSTALGIE-MODE
    note: "British Underground est un faux fanzine mobilisant les codes du punk."

  - source: S69-A033
    type: tension
    cible: PERSONNE-PETER-HOOK
    note: "Hook devient à la fois témoin primaire et acteur contesté du marché mémoriel."

  - source: S69-A033
    type: tension
    cible: PERSONNE-BERNARD-SUMNER
    note: "Sumner sacralise le patrimoine Joy Division contre l’usage scénique de Hook."

  - source: S69-A034
    type: prolonge
    cible: CONCEPT-MYTHE-EVOLUTIF
    note: "Les publics tardifs, remasters, mash-ups et détournements prolongent la légende."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 9 : mémoire urbaine, Manchester, documentaire Grant Gee."
    - "Chapitre 12 : témoins d’autorité, Deborah Curtis, récits concurrents."
    - "Chapitre 14 : nostalgie ersatz, commerce de la mémoire, appropriations contemporaines."
  requetes_utiles:
    - "S69 nostalgie comme humeur mode ersatz"
    - "S69 témoins d’autorité légitimité mémoire Joy Division"
    - "S69 Deborah Curtis Control Corbijn mythification"
    - "S69 Grant Gee Manchester mémoire urbaine"
    - "S69 British Underground Warner JB Hi-Fi faux fanzine"
    - "S69 Peter Hook and The Light Bernard Sumner authenticité"
  exclusions:
    - "Ne pas utiliser S69 pour établir les faits primaires de 1976-1980."
    - "Ne pas réduire l’article à la dénonciation du marketing."
    - "Ne pas employer nostalgie sans distinguer humeur, mode et ersatz."
```
