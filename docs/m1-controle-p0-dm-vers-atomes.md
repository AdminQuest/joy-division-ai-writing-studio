# Controle P0 M1 - DM vers atomes

# Objet du controle

Le controle DM -> atomes est le premier controle P0 M1 parce qu'il verifie l'ancrage documentaire minimal des documents maitres.

Les documents maitres sont les vues redactionnelles persistantes les plus exposees du corpus exporte. Ils ne sont pas des sources et ne constituent pas des preuves autonomes, mais ils concentrent les informations appelees a circuler vers le travail de redaction. Leur fiabilite depend donc de leur capacite a rester relies aux atomes qui les soutiennent.

Ce controle est prioritaire avant les autres controles M1 pour trois raisons :

- il etablit si un document maitre peut etre relie au corpus a un niveau plus fin que la simple liste de sources ;
- il prepare les controles de derivabilite, qui ne peuvent etre interpretes que si les atomes d'appui sont identifiables ;
- il fournit une base stable pour les controles ulterieurs DM -> sources, DM -> registres et DM -> exports.

Ce document ne cree pas le controle. Il definit le comportement attendu d'un futur controle M1 et les arbitrages a valider avant implementation.

# Defaillances couvertes

## Defaillance de tracabilite

Couverture principale.

Le controle doit detecter les cas ou un document maitre, une section ou un bloc d'information ne peut pas etre rattache a des atomes identifiables dans le corpus exporte.

Exemples couverts :

- atome affiche dans un document maitre mais introuvable dans `exports/generated/atoms.json` ;
- atome mentionne sans identifiant exploitable ;
- volume d'atomes declare incoherent avec les atomes effectivement rattaches ;
- section redactionnelle qui annonce des atomes d'appui sans les exposer ou les rendre retrouvables.

## Defaillance de derivabilite

Couverture partielle.

Le controle DM -> atomes ne peut pas prouver a lui seul qu'une formulation redactionnelle est entierement derivable du corpus. Il peut cependant signaler les zones ou la derivabilite devient suspecte, notamment lorsqu'un contenu du document maitre ne dispose d'aucun atome d'appui identifiable.

Exemples partiellement couverts :

- information presente dans un document maitre mais sans atome d'appui visible ;
- synthese de chapitre impossible a rattacher a un ensemble d'atomes ;
- interpretation conservee sans base atomique explicite.

## Defaillances partiellement couvertes

Le controle peut fournir des indices pour d'autres defaillances M1 sans les traiter completement :

- obsolescence : un atome retrouve mais modifie depuis la derniere generation du document maitre peut signaler un risque de peremption, mais ce controle ne compare pas les horodatages ni les dependances completes ;
- coherence documentaire : une divergence visible entre le contenu d'un atome et son rendu dans le document maitre peut etre signalee, mais l'arbitrage exige un controle de contenu plus fin ;
- generation : un ecart entre atomes exportes et document maitre peut suggerer une regeneration manquante, mais la synchronisation canonique releve de controles dedies comme `tools/check_generated_sync.py`.

## Defaillances non couvertes

Le controle DM -> atomes ne couvre pas :

- la verification directe des sources primaires ;
- la validation des citations ;
- la coherence entre registres ;
- le statut documentaire des livrables RAG ;
- l'obsolescence complete des documents maitres ;
- la correction des donnees atomiques ;
- la generation ou regeneration des documents maitres.

# Question de controle

Pour un document maitre donne :

- quels atomes le soutiennent ?
- combien d'atomes sont annonces, affiches ou rattaches ?
- ces atomes sont-ils identifiables par des identifiants stables ?
- ces identifiants existent-ils dans les exports du corpus ?
- les atomes retrouves sont-ils coherents avec le contenu visible du document maitre ?

La question centrale n'est pas de savoir si le document maitre est bien ecrit ou complet. Elle est de savoir si son contenu documentaire peut etre rattache a des atomes existants et exploitables.

