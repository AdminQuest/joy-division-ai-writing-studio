# Controle P0 M1 - DM vers registres

# Objet du controle

Le controle DM -> registres est le deuxieme controle P0 M1 parce qu'il verifie la coherence des entites, identifiants, statuts et relations repris dans les documents maitres.

Les documents maitres sont des vues redactionnelles persistantes du corpus exporte. Ils ne sont pas des sources et ne remplacent pas les registres canoniques. Lorsqu'ils affichent une personne, un lieu, une chanson, un concert, une session, une date, une citation, un concept, un motif, un mythe, une organisation ou une relation, cette information doit pouvoir etre reliee a un registre ou a un export de registre identifiable.

Ce controle vient apres DM -> atomes pour trois raisons :

- le controle DM -> atomes etablit d'abord que le document maitre reste rattache au socle atomique minimal ;
- les registres donnent ensuite une verification transversale des identifiants, libelles, statuts et relations qui peuvent etre reutilises dans plusieurs chapitres ;
- la coherence documentaire entre documents maitres et registres ne peut etre interpretee correctement que si le rattachement atomique minimal est deja controle.

Le controle DM -> registres protege donc le passage entre le contenu redactionnel conserve et les objets canoniques qui structurent les entites du corpus. Il prepare les futurs controles de coherence documentaire, sans corriger les documents maitres ni modifier les registres.

Ce document definit le comportement attendu du futur controle. Il ne cree aucun script et ne presente aucun controle comme deja implemente.

# Defaillances couvertes

## Defaillance de tracabilite

Couverture principale.

Le controle doit detecter les cas ou une entite, une date, une citation, un concept, un motif, un mythe ou une relation visible dans un document maitre ne peut pas etre relie a un registre canonique ou a un export de registre.

Exemples couverts :

- identifiant de personne visible dans un document maitre mais absent de `exports/generated/people.json` ;
- identifiant de chanson, concert ou session introuvable dans l'export correspondant ;
- citation affichee sans identifiant resoluble dans `exports/generated/quotes.json` ;
- relation mentionnee sans rattachement exploitable dans les exports de relations ou de graphe documentaire.

## Defaillance de coherence documentaire

Couverture principale.

Le controle doit signaler les divergences entre un document maitre et les registres ou exports canoniques lorsqu'elles sont observables automatiquement ou semi-automatiquement.

Exemples couverts :

- libelle de personne divergent entre document maitre et registre des personnes ;
- chanson affichee avec un titre different de l'export canonique ;
- compteur de personnes, chansons, citations ou evenements incompatible avec `exports/generated/master_docs_index.json` ;
- relation visible dans un document maitre mais non resolue dans les exports disponibles.

## Defaillance de statut documentaire

Couverture partielle.

Le controle peut detecter des usages suspects lorsqu'un objet non canonique ou non qualifie est traite comme registre dans un document maitre. Il ne peut pas, a lui seul, arbitrer tous les statuts documentaires.

Exemples partiellement couverts :

- sortie RAG ou note temporaire reprise comme si elle etait un registre ;
- citation candidate affichee comme citation stabilisee ;
- relation exploratoire affichee sans statut ;
- objet specialise non couvert par le MVP mais utilise comme reference stable.

## Defaillances partiellement couvertes

Le controle DM -> registres peut fournir des indices sur :

- derivabilite : une relation ou entite non retrouvee dans les registres peut signaler une information non reconstruisible, mais la preuve fine exige un controle de contenu ;
- obsolescence : un libelle divergent peut indiquer un document maitre perime, mais le controle ne compare pas encore tous les horodatages et dependances ;
- generation : une divergence entre document maitre et export peut signaler une regeneration manquante, mais la synchronisation des artefacts generes releve de controles dedies.

## Defaillances non couvertes

Le controle DM -> registres ne couvre pas :

- la validation directe des sources primaires ;
- le controle DM -> sources ;
- le controle DM -> exports complet ;
- la verification passage par passage ;
- l'arbitrage historiographique entre versions concurrentes ;
- la correction des registres ;
- la correction ou regeneration des documents maitres ;
- la qualification definitive des citations publiables.

