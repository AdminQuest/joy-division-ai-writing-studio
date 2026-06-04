# Roadmap strategique 2026

## Gouvernance

Cette roadmap strategique ne remplace pas la roadmap technique existante. Elle fournit une couche de lecture superieure. Toute tache technique existante doit etre conservee, mais rattachee progressivement a l'un des jalons M0 a M7.

Ce document sert de repere stable pour un lecteur humain comme pour un assistant IA reprenant le projet dans une semaine ou dans un mois. Il ne supprime aucun decoupage existant, ne remplace aucun suivi technique et ne lance pas de chantier de fusion des repos.

## Calendrier de decision

- **Activable immediatement** : M0 et M1 uniquement.
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

- un assistant IA peut comprendre l'etat reel du repo sans relire tout l'historique ;
- les principaux artefacts generes sont identifies ;
- les dependances critiques entre registres, exports et applications sont explicites ;
- les limites connues sont distinguees des anomalies a corriger.

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

- une information nouvelle peut etre integree avec un risque reduit de casse ;
- les champs de provenance ne polluent pas les facettes documentaires ;
- les liens inter-registres sont verifies avant publication ;
- les cas sans droits etablis restent reference-only ou documentes sans republication.

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
