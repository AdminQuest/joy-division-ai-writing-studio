# Roadmap strategique 2026

| Champ | Valeur |
| --- | --- |
| Version | 2.0 |
| Date | 2026-06-04 |
| Auteur de la revision | Codex, sur instruction utilisateur |
| Statut | roadmap strategique additive |

## Journal des modifications

| Evolution | Description |
| --- | --- |
| Ajout d'un bloc de versionnement | Le document indique sa version, sa date, son auteur de revision et son statut additif. |
| Ajout d'une table de rattachement initiale | Les chantiers deja identifies sont rattaches aux jalons M0 a M7 sans remplacer les decoupages techniques existants. |
| Criteres M0 et M1 rendus verifiables | Les criteres qualitatifs initiaux sont completes par des criteres observables et controlables. |
| Definition d'un tableau de bord qualite | Le tableau de bord est defini comme artefact genere par le build, sans comptage manuel stable. |
| Decision Cloudflare Pages + Zero Trust | Cloudflare Pages et Zero Trust sont inscrits comme decision d'architecture M3, non comme hypothese immediate. |
| Clarification M0 // M1 et verrou M2 | M0 et M1 progressent en parallele ; M2 reste interdit tant que M0 et M1 ne sont pas clotures. |
| Contraintes PR automatisees et GITHUB_TOKEN | Les limites d'automatisation, de validation humaine et de declenchement des workflows sont explicitees. |

## Gouvernance

Cette roadmap strategique ne remplace pas la roadmap technique existante. Elle fournit une couche de lecture superieure. Toute tache technique existante doit etre conservee, mais rattachee progressivement a l'un des jalons M0 a M7.

Ce document sert de repere stable pour un lecteur humain comme pour un assistant IA reprenant le projet dans une semaine ou dans un mois. Il ne supprime aucun decoupage existant, ne remplace aucun suivi technique et ne lance pas de chantier de fusion des repos.

## Calendrier de decision

- **Activable immediatement** : M0 et M1 uniquement.
- **Progression parallele** : M0 et M1 progressent en parallele.
- **Verrou M2** : M2 reste interdit tant que M0 et M1 ne sont pas clotures.
- **Prochain, pas avant une semaine** : M2, apres stabilisation documentee de M0 et M1.
- **Ulterieur** : M3 a M7.
- **Interdits pour les prochains jours** : fusion des repos, refonte d'interface, nouveau developpement d'enrichment-studio.

## Prochaines actions autorisees

Pour les prochains jours, seules les actions suivantes sont autorisees :

- documenter M0 ;
- documenter M1 ;
- auditer les registres ;
- auditer les exports ;
- renforcer les validations ;
- produire un tableau de bord qualite ;
- clarifier les dependances ;
- ne pas lancer M2 ;
- ne pas fusionner les repos ;
- ne pas refondre l'interface.

## Commandes de controle de reference

Les controles de reference distinguent la generation de STATUS.md et le controle global du pipeline.

```bash
python3 tools/generate_status.py
python3 tools/build_all.py
python3 tools/check_generated_sync.py
python3 tools/audit_repo.py
git status
```

`tools/generate_status.py` est le generateur direct de STATUS.md. `tools/build_all.py` reste le controle global du pipeline registres / documents maitres / exports / audits.

`tools/check_generated_sync.py` ne couvre pas necessairement STATUS.md. La fraicheur de STATUS.md est donc assuree par l'execution explicite de `tools/generate_status.py` et par le commit du snapshot regenere lorsque celui-ci differe.

STATUS.md est un snapshot genere. Il doit etre regenere immediatement avant son commit lorsque la roadmap, les audits ou les artefacts de pilotage changent. Les metadonnees de branche et de commit indiquent le HEAD source utilise par `tools/generate_status.py` au moment de produire le snapshot. Le commit qui inclut STATUS.md peut etre posterieur, car un fichier ne peut pas contenir le SHA du commit qui depend lui-meme de ce fichier.

## Vue d'ensemble

