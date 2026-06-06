# M2 - Industrialisation de la preparation de PR

## Objet

Ce document decrit l'implementation du premier chantier M2 Phase 2 :

```text
Industrialisation de la preparation de PR
```

L'objectif est de permettre aux flux M2 actifs de produire un resume Markdown
standardise, destine a la revue humaine.

Le dispositif ne cree pas de branche, n'ouvre pas de Pull Request GitHub, ne
commit pas et ne merge pas. Il prepare seulement un artefact documentaire.

## Flux raccordes

Les flux raccordes sont :

- `tools/m2_add_person.py` ;
- `tools/m2_add_org.py` ;
- `tools/m2_integrate_source.py`.

Chaque CLI accepte l'option :

```text
--pr-summary
```

Lorsque cette option est presente, le prototype conserve sa sortie habituelle et
ecrit en plus un fichier :

```text
exports/generated/pr_summary_*.md
```

## Architecture

Le noyau commun `tools/m2_core.py` fournit :

- `PRSummary` ;
- `build_pr_summary()` ;
- `render_pr_summary()` ;
- `write_pr_summary()`.

Le noyau commun ne connait aucune famille documentaire. Il ne sait pas ce
qu'est une personne, une organisation ou une source longue.

Les adaptateurs fournissent les informations metier :

- objet de la proposition ;
- perimetre ;
- validations executees ;
- arbitrages humains ;
- impact documentaire ;
- commandes de verification.

Le pipeline logique est :

```text
diagnostic M2
  ->
adaptateur
  ->
PRSummary
  ->
rendu Markdown
  ->
exports/generated/pr_summary_*.md
```

## Format du resume

Le format suit `docs/m2-contrat-pr-summary.md`.

Sections produites :

- objet ;
- perimetre ;
- validations executees ;
- bloquants ;
- reserves ;
- informations ;
- arbitrages humains ;
- impact documentaire ;
- commandes de verification.

Les listes vides sont rendues par :

```text
- aucun
```

Les commandes de verification sont rendues en code inline.

## Exemple PERSON

Commande :

```bash
python3 tools/m2_add_person.py \
  --name "Prototype Person" \
  --category industrie \
  --role producteur \
  --sources S41 \
  --pr-summary
```

Sortie supplementaire attendue :

```text
exports/generated/pr_summary_person_person-prototype-person.md
```

Le resume expose notamment :

- ajout `PERSON` ;
- sources verifiees contre `data/registre.json` ;
- validation de schema PERSON ;
- collisions nom, alias, identifiant et `same_as` ;
- arbitrage humain final ou reserves a traiter.

## Exemple ORG

Commande :

```bash
python3 tools/m2_add_org.py \
  --name "Prototype Organisation" \
  --category label \
  --country GB \
  --jd-relation label_mate \
  --sources S41 \
  --last-verified 2026-06-01 \
  --pr-summary
```

Sortie supplementaire attendue :

```text
exports/generated/pr_summary_org_org-*.md
```

Le resume expose notamment :

- ajout `ORG` ;
- prochain identifiant propose ;
- sources verifiees contre `data/registre.json` ;
- validation de schema ORG ;
- collisions nom, alias, identifiant et Wikidata ;
- reserves ORG eventuelles.

## Exemple SOURCE LONGUE

Commande :

```bash
python3 tools/m2_integrate_source.py \
  --title "Prototype Long Source" \
  --author "Prototype Author" \
  --type livre \
  --year 2026 \
  --reference "Prototype Author, Prototype Long Source, Test Press, 2026." \
  --pr-summary
```

Sortie supplementaire attendue :

```text
exports/generated/pr_summary_source_prototype_author_prototype_long_source.md
```

Le resume expose notamment :

- integration documentaire longue ;
- comparaison avec `data/registre.json` ;
- doublons certains ;
- proximites documentaires ;
- `Sxx` existant ou probable ;
- dossier source probable ;
- absence de creation automatique d'atome, citation ou relation.

## Verifications

Commandes utiles pour ce chantier :

```bash
python3 -m unittest tools.test_m2_pr_summary
python3 -m unittest tools.test_m2_add_person
python3 -m unittest tools.test_m2_add_org
python3 -m unittest tools.test_m2_integrate_source
python3 tools/m2_add_person.py --help
python3 tools/m2_add_org.py --help
python3 tools/m2_integrate_source.py --help
```

Les validateurs documentaires restent ceux des familles :

```bash
python3 tools/validate_people.py
python3 tools/validate_orgs.py
```

## Limites

Le dispositif ne doit jamais :

- ouvrir une Pull Request GitHub ;
- creer ou pousser une branche ;
- commit automatiquement ;
- modifier `main` ;
- merger ;
- masquer une reserve ;
- transformer une pre-validation en validation humaine ;
- creer une source canonique ;
- creer un atome, une citation ou une relation.

Le resume est un artefact de preparation. La decision reste humaine.
