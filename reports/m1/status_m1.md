# Status consolidé M1

Rapport genere par `python3 tools/aggregate_m1.py` à partir des rapports M1 versionnés.

L'agrégateur lit uniquement les rapports M1 existants. Il ne relance aucun contrôle, ne recalcule aucun diagnostic, ne corrige aucun écart et ne modifie aucun objet documentaire.

## État général

**M1 STATUS** : conforme avec réserve

### Contrôles

| Contrôle | Statut | Rapport | Observations |
| --- | --- | --- | --- |
| ✓ DM -> atomes | conforme | `reports/m1/dm_atoms_traceability.md` | 2477/2477 atomes visibles retrouvés.<br>0 écart détecté dans le rapport agrégé. |
| ⚠ DM -> registres | conforme avec réserve | `reports/m1/dm_registers_consistency.md` | 80 écart(s) détecté(s).<br>0 document(s) non cohérent(s).<br>0 identifiant introuvable.<br>29 libellé divergent.<br>51 famille non couverte.<br>Les écarts restants relèvent des libellés divergents ou des familles hors MVP. |

### Audits M1

| Audit | Contrôle associé | Statut | Observation |
| --- | --- | --- | --- |
| ✓ Atomes S35 source vide | DM -> atomes | validé | Validation confirmée par le contrôle `DM -> atomes` conforme. |
| ✓ SONG-S45-SHADOWPLAY-RCA | DM -> registres | validé avec réserve | Validation confirmée par `Identifiants introuvables=0` dans le contrôle `DM -> registres`. |

## Dette documentaire connue

| Chantier | Statut |
| --- | --- |
| DM -> sources | non implémenté |
| DM -> exports | non implémenté |
| DM -> génération | non implémenté |
| DM -> obsolescence | non implémenté |
| DM -> statut documentaire | non implémenté |

## Maturité

| Jalon | Statut |
| --- | --- |
| M0 | ✓ terminé |
| M1.1 | ✓ contrôles fondamentaux |
| M1.2 | ✓ agrégation minimale |
| M1.3 | non démarré |
| M2 | non ouvert |

## Limites

- Ce status consolide les rapports déjà produits ; il ne prouve pas que les rapports sont fraîchement régénérés.
- Les divergences lexicales et les familles hors MVP restent des réserves documentaires, pas des corrections automatiques.
- L'agrégateur ne remplace pas les audits ciblés lorsque le sens documentaire d'un écart est ambigu.
- Ce fichier n'est pas un tableau de bord M1 et ne définit aucun seuil CI.

## Conclusion

L'agrégation minimale M1 est disponible pour consolider les contrôles existants. Elle peut préparer un futur tableau de bord ou une future intégration CI, mais elle ne les implémente pas.
