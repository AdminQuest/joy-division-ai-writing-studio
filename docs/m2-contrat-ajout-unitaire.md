# M2.1 - Contrat d'ajout unitaire

## 1. Objet du contrat

Un ajout unitaire est l'ajout cible d'un seul objet documentaire dans le corpus : une personne, un lieu, une organisation, une image, un concert, une occurrence discographique ou une citation.

Le contrat couvre :

- la qualification du type d'objet ;
- l'identifiant attendu ;
- les champs minimaux observes dans le depot ;
- les fichiers potentiellement touches ;
- les validations minimales a obtenir avant une Pull Request ;
- les cas ou l'ajout doit etre refuse.

Le contrat ne couvre pas :

- l'integration d'une nouvelle source longue ;
- l'atomisation d'un livre, article, entretien, fanzine ou archive ;
- la creation massive d'objets a partir d'une source ;
- la resolution historiographique d'un conflit ;
- la conception d'une interface, d'un formulaire ou d'un script.

Difference avec M2.3 : M2.1 part d'un objet unique deja qualifie et documente. M2.3 part d'une source documentaire importante et prepare un dossier source, des atomes, des citations, des relations et plusieurs enrichissements possibles. M2.1 est donc un contrat d'ajout ponctuel ; M2.3 est un contrat d'integration documentaire.

Ce document definit une reference pour les futurs assistants d'ajout, pre-validateurs, formulaires ou outils d'automatisation. Il ne cree aucun outil et ne modifie aucun registre.

## 2. Principes generaux

Principes obligatoires :

- aucun ajout direct sur `main` ;
- aucun merge automatique ;
- validation humaine obligatoire ;
- source documentaire avant enrichissement ;
- controles avant PR.

Un assistant d'ajout peut preparer une proposition. Il ne valide pas seul une verite documentaire.

La source documentaire doit etre distinguee :

- d'une URL de consultation ;
- d'une provenance technique ;
- d'un identifiant interne comme `IMAGE-*`, `PERSON-*`, `ORG-*` ou `JD-SONG-*` ;
- d'une sortie generee par le depot.

Lorsque le depot possede un schema ou un validateur pour le type concerne, l'ajout doit rester compatible avec ce contrat existant. Lorsque le type n'a pas encore de registre canonique autonome, l'ajout unitaire doit rester limite au support reel du depot et ne doit pas inventer un nouveau modele.

## 3. Types d'objets couverts

### PERSON

#### Finalite

Une entree `PERSON-` represente une identite canonique de personne : membre, entourage, industrie musicale, critique ou journaliste, auteur secondaire, influence ou theoricien mobilise.

#### Identifiant

Format attendu : `PERSON-<slug>`.

Exemples observes :

- `PERSON-ian-curtis`
- `PERSON-kevin-cummins`
- `PERSON-pennie-smith`

Le slug est semantique, en minuscules, avec segments separes par des tirets.

#### Champs obligatoires

Le schema `schemas/person_canonical.schema.json` rend obligatoires :

- `id`
- `type_unite`
- `name`
- `categorie`
- `role`
- `sources`
- `same_as`
- `alt_names`
- `categorie_a_arbitrer`
- `a_arbitrer`

Valeur attendue pour `type_unite` : `person`.

`categorie` doit appartenir au vocabulaire existant :

- `membre`
- `entourage`
- `industrie`
- `critique_journaliste`
- `auteur_secondaire`
- `influence`
- `theoricien_mobilise`

#### Champs facultatifs

Champs facultatifs observes :

- `note`
- `origine`

`origine` est limitee par le schema a `auteur_source` lorsqu'elle est utilisee.

#### Source documentaire

Obligatoire.

Le champ `sources` doit contenir au moins une source documentaire. Dans le cas normal, il s'agit d'identifiants `Sxx` presents dans `data/registre.json`. Un identifiant interne `PERSON-*`, `IMAGE-*` ou `ORG-*` ne peut pas tenir lieu de source documentaire.

#### Relations minimales

Relations existantes dans le modele :

