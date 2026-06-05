# M0 — Architecture Corpus, RAG, Manuscript et documents maitres

## Decision d'architecture

Cette note grave la decision d'architecture M0 relative au statut du corpus, du RAG, de Manuscript et des documents maitres.

```text
Corpus + RAG = infrastructure documentaire.
Manuscript = infrastructure redactionnelle.
Documents maitres = vues redactionnelles persistantes du corpus exporte, generees par le pipeline documentaire.
```

Le corpus est le coeur documentaire du projet. Le RAG fait partie de cette infrastructure documentaire : il permet d'explorer, de filtrer, de regrouper et d'assembler les elements du corpus. Manuscript appartient a un autre plan : il sert a rediger le livre a partir de materiaux documentaires stabilises.

Les documents maitres ne constituent pas un composant autonome du systeme. Dans l'etat actuel du repo, ils sont produits par le pipeline documentaire, notamment `tools/build_master_docs.py`, a partir des exports, atomes et registres du corpus. Ils peuvent etre charges dans Manuscript, mais ils ne possedent pas d'autorite documentaire propre.

## Ce qui appartient au corpus

Le corpus regroupe les objets documentaires primaires, normalises ou derives qui permettent de documenter le projet :

- sources ;
- atomes ;
- citations ;
- registres canoniques ;
- chronologie ;
- concepts ;
- motifs ;
- mythes ;
- chansons ;
- concerts ;
- lieux ;
- personnes ;
- organisations ;
- images ;
- sessions ;
- relations inter-registres ;
- schemas ;
- exports generes ;
- contextes et index utilises par le RAG lorsqu'ils sont derivables du corpus.

Les objets generes ou indexes ne remplacent pas les sources et les registres. Ils rendent le corpus exploitable par les outils, les audits et les interfaces.

## Role du RAG

Le RAG est l'outil d'exploration du corpus. Il sert a :

- interroger les sources atomisees et les registres ;
- filtrer les donnees par source, concept, motif, mythe, chapitre ou entite ;
- regrouper des elements disperses ;
- assembler des dossiers documentaires ;
- produire des livrables exploitables par le travail redactionnel.

Le RAG n'est pas un outil de redaction. Il ne remplace ni l'analyse historiographique, ni l'ecriture du livre, ni la responsabilite editoriale. Il produit des regroupements, des extractions et des assemblages documentaires dont la valeur depend de leur tracabilite vers le corpus.

Les livrables RAG peuvent etre charges directement dans Manuscript ou inspirer des dossiers par chapitre. Ils ne sont toutefois pas, dans l'architecture actuelle, le producteur technique des documents maitres : ce role revient au pipeline documentaire et aux scripts de generation.

## Role de Manuscript

Manuscript est l'infrastructure redactionnelle du projet de livre. Il sert a :

- organiser le travail d'ecriture ;
- charger des materiaux issus du corpus ou du RAG ;
- rediger, reviser et structurer les chapitres ;
- separer l'acte d'ecriture de l'autorite documentaire.

Manuscript n'est pas la source de verite documentaire. Les contenus qui y sont mobilises doivent rester rattaches au corpus lorsque leur statut documentaire importe pour le manuscrit.

## Statut des documents maitres

Les documents maitres sont des vues redactionnelles persistantes du corpus exporte. Ils sont generes par le pipeline documentaire a partir des entrees structurees du corpus, en particulier les atomes, registres et exports. Le script `tools/build_master_docs.py` est le producteur technique actuel de ces documents.

Un livrable RAG peut preparer, inspirer ou completer un dossier de chapitre, mais il ne devient pas automatiquement document maitre. Pour etre traite comme document maitre, un livrable doit etre integre dans le flux de generation documentaire ou rester explicitement derivable des memes entrees de corpus.

Un document maitre :

- n'est pas une source ;
- n'est pas un registre ;
- n'est pas une preuve autonome ;
- n'a pas d'autorite documentaire propre ;
- doit rester tracable vers le corpus structure ;
- doit rester derivable du corpus ;
- peut etre charge dans Manuscript comme materiau de redaction.

Lorsqu'un document maitre contient une information qui ne peut pas etre reliee a une source, un atome, une citation, un registre ou un export derive du corpus, cette information doit etre consideree comme suspecte jusqu'a clarification.

## Consequences pour M0

M0 doit stabiliser la cartographie entre corpus, RAG, Manuscript et documents maitres.

Implications :

- stabiliser la cartographie corpus / RAG / Manuscript ;
- distinguer les objets persistants des vues generees ;
- eviter de traiter les documents maitres comme un composant strategique autonome ;
- documenter les flux existants avant toute refonte ;
- conserver la separation entre infrastructure documentaire et infrastructure redactionnelle.

Cette decision ne lance pas de chantier M2, ne cree pas de nouvelle application et ne modifie pas l'architecture technique existante.

## Consequences pour M1

M1 devra renforcer les controles de fiabilite et de derivabilite autour des documents maitres comme vues persistantes du corpus exporte. Ces controles doivent viser les entrees du pipeline documentaire, les exports de corpus et les scripts de generation, plutot qu'un etat interne du RAG.

Controles a prevoir :

- verifier la tracabilite des documents maitres vers le corpus ;
- detecter les documents maitres obsoletes ;
- verifier qu'un document maitre ne contient pas d'information non derivable du corpus ;
- qualifier les livrables RAG selon leur statut : temporaire, conserve, document maitre ;
- signaler les ecarts entre un document maitre, les exports dont il depend et le script qui le produit ;
- verifier que `tools/build_master_docs.py` et les autres generateurs documentaires restent coherents avec les registres, atomes et exports utilises.

Ces controles relevent de la fiabilisation M1. Ils ne doivent pas etre confondus avec une campagne d'enrichissement M2 ni avec une refonte de Manuscript.
