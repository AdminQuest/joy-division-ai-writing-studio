# M0 — Audit final des criteres de sortie

Etat audite : 2026-06-05.

Ce document audite les criteres de sortie M0 definis dans `docs/roadmap-strategique-2026.md`. Il ne constitue pas un document de cloture M0 et ne decide pas la cloture du jalon.

Perimetre de cette PR :

- constater l'etat reel du depot ;
- qualifier les criteres de sortie M0 ;
- identifier les ecarts et leur caractere bloquant ou non ;
- ne corriger aucun probleme ;
- ne lancer ni M1 ni M2.

## Audit critere par critere

### 1. `STATUS.md` se regenere sans erreur via `tools/generate_status.py`, puis le snapshot regenere est committe lorsqu'il differe

| Champ | Valeur |
| --- | --- |
| Critere | `STATUS.md` se regenere sans erreur via `tools/generate_status.py`, puis le snapshot regenere est committe lorsqu'il differe. |
| Preuves concernees | `STATUS.md`, `tools/generate_status.py`, PR #110, commit `880f2756`, merge commit `4c252be9`. |
| Etat reel observe | `STATUS.md` est present, indique `Genere par : tools/generate_status.py`, et le snapshot regenere par la PR #110 est merge dans `main`. |
| Resultat | rempli sous reserve |
| Justification courte | Le critere a ete verifie dans la PR #110 et le snapshot a ete inclus. Cette PR d'audit ne relance pas le generateur, conformement a la contrainte de ne regenerer aucun artefact. |
| Manque eventuel | Aucune action technique immediate. La reserve tient seulement au fait que l'audit courant ne regenere pas `STATUS.md`. |
| Bloque la cloture M0 ? | Non. |

### 2. Les artefacts generes couverts par la sentinelle sont verifies par `check-generated-sync`

| Champ | Valeur |
| --- | --- |
| Critere | Les artefacts generes couverts par la sentinelle sont verifies par `check-generated-sync`. |
| Preuves concernees | `tools/check_generated_sync.py`, `.github/workflows/check-generated-sync.yml`, `exports/generated/`, `chapters/*/document_maitre.md`, `chapters/master_docs.json`, PR #110. |
| Etat reel observe | La PR #110 affiche le check GitHub Actions `check-generated-sync` en succes. Le workflow appelle `python tools/check_generated_sync.py`. |
| Resultat | rempli |
| Justification courte | Le dernier passage M0 merge a ete controle par la sentinelle en CI avec conclusion `SUCCESS`. |
| Manque eventuel | Aucun manque pour M0. |
| Bloque la cloture M0 ? | Non. |

### 3. `build_all.py` reste le controle global du pipeline, sans etre presente comme generateur direct de `STATUS.md`

| Champ | Valeur |
| --- | --- |
| Critere | `build_all.py` reste le controle global du pipeline registres / documents maitres / exports / audits, mais il n'est pas presente comme generateur direct de `STATUS.md` sauf appel explicite a `tools/generate_status.py`. |
| Preuves concernees | `tools/build_all.py`, `tools/generate_status.py`, `docs/m0-etat-du-socle.md`, `docs/roadmap-strategique-2026.md`. |
| Etat reel observe | `tools/build_all.py` appelle `build_registers.py`, `build_attribution_edges.py`, `build_master_docs.py`, `build_edges.py` et `audit_repo.py`. Il n'appelle pas `tools/generate_status.py`. |
| Resultat | rempli |
| Justification courte | La distinction est presente dans la roadmap et reprise dans l'inventaire M0. Le code observe confirme que `generate_status.py` est le producteur direct de `STATUS.md`. |
| Manque eventuel | Aucun. |
| Bloque la cloture M0 ? | Non. |

### 4. `check-generated-sync` est au vert sur la derniere PR

