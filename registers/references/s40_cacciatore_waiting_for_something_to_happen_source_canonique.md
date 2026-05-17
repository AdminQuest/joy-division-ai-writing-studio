# S40 — Source canonique — Cacciatore, « ...waiting for something to happen... », 2021

## 1. Identifiant canonique

```text
S40
```

## 2. Libelle source

```text
S40 — Cacciatore, ...waiting for something to happen..., 2021
```

## 3. Dossier source

```text
sources/cacciatore_waiting_for_something_to_happen/
```

## 4. Reference complete

CACCIATORE, Fortunato M., « ...waiting for something to happen... », dans Alfonso Amendola et Linda Barone (dir.), *Our Vision Touched the Sky: Fenomenologia dei Joy Division*, Roma, Rogas Edizioni, 2021, pagination a verrouiller sur l'exemplaire de travail.

## 5. Entree a ajouter dans `data/registre.json`

```json
{
  "id": "S40",
  "source_label": "S40 — Cacciatore, ...waiting for something to happen..., 2021",
  "source_short_title": "Cacciatore, ...waiting for something to happen..., 2021",
  "auteur": "Fortunato M. Cacciatore",
  "titre": "...waiting for something to happen...",
  "annee": "2021",
  "reference_complete": "CACCIATORE, Fortunato M., « ...waiting for something to happen... », dans Alfonso Amendola et Linda Barone (dir.), Our Vision Touched the Sky: Fenomenologia dei Joy Division, Roma, Rogas Edizioni, 2021, pagination a verrouiller sur l'exemplaire de travail.",
  "nature": "article de volume collectif / essai philosophico-esthetique",
  "statut": "verifie ; source canonique corrigee ; fichier Drive identifie ; pagination a verrouiller",
  "fiabilite": "forte comme source secondaire critique ; prudence requise pour les citations et la pagination",
  "usage": [
    "attente",
    "waiting for something to happen",
    "hauntologie",
    "spectres",
    "futur perdu",
    "no future",
    "nostalgie du futur",
    "modernite tardive",
    "critique musicale",
    "historicisme imaginatif",
    "Mark Fisher",
    "Derrida",
    "Bifo Berardi",
    "post-punk",
    "Joy Division comme seuil temporel"
  ],
  "chapitres": [
    "Chapitre 11",
    "Chapitre 14"
  ],
  "chapitres_secondaires": [
    "Chapitre 1",
    "Chapitre 3",
    "Chapitre 13"
  ],
  "source_origin": [
    "Google Drive",
    "PDF integral",
    "volume collectif",
    "registre canonique"
  ],
  "dossier_source": "sources/cacciatore_waiting_for_something_to_happen/",
  "fichier_source": "S40_cacciatore_waiting_for_something_to_happen_2021.pdf",
  "fichier_source_original": "Alfonso Amendola e Linda Barone - Our vision touched the sky.pdf",
  "source_drive": "https://drive.google.com/file/d/1qyK58ESFhF_yLIULGXV6uIu4lxS2ZNF-/view?usp=drive_link",
  "volume_contenant": "Alfonso Amendola et Linda Barone (dir.), Our Vision Touched the Sky: Fenomenologia dei Joy Division, Roma, Rogas Edizioni, 2021",
  "lieu_edition": "Roma",
  "editeur": "Rogas Edizioni",
  "niveau_preuve": "source secondaire critique / article philosophico-esthetique",
  "arbitrage": "S40 ne reference que l'article de Fortunato M. Cacciatore, « ...waiting for something to happen... ». Le volume collectif complet n'est que le contenant bibliographique. L'ancienne entree S40 doit etre resserree autour de cet article.",
  "prudence": "Ne pas confondre S40 avec le volume complet dirige par Amendola et Barone. Ne pas confondre S40 avec S13, qui concerne l'article de Caterina Tomeo dans le meme volume. Verrouiller la pagination avant toute citation directe. Distinguer les references philosophiques mobilisees par Cacciatore des faits historiques sur Joy Division."
}
```

## 6. Risques de confusion

1. Ne pas faire de S40 la reference du volume collectif complet.
2. Ne pas attribuer a Fortunato M. Cacciatore les theses des autres contributeurs du volume.
3. Ne pas confondre S40 avec S13, consacre a Caterina Tomeo et a l'articulation Joy Division / rave era.
4. Ne pas maintenir l'ancienne reference « Waiting for Something to Happen, 2019, Milan, Mimesis » si elle ne correspond pas a l'exemplaire Drive fourni.
5. Ne pas citer directement Cacciatore sans verification de la pagination exacte.
6. Ne pas convertir l'hauntologie en preuve historique directe sur Joy Division.
7. Ne pas reduire l'article a la seule formule « nostalgie du futur » : l'article travaille plus largement l'attente, les spectres, le no future, Derrida, Fisher, Bifo et l'apres-coup critique.

## 7. Consignes pour les futurs atomes

Les futurs atomes S40 doivent rester philosophiques, conceptuels et prudents. Ils doivent documenter les relations entre Joy Division, temporalite, spectres, attente et futurs perdus, sans transformer Cacciatore en source factuelle principale.

Atomes prioritaires recommandes :

```text
S40-A001 — S40 comme article philosophico-esthetique, non source primaire
S40-A002 — « ...waiting for something to happen... » : l'attente comme structure temporelle
S40-A003 — Hauntologie : Derrida, Fisher et les futurs perdus
S40-A004 — No future et fin du futur : articulation Bifo / punk / post-punk
S40-A005 — Joy Division comme seuil spectral entre histoire vecue et reception posthume
S40-A006 — Critique de l'historicisme imaginatif et prudence methodologique
S40-A007 — La formule du futur perdu comme outil de reception, non comme preuve historique
```

Bloc d'usage recommande :

```yaml
source_id: S40
source_label: "S40 — Cacciatore, ...waiting for something to happen..., 2021"
article_author: "Fortunato M. Cacciatore"
article_title: "...waiting for something to happen..."
volume: "Our Vision Touched the Sky: Fenomenologia dei Joy Division"
preuve: "source secondaire critique / article philosophico-esthetique"
usage: "attente, hauntologie, no future, futur perdu, spectres, reception posthume"
prudence: "ne pas utiliser comme source factuelle principale ; verifier la pagination avant citation ; distinguer l'article du volume collectif"
```

Formules utilisables :

```text
attente sans horizon stable
futur perdu
condition spectrale de la reception
hauntologie du post-punk
Joy Division comme seuil temporel
no future sans messianisme
```

Formules a proscrire :

```text
Cacciatore prouve que Joy Division n'avait pas de futur
le volume S40 explique Joy Division
Amendola et Barone disent que...
Joy Division est une preuve de l'hauntologie
Curtis annonce Fisher ou Derrida
```

## 8. Fichiers operationnels

```text
sources/cacciatore_waiting_for_something_to_happen/source.md
sources/cacciatore_waiting_for_something_to_happen/registre_patch_s40.json
tools/apply_s40_registre_patch.py
```
