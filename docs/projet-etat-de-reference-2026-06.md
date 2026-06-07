# État de référence du projet

État de référence : juin 2026.

> **Mise à jour 2026-06-07.** Ce document est un repère de continuité daté. Depuis
> sa rédaction, **M0 (2026-06-05), M1 (2026-06-06) et M2 (2026-06-06) sont
> clôturés** et **M3 est lancé (2026-06-07)**. Les sections décrivant M1 comme
> non ouvert et listant M2, l'industrialisation documentaire ou le repo privé
> unifié parmi les « sujets reportés » reflètent l'état antérieur. La référence
> à jour est `docs/roadmap-strategique-2026.md` (objectif n°1 de M3 : dépôt
> unique privé derrière Cloudflare Zero Trust).

Le projet est aujourd'hui un atelier documentaire et rédactionnel consacré au livre Joy Division. Il rassemble un corpus structuré, des registres canoniques, des exports générés, des documents maîtres, des applications de consultation, un RAG d'exploration et des workflows de contrôle.

Le projet n'est pas un simple dépôt de notes, ni une application unique, ni un studio d'enrichissement automatisé. Il n'est pas encore une architecture finale unifiée, ni une chaîne de publication définitive. Les évolutions futures doivent respecter les décisions stabilisées avant d'ajouter de nouvelles surfaces.

# Grille de lecture fonctionnelle — modèle d'organisation du hub M3

> **Adoptée le 2026-06-07** comme modèle d'organisation du futur dépôt unique
> privé (hub), par fonction et non par technologie. Cadre d'organisation, **non
> figé** comme architecture technique définitive. Elle ne remplace pas la
> doctrine documentaire stabilisée (Corpus / RAG / Manuscript / documents
> maîtres), qui reste valable au sein de l'Entrepôt et de l'Atelier. Rien ne
> reste public : tout le hub est privé derrière Cloudflare Zero Trust.

```text
Collection
↓
Usine
↓
Entrepôt
↓
Atelier
↓
Vigie
```

## Collection

| Champ | Valeur |
| --- | --- |
| Statut | Nom de travail possible, non décisionnel. |
| Rattachement M0 | Fonds personnel ou matériaux externes potentiels, distincts du Corpus tant qu'ils ne sont pas intégrés documentairement. |
| Fonction envisagée | Rassembler ce qui pourrait devenir matière documentaire après qualification. |
| Périmètre possible | Documents personnels, médias, archives, notes ou références encore hors corpus structuré. |
| Objets principaux | Matériaux à qualifier avant intégration éventuelle : sources potentielles, médias, références, traces de collecte. |
| Limites | La Collection n'est pas le Corpus et ne possède pas d'autorité documentaire tant qu'elle n'est pas structurée, sourcée et intégrée. |

## Usine

| Champ | Valeur |
| --- | --- |
| Statut | Nom de travail possible, non décisionnel. |
| Rattachement M0 | Espace possible pour l'enrichissement documentaire industrialisé, explicitement reporté hors M0. |
| Fonction envisagée | Préparer de futurs flux d'ajout, transformation ou contrôle avant intégration au corpus. |
| Périmètre possible | Formulaires d'ajout, génération d'identifiants, contrôles avant commit, automatisations futures. |
| Objets principaux | Brouillons d'ajout, propositions structurées, validations préalables, PR automatisables. |
| Limites | L'Usine ne doit pas être ouverte en M0 ; elle relève de M2 ou d'une décision ultérieure selon le périmètre exact. |

## Entrepôt

| Champ | Valeur |
| --- | --- |
| Statut | Nom de travail possible, non décisionnel. |
| Rattachement M0 | Espace Corpus + registres + RAG, c'est-à-dire le socle documentaire et ses vues d'exploration. |
| Fonction envisagée | Conserver et exposer les objets structurés et les vues exploitables du corpus. |
| Périmètre possible | `sources/`, `registers/`, `exports/generated/`, RAG Studio, documents de navigation. |
| Objets principaux | Sources, atomes, registres, exports générés, index, fragments RAG, diagnostics et audits. |
| Limites | L'Entrepôt n'est pas une nouvelle architecture décidée ; il ne remplace pas la distinction Corpus / RAG / documents maîtres. |

## Atelier

| Champ | Valeur |
| --- | --- |
| Statut | Nom de travail possible, non décisionnel. |
| Rattachement M0 | Espace de production du manuscrit, incluant documents maîtres, exports RAG, Forge et usages Manuscript. |
| Fonction envisagée | Préparer et produire la rédaction à partir de matériaux documentaires stabilisés. |
| Périmètre possible | Documents maîtres, dossiers de chapitre, prompts, notes rédactionnelles, synthèses et livrables de rédaction. |
| Objets principaux | Manuscrit, plans, scènes, chapitres, matériaux de rédaction, vues dérivées du corpus. |
| Limites | L'Atelier ne remplace pas le Corpus et ne devient pas source de vérité documentaire. |

## Vigie