# Question de controle

Pour un document maitre donne :

- quelles entites et quels registres sont mobilises ?
- les identifiants visibles sont-ils resolus dans les registres attendus ?
- les libelles affiches sont-ils coherents avec les registres canoniques ?
- les statuts ou relations affiches sont-ils retrouvables ?
- les compteurs de registres sont-ils coherents avec les exports ou l'index ?

La question centrale n'est pas de savoir si le document maitre est complet. Elle est de savoir si les objets de registre qu'il mobilise restent identifiables, resolubles et coherents avec les objets canoniques du corpus.

# Objet controle

Le futur controle portera sur :

- les documents maitres `chapters/*/document_maitre.md` ;
- le manifeste `chapters/master_docs.json` ;
- les registres canoniques sous `registers/` ;
- les exports de registres sous `exports/generated/` ;
- `exports/generated/master_docs_index.json` pour les volumetries principales ;
- `exports/generated/index_by_id.json` si une resolution transversale des identifiants est necessaire ;
- les exports de graphe ou de relations, notamment `exports/generated/documentary_edges.json`, `exports/generated/documentary_graph.json` ou `exports/generated/edges.json`, si le MVP decide de les utiliser.

Hors perimetre :

- les sources primaires ;
- les fichiers d'atomes source sous `sources/` ;
- la correction des registres ;
- la correction des documents maitres ;
- la regeneration de documents maitres ;
- la validation editoriale des passages ;
- les livrables RAG conserves ;
- les brouillons et notes de travail hors documents maitres.

# Registres concernes

## Registres P0

Les registres P0 sont ceux qui sont fortement visibles dans les documents maitres, presents dans les exports generes et utiles a une premiere coherence transversale.

| Famille | Registre ou export principal | Raison P0 |
| --- | --- | --- |
| Personnes | `registers/people/`, `exports/generated/people.json` | Entites centrales, reutilisees dans plusieurs chapitres et deja comptees dans `master_docs_index.json`. |
| Chansons | `registers/songs/`, `exports/generated/songs.json` | Objets recurrents du manuscrit et souvent relies a concerts, sessions, albums ou analyses. |
| Chronologie | `registers/chronology/`, `exports/generated/chronology.json` | Supporte la coherence temporelle et les compteurs de chronologie. |
| Citations | `registers/quotes/`, `exports/generated/quotes.json` | Objets sensibles pour la tracabilite et le statut documentaire. |
| Concerts | `registers/concerts/`, `exports/generated/concerts.json` | Entites evenementielles structurantes, reliees aux lieux, dates et personnes. |
| Sessions | `registers/sessions/`, `exports/generated/sessions.json` | Objets utiles aux passages sur enregistrement, production et trajectoire musicale. |

## Registres P1

Les registres P1 sont importants mais demandent davantage d'arbitrage de libelles, de typologie ou de relations.

| Famille | Registre ou export principal | Raison P1 |
| --- | --- | --- |
| Lieux | `registers/places/`, `exports/generated/places.json` | Les alias et granularites geographiques peuvent produire des faux positifs. |
| Concepts | `registers/concepts/`, `exports/generated/concepts.json` | Les libelles peuvent etre synthetiques ou varies selon le contexte redactionnel. |
| Motifs | `registers/motifs/`, `exports/generated/motifs.json` | Les motifs peuvent etre selectionnes ou reformules dans les documents maitres. |
| Mythes | `registers/myths/`, `exports/generated/myths.json` | Leur statut interpretatif impose une qualification humaine. |
| Organisations | `registers/organizations/`, `registers/orgs/` | La coexistence de familles proches peut demander un arbitrage prealable. |
| Relations | `registers/relations/`, exports de graphe | Les relations transversales sont centrales mais souvent plus difficiles a qualifier automatiquement. |

## Registres hors MVP

Restent hors MVP :

- `registers/images/`, sauf si un document maitre affiche explicitement des identifiants d'images ;
- `registers/references/`, si les objets relevent davantage de la bibliographie ou des sources ;
- `registers/specialized/`, sauf decision explicite de rattachement a une famille P0 ou P1 ;
- tout registre non exporte ou non stabilise ;
- toute relation dont le statut canonique n'est pas encore clairement lisible dans les exports.

