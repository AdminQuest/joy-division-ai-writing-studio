# C3A-9 — Audit documentaire du registre Sessions / Répétitions

## Objectif

Construire un registre spécialisé pour la fabrication du son Joy Division :
répétitions, démos, sessions studio, sessions radio, sessions télévisées et
lieux de travail musical.

Le lot reste strictement documentaire : aucun chapitre, aucun texte de
manuscrit et aucun workflow ne sont modifiés.

## Corpus consulté

| Corpus | Usage |
|--------|-------|
| `https://www.joydiv.org/sessions.htm` | Socle des sessions studio, radio, démos et session posthume Still |
| `https://www.joydiv.org/rehearsals.htm` | Répétitions documentées par bandes circulantes, dates souvent tentatives |
| `https://www.joydiv.org/jdtv.htm` | Apparitions télévisées Granada / What's On / Something Else |
| `registers/chronology/events_canonical.md` | Alignement avec les événements chronologiques canoniques |
| `registers/chronology/**` | Recoupements S41, S45, S75, S76 |
| `registers/places/**` | Lieux canoniques déjà exposés : Pennine, Cargo, Strawberry, Britannia Row, T.J. Davidson's, Graveyard |
| `registers/people/**` | Personnes canoniques : membres du groupe, Hannett, Wilson, Peel, Rushent, Davidson |
| `sources/middles_reade_torn_apart/**` | Répétitions post-Cargo, T.J. Davidson's, maturation sonore |
| `sources/cashell_spectral_presences_new_order/**` | Ceremony / In a Lonely Place et statut spectral des enregistrements tardifs |

## Livrables produits

| Fichier | Rôle |
|---------|------|
| `registers/sessions/joy_division_sessions_register_v1.md` | Registre actif C3A-9 |
| `registers/sessions/00_canonical_sessions.md` | Note legacy pour éviter les doublons d'identifiants |
| `registers/sessions/README.md` | Documentation mise à jour du registre |
| `docs/c3a-9-sessions-audit.md` | Présent audit |

## Inventaire

Le registre actif contient 26 entrées `JD-SESSION-*`.

| Type | Nombre | Lecture |
|------|--------|---------|
| `demo` | 3 | Warsaw demo, An Ideal for Living, Genetic Demos |
| `studio` | 10 | RCA, Factory Sample, Unknown Pleasures, Transmission, Sordide, LWTUA, Closer, Still |
| `radio` | 3 | Peel 1, Piccadilly, Peel 2 |
| `television` | 3 | Granada Reports, What's On, Something Else |
| `rehearsal` | 7 | Répétitions Warsaw, T.J. Davidson's, Bedge tape, Ceremony / In a Lonely Place |

| Statut documentaire | Nombre | Critère |
|---------------------|--------|---------|
| `etabli` | 19 | Date et nature suffisamment stables dans joydiv.org et/ou registres internes |
| `probable` | 5 | Date ou localisation indiquée comme tentative mais exploitable comme témoin documentaire |
| `conteste` | 2 | Attribution de lieu ou nature de bande explicitement fragile |

## Couverture des priorités

| Priorité C3A-9 | Couverture |
|----------------|------------|
| Premières répétitions Warsaw | Ajout des répétitions août/septembre 1977 et octobre/novembre 1977 |
| Évolution des lieux de répétition | T.J. Davidson's, lieux inconnus, Graveyard / rehearsal room, Pinky's à confirmer |
| Apparition de Stephen Morris | Reliée à la répétition Warsaw probable de septembre 1977 et à l'événement canonique `EVENT-ARRIVEE-STEPHEN-MORRIS` |
| Sessions RCA | Session Arrow / RCA conservée et enrichie |
| Sessions Cargo | Factory Sample et Sordide Sentimental conservées |
| Unknown Pleasures | Session Strawberry conservée et enrichie |
| Closer | Session Britannia Row conservée et enrichie |
| Peel Sessions | Deux sessions Peel conservées |
| Love Will Tear Us Apart | Pennine janvier 1980, Strawberry mars 1980 et contexte vidéo séparé |
| Atmosphere | Piccadilly Radio (`Chance`) et Cargo / Sordide |
| Ceremony | Rehearsal room / Graveyard, statut contesté |
| In a Lonely Place | Rehearsal room / Graveyard et prise probable du 14 mai 1980 |

## Relations documentées

Le registre ajoute des relations documentaires internes dans le champ
`relations`, sans générer d'arêtes dans `edges.json`.

| Relation | Statut |
|----------|--------|
| session -> place | Renseignée lorsqu'un `PLACE-*` canonique existe déjà |
| session -> chronology | Renseignée pour les événements canoniques déjà présents |
| session -> person | Renseignée sur quelques producteurs, médiateurs et membres quand l'identifiant canonique est stable |
| session -> song | Non générée en ID strict dans ce lot ; les titres restent en labels dans `titres` |
| session -> release | Présente sous forme documentaire dans `premiere_sortie_officielle`, pas encore en arête |
| session -> bootleg | Mentionnée seulement en notes lorsque nécessaire ; pas de registre bootlegs créé |

## Points de prudence

Les répétitions joydiv.org ne forment pas un journal exhaustif de répétition.
La page documente les bandes connues ou discutées, souvent avec des dates
tentatives. Le registre ne transforme donc pas ces entrées en certitudes
historiques.

Les lieux suivants ne doivent pas encore produire d'arêtes `session -> place` :

| Cas | Raison |
|-----|--------|
| Répétition août/septembre 1977 | Lieu non documenté |
| Bedge tape mars 1979 | Cassette étiquetée live possible, nature de répétition seulement probable |
| BBC2 / Oxford Road | Aucun `PLACE-*` canonique exposé pour le lieu TV exact |
| Granada TV | Aucun `PLACE-*` canonique exposé pour les studios Granada dans le registre lieux |
| Pinky's Rehearsal Room | Lieu cité comme supposé ; aucun `PLACE-*` canonique stabilisé |

## Compléments aux registres existants

Aucun complément n'a été appliqué à `chronology`, `songs`, `places` ou
`people` dans ce lot. Plusieurs compléments deviennent cependant candidats :

| Registre | Complément candidat |
|----------|--------------------|
| `places` | Créer ou confirmer Granada TV, BBC2 Oxford Road et Pinky's Rehearsal Room uniquement après validation documentaire |
| `songs` | Ajouter des relations sessionnelles pour les versions de Transmission, LWTUA, Atmosphere, Ceremony, In a Lonely Place |
| `chronology` | Ajouter des membres canoniques pour les répétitions probables si le statut documentaire est accepté |
| `people` | Consolider les rôles d'ingénieurs et producteurs quand les crédits sont recoupés par supports officiels |

## Exclusions

| Exclusion | Motif |
|-----------|-------|
| Concerts ordinaires | Déjà couverts par le registre Concerts |
| Bootlegs live sans contenu sessionnel | Hors périmètre C3A-9 |
| Mentions critiques sans fait sessionnel | À conserver dans sources / concepts, pas dans sessions |
| Lieux seulement supposés | Pas de création automatique de `PLACE-*` |

## Recommandation

Le registre Sessions / Répétitions peut être considéré comme ouvert.

Prochain lot recommandé : **C3A-10 — Audit des relations session -> song /
session -> release**.

Justification : les sessions sont maintenant exportables et typées ; la valeur
utilisateur la plus forte vient ensuite de la navigation depuis une chanson ou
une sortie officielle vers ses sessions de fabrication. Les relations vers les
lieux peuvent suivre, mais seulement après clarification des lieux TV et des
salles de répétition incertaines.