| Champ | Valeur |
| --- | --- |
| Statut | Nom de travail possible, non décisionnel. |
| Rattachement M0 | Pilotage, audits, qualité, roadmap et décisions de passage de jalon. |
| Fonction envisagée | Observer la cohérence du projet, documenter les écarts et préparer les décisions humaines. |
| Périmètre possible | Audits, validations, checks CI, roadmap, documents de statut, revues humaines. |
| Objets principaux | `STATUS.md`, audits, diagnostics, critères de sortie, décisions de clôture ou de report. |
| Limites | La Vigie n'est pas un mécanisme automatique de décision ; elle fournit des preuves et signale des réserves. |

# Doctrine documentaire stabilisée

- Corpus = socle documentaire.
- RAG = outil d'exploration du corpus.
- Documents maîtres = vues rédactionnelles persistantes du corpus exporté.
- `tools/build_master_docs.py` = producteur technique actuel des documents maîtres.
- Manuscript = outil rédactionnel.
- Documentation et rédaction restent séparées.

# Décisions majeures acquises

- Corpus = socle documentaire.
- RAG = outil d'exploration du corpus.
- Manuscript = outil rédactionnel.
- Documents maîtres = vues rédactionnelles persistantes du corpus exporté.
- `tools/build_master_docs.py` = producteur technique actuel des documents maîtres.

# M0

| Champ | Valeur |
| --- | --- |
| Objectif | Stabiliser le socle existant et rendre lisible l'état réel du projet. |
| Livrables | `docs/m0-architecture-corpus-rag-manuscript.md`, `docs/m0-etat-du-socle.md`, `docs/m0-audit-sortie.md`, `docs/m0-cloture.md`. |
| Résultat | Doctrine, inventaire, dépendances, critères de sortie et réserves non bloquantes documentés. |
| Date de clôture | 2026-06-05, à compter de la PR de clôture M0. |

# M1

M1 a pour objectif général de fiabiliser le corpus documentaire sans ouvrir de studio d'enrichissement. Son périmètre attendu porte sur les contrôles, la traçabilité, les invariants, les validateurs, les écarts documentaires et la cohérence entre registres, exports, documents maîtres et sources.

Les sujets déjà identifiés sont :

- fiabilisation des liens inter-registres, invariants et validateurs ;
- traçabilité fine des documents maîtres vers sources, atomes, registres et exports ;
- qualification documentaire des livrables RAG conservés ;
- analyse des warnings et blocs inconnus signalés par les diagnostics générés ;
- clarification des écarts de volumétrie entre canons et exports lorsque ces écarts affectent la fiabilité documentaire.

Ce document ne détaille pas les travaux M1 et ne les ouvre pas.

# Sujets explicitement reportés

- Cloudflare.
- Architecture finale unifiée.
- `manuscript-studio`.
- Génération dynamique éventuelle des documents maîtres.
- Formulaires d'ajout documentaire.
- Studio d'enrichissement documentaire.
- Génération automatique d'identifiants pour ajouts courants.
- Contrôles avant commit liés à un workflow d'ajout.
- Améliorations d'interface visant l'ajout ou la modification des données.
- Refondre ou non les interfaces de consultation.
- Intégration d'un repo privé unifié.
- Industrialisation documentaire et autonomisation du studio privé : sas normalisé d'entrée des sources, canonisation assistée, atomisation reproductible, preuve automatique de propagation, suppression progressive des dépendances runtime du repo privé vers le repo public, synchronisation locale des exports, registres et documents maîtres, et refonte des interfaces privées pour lecture locale maîtrisée.
- Politique multimédia, droits, provenance et republication.

# Invariants du projet

- Le corpus est la source de vérité.
- Les documents maîtres ne sont pas des sources.
- Le RAG n'est pas le producteur technique des documents maîtres.
- Les documents maîtres sont générés actuellement par `tools/build_master_docs.py`.
- Les artefacts générés ne sont jamais corrigés manuellement.
- `STATUS.md` est généré par `tools/generate_status.py`.
- `tools/build_all.py` ne doit pas être présenté comme générateur direct de `STATUS.md` sauf changement explicite du code.
- Les réserves acceptées à la clôture M0 ne doivent pas être transformées rétroactivement en blocages M0.
- M2 ne doit pas être ouvert avant décision explicite.
- Les décisions d'architecture doivent être documentées avant toute refonte.
- Les applications privées ne doivent pas devenir durablement de simples lecteurs runtime du repo public ; toute dépendance inter-repos doit être cartographiée puis remplacée par une synchronisation maîtrisée lorsque M3 sera activé.
- À partir de M3, aucune source nouvelle ne doit entrer dans le corpus sans sas documentaire normalisé, canonisation outillée et preuve de propagation jusqu'aux exports, registres, documents maîtres et interfaces concernées.

# Utilisation du document

Ce document sert :

- à reprendre le projet après interruption ;
- à accueillir un nouvel agent ;
- à préparer les futures évolutions ;
- à éviter de rouvrir les décisions M0 déjà stabilisées ;
- à distinguer les décisions acquises, les sujets reportés et les futurs jalons.

Il doit être lu comme un repère de continuité stratégique, pas comme une roadmap et pas comme une demande d'exécution.