- `same_as` peut rattacher des identifiants provisoires `PERS-*` a un `PERSON-` canonique ;
- une image peut pointer vers une personne via `photographer` ou `subjects` ;
- une citation peut designer un auteur, un locuteur ou un rapporteur sous forme textuelle ou, lorsque la couche d'attribution le permet, via les relations d'attribution.

Pour un ajout `PERSON`, le rattachement `same_as` doit rester coherent avec la couche provisoire existante lorsqu'elle existe. Un `PERSON-` ne doit pas pointer en `same_as` vers un autre `PERSON-`.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant `PERSON-` existe deja ;
- le nom correspond manifestement a une personne existante ou a un alias connu ;
- la source documentaire est absente ;
- la categorie n'appartient pas au vocabulaire du schema ;
- `same_as` pointe vers un `PERS-*` inexistant ou deja rattache autrement ;
- l'ajout risque de fusionner deux personnes distinctes ;
- l'ajout contourne la generation du registre canonique declaree dans `registers/people/00_canonical_people.md`.

### PLACE

#### Finalite

Une entree `PLACE-` represente un lieu documentaire : ville, quartier, habitat, studio, salle, commerce, lieu d'education, lieu de sante, site industriel, infrastructure, lieu de pouvoir ou lieu de memoire.

#### Identifiant

Format attendu : `PLACE-<SLUG>`.

Exemples observes :

- `PLACE-HULME`
- `PLACE-TJ-DAVIDSONS`
- `PLACE-BOWDON-VALE-YOUTH-CLUB`

Le slug est en majuscules, avec segments separes par des tirets.

#### Champs obligatoires

Le schema `schemas/places.schema.yaml` rend obligatoires :

- `id`
- `label`
- `type`

Si `type_unite` est present, il doit valoir `place`.

`type` doit appartenir au vocabulaire existant :

- `ville`
- `quartier`
- `habitat`
- `studio`
- `salle`
- `commerce`
- `education`
- `sante`
- `industrie`
- `science`
- `infrastructure`
- `pouvoir`
- `lieu_memoire`

#### Champs facultatifs

Champs facultatifs observes :

- `type_detail`
- `sources`
- `source_id`
- `source_label`
- `usage`
- `prudence`
- `chapitres`
- `atoms`
- `song_ids`
- `lat`
- `lng`
- `geo_precision`
- `geo_source`
- `source_url`
- `note_geo`
- `same_as`
- `reference_croisee`

Les champs `usage_s02`, `usage_s05`, `usage_s06`, `usage_s10` et `usage_s20` existent en transition, mais ne doivent pas devenir le modele cible d'un nouvel ajout.

#### Source documentaire

Obligatoire pour un nouveau lieu documentaire accepte par M2.1, meme si le schema technique ne rend pas `sources` obligatoire.

Une coordonnee geographique, un `source_url` de geolocalisation ou un QID d'autorite ne remplace pas une source documentaire du corpus. Ces elements peuvent completer l'ajout ; ils ne suffisent pas a l'etablir.

#### Relations minimales

Relations existantes dans le modele :

- `same_as` peut pointer d'un enregistrement legacy vers le `PLACE-` canonique ;
- `song_ids` peut relier un lieu a des chansons `JD-SONG-*` ;
- une image peut pointer vers un lieu via `place` ;
- un concert porte un lieu textuel, une ville et un pays ; le lien strict `CONCERT -> PLACE` n'est pas encore un champ obligatoire du schema concert.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant `PLACE-` existe deja ;
- `id` utilise `PLACES-*`, qui designe un en-tete de document et non un lieu ;
- le lieu est deja present sous un libelle, alias ou `same_as` equivalent ;
- aucune source documentaire ne justifie le lieu ;
- la categorie `type` sort du vocabulaire ;
- les coordonnees sont non verifiees ou incoherentes ;
- l'ajout cree une fusion de lieux distincts.

### ORG

#### Finalite

Une entree `ORG-` represente une organisation canonique : groupe, label, institution, organisation-lieu, equipe technique, media ou autre organisation liee au corpus.

