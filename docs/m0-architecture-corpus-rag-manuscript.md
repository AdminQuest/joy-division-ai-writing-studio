# M0 — Architecture Corpus, RAG, Manuscript et documents maitres

## Decision d'architecture

Cette note grave la decision d'architecture M0 relative au statut du corpus, du RAG, de Manuscript et des documents maitres.

```text
Corpus + RAG = infrastructure documentaire.
Manuscript = infrastructure redactionnelle.
Documents maitres = livrables RAG persistants.
```

Le corpus est le coeur documentaire du projet. Le RAG fait partie de cette infrastructure documentaire : il permet d'explorer, de filtrer, de regrouper et d'assembler les elements du corpus. Manuscript appartient a un autre plan : il sert a rediger le livre a partir de materiaux documentaires stabilises.

Les documents maitres ne constituent pas un composant autonome du systeme. Ils sont des livrables RAG persistants, organises par chapitre et conserves dans le temps. Ils peuvent etre charges dans Manuscript, mais ils ne possedent pas d'autorite documentaire propre.

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

## Role de Manuscript

Manuscript est l'infrastructure redactionnelle du projet de livre. Il sert a :

- organiser le travail d'ecriture ;
- charger des materiaux issus du corpus ou du RAG ;
- rediger, reviser et structurer les chapitres ;
- separer l'acte d'ecriture de l'autorite documentaire.

Manuscript n'est pas la source de verite documentaire. Les contenus qui y sont mobilises doivent rester rattaches au corpus lorsque leur statut documentaire importe pour le manuscrit.

## Statut des documents maitres

Les documents maitres sont des sorties stabilisees du RAG lorsqu'un livrable documentaire est agence par chapitre, conserve dans le temps et reutilise comme support de travail.

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

M1 devra renforcer les controles de fiabilite et de derivabilite autour des livrables RAG persistants.

Controles a prevoir :

- verifier la tracabilite des documents maitres vers le corpus ;
- detecter les documents maitres obsoletes ;
- verifier qu'un document maitre ne contient pas d'information non derivable du corpus ;
- qualifier les livrables RAG selon leur statut : temporaire, conserve, document maitre ;
- signaler les ecarts entre une sortie RAG persistante et les registres ou exports dont elle depend.

Ces controles relevent de la fiabilisation M1. Ils ne doivent pas etre confondus avec une campagne d'enrichissement M2 ni avec une refonte de Manuscript.
