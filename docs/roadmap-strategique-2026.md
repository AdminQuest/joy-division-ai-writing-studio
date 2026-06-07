# Roadmap strategique 2026

| Champ | Valeur |
| --- | --- |
| Version | 2.3 |
| Date | 2026-06-07 |
| Auteur de la revision | Assistant, sur instruction utilisateur |
| Statut | roadmap strategique additive — roadmap de reference unique |

## Journal des modifications

| Evolution | Description |
| --- | --- |
| Cloture M0, M1 et M2 et lancement M3 (v2.3) | M0 (2026-06-05), M1 (2026-06-06) et M2 (2026-06-06) sont clotures. M3 est lance le 2026-06-07. Les statuts, le calendrier de decision et les actions autorisees sont mis a jour en consequence. |
| Objectif n1 de M3 : depot unique prive derriere Cloudflare Zero Trust (v2.3) | La decision utilisateur leve l'interdiction de fusion : les deux depots public et prive sont destines a etre remplaces par un depot unique, nouveau, prive, expose derriere Cloudflare Zero Trust. Ce chantier impose une reprise de l'architecture globale. |
| Bascule de la dette residuelle M1 en M3 (v2.3) | La dette acceptee a la cloture M1 (tableau de bord qualite complet, audit Pennie Smith, indicateurs consolides, reserves DM -> registres, verification provenance/droits) est reprise comme chantiers M3 sans rouvrir M1. |
| Roadmap de reference unique (v2.3) | L'ancien ROADMAP.md du depot prive a ete supprime. Ce document est la roadmap de reference unique du projet. |
| Perimetre M3 : quatre depots et reagencement leger (v2.3) | Le hub absorbe les quatre depots (public, prive, releases, collection) ; tout devient prive (aucune diffusion publique, y compris releases). Le reagencement est un mapping logique sur cinq espaces, sans deplacement massif de dossiers. |
| Renommage de l'espace corpus : Le Fonds (v2.3) | L'espace corpus + RAG, auparavant nomme « Entrepot », est renomme « Le Fonds ». Les cinq espaces deviennent : La Collection, L'Usine, Le Fonds, L'Atelier, La Vigie. |
| Ajout d'un bloc de versionnement | Le document indique sa version, sa date, son auteur de revision et son statut additif. |
| Ajout d'une table de rattachement initiale | Les chantiers deja identifies sont rattaches aux jalons M0 a M7 sans remplacer les decoupages techniques existants. |
| Criteres M0 et M1 rendus verifiables | Les criteres qualitatifs initiaux sont completes par des criteres observables et controlables. |
| Definition d'un tableau de bord qualite | Le tableau de bord est defini comme artefact genere par le build, sans comptage manuel stable. |
| Decision Cloudflare Pages + Zero Trust | Cloudflare Pages et Zero Trust sont inscrits comme decision d'architecture M3, non comme hypothese immediate. |
| Priorite M3 d'industrialisation documentaire et d'autonomisation du studio prive | Le chantier "Industrialisation documentaire et autonomisation du studio prive" est inscrit au meme niveau strategique que Cloudflare Zero Trust, la securisation des acces et la consolidation applicative. |
| Clarification M0 // M1 et verrou M2 | M0 et M1 progressent en parallele ; M2 reste interdit tant que M0 et M1 ne sont pas clotures. |
| Contraintes PR automatisees et GITHUB_TOKEN | Les limites d'automatisation, de validation humaine et de declenchement des workflows sont explicitees. |

## Gouvernance

Cette roadmap strategique ne remplace pas la roadmap technique existante. Elle fournit une couche de lecture superieure. Toute tache technique existante doit etre conservee, mais rattachee progressivement a l'un des jalons M0 a M7.

Ce document sert de repere stable pour un lecteur humain comme pour un assistant IA reprenant le projet dans une semaine ou dans un mois. Il ne supprime aucun decoupage existant, ne remplace aucun suivi technique et ne lance pas de chantier de fusion des repos.

## Calendrier de decision

