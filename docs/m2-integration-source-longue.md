# M2.3 - Integration documentaire d'une source longue

## 1. Objet de l'integration documentaire

L'integration documentaire est le flux M2 qui part d'une source importante et prepare son entree controlee dans le corpus.

Elle couvre :

- la qualification d'une source candidate ;
- la creation ou la mise a jour d'une source canonique dans `data/registre.json` ;
- la preparation d'un dossier source dans `sources/<source>/` ;
- la proposition d'atomes ;
- la proposition de citations, paraphrases et concepts ;
- la proposition de relations vers les registres existants ;
- la proposition d'enrichissements de registres ;
- la pre-validation, les controles et la preparation de PR.

Elle ne couvre pas :

- l'acceptation automatique d'une atomisation ;
- la validation historiographique d'une interpretation ;
- la creation silencieuse d'objets ;
- la fusion automatique de sources, personnes, lieux, organisations, concerts ou concepts ;
- l'ouverture d'un nouveau schema, registre, assistant, formulaire ou workflow ;
- la modification directe de `main`.

Difference avec M2.1 : M2.1 part d'un objet unique deja qualifie et documente. M2.3 part d'une source importante et prepare un ensemble de propositions documentaires. Une integration documentaire peut produire plusieurs ajouts unitaires candidats, mais chacun reste soumis aux contrats M2.1, M2.2 et M2.4 avant integration.

L'integration documentaire prepare une Pull Request relisible. Elle ne transforme pas la source en verite canonique par elle-meme.

## 2. Types de sources concernees

Les categories couvertes par M2.3 sont limitees aux types suivants.

| Type | Description | Attention principale |
| --- | --- | --- |
| livre | Ouvrage publie, monographie, recit, essai ou biographie. | Identifier edition, annee, pagination utile, statut de temoignage ou source secondaire. |
| article | Article universitaire, journalistique ou critique. | Identifier publication, volume, numero, date, pagination et version consultee. |
| interview | Entretien publie, retranscrit, audio, video ou archive. | Distinguer parole citee, montage editorial, date de l'entretien et date de publication. |
| fanzine | Publication amateure ou semi-professionnelle. | Documenter provenance, numero, date, statut fragile et limites de fiabilite. |
| archive | Document d'archive, fac-simile, dossier, photographie, piece administrative ou element conserve. | Distinguer cote, provenance, droits, consultation et interpretation. |
| memoire | Memoire universitaire ou travail de recherche non publie comme livre. | Identifier institution, niveau, encadrement si connu, statut academique et limites de diffusion. |
| these | These universitaire. | Identifier institution, discipline, date, version et statut de validation academique. |
| dossier documentaire | Ensemble constitue de documents heterogenes autour d'un sujet. | Ne pas confondre le dossier avec une source unique si les pieces doivent rester distinctes. |

Ces categories ne creent pas de nouveaux registres. Elles servent a qualifier le traitement documentaire et les reserves de revue.

## 3. Pipeline d'integration

```text
source candidate
  |
  v
qualification documentaire
  |
  v
source canonique
  |
  v
dossier source
  |
  v
proposition d'atomes
  |
  v
proposition de citations
  |
  v
proposition de relations
  |
  v
proposition d'enrichissements
  |
  v
pre-validation
  |
  v
controles
  |
  v
PR
  |
  v
validation humaine
```

