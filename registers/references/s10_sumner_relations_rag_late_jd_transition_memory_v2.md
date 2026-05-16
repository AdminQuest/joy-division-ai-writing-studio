# S10 — Relations stabilisées et note RAG — Joy Division tardif, transition, mémoire

```yaml
id: REL-RAG-S10-LATE-JD-TRANSITION-MEMORY-V2
source_id: S10
source_label: "S10 — Sumner, Chapter and Verse, 2014/2015"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S10-A026
  - S10-A027
  - S10-A028
  - S10-A029
  - S10-A030
  - S10-A031
  - S10-A032
  - S10-A033
  - S10-A034
  - S10-A035
  - S10-A036
chapitres:
  - Chapitre 3
  - Chapitre 4
  - Chapitre 6
  - Chapitre 7
  - Chapitre 8
  - Chapitre 10
  - Chapitre 12
  - Chapitre 14
```

## Fonction

Cette carte complète la première passe S10. Elle stabilise les relations liées au Joy Division tardif : après *Unknown Pleasures*, « Transmission », « Atmosphere », *Closer*, derniers morceaux, mort de Curtis, naissance contrainte de New Order et mémoire mondiale. Elle doit être croisée avec S41, S45, S75, S76 et S69.

## Relations stabilisées

```yaml
relations:
  - source: S10-A026
    type: prolonge
    cible: CONCEPT-JOY-DIVISION-NON-REPETITION
    note: "Après Unknown Pleasures, le groupe cherche le dépassement plutôt que la formule."

  - source: S10-A027
    type: prolonge
    cible: SONG-TRANSMISSION
    note: "Transmission articule radio, injonction collective et tension répétitive."

  - source: S10-A028
    type: prolonge
    cible: SONG-ATMOSPHERE
    note: "Atmosphere ouvre un régime spectral et cérémoniel du son Joy Division."

  - source: S10-A028
    type: relie
    cible: ORG-SORDIDE-SENTIMENTAL
    note: "À croiser avec la sortie Licht und Blindheit."

  - source: S10-A029
    type: prolonge
    cible: ALBUM-CLOSER
    note: "Closer devient intensification sonore et déplacement hors Manchester."

  - source: S10-A030
    type: prolonge
    cible: CONCEPT-CURTIS-PRESSION-CLOSER
    note: "L’écriture de Closer est liée à un sentiment d’accélération et de perte de contrôle."

  - source: S10-A031
    type: cree
    cible: CONCEPT-SEUIL-CEREMONY-IN-A-LONELY-PLACE
    note: "Les derniers morceaux fonctionnent comme seuil entre Joy Division et New Order."

  - source: S10-A032
    type: nuance
    cible: MYTH-MORT-CURTIS-PURE-LEGENDE
    note: "La mort de Curtis est d’abord rupture pratique, affective et logistique."

  - source: S10-A033
    type: cree
    cible: CONCEPT-CONTRAINTE-CONTINUER-SANS-CURTIS
    note: "Ne plus pouvoir être Joy Division fonde la contrainte New Order."

  - source: S10-A034
    type: prolonge
    cible: CONCEPT-VOIX-SUMNER-PAR-DEFAUT
    note: "Sumner chante par nécessité, avant stabilisation d’une identité vocale."

  - source: S10-A035
    type: prolonge
    cible: ALBUM-MOVEMENT
    note: "Movement est disque de seuil, encore chargé du deuil de Joy Division."

  - source: S10-A036
    type: prolonge
    cible: CONCEPT-MEMOIRE-MONDIALE-JOY-DIVISION
    note: "La préface de Sumner inscrit Joy Division / New Order dans une réception globale et intergénérationnelle."

  - source: S10-A036
    type: relie
    cible: S69
    note: "À croiser avec Greig & Strong sur nostalgie, publics tardifs et patrimonialisation."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: haute
  usages:
    - "Chapitre 3 : après Unknown Pleasures, Transmission, Atmosphere, sessions tardives."
    - "Chapitre 4 : Closer, pression Curtis, Ceremony / In a Lonely Place."
    - "Chapitre 10 : mort de Curtis, rupture pratique, mémoire du traumatisme."
    - "Chapitre 12 : passage à New Order, voix de Sumner, Movement."
    - "Chapitre 14 : mémoire mondiale, publics intergénérationnels, Unknown Pleasures T-shirt."
  requetes_utiles:
    - "S10 Transmission radio Joy Division"
    - "S10 Atmosphere Dead Souls Sordide Sentimental"
    - "S10 Closer Britannia Row Curtis whirlpool"
    - "S10 Ceremony In a Lonely Place cheer up Ian Curtis"
    - "S10 Curtis death American tour New Order"
    - "S10 Movement grief New Order"
    - "S10 global fans Unknown Pleasures T-shirt"
  exclusions:
    - "Ne pas citer longuement Sumner."
    - "Ne pas utiliser S10 seul pour la mort de Curtis ou Closer."
    - "Ne pas faire de New Order une continuation simple de Joy Division."
```
