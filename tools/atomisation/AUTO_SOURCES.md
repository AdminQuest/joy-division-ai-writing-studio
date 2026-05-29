# Atomisation automatique des sources — `Registre_sources/`

Ce document décrit le mécanisme semi-automatique d'atomisation des PDF déposés
dans le dossier Google Drive `Registre_sources/`, via l'orchestrateur
`tools/atomize_new_sources.py`.

> **Principe directeur.** L'orchestrateur ne fait **pas** l'atomisation : il gère
> la *tuyauterie* (détection, branche Git, PR, archivage du PDF). L'atomisation
> elle-même — lecture du PDF, production des atomes, citations, relations,
> registres — reste une tâche **cognitive** réalisée par un agent Claude (ou par
> Fabrice) en suivant le workflow de référence
> `joy-division-studio-private:prompts/atomisation_workflow.md`.

---

## 1. Déposer un PDF source

Sur le Drive, le dossier `Registre_sources/` est organisé **par source**, un
sous-dossier par identifiant canonique :

```
Registre_sources/
├── S89_Savage_Englands_Dreaming/        → <le PDF>
├── S90_Fisher_Ghosts_of_My_Life_2014/   → <le PDF>
├── …
└── atomized/                            ← PDF archivés après fusion de la PR
```

Pour une **nouvelle source** :

1. Créer le sous-dossier `SXX_Auteur_TitreAbrege/` et y déposer le PDF.
2. Déclarer la source dans `data/registre.json` (repo public) avec un `statut`
   contenant la mention **« atomisation à démarrer »**. C'est ce marqueur qui
   rend la source détectable.

> Le `SXX` est l'identifiant canonique. Vérifier le prochain numéro libre dans
> `data/registre.json` (cf. `docs/ATOMISATION_SOURCE.md`).

---

## 2. Déclencher l'atomisation

Le mécanisme est **semi-automatique** et **en deux temps** : un humain valide à
chaque frontière (validation niveau 2 = branche + PR). Aucun démon permanent.

### Étape A — Détecter

```bash
python3 tools/atomize_new_sources.py --detect
```

Liste les sources dont le `statut` annonce « atomisation à démarrer » et qui ne
possèdent encore aucun atome dans `sources/`.

### Étape B — Préparer (branche + consigne)

```bash
python3 tools/atomize_new_sources.py --prepare S90
```

- Met à jour `main`, crée la branche `claude/atomize-{YYYY-MM-DD}-{slug}`.
- Localise le PDF (montage Drive local, ou indication MCP en mode cloud).
- **Affiche la consigne d'atomisation** destinée à l'agent (périmètre public,
  surcharges du workflow, rappels qualité).

> L'orchestrateur **n'invoque pas** l'agent. Le mode « tout-en-un » n'existe pas
> volontairement (trop ambitieux pour cette première version).

### Étape C — Atomiser (agent ou Fabrice)

L'agent Claude (en interactif) ou Fabrice exécute la passe d'atomisation en
suivant `prompts/atomisation_workflow.md`, **avec deux surcharges** :

- **Périmètre PUBLIC uniquement** : on écrit seulement dans le repo public
  (`sources/`, `registers/`, `rag/`, `data/`, `reports/`, `apps/`). Le volet privé
  (`chapters/`, `songs/` du repo `joy-division-studio-private`) reste **manuel**
  pour cette passe, afin qu'aucune parole ni note privée ne fuite dans une PR
  publique.
- **Pas de commit sur `main`** : on reste sur la branche de travail ; le commit,
  le push et la PR sont gérés par l'étape D.

### Étape D — Commiter et ouvrir la PR

```bash
python3 tools/atomize_new_sources.py --commit-and-pr S90
```

- Lance `python3 tools/build_registers.py --strict` puis
  `python3 tools/audit_repo.py --fail-on-error`.
- `git add` du **matériel public uniquement**, commit
  (`feat(SXX): atomisation — …`), push de la branche.
- Ouvre une **PR publique** vers `main` (via `gh` si disponible, sinon affiche les
  éléments à créer manuellement / via le MCP GitHub).

