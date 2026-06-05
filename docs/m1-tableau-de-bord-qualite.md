# Tableau de bord qualité documentaire M1

# Objet du document

Ce document définit les indicateurs qui permettraient de suivre l'état de santé documentaire du projet pendant M1.

Il précise :

- aucun tableau de bord n'est encore implémenté ;
- aucun script n'est créé ;
- aucun calcul automatique n'est mis en œuvre ;
- ce document prépare les futures décisions M1.

Les indicateurs décrits ici servent à mesurer, alerter et prioriser les défaillances documentaires déjà définies dans M1. Ils ne corrigent aucun écart et ne modifient aucun objet du corpus.

# Principes

Le tableau de bord M1 doit :

- mesurer ;
- alerter ;
- prioriser ;

sans :

- corriger ;
- enrichir ;
- modifier le corpus.

Un indicateur M1 doit rester un signal documentaire. Il peut aider à décider quoi auditer, quoi régénérer ultérieurement avec un outil canonique, quoi qualifier comme suspect ou quoi reporter, mais il ne remplace pas le jugement humain.

# Axes de pilotage

## Axe 1 — Traçabilité

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre de DM traçables vers les atomes | Nombre de documents maîtres dont les informations principales peuvent être reliées à des atomes du corpus. | Mesure l'ancrage documentaire minimal des vues rédactionnelles persistantes. | Compter les documents maîtres pour lesquels une relation DM -> atomes est établie ou vérifiable. | Élevée | Moyenne |
| Pourcentage de DM traçables vers les registres | Part des documents maîtres dont les entités, libellés ou relations sont rattachés aux registres canoniques. | Vérifie que les documents maîtres restent alignés avec les objets persistants. | Diviser le nombre de DM rattachés aux registres par le nombre total de DM évalués. | Moyenne | Moyenne |
| Pourcentage de DM traçables vers les sources | Part des documents maîtres dont les faits ou citations peuvent être reliés à des sources identifiables. | Renforce la preuve documentaire au-delà des seules vues générées. | Diviser le nombre de DM avec rattachement source vérifié par le nombre total de DM évalués. | Élevée | Faible |
| Nombre de livrables RAG conservés avec rattachement documentaire explicite | Nombre de livrables RAG conservés qui indiquent leurs sources, atomes, registres ou exports d'appui. | Évite qu'une sortie exploratoire soit réutilisée sans ancrage. | Compter les livrables RAG conservés dont le rattachement documentaire est explicitement documenté. | Moyenne | Faible |

## Axe 2 — Dérivabilité

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre d'informations non dérivables | Nombre d'informations présentes dans un document maître ou livrable conservé sans reconstruction possible depuis le corpus exporté. | Identifie les contenus qui ne peuvent pas être justifiés par le socle documentaire. | Comparer les affirmations du livrable aux sources, atomes, registres et exports disponibles. | Élevée | Faible |
| Nombre de passages suspects | Nombre de passages dont l'ancrage documentaire est insuffisant, contradictoire ou non dérivable. | Aide à prioriser les revues humaines avant réutilisation rédactionnelle. | Compter les passages marqués ou qualifiables comme suspects selon les critères M1. | Moyenne | Faible |
| Nombre de livrables conservés sans reconstruction possible | Nombre de livrables conservés dont le contenu ne peut pas être reconstruit depuis les objets du corpus. | Évalue le risque porté par les livrables hors pipeline ou mal qualifiés. | Identifier les livrables conservés puis vérifier leur reconstructibilité depuis le corpus exporté. | Élevée | Faible |
| Taux de dérivabilité des documents maîtres | Part des documents maîtres dont le contenu peut être reconstruit ou expliqué depuis le corpus exporté. | Donne une mesure synthétique de la fiabilité des vues rédactionnelles persistantes. | Diviser le nombre de DM dérivables par le nombre total de DM évalués. | Élevée | Moyenne |

## Axe 3 — Obsolescence

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre de DM potentiellement obsolètes | Nombre de documents maîtres dont une dépendance semble plus récente ou modifiée sans requalification. | Signale les vues qui pourraient ne plus refléter l'état courant du corpus. | Comparer les dates, empreintes ou versions des DM avec celles des dépendances identifiées. | Moyenne | Moyenne |
| Nombre de livrables plus anciens que leurs dépendances | Nombre de livrables conservés antérieurs aux sources, registres, exports ou scripts dont ils dépendent. | Repère les livrables à vérifier avant réutilisation. | Compter les livrables dont une dépendance connue est plus récente que le livrable. | Moyenne | Moyenne |
| Âge moyen des documents maîtres | Durée moyenne depuis la dernière génération ou modification contrôlée des documents maîtres. | Donne un signal simple de fraîcheur documentaire. | Calculer la moyenne des âges des fichiers `chapters/*/document_maitre.md` selon la donnée de référence retenue. | Faible | Élevée |
| Nombre de livrables nécessitant une régénération | Nombre de livrables dont la logique reste valide mais dont le contenu devrait être reconstruit par l'outil canonique. | Distingue les livrables périmés des livrables structurellement invalides. | Compter les livrables qualifiés comme à régénérer après comparaison avec leurs dépendances. | Moyenne | Moyenne |