# Objet controle

Le futur controle portera sur :

- les documents maitres `chapters/*/document_maitre.md` ;
- les atomes du corpus exporte, notamment `exports/generated/atoms.json` ;
- l'index documentaire `exports/generated/master_docs_index.json` ;
- l'index global `exports/generated/index_by_id.json` si necessaire ;
- le manifeste `chapters/master_docs.json` si le controle doit identifier le perimetre attendu des documents maitres.

Les documents maitres restent des vues generees par `tools/build_master_docs.py`. Le controle ne doit pas les traiter comme des sources ni comme des preuves autonomes.

Hors perimetre :

- les sources primaires ;
- les fichiers d'atomes source sous `sources/`, sauf pour diagnostic humain separe ;
- les registres non atomiques, sauf si leur contenu est necessaire a une qualification secondaire ;
- les livrables RAG conserves ;
- les brouillons redactionnels hors documents maitres ;
- toute correction ou regeneration.

# Donnees necessaires

## Fichiers

- `chapters/*/document_maitre.md` : vues redactionnelles persistantes a controler ;
- `chapters/master_docs.json` : manifeste des documents maitres ;
- `exports/generated/atoms.json` : export canonique des atomes ;
- `exports/generated/master_docs_index.json` : index genere des rattachements et volumetries ;
- `exports/generated/index_by_id.json` : resolution eventuelle des identifiants ;
- `tools/build_master_docs.py` : producteur technique actuel des documents maitres, cite seulement comme contexte de generation.

## Metadonnees

Le controle aura besoin des metadonnees suivantes :

- chemin du document maitre ;
- numero ou identifiant de chapitre ;
- identifiants d'atomes affiches dans le document maitre ;
- volumetrie d'atomes declaree dans le document maitre ;
- atomes rattaches dans `master_docs_index.json` lorsque disponibles ;
- presence de l'atome dans `atoms.json` ;
- champs de base de l'atome retrouve : `id`, `source_id`, `source_label`, `type_unite`, `importance`, `resume`, `usage_livre`.

## Champs requis

Le futur controle doit au minimum pouvoir lire :

- `id` de l'atome ;
- chemin ou identifiant du document maitre ;
- liste ou compteur d'atomes rattaches au document maitre ;
- statut de presence ou absence dans les exports ;
- valeur observee dans le document maitre lorsque l'atome est affiche.

Ce document ne definit pas encore le format exact du rapport produit par un script.

# Methode theorique

Le futur controle pourrait suivre les etapes suivantes.

## 1. Identification du document maitre

Identifier le document maitre a controler depuis :

- le chemin `chapters/*/document_maitre.md` ;
- le manifeste `chapters/master_docs.json` ;
- l'index `exports/generated/master_docs_index.json`.

Le controle doit signaler tout document maitre present hors manifeste ou tout manifeste pointant vers un document absent.

## 2. Extraction des atomes references

Extraire les atomes visibles ou declares dans le document maitre.

Les points d'extraction probables sont :

- les sections d'atomes critiques ou majeurs ;
- les sections d'autres atomes utiles ;
- les tableaux de bord internes ;
- les lignes contenant des identifiants atomiques explicites ;
- les volumetries declarees.

Le controle doit distinguer les identifiants explicitement affiches des volumetries globales. Une volumetrie n'est pas une preuve suffisante de rattachement atome par atome.

## 3. Comparaison avec les atomes declares

Comparer les atomes extraits avec :

- les atomes rattaches au chapitre dans `master_docs_index.json` ;
- les atomes disponibles dans `exports/generated/atoms.json` ;
- les references resolues par `exports/generated/index_by_id.json`, si necessaire.

Cette comparaison doit produire des constats, pas des corrections.

## 4. Detection des ecarts

Identifier notamment :

