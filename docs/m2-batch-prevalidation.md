# M2 - Batch de pre-validation documentaire

## Objet

Ce document decrit le chantier `feat/m2-batch-prevalidation`.

L'objectif est d'introduire une couche d'orchestration documentaire de campagne
au-dessus des adaptateurs M2 existants.

Le dispositif permet de passer de :

```text
1 objet
  -> 1 diagnostic
  -> 1 resume PR
```

a :

```text
N objets
  -> N diagnostics
  -> 1 rapport consolide
  -> N resumes PR
```

## Architecture

Le noyau commun `tools/m2_core.py` porte les concepts batch generiques :

- `BatchItemResult` ;
- `BatchResult` ;
- `build_batch_result()` ;
- `render_batch_summary()` ;
- `write_batch_summary()`.

Le noyau commun ne connait aucune famille documentaire. Il manipule seulement :

- un libelle de famille ;
- un libelle d'objet ;
- un `CheckResult` ;
- un chemin optionnel vers un resume PR individuel.

La CLI `tools/m2_batch_prevalidation.py` porte le routage concret vers les
adaptateurs disponibles aujourd'hui :

- `person` -> `tools/m2_add_person.py` ;
- `org` -> `tools/m2_add_org.py`.

Cette separation prepare l'ajout de futures familles sans modifier le moteur de
rendu batch.

Pour les campagnes ORG, la CLI reserve les candidats deja diagnostiques pendant
la campagne. Cela permet de proposer des identifiants successifs dans un meme
lot, meme si le registre source reste en lecture seule.

## Format d'entree

La CLI accepte un fichier JSON.

Structure minimale :

```json
{
  "campaign": "campagne-demo",
  "items": [
    {
      "family": "person",
      "name": "Prototype Person",
      "category": "industrie",
      "roles": ["producteur"],
      "sources": ["S41"]
    }
  ]
}
```

Le champ `family` selectionne l'adaptateur.

Les autres champs sont ceux de l'adaptateur cible.

## Commande

```bash
python3 tools/m2_batch_prevalidation.py path/to/campaign.json
```

Sortie consolidee :

```text
exports/generated/batch_summary_campagne-demo.md
```

Par defaut, la CLI genere aussi les resumes PR individuels :

```text
exports/generated/pr_summary_*.md
```

Option disponible :

```bash
python3 tools/m2_batch_prevalidation.py path/to/campaign.json --no-pr-summaries
```

## Rapport consolide

Le rapport Markdown contient :

- synthese ;
- statistiques ;
- liste des objets ;
- reserves ;
- bloquants ;
- arbitrages humains.

Les statistiques consolident :

- nombre d'objets ;
- nombre de pre-validations ;
- nombre de pre-validations avec reserve ;
- nombre de refus ;
- nombre de reserves ;
- nombre de bloquants.

## Exemple PERSON

```json
{
  "campaign": "batch-person",
  "items": [
    {
      "family": "person",
      "name": "Prototype Person",
      "category": "industrie",
      "roles": ["producteur"],
      "sources": ["S41"]
    }
  ]
}
```

Effets :

- execution du diagnostic PERSON ;
- generation du rapport batch ;
- generation du resume PR PERSON.

## Exemple ORG

```json
{
  "campaign": "batch-org",
  "items": [
    {
      "family": "org",
      "name": "Prototype Organisation",
      "category": "label",
      "country": "GB",
      "jd_relation": "label_mate",
      "sources": ["S41"],
      "last_verified": "2026-06-01"
    }
  ]
}
```

Effets :

- execution du diagnostic ORG ;
- generation du rapport batch ;
- generation du resume PR ORG.

## Exemple mixte

```json
{
  "campaign": "batch-mixte",
  "items": [
    {
      "family": "person",
      "name": "Prototype Person",
      "category": "industrie",
      "roles": ["producteur"],
      "sources": ["S41"]
    },
    {
      "family": "org",
      "name": "Prototype Organisation",
      "category": "label",
      "country": "GB",
      "jd_relation": "label_mate",
      "sources": ["S41"],
      "last_verified": "2026-06-01"
    }
  ]
}
```

Le rapport consolide les decisions des deux familles sans que le moteur commun
ait a connaitre leurs regles metier.

Si plusieurs ORG sont presentes dans le meme lot, leurs identifiants provisoires
sont reserves les uns apres les autres pour eviter une collision interne au
rapport de campagne.

## Cas d'usage

Ce chantier couvre :

- pre-validation d'une liste de personnes candidates ;
- pre-validation d'une liste d'organisations candidates ;
- campagne mixte PERSON / ORG ;
- preparation d'une revue humaine avec un rapport unique et des resumes PR
  individuels.

## Limites

Le dispositif ne cree pas :

- interface graphique ;
- formulaire ;
- API ;
- branche Git ;
- Pull Request GitHub ;
- workflow CI ;
- merge ;
- modification de registre.

Le rapport batch reste un artefact documentaire. Les integrations restent sous
controle humain.

## Verifications

Commandes utiles :

```bash
python3 -m unittest tools.test_m2_batch_prevalidation
python3 -m unittest tools.test_m2_add_person tools.test_m2_add_org tools.test_m2_pr_summary
python3 tools/m2_batch_prevalidation.py --help
```
