# Ch.01 — Note éditoriale : nettoyage du DM Ch.09 (2026-05-27)

```yaml
id: NOTE-CH01-NETTOYAGE-CH09-2026-05-27
type_unite: source_notes_nettoyage
chapitre_cible: "Chapitre 1"
chapitre_origine: "Chapitre 9"
date: "2026-05-27"
auteur_action: "Claude (session canonical-sources)"
statut: "applique"
```

## Contexte

L'audit du `2026-05-27` (cf. mon analyse des lacunes critiques des Ch.07 et Ch.09 dans la session courante) a identifié que le `document_maitre.md` du Ch.09 (« Résonances globales : l'influence internationale de Joy Division ») était pollué par **environ 50 atomes de contexte urbain mancunien** issus de 7 sources qui n'ont aucun lien avec la diffusion internationale du groupe.

Ce nettoyage a été appliqué à la source (champs `chapitres:` des atomes dans `sources/`), suivi de la régénération du pipeline (`build_registers.py` + `build_master_docs.py`).

## Atomes rapatriés vers Ch.01

Les atomes ci-dessous étaient tagués `Chapitre 9` à tort. Leur fonction réelle relève de la **matrice urbaine, sociale et affective** que le Ch.01 (« Manchester année zéro : le terreau de la colère ») est précisément chargé d'établir.

### S02 — Sueur, *Villes du futur, futur des villes*, 2011

Matrice urbaine de Manchester comme *shrinking city* industrielle, politique de renouvellement urbain, événements urbains (bombe IRA 1996), inégalités sociales.

| Atome | Titre court | Rattachement final |
|---|---|---|
| S02-PART-MANCHESTER-SHRINKING-CITY-V2 | Passe Manchester shrinking city / renouveau urbain | Ch.1 |
| S02-A001 | Manchester comme archétype de la shrinking city industrielle | Ch.1 |
| S02-A003 | Changement d'échelle : City of Manchester, Greater Manchester, aire urbaine | Ch.1 |
| S02-A004 | La ville rétrécie : vacance, réseaux et coût des infrastructures | Ch.1 |
| S02-A005 | Le renouvellement urbain comme réponse politique au déclin | Ch.1, Ch.14 |
| S02-A006 | Manchester entrepreneuriale : partenariats, événements, compétition | Ch.1, Ch.14 |
| S02-A007 | La bombe de l'IRA de 1996 comme accélérateur de recomposition | Ch.1, Ch.14 |
| S02-A009 | Cultures urbaines, post-punk et régénération symbolique de Manchester | Ch.1, Ch.14 |
| S02-A010 | Le modèle Manchester reste traversé par des inégalités et des limites sociales | Ch.1, Ch.14 |

S02-A008 (Hulme comme laboratoire et limite du renouvellement urbain) → Ch.1 **+ Ch.13** (vécu affectif de Hulme, voir `chapters/13/source_notes_nettoyage_ch09.md`).

### S05 — Jeffery, Tufail & Jackson, *Policing and the Reproduction of Local Social Order*, 2015

Institutions policières mancuniennes, Tactical Aid Group, événements de violence locale (Moss Side 1981, Ordsall 1992, Barton Moss 2014), policing comme reproduction de l'ordre local.

| Atome | Titre court | Rattachement final |
|---|---|---|
| S05-A004 | Tactical Aid Group : force mobile, centralisée, paramilitaire | Ch.1 |
| S05-A006 | Racisme policier et Moss Side 1981 | Ch.1 |
| S05-A009 | Ordsall 1992 : désindustrialisation, inner city et anti-police riot | Ch.1 |
| S05-A011 | Régénération, sécuritisation et policing de la ville attractive | Ch.1, Ch.14 |
| S05-A012 | Barton Moss : police, anti-fracking et défense de l'ordre local | Ch.1 |
| S05-A013 | Police, ordre local et Manchester post-industriel | Ch.1 |

### S06 — Carter, *Youth, race and the inner-city estate*, 2021/2023

Hulme comme inner-city estate, démolition / redevelopment des Crescents, défensible space, fabrique médiatique de l'inner-city crisis.

| Atome | Titre court | Rattachement final |
|---|---|---|
| S06-A002 | Hulme Crescents : démolition, redevelopment, récit de renaissance familiale | Ch.1 |
| S06-A003 | Jeunesse, race et fabrication médiatique de l'inner-city crisis | Ch.1 |
| S06-A005 | Deck-access estates, défensible space, causalité architecturale du crime | Ch.1 |

Les autres atomes S06 (vécu, oral history, témoignages individuels, motifs discursifs affectifs) sont rapatriés vers **Ch.13** plutôt que Ch.1 — voir `chapters/13/source_notes_nettoyage_ch09.md`.

S06-PART-HULME-LIVED-DISCURSIVE-SPACE-V2 est rattachée à **Ch.1 + Ch.13** (la passe couvre les deux registres).

### S11 — HM Treasury, *Financial Statement and Budget Report 1987-88*, 1987

Cadrage budgétaire national avec implications locales mancuniennes (collectivités, dépense publique).

| Atome | Titre court | Rattachement final |
|---|---|---|
| S11-A009 | Local authorities et public expenditure : place des collectivités | Ch.1 |
| REL-S11-007 | Relation S11 / contexte local Manchester | Ch.1 |

### S12 — Dossier de presse, AIDS / Anderton, 13 décembre 1986

Controverse Anderton (chief constable Greater Manchester Police) sur le sida, ordre moral, conflit institutionnel.