- identifiant d'atome absent du corpus exporte ;
- atome attendu mais non affiche ;
- atome affiche mais absent des rattachements attendus ;
- compteur declare incompatible avec le nombre d'atomes rattaches ;
- atome present mais prive d'un champ minimal necessaire a la tracabilite ;
- contenu affiche dont l'atome source ne peut pas etre retrouve.

## 5. Qualification des resultats

Qualifier le document maitre et les ecarts observes selon une grille stable :

- niveau de tracabilite ;
- type d'ecart ;
- gravite ;
- element de preuve ;
- action documentaire recommandee.

Le controle doit permettre une relecture humaine. Un resultat automatique ne doit pas suffire a conclure a une defaillance de derivabilite fine sans passage precis identifie.

# Resultats attendus

Les sorties theoriques du controle pourraient utiliser les statuts suivants.

| Resultat | Definition |
| --- | --- |
| DM tracable | Les atomes affiches ou declares sont identifiables et retrouves dans les exports attendus. |
| DM partiellement tracable | Une partie des atomes est identifiable, mais certaines listes, sections ou volumetries restent insuffisamment reliees. |
| DM non tracable | Le document maitre ne permet pas d'identifier les atomes qui le soutiennent. |
| Atome manquant | Un identifiant attendu est cite ou derive du document maitre mais absent des exports. |
| Atome orphelin | Un atome semble rattache au document maitre dans les exports, mais n'apparait dans aucune section exploitable du document maitre. |
| Atome non retrouve | Un identifiant visible dans le document maitre ne peut pas etre resolu dans `atoms.json` ou `index_by_id.json`. |
| Incoherence de volumetrie | Le nombre d'atomes declare dans le document maitre, l'index ou les exports ne concorde pas. |
| Trace insuffisante | Les atomes existent, mais le rattachement reste trop global pour qualifier la tracabilite au niveau eleve. |

Le resultat doit separer :

- le statut global du document maitre ;
- la liste des atomes en ecart ;
- les reservations methodologiques ;
- les recommandations de suite M1.

# Grille de gravite

| Gravite | Criteres |
| --- | --- |
| Bloquant | Le document maitre ne peut pas etre rattache aux atomes exportes, ou un ecart empeche toute verification documentaire avant decision de merge ou de jalon. |
| Majeur | Un ou plusieurs atomes critiques, majeurs ou fortement reutilises sont absents, non retrouves ou incoherents avec le document maitre. |
| Mineur | L'ecart concerne un atome utile, une volumetrie secondaire ou une trace incomplete sans effet direct sur une information structurante. |
| Informationnel | Le constat ameliore la qualite de l'audit sans imposer de correction immediate. |

La gravite doit tenir compte :

- du statut de l'atome ;
- de son importance ;
- de son usage dans le document maitre ;
- de sa reutilisation interchapitres ;
- de la possibilite de reproduire l'ecart ;
- du risque de propagation vers d'autres controles M1.

# Faux positifs connus

Le futur controle devra eviter de transformer toute limite documentaire en defaillance demontree.

Faux positifs probables :

- listes d'atomes selectionnees dans les documents maitres : l'absence d'un atome dans une section visible ne signifie pas forcement qu'il n'est pas rattache au document ;
- atomes herites d'un ancien schema et encore incomplets, mais correctement retrouves dans les exports ;
- sections qui exposent seulement les atomes critiques ou majeurs, alors que les atomes utiles sont rattaches ailleurs ;
- differences de libelle ou de typographie entre un resume d'atome et son rendu dans le document maitre ;
- atomes supportant une synthese sans etre cites passage par passage ;
- atomes presents dans `master_docs_index.json` mais non affiches pour des raisons de seuil ou de selection redactionnelle ;
- citations candidates ou a verifier, qui limitent la reutilisation mais ne sont pas en soi des atomes manquants.

Une alerte ne doit donc etre qualifiee comme defaillance M1 que si un element precis est identifie : identifiant absent, atome introuvable, compteur incoherent, trace impossible ou contenu non rattache.

