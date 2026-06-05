# Agrégation minimale du status M1

## Objet

Ce document décrit la première couche d'agrégation documentaire M1.

L'agrégation minimale répond au besoin suivant :

```text
Rapports M1
↓
Agrégation minimale
↓
Status consolidé
```

Elle intervient après l'implémentation des premiers contrôles M1 et avant tout tableau de bord, toute intégration CI ou tout nouveau contrôle documentaire.

## Rôle de l'agrégateur

L'agrégateur lit les rapports M1 déjà produits dans `reports/m1/` et produit un status consolidé unique :

- contrôle `DM -> atomes` ;
- contrôle `DM -> registres` ;
- audits M1 déjà documentés ;
- dette documentaire connue ;
- maturité actuelle de M1.

Le script associé est `tools/aggregate_m1.py`.

Le status généré est `reports/m1/status_m1.md`.

## Périmètre

L'agrégation minimale couvre uniquement les contrôles M1 déjà opérationnels :

| Contrôle | Rapport lu | Statut |
| --- | --- | --- |
| DM -> atomes | `reports/m1/dm_atoms_traceability.md` | implémenté |
| DM -> registres | `reports/m1/dm_registers_consistency.md` | implémenté |

Elle mentionne aussi les audits M1 déjà stabilisés :

- atomes S35 avec source vide ;
- `SONG-S45-SHADOWPLAY-RCA`.

Elle rappelle enfin la dette documentaire connue :

- `DM -> sources` ;
- `DM -> exports` ;
- `DM -> génération` ;
- `DM -> obsolescence` ;
- `DM -> statut documentaire`.

## Différence entre contrôle et agrégation

Un contrôle M1 inspecte un périmètre documentaire précis et produit des constats.

Une agrégation M1 consolide les constats déjà produits.

L'agrégateur ne remplace aucun contrôle.

Il ne produit aucun diagnostic nouveau.

Il consolide uniquement les diagnostics existants.

Il ne lit pas les documents maîtres, les atomes, les registres ou les exports pour recalculer un résultat. Il lit les rapports existants et en déduit un status documentaire consolidé.

## Limites

L'agrégation minimale ne garantit pas que les rapports lus viennent d'être régénérés. Elle indique seulement l'état consolidé des rapports versionnés dans le dépôt.

Elle ne décide pas qu'un écart est historiographique, documentaire ou technique lorsque le rapport source ne le permet pas.

Elle ne qualifie pas automatiquement les divergences de libellés comme erreurs. Les cas de type nom complet / nom d'usage restent des réserves ou des faux positifs possibles tant qu'un audit ou une règle documentaire ne les a pas arbitrés.

Elle ne traite pas les familles hors MVP comme des anomalies bloquantes.

## Statuts consolidés

Les statuts utilisés par l'agrégateur sont volontairement simples :

| Statut | Signification |
| --- | --- |
| conforme | Aucun écart bloquant ou réserve connue dans le rapport lu. |
| conforme avec réserve | Le contrôle est exploitable, mais le rapport contient des réserves, limites MVP ou divergences à relire. |
| non conforme | Le rapport signale un écart objectif relevant du périmètre du contrôle. |
| rapport illisible | Le rapport attendu existe ou est appelé, mais ses indicateurs obligatoires sont absents ou non parsables. |
| non exécuté | Le rapport attendu est absent. |

Ces statuts ne constituent pas encore des seuils CI.

## Rôle futur dans le tableau de bord M1

L'agrégation minimale prépare le futur tableau de bord M1 en fournissant une source consolidée unique.

Le futur tableau de bord pourra s'appuyer sur `reports/m1/status_m1.md` pour afficher :

- l'état des contrôles existants ;
- les réserves documentaires ;
- la dette restante ;
- les jalons M1 disponibles ou non démarrés.

Le tableau de bord n'est pas créé par cette étape.

## Rôle futur éventuel dans la CI

Une future intégration CI pourrait exécuter les contrôles, régénérer leurs rapports, puis exécuter l'agrégateur.

Cette option reste hors périmètre de l'agrégation minimale.

Avant toute CI, il faudra décider :

- quels statuts bloquent une PR ;
- quels statuts doivent seulement alerter ;
- comment traiter les réserves lexicales ;
- comment vérifier que les rapports sont synchronisés avec leurs scripts.

## Hors périmètre

Cette étape ne crée pas :

- nouveau contrôle documentaire ;
- tableau de bord ;
- GitHub Action ;
- intégration CI ;
- système de scoring ;
- correction automatique ;
- audit ciblé supplémentaire.

Elle ne modifie pas les contrôles existants et ne change pas les rapports sources.

## Conclusion

L'agrégation minimale M1 fournit un status consolidé reproductible à partir des rapports existants.

Elle stabilise une couche de lecture intermédiaire entre les contrôles opérationnels et les futurs dispositifs de pilotage, sans ouvrir M2 et sans transformer les rapports en critères bloquants automatiques.