# Donnees necessaires

## Fichiers

- `chapters/*/document_maitre.md` : documents maitres a controler ;
- `chapters/master_docs.json` : manifeste des documents maitres ;
- `exports/generated/master_docs_index.json` : volumetries principales par document maitre ;
- `exports/generated/index_by_id.json` : index transversal eventuel ;
- `exports/generated/people.json` ;
- `exports/generated/songs.json` ;
- `exports/generated/chronology.json` ;
- `exports/generated/quotes.json` ;
- `exports/generated/concerts.json` ;
- `exports/generated/sessions.json` ;
- exports P1 eventuels : `places.json`, `concepts.json`, `motifs.json`, `myths.json` ;
- exports de relations eventuels : `documentary_edges.json`, `documentary_graph.json`, `edges.json`.

## Metadonnees

Le futur controle aura besoin des metadonnees suivantes :

- chemin du document maitre ;
- numero ou identifiant de chapitre ;
- famille de registre identifiee ;
- identifiant visible dans le document maitre ;
- libelle visible dans le document maitre, si extractible ;
- identifiant canonique retrouve dans l'export ou le registre ;
- libelle canonique retrouve ;
- statut ou type de l'objet, lorsque disponible ;
- compteur attendu dans `master_docs_index.json`, lorsque disponible ;
- compteur observe dans le document maitre, lorsque disponible.

## Champs requis

Le futur controle doit au minimum pouvoir lire :

- `id` ou identifiant equivalent de l'objet de registre ;
- libelle ou titre canonique ;
- famille documentaire de l'objet ;
- chemin ou chapitre de rattachement si disponible ;
- statut, type ou categorie lorsque le registre l'expose ;
- liens ou relations lorsque l'objet est controle dans le MVP ;
- volumetrie attendue par document maitre pour les familles deja presentes dans `master_docs_index.json`.

Ce document ne definit pas encore le format exact du rapport produit par un script.

# Methode theorique

Le futur controle pourrait suivre les etapes suivantes.

## 1. Identification du document maitre

Identifier le document maitre a controler depuis :

- le manifeste `chapters/master_docs.json` ;
- les fichiers `chapters/*/document_maitre.md` ;
- l'index `exports/generated/master_docs_index.json`.

Le controle devra conserver les protections deja etablies par DM -> atomes : ne pas lire de chemin invalide, ne pas suivre des symlinks hors perimetre et signaler les incoherences de manifeste ou d'index sans corriger.

## 2. Extraction des identifiants de registres visibles

Extraire les identifiants visibles relevant de registres.

Les points d'extraction probables sont :

- tableaux de bord du document maitre ;
- sections de personnes, chansons, chronologies, citations ou relations ;
- listes de concepts, motifs ou mythes ;
- lignes contenant des identifiants explicites ;
- blocs de relations ou d'entites transversales.

L'extraction doit distinguer :

- identifiant explicite ;
- libelle visible sans identifiant ;
- compteur global ;
- relation textuelle non resolue.

## 3. Classification par famille de registre

Classer les identifiants ou libelles extraits par famille :

- personne ;
- lieu ;
- chanson ;
- concert ;
- session ;
- chronologie ;
- citation ;
- concept ;
- motif ;
- mythe ;
- organisation ;
- relation.

Un objet non classable ne doit pas etre force dans une famille. Il doit etre signale comme hors MVP ou non qualifie selon le cas.

## 4. Resolution dans les exports ou registres canoniques

Verifier que les identifiants extraits existent dans les exports disponibles.

Le MVP devrait privilegier les exports JSON generes, car ils donnent une vue uniforme et regenerable du corpus. Les registres source sous `registers/` peuvent rester utiles pour diagnostic humain, mais ne doivent pas etre modifies par le controle.

## 5. Comparaison des libelles affiches

Comparer les libelles affiches dans le document maitre avec les libelles canoniques lorsque le format le permet.

La comparaison doit etre prudente :

- normaliser les espaces et la casse si necessaire ;
- distinguer alias acceptable et divergence ;
- ne pas qualifier automatiquement une abreviation comme erreur ;
- conserver la preuve textuelle de la divergence observee.