| Milestone | Statut | Priorite | Intention |
| --- | --- | --- | --- |
| M0 — Stabilisation du socle | immediat | P0 | Comprendre et consolider l'existant. |
| M1 — Fiabilisation du corpus | immediat | P0 | Reduire le risque d'integration documentaire. |
| M2 — Studio d'enrichissement documentaire | prochain, pas avant une semaine | P1 | Industrialiser les ajouts apres stabilisation. |
| M3 — Corpus prive unifie | ulterieur | P2 | Preparer repo unique prive et deploiement protege. |
| M4 — Studio de redaction | ulterieur | P2 | Clarifier les outils de redaction sans refonte immediate. |
| M5 — Fonds documentaire multimedia | ulterieur | P3 | Structurer photos, scans, bootlegs, videos et documents rares. |
| M6 — Assistant historiographique | ulterieur | P3 | Exploiter relations, concepts, motifs, mythes et argumentation. |
| M7 — Publication et perennisation | ulterieur | P3 | Preparer exports, sauvegarde et publication durable. |

## Table de rattachement initiale des chantiers

Un chantier peut se rattacher a plusieurs jalons selon sa phase : documentation, fiabilisation, enrichissement, redaction, publication ou perennisation. Le rattachement ne remplace pas les decoupages techniques existants ; il fournit une lecture strategique de leur fonction.

| Chantier | Statut | Jalon(s) | Phase / justification |
| --- | --- | --- | --- |
| Step 9 — registre PERSON- | clos | M0 + M1 | Documente en M0 ; invariants, attributions et controles en M1. |
| Step 10 — registre ORG- | clos | M0 + M1 | Documente en M0 ; coherence canonique et controles en M1. |
| Step 11 — registre IMAGE- | clos | M0 + M1 + M5 | Documente en M0 ; invariants image/session/personne en M1 ; droits, provenance et multimedia en M5. |
| Enrichissement geo PLACE- | partiel | M0 + M1 | Inventaire en M0 ; precision, sources et coherence geographique en M1. |
| Atomisation S93/S94, documents maitres | clos | M0 | Etat du corpus documentaire et des documents maitres. |
| sync_dm_to_claude_kb.py | actif | M0 | Dependance build vers base de connaissance Claude a cartographier. |
| Generation STATUS.md | actif | M0 | Livrable socle de M0, a consolider et non a recreer. |
| Step 12 — cross-registres profond | en cours | M1 | Fiabilite inter-registres ; blocages pouvant preparer M2. |
| Tracklists + cle etrangere song_id dans les releases | a faire | M1 | Structure et fiabilite du corpus releases. |
| Deep-link par variante | a faire | M1 -> M2 | Pre-requis de fiabilite, puis surface d'usage ou d'ajout. |
| Application registre-concerts | existant, a auditer | M0 + M1 -> M2 (formulaire) | L'application de consultation existe deja et doit etre inventoriee, auditee et documentee en M0 ; les donnees et liens concerts relevent de M1 ; seul le futur formulaire d'ajout releve de M2. |
| Fiche personne avec deep-link ?id= | differe | M1 / M2 | Rattache a la passe 12b-2.c-extended ; fiabilite d'abord, ergonomie ensuite. |
| Chantiers RAG / manuscript-studio | experimental | M4 | Roles a clarifier sans refonte immediate. |
| Collection personnelle | actif | M0 + M3 + M5 | Inventaire en M0 ; integration au repo unique prive en M3 ; medias, objets et droits en M5. |
| Migration Cloudflare Pages + Zero Trust | decide, non lance | M3 | Decision d'architecture ; migration ulterieure apres stabilisation M0/M1. |

L'application de consultation du registre concerts appartient au perimetre des applications existantes a inventorier et a auditer ; elle ne doit pas etre recreee. Le point ouvert concerne uniquement les ameliorations futures et le formulaire d'ajout, qui relevent de M2.

## M0 — Stabilisation du socle

**Statut** : immediat.

**Priorite** : P0.

**Objectif** : consolider ce qui existe deja et rendre l'etat reel du projet lisible sans relire tout l'historique des PR, audits et corrections.

**Perimetre** :

- applications publiques existantes ;
- registres canoniques ;
- exports generes ;
- audits documentaires ;
- RAG Studio ;
- manuscript-studio ;
- documents maitres ;
- dependances entre outils de build, validation et publication.

**Livrables** :

- etat des applications actuelles ;
- etat des registres ;
- etat des exports ;
- etat des audits ;
- etat du RAG Studio ;
- etat du manuscript-studio ;
- etat des documents maitres ;
- cartographie des dependances entre outils.

**Criteres de sortie** :

M0 est termine si :

