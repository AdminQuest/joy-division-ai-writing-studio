# M1 — Qualite documentaire des vues et livrables

## Objet

Cette note ouvre le cadrage M1 apres la stabilisation M0 de l'architecture Corpus, RAG, Manuscript et documents maitres.

M1 ne cree pas de nouveau pipeline technique. Il definit les controles documentaires a formaliser pour verifier que les vues persistantes, les documents maitres et les livrables conserves restent fiables, derivables et clairement qualifies.

Cette note n'ouvre pas de chantier M2. Elle ne cree pas de script de controle, ne modifie pas la roadmap et ne change pas le statut technique des documents maitres.

## Objectifs M1

M1 vise quatre objectifs documentaires.

### Tracabilite

Chaque information conservee dans une vue redactionnelle persistante doit pouvoir etre reliee au corpus.

La tracabilite attendue porte notamment sur :

- les sources ;
- les atomes ;
- les citations ;
- les registres ;
- les exports generes ;
- le script ou le pipeline qui produit la vue.

La tracabilite ne transforme pas une vue en source. Elle permet seulement d'etablir par quels objets du corpus une information peut etre verifiee.

### Obsolescence

M1 doit permettre d'identifier les vues qui ne correspondent plus aux objets dont elles dependent.

Un document maitre, un export ou un livrable conserve peut devenir obsolete si :

- les sources ou atomes de reference ont ete modifies ;
- un registre canonique a change ;
- un export a ete regenere avec un contenu different ;
- le script de generation a change de logique ;
- le livrable n'a pas ete requalifie apres evolution du corpus.

### Coherence documentaire

M1 doit verifier que les informations presentes dans les documents maitres et les livrables conserves restent coherentes avec les objets persistants du corpus.

La coherence documentaire concerne les correspondances entre :

- identifiants ;
- libelles ;
- citations ;
- personnes, lieux, chansons, concerts, sessions et autres entites ;
- relations inter-registres ;
- champs de statut ou de fiabilite.

### Statut des livrables

M1 doit clarifier le statut des sorties qui circulent entre corpus, RAG, documents maitres et Manuscript.

Un livrable RAG, une note de chapitre ou une vue intermediaire ne doit pas rester dans un statut implicite. Son usage doit indiquer s'il s'agit d'un brouillon temporaire, d'un livrable conserve, d'un document maitre, d'une sortie generee, d'un element obsolete ou d'un element suspect.

## Typologie des controles

Les controles M1 sont d'abord des controles de relation entre les documents maitres et leurs dependances documentaires.

### DM -> sources

Verifier que les informations d'un document maitre peuvent etre reliees aux sources declarees ou aux references conservees dans le corpus.

Ce controle doit permettre de reperer les citations, faits, interpretations ou attributions qui apparaissent dans un document maitre sans source identifiable.

### DM -> atomes

Verifier que les blocs d'information d'un document maitre restent derivables des atomes disponibles.

Ce controle doit permettre de distinguer :

- une information issue directement d'un atome ;
- une synthese derivable de plusieurs atomes ;
- une information qui n'a pas d'ancrage atomique clair.

### DM -> registres

Verifier que les entites, libelles, statuts et relations presents dans un document maitre restent coherents avec les registres canoniques.

Ce controle concerne notamment les personnes, lieux, chansons, concerts, sessions, concepts, motifs et mythes.

### DM -> exports

Verifier que les documents maitres correspondent aux exports generes depuis le corpus.

Ce controle sert a detecter les divergences entre une vue redactionnelle persistante et les donnees exportees qui devraient l'alimenter ou permettre de l'auditer.

### DM -> script de generation

Verifier que le document maitre observe correspond au producteur technique attendu.

Dans l'etat actuel du repo, ce producteur est `tools/build_master_docs.py`. M1 doit donc pouvoir distinguer :

- le principe conceptuel : le document maitre est une vue redactionnelle persistante du corpus exporte ;
- le pipeline technique reel : le document maitre est produit par `tools/build_master_docs.py`, et non par le RAG.

## Typologie des anomalies

### Information orpheline

Information presente dans un document maitre ou un livrable conserve sans lien identifiable vers une source, un atome, une citation, un registre ou un export.

Une information orpheline doit etre signalee avant toute reutilisation editoriale forte.

### Information non derivable

Information qui peut sembler documentee mais dont le contenu ne peut pas etre derive des objets du corpus disponibles.

Une information non derivable est plus grave qu'une simple absence de lien : elle indique un ecart entre la vue et le corpus.

### Document maitre perime

Document maitre qui ne reflete plus l'etat courant des objets dont il depend.

Un document maitre perime doit etre marque comme obsolete ou a regenerer selon la cause de l'ecart.

### Divergence entre export et DM

Ecart entre un export genere et le document maitre qui devrait en etre une vue persistante ou une synthese derivable.

Cette divergence peut provenir d'une regeneration incomplete, d'un changement de schema, d'un script de generation non relance ou d'un livrable conserve hors pipeline.

### Divergence entre registre et DM

Ecart entre un registre canonique et les entites, statuts ou relations repris dans un document maitre.

Cette anomalie peut concerner un identifiant, un libelle, une attribution, un statut de fiabilite ou une relation inter-registre.

### Livrable RAG non qualifie

Sortie issue d'une exploration RAG dont le statut documentaire n'est pas explicite.

Un livrable RAG non qualifie ne doit pas etre traite comme document maitre, preuve ou source. Il doit etre classe, conserve avec statut, remplace, ou abandonne.

## Vocabulaire de statut documentaire

### Temporaire

Livrable ou vue de travail utile pour une exploration, une comparaison ou une preparation redactionnelle, mais qui n'est pas destine a faire autorite dans la duree.

### Conserve

Livrable garde dans le repo ou dans un espace documentaire controle parce qu'il conserve une valeur de travail, d'audit ou de transmission.

Un livrable conserve doit avoir un statut explicite et rester tracable vers le corpus lorsqu'il contient une information documentaire.

### Document maitre

Vue redactionnelle persistante du corpus exporte, produite par le pipeline documentaire actuel.

Un document maitre n'est pas une source, n'est pas une preuve autonome et n'a pas d'autorite documentaire propre.

### Genere

Artefact produit par un script ou un pipeline reproductible.

Un artefact genere peut etre commite si le workflow du repo l'exige, mais il ne doit pas etre corrige manuellement hors procedure explicite.

### Obsolete

Vue, export ou livrable qui ne correspond plus a l'etat courant du corpus, des registres ou du script de generation dont il depend.

### Suspect

Information, passage ou livrable dont l'ancrage documentaire est insuffisant, contradictoire ou non derivable.

Un element suspect doit etre clarifie avant d'etre mobilise comme base redactionnelle stable.

### A regenerer

Artefact dont la logique documentaire reste valide mais dont le contenu doit etre reconstruit par le pipeline attendu.

Ce statut vise notamment les documents maitres ou exports dont les dependances ont evolue.

## Hors perimetre M1

M1 ne doit pas :

- creer un script de controle dans cette etape de cadrage ;
- modifier la roadmap ;
- ouvrir un chantier M2 ;
- presenter les documents maitres comme des sources ou des preuves ;
- presenter le RAG comme producteur technique des documents maitres ;
- corriger manuellement des artefacts generes.

La suite de M1 pourra transformer ce vocabulaire en controles outilles, mais seulement apres validation du perimetre documentaire.