| Etape | Role |
| --- | --- |
| source candidate | Recevoir une source potentielle et determiner si elle releve bien d'une integration documentaire. |
| qualification documentaire | Identifier type, auteur, titre, date, edition, statut, perimetre utile, provenance, droits et risques. |
| source canonique | Proposer une entree `Sxx` ou la mise a jour d'une entree existante dans `data/registre.json`. |
| dossier source | Preparer un espace de travail `sources/<source>/` qui conserve les notes, parties utiles, propositions et limites. |
| proposition d'atomes | Extraire des unites documentaires candidates sans les presenter comme integrees. |
| proposition de citations | Isoler citations exactes, paraphrases et concepts avec prudence sur les droits et la verification. |
| proposition de relations | Reperer les liens possibles vers personnes, lieux, organisations, chansons, concerts, concepts, motifs et mythes. |
| proposition d'enrichissements | Identifier les ajouts ou corrections de registres justifies par la source. |
| pre-validation | Appliquer les verifications M2.2 : identifiants, sources, schemas, relations, collisions, artefacts et reserves. |
| controles | Executer les validateurs existants, build, synchronisation et controles M1 pertinents selon les fichiers touches. |
| PR | Ouvrir une Pull Request conforme a M2.4, avec diff limite, resume, validations et reserves. |
| validation humaine | Relire, arbitrer, demander correction, accepter, differer ou refuser. |

Chaque etape doit pouvoir etre relue separement. Une source longue ne doit pas devenir une grosse PR opaque qui melange bibliographie, atomisation, relations, registres et corrections sans explication.

## 4. Creation de la source canonique

Question : quand une source merite-t-elle un identifiant `Sxx` ?

Une source merite un identifiant canonique lorsqu'elle remplit les conditions suivantes :

- elle est identifiable comme source documentaire autonome ;
- elle apporte une preuve, un contexte, un temoignage ou une interpretation mobilisable dans le corpus ;
- elle n'est pas deja presente dans `data/registre.json` sous le meme titre, auteur, edition, URL, publication ou identifiant proche ;
- elle peut etre rattachee a un usage documentaire explicite ;
- son statut et ses limites peuvent etre decrits sans masquer les incertitudes ;
- elle n'est pas seulement un document maitre, un export, une sortie RAG, une note interne ou une provenance technique.

Informations minimales a proposer dans `data/registre.json`, en respectant les champs observes dans le depot :

- `id` ;
- `source_label` ;
- `auteur` ;
- `titre` ;
- `annee` ;
- `reference_complete` ;
- `nature` ;
- `statut` ;
- `fiabilite` ;
- `usage` ;
- `chapitres` ;
- `source_origin` ;
- `arbitrage`.

Champs complementaires observes et utiles selon les cas :

- `dossier_source` ;
- `fichier_source` ;
- `source_url` ;
- `source_drive` ;
- `publication` ;
- `volume_numero` ;
- `pagination` ;
- `version` ;
- `section_utile` ;
- `pages_utiles` ;
- `chapitres_secondaires` ;
- `niveau_preuve` ;
- `prudence`.

Cas de refus :

- la source existe deja dans `data/registre.json` ;
- la source candidate est seulement une URL non qualifiee ;
- la source candidate est un document maitre ou un artefact genere ;
- les metadonnees minimales ne permettent pas d'identifier la source ;
- les droits ou la provenance sont inconnus et indispensables au traitement demande ;
- le candidat est en realite un objet unitaire relevant de M2.1 ;
- le candidat est un dossier composite dont les pieces doivent etre separees avant canonisation.

Lien avec `data/registre.json` :

- `data/registre.json` est la source de verite canonique pour les identifiants `Sxx` ;
- `registers/references/` et `sources/<source>/` ne remplacent pas cette source de verite ;
- une proposition utilisant un `Sxx` inconnu est bloquante ;
- une source canonique creee ou modifiee doit rester relisible dans le diff de PR.

## 5. Dossier source

Le dossier source prend la forme :

```text
sources/<source>/
```

Role :

- regrouper les fichiers de travail d'une source longue ;
- conserver les parties utiles et notes de lecture ;
- rendre visibles les propositions d'atomes, citations, relations et mises a jour de registres ;
- documenter les limites, prudences et arbitrages ;
- faciliter la revue humaine avant integration.

Contenu observe ou attendu selon les cas :