## Axe 4 — Cohérence documentaire

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre de divergences registre/export | Nombre d'écarts entre registres canoniques et exports générés. | Vérifie la cohérence entre objets persistants et vues générées. | Comparer les identifiants, libellés, statuts et relations exportés aux registres de référence. | Moyenne | Élevée |
| Nombre de divergences DM/corpus | Nombre d'écarts entre documents maîtres et corpus exporté. | Protège les vues rédactionnelles persistantes contre la dérive documentaire. | Comparer les affirmations structurantes des DM aux atomes, registres et exports disponibles. | Élevée | Moyenne |
| Nombre de contradictions documentaires ouvertes | Nombre de contradictions connues entre objets documentaires sans arbitrage documenté. | Permet de suivre les incohérences qui nécessitent une décision humaine. | Compter les contradictions signalées mais non qualifiées comme résolues, acceptées ou reportées. | Moyenne | Faible |
| Nombre de divergences non arbitrées | Nombre de divergences détectées sans statut, responsable documentaire ou décision de traitement. | Priorise les écarts qui risquent de rester implicites. | Compter les divergences ouvertes sans qualification documentaire explicite. | Moyenne | Faible |

## Axe 5 — Statut documentaire

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre de livrables non qualifiés | Nombre de livrables conservés sans statut documentaire explicite. | Évite la circulation d'objets ambigus dans les usages rédactionnels ou documentaires. | Compter les livrables conservés dépourvus d'un statut tel que temporaire, conservé, document maître, généré, obsolète, suspect ou à régénérer. | Moyenne | Moyenne |
| Nombre de sorties RAG conservées sans statut | Nombre de sorties RAG gardées sans indication de statut ou de périmètre d'usage. | Empêche de traiter une sortie exploratoire comme preuve ou source. | Identifier les livrables RAG conservés et compter ceux qui n'ont pas de statut explicite. | Moyenne | Faible |
| Nombre d'objets temporaires utilisés comme objets canoniques | Nombre de livrables temporaires ou expérimentaux utilisés comme sources, registres ou documents maîtres. | Détecte les inversions de statut documentaire. | Repérer les références à des objets temporaires dans des documents ou emplacements canoniques. | Élevée | Faible |
| Nombre de livrables suspects non traités | Nombre de livrables qualifiés comme suspects sans décision de traitement. | Mesure le stock d'éléments à clarifier avant réutilisation forte. | Compter les livrables ou passages marqués suspects et non requalifiés. | Moyenne | Faible |

## Axe 6 — Génération

| Indicateur | Définition | Intérêt | Mode de calcul théorique | Difficulté | Automatisabilité estimée |
| --- | --- | --- | --- | --- | --- |
| Nombre d'artefacts désynchronisés | Nombre d'artefacts générés qui diffèrent de leur sortie canonique attendue. | Signale les écarts qui ne doivent pas être corrigés manuellement. | Comparer les artefacts versionnés aux sorties produites par les outils canoniques. | Moyenne | Élevée |
| État de `check-generated-sync` | Statut du contrôle de synchronisation des artefacts générés lorsqu'il est exécuté. | Donne un signal rapide sur la cohérence des artefacts couverts. | Relever le statut du contrôle sans en déduire de succès non attesté. | Faible | Élevée |
| État de `STATUS.md` | État du snapshot `STATUS.md` par rapport à son producteur technique attendu. | Vérifie que le statut de dépôt n'est pas traité comme texte manuel. | Comparer `STATUS.md` à la sortie attendue de `tools/generate_status.py` dans un contexte autorisé. | Faible | Élevée |
| Nombre d'artefacts générés sans producteur identifié | Nombre d'artefacts conservés dont le script ou pipeline producteur n'est pas identifié. | Clarifie la provenance technique avant tout contrôle automatique. | Inventorier les artefacts conservés et vérifier l'existence d'un producteur documenté. | Moyenne | Moyenne |

# Classification des indicateurs

