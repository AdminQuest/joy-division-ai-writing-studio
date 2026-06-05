# Cartographie des contrôles M1

# Objet du document

Ce document constitue le pont entre :

- les défaillances documentaires définies pour M1 ;
- les futurs audits documentaires ;
- les futurs tableaux de bord qualité ;
- les futurs scripts éventuels.

Il ne crée aucun contrôle opérationnel et n'implémente aucun script. Il décrit les contrôles qui devront exister pour détecter, qualifier et prioriser les défaillances documentaires déjà cadrées dans M1.

Lorsqu'un outil existant est cité, il sert seulement de point de rattachement documentaire possible. Sa mention ne signifie pas que le contrôle M1 correspondant est déjà implémenté.

Cette cartographie ne corrige aucun écart du dépôt. Elle prépare seulement un vocabulaire de contrôle partagé avant toute décision d'automatisation.

# Principes M1

- M1 vérifie.
- M1 ne produit pas de contenu documentaire.
- M1 ne remplace pas le jugement humain.
- M1 ne crée pas de nouvelles sources.
- M1 ne modifie pas le corpus.

Les contrôles M1 doivent établir des constats : présence ou absence de lien, cohérence ou divergence, statut explicite ou implicite, synchronisation ou désynchronisation. La décision de corriger, régénérer, conserver, déclasser ou reporter reste une décision documentaire séparée.

# Cartographie des contrôles

## Contrôles de traçabilité

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance de traçabilité | DM -> atomes | `chapters/*/document_maitre.md`, atomes du corpus exporté | semi-automatique | moyen | P0 |
| Défaillance de traçabilité | DM -> registres | documents maîtres, registres canoniques | semi-automatique | moyen | P0 |
| Défaillance de traçabilité | DM -> exports | documents maîtres, `exports/generated/` | semi-automatique | moyen | P0 |
| Défaillance de traçabilité | DM -> sources | documents maîtres, sources, citations | semi-automatique | faible | P1 |
| Défaillance de traçabilité | Livrables RAG -> corpus | livrables RAG conservés, sources, atomes, registres, exports | manuel | faible | P1 |
| Défaillance de traçabilité | Livrable -> script de génération | exports, documents maîtres, audits, `STATUS.md` | semi-automatique | moyen | P1 |

## Contrôles de dérivabilité

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance de dérivabilité | Information présente dans un DM mais absente du corpus | documents maîtres, corpus exporté | semi-automatique | faible | P0 |
| Défaillance de dérivabilité | Information présente dans un livrable conservé mais non reconstruisible | livrables conservés, sources, atomes, registres, exports | manuel | faible | P1 |
| Défaillance de dérivabilité | Synthèse non dérivable de plusieurs atomes | documents maîtres, atomes, exports | manuel | faible | P2 |
| Défaillance de dérivabilité | Relation reprise sans ancrage dans les registres | relations, registres, documents maîtres | semi-automatique | moyen | P1 |

## Contrôles d'obsolescence

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance d'obsolescence | DM plus ancien que ses dépendances | documents maîtres, sources, atomes, registres, exports | semi-automatique | moyen | P0 |
| Défaillance d'obsolescence | Export plus récent que le document qui en dépend | exports générés, documents maîtres, livrables conservés | semi-automatique | élevé | P1 |
| Défaillance d'obsolescence | Registre modifié sans mise à jour du livrable associé | registres, documents maîtres, livrables conservés | semi-automatique | moyen | P1 |
| Défaillance d'obsolescence | Audit ou statut daté sans périmètre temporel clair | audits, `STATUS.md`, documents de statut | manuel | faible | P2 |

## Contrôles de cohérence documentaire

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance de cohérence documentaire | Divergence entre registres | registres canoniques, relations inter-registres | semi-automatique | moyen | P1 |
| Défaillance de cohérence documentaire | Divergence entre export et registre | exports générés, registres canoniques | automatique | élevé | P1 |
| Défaillance de cohérence documentaire | Divergence entre DM et corpus | documents maîtres, corpus exporté | semi-automatique | moyen | P0 |
| Défaillance de cohérence documentaire | Divergence entre chronologie et livrable conservé | chronologies, documents maîtres, livrables conservés | semi-automatique | moyen | P2 |
| Défaillance de cohérence documentaire | Contradiction non signalée entre audits | audits documentaires, documents de statut | manuel | faible | P3 |

