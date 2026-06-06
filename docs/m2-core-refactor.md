# M2.9 - Refactorisation limitee du noyau commun M2

## Objet

Ce document decrit la refactorisation limitee realisee apres validation de
`docs/m2-architecture-adaptateurs.md`.

L'objectif est de reduire la duplication entre les prototypes `PERSON` et `ORG`
sans changer leur comportement documentaire, sans ouvrir de nouvelle famille et
sans creer d'assistant multi-types.

La refactorisation applique l'orientation :

```text
moteur commun
  +
adaptateurs par famille documentaire
```

## Elements mutualises

Le fichier `tools/m2_core.py` porte uniquement les invariants deja observes dans
`tools/m2_add_person.py` et `tools/m2_add_org.py`.

| Element mutualise | Role |
| --- | --- |
| `CheckResult` | Stocke l'entree candidate, les bloquants, les reserves et les informations. |
| Decision | Calcule `non pre-validee`, `pre-validee avec reserve` ou `pre-validee`. |
| Deduplication | Dedoublonne les diagnostics en conservant l'ordre d'apparition. |
| Normalisation texte | Fournit la normalisation utilisee pour les collisions de noms et alias. |
| Proximite texte | Fournit le test de proximite deja commun aux deux prototypes. |
| CSV CLI | Parse les listes CLI separees par virgules. |
| Sources `Sxx` | Charge `data/registre.json` et ajoute les diagnostics source inconnue, source invalide ou source absente. |
| Formatage de valeurs | Produit les listes de valeurs autorisees dans les messages d'erreur. |
| Rendu commun | Rend `Decision`, `Identifiant propose`, `Bloquants`, `Reserves`, `Informations` et `Entree candidate`. |
| Code de sortie | Retourne `1` en presence d'un bloquant, sinon `0`. |

Ces elements correspondent aux invariants autorises par M2.8 :

- classification ;
- decision ;
- stockage et deduplication des diagnostics ;
- lecture et verification generique des sources ;
- structure commune de sortie ;
- determinisme ;
- codes de sortie.

## Elements conserves dans les adaptateurs

Les fichiers `tools/m2_add_person.py` et `tools/m2_add_org.py` conservent toute
la logique propre aux familles documentaires.

### Adaptateur PERSON

Restent dans `tools/m2_add_person.py` :

- format `PERSON-<slug>` ;
- fonction de slugification ;
- lecture des registres people ;
- extraction des blocs YAML `PERSON`;
- `same_as` vers `PERS-*` ;
- verification des `PERS-*` provisoires ;
- index de rattachement `same_as` ;
- `origine: auteur_source` ;
- `alt_names` ;
- `categorie_a_arbitrer` ;
- `a_arbitrer` ;
- categorie PERSON et messages associes ;
- cible d'ecriture people ;
- rendu YAML de l'entree candidate ;
- validation de forme PERSON.

### Adaptateur ORG

Restent dans `tools/m2_add_org.py` :

- format `ORG-NNNN` ;
- calcul du prochain identifiant ORG ;
- lecture de `registers/orgs/orgs.json` ;
- `joy_division_relation` ;
- Wikidata, Discogs et MusicBrainz ;
- `country` ;
- `status` ;
- `gate` ;
- `identity_frozen` ;
- `drift_sentinel` ;
- `last_verified` ;
- categories ORG, statuts et gates ;
- cible d'ecriture ORG ;
- rendu JSON de l'entree candidate ;
- validation de forme ORG.

## Justification

Les choix suivent la separation definie par M2.8.

Le noyau commun ne porte que ce qui est identique dans le comportement observe :
classification, decision, diagnostics, sources, rendu general et code de sortie.

Les adaptateurs gardent ce qui donne son sens documentaire a chaque famille :
identifiants, schemas, relations, collisions, champs metier, artefacts candidats
et cibles d'ecriture.

Cette limite evite deux risques :

- creer une abstraction preventive pour des familles non ouvertes ;
- rendre generiques des decisions qui doivent rester documentaires et humaines.

## Limites

La refactorisation reste volontairement partielle.

Restent dupliques ou proches entre adaptateurs :

- construction des index de noms et alias ;
- parcours des collisions strictes et proches ;
- filtrage des diagnostics schema redondants ;
- construction de l'entree candidate ;
- validation locale de forme ;
- documentation CLI propre a chaque famille.

Cette duplication est acceptee parce qu'elle porte encore du sens documentaire
specifique. La mutualiser maintenant risquerait de melanger les invariants M2
avec les regles propres a `PERSON` ou `ORG`.

La PR ne cree pas :

- `PLACE` ;
- `IMAGE` ;
- `CONCERT` ;
- `RELEASE` ;
- `CITATION` ;
- assistant multi-types ;
- interface ;
- formulaire ;
- automatisation Git ou GitHub.

## Compatibilite comportementale

Les tests existants restent la reference de non-regression :

```bash
python3 -m unittest tools.test_m2_add_person
python3 -m unittest tools.test_m2_add_org
```

Des cas CLI representatifs ont ete compares avant et apres refactorisation :

- `PERSON` conforme ;
- `PERSON` avec source inconnue ;
- `ORG` conforme ;
- `ORG` avec categorie invalide.

Constat :

- meme decision ;
- memes bloquants ;
- memes reserves ;
- memes informations ;
- meme entree candidate ;
- memes codes de sortie.

Aucune divergence de sortie utilisateur n'a ete introduite.
