# Bilan intermédiaire M1

État observé au 5 juin 2026, après clôture de M0, ouverture de M1, implémentation des contrôles P0 `DM -> atomes` et `DM -> registres`, et correction ciblée de `SONG-S45-SHADOWPLAY-RCA`.

Ce document dresse un bilan factuel de M1. Il ne crée aucun contrôle, aucun script, aucun rapport automatisé et ne modifie pas le périmètre de M1.

## 1. Objet du chantier M1

M1 vise à fiabiliser le système documentaire dans le temps. Le chantier porte sur la capacité du dépôt à détecter, qualifier et suivre les défaillances qui peuvent affecter les documents maîtres, les registres, les exports générés, les livrables conservés et les rapports de contrôle.

Le périmètre retenu à ce stade est volontairement documentaire et non fonctionnel. M1 ne produit pas de contenu documentaire nouveau, ne modifie pas le corpus par principe, ne remplace pas le jugement humain et n'ouvre pas les chantiers M2. Les corrections réalisées dans M1 sont des corrections ciblées, déclenchées par un audit documenté, puis validées par les contrôles concernés.

Les défaillances documentaires ciblées sont les suivantes :

| Défaillance | État dans M1 |
| --- | --- |
| Traçabilité | Cadrée, auditée sur les documents maîtres, partiellement contrôlée par `DM -> atomes`. |
| Dérivabilité | Cadrée, mais pas encore contrôlée passage par passage. |
| Obsolescence | Cadrée, mais aucun contrôle automatisé n'existe encore. |
| Cohérence documentaire | Cadrée, partiellement contrôlée par `DM -> registres`. |
| Statut documentaire | Cadré, mais pas encore contrôlé automatiquement. |
| Génération | Cadrée, mais non intégrée aux contrôles M1 actuels. |

## 2. Architecture retenue

L'architecture M1 stabilisée repose sur la chaîne suivante :

```text
Contrôle
↓
Rapport
↓
Agrégation
↓
Tableau de bord
```

Le rôle de chaque étage est distinct :

| Étage | Rôle | État actuel |
| --- | --- | --- |
| Contrôle | Lire les objets documentaires et produire des constats sans correction. | Implémenté pour `DM -> atomes` et `DM -> registres`. |
| Rapport | Conserver le résultat régénérable d'un contrôle dans `reports/m1/`. | Implémenté pour les deux contrôles existants. |
| Agrégation | Consolider plusieurs rapports sans recalculer les contrôles. | Défini dans `docs/m1-architecture-de-l-agregation.md`, non implémenté. |
| Tableau de bord | Donner une vue synthétique de la qualité documentaire. | Cadré dans `docs/m1-tableau-de-bord-qualite.md`, non implémenté. |

Les principes retenus sont stabilisés : lecture seule, absence de correction automatique, séparation entre contrôle et rapport, reproductibilité, rapport canonique, agrégation indépendante et absence d'effet de bord. Les intégrations à `build_all.py`, `check_generated_sync.py`, GitHub Actions ou à la CI restent hors de l'état implémenté.

## 3. Contrôles implémentés

### DM -> atomes

| Élément | État |
| --- | --- |
| Objectif | Vérifier que les identifiants d'atomes visibles dans les documents maîtres existent dans `exports/generated/atoms.json` et que les volumétries principales restent cohérentes avec `exports/generated/master_docs_index.json`. |
| Niveau de criticité | P0. Le contrôle établit l'ancrage documentaire minimal des documents maîtres. |
| Script | `tools/check_dm_atoms_traceability.py`. |
| Rapport généré | `reports/m1/dm_atoms_traceability.md`. |
| Périmètre | Documents maîtres, manifeste, index des documents maîtres, export des atomes. |
| Limite assumée | Le contrôle ne vérifie pas le rattachement passage par passage à un atome précis. |

Résultats observés dans le rapport actuel :

| Indicateur | Valeur |
| --- | --- |
| Documents maîtres déclarés | 14 |
| Documents maîtres présents sur disque | 14 |
| Documents maîtres traçables | 14 |
| Documents maîtres partiellement traçables | 0 |
| Documents maîtres non traçables | 0 |
| Atomes visibles | 2477 |
| Atomes retrouvés | 2477 |
| Alias résolus | 9 |
| Écarts détectés | 0 |

Le contrôle valide donc la traçabilité minimale `DM -> atomes` au niveau des identifiants visibles. Il ne prouve pas encore la dérivabilité fine de chaque passage.