## 6. Comparaison des volumetries principales

Comparer les compteurs visibles ou declares avec `exports/generated/master_docs_index.json` pour les familles disponibles.

Le MVP peut commencer par les compteurs deja presents dans l'index :

- `people` ;
- `songs` ;
- `quotes` ;
- `chronology`.

Les compteurs absents de l'index ne doivent pas etre inventes. Ils peuvent etre signales comme hors MVP.

## 7. Detection des ecarts

Identifier notamment :

- identifiant de registre introuvable ;
- famille de registre non determinee ;
- libelle divergent ;
- relation non resolue ;
- compteur incoherent ;
- document maitre absent ;
- entree d'index ou de manifeste incoherente ;
- registre non couvert par le MVP.

## 8. Qualification des resultats

Qualifier le document maitre et les ecarts observes selon une grille stable :

- statut global du document ;
- famille de registre concernee ;
- type d'ecart ;
- gravite ;
- preuve ou champ observe ;
- action documentaire recommandee.

La qualification doit rester un constat. Le controle ne doit jamais corriger les documents maitres, les registres, les exports ou le manifeste.

# Resultats attendus

Les sorties theoriques du controle pourraient utiliser les statuts suivants.

| Resultat | Definition |
| --- | --- |
| DM coherent avec les registres | Les identifiants et compteurs MVP visibles sont resolus dans les exports attendus et ne presentent pas de divergence de libelle significative. |
| DM partiellement coherent | Une partie des identifiants ou compteurs est resolue, mais certains objets restent non couverts, ambigus ou incomplets. |
| Identifiant de registre introuvable | Un identifiant visible dans le document maitre est absent de l'export ou de l'index attendu. |
| Libelle divergent | Un libelle affiche ne correspond pas au libelle canonique ou a un alias accepte. |
| Relation non resolue | Une relation visible ne peut pas etre retrouvee dans les exports de relations ou de graphe disponibles. |
| Compteur incoherent | Une volumetrie visible ou declaree ne correspond pas a `master_docs_index.json` ou a l'export cible. |
| Registre non couvert par le MVP | La famille est identifiee mais volontairement hors perimetre de la premiere implementation. |
| Objet non qualifie | L'objet visible ne peut pas etre rattache de maniere fiable a une famille de registre. |

Le resultat doit separer :

- le statut global du document maitre ;
- les ecarts par famille de registre ;
- les objets hors MVP ;
- les faux positifs possibles ;
- les recommandations de suite M1.

# Grille de gravite

| Gravite | Criteres |
| --- | --- |
| Bloquant | Un document maitre mobilise des identifiants ou relations structurants impossibles a resoudre, rendant impossible la verification minimale de coherence documentaire. |
| Majeur | Un objet central ou fortement reutilise diverge du registre canonique, ou un compteur structurant est incoherent. |
| Mineur | L'ecart concerne un libelle secondaire, une abreviation, un objet peu reutilise ou une famille P1 sans effet direct sur la coherence du chapitre. |
| Informationnel | Le constat clarifie le statut ou le perimetre du controle sans imposer de correction immediate. |

La gravite doit tenir compte :

- de la famille de registre ;
- du statut canonique ou non de l'objet ;
- de sa reutilisation interchapitres ;
- de sa visibilite dans le document maitre ;
- du risque de propagation vers la redaction ;
- de la possibilite de reproduire l'ecart.

# Faux positifs connus

Le futur controle devra eviter de transformer toute difference de presentation en defaillance demontree.

Faux positifs probables :

- libelles abreges dans les documents maitres ;
- differences de casse, ponctuation ou typographie ;
- alias de personnes, lieux, groupes ou organisations ;
- entites historiques dont le nom varie selon les sources ;
- chansons affichees avec un titre courant different du titre canonique ;
- concepts ou motifs reformules pour la lisibilite ;
- registres non encore exportes ;
- relations affichees mais non controlables dans le MVP ;
- citations candidates ou a verifier ;
- objets presents dans un export mais volontairement absents d'une section visible du document maitre.

