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
    lat: 53.4808
    lng: -2.2426
    geo_precision: ville
    prudence_methodologique: >-
      Partage volontairement le centroïde de PLACE-MANCHESTER : échelles
      emboîtées (municipalité vs ville-noyau), entités documentaires distinctes,
      même point géographique.
    label: "City of Manchester"
    type: ville
    type_detail: municipalite
    sources:
      - S02-A003
    usage: "Échelle municipale à distinguer de Greater Manchester et de l’aire urbaine."
    prudence: "Ne pas lui attribuer mécaniquement les données de la conurbation ou de la région urbaine."

  - id: PLACE-GREATER-MANCHESTER
    lat: 53.59
    lng: -2.3
    geo_precision: ville
    prudence_methodologique: >-
      Comté métropolitain — coordonnée = centroïde approximatif, non un point.
    label: "Greater Manchester"
    type: ville
    type_detail: comte_metropolitain
    sources:
      - S02-A003
    usage: "Échelle métropolitaine utile pour comprendre la recomposition de Manchester au-delà de son centre municipal."
    prudence: "Préciser l’échelle lorsque les données portent sur population, emplois ou politiques urbaines."

  - id: PLACE-HULME
    lat: 53.464
    lng: -2.247
    geo_precision: quartier
    label: "Hulme"
    type: quartier
    type_detail: quartier
    sources:
      - S02-A008
      - S06
    usage: "Quartier emblématique des expérimentations urbaines, des limites du logement moderniste et des politiques de renouvellement."
    prudence: "Croiser S02 avec S06 et les sources spécialisées sur Hulme."

  - id: PLACE-MANCHESTER-CENTRE
    lat: 53.4794
    lng: -2.2453
    geo_precision: quartier
    label: "Centre-ville de Manchester"
    type: ville
    type_detail: centralite_urbaine
    sources:
      - S02-A005
      - S02-A006
      - S02-A007
    usage: "Espace de reconstruction, marketing territorial et recomposition après la crise urbaine et l’attentat de 1996."
    prudence: "Ne pas confondre renaissance du centre et transformation sociale homogène de toute la ville."
```
