# S12 — Relations stabilisées et note RAG — AIDS, Anderton et ordre moral

```yaml
id: REL-RAG-S12-AIDS-ANDERTON-MORAL-ORDER-V2
source_id: S12
source_label: "S12 — Dossier de presse, AIDS / Anderton, 13 décembre 1986"
type_unite: relations_rag
statut: integration_directe
atomes:
  - S12-A001
  - S12-A002
  - S12-A003
  - S12-A004
  - S12-A005
  - S12-A006
  - S12-A007
  - S12-A008
chapitres:
  - Chapitre 1
chapitres_secondaires:
  - Chapitre 9
  - Chapitre 14
```

## Fonction

Ce fichier stabilise les relations issues de la passe v2 de S12. Il sert au RAG Studio pour documenter un épisode de moralisation publique du sida, centré sur James Anderton, mais inséré dans un débat plus large : gouvernement Thatcher, santé publique, Église catholique, police authority, presse nationale et discours stigmatisants.

## Relations stabilisées

```yaml
relations:
  - source: S12-A001
    type: cree
    cible: CONCEPT-SIDA-MORALE-PUBLIQUE-1986
    note: "Le sida devient objet de controverse sanitaire, morale et politique."

  - source: S12-A002
    type: prolonge
    cible: PERSONNE-JAMES-ANDERTON
    note: "Anderton intervient dans le débat public par une moralisation policière du sida."

  - source: S12-A002
    type: prolonge
    cible: CONCEPT-POLICE-MORALE-ANDERTON
    note: "Le discours policier s’étend à la sexualité, la santé publique et les minorités."

  - source: S12-A003
    type: nuance
    cible: MYTH-THATCHERISME-MORALE-UNIVOQUE
    note: "Le dossier distingue pragmatisme sanitaire gouvernemental et croisade morale."

  - source: S12-A004
    type: prolonge
    cible: CONCEPT-POLICE-ACCOUNTABILITY-MANCHESTER
    note: "La police authority envisage une censure des propos d’Anderton."

  - source: S12-A005
    type: relie
    cible: PERSONNE-CARDINAL-BASIL-HUME
    note: "Le discours religieux sur moral Chernobyl situe la controverse dans un espace moral plus large."

  - source: S12-A006
    type: cree
    cible: MOTIF-LANGAGE-DEGENERESCENCE-ORDRE-MORAL
    note: "Le dossier conserve un lexique stigmatisant à analyser avec distance critique."

  - source: S12-A007
    type: prolonge
    cible: CONCEPT-ORDRE-SOCIAL-LOCAL
    note: "Anderton illustre l’articulation entre police, morale, santé et ordre social."

  - source: S12-A008
    type: relie
    cible: S05
    note: "S12 est source de presse contemporaine ; S05 fournit la mise en perspective universitaire."
```

## Corpus RAG recommandé

```yaml
rag:
  priorite: moyenne_haute
  usages:
    - "Chapitre 1 : climat moral et institutionnel du Greater Manchester sous Anderton."
    - "Chapitre 9 : géographie conflictuelle, police, sexualité, minorités, ordre social."
    - "Chapitre 14 : mémoire critique des discours stigmatisants et de la ville régénérée / sécurisée."
  requetes_utiles:
    - "S12 Anderton AIDS self-inflicted wound"
    - "S12 moral Chernobyl Cardinal Hume AIDS"
    - "S12 police authority Anderton censure accountability"
    - "S12 Thatcher government AIDS pragmatism moral crusade"
    - "S12 degeneracy homosexuality drugs prostitution moral order"
  exclusions:
    - "Ne pas utiliser S12 comme source médicale."
    - "Ne pas présenter S12 comme texte d’Anderton."
    - "Ne pas reprendre les expressions stigmatisantes sans guillemets ni attribution."
    - "Ne pas isoler S12 de S05."
```