- `source.md` pour la fiche de travail principale ;
- `source_part_*.md` pour les parties utiles ;
- `atoms_*.md`, `atomes_*.md` ou `atoms_dm_*.md` pour des atomes proposes ;
- `citations_exactes.md` ou fichier equivalent pour les citations proposees ;
- `relations_*.md` ou `relations_stabilisees.md` pour les relations candidates ;
- `registre_patch_*.json` pour des enrichissements proposes de registre ;
- `registers_update_*.md`, `registres_specialises_*.md` ou `registres_structurants_*.md` pour des propositions documentaires ciblees ;
- `README.md` lorsque le dossier a besoin d'une note de structure.

Limites :

- le dossier source n'est pas automatiquement canonique ;
- un fichier dans `sources/<source>/` ne suffit pas a creer un `Sxx` ;
- un `registre_patch_*.json` n'est pas une modification acceptee tant qu'il n'est pas integre, valide et relu ;
- les propositions d'atomes ou relations restent candidates tant qu'elles ne sont pas integrees dans les fichiers cibles ;
- le dossier source ne prouve pas les droits de reproduction ;
- le dossier source ne doit pas contenir de correction silencieuse de registres.

Dossier source != source canonique.

La source canonique est l'entree `Sxx` de `data/registre.json`. Le dossier source est l'espace de travail documentaire qui accompagne cette source.

## 6. Proposition d'atomes

Une integration documentaire peut proposer des atomes issus de la source longue.

Ce qui peut etre propose :

- unites documentaires courtes et relisibles ;
- rattachement a une source `Sxx` connue ;
- indication de partie, page, chapitre ou passage lorsque disponible ;
- distinction entre fait, citation, paraphrase, interpretation et hypothese ;
- statut de verification ;
- liens candidats vers chapitres, themes ou documents maitres ;
- limites de lecture et reserves.

Ce qui ne doit pas etre impose :

- acceptation automatique de l'atomisation ;
- transformation d'une interpretation en fait canonique ;
- creation d'atomes sans source canonique ;
- numerotation en collision avec des atomes existants ;
- modification des documents maitres pour faire accepter les atomes ;
- suppression d'atomes existants sans audit.

Difference entre proposition et integration effective :

- une proposition d'atome est une lecture candidate ;
- une integration effective suppose un fichier cible, des identifiants coherents, des controles applicables et une revue humaine ;
- les controles M1 ne valident les documents maitres que lorsqu'ils sont affectes ; ils ne remplacent pas la validation de fond des atomes proposes.

## 7. Proposition de citations

Une source longue peut contenir des citations exactes, des paraphrases et des concepts.

Citations :

- doivent etre rattachees a la source canonique ;
- doivent indiquer page, passage, locuteur, auteur ou contexte lorsque disponible ;
- doivent rester limitees au besoin documentaire ;
- doivent respecter les contraintes de droits et de citation ;
- doivent distinguer texte exact, traduction, coupe et commentaire editorial.

Paraphrases :

- doivent etre identifiees comme reformulation ;
- ne doivent pas etre presentees comme verbatim ;
- doivent conserver le sens attribuable a la source ;
- doivent signaler les incertitudes ou interpretations.

Concepts :

- peuvent etre proposes lorsque la source introduit une notion utile au corpus ;
- ne doivent pas devenir des faits ;
- doivent etre relies a leur contexte d'apparition ;
- doivent rester distinguables des motifs, mythes et interpretations du projet.

Exigences de verification :

- verifier l'exactitude du passage et sa localisation ;
- verifier le statut de traduction ou d'edition ;
- verifier que les droits ou limites de reproduction sont compatibles avec l'usage propose ;
- exposer les doutes plutot que les corriger silencieusement ;
- refuser une citation si son origine, son locuteur ou son statut exact ne peuvent pas etre etablis.

## 8. Proposition de relations

Une integration documentaire peut proposer des relations vers les familles existantes.

Familles concernees :

- personnes ;
- lieux ;
- organisations ;
- chansons ;
- concerts ;
- concepts ;
- motifs ;
- mythes.

Pour chaque relation proposee, la PR doit indiquer :

