# Décision de clôture M0

M0 avait pour objectif de stabiliser le socle existant du projet : rendre lisibles le corpus, les applications, les registres, les exports, les audits, le RAG Studio, les documents maitres et les dependances de build / validation / publication.

Son perimetre couvrait l'existant. Il ne portait ni sur une refonte d'interface, ni sur un studio d'enrichissement, ni sur une correction des reserves documentaires identifiees.

Les livrables M0 realises sont :

- `docs/m0-architecture-corpus-rag-manuscript.md` ;
- `docs/m0-etat-du-socle.md` ;
- `docs/m0-audit-sortie.md`.

Ces livrables documentent l'architecture conceptuelle, l'etat date du socle, les dependances principales et l'audit final des criteres de sortie.

# Décisions stabilisées

Les decisions suivantes sont desormais acquises pour le socle M0 :

- Corpus = socle documentaire ;
- RAG = outil d'exploration du corpus ;
- Manuscript = outil redactionnel ;
- documents maitres = vues redactionnelles persistantes du corpus exporte ;
- `tools/build_master_docs.py` = producteur technique actuel des documents maitres ;
- les objets persistants sont distingues des vues generees ;
- la cartographie du socle est disponible ;
- la cartographie des dependances build / validation / publication est disponible ;
- l'inventaire des composants existants est disponible.

# Critères de sortie

L'audit final `docs/m0-audit-sortie.md` conclut qu'aucun critere de sortie M0 ne bloque la cloture.

Les criteres remplis couvrent notamment :

- le maintien de `tools/build_all.py` comme controle global du pipeline, sans confusion avec le generateur direct de `STATUS.md` ;
- l'inventaire des registres canoniques avec volumetrie ;
- la table des dependances build / validation / publication ;
- la table de rattachement initiale ;
- la distinction entre limites connues et anomalies ;
- l'absence de chantier M2 lance.

Les criteres remplis sous reserve ou non verifiables portent sur :

- `STATUS.md`, dont le snapshot regenere est present mais non regenere dans l'audit de sortie ;
- les artefacts couverts par `check-generated-sync`, dont le mecanisme est present dans le depot ;
- le statut du check GitHub Actions, dont la verification depend de la PR courante et non d'un artefact versionne ;
- l'inventaire des applications, avec une reserve explicite sur `manuscript-studio`.

Ces reserves ont ete qualifiees comme non bloquantes dans l'audit.

# Réserves acceptées

Les reserves suivantes sont acceptees comme non bloquantes pour la cloture de M0 :

- absence de chemin local verifie pour `manuscript-studio` ;
- verification CI dependante de GitHub Actions et non d'un artefact versionne dans le depot ;
- `STATUS.md` non regenere dans l'audit de sortie lui-meme, conformement a son perimetre sans regeneration ;
- ecarts de volumetrie entre certains canons et exports, deja constates comme limites documentaires ;
- warnings et blocs inconnus existants dans les diagnostics generes, reportes hors cloture M0 ;
- limites de cache ou de publication GitHub Pages, constatees sans correction dans M0.

Ces reserves ne bloquent pas la cloture de M0. Elles restent documentees pour traitement ou decision dans les jalons appropries.

# Sujets reportés

## Reporté à M1

- Fiabilisation des liens inter-registres, invariants et validateurs.
- Tracabilite fine des documents maitres vers sources, atomes, registres et exports.
- Qualification documentaire des livrables RAG conserves.
- Analyse des warnings et blocs inconnus signales par les diagnostics generes.
- Clarification des ecarts de volumetrie entre canons et exports lorsque ces ecarts affectent la fiabilite documentaire.

## Reporté à M2

- Formulaires d'ajout documentaire.
- Studio d'enrichissement documentaire.
- Generation automatique d'identifiants pour ajouts courants.
- Controles avant commit lies a un workflow d'ajout.
- Ameliorations d'interface visant l'ajout ou la modification des donnees.

## Décisions ultérieures

- Localisation ou statut externe de `manuscript-studio`.
- Refondre ou non les interfaces de consultation.
- Strategie Cloudflare Pages / Zero Trust.
- Integration d'un repo prive unifie.
- Politique multimedia, droits, provenance et republication.

# Décision

M0 est considéré comme clôturé à compter de cette PR.

Les futurs travaux relèvent désormais de M1 ou des jalons ultérieurs.
