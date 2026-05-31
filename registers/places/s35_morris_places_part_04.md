# Registre lieux — S35 — Morris, *Record Play Pause*, 2019 — part 04

```yaml
source_id: S35
source_part: S35-PART-04
type_unite: registre_lieux
statut: supplement
passage_atomise: "PDF p. 75-102"
```

## Lieux structurants

```yaml
places:
  - id: PLACE-IVY-LANE
    label: "Ivy Lane"
    type: habitat
    type_detail: domicile_adolescent
    sources: [S35]
    usage: "Chambre, disques, batterie, repli adolescent."
    atoms: [S35-A052, S35-A053]
    chapitres: [Chapitre 1, Chapitre 3]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-SOUTHPORT-FLORAL-HALL
    lat: 53.654
    lng: -3.01
    geo_precision: exacte
    label: "Southport Floral Hall"
    type: salle
    type_detail: salle_spectacle
    sources: [S35]
    usage: "Pacte paternel ; Basie et Dietrich."
    atoms: [S35-A050]
    chapitres: [Chapitre 1, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-PIPS
    lat: 53.48480
    lng: -2.24460
    geo_precision: rue
    prudence_methodologique: >-
      Pips Disco, 55 Fennel Street, Manchester. Source :
      https://www.joydiv.org/places.htm. Rue remodelée ; bâtiment disparu.
    label: "Pips"
    type: salle
    type_detail: club
    sources: [S35]
    usage: "Sophistication glam ; contraste social avec le public rock."
    atoms: [S35-A051]
    chapitres: [Chapitre 2, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-AUDENSHAW-GRAMMAR-SCHOOL
    lat: 53.46669
    lng: -2.11910
    geo_precision: exacte
    reference_croisee: ["gias:136273"]
    prudence_methodologique: >-
      Audenshaw School (ancien Audenshaw Grammar School), Hazel Street,
      Audenshaw. Source :
      get-information-schools.service.gov.uk/Establishments/Establishment/Details/136273.
      Établissement existant. (gias = Get Information About Schools, URN:136273.)
    label: "Audenshaw Grammar School"
    type: education
    type_detail: grammar_school
    sources: [S35]
    usage: "Bannissement scolaire ; trajet vers Manchester."
    atoms: [S35-A057]
    chapitres: [Chapitre 1]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-GUIDE-BRIDGE
    lat: 53.4744
    lng: -2.1127
    geo_precision: quartier
    reference_croisee: ["wikidata:Q5615429"]
    label: "Guide Bridge"
    type: infrastructure
    type_detail: seuil_ferroviaire
    sources: [S35]
    usage: "Seuil ferroviaire vers l'auto-éducation mancunienne."
    atoms: [S35-A057]
    chapitres: [Chapitre 1]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-HOUSE-ON-THE-BORDERLAND
    label: "House on the Borderland"
    type: commerce
    type_detail: librairie
    sources: [S35]
    usage: "Librairie de contre-savoirs ; science-fiction, occultisme, underground."
    atoms: [S35-A058]
    chapitres: [Chapitre 1, Chapitre 11, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-PERCIVALS
    label: "Percival's"
    type: commerce
    type_detail: librairie
    sources: [S35]
    usage: "Librairie ; Ballard, Burroughs, presse marginale."
    atoms: [S35-A058]
    chapitres: [Chapitre 1, Chapitre 11, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-BLACK-SEDAN
    label: "Black Sedan"
    type: commerce
    type_detail: disquaire
    sources: [S35]
    usage: "Disquaire / bootlegs ; rareté et déception matérielle."
    atoms: [S35-A059]
    chapitres: [Chapitre 8, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-RARE-RECORDS
    label: "Rare Records"
    type: commerce
    type_detail: disquaire
    sources: [S35]
    usage: "Disquaire ; non-rencontre mémorielle avec Curtis ; chasse au disque."
    atoms: [S35-A061]
    chapitres: [Chapitre 2, Chapitre 8, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-ATWELL-AND-JENNERS-MILL
    lat: 53.25700
    lng: -2.12480
    geo_precision: rue
    prudence_methodologique: >-
      Atwell & Jenner Ltd, Goodall Street Works, Macclesfield. Source :
      Cheshire Archives DRY/5/7
      (catalogue.cheshirearchives.org.uk/records/DRY/5/7). Coordonnée de
      Goodall Street ; usine exacte à confirmer.
    label: "Atwell and Jenner's mill"
    type: industrie
    type_detail: usine_textile
    sources: [S35]
    usage: "Travail textile ; rythme industriel vécu."
    atoms: [S35-A060]
    chapitres: [Chapitre 1, Chapitre 3, Chapitre 13]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-STONEGROUND-MAYFLOWER
    lat: 53.46100
    lng: -2.18200
    geo_precision: rue
    prudence_methodologique: >-
      Stoneground / Mayflower Club, Birch Street, West Gorton (ancien cinéma
      Corona, démoli). Source :
      manchesterbeat.com/venues/venues-gorton/stoneground-mayflower-birch-st-gorton.
    label: "Stoneground / Mayflower"
    type: salle
    type_detail: salle_concert
    sources: [S35]
    usage: "Lieu-palimpseste ; scène pré-punk et futur lieu Joy Division."
    atoms: [S35-A062]
    chapitres: [Chapitre 2, Chapitre 3, Chapitre 13]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-HARDROCK
    lat: 53.45980
    lng: -2.28930
    geo_precision: rue
    prudence_methodologique: >-
      Hardrock, Greatstone Road, Stretford. Source :
      manchesterbeat.com/venues/stretford/hardrock-greatstone-road-stretford.
      Salle disparue.
    label: "Hardrock"
    type: salle
    type_detail: salle_concert
    sources: [S35]
    usage: "Écoute live non segmentée ; Bowie, Genesis, Hawkwind, Lou Reed."
    atoms: [S35-A062]
    chapitres: [Chapitre 2, Chapitre 3]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-BUXTON
    lat: 53.259
    lng: -1.911
    geo_precision: ville
    label: "Buxton"
    type: ville
    type_detail: ville_provinciale
    sources: [S35]
    usage: "Festival pluvieux ; anti-utopie contre-culturelle."
    atoms: [S35-A063]
    chapitres: [Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-WHITE-CITY
    lat: 53.46200
    lng: -2.28700
    geo_precision: rue
    prudence_methodologique: >-
      White City Stadium, Chester Road, Old Trafford. Source :
      https://en.wikipedia.org/wiki/White_City_Stadium_(Manchester). Coordonnée
      du complexe (corrigé de « site » → rue).
    label: "White City"
    type: salle
    type_detail: salle_concert
    sources: [S35]
    usage: "Festival ; Children of God ; désillusion contre-culturelle."
    atoms: [S35-A063]
    chapitres: [Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-LEWISS
    label: "Lewis's"
    type: commerce
    type_detail: grand_magasin
    sources: [S35]
    usage: "Grand magasin ; Great Vinyl Robbery."
    atoms: [S35-A064]
    chapitres: [Chapitre 8, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-BOOTLE-STREET
    label: "Bootle Street"
    type: pouvoir
    type_detail: commissariat
    sources: [S35]
    usage: "Arrestation ; retour brutal au réel."
    atoms: [S35-A064]
    chapitres: [Chapitre 8, Chapitre 14]
    _legacy_format: s35-lieux-fonction
  - id: PLACE-MACCLESFIELD
    label: "Macclesfield"
    type: ville
    type_detail: ville_provinciale
    sources: [S35]
    usage: "Espace d'étouffement, danger local, désir de rupture."
    atoms: [S35-A065]
    chapitres: [Chapitre 1, Chapitre 12, Chapitre 14]
    _legacy_format: s35-lieux-fonction
```