#### Identifiant

Format attendu : `ORG-NNNN`.

Exemples observes :

- `ORG-0001`
- `ORG-0002`
- `ORG-0005`

Le numero est zero-padde sur quatre chiffres.

#### Champs obligatoires

Le schema `schemas/organization_canonical.schema.json` rend obligatoires :

- `org_id`
- `canonical_name`
- `aliases`
- `category`
- `country`
- `status`
- `same_as`
- `joy_division_relation`
- `sources`
- `identity_frozen`
- `drift_sentinel`
- `gate`
- `last_verified`

`category` doit appartenir au vocabulaire existant :

- `group`
- `label`
- `institution`
- `venue_org`
- `crew`
- `media`
- `other`

`status` doit appartenir au vocabulaire existant :

- `active`
- `dissolved`
- `dormant`
- `unknown`

`gate` doit valoir `public` ou `private`.

#### Champs facultatifs

Champs facultatifs observes :

- `subcategory`
- `city`
- `active_from`
- `active_until`
- `provenance`

Le champ `same_as` peut contenir des identifiants externes `wikidata`, `discogs` et `musicbrainz`, avec valeur `null` lorsque l'identifiant n'est pas documente.

#### Source documentaire

Obligatoire.

Le champ `sources` doit contenir au moins une source documentaire du corpus. Dans le cas normal, ces identifiants doivent exister dans `data/registre.json`.

#### Relations minimales

Relations existantes dans le modele :

- `joy_division_relation` decrit la relation documentee avec Joy Division ;
- `same_as` porte les identifiants externes verifies ;
- `provenance.from_pers` peut documenter une origine issue d'un `PERS-*` ;
- `provenance.from_attribution` peut signaler une origine issue de l'attribution de citations.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant `ORG-` existe deja ;
- le nom canonique ou un alias collisionne avec une organisation existante ;
- la source documentaire est absente ;
- `country` n'est pas un code ISO alpha-2 ;
- `joy_division_relation.type` est vide ;
- `identity_frozen` n'est pas `true` apres validation humaine ;
- l'organisation est en realite une personne, un lieu ou un concept.

### IMAGE

#### Finalite

Une entree `IMAGE-` represente soit une seance photographique, soit un cliche individuel. Le modele distingue deux niveaux :

- `IMAGE-S-NNNN` pour une session ;
- `IMAGE-I-NNNN` pour une image individuelle.

#### Identifiant

Formats attendus :

- `IMAGE-S-NNNN`
- `IMAGE-I-NNNN`

Exemples observes :

- `IMAGE-S-0001`
- `IMAGE-S-0007`
- `IMAGE-I-0001`

#### Champs obligatoires

Le schema `schemas/image_canonical.schema.json` rend obligatoires :

- `image_id`
- `level`
- `canonical_name`
- `photographer`
- `date`
- `date_precision`
- `subjects`
- `sources`
- `same_as`
- `identity_frozen`
- `drift_sentinel`
- `gate`
- `last_verified`

Si `level` vaut `image`, le champ `session_ref` est obligatoire et doit pointer vers une session `IMAGE-S-NNNN`.

Valeurs existantes pour `level` :

- `session`
- `image`

Valeurs existantes pour `date_precision` :

- `day`
- `month`
- `year`
- `approximate`

#### Champs facultatifs

Champs facultatifs observes :

- `session_ref`
- `place`
- `event_ref`
- `context`
- `output_count`
- `usage`
- `iconic`
- `notes`

Valeurs existantes pour `context` :

- `promo`
- `live`
- `portrait`
- `artwork`
- `rehearsal`
- `other`

#### Source documentaire

Obligatoire.

Le champ `sources` doit documenter l'existence, l'attribution ou l'usage de la session ou du cliche. Une URL publique peut etre presente lorsqu'elle est la seule trace disponible, mais elle doit etre signalee comme telle et ne doit pas etre confondue avec un identifiant canonique `Sxx`.