### DM -> registres

| Élément | État |
| --- | --- |
| Objectif | Vérifier que les identifiants de registres visibles dans les documents maîtres sont présents dans les exports concernés et cohérents avec les volumétries principales. |
| Niveau de criticité | P0. Le contrôle vérifie l'alignement minimal entre documents maîtres et registres canoniques exportés. |
| Script | `tools/check_dm_registers_consistency.py`. |
| Rapport généré | `reports/m1/dm_registers_consistency.md`. |
| Périmètre MVP | Personnes, chansons, chronologie, citations, concerts, sessions. |
| Hors périmètre actuel | Familles P1 et hors MVP, notamment concepts, motifs, mythes, lieux, organisations et relations. |

Résultats observés dans le rapport actuel :

| Indicateur | Valeur |
| --- | --- |
| Documents maîtres déclarés | 14 |
| Documents maîtres présents sur disque | 14 |
| Documents maîtres cohérents | 1 |
| Documents maîtres partiellement cohérents | 13 |
| Documents maîtres non cohérents | 0 |
| Écarts détectés | 80 |
| Identifiants introuvables | 0 |
| Registres absents | 0 |
| Compteurs incohérents | 0 |
| Relations non résolues | 0 |
| Familles non couvertes | 51 |
| Libellés divergents | 29 |

Les identifiants des familles P0 sont retrouvés :

| Famille | Visibles / retrouvés |
| --- | --- |
| Personnes | 477 / 477 |
| Chansons | 238 / 238 |
| Chronologie | 413 / 413 |
| Citations | 511 / 511 |
| Concerts | 0 / 0 |
| Sessions | 0 / 0 |

Le contrôle ne signale plus d'identifiant chanson introuvable après la correction de `SONG-S45-SHADOWPLAY-RCA`. Les écarts restants relèvent surtout de familles hors MVP et de divergences de libellés objectivement détectables, mais pas nécessairement fautives.

## 4. Audits et corrections réalisés

M1 a déjà validé deux boucles complètes de traitement :

```text
Anomalie
↓
Audit
↓
Correction
↓
Validation
```

### Atomes S35 avec source vide

| Étape | Constat |
| --- | --- |
| Anomalie détectée | L'audit pilote de traçabilité des documents maîtres a identifié des occurrences `Source :  ;`. |
| Audit | `docs/m1-audit-atomes-source-vide-dm.md`. |
| Diagnostic | 48 occurrences, 17 atomes uniques, de `S35-A086` à `S35-A102`. Tous les atomes concernés appartenaient à `S35`. La source `S35` était retrouvée sans ambiguïté, mais la provenance n'était pas correctement portée par les atomes exportés. |
| Correction | Correction ciblée de la provenance `S35`, puis régénération canonique des artefacts concernés. |
| Validation | Le contrôle `DM -> atomes` actuel ne signale plus d'écart et retrouve 2477 atomes sur 2477 visibles. |

Ce cas a démontré que M1 peut passer d'un symptôme visible dans les documents maîtres à un diagnostic sur la chaîne de provenance, puis à une correction limitée.

### SONG-S45-SHADOWPLAY-RCA

| Étape | Constat |
| --- | --- |
| Anomalie détectée | Le contrôle `DM -> registres` a signalé `SONG-S45-SHADOWPLAY-RCA` comme visible dans un document maître mais absent de `exports/generated/songs.json`. |
| Audit | `docs/m1-audit-song-s45-shadowplay-rca.md`. |
| Diagnostic | L'identifiant, le registre, l'atome et la relation existaient. Le document maître et le contrôle étaient corrects. L'export chansons ne contenait pas l'objet. La cause la plus probable était une non-conformité de schéma dans le registre chanson `S45`. |
| Correction | Normalisation ciblée de l'entrée `SONG-S45-SHADOWPLAY-RCA` dans le registre concerné, puis régénération canonique. |
| Validation | Le rapport `DM -> registres` actuel indique `238 / 238` chansons visibles et retrouvées, avec `0` identifiant introuvable. |

Ce cas a validé le rôle du contrôle `DM -> registres` comme détecteur d'une divergence registre/export réellement corrigeable.

## 5. Enseignements tirés

Les contrôles automatisés en lecture seule fonctionnent lorsqu'ils portent sur des identifiants explicites, des fichiers attendus et des exports structurés. Les deux contrôles existants ont produit des constats exploitables sans modifier le corpus.