- **Clotures** : M0 (2026-06-05), M1 (2026-06-06) et M2 (2026-06-06).
- **Actif** : M3, lance le 2026-06-07.
- **Ulterieur** : M4 a M7.
- **Decision M3 actee** : la fusion des depots n'est plus interdite. Elle devient
  l'objectif n1 de M3 : un depot unique, nouveau, prive, derriere Cloudflare
  Zero Trust. La bascule effective reste conditionnee a une architecture cible
  et un plan de migration valides par decision humaine.

## Prochaines actions autorisees

M3 etant lance, les actions prioritaires autorisees sont :

- concevoir l'architecture cible du depot unique prive (arborescence, surfaces
  internes ex-public / ex-prive, exports, apps, CI, secrets, acces Zero Trust) ;
- produire un plan de migration reversible, sans perte de donnees ni d'historique
  utile ;
- traiter la dette residuelle M1 basculee en M3 (tableau de bord qualite complet,
  audit Pennie Smith, indicateurs consolides, reserves DM -> registres,
  verification provenance / droits) ;
- poursuivre l'industrialisation documentaire (sas d'entree, canonisation
  outillee, preuve de propagation) et l'autonomisation du studio prive ;
- preparer l'exposition Cloudflare Pages + Zero Trust.

Ne pas executer la suppression des depots existants ni la bascule finale tant que
l'architecture cible et le plan de migration ne sont pas valides par decision
humaine.

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

STATUS.md est genere a partir de l'etat de travail observe par `tools/generate_status.py`. La reference git inscrite designe l'etat observe avant le commit du snapshot ; elle ne doit pas etre interpretee comme le hash du commit final contenant STATUS.md. Il ne faut pas chercher a faire correspondre artificiellement cette reference au commit final, car cela creerait une boucle de commits de snapshots. Le fichier doit etre regenere immediatement avant son commit lorsque la roadmap, les audits ou les artefacts de pilotage changent.

## Vue d'ensemble

| Milestone | Statut | Priorite | Intention |
| --- | --- | --- | --- |
| M0 — Stabilisation du socle | cloture (2026-06-05) | P0 | Comprendre et consolider l'existant. |
| M1 — Fiabilisation du corpus | cloture (2026-06-06) | P0 | Reduire le risque d'integration documentaire. |
| M2 — Studio d'enrichissement documentaire | cloture (2026-06-06) | P1 | Industrialiser la preparation des ajouts (le studio prepare, l'humain valide). |
| M3 — Corpus prive unifie | actif (lance 2026-06-07) | P1 | Objectif n1 : depot unique prive derriere Cloudflare Zero Trust ; chaine documentaire industrialisee et autonomisation du studio prive. |
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
| Industrialisation documentaire et autonomisation du studio prive | decide, prioritaire M3 | M3 | Passer d'ajouts documentaires artisanaux a une chaine observable : sas d'entree, canonisation assistee, atomisation reproductible, preuve de propagation et lecture locale maitrisee dans le repo prive. |

L'application de consultation du registre concerts appartient au perimetre des applications existantes a inventorier et a auditer ; elle ne doit pas etre recreee. Le point ouvert concerne uniquement les ameliorations futures et le formulaire d'ajout, qui relevent de M2.

## M0 — Stabilisation du socle

**Statut** : cloture le 2026-06-05 (voir `docs/m0-cloture.md`).

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

**Statut** : cloture le 2026-06-06 (voir `docs/m1-cloture.md` et la PR de cloture M1 #134). La dette residuelle acceptee a la cloture est basculee en M3.

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

**Statut** : cloture le 2026-06-06 (voir `docs/m2-bilan-final.md`).

**Priorite** : P1.

**Objectif** : industrialiser les ajouts documentaires une fois M0 et M1 stabilises.

**Acquis a respecter en M3** : le studio M2 est un outil de preparation, pas
d'integration automatique (« le studio prepare, l'humain valide »). Garde-fous
conserves : aucune creation automatique de sources, atomes, citations ou
relations ; aucune modification automatique de registres ; aucun GitHub
automatique (branche / PR / merge). Familles couvertes par les CLI : PERSON,
ORG, IMAGE, PLACE, SOURCE longue, plus batch et formulaire.

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

**Statut** : actif, lance le 2026-06-07.