## Contrôles de statut documentaire

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance de statut documentaire | Livrable temporaire utilisé comme document maître | livrables temporaires, documents maîtres | manuel | faible | P1 |
| Défaillance de statut documentaire | Sortie RAG utilisée comme preuve documentaire | livrables RAG conservés, documents maîtres, notes de chapitre | manuel | faible | P1 |
| Défaillance de statut documentaire | Objet non qualifié utilisé comme source | livrables conservés, sources, registres | manuel | faible | P1 |
| Défaillance de statut documentaire | Livrable conservé sans statut explicite | livrables RAG, notes, synthèses, audits | semi-automatique | moyen | P1 |
| Défaillance de statut documentaire | Artefact expérimental présenté comme canonique | exports exploratoires, documents de travail | manuel | faible | P2 |

## Contrôles de génération

| Défaillance | Contrôle proposé | Objet contrôlé | Type | Niveau d'automatisation possible | Priorité |
|-------------|------------------|----------------|--------|----------------------------------|----------|
| Défaillance de génération | Artefact généré modifié manuellement | exports générés, documents maîtres, audits générés, `STATUS.md` | semi-automatique | moyen | P1 |
| Défaillance de génération | Divergence détectée par `check-generated-sync` | artefacts couverts par `tools/check_generated_sync.py` | automatique | élevé | P1 |
| Défaillance de génération | Document maître différent de la sortie de `tools/build_master_docs.py` | documents maîtres, manifeste, script de génération | automatique | élevé | P1 |
| Défaillance de génération | `STATUS.md` différent de la sortie de `tools/generate_status.py` | `STATUS.md`, script de génération de statut | automatique | élevé | P2 |
| Défaillance de génération | Producteur technique non identifié pour un artefact conservé | exports, audits, livrables conservés | semi-automatique | moyen | P2 |

# Classification des contrôles

## Contrôles à mettre en œuvre en premier

Les contrôles prioritaires sont ceux qui protègent directement les documents maîtres, les registres et les exports générés, car ils structurent la confiance documentaire du projet.

### P0

| Contrôle | Justification |
| --- | --- |
| DM -> atomes | Vérifie l'ancrage documentaire minimal des documents maîtres. |
| DM -> registres | Protège les identifiants, libellés, statuts et relations repris dans les vues rédactionnelles persistantes. |
| DM -> exports | Vérifie que les documents maîtres restent reliés au corpus exporté. |
| Information présente dans un DM mais absente du corpus | Détecte les informations non dérivables dans les livrables les plus sensibles. |
| Divergence entre DM et corpus | Signale les écarts structurants entre vue rédactionnelle et socle documentaire. |

### P1

| Contrôle | Justification |
| --- | --- |
| DM -> sources | Renforce la traçabilité fine lorsque l'ancrage par atomes ou exports ne suffit pas. |
| Livrables RAG -> corpus | Évite qu'une exploration RAG conservée circule sans rattachement documentaire. |
| Livrable -> script de génération | Clarifie la provenance technique des artefacts conservés. |
| Information présente dans un livrable conservé mais non reconstruisible | Étend la dérivabilité au-delà des seuls documents maîtres. |
| Relation reprise sans ancrage dans les registres | Protège les relations inter-entités contre les ajouts implicites. |
| Export plus récent que le document qui en dépend | Repère les vues potentiellement périmées après génération. |
| Registre modifié sans mise à jour du livrable associé | Détecte les effets de bord des évolutions de registres. |
| Divergence entre registres | Identifie les contradictions canoniques avant propagation. |
| Divergence entre export et registre | Vérifie la cohérence entre objets persistants et vues générées. |
| Divergence détectée par `check-generated-sync` | Signale les désynchronisations d'artefacts générés sans correction manuelle. |

# Contrôles explicitement hors M1

Les sujets suivants ne relèvent pas de cette cartographie M1 :

- enrichissement documentaire ;
- formulaires d'ajout ;
- workflows de saisie ;
- nouvelles applications ;
- migration Cloudflare ;
- évolution du RAG ;
- évolution de la Forge / Atelier.

Ces sujets peuvent nécessiter des décisions ultérieures, mais ils ne sont pas ouverts par ce document.

# Préparation du tableau de bord M1

## Indicateurs potentiels

Un futur tableau de bord M1 pourrait suivre :

- nombre de documents maîtres traçables ;
- nombre de documents maîtres obsolètes ;
- nombre de divergences détectées ;
- nombre d'artefacts désynchronisés ;
- nombre de livrables non qualifiés ;
- nombre de livrables RAG rattachés au corpus ;
- nombre d'informations non dérivables ;
- nombre de divergences entre registres ;
- nombre de divergences entre exports et registres ;
- nombre d'artefacts générés dont le producteur technique est identifié.

Ce tableau de bord n'est pas construit dans cette PR. Les indicateurs listés ici servent uniquement à préparer de futures décisions sur les audits, les scripts éventuels et la présentation des résultats qualité.