Pour les images, les droits et la provenance sont critiques. Un ajout peut etre documentaire sans stocker ni republier le fichier image.

#### Relations minimales

Relations existantes dans le modele :

- `photographer` doit pointer vers un `PERSON-` ;
- `subjects` peut contenir des `PERSON-` ou des descriptions libres ;
- `place` peut pointer vers un `PLACE-`, contenir une description libre si aucun `PLACE-` n'existe, ou rester `null` ;
- `event_ref` peut pointer vers un evenement `EVENT-` ;
- une image individuelle doit pointer vers sa session par `session_ref`.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant `IMAGE-` existe deja ;
- `level=image` sans `session_ref` valide ;
- `photographer` pointe vers une personne absente ;
- la source documentaire est absente ;
- les droits, la provenance ou l'attribution sont inconnus au point de rendre l'entree trompeuse ;
- l'ajout implique de republier un fichier image sans droit clair ;
- une image individuelle est creee alors que seule une session vague est documentee.

### CONCERT

#### Finalite

Le depot distingue deux strates pour les concerts :

- l'identite canonique `CONCERT-<SLUG>` dans `registers/concerts/concert_canonical_units.md` ;
- la couche legacy `JD-CONCERT-*` dans `registers/concerts/00_canonical_concerts.md`.

Un ajout unitaire `CONCERT` acceptable doit respecter la couche canonique lorsque le concert entre dans son perimetre. La couche legacy reste la source joydiv.org reconciliee par `same_as`.

#### Identifiant

Format canonique attendu : `CONCERT-YYYYMMDD-LIEU`.

Exemples observes :

- `CONCERT-19770529-ELECTRIC-CIRCUS`
- `CONCERT-19771200-RAFTERS-MANCHESTER`
- `CONCERT-19780125-PIPS`

Format legacy observe : `JD-CONCERT-YYYYMMDD-NNN`.

Exemples observes :

- `JD-CONCERT-19770529-001`
- `JD-CONCERT-19770827-002`
- `JD-CONCERT-19771200-001`

Le suffixe `NNN` distingue plusieurs evenements le meme jour. Si le jour est inconnu, le schema documentaire autorise `00`.

#### Champs obligatoires

Pour la couche canonique `CONCERT-`, le validateur `tools/validate_concerts.py` et `tools/schema_validation.py` attendent :

- `id`
- `type_unite`
- `label`
- `date_precision`
- `lieu`
- `membres_reconcilies`

Valeur attendue pour `type_unite` : `concert`.

L'entree canonique doit aussi porter exactement l'une des deux formes temporelles :

- `date`
- ou `date_debut` et `date_fin`

Valeurs controlees pour `date_precision` :

- `jour`
- `mois`
- `saison`
- `annee`
- `circa`
- `intervalle`

Valeurs controlees pour `statut` lorsqu'il est present :

- `confirmé`
- `annulé`
- `douteux`

Pour la couche legacy `JD-CONCERT-*`, `schemas/concert_v1.yaml` rend obligatoires :

- `id`
- `date`
- `statut`
- `lieu`
- `ville`
- `pays`
- `ere`
- `source`

Valeurs legacy existantes pour `statut` :

- `confirme`
- `annule`
- `reporte`
- `douteux`
- `tv`

Valeurs legacy existantes pour `ere` :

- `Warsaw`
- `Stiff Kittens`
- `Joy Division`

#### Champs facultatifs

Champs recommandes ou facultatifs observes :

- `url_detail`
- `atomes_lies`
- `notes`
- `chronologie_id`
- `nom_tournee`
- `setlist`
- `same_as`

#### Source documentaire

Obligatoire.

Le schema legacy documente `joydiv.org` comme source canonique primaire du registre concerts. Une autre source peut appuyer une correction ou une contradiction, mais elle doit etre nommee explicitement. Une setlist ne doit jamais etre inventee.

#### Relations minimales

Relations existantes dans le modele :