**Priorite** : P1.

**Objectif n1 (decision utilisateur 2026-06-07)** : supprimer les deux depots
existants — `joy-division-ai-writing-studio` (public) et
`joy-division-studio-private` (prive) — au profit d'un **depot unique, nouveau,
prive, expose derriere Cloudflare Zero Trust**. Ce chantier impose une reprise
de l'architecture globale, confiee a l'assistant.

La fusion n'est plus interdite : elle est decidee. La bascule effective et la
suppression des depots existants restent toutefois conditionnees a une
architecture cible et a un plan de migration reversible valides par decision
humaine. M3 commence donc par la conception, pas par la bascule.

**Decisions d'architecture actees (2026-06-07)** :

- **Historique git** : le depot unique repart d'un commit initial propre. Les
  deux depots actuels sont archives en lecture seule comme reference historique
  (pas de fusion d'historiques git).
- **Rien ne reste public** : un seul depot prive, tout expose derriere
  Cloudflare Zero Trust. La frontiere actuelle entre depot public et depot prive
  disparait.
- **Organisation par fonction, pas par technologie** : la structure interne du
  hub suit cinq espaces fonctionnels (Collection, Usine, Le Fonds, Atelier,
  Vigie), et non un decoupage ex-public / ex-prive.
- **Perimetre : quatre depots absorbes** — `joy-division-ai-writing-studio`,
  `joy-division-studio-private`, `joy-division-releases` (registre des
  variantes, 14e registre) et `joy-division-collection` (Collection
  personnelle). `releases`, aujourd'hui public en CC BY-SA, bascule en prive
  comme le reste du hub.
- **Reagencement leger = mapping logique** : l'arborescence actuelle est
  conservee et les apps ne sont pas reecrites ; les cinq espaces sont une couche
  de lecture (README / manifest + navigation), pas un deplacement massif de
  dossiers. Aucune fonctionnalite perdue (14 registres, RAG, manuscript-studio,
  dashboard, collection).
- Le dossier d'architecture detaille est produit : `docs/m3-architecture-depot-unique.md`
  (arborescence cible, manifest des cinq espaces, import des quatre depots,
  bascule des fetchs distants en lecture locale, CI unifiee, exposition Zero
  Trust, plan de migration reversible). Il est en attente de validation humaine
  avant toute migration.

### Transposition des depots actuels (cadre)

Mapping indicatif des surfaces existantes vers les cinq espaces (deplacement
logique, contenus conserves) :

| Espace | Surfaces actuelles rattachees |
| --- | --- |
| La Collection | `joy-division-collection/` (possession, observations, wishlist) ; `joy-division-releases/` (registre des variantes). |
| L'Usine | `tools/` (atomisation, build, validation, canonisation) ; `apps/m2-formulaire/` ; `schemas/`. |
| Le Fonds | `sources/`, `registers/`, `exports/`, `rag/` ; les 11 apps registres ; `apps/rag-studio/`. |
| L'Atelier | `chapters/` (DM generes + matiere editoriale privee), `master_docs/`, `prompts/` ; `apps/manuscript-studio/`, `apps/master-docs/`, `apps/prompt-studio/`, `apps/local-songbook-editor/`. |
| La Vigie | `reports/`, `docs/` (roadmap, audits), `STATUS*.md` ; `apps/corpus-dashboard/` ; indicateurs M1. |

Points de reconciliation connus : `chapters/` (la matiere editoriale privee est
la source, le `document_maitre.md` public en est la sortie generee) ;
`generate_status.py` (conserver la variante du build canonique) ; dossiers
presents des deux cotes (`_meta/`, `docs/`, `prompts/`, `reports/`) reunis par
union. Modification technique principale : remplacer les fetchs GitHub distants
des apps privees par une lecture locale synchronisee.

### Modele d'organisation cible — hub fonctionnel

Le hub unifie est organise par fonction (cadre d'organisation, non fige comme
architecture technique definitive ; voir aussi
`docs/projet-etat-de-reference-2026-06.md`) :

| Espace | Fonction |
| --- | --- |
| La Collection | Conserver les objets possedes : preserver, documenter, valoriser (vinyles, CD, cassettes, bootlegs, livres, affiches, photos, objets, scans, provenance). |
| L'Usine | Transformer la matiere brute en donnees structurees : atomisation, enrichissement, integration de sources, registres, normalisation, validation. Elle fabrique le Corpus. |
| Le Fonds | Conserver, structurer et interroger le corpus : sources, atomes, registres, relations, chronologies, citations, exports, moteur RAG. On y cherche, on n'y redige pas. |
| L'Atelier | Produire le manuscrit : exports RAG, documents maitres, Forge, manuscrits, audits de chapitres, versions de travail. Seul espace de redaction. |
| La Vigie | Piloter la qualite et la strategie : roadmap, audits, controles, rapports, agregation, tableau de bord, indicateurs. Ce que M1 a commence a construire. |

Flux : Collection -> Usine -> Le Fonds -> Atelier -> Vigie.

Regles structurantes : Collection != Corpus (un objet peut exister dans la
Collection sans etre integre au Corpus) ; les IA (Claude, Codex, ChatGPT, futurs
agents) ne sont pas un espace mais des operateurs intervenant a chaque niveau.

**Objectif general** : autour de ce depot unique, etablir une architecture
cible, une chaine documentaire industrialisee, un deploiement Cloudflare Pages
et un acces Zero Trust.

Decision d'architecture : la cible retenue est un depot prive unique publie via Cloudflare Pages, protege par Cloudflare Zero Trust.

Le devenir de l'abonnement Pages Pro existant doit etre inventorie dans M3 afin d'eviter un cout orphelin ou une infrastructure residuelle inutile.

Cloudflare est decide. La fusion des repos est desormais decidee et constitue l'objectif n1 de M3 ; son calendrier de bascule reste subordonne a la validation de l'architecture cible et du plan de migration.

Decision d'architecture complementaire : le repo prive doit progressivement devenir autonome sur le plan documentaire. Les applications privees ne doivent plus dependre, au runtime, de fetchs GitHub distants vers le repo public pour afficher l'etat du corpus. La cible M3 est une consommation locale des exports, registres et documents maitres, appuyee sur une synchronisation maitrisee plutot que sur une lecture distante.

### Dette M1 residuelle basculee en M3

La dette acceptee a la cloture M1 (voir `docs/m1-cloture.md`) est reprise comme
chantiers M3, sans rouvrir le jalon M1 :

- tableau de bord qualite complet : blocs volumetrie, integrite et verification,
  genere par le build et jamais saisi manuellement ;
- audit Pennie Smith clos et documente ;
- indicateurs consolides publies : `0` lien inter-registres orphelin sur le
  perimetre publie, `0` identifiant canonique duplique, validation de schema a
  `100 %` ;
- reserves `DM -> registres` : 29 libelles divergents et 51 familles hors MVP
  (concepts, motifs, mythes, organisations, relations) ;
- regles de source, provenance et droits verifiees au-dela du perimetre DM,
  notamment qu'aucun champ `sources` ne contient un identifiant interne comme
  `IMAGE-*` a la place d'une source documentaire `Sxx`.

Ces chantiers doivent etre integres a l'architecture cible du depot unique, et
non recrees a l'identique sur l'ancienne separation public / prive.

Le chantier explicitement retenu est intitule : **M3.X — Industrialisation documentaire et autonomisation du studio prive**.

Ce chantier est place dans M3 avec un niveau de priorite equivalent au chantier Cloudflare Pages + Zero Trust, a la securisation des acces et a la consolidation applicative. Le constat qui le motive est structurel : les travaux recents sur S37, S95, le dashboard corpus prive et le miroir prive des documents maitres montrent que la production documentaire peut etre correcte alors que la visibilite, la tracabilite ou l'exposition applicative restent trop artisanales.

Le probleme M3 n'est donc plus seulement documentaire. Il concerne toute la chaine :

- entree des sources ;
- canonisation ;
- atomisation ;
- propagation ;
- exposition dans les interfaces ;
- dependances entre repo public et repo prive.

### M3.X — Industrialisation documentaire et autonomisation du studio prive

**Objectif general** : passer d'un ensemble de scripts et de conventions a une chaine documentaire industrialisee, observable et verifiable.

Principes a appliquer a partir de M3 :

- aucune source n'entre directement dans le systeme ;
- toute source passe par un sas normalise ;
- toute canonisation est outillee ;
- toute atomisation produit une preuve automatique de propagation ;
- toute interface privee lit des donnees locales maitrisees ;
- les dependances runtime au repo public sont progressivement supprimees.

Sous-chantiers prioritaires :

1. **Sas documentaire d'entree**

   Convention cible :

   ```text
   sources/_incoming/Sxx/
   source.pdf
   source.txt
   source_meta.yaml
   ```

   Objectif : supprimer les ambiguites sur les sources visibles par Codex, les assistants documentaires et les scripts de canonisation.

2. **Canonisation assistee**

   Outillage attendu :

   - creation du dossier source ;
   - creation de l'entree registre ;
   - creation des fichiers standards ;
   - generation du squelette documentaire.

   Objectif : reduire les taches repetitives et limiter les erreurs de nommage, de source_id, de dossier et de metadonnees.

3. **Industrialisation de l'atomisation**

   Workflow standard :

   ```text
   source
   -> canonisation
   -> atomes
   -> relations
   -> registres
   -> exports
   -> documents maitres
   -> interfaces
   ```

   Objectif : rendre la chaine unique, reproductible et comprehensible par revue humaine.

4. **Preuve automatique de propagation**

   Rapport systematique attendu :

   ```text
   Sxx_propagation_report.md
   ```

   Contenu minimal :

   - atomes crees ;
   - exports impactes ;
   - registres impactes ;
   - documents maitres impactes ;
   - interfaces impactees.

   Objectif : supprimer les verifications manuelles dispersees apres atomisation.

5. **Autonomisation du studio prive**

   Audit attendu :

   - dashboard corpus ;
   - documents maitres ;
   - registres ;
   - RAG ;
   - autres applications privees.

   Objectif : remplacer progressivement les fetchs GitHub distants vers le repo public par des donnees locales synchronisees, versionnees ou explicitement miroires.

6. **Preparation Cloudflare Zero Trust**

   L'autonomisation documentaire devient un prerequis du basculement final sous Zero Trust : la securisation, l'autonomie documentaire et l'architecture applicative doivent converger avant exposition protegee.

**Perimetre futur** :

- architecture cible ;
- strategie de migration ;
- industrialisation du cycle source -> interface ;
- sas documentaire d'entree ;
- canonisation assistee ;
- preuve automatique de propagation documentaire ;
- audit des dependances actuelles entre repo public et repo prive ;
- cartographie des applications privees consommant encore des ressources publiques ;
- suppression progressive des dependances runtime au repo public ;
- strategie de synchronisation locale des exports, registres et documents maitres ;
- lecture locale du dashboard corpus prive ;
- lecture locale ou miroir maitrise des documents maitres prives ;
- preservation des deux roadmaps ;
- integration studio, registres et collection ;
- absence de perte de donnees.

**Livrables futurs** :

- note d'architecture cible ;
- convention `sources/_incoming/Sxx/` avec `source.pdf`, `source.txt` et `source_meta.yaml` ;
- outillage de canonisation assistee ;
- squelette documentaire standard par source canonisee ;
- workflow source -> canonisation -> atomes -> relations -> registres -> exports -> documents maitres -> interfaces ;
- rapport automatique `Sxx_propagation_report.md` ;
- inventaire des repos et flux a rapprocher ;
- inventaire des fetchs, URLs distantes et ressources inter-repos encore utilisees par les applications privees ;
- matrice application privee -> ressource consommee -> strategie cible ;
- plan de migration reversible ;
- strategie de synchronisation locale reproductible ;
- refonte du dashboard corpus pour lecture locale ;
- validation fonctionnelle apres suppression des dependances runtime au repo public ;
- strategie de sauvegarde ;
- matrice des donnees a conserver.

**Criteres de sortie** :

- aucun repo n'est fusionne sans plan valide ;
- les roadmaps existantes sont conservees ;
- les donnees publiques et privees sont distinguees ;
- aucune source nouvelle n'entre dans le systeme sans sas documentaire normalise ;
- toute canonisation produit un dossier source, une entree registre et des fichiers standards coherents ;
- toute atomisation nouvelle produit une preuve de propagation vers exports, registres, documents maitres et interfaces concernees ;
- les applications privees critiques ne dependent plus de fetchs GitHub distants vers le repo public pour rendre l'etat courant du corpus ;
- les exports, registres et documents maitres necessaires aux interfaces privees sont disponibles localement ou synchronises par un mecanisme explicite ;
- le dashboard corpus prive affiche l'etat documentaire local synchronise, pas un etat distant implicite ;
- les documents maitres prives exposent la meme version documentaire que le corpus synchronise ;
- les risques de perte ou d'ecrasement sont documentes.

Ces criteres devront etre rendus mesurables au declenchement effectif du jalon.

**Liens avec la roadmap existante** :

- rattache les chantiers techniques d'infrastructure, de publication et de securisation ;
- rattache le chantier d'autonomisation documentaire du studio prive ;
- doit rester posterieur a M0 et M1.

**Risques** :

- fusion prematuree des repos ;
- perte de contexte entre corpus public, corpus prive et studios ;
- nouvelle source ajoutee hors sas, impossible a reproduire ou relire par Codex ;
- atomisation correcte mais propagation non prouvee jusqu'aux interfaces ;
- interfaces privees affichant un etat documentaire ancien a cause d'une lecture distante ou d'un miroir non synchronise ;
- confusion entre synchronisation maitrisee et dependance runtime implicite ;
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

### Seconde passe historiographique sur les sources fondatrices

Le corpus dispose deja d'un volume important d'atomes, de registres structurants, de documents maitres et d'une atomisation avancee des sources fondatrices. Une partie importante des sources majeures a deja ete atomisee, notamment Peter Hook, Bernard Sumner, Deborah Curtis, Mick Middles, Middles & Reade, Chris Ott, Johnson, West, Reynolds, Kevin Cummins et d'autres sources fondatrices.

Le probleme principal ne releve donc plus seulement de la collecte d'informations nouvelles. Il releve aussi de la capacite a extraire davantage de valeur intellectuelle du corpus existant.

Cette seconde passe ne constitue pas une reatomisation complete. Elle consiste a reexaminer les atomes deja produits afin d'identifier :

- les citations les plus fortes ;
- les formulations canoniques ;
- les scenes fondatrices ;
- les temoignages de premiere main ;
- les chaines argumentatives ;
- les motifs recurrents ;
- les elements a fort potentiel redactionnel.

Cette demarche vise a distinguer progressivement deux dimensions complementaires :

- l'importance documentaire ;
- le potentiel redactionnel.

Un atome ou une citation peut etre fortement important pour le corpus mais faiblement utile au manuscrit. A l'inverse, un element documentaire plus ponctuel peut posseder un potentiel redactionnel eleve parce qu'il cristallise une scene, une tension, une formule ou une articulation argumentative.

Cette distinction ne remet pas en cause les atomes existants. Elle ajoute une couche de lecture historiographique et editoriale, sans creer immediatement de nouveaux schemas ni de nouvelles obligations.

| Priorite | Sources |
| --- | --- |
| Tres elevee | Hook, Sumner, Deborah Curtis, Middles, Middles & Reade, Ott |
| Elevee | Johnson, West, Reynolds |
| Moyenne | Cummins, Hannett, Gretton, autres temoins directs |

Positionnement :

- ce chantier releve de M6 ;
- il ne releve pas de M1 ;
- il ne releve pas de M2 ;
- il ne constitue pas une nouvelle campagne d'atomisation ;
- il constitue une operation de valorisation historiographique du corpus existant.

Criteres de sortie proposes :

- identification des principales citations candidates pour le manuscrit ;
- identification des atomes a fort potentiel redactionnel ;
- cartographie des chaines argumentatives majeures ;
- reperage des scenes fondatrices mobilisables dans plusieurs chapitres ;
- enrichissement progressif des registres sans duplication documentaire.

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