- STATUS.md se regenere sans erreur via tools/generate_status.py, puis le snapshot regenere est committe lorsqu'il differe ;
- les artefacts generes couverts par la sentinelle sont verifies par check-generated-sync ;
- build_all.py reste le controle global du pipeline registres / documents maitres / exports / audits, mais il n'est pas presente comme le generateur direct de STATUS.md sauf s'il appelle explicitement tools/generate_status.py ;
- check-generated-sync est au vert sur la derniere PR ;
- l'inventaire des applications existantes est disponible et date ;
- l'inventaire des registres canoniques est disponible, avec volumetrie ;
- la table des dependances build / validation / publication est disponible ;
- la table de rattachement initiale est renseignee ;
- les limites connues sont distinguees des anomalies dans une liste explicite ;
- aucun chantier M2 n'est lance.

Note : le pathspec complet attendu couvre au minimum les chemins suivants.

| Groupe | Pathspec minimal |
| --- | --- |
| Registres | `registers/` |
| Exports generes | `exports/generated/` |
| Documents maitres par chapitre | `chapters/*/document_maitre.md` |
| Manifest documents maitres | `chapters/master_docs.json` |

**Liens avec la roadmap existante** :

- rattache les lots techniques de stabilisation deja ouverts ou recemment traites ;
- fournit un niveau de lecture au-dessus des lots C3A, des audits de registres et des correctifs d'exports ;
- ne remplace pas les decoupages techniques existants.

**Risques** :

- confondre documentation d'etat et refonte ;
- ouvrir trop vite M2 avant d'avoir stabilise les invariants ;
- laisser des exports ou applications implicites non cartographies.

## M1 — Fiabilisation du corpus

**Statut** : immediat.

**Priorite** : P0.

**Objectif** : rendre l'ajout d'informations plus sur, sans encore creer de formulaires ni automatiser un nouveau studio d'enrichissement.

**Perimetre** :

- schemas ;
- validateurs ;
- controles croises entre registres ;
- conventions d'identifiants ;
- regles de source, provenance et droits ;
- anomalies recentes, notamment les cas d'integration iconographique comme Pennie Smith.

**Livrables** :

- validations renforcees ;
- controles croises entre registres ;
- audit des cas recents comme Pennie Smith ;
- liste des anomalies connues ;
- tableau de bord qualite minimal ;
- regles d'identifiants canoniques ;
- regles de source, provenance et droits.

**Criteres de sortie** :

M1 est termine si :

- le nombre de liens inter-registres orphelins est nul sur le perimetre publie ;
- le nombre d'identifiants canoniques dupliques est nul ;
- les invariants critiques sont au vert ;
- la validation de schema atteint le seuil attendu ;
- le tableau de bord qualite est genere et publie ;
- l'audit du cas Pennie Smith est clos et documente ;
- les regles de source, de provenance et de droits sont ecrites et appliquees ;
- les champs de provenance sont isoles des facettes documentaires, verification a l'appui ;
- aucun champ de type sources ne contient d'identifiant interne inadapte comme IMAGE-* lorsqu'il doit contenir des sources documentaires SNN.

Les invariants critiques incluent explicitement le maintien de la distinction entre Kevin Curtis et Ian Curtis au niveau du validateur.

| Critere numerique | Seuil |
| --- | --- |
| Liens inter-registres orphelins sur le perimetre publie | 0 |
| Identifiants canoniques dupliques | 0 |
| Validation de schema | 100 % |

## Tableau de bord qualite minimal

Le tableau de bord qualite est un artefact genere par le build, jamais un comptage manuel.

Toute metrique susceptible d'etre calculee par le depot doit etre generee automatiquement. Une tache de comptage manuel qui peut etre automatisee ne constitue pas un livrable stable.

| Bloc | Champs | Seuil |
| --- | --- | --- |
| Volumetrie | sources, personnes, organisations, lieux, concerts, images, variantes de releases, possessions, chansons | informatif |
| Integrite | liens casses, identifiants dupliques, exports en echec, schemas invalides | = 0 |
| Verification | taux global de verification, taux par registre, dont releases | suivi de tendance |

Les valeurs ne sont pas codees en dur. Elles sont calculees a la generation. Les chiffres connus peuvent servir de ligne de base, mais ils ne sont pas saisis manuellement dans la roadmap.

| Exemple de metrique deja disponible | Valeur indicative | Regle |
| --- | --- | --- |
| Taux de verification releases | 86,6 % | Exemple seulement ; la valeur doit etre regeneree automatiquement. |

**Liens avec la roadmap existante** :

- prolonge les audits C3A sur les registres, les lieux, les relations et les images ;
- consolide les invariants introduits par les schemas et validateurs existants ;
- prepare les conditions minimales avant tout studio d'ajout.