- une entree canonique `CONCERT-` doit lister au moins un membre dans `membres_reconcilies` ;
- une entree legacy `JD-CONCERT-*` reconciliee doit pointer vers le `CONCERT-` canonique par `same_as` ;
- `lieu` d'un `CONCERT-` doit resoudre vers un `PLACE-` existant ;
- `atomes_lies` peut pointer vers des atomes documentaires ;
- `chronologie_id` peut pointer vers une entree de chronologie ;
- les passages TV restent hors du perimetre canonique indique par `registers/concerts/concert_canonical_units.md`.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant `CONCERT-` ou `JD-CONCERT-*` existe deja ;
- un concert relevant du perimetre canonique est ajoute seulement comme legacy `JD-CONCERT-*` ;
- la date, le lieu ou l'existence du concert ne sont pas documentes ;
- le `lieu` canonique ne resout vers aucun `PLACE-` ;
- `membres_reconcilies` est absent ou vide ;
- `statut`, `date_precision` ou `ere` sort du vocabulaire applicable ;
- deux concerts distincts sont fusionnes ;
- une setlist est ajoutee sans source ;
- une contradiction de date est masquee au lieu d'etre documentee dans `notes`.

### RELEASE

#### Finalite

Dans l'etat reel du depot, `RELEASE` n'est pas un registre canonique autonome comparable a `PERSON-`, `ORG-` ou `IMAGE-`.

Le type couvert par M2.1 est donc limite a une occurrence discographique rattachee au Songbook : sortie officielle, compilation, single, album, bootleg, diffusion radio, archive ou collection personnelle, selon `schemas/song_occurrence.schema.yaml` et les fichiers references par `data/song_dossiers_index.json`.

Un ajout unitaire `RELEASE` ne doit pas creer un nouveau registre global des releases.

#### Identifiant

Format attendu pour une occurrence : selon `schemas/song_occurrence.schema.yaml`.

Exemples de formats documentes :

- `JD-SONG-XXX-REL-001`
- `JD-SONG-XXX-LIVE-OCC-YYYYMMDD-001`
- `JD-SONG-XXX-BOOT-001`

Le `song_id` rattache doit pointer vers une chanson canonique `JD-SONG-NNN`.

#### Champs obligatoires

Le schema `schemas/song_occurrence.schema.yaml` rend obligatoires :

- `occurrence_id`
- `song_id`
- `canonical_song`
- `occurrence_type`

Valeurs existantes pour `occurrence_type` :

- `official_release`
- `compilation`
- `single`
- `album`
- `live_event`
- `bootleg`
- `radio_broadcast`
- `archive`
- `personal_collection`

#### Champs facultatifs

Champs observes dans le schema :

- `version_id`
- `title`
- `date`
- `place`
- `catalogue`
- `track_position`
- `source_ids`
- `verification_status`
- `notes`

Valeurs existantes pour `verification_status` :

- `verifie`
- `a_verifier`
- `conflit`
- `hypothese`

Les fichiers de releases du Songbook sont references dans `data/song_dossiers_index.json`, mais les dossiers `songs/<slug>/` ne sont pas presents comme arborescence versionnee dans l'etat observe du depot. Toute automatisation future doit donc verifier le support reel avant de proposer un diff.

#### Source documentaire

Obligatoire.

Une occurrence discographique doit etre justifiee par une source discographique ou documentaire : livret officiel, Discogs, site officiel, source canonique `Sxx`, source web repertoriee ou autre preuve explicite. Le numero de catalogue seul ne suffit pas si la sortie n'est pas autrement documentee.

#### Relations minimales

Relations existantes dans le modele :

- `song_id` doit pointer vers un `JD-SONG-NNN` canonique ;
- `version_id`, s'il est renseigne, doit correspondre a une version connue ;
- `place`, lorsqu'il decrit un concert ou une session, doit rester coherent avec les lieux existants ou etre signale comme description non canonicalisee ;
- les doublons entre release officielle et bootleg doivent etre signales.

#### Cas de refus

Refuser l'ajout si :