Une alerte ne doit etre qualifiee comme defaillance M1 que si un objet precis est identifie : identifiant absent, libelle divergent non explique, relation introuvable, compteur incompatible ou statut documentaire non qualifie.

# Cas limites

Le controle devra documenter les cas limites suivants :

- anciens schemas de registres ;
- identifiants renommes ou migres ;
- entites multi-registres, par exemple une personne aussi rattachee a une organisation ;
- relations transversales entre personnes, lieux, chansons, concerts et sessions ;
- objets presents dans les exports mais non dans les registres sources ;
- objets presents dans les registres mais non affiches dans les documents maitres ;
- familles proches, notamment `organizations` et `orgs` ;
- registres specialises dont la famille canonique n'est pas encore tranchee ;
- evolution future du corpus ou des exports ;
- documents maitres generes avec une version anterieure du pipeline.

# MVP du controle

La premiere version realiste du controle doit obtenir rapidement un resultat utile sans pretendre couvrir toute la coherence documentaire.

Le MVP pourrait :

- lire le manifeste `chapters/master_docs.json` ;
- verifier que les 14 documents maitres existent ;
- extraire les identifiants visibles relevant de registres ;
- verifier leur presence dans les exports disponibles ;
- comparer les principales volumetries de registres avec `exports/generated/master_docs_index.json` ;
- produire un statut global par document maitre ;
- produire une liste d'ecarts par famille de registre.

Le MVP devrait commencer par :

- personnes ;
- chansons ;
- chronologie ;
- citations ;
- concerts ;
- sessions.

Le MVP ne doit pas :

- verifier chaque passage redactionnel ;
- arbitrer les divergences historiographiques ;
- corriger les registres ;
- corriger les documents maitres ;
- valider les citations comme citations publiables ;
- controler tous les registres specialises ;
- remplacer le jugement humain ;
- integrer automatiquement le controle a `build_all.py`, `check_generated_sync.py` ou GitHub Actions sans PR dediee.

# Preparation de l'implementation

## Ce qui est deja defini

- La doctrine M0 : Corpus = socle documentaire, RAG = outil d'exploration, Manuscript = outil redactionnel, documents maitres = vues redactionnelles persistantes du corpus exporte.
- La typologie M1 des defaillances documentaires.
- La cartographie M1 des controles, qui classe DM -> registres en P0.
- Le controle DM -> atomes, deja implemente comme MVP dans `tools/check_dm_atoms_traceability.py`.
- Les protections attendues pour un controle non destructif : lecture seule du corpus, rapport regenerable et absence de correction automatique.

## Ce qui reste a arbitrer

- Le format exact des identifiants de registre a extraire dans les documents maitres.
- La liste definitive des familles P0 couvertes par la premiere implementation.
- Les regles de normalisation de libelles.
- La gestion des alias.
- La distinction entre relation non resolue et relation hors MVP.
- Le format du futur rapport.
- Le statut des registres proches ou redondants, notamment `organizations` et `orgs`.

## Ce qui devra etre valide avant ecriture du script

- Les chemins d'entree exacts.
- Les champs disponibles dans chaque export JSON.
- Les compteurs exploitables dans `master_docs_index.json`.
- Le comportement attendu en cas de document maitre absent, hors manifeste ou symlinke.
- La liste des familles hors MVP.
- Les seuils de gravite pour identifiant introuvable, libelle divergent et compteur incoherent.
- La garantie que le controle reste strictement en lecture.

# Conclusion

Le controle DM -> registres est moyennement automatisable.

Il est plus complexe que DM -> atomes parce qu'il ne suffit pas de verifier la presence d'identifiants dans un export unique. Les registres couvrent plusieurs familles, plusieurs formats, des alias, des libelles variables et des relations transversales. Une premiere implementation peut toutefois etre utile rapidement si elle se limite a un MVP : identification des documents maitres, extraction des identifiants visibles, resolution dans les exports disponibles et comparaison de quelques volumetries principales.

Le controle ne doit donc pas chercher a prouver toute la coherence documentaire. Il doit produire des constats robustes, limites et relisibles humainement, afin de preparer les suites M1 sans ouvrir M2.