**Risques** :

- multiplier les exceptions de schema pour un cas ponctuel ;
- confondre URL de consultation, source documentaire et source canonique ;
- publier des donnees multimedia dont les droits ou l'identite restent incertains.

## M2 — Studio d'enrichissement documentaire

**Statut** : prochain, pas avant une semaine.

**Priorite** : P1.

**Objectif** : industrialiser les ajouts documentaires une fois M0 et M1 stabilises.

**Perimetre futur** :

- ajout d'images ;
- ajout de personnes ;
- ajout de sources ;
- ajout de concerts ;
- ajout de releases ;
- ajout de citations ;
- generation d'identifiants ;
- controles avant commit ;
- ouverture de PR automatisee.

**Livrables futurs** :

- formulaire d'ajout image ;
- formulaire d'ajout personne ;
- formulaire d'ajout source ;
- formulaire d'ajout concert ;
- formulaire d'ajout release ;
- formulaire d'ajout citation ;
- generation automatique des IDs ;
- controles avant commit ;
- PR automatique.

**Criteres de sortie** :

- les ajouts courants ne passent plus par edition manuelle des JSON ;
- les validateurs bloquent les incoherences avant commit ;
- la provenance et les droits sont renseignes dans les bons champs ;
- les exports sont regeneres de facon reproductible.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

### Contraintes d'automatisation

- l'automatisation peut preparer une branche, generer les identifiants, lancer les controles et ouvrir une PR ;
- elle ne doit pas merger ;
- elle ne doit pas contourner la validation humaine ;
- le principe "aucun commit sans validation humaine" reste applicable ;
- les limites du GITHUB_TOKEN doivent etre prises en compte, notamment le fait qu'il ne declenche pas necessairement les workflows attendus sur pull_request ;
- si une automatisation de PR est developpee, elle doit utiliser une methode compatible avec les verifications requises ou documenter ses limites ;
- le workflow update-status abandonne ou problematique constitue une contrainte historique a prendre en compte.

**Liens avec la roadmap existante** :

- depend des invariants et audits de M1 ;
- ne doit pas court-circuiter les lots techniques existants ;
- pourra rattacher les futurs formulaires aux registres deja stabilises.

**Risques** :

- lancer trop tot un outil qui encode des regles encore instables ;
- creer des raccourcis UI qui contournent les schemas ;
- confondre ergonomie d'ajout et validation historiographique.

## M3 — Corpus prive unifie

**Statut** : ulterieur.

**Priorite** : P2.

**Objectif** : preparer une architecture cible autour d'un repo prive unifie, d'un deploiement Cloudflare Pages et d'un acces Zero Trust.

Decision d'architecture : la cible retenue est un depot prive unique publie via Cloudflare Pages, protege par Cloudflare Zero Trust. Cette decision n'est pas activee immediatement : elle releve de M3 et reste interdite tant que M0 et M1 ne sont pas clotures.

Le devenir de l'abonnement Pages Pro existant doit etre inventorie dans M3 afin d'eviter un cout orphelin ou une infrastructure residuelle inutile.

Cloudflare est decide ; le calendrier de migration n'est pas lance. La fusion des repos reste interdite a ce stade. L'objectif est un repo prive unique, mais seulement dans M3.

**Perimetre futur** :

- architecture cible ;
- strategie de migration ;
- preservation des deux roadmaps ;
- integration studio, registres et collection ;
- absence de perte de donnees.

**Livrables futurs** :

- note d'architecture cible ;
- inventaire des repos et flux a rapprocher ;
- plan de migration reversible ;
- strategie de sauvegarde ;
- matrice des donnees a conserver.

**Criteres de sortie** :

- aucun repo n'est fusionne sans plan valide ;
- les roadmaps existantes sont conservees ;
- les donnees publiques et privees sont distinguees ;
- les risques de perte ou d'ecrasement sont documentes.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- rattache les chantiers techniques d'infrastructure, de publication et de securisation ;
- doit rester posterieur a M0 et M1.

**Risques** :

- fusion prematuree des repos ;
- perte de contexte entre corpus public, corpus prive et studios ;
- complexite Cloudflare/Zero Trust introduite avant stabilisation documentaire.

## M4 — Studio de redaction

**Statut** : ulterieur.

**Priorite** : P2.

**Objectif** : clarifier les roles respectifs du RAG Studio, du manuscript-studio et des documents maitres.

