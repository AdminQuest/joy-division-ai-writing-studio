# S02 — Compléments au registre des lieux — Manchester, Greater Manchester, Hulme

```yaml
id: PLACES-S02-MANCHESTER-SHRINKING-CITY-V2
source_id: S02
source_label: "S02 — Sueur, Villes du futur, futur des villes, 2011"
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-MANCHESTER-CITY
    label: "City of Manchester"
    type: municipalite
    sources:
      - S02-A003
    usage: "Échelle municipale à distinguer de Greater Manchester et de l’aire urbaine."
    prudence: "Ne pas lui attribuer mécaniquement les données de la conurbation ou de la région urbaine."

  - id: PLACE-GREATER-MANCHESTER
    label: "Greater Manchester"
    type: comte_metropolitain
    sources:
      - S02-A003
    usage: "Échelle métropolitaine utile pour comprendre la recomposition de Manchester au-delà de son centre municipal."
    prudence: "Préciser l’échelle lorsque les données portent sur population, emplois ou politiques urbaines."

  - id: PLACE-HULME
    label: "Hulme"
    type: quartier
    sources:
      - S02-A008
      - S06
    usage: "Quartier emblématique des expérimentations urbaines, des limites du logement moderniste et des politiques de renouvellement."
    prudence: "Croiser S02 avec S06 et les sources spécialisées sur Hulme."

  - id: PLACE-MANCHESTER-CENTRE
    label: "Centre-ville de Manchester"
    type: centralite_urbaine
    sources:
      - S02-A005
      - S02-A006
      - S02-A007
    usage: "Espace de reconstruction, marketing territorial et recomposition après la crise urbaine et l’attentat de 1996."
    prudence: "Ne pas confondre renaissance du centre et transformation sociale homogène de toute la ville."
```
