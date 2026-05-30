# S05 — Compléments au registre des lieux — policing et ordre public dans le Greater Manchester

```yaml
id: PLACES-S05-PUBLIC-ORDER-GREATER-MANCHESTER-V2
source_id: S05
source_label: "S05 — Jeffery, Tufail & Jackson, Policing and the Reproduction of Local Social Order, 2015"
type_unite: registre_lieux
statut: integration_directe
```

```yaml
places:
  - id: PLACE-GREATER-MANCHESTER
    label: "Greater Manchester"
    type: ville
    type_detail: comte_metropolitain
    sources:
      - S05-A002
      - S05-A013
    usage_s05: "Échelle institutionnelle de Greater Manchester Police et de la reproduction d’un ordre social local."

  - id: PLACE-HYDE
    lat: 53.451
    lng: -2.081
    geo_precision: ville
    label: "Hyde"
    type: ville
    type_detail: ville_greater_manchester
    sources:
      - S05-A005
    usage_s05: "Lieu de mobilisation du National Front en 1977 et de policing antifasciste."

  - id: PLACE-BOLTON
    lat: 53.578
    lng: -2.429
    geo_precision: ville
    label: "Bolton"
    type: ville
    type_detail: ville_greater_manchester
    sources:
      - S05-A005
    usage_s05: "Lieu de confrontation National Front / antifascistes en 1978."

  - id: PLACE-MOSS-SIDE
    lat: 53.453
    lng: -2.249
    geo_precision: quartier
    label: "Moss Side"
    type: quartier
    type_detail: quartier_inner_city
    sources:
      - S05-A006
    usage_s05: "Espace central des tensions racialisées entre GMP et communautés afro-caribéennes, notamment en 1981."
    prudence: "Croiser avec sources locales si usage factuel détaillé."

  - id: PLACE-UNIVERSITY-OF-MANCHESTER
    lat: 53.4668
    lng: -2.2339
    geo_precision: exacte
    reference_croisee: ["wikidata:Q230899"]
    label: "University of Manchester"
    type: education
    type_detail: universite
    sources:
      - S05-A007
    usage_s05: "Lieu de la Battle of Brittan en 1985."

  - id: PLACE-ORDSALL
    lat: 53.474
    lng: -2.272
    geo_precision: quartier
    label: "Ordsall"
    type: quartier
    type_detail: quartier_salford
    sources:
      - S05-A009
    usage_s05: "Lieu de l’émeute de 1992, articulant désindustrialisation, policing lourd, gentrification et réputation de no-go area."

  - id: PLACE-OLDHAM
    lat: 53.5409
    lng: -2.1183
    geo_precision: ville
    label: "Oldham"
    type: ville
    type_detail: ville_greater_manchester
    sources:
      - S05-A010
    usage_s05: "Lieu des émeutes de 2001, de racialisation du désordre et de discours de community cohesion."

  - id: PLACE-BARTON-MOSS
    label: "Barton Moss"
    type: lieu_memoire
    type_detail: site_protestation
    sources:
      - S05-A012
    usage_s05: "Site des protestations anti-fracking, cas contemporain de policing d’un conflit environnemental et économique."
```