- l'objet propose suppose un registre `RELEASE-*` autonome inexistant ;
- le `song_id` est absent ou inconnu ;
- la source documentaire est absente ;
- l'occurrence cree une chanson nouvelle alors qu'elle doit rattacher une chanson existante ;
- le type d'occurrence sort du vocabulaire ;
- le meme objet discographique est deja present ou reference ;
- la difference entre release officielle, compilation, bootleg et archive est non tranchee.

### CITATION

#### Finalite

Une entree de citation represente une citation, une paraphrase ou un concept extrait ou derive d'une source. Son identite est construite a partir de la source et d'un ordinal conserve.

#### Identifiant

Conventions reconnues par `schemas/quote.schema.yaml` :

- `Sxx-Qn`
- `Sxx-CIT-n`
- `CIT-Sxx-n`

Exemples de formes attendues :

- `S41-Q1`
- `S76-CIT-12`
- `CIT-S45-3`

#### Champs obligatoires

Le schema `schemas/quote.schema.yaml` rend obligatoires :

- `id`
- `kind`
- `source_id`
- `texte`
- `type`

Le validateur gateable `tools/validate_quotes.py` exige aussi pour un ajout acceptable :

- `page` ou un localisateur equivalent, avec `inconnue` comme sentinelle explicite si aucun localisateur reel n'est disponible ;
- `locuteur`, sous forme de nom ou `anonyme`.

Valeurs controlees pour `type` :

- `verbatim`
- `paraphrase`
- `concept`

#### Champs facultatifs

Champs recommandes ou observes :

- `auteur_source`
- `rapporteur`
- `citation_originale`
- `langue_originale`
- `traduction_litterale_fr`
- `traduction_editoriale_fr`
- `date_publication`
- `date_enonciation`
- `atomes_lies`
- `attribution_a_arbitrer`
- `type_a_arbitrer`
- `texte_pointeur`
- `migration_concept_register`

Valeurs controlees observees :

- `langue_originale` : `en`, `fr`, `de`, `it`
- `importance` : `forte`, `moyenne`, `faible`
- `statut_verification` original : `verifie`, `a_verifier`, `a_reverifier`

#### Source documentaire

Obligatoire.

`source_id` doit correspondre a une source canonique presente dans `data/registre.json`. Une citation ne peut pas etre ajoutee depuis un document maitre seul, une memoire approximative ou une sortie RAG non verifiee.

#### Relations minimales

Relations existantes dans le modele :

- `source_id` relie la citation a une source `Sxx` ;
- `atomes_lies` peut pointer vers des atomes ;
- `auteur_source`, `locuteur` et `rapporteur` portent l'attribution textuelle ou preparent les relations d'attribution ;
- l'attribution fine ne doit pas etre inventee si elle reste a arbitrer.

#### Cas de refus

Refuser l'ajout si :

- l'identifiant de citation existe deja ;
- `source_id` est absent ou inconnu ;
- le texte original est remplace par une traduction ;
- la citation est longue au point de poser un probleme de droits ou de perimetre ;
- l'attribution est reconstruite sans preuve ;
- `type` sort du vocabulaire ;
- une paraphrase est presentee comme verbatim ;
- la page ou le localisateur est requis par l'usage mais absent sans signalement.

## 4. Fichiers potentiellement modifies

Les fichiers ci-dessous sont les emplacements potentiels identifies dans l'etat reel du depot. Un ajout unitaire ne doit modifier que les fichiers necessaires a son type et ne doit pas corriger au passage des objets sans rapport.