### Étape E — Finaliser (après fusion)

À lancer **manuellement après la fusion de la PR** (pas de webhook ni d'action
GitHub pour l'instant) :

```bash
python3 tools/atomize_new_sources.py --finalize S90
```

Déplace le PDF vers `Registre_sources/atomized/{YYYY-MM-DD}-{nom-original}.pdf`.
En mode cloud (sans montage Drive local), l'orchestrateur affiche l'opération
équivalente à réaliser via le MCP Google Drive.

---

## 3. Déclenchement depuis Android (Remote Control)

Depuis le téléphone, via Claude Code on the web / Remote Control, une requête en
langage naturel suffit, par exemple :

> « Atomise les nouveaux PDF de Registre_sources »

L'agent doit alors :

1. `--detect` pour lister les sources en attente ;
2. pour **chaque** source en attente, dérouler `--prepare SXX`, faire la passe
   d'atomisation (périmètre public), puis `--commit-and-pr SXX` ;
3. **une branche et une PR par source** (atomicité de validation) ;
4. s'arrêter là : `--finalize` n'est lancé qu'après validation et fusion par
   Fabrice.

En mode cloud, l'agent lit les PDF via le **MCP Google Drive** (le dossier
`Registre_sources/` a l'ID `1sm5L4X045TM0hESmAYuoT9EJpiHh13cF`) ; aucun accès au
Mac n'est nécessaire.

---

## 4. Workflow de validation des PR

- Une PR **publique** par source, vers `main` de `joy-division-ai-writing-studio`.
- **Aucune fusion automatique** : Fabrice relit puis fusionne manuellement.
- Points de contrôle lors de la relecture :
  - atomes v2 sélectifs et reliés (relations, concepts) ;
  - `data/registre.json` mis à jour (statut de la source) ;
  - **aucune parole complète** ni contenu privé dans la PR ;
  - `build_registers --strict` et `audit_repo` passés au vert.
- Après fusion : lancer `--finalize SXX` pour archiver le PDF.

---

## 5. Résolution du chemin Google Drive (jamais hardcodé)

L'orchestrateur résout le chemin local de `Registre_sources/` dans cet ordre :

1. option `--registre-path PATH` ;
2. variable d'environnement `REGISTRE_SOURCES_PATH` ;
3. `tools/atomisation/config.json` (clé `registre_sources_path`) ;
4. auto-détection sous `~/Library/CloudStorage/GoogleDrive-*/**/Registre_sources`
   (Google Drive Desktop sur Mac).

Si aucun montage local n'est trouvé (cas d'un agent cloud), l'orchestrateur passe
en **mode MCP** : il n'effectue pas d'opération de fichier mais affiche
l'opération Drive à réaliser via le MCP Google Drive.

Exemple de configuration locale (`tools/atomisation/config.json`) :

```json
{
  "registre_sources_path": "~/Library/CloudStorage/GoogleDrive-fabrice.ribet@gmail.com/Mon Drive/6 - Musique/1 - Joy Division/5 - Projet de livre/Registre_sources"
}
```

---

## 6. Mode `--watch` (différé — pas dans cette version)

Un mode `--watch` (surveillance continue du dossier `Registre_sources/` avec
déclenchement automatique de `--prepare` à chaque nouveau PDF) est **envisagé mais
non implémenté**. Il n'est volontairement pas inclus ici :

- il suppose un processus permanent (démon), contraire au choix semi-automatique ;
- il devra réutiliser tel quel `--detect` / `--prepare` / `--commit-and-pr`, sans
  jamais court-circuiter la validation humaine par PR.

À spécifier dans une itération ultérieure.

---

## 6 bis. Garde-fous et robustesse

L'orchestrateur est conçu pour échouer **proprement** plutôt que de produire un
état douteux :

