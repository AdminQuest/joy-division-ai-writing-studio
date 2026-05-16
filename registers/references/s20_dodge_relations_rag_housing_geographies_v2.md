# S20 — Relations stabilisées et note RAG — géographies du logement mancunien

```yaml
id: REL-RAG-S20-HOUSING-GEOGRAPHIES-V2
source_id: S20
source_label: "S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
type_unite: relations_rag
statut: integration_directe
atomes:
  - S20-A001
  - S20-A002
  - S20-A003
  - S20-A004
  - S20-A005
  - S20-A006
  - S20-A007
  - S20-A008
  - S20-A009
  - S20-A010
  - S20-A011
  - S20-A012
  - S20-A013
  - S20-A014
chapitres:
  - Chapitre 1
  - Chapitre 9
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S20. Il sert au RAG Studio comme carte d’orientation sur la matérialité urbaine de Manchester : logement ouvrier, taudis, cartographie sanitaire, suburbanisation, logement social, overspill estates, urban renewal, mégastructures, désindustrialisation et gentrification contemporaine.

## Relations stabilisées

```yaml
relations:
  - source: S20-A001
    type: prolonge
    cible: CONCEPT-MANCHESTER-INDUSTRIEL
    note: "Manchester se construit sous contrainte industrielle et selon une logique de profit, sans plan d’ensemble."

  - source: S20-A002
    type: relie
    cible: S07
    note: "Little Ireland et Angel Meadow prolongent le cadre engelsien des conditions ouvrières."

  - source: S20-A003
    type: cree
    cible: CONCEPT-SEGREGATION-RESIDENTIELLE-MANCHESTER
    note: "Victoria Park illustre la séparation résidentielle bourgeoise face aux quartiers industriels."

  - source: S20-A004
    type: cree
    cible: CONCEPT-CARTOGRAPHIE-SANITAIRE-MANCHESTER
    note: "Bastow et Marr produisent une géographie sociale objectivée du logement."

  - source: S20-A005
    type: cree
    cible: MOTIF-CEINTURE-DE-TAUDIS
    note: "La carte de Marr montre les slums entourant le cœur commercial."

  - source: S20-A006
    type: nuance
    cible: CONCEPT-GARDEN-SUBURB
    note: "Chorltonville montre une solution réformatrice mais socialement limitée."

  - source: S20-A007
    type: prolonge
    cible: PLACE-WYTHENSHAWE
    note: "Wythenshawe est ville satellite, solution municipale et lieu de désancrage."

  - source: S20-A008
    type: prolonge
    cible: PLACE-HULME
    note: "Le plan de 1945 programme la dédensification massive de Hulme."

  - source: S20-A008
    type: relie
    cible: S06
    note: "À croiser avec Carter pour l’expérience vécue de Hulme."

  - source: S20-A009
    type: cree
    cible: CONCEPT-OVERSPILL-ESTATES
    note: "Hattersley, Hyde, Heywood et Longdendale déplacent la crise du logement vers la périphérie."

  - source: S20-A010
    type: prolonge
    cible: CONCEPT-URBAN-RENEWAL-MANCHESTER
    note: "Les Action Areas effacent les rues victoriennes et installent les solutions planifiées."

  - source: S20-A011
    type: cree
    cible: MOTIF-STREETS-IN-THE-SKY-ECHEC
    note: "Les walkways de Fort Beswick échouent à devenir des rues sociales."

  - source: S20-A012
    type: prolonge
    cible: CONCEPT-DESINDUSTRIALISATION-MANCHESTER
    note: "La crise des estates se comprend avec le chômage ouvrier et la disparition des emplois industriels."

  - source: S20-A013
    type: cree
    cible: EVENT-DEMOLITION-FORT-BESWICK-1982
    note: "La démolition devient le signe d’un retournement contre les mégastructures."

  - source: S20-A014
    type: prolonge
    cible: CONCEPT-CITY-CENTRE-LIVING-MANCHESTER
    note: "Les héritages contemporains réinscrivent la question du logement dans la gentrification et le marché résidentiel."

  - source: S20-A014
    type: nuance
    cible: MYTH-MANCHESTER-RENAISSANCE-HOMOGENE
    note: "Le retour résidentiel et la verticalisation du centre ne résolvent pas les tensions d’accessibilité."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 1 : matérialité urbaine, logement ouvrier, taudis, spatialisation sociale de Manchester."
    - "Chapitre 9 : morphologie de la ville, Hulme, Wythenshawe, urban renewal, Fort Beswick, géographie émotionnelle."
    - "Chapitre 14 : gentrification, city centre living et conversion contemporaine du passé urbain."
  requetes_utiles:
    - "S20 Dodge Manchester housing problems"
    - "S20 Little Ireland Angel Meadow Victorian slums"
    - "S20 Marr 1904 belt of slums Manchester"
    - "S20 Wythenshawe satellite town isolation"
    - "S20 Hulme 1945 plan population shrink"
    - "S20 Fort Beswick streets in the sky"
    - "S20 deindustrialisation male unemployment estates"
    - "S20 city centre living gentrified mills"
  exclusions:
    - "Ne pas utiliser S20 comme source directe sur Joy Division."
    - "Ne pas confondre S20 Dodge avec S04 Kidd."
    - "Ne pas réactiver l’ancien S20 Reynolds : utiliser S72 pour Reynolds."
    - "Ne pas utiliser les figures cartographiques comme simples images d’ambiance."
```
