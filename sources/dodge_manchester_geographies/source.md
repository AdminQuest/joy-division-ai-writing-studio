# Source candidate — Martin Dodge, *Manchester Geographies*, chapitre 3

```yaml
source_id_requested: S04
source_id_effective: A_DETERMINER
source_id_recommended: S77
conflict_status: "S04 déjà occupé dans data/registre.json par Alan J. Kidd, Manchester: A History, 2006"
source_label_recommended: "S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
auteur: "Martin Dodge"
titre_chapitre: "Mapping the geographies of Manchester’s housing problems and the twentieth century solutions"
titre_ouvrage: "Manchester Geographies"
annee: "s.d."
edition: "à confirmer"
nature: "chapitre d’ouvrage / géographie historique urbaine"
statut: "source candidate ; conflit d’identifiant à résoudre"
fiabilite: "forte pour le contenu ; référence bibliographique à compléter"
source_drive: "https://drive.google.com/file/d/1w-c8zDBcSzLnLwjVo0IjZ0p2EbnCdXZ-/view?usp=drive_link"
fichier_source_original: "Manchester_Geographies_3_Dodge.pdf"
fichier_source_recommande: "S77_dodge_manchester_geographies_housing_problems.pdf"
pages_utiles_pdf: "19-36"
chapitres:
  - Chapitre 1
  - Chapitre 9
chapitres_secondaires:
  - Chapitre 14
niveau_preuve: "source secondaire universitaire"
```

## Décision canonique

Le fichier fourni ne doit pas être intégré sous **S04** en l’état du repo.

Dans `data/registre.json`, **S04** est déjà attribué à :

```text
S04 — Kidd, Manchester: A History, 2006
```

Le PDF Drive correspond à une autre source :

```text
DODGE, Martin, « Mapping the geographies of Manchester’s housing problems and the twentieth century solutions », dans Manchester Geographies, chapitre 3, p. 19-36.
```

La recommandation est donc d’attribuer à cette source le prochain identifiant libre apparent : **S77**, sous réserve d’un contrôle exhaustif local du registre.

## Libellé source recommandé

Libellé court :

```text
S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d.
```

Libellé long :

```text
DODGE, Martin, « Mapping the geographies of Manchester’s housing problems and the twentieth century solutions », Manchester Geographies, chapitre 3, p. 19-36, année et édition à confirmer.
```

## Dossier source recommandé

```text
sources/dodge_manchester_geographies/
```

Fichier PDF recommandé, s’il est conservé localement hors exports générés :

```text
sources/dodge_manchester_geographies/S77_dodge_manchester_geographies_housing_problems.pdf
```

## Usage principal

Cette source sert à documenter la géographie historique des problèmes de logement à Manchester : taudis industriels, différenciation sociale centre / banlieue, cartes sanitaires et sociales, logement municipal, Wythenshawe, relogement périphérique, Hulme, Hattersley, Beswick / Fort Beswick, urban renewal, système des deck-access estates, effets sociaux des politiques de logement et continuités contemporaines.

## Risques de confusion

1. Ne pas écraser S04 : S04 est déjà Alan J. Kidd, *Manchester: A History*, 2006.
2. Ne pas traiter Dodge comme Kidd : Dodge est une source géographique et cartographique sur le logement, non une histoire générale de Manchester.
3. Ne pas confondre *Manchester Geographies* avec *Manchester: A History*.
4. Ne pas utiliser cette source comme source directe sur Joy Division.
5. Ne pas réduire Manchester au seul motif des taudis victoriens : Dodge suit une séquence longue, du XIXe siècle aux politiques de logement du XXe siècle et aux transformations contemporaines.
6. Ne pas confondre Hulme, Wythenshawe, Hattersley, Beswick et Moss Side : chacun relève d’une séquence urbaine différente.
7. Ne pas utiliser les cartes comme simples illustrations atmosphériques : elles servent à spatialiser des politiques de logement, des diagnostics sociaux et des choix de planification.
8. Vérifier l’année et l’édition de *Manchester Geographies* avant citation bibliographique finale.

## Consignes pour les futurs atomes

Les futurs atomes doivent se concentrer sur la matérialité urbaine de Manchester. La source est particulièrement utile pour le chapitre 1 et le chapitre 9.

Atomes attendus :

```text
S77-A001 — Manchester industriel et logement ouvrier : absence de plan et logique du profit
S77-A002 — Little Ireland et Angel Meadow comme figures du taudis industriel
S77-A003 — Victoria Park et la ségrégation résidentielle bourgeoise
S77-A004 — Cartographier les problèmes de logement : Bastow, Marr et la géographie sanitaire
S77-A005 — La ceinture de taudis autour du cœur commercial de Manchester
S77-A006 — Chorltonville et la solution garden suburb
S77-A007 — Wythenshawe : ville satellite, relogement social et désancrage urbain
S77-A008 — Le plan de 1945 et la dédensification programmée de Hulme
S77-A009 — Overspill estates : Hattersley, Hyde, Heywood, Longdendale
S77-A010 — Urban renewal des années 1960 : Action Areas et effacement des rues victoriennes
S77-A011 — Beswick / Fort Beswick : échec des megastructures et des streets-in-the-sky
S77-A012 — Deindustrialisation, chômage masculin et crise des estates
S77-A013 — Démolition et retour aux maisons conventionnelles dans les années 1980
S77-A014 — Héritages contemporains : gentrification, city centre living et pression immobilière
```

Règle d’usage :

```yaml
source_id: S77
source_label: "S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
preuve: "source secondaire universitaire"
usage: "logement, morphologie urbaine, taudis, logement social, Wythenshawe, Hulme, Beswick, géographie historique de Manchester"
prudence: "ne pas utiliser comme source interne sur Joy Division ; ne pas confondre avec S04 Kidd ; vérifier année et édition avant citation finale"
```