- la source `Sxx` qui la justifie ;
- l'objet cible pressenti ;
- le passage ou contexte utile ;
- la force de la relation si elle est incertaine ;
- le statut : relation nouvelle, relation confirmee, relation a arbitrer ou relation refusee.

Regles :

- verifier que l'objet cible existe lorsque la relation pointe vers un identifiant canonique ;
- ne pas creer automatiquement l'objet cible pour faire passer la relation ;
- ne pas fusionner deux objets pour simplifier une relation ;
- ne pas imposer une relation causale forte a partir d'une mention faible ;
- ne pas confondre co-occurrence, influence, citation, attribution et preuve.

Relation proposee != relation validee.

Une relation proposee devient valide seulement apres integration explicite dans les fichiers cibles, controle applicable et validation humaine.

## 9. Enrichissements de registres

Une source longue peut justifier des enrichissements de registres.

Enrichissements justifies :

- ajout d'un objet unitaire lorsque la source fournit une preuve suffisante ;
- correction d'un champ errone ou incomplet ;
- ajout d'une source `Sxx` a un objet deja existant ;
- ajout d'un alias, `same_as`, note de prudence ou usage documente ;
- ajout d'une relation lorsque le modele la supporte ;
- proposition de patch de registre visible et relisible.

Enrichissements a refuser :

- ajout d'un objet sans source canonique ;
- creation d'un doublon alors qu'un objet proche existe deja ;
- modification d'un registre pour faire correspondre une interpretation non arbitree ;
- correction massive sans audit ;
- suppression d'un objet ou d'une relation sans justification documentee ;
- ajout d'un champ absent du modele reel pour satisfaire un cas ponctuel.

Comment eviter les doublons :

- rechercher identifiants, libelles, alias, `same_as`, dates, lieux, publications et sources proches ;
- comparer la source candidate avec `data/registre.json` avant de proposer un nouveau `Sxx` ;
- comparer les objets candidats avec les registres et exports disponibles ;
- classer les collisions probables comme reserve ou bloquant selon le contrat M2.2 ;
- preferer une mise a jour explicite d'objet existant a une creation concurrente.

## 10. Pre-validation specifique

Une integration de source longue doit appliquer les verifications M2.2 et ajouter les points specifiques suivants.

| Verification | Regle attendue |
| --- | --- |
| source deja presente | Rechercher l'auteur, le titre, l'edition, l'URL, la publication et les identifiants proches dans `data/registre.json`. |
| source proche | Signaler les sources dont le titre, l'auteur, le sujet ou la publication peuvent creer une collision documentaire. |
| doublon | Refuser la creation d'un nouveau `Sxx` si l'entree canonique existe deja, sauf mise a jour documentee de l'entree existante. |
| source partielle | Documenter la section, les pages, l'extrait ou le dossier effectivement traite ; ne pas laisser croire que toute la source est integree. |
| edition differente | Distinguer edition, version, traduction, reedition, preprint, submitted version, scan et transcription. |
| traduction | Distinguer source originale, traduction publiee, traduction de travail et reformulation ; ne pas citer une traduction comme original. |
| droits | Identifier les limites de citation, reproduction, scan, image ou transcription avant proposition. |
| granularite | Decouper une source longue en PR ou parties si l'ensemble devient trop large pour une revue fiable. |
| relations massives | Refuser les relations imposees en bloc ; demander une qualification et une justification par relation ou groupe homogene. |
| registres touches | Identifier les registres concernes et appliquer les validateurs existants selon le perimetre reel. |

Classification :

- source canonique inconnue ou dupliquee : bloquant ;
- edition differente non documentee : reserve forte ou bloquant selon l'effet ;
- source partielle correctement signalee : information ou reserve ;
- droits non etablis pour une citation exacte longue : bloquant ;
- relation incertaine mais visible : reserve ;
- creation silencieuse d'objet : bloquant.

## 11. Resultat attendu

Un futur assistant d'integration doit produire au minimum :