| Atome | Titre court | Rattachement final |
|---|---|---|
| S12-A001 | Décembre 1986 : sida, morale publique et controverse nationale | Ch.1 |
| S12-A003 | Gouvernement Thatcher : pragmatisme sanitaire contre croisade morale | Ch.1 |
| S12-A004 | Greater Manchester Police Authority : menace de censure et conflit d'accountability | Ch.1 |
| S12-A007 | Anderton au croisement de police, morale, religion et santé publique | Ch.1 |
| S12-A008 | S12 comme source de presse à croiser avec S05 | Ch.1 |

S12-A006 (Langage de la dégénérescence : homosexualité, drogue, prostitution et ordre moral) → Ch.1 **+ Ch.13** (atmosphère morale, voir Ch.13 note).

### S20 — Dodge, *Mapping Manchester's housing problems*, *Manchester Geographies*, s.d.

Géographies urbaines mancuniennes : taudis victoriens, Little Ireland, Angel Meadow, plans d'urbanisme XXe siècle, overspill estates, mégastructures, urban renewal, gentrification contemporaine.

| Atome | Titre court | Rattachement final |
|---|---|---|
| S20-PART-HOUSING-GEOGRAPHIES-V2 | Passe Manchester, géographies du logement et solutions du XXe siècle | Ch.1 |
| S20-A002 | Little Ireland et Angel Meadow comme figures du taudis industriel | Ch.1 |
| S20-A004 | Cartographier les problèmes de logement : Bastow, Marr, géographie sanitaire | Ch.1 |
| S20-A005 | La ceinture de taudis autour du cœur commercial de Manchester | Ch.1 |
| S20-A007 | Wythenshawe : ville satellite, relogement social et désancrage urbain | Ch.1 |
| S20-A008 | Le plan de 1945 et la dédensification programmée de Hulme | Ch.1 |
| S20-A009 | Overspill estates : Hattersley, Hyde, Heywood, Longdendale | Ch.1 |
| S20-A010 | Urban renewal des années 1960 : Action Areas et effacement des rues victoriennes | Ch.1 |
| S20-A011 | Beswick / Fort Beswick : échec des mégastructures et des streets-in-the-sky | Ch.1 |
| S20-A012 | Désindustrialisation, chômage masculin et crise des estates | Ch.1 |
| S20-A013 | Démolition et retour aux maisons conventionnelles dans les années 1980 | Ch.1 |
| S20-A014 | Héritages contemporains : gentrification, city centre living, pression immobilière | Ch.1, Ch.14 |

## Bilan quantitatif (post-régénération)

| Source | Atomes dans Ch.01 (avant) | Atomes dans Ch.01 (après) | Delta |
|---|---:|---:|---:|
| S02 | ≈2 | 11 | +9 |
| S05 | ≈8 | 14 | +6 |
| S06 | ≈3 | 9 | +6 |
| S11 | ≈9 | 11 | +2 |
| S12 | ≈3 | 9 | +6 |
| S14 | ≈2 | 5 | +3 |
| S20 | ≈3 | 15 | +12 |
| **Total** | **≈30** | **74** | **+44** |

Le compte avant est estimatif : il dépend de l'état antérieur des champs `chapitres:` de chaque atome. La régénération `build_master_docs.py` du `2026-05-27` reflète la nouvelle distribution.

## Méthode

1. Identification des 52 atomes des 7 sources visées contenant `Chapitre 9` dans leur champ `chapitres:`.
2. Reclassement éditorial atome par atome (cf. table ci-dessus + `chapters/13/source_notes_nettoyage_ch09.md`).
3. Modification scriptée des fichiers atomes sources (`sources/<source>/<source_part>.md`) pour retirer `Chapitre 9` et ajouter le(s) chapitre(s) cible(s) selon table.
4. Nettoyage complémentaire des métadonnées source-level (`source.md`, `registre_patch_*.json`, `data/registre.json`) pour cohérence : suppression de `Chapitre 9` des champs `chapitres` et `chapitres_secondaires` des 7 sources.
5. Régénération de `exports/generated/atoms.json` via `tools/build_registers.py`.
6. Régénération de `chapters/*/document_maitre.md` via `tools/build_master_docs.py` (sortie locale).
7. Cette note est créée pour traçabilité éditoriale (le fichier n'est pas lu par `build_master_docs.py`).

## Critère de séparation Ch.01 / Ch.13

- **Ch.01 (matrice urbaine)** : atomes décrivant structures urbaines, institutions policières ou budgétaires, événements urbains datés, politiques publiques, concepts méthodologiques sur la ville.
- **Ch.13 (territoires de la mélancolie / géographie émotionnelle)** : atomes décrivant vécu individuel, témoignages oraux, motifs discursifs affectifs (stigmatisation, atmosphère morale), satire culturelle locale, lecture symbolique des lieux.

## Action restante en environnement local (privé)

Pour propager le nettoyage au repo privé `~/repos/joy-division-studio-private/` (non accessible dans cet environnement remote), exécuter :

```bash
cd ~/repos/joy-division-ai-writing-studio   # ou équivalent local du repo public
git pull   # récupérer la branche claude/curtis-canonical-sources-BFidn
python3 tools/build_registers.py
python3 tools/build_master_docs.py --chapters-dir ~/repos/joy-division-studio-private/chapters
cd ~/repos/joy-division-studio-private
git status   # constater les modifications de chapters/01/, chapters/09/, chapters/13/
git add chapters/01/document_maitre.md chapters/09/document_maitre.md chapters/13/document_maitre.md chapters/master_docs.json
git commit -m "chore: nettoyage Ch.09 → Ch.01 et Ch.13 (sources S02/S05/S06/S11/S12/S14/S20)"
```

Cette opération n'a pas pu être exécutée par l'agent : le repo privé n'est pas monté dans l'environnement remote de la session.