# Cas limites

Le controle devra documenter les cas limites suivants :

- documents maitres historiques generes avec une version anterieure du pipeline ;
- evolution du schema des atomes ou des champs exportes ;
- changements d'identifiants atomiques ;
- exports partiels ou absents dans un environnement de travail incomplet ;
- document maitre ajoute au depot mais non encore inscrit dans le manifeste ;
- atomes rattaches a plusieurs chapitres ;
- atomes dont `usage_livre` ne correspond pas exactement a la structure actuelle des chapitres ;
- corrections futures du corpus modifiant la volumetrie sans changement redactionnel visible ;
- futures evolutions du corpus qui pourraient ajouter un rattachement plus fin passage -> atome.

Ces cas limites doivent etre signales comme reservations ou besoins d'arbitrage, pas automatiquement comme defaillances bloquantes.

# MVP du controle

La premiere version realiste du controle doit chercher un resultat utile rapidement, sans viser une tracabilite parfaite.

MVP propose :

- lire le manifeste des documents maitres ;
- verifier que les 14 documents maitres attendus existent ;
- extraire les identifiants d'atomes explicitement visibles dans chaque document maitre ;
- verifier que chaque identifiant extrait existe dans `exports/generated/atoms.json` ;
- comparer les volumetries principales avec `exports/generated/master_docs_index.json` ;
- signaler les atomes visibles mais introuvables ;
- signaler les documents sans atomes visibles ;
- produire un statut global par document maitre : tracable, partiellement tracable, non tracable.

Ce MVP ne doit pas :

- reconstruire le document maitre ;
- verifier chaque passage redactionnel ;
- valider les sources primaires ;
- corriger les atomes ;
- regenerer les exports ;
- modifier les documents maitres.

# Preparation de l'implementation

## Ce qui est deja defini

- les defaillances M1 ;
- la cartographie des controles M1 ;
- la priorite P0 du controle DM -> atomes ;
- le statut des documents maitres comme vues generees ;
- le producteur technique actuel des documents maitres : `tools/build_master_docs.py` ;
- la premiere boucle M1 ayant montre l'utilite d'un controle ciblant les atomes.

## Ce qui reste a arbitrer

- format exact du rapport de controle ;
- niveau de sortie attendu : console, Markdown, JSON, CSV ou combinaison ;
- seuil de passage entre DM tracable et DM partiellement tracable ;
- statut des atomes rattaches mais non affiches ;
- usage exact de `master_docs_index.json` par rapport au contenu Markdown des documents maitres ;
- gestion des documents historiques ou incomplets ;
- integration eventuelle au tableau de bord M1.

## A valider avant ecriture du script

Avant toute implementation, il faudra valider :

- le perimetre exact des documents controles ;
- la liste canonique des exports lus ;
- la definition d'un atome attendu ;
- la difference entre trace globale, trace sectionnelle et trace passage par passage ;
- la forme de la gravite retournee ;
- les cas ou une alerte doit rester une reserve methodologique ;
- le fait que le controle ne modifie aucun fichier.

Cette PR ne realise pas cette implementation.

# Conclusion

Le controle DM -> atomes est moyennement automatisable.

Il est facilement automatisable pour les verifications structurelles : existence des documents maitres, extraction d'identifiants, presence des atomes dans les exports et comparaison de volumetries.

Il devient plus difficile pour les controles de coherence fine, car les documents maitres ne fournissent pas encore de table explicite passage -> atome. Une automatisation fiable devra donc commencer par un MVP prudent, produire des constats verifiables et laisser les qualifications fines a une relecture documentaire.

Le controle est neanmoins suffisamment cadrable pour devenir le premier controle P0 M1, a condition de ne pas le presenter comme deja implemente et de ne pas lui demander de trancher seul la derivabilite passage par passage.