Le principe de boucle M1 est validé : un contrôle peut révéler un écart, un audit ciblé peut confirmer ou infirmer l'anomalie, une correction limitée peut être réalisée ensuite, puis le rapport régénéré peut valider la disparition du symptôme.

Les audits ciblés sont utiles parce qu'ils empêchent de corriger trop vite. Dans le cas `SONG-S45-SHADOWPLAY-RCA`, l'audit a distingué le document maître, le contrôle, le registre, l'atome, la relation et l'export avant de conclure. Cette séparation a évité de traiter le document maître comme fautif alors qu'il ne l'était pas.

Les limites des contrôles purement lexicaux sont visibles. Un contrôle lexical peut dire qu'un identifiant est présent ou absent et qu'un libellé diffère. Il ne sait pas toujours décider si la divergence est une erreur, un nom d'usage, un alias acceptable, un libellé long ou un choix rédactionnel. Cette limite impose de conserver l'audit humain pour les cas ambigus.

Ce qui est validé :

- les contrôles M1 peuvent rester strictement en lecture seule ;
- les rapports `reports/m1/*.md` sont utilisables comme preuves de contrôle ;
- les corrections ciblées peuvent être validées par disparition d'un écart dans le rapport concerné ;
- les documents maîtres sont un bon premier périmètre de contrôle.

Ce qui reste incertain :

- la qualification automatique des variantes de libellés ;
- la traçabilité passage par passage ;
- la dérivabilité fine des affirmations rédactionnelles ;
- la règle de gravité à appliquer aux familles hors MVP ;
- les seuils qui pourraient justifier une future intégration CI.

## 6. Faux positifs et limites observées

Le rapport `DM -> registres` signale des divergences de libellés qui ne constituent pas nécessairement des anomalies documentaires. Les principaux cas observés concernent les noms complets et les noms d'usage.

| Cas | Nature de l'écart | Interprétation |
| --- | --- | --- |
| Ian Kevin Curtis / Ian Curtis | Nom complet visible, nom d'usage exporté. | Divergence lexicale, pas une preuve d'erreur documentaire. |
| Stephen Paul David Morris / Stephen Morris | Nom complet visible, nom d'usage exporté. | Divergence lexicale, à traiter comme variante possible. |
| Robert Leo Gretton / Rob Gretton | Nom civil ou complet contre nom d'usage. | Le contrôle détecte une différence réelle de chaîne, sans arbitrer le statut documentaire. |
| Anthony Howard Wilson / Tony Wilson | Nom complet contre nom public. | Cas typique de libellé alternatif. |
| James Martin Hannett / Martin Hannett | Nom complet contre nom d'usage. | Divergence à qualifier par règle d'alias ou de libellé canonique. |
| Peter Andrew Saville / Peter Saville | Nom complet contre nom d'usage. | Divergence lexicale attendue dans certains contextes. |

D'autres limites proviennent des familles non couvertes par le MVP. Les identifiants de concepts, motifs, mythes, lieux, organisations ou relations peuvent être visibles dans les documents maîtres, mais le contrôle actuel les classe hors périmètre au lieu de les résoudre. Ce comportement est conforme au MVP, mais il maintient un bruit documentaire dans le rapport.

La limite principale reste la granularité. Les contrôles actuels savent établir qu'un document maître contient des identifiants retrouvés dans les exports. Ils ne démontrent pas encore que chaque passage rédactionnel est correctement relié à une source, un atome, un registre et un export.

## 7. Dette documentaire restante

Les contrôles suivants sont identifiés mais non implémentés :

| Contrôle absent | État |
| --- | --- |
| DM -> sources | Non implémenté. Le lien fin entre passages, sources et citations reste à contrôler. |
| DM -> exports | Non implémenté. Les documents maîtres ne sont pas encore comparés systématiquement à l'ensemble des exports dont ils dépendent. |
| DM -> génération | Non implémenté dans M1. Le lien entre documents maîtres, script de génération et artefacts générés reste à qualifier dans un contrôle dédié. |
| DM -> obsolescence | Non implémenté. Aucun contrôle M1 ne compare encore les documents maîtres à l'état temporel de leurs dépendances. |
| DM -> statut documentaire | Non implémenté. Les livrables et vues conservées ne sont pas encore qualifiés automatiquement selon le vocabulaire M1. |