| Champ | Valeur |
| --- | --- |
| Critere | `check-generated-sync` est au vert sur la derniere PR. |
| Preuves concernees | PR #110, workflow `.github/workflows/check-generated-sync.yml`, check GitHub Actions `check-generated-sync`. |
| Etat reel observe | La derniere PR M0 mergee, #110, a un check `check-generated-sync` termine avec conclusion `SUCCESS`. |
| Resultat | rempli |
| Justification courte | Le check requis est passe sur la PR qui a ajoute l'inventaire M0 et les artefacts regenerees. |
| Manque eventuel | Le futur check de cette PR d'audit devra aussi passer avant merge, mais ce n'est pas un ecart M0 existant. |
| Bloque la cloture M0 ? | Non. |

### 5. L'inventaire des applications existantes est disponible et date

| Champ | Valeur |
| --- | --- |
| Critere | L'inventaire des applications existantes est disponible et date. |
| Preuves concernees | `docs/m0-etat-du-socle.md`, `apps/`, `tools/rag_server.py`. |
| Etat reel observe | `docs/m0-etat-du-socle.md` contient une section datee "Etat date des applications existantes" listant les apps presentes, RAG Studio, serveur RAG local et l'absence de chemin local pour `manuscript-studio`. |
| Resultat | rempli sous reserve |
| Justification courte | L'inventaire est disponible et date. La reserve tient au statut de `manuscript-studio`, cite par la roadmap mais non materialise par un chemin local verifie. |
| Manque eventuel | Si `manuscript-studio` existe hors depot, son emplacement devra etre fourni dans une decision ulterieure. |
| Bloque la cloture M0 ? | Non, car l'absence locale est explicitement constatee dans l'inventaire. |

### 6. L'inventaire des registres canoniques est disponible, avec volumetrie

| Champ | Valeur |
| --- | --- |
| Critere | L'inventaire des registres canoniques est disponible, avec volumetrie. |
| Preuves concernees | `docs/m0-etat-du-socle.md`, `STATUS.md`, `exports/generated/*.json`, `registers/`. |
| Etat reel observe | L'inventaire M0 liste sources, atomes, organisations, images, chronologie, concerts, acteurs, lieux, chansons, citations, concepts, motifs, mythes, sessions, relations, references et registres specialises, avec volumetrie lorsque disponible. |
| Resultat | rempli |
| Justification courte | Les volumes disponibles sont reportes depuis `STATUS.md` et les exports generes ; les volumes non consolides sont identifies comme tels. |
| Manque eventuel | Aucun manque bloquant. Les ecarts canon/export peuvent etre clarifies plus tard si necessaire. |
| Bloque la cloture M0 ? | Non. |

### 7. La table des dependances build / validation / publication est disponible

| Champ | Valeur |
| --- | --- |
| Critere | La table des dependances build / validation / publication est disponible. |
| Preuves concernees | `docs/m0-etat-du-socle.md`, `tools/build_all.py`, `tools/check_generated_sync.py`, `.github/workflows/check-generated-sync.yml`, `tools/rag_server.py`. |
| Etat reel observe | L'inventaire M0 contient une table dediee listant outils, chemins, types, entrees, sorties, dependances, artefacts couverts et statut M0. |
| Resultat | rempli |
| Justification courte | Les dependances centrales du build, de la validation, des audits et de la publication statique/local RAG sont cartographiees. |
| Manque eventuel | Aucun manque bloquant. Les dependances externes non locales peuvent rester a documenter hors decision M0. |
| Bloque la cloture M0 ? | Non. |

### 8. La table de rattachement initiale est renseignee

| Champ | Valeur |
| --- | --- |
| Critere | La table de rattachement initiale est renseignee. |
| Preuves concernees | `docs/m0-etat-du-socle.md`, `docs/roadmap-strategique-2026.md`. |
| Etat reel observe | L'inventaire M0 contient une table de rattachement initiale couvrant registres, sources/atomes, exports generes, documents maitres, manifest, applications, audits, scripts et workflow CI. |
| Resultat | rempli |
| Justification courte | Les groupes roadmap attendus et les pathspecs minimaux sont renseignes. |
| Manque eventuel | Aucun manque bloquant. |
| Bloque la cloture M0 ? | Non. |