- **Périmètre public garanti par liste blanche.** `--commit-and-pr` ne `git add`
  que `data/registre.json sources/ registers/ rag/ reports/ apps/` +
  `exports/generated`. Aucun chemin `chapters/` ou `songs/` n'est jamais stagé
  (c'est une liste blanche, pas une liste noire).
- **Gate de complétude.** `--commit-and-pr` exige au moins un atome réel
  (`SXX-Axxx`) dans `sources/`. Une passe partielle (par ex. `source.md` créé mais
  aucun atome) est **refusée proprement** (exit 1), sans commit.
- **Validation non destructive.** Si `build_registers --strict` ou
  `audit_repo --fail-on-error` échoue, le script s'arrête avec un message clair
  (pas de traceback) **avant** tout `git commit`/`push`. La complétude éditoriale
  fine reste vérifiée par le relecteur de la PR.
- **Idempotence de `--prepare`.** Si la branche de travail existe déjà, le script
  **échoue proprement sans rien écraser** et indique quoi faire. Pour reprendre le
  travail sur cette branche, ajouter `--reuse-branch` (`git checkout` de
  l'existante, sans recréation).

---

## 6 ter. Limitations connues — différences Mac / cloud

Le comportement de `--finalize` (archivage du PDF) **dépend de l'environnement
d'exécution**, car les deux modes n'ont pas les mêmes capacités sur Google Drive.

### Exécution sur Mac (Drive monté localement)

Avec Google Drive Desktop, `Registre_sources/` est un dossier de fichiers
locaux. `--finalize SXX` effectue alors un **vrai déplacement** (`shutil.move`) :

- copie du PDF vers `Registre_sources/atomized/{YYYY-MM-DD}-{nom-original}.pdf` ;
- **suppression de l'original** dans `Registre_sources/SXX_.../`.

Le dossier racine ne conserve donc que les PDF en attente, comme prévu.

### Exécution en cloud (Remote Control depuis Android, sans montage local)

Sans montage Drive local, `--finalize` passe en **mode MCP** et s'appuie sur les
outils du MCP Google Drive. **À ce jour, ce MCP ne fournit ni outil de
suppression ni outil de déplacement (`update parents`)** : seulement `copy_file`
et `create_file`.

Conséquence : l'archivage en cloud est une **COPIE**, pas un déplacement.
L'agent :

1. crée si besoin le sous-dossier `Registre_sources/atomized/` ;
2. **copie** le PDF vers `atomized/{YYYY-MM-DD}-{source}.pdf` ;
3. **ne peut pas supprimer l'original** : l'utilisateur doit **supprimer
   manuellement** le PDF d'origine côté Drive (interface web ou Finder), après
   avoir vérifié que la copie archivée est correcte (nom et taille identiques).

### ⚠️ Ne pas mélanger les deux modes pour une même source

Si une copie a déjà été faite en **cloud**, **ne pas relancer `--finalize` sur le
Mac** pour la même source : le mode Mac déplacerait l'original sous un nom basé
sur le nom de fichier d'origine (`{date}-{nom-original}.pdf`), distinct du nom
généré en cloud (`{date}-{source}.pdf`) — ce qui produirait un **doublon** dans
`atomized/`.

**Règle : choisir un seul mode de finalisation par source.**

- Source finalisée en cloud → terminer en supprimant l'original à la main.
- Source finalisée sur Mac → laisser le script faire le déplacement complet, ne
  rien finaliser en cloud.

---

## 7. Aide-mémoire des commandes

| But | Commande |
|---|---|
| Lister les sources en attente | `python3 tools/atomize_new_sources.py --detect` |
| Préparer une source | `python3 tools/atomize_new_sources.py --prepare SXX` |
| Préparer tout le lot (souvent en dry-run) | `python3 tools/atomize_new_sources.py --prepare --all --dry-run` |
| Reprendre une branche de travail existante | `python3 tools/atomize_new_sources.py --prepare SXX --reuse-branch` |
| Commiter + PR | `python3 tools/atomize_new_sources.py --commit-and-pr SXX` |
| Archiver le PDF (après fusion) | `python3 tools/atomize_new_sources.py --finalize SXX` |
| Simulation (aucune écriture) | ajouter `--dry-run` à n'importe quelle commande |
