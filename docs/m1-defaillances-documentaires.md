# Défaillances documentaires M1

# Objet du document

M1 vise à fiabiliser le système documentaire dans le temps. Il doit permettre de détecter, qualifier et traiter les écarts qui fragilisent la traçabilité, la dérivabilité, l'obsolescence, la cohérence documentaire ou le statut des livrables.

Ce document ne crée pas de script. Il définit les types de défaillances que les futurs contrôles M1 devront détecter.

Il ne corrige aucun écart existant et ne modifie pas les décisions M0. Les documents maîtres restent des vues rédactionnelles persistantes du corpus exporté, produites techniquement par `tools/build_master_docs.py`.

# Doctrine M1

M1 porte sur :

- traçabilité ;
- dérivabilité ;
- obsolescence ;
- cohérence documentaire ;
- statut des livrables.

M1 doit permettre de vérifier qu'un livrable documentaire conservé peut être relié au corpus, reconstruit ou expliqué depuis les objets documentaires disponibles, comparé à ses dépendances et qualifié par un statut explicite.

M1 ne doit pas :

- enrichir le corpus ;
- créer des formulaires ;
- refondre les applications ;
- lancer Cloudflare ;
- ouvrir M2.

# Typologie des défaillances documentaires

## Défaillance de traçabilité

Définition : une information présente dans un livrable documentaire ne peut plus être reliée à une source, un atome, un registre, un export ou un script de génération.

Exemples :

- un passage de document maître affirme un fait sans source ou atome identifiable ;
- une citation reprise dans un livrable conservé ne renvoie plus à son origine ;
- un livrable RAG conservé ne précise pas les registres ou exports utilisés ;
- un document généré ne permet pas d'identifier le script qui l'a produit.

Gravité indicative : majeure si l'information est réutilisée dans un document maître ou un livrable conservé ; bloquante si elle fonde une décision documentaire sans preuve retrouvable.

Preuve attendue : absence de lien ou de référence vérifiable vers une source, un atome, un registre, un export, un manifeste ou un script de génération.

Action de traitement possible : qualifier l'information comme suspecte, retrouver l'ancrage documentaire, ajouter la référence manquante dans l'objet canonique approprié ou retirer l'information du livrable conservé.

## Défaillance de dérivabilité

Définition : une information présente dans un document maître ou un livrable conservé ne peut pas être reconstruite à partir du corpus exporté.

Exemples :

- une synthèse de chapitre contient une interprétation qui ne peut être dérivée d'aucun export ;
- un document maître contient une chronologie différente de celle reconstruite depuis les atomes disponibles ;
- une relation entre deux entités apparaît dans un livrable conservé sans correspondance dans les registres ou exports ;
- un passage mélange plusieurs faits documentés mais produit une conclusion qui n'est pas justifiée par le corpus.

Gravité indicative : majeure par défaut ; bloquante si l'information non dérivable est présentée comme stable, canonique ou prête à publier.

Preuve attendue : comparaison entre le contenu du livrable et les sources, atomes, registres ou exports disponibles montrant que l'information ne peut pas être reconstruite.

Action de traitement possible : déclasser le passage, documenter son statut d'hypothèse, l'adosser à des objets persistants vérifiables ou le supprimer du livrable conservé.

## Défaillance d'obsolescence

Définition : un livrable conservé, notamment un document maître, ne reflète plus l'état courant du corpus, des registres ou des exports.

Exemples :

- un document maître conserve un ancien libellé d'entité après mise à jour d'un registre ;
- un export généré a changé mais le livrable qui en dépend n'a pas été régénéré ou requalifié ;
- `STATUS.md` ou un audit documente un état antérieur sans indiquer son périmètre temporel ;
- une synthèse conservée repose sur des atomes qui ont été remplacés, déplacés ou corrigés.

Gravité indicative : mineure si l'écart est explicitement daté et sans usage actif ; majeure si le livrable est encore utilisé ; bloquante si l'obsolescence masque un changement documentaire significatif.

Preuve attendue : différence vérifiable entre le livrable conservé et l'état courant des sources, atomes, registres, exports ou scripts dont il dépend.

Action de traitement possible : marquer le livrable comme obsolète, le régénérer avec l'outil canonique si son statut le prévoit, ou documenter la réserve avant réutilisation.

## Défaillance de cohérence documentaire

