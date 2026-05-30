# Convention — Numérotation des atomes et fiches canoniques

> Statut : convention active (dette D.4 de la ROADMAP, étape 2).
> Périmètre : tout atome `SXX-Annn` produit par le workflow d'atomisation.

## Principe

Une fiche canonique de source (`registers/references/sXX_..._source_canonique.md`)
peut proposer, sous « Atomes prioritaires à viser », une liste d'identifiants
`SXX-A001` … `SXX-A0NN`. **Ces identifiants sont des réservations thématiques**,
pas un ordre de création ni un engagement que chaque atome existera.

Concrètement :

1. **La carte `A001`–`A0NN` de la fiche est une réservation.** Chaque numéro
   désigne un *thème* attendu de la source (ex. pour S89 : `A007` = « 4 juin 1976,
   Lesser Free Trade Hall »). Tant qu'une passe n'a pas traité ce thème, le numéro
   reste libre — il n'est pas consommé par un autre atome.

2. **Une passe d'atomisation respecte la carte.** Quand une passe traite un thème
   présent dans la carte, elle réutilise le numéro réservé correspondant
   (ex. la passe S89 sur l'introduction a produit `S89-A020` parce que la fiche
   réservait `A020` à la grammaire « no future »).

3. **Les atomes hors carte commencent à `A021`.** Tout atome utile au manuscrit
   mais absent de la carte thématique de la fiche est numéroté séquentiellement à
   partir de `A021` (premier numéro après la plage de réservation `A001`–`A020`),
   dans l'ordre de création, sans toucher aux créneaux réservés `A001`–`A020`.

4. **Les créneaux réservés non encore traités ne sont jamais réaffectés** à un
   atome d'un autre thème. Ils restent disponibles pour la passe qui traitera
   effectivement le thème prévu.

Cette convention évite que la numérotation « ne survive pas au contact » d'une
atomisation partielle : on peut atomiser une source en plusieurs passes, dans le
désordre thématique, sans renuméroter ni créer de collisions.

## Pourquoi (rationale)

- **Anti-churn (dette D.1).** Un atome reçoit un identifiant stable dès sa
  création ; les passes ultérieures n'ont pas à le renuméroter.
- **Lisibilité.** Le numéro porte une intention : un lecteur de la fiche sait que
  `A007` parlera du LFTH, qu'il soit déjà écrit ou non.
- **Passes partielles.** Une source longue (livre entier) s'atomise en plusieurs
  passes ; la carte garantit que chaque passe sait quels numéros lui reviennent.

## Précédent de référence — S89 (Savage, *England's Dreaming*)

La première passe S89 (introduction + ouverture du chapitre 1) illustre la
convention :

| Atome créé | Thème | Origine du numéro |
|---|---|---|
| `S89-A001` | Préhistoire de la boutique 430 King's Road | créneau réservé `A001` (préhistoire glam) |
| `S89-A002` | McLaren & Westwood, matrice pré-SEX | créneau réservé `A002` |
| `S89-A020` | Trois négations / « no future » | créneau réservé `A020` (grammaire culturelle) |
| `S89-A021` | Curtis / « Ice Age », renvoi S45 | **hors carte → premier numéro libre `A021`** |
| `S89-A022` | Prudence : auto-mythologie McLaren/Westwood | **hors carte → `A022`** |
| `S89-A023` | World's End comme espace-matrice | **hors carte → `A023`** |

Les créneaux `A003`–`A019` (formation des Sex Pistols, 100 Club, Bill Grundy,
LFTH, Buzzcocks, Spiral Scratch, Wilson/Factory, etc.) **restent réservés** pour
les passes ultérieures sur les chapitres correspondants.

## Application

- Au début d'une passe, lire la carte de la fiche canonique et identifier les
  créneaux thématiques mobilisables.
- Réutiliser le créneau réservé quand le thème correspond ; sinon, prendre le
  prochain numéro libre ≥ `A021`.
- Ne jamais réaffecter un créneau réservé `A001`–`A020` à un thème différent.
- En cas de doute sur la frontière de réservation d'une source, la fiche
  canonique fait foi (cf. `registers/references/`).