| Type | Registre | Export genere | Relation | Document complementaire |
| --- | --- | --- | --- | --- |
| PERSON | `registers/people/*.md` pour la couche source/provisoire ; `registers/people/00_canonical_people.md` seulement par generation controlee | `exports/generated/people.json` si le pipeline le regenere | `same_as`, hand-off `pending_org.json` ou `pending_concept.json` si necessaire | audit ou note seulement si arbitrage humain requis |
| PLACE | `registers/places/*.md` | export genere par le pipeline de registres si disponible | `same_as`, `reference_croisee`, liens eventuels depuis images, chansons ou atomes | note geo ou prudence si necessaire |
| ORG | `registers/orgs/orgs.json` | export genere par le pipeline de registres si disponible | `joy_division_relation`, `same_as`, `provenance` | audit si collision personne/organisation |
| IMAGE | `registers/images/images.json` | export genere par le pipeline de registres si disponible | `photographer`, `subjects`, `place`, `event_ref`, `session_ref` | note de droits ou provenance si necessaire |
| CONCERT | `registers/concerts/concert_canonical_units.md` pour la couche `CONCERT-` ; `registers/concerts/00_canonical_concerts.md` pour la couche legacy `JD-CONCERT-*` | export genere par le pipeline de registres si disponible | `membres_reconcilies`, `same_as`, `lieu`, `atomes_lies`, `chronologie_id` | note si contradiction de date, statut ou setlist |
| RELEASE | support Songbook reel a confirmer ; references actuelles dans `data/song_dossiers_index.json` et schemas Songbook | index Songbook si le pipeline le regenere | `song_id`, `version_id`, liens eventuels vers lieu, concert ou session | `source_notes` ou notes discographiques si le support existe |
| CITATION | `registers/quotes/*.md` | export genere par le pipeline de registres si disponible | `source_id`, `atomes_lies`, attribution | note d'attribution si arbitrage requis |

Cas normaux :

- ne pas editer a la main un fichier declare genere ;
- ne pas modifier `data/registre.json` pour un ajout unitaire sauf si l'objet est en realite une nouvelle source, ce qui releve de M2.3 ;
- ne pas creer de nouveau registre pour faire entrer un objet qui ne rentre pas dans le modele existant ;
- ne pas modifier les exports si le pipeline les regenere.

## 5. Pre-validations minimales

Avant ouverture de PR, un futur assistant d'ajout devra au minimum verifier :

| Verification | Regle attendue |
| --- | --- |
| Unicite d'identifiant | L'identifiant propose n'existe pas deja dans le registre cible, les exports disponibles ou les alias connus. |
| Schema valide | L'objet satisfait le schema existant lorsqu'il existe. |
| Source connue | Les identifiants `Sxx` utilises comme sources existent dans `data/registre.json`. |
| Source suffisante | La source justifie bien l'existence de l'objet ajoute, pas seulement une URL ou une mention technique. |
| Relation valide | Les identifiants lies existent lorsque le modele exige une relation : `PERSON-`, `PLACE-`, `IMAGE-S-*`, `JD-SONG-*`, `EVENT-*`, atomes. |
| Absence de collision | Le nom, les alias, `same_as`, dates, lieux ou numeros de catalogue ne dupliquent pas un objet existant. |
| Separation source/provenance/droits | Les champs de source documentaire ne contiennent pas de simples identifiants internes ou de provenance technique. |
| Drift genere | Les fichiers declares generes restent coherents avec leur generateur lorsque le depot fournit une sentinelle. |
| Perimetre PR | Le diff reste limite a l'objet ajoute et aux artefacts strictement necessaires. |
| Validation humaine | Les arbitrages non decidables automatiquement sont listes au lieu d'etre resolus silencieusement. |

Commandes de validation possibles dans l'etat actuel du depot, selon le type concerne :

- `python3 tools/validate_people.py`
- `python3 tools/validate_places.py`
- `python3 tools/validate_orgs.py`
- `python3 tools/validate_images.py`
- `python3 tools/validate_concerts.py`
- `python3 tools/validate_quotes.py`
- `python3 tools/check_generated_sync.py`
- `python3 tools/build_all.py`

Cette liste decrit des validations existantes. M2.1 ne cree pas de nouvelle commande.

Note sur `RELEASE` : dans l'etat observe du depot, il n'existe pas encore de validateur gateable dedie aux occurrences discographiques de `schemas/song_occurrence.schema.yaml`. `tools/validate_songs.py` valide les chansons canoniques, pas les occurrences `RELEASE`. Un futur assistant ne doit donc pas presenter `validate_songs.py` comme preuve de validation d'une occurrence discographique.