Cette dette est documentaire et technique. Elle ne signifie pas que les objets concernés sont erronés ; elle signifie que M1 ne dispose pas encore des contrôles nécessaires pour les qualifier automatiquement.

## 8. État de maturité de M1

Éléments stabilisés :

- doctrine M1 des défaillances documentaires ;
- typologie des contrôles ;
- architecture commune des contrôles ;
- architecture future de l'agrégation ;
- principe du rapport régénérable dans `reports/m1/`;
- contrôle `DM -> atomes`;
- contrôle `DM -> registres`;
- boucle audit -> correction -> validation sur deux cas réels.

Éléments encore expérimentaux :

- qualification des divergences de libellés ;
- traitement des familles hors MVP ;
- règles de statut consolidé entre plusieurs contrôles ;
- futures sorties d'agrégation ;
- seuils de passage éventuels pour CI ou GitHub Actions.

Éléments nécessitant encore validation :

- contrôle `DM -> sources`;
- contrôle de dérivabilité fine ;
- contrôle d'obsolescence ;
- contrôle de statut documentaire ;
- passage d'un rapport par contrôle à une synthèse consolidée ;
- critères de blocage acceptables pour une intégration automatique.

Le niveau de confiance atteignable à ce stade est moyen à bon pour la traçabilité structurelle des documents maîtres vers les atomes et les familles P0 de registres. Il reste partiel pour la dérivabilité rédactionnelle, la preuve source par source, l'obsolescence et la qualification consolidée des livrables.

## 9. Arbitrages ouverts

| Option | Bénéfice attendu | Prérequis | Dépendances |
| --- | --- | --- | --- |
| DM -> sources | Renforcer la preuve documentaire en reliant les documents maîtres aux sources et citations mobilisées. | Définir la granularité attendue : document, section, passage ou citation. Clarifier le traitement des sources sans atome mais avec citations. | Documents maîtres, sources, citations, atomes, exports disponibles. |
| Agrégateur M1 | Produire une vue consolidée des rapports existants sans relancer la logique de contrôle. | Stabiliser le format minimal d'échange et la table de statuts commune. | Rapports `reports/m1/*.md`, architecture d'agrégation, convention de nommage. |
| Tableau de bord M1 | Donner une vision décisionnelle de la santé documentaire et suivre les tendances. | Disposer d'une agrégation fiable et de règles de gravité stabilisées. | Agrégateur, indicateurs définis, rapports de contrôles. |
| CI / GitHub Actions | Prévenir les régressions documentaires avant merge. | Définir ce qui doit bloquer une PR et ce qui doit seulement alerter. Réduire les faux positifs lexicaux. | Contrôles stables, rapports régénérables, seuils de gravité, politique de synchronisation. |

Ces arbitrages ne sont pas équivalents. Le tableau de bord et la CI dépendent d'une qualification plus stable des rapports. L'agrégateur peut être utile avant le tableau de bord, mais il ne doit pas masquer les limites des contrôles actuels. `DM -> sources` est le prochain contrôle le plus structurant pour améliorer la preuve documentaire, mais il demande un arbitrage de granularité plus exigeant que les contrôles déjà implémentés.

## 10. Recommandation de phase suivante

La suite de M1 devrait éviter de passer directement à la CI ou à un tableau de bord décisionnel complet. L'état réel du dépôt montre que les contrôles fonctionnent, mais que leur interprétation consolidée reste jeune : les rapports mélangent des écarts résolus, des familles hors MVP et des divergences lexicales qui ne doivent pas toutes être traitées comme des anomalies.

La recommandation est de poursuivre en deux temps :

1. Stabiliser une agrégation M1 minimale, centrée sur la lecture des rapports existants, les statuts consolidés et la distinction entre anomalie, limite MVP, faux positif probable et réserve documentaire.
2. Préparer ensuite le contrôle `DM -> sources`, en commençant par une décision de granularité et de preuve attendue, plutôt qu'en écrivant immédiatement un contrôle général.

Le tableau de bord M1 devrait venir après l'agrégation minimale. L'intégration CI ou GitHub Actions devrait rester reportée tant que les règles de blocage ne distinguent pas clairement les erreurs objectives des divergences de libellés ou des familles volontairement hors périmètre.

À ce stade, M1 est suffisamment mature pour continuer l'implémentation de contrôles ciblés. Il n'est pas encore suffisamment mature pour transformer tous les signaux en critères bloquants automatiques.