**Perimetre** :

- documentation des questions ouvertes ;
- cartographie des flux entre registres, RAG et documents maitres ;
- clarification des usages reels avant refonte.

**Livrables futurs** :

- note de cadrage RAG Studio / manuscript-studio ;
- inventaire des fonctions utiles et inutiles ;
- liste des frictions observees en usage reel ;
- recommandations sans refonte immediate.

**Criteres de sortie** :

- les roles des outils de redaction sont distingues ;
- les documents maitres restent preserves ;
- aucune refonte n'est lancee sans retour d'usage.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- prolonge les decisions indiquant que le Studio est en experimentation reelle ;
- rattache les futurs lots UI/redaction sans les activer maintenant.

**Risques** :

- refondre l'interface avant retour d'usage ;
- melanger outil de consultation, outil d'enrichissement et outil de redaction ;
- modifier les documents maitres au lieu de documenter le flux.

## M5 — Fonds documentaire multimedia

**Statut** : ulterieur.

**Priorite** : P3.

**Objectif** : integrer prudemment photos, scans, bootlegs, videos, affiches, tickets et documents rares.

**Perimetre futur** :

- registre images ;
- registres bootlegs et archives ;
- documents multimedia externes ;
- droits, provenance et restrictions de publication.

**Livrables futurs** :

- politique de droits et republication ;
- modele de reference externe ;
- inventaire des supports ;
- criteres d'exposition publique ;
- liens avec personnes, concerts, lieux, sessions et releases.

**Criteres de sortie** :

- aucun media n'est republie sans clarification des droits ;
- les references externes restent consultables sans casser le modele canonique ;
- les liens inter-registres multimedia sont exploitables.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- consolide les travaux recents sur le registre images ;
- rattache les futurs enrichissements issus de joydiv.org ou d'autres fonds.

**Risques** :

- importer des images sans droits ;
- creer des namespaces opportunistes ;
- confondre canal de diffusion et source intellectuelle.

## M6 — Assistant historiographique

**Statut** : ulterieur.

**Priorite** : P3.

**Objectif** : exploiter les relations, concepts, motifs, mythes et chaines argumentatives pour assister l'analyse historiographique.

**Perimetre futur** :

- graphe documentaire ;
- concepts ;
- motifs ;
- mythes ;
- citations ;
- sources ;
- relations inter-registres ;
- chaines argumentatives.

**Livrables futurs** :

- requetes historiographiques types ;
- tableaux de preuves ;
- chemins source -> concept -> chapitre ;
- aide a la detection de contradictions ;
- syntheses argumentatives controlees.

**Criteres de sortie** :

- l'assistant sait citer ses points d'appui ;
- les hypotheses restent distinguees des faits documentes ;
- les mythes et motifs sont relies aux sources et chapitres.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- valorise les registres concepts, motifs, mythes, citations et chronologie ;
- depend de la qualite des relations inter-registres.

**Risques** :

- produire des syntheses trop affirmatives ;
- masquer les incertitudes documentaires ;
- utiliser le graphe comme preuve sans retour aux sources.

## M7 — Publication et perennisation

**Statut** : ulterieur.

**Priorite** : P3.

**Objectif** : preparer les exports, sauvegardes, publications partielles ou totales et la documentation durable du projet.

**Perimetre futur** :

- publication publique ;
- publication privee ;
- sauvegardes ;
- exports ;
- documentation utilisateur et technique ;
- preservation des donnees.

**Livrables futurs** :

- strategie de publication ;
- plan de sauvegarde ;
- documentation de reprise par assistant IA ;
- politique de versionnement ;
- criteres de publication partielle ou totale.

**Criteres de sortie** :

- le projet peut etre repris sans dependance a une memoire conversationnelle ;
- les exports essentiels sont reproductibles ;
- les choix de publication sont documentes ;
- les donnees privees et publiques sont separees.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- rattache les lots de publication, sauvegarde, deploiement et documentation finale ;
- ne remplace aucun suivi technique.

**Risques** :

- publier trop tot un corpus instable ;
- exposer des donnees privees ;
- documenter la surface publique sans documenter la reproductibilite.

## Regle de rattachement progressif

Chaque nouveau lot technique doit indiquer explicitement son rattachement a l'un des jalons M0 a M7. Les lots deja existants peuvent etre rattaches progressivement, sans redecoupage brutal ni perte des references historiques.

Priorite actuelle : documenter et fiabiliser. Les outils nouveaux viennent ensuite.