### 9. Les limites connues sont distinguees des anomalies dans une liste explicite

| Champ | Valeur |
| --- | --- |
| Critere | Les limites connues sont distinguees des anomalies dans une liste explicite. |
| Preuves concernees | `docs/m0-etat-du-socle.md`, sections "Limites connues" et "Anomalies". |
| Etat reel observe | L'inventaire M0 separe explicitement limites connues, anomalies, sujets reportes et chantiers interdits. |
| Resultat | rempli |
| Justification courte | La distinction est presente et limite les corrections hors perimetre. |
| Manque eventuel | Aucun manque bloquant. |
| Bloque la cloture M0 ? | Non. |

### 10. Aucun chantier M2 n'est lance

| Champ | Valeur |
| --- | --- |
| Critere | Aucun chantier M2 n'est lance. |
| Preuves concernees | `docs/roadmap-strategique-2026.md`, `docs/m0-architecture-corpus-rag-manuscript.md`, `docs/m0-etat-du-socle.md`, historique des PR M0. |
| Etat reel observe | Les documents M0 rappellent que les formulaires d'ajout, refontes et studios d'enrichissement restent interdits ou reportes. Cette PR d'audit ne cree ni script, ni interface, ni artefact fonctionnel. |
| Resultat | rempli |
| Justification courte | M0 documente l'existant et ses dependances ; aucun developpement M2 n'est introduit par les livrables M0 audites. |
| Manque eventuel | Aucun. |
| Bloque la cloture M0 ? | Non. |

## Synthèse exécutive

| Critere | Statut | Bloquant ? |
| --- | --- | --- |
| `STATUS.md` regenere via `tools/generate_status.py` et snapshot committe si different | rempli sous reserve | Non |
| Artefacts generes verifies par `check-generated-sync` | rempli | Non |
| `build_all.py` conserve son role de controle global sans etre generateur direct de `STATUS.md` | rempli | Non |
| `check-generated-sync` au vert sur la derniere PR | rempli | Non |
| Inventaire date des applications existantes | rempli sous reserve | Non |
| Inventaire des registres canoniques avec volumetrie | rempli | Non |
| Table des dependances build / validation / publication | rempli | Non |
| Table de rattachement initiale | rempli | Non |
| Limites connues distinguees des anomalies | rempli | Non |
| Aucun chantier M2 lance | rempli | Non |

## Conditions restantes avant clôture de M0

- Faire valider humainement cette PR d'audit de sortie.
- Verifier que le check GitHub Actions de cette PR d'audit reste au vert avant merge.
- Decider explicitement si la reserve sur `manuscript-studio` est acceptable comme constat M0 ou si un emplacement externe doit etre fourni avant cloture.

## Sujets reportés hors M0

### Releve de M1

- Fiabilisation des liens inter-registres, invariants et validateurs.
- Tracabilite fine des documents maitres vers sources, atomes, registres et exports.
- Qualification documentaire des livrables RAG conserves.
- Analyse des warnings et blocs inconnus signales par les diagnostics generes.
- Clarification des ecarts de volumetrie entre canons et exports lorsque ces ecarts affectent la fiabilite documentaire.

### Releve de M2

- Formulaires d'ajout documentaire.
- Studio d'enrichissement documentaire.
- Generation automatique d'identifiants pour ajouts courants.
- Controles avant commit lies a un workflow d'ajout.
- Ameliorations d'interface visant l'ajout ou la modification des donnees.

### Releve d'une decision ulterieure

- Localisation ou statut externe de `manuscript-studio`.
- Refondre ou non les interfaces de consultation.
- Strategie Cloudflare Pages / Zero Trust.
- Integration d'un repo prive unifie.
- Politique multimedia, droits, provenance et republication.
- Documentation de cloture formelle M0, si l'audit est valide.