Définition : deux objets documentaires du dépôt affirment simultanément des informations incompatibles sans signaler la contradiction.

Exemples :

- un registre et un document maître utilisent deux statuts différents pour la même entité ;
- deux exports générés présentent des valeurs incompatibles pour un même identifiant ;
- une chronologie et une note de chapitre placent le même événement à deux dates différentes ;
- un audit signale un écart alors qu'un autre document le présente comme résolu sans justification.

Gravité indicative : majeure si l'incompatibilité concerne un objet canonique ou un document maître ; bloquante si elle rend impossible l'interprétation fiable d'un livrable.

Preuve attendue : identification des deux objets concernés, des passages ou champs incompatibles, et absence de note expliquant la contradiction.

Action de traitement possible : signaler l'écart, choisir l'objet canonique de référence, qualifier l'un des objets comme suspect ou obsolète, puis traiter la divergence dans le jalon approprié.

## Défaillance de statut documentaire

Définition : un livrable temporaire, expérimental ou non canonique est utilisé comme s'il était une source, un registre ou un document maître.

Exemples :

- une sortie RAG est citée comme preuve documentaire ;
- une note de travail est reprise comme registre canonique ;
- un brouillon de chapitre est traité comme document maître ;
- un export exploratoire est conservé sans statut puis utilisé dans une synthèse stable.

Gravité indicative : mineure si l'usage est isolé et sans effet documentaire ; majeure si le livrable circule comme référence ; bloquante si une source de vérité est remplacée par un objet non qualifié.

Preuve attendue : usage explicite ou implicite d'un livrable non canonique comme preuve, source, registre, document maître ou artefact généré officiel.

Action de traitement possible : attribuer un statut documentaire explicite, déplacer l'objet hors du périmètre canonique si nécessaire, ou remplacer la référence par un objet persistant qualifié.

## Défaillance de génération

Définition : un artefact généré diffère de sa sortie canonique ou a été modifié manuellement.

Exemples :

- un export généré ne correspond plus à la sortie de son script canonique ;
- un document maître a été corrigé directement au lieu d'être reconstruit par `tools/build_master_docs.py` ;
- `STATUS.md` diffère de la sortie attendue de `tools/generate_status.py` ;
- un artefact couvert par `tools/check_generated_sync.py` présente un écart non régénéré.

Gravité indicative : majeure par défaut ; bloquante si l'artefact généré sert de base à une validation, une publication ou une décision de jalon.

Preuve attendue : diff reproductible entre l'artefact versionné et la sortie canonique du script, historique de modification manuelle, ou échec d'un contrôle de synchronisation générée.

Action de traitement possible : ne pas corriger l'artefact à la main, régénérer avec l'outil canonique lorsque le périmètre de la PR l'autorise, ou signaler l'écart comme réserve si la PR est uniquement documentaire.

# Grille de gravité

| Gravité | Critères de classement |
| --- | --- |
| Bloquant | L'écart empêche de considérer un livrable, un registre, un export ou un critère de jalon comme fiable avant décision ou merge. |
| Majeur | L'écart affecte un objet conservé, canonique ou réutilisé, mais peut être isolé, qualifié ou traité dans un jalon identifié. |
| Mineur | L'écart est local, explicite, daté ou sans impact direct sur la source de vérité documentaire. |
| Informationnel | Le constat améliore la compréhension du dépôt sans exiger de correction immédiate. |

Le classement doit tenir compte de l'objet touché, de son statut documentaire, de sa réutilisation effective, de la possibilité de reproduire l'écart et du risque de propagation vers les documents maîtres, exports, audits ou décisions de jalon.

# Objets concernés

Les défaillances M1 peuvent concerner :

- sources ;
- atomes ;
- registres ;
- citations ;
- chronologies ;
- entités ;
- relations ;
- exports générés ;
- documents maîtres ;
- livrables RAG conservés ;
- audits ;
- `STATUS.md`.

# Sortie attendue de M1

Ce document prépare les futurs contrôles M1 :

- audit de traçabilité ;
- audit de dérivabilité ;
- audit d'obsolescence ;
- tableau de bord qualité ;
- règles de traitement des écarts.

Ces contrôles ne sont pas créés dans cette PR. Leur définition technique, leur automatisation éventuelle et leur intégration au pipeline devront faire l'objet de décisions et de PR dédiées.