## 6. Resultat attendu

Un futur assistant d'ajout unitaire doit produire :

- une branche dediee ;
- un diff lisible ;
- un seul objet principal ajoute ;
- les artefacts generes strictement necessaires, si le pipeline les produit ;
- un resume de l'objet ajoute ;
- la liste des fichiers modifies ;
- le resultat des validations executees ;
- les arbitrages humains restants ;
- une Pull Request.

La Pull Request doit permettre a un humain de repondre rapidement a quatre questions :

- quel objet est ajoute ?
- quelle source le justifie ?
- quels fichiers changent ?
- quels controles ont ete passes ?

Un ajout unitaire acceptable peut contenir une reserve documentee, mais seulement si elle est visible dans le diff et explicitement soumise a validation humaine. Une reserve ne doit jamais masquer une source absente, une collision d'identifiant ou un schema invalide.

## 7. Cas explicitement hors perimetre

Relevent de M2.3 ou d'un jalon ulterieur :

- nouveau livre ;
- nouvel article ;
- nouvelle interview ;
- nouveau fanzine ;
- nouvelle archive ;
- nouvelle source canonique dans `data/registre.json` ;
- dossier source complet ;
- atomisation ;
- creation massive de personnes, lieux, organisations, citations ou relations ;
- extraction automatique d'un lot de citations ;
- reconstruction d'une chronologie depuis une source longue ;
- enrichissement discographique global ;
- politique multimedia complete ;
- republication de fichiers image, audio ou video ;
- formulaire ou interface ;
- automatisation de PR assistee au-dela du contrat documentaire ;
- modification des controles M1.

Un ajout doit aussi etre refuse ou reclasse hors M2.1 si sa validation exige de lire et traiter une source entiere plutot que de verifier un objet ponctuel deja identifie.

## 8. Risques

### Risques techniques

- encoder dans un outil des champs non presents dans les schemas ;
- editer a la main des fichiers generes ;
- creer des identifiants incompatibles avec les validateurs ;
- modifier trop de fichiers pour un objet simple ;
- traiter `RELEASE` comme un registre autonome alors que le depot ne l'expose pas ainsi ;
- ouvrir une PR dont les validations ne peuvent pas etre reproduites.

### Risques documentaires

- confondre source canonique, URL, provenance, droit et identifiant interne ;
- accepter un objet sans source suffisante ;
- creer des doublons sous pretexte d'alias ou de variante ;
- perdre les prudences existantes ;
- transformer une entree incertaine en entree canonique sans signalement ;
- introduire une source inconnue dans un champ `sources`.

### Risques historiographiques

- fusionner deux personnes, lieux, concerts ou organisations distincts ;
- imposer une attribution photographique incertaine ;
- presenter une paraphrase comme citation verbatim ;
- creer une relation Joy Division trop forte pour une organisation seulement contextuelle ;
- transformer une occurrence discographique en preuve d'interpretation ;
- supprimer la nuance entre fait atteste, hypothese, conflit et memoire posterieure.

## 9. Decision proposee

Decision proposee :

La version minimale du contrat M2.1 est suffisante pour demarrer M2.2 si les futurs pre-validateurs respectent les limites suivantes :

- ils ne creent aucun nouveau type documentaire ;
- ils s'appuient uniquement sur les champs et schemas deja presents ;
- ils verifient l'unicite d'identifiant avant toute proposition ;
- ils imposent une source documentaire pour tout nouvel objet accepte ;
- ils refusent les sources absentes de `data/registre.json` lorsque le champ attend un identifiant `Sxx` ;
- ils distinguent les cas sans registre autonome, notamment `RELEASE` ;
- ils produisent une PR relisible, sans merge automatique ;
- ils laissent les arbitrages historiographiques a la validation humaine.

Contrat minimal retenu :

Un ajout unitaire acceptable est un objet unique, identifie, documente par une source, compatible avec le modele reel du depot, sans collision connue, limite a ses fichiers necessaires, pre-valide avant PR et soumis a validation humaine.