| Indicateur | Valeur stratégique | Difficulté | Priorité |
|------------|--------------------|-------------|----------|
| Nombre de DM traçables vers les atomes | Établit l'ancrage minimal des documents maîtres. | Élevée | P0 |
| Pourcentage de DM traçables vers les registres | Protège les entités, relations et libellés canoniques repris dans les DM. | Moyenne | P0 |
| Taux de dérivabilité des documents maîtres | Mesure la capacité à reconstruire les vues rédactionnelles depuis le corpus exporté. | Élevée | P0 |
| Nombre de DM potentiellement obsolètes | Signale les vues les plus sensibles à requalifier avant usage. | Moyenne | P0 |
| Nombre de divergences DM/corpus | Mesure les écarts structurants entre vue rédactionnelle et socle documentaire. | Élevée | P0 |
| Nombre d'artefacts désynchronisés | Protège la reproductibilité des artefacts générés. | Moyenne | P1 |
| État de `check-generated-sync` | Donne un signal de synchronisation sur les artefacts couverts. | Faible | P1 |
| Nombre de livrables non qualifiés | Réduit l'ambiguïté de statut des livrables conservés. | Moyenne | P1 |
| Nombre de sorties RAG conservées sans statut | Empêche la confusion entre exploration RAG, preuve et source. | Moyenne | P1 |
| Nombre de divergences registre/export | Vérifie la cohérence entre registres et vues générées. | Moyenne | P1 |
| Nombre d'informations non dérivables | Identifie les contenus les plus risqués du point de vue documentaire. | Élevée | P1 |
| Nombre de livrables plus anciens que leurs dépendances | Donne un signal d'obsolescence hors documents maîtres. | Moyenne | P2 |
| Âge moyen des documents maîtres | Fournit une indication de fraîcheur, moins probante qu'une comparaison de dépendances. | Faible | P2 |
| Nombre de contradictions documentaires ouvertes | Suit les contradictions qui appellent un arbitrage humain. | Moyenne | P2 |
| Nombre d'artefacts générés sans producteur identifié | Prépare la fiabilisation des contrôles de génération. | Moyenne | P2 |
| Nombre de livrables suspects non traités | Suit le stock d'éléments à clarifier. | Moyenne | P3 |

# Tableau de bord minimal viable

## MVP du tableau de bord M1

Le MVP du tableau de bord M1 devrait rester limité à un ensemble court d'indicateurs donnant rapidement une vision globale de la santé documentaire du projet.

| Indicateur | Justification |
| --- | --- |
| Nombre de DM traçables vers les atomes | Couvre l'ancrage documentaire minimal des documents maîtres. |
| Pourcentage de DM traçables vers les registres | Vérifie l'alignement avec les objets canoniques. |
| Taux de dérivabilité des documents maîtres | Mesure la reconstructibilité des vues rédactionnelles persistantes. |
| Nombre de DM potentiellement obsolètes | Signale les vues sensibles à vérifier avant réutilisation. |
| Nombre de divergences DM/corpus | Repère les incohérences structurantes entre vue et socle. |
| Nombre de divergences registre/export | Contrôle la cohérence entre objets persistants et vues générées. |
| Nombre d'artefacts désynchronisés | Suit les écarts de génération sans correction manuelle. |
| État de `check-generated-sync` | Fournirait un signal rapide sur les artefacts couverts par le mécanisme de synchronisation existant. |
| Nombre de livrables non qualifiés | Mesure l'ambiguïté documentaire qui peut contaminer les usages. |
| Nombre de sorties RAG conservées sans statut | Protège la distinction entre exploration RAG, preuve et source. |

Ces indicateurs ne sont pas calculés dans cette PR. Ils définissent seulement le périmètre souhaitable d'une première vision qualité.

# Tableau de bord complet

## Version étendue

Une version étendue pourrait ajouter :

- pourcentage de DM traçables vers les sources ;
- nombre de livrables RAG conservés avec rattachement documentaire explicite ;
- nombre d'informations non dérivables ;
- nombre de passages suspects ;
- nombre de livrables conservés sans reconstruction possible ;
- nombre de livrables plus anciens que leurs dépendances ;
- âge moyen des documents maîtres ;
- nombre de livrables nécessitant une régénération ;
- nombre de contradictions documentaires ouvertes ;
- nombre de divergences non arbitrées ;
- nombre d'objets temporaires utilisés comme objets canoniques ;
- nombre de livrables suspects non traités ;
- état de `STATUS.md` ;
- nombre d'artefacts générés sans producteur identifié.

Cette version étendue ne doit être envisagée qu'après validation du MVP documentaire et des règles de qualification des écarts.

# Hors périmètre

Les sujets suivants sont explicitement hors périmètre de ce document :

- enrichissement documentaire ;
- formulaires d'ajout ;
- nouvelles applications ;
- migration Cloudflare ;
- évolution du RAG ;
- évolution de l'Atelier / Forge ;
- évolution de la Collection.

Ils ne sont pas ouverts par cette PR.

# Préparation de la suite

## Étape suivante de M1

Après validation documentaire du tableau de bord, les contrôles P0 les plus susceptibles d'être implémentés dans des PR dédiées seraient :

- DM -> atomes ;
- DM -> registres ;
- DM -> exports ;
- information présente dans un DM mais absente du corpus ;
- divergence entre DM et corpus.

Ces contrôles ne sont pas implémentés ici. Leur éventuelle automatisation devra faire l'objet d'une décision séparée, avec un périmètre explicite, des preuves attendues et une règle claire pour éviter toute correction manuelle d'artefacts générés.