- une source canonique proposee ou une mise a jour d'une source existante ;
- un dossier source `sources/<source>/` lorsque le traitement exige un espace de travail ;
- des atomes proposes ;
- des citations proposees ;
- des relations proposees ;
- des enrichissements proposes ;
- un resume documentaire ;
- la liste des fichiers modifies ;
- les validations executees ;
- les reserves et arbitrages humains restants ;
- une Pull Request conforme a M2.4.

La PR doit permettre a un humain de repondre rapidement :

- quelle source est integree ?
- existe-t-elle deja dans `data/registre.json` ?
- quel perimetre de la source est traite ?
- quelles propositions sont seulement candidates ?
- quels registres sont touches ?
- quels controles ont ete executes ?
- quelles reserves restent a arbitrer ?

## 12. Cas explicitement interdits

Sont interdits dans le cadre M2.3 :

- atomisation automatique acceptee comme verite ;
- creation automatique de citations ;
- relations imposees ;
- fusion automatique ;
- creation silencieuse d'objets ;
- modification directe de `main` ;
- creation d'un `Sxx` sans verification des doublons ;
- utilisation de `sources/<source>/` comme source de verite a la place de `data/registre.json` ;
- modification de schema pour accepter une source particuliere ;
- modification des controles M1 ;
- contournement de la revue Codex ou de la validation humaine ;
- suppression automatique de donnees existantes.

## 13. Risques

### Risques documentaires

- confondre source canonique, dossier source, fichier source, URL, provenance technique et droits ;
- creer une source dupliquee sous un nouvel identifiant `Sxx` ;
- laisser croire qu'une source partielle a ete integree en entier ;
- melanger notes de travail, citations exactes et paraphrases ;
- produire une PR trop large pour etre relue correctement.

### Risques historiographiques

- transformer un temoignage en fait etabli ;
- survaloriser une source unique ;
- imposer une relation causale a partir d'une proximite narrative ;
- effacer les contradictions entre sources ;
- convertir une interpretation utile en entree canonique sans arbitrage.

### Risques juridiques

- reproduire trop largement un texte protege ;
- citer une traduction ou transcription sans statut clair ;
- utiliser une image, un scan ou une archive sans droits etablis ;
- confondre acces technique au fichier et autorisation d'usage ;
- publier une citation dont l'origine ou l'auteur n'est pas verifie.

### Risques de gouvernance

- contourner M2.1 en creant massivement des objets unitaires ;
- contourner M2.2 en ouvrant une PR avec des bloquants connus ;
- contourner M2.4 en ouvrant une PR sans resume, validations ou reserves ;
- modifier `data/registre.json` sans rendre la decision canonique visible ;
- traiter les remarques de revue comme facultatives ;
- transformer M2.3 en automatisation avant stabilisation du contrat.

## 14. Decision proposee

La version minimale du contrat d'integration documentaire M2.3 est definie comme un flux source longue -> source canonique -> dossier source -> propositions documentaires -> pre-validation -> controles -> PR -> validation humaine.

Une integration documentaire acceptable part d'une source candidate qualifiee, verifie son existence ou son absence dans `data/registre.json`, propose une source canonique si necessaire, prepare un dossier source relisible, distingue atomes proposes, citations proposees, relations proposees et enrichissements proposes, puis ouvre une PR conforme aux contrats M2.2 et M2.4.

Cette version minimale est suffisante avant toute automatisation si elle respecte les limites suivantes :

- aucun script ;
- aucun assistant ;
- aucun formulaire ;
- aucun workflow ;
- aucune modification des schemas ;
- aucune modification des controles M1 ;
- aucune atomisation acceptee automatiquement ;
- aucune relation imposee ;
- aucune fusion automatique ;
- aucune creation silencieuse d'objet ;
- validation humaine obligatoire.

Le contrat M2.3 etablit que l'integration documentaire prepare une decision. Elle ne remplace ni la revue Codex, ni les controles existants, ni l'arbitrage humain.
