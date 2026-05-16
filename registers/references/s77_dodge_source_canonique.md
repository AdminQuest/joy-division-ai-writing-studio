# S77 — Source canonique recommandée — Martin Dodge, *Manchester Geographies*, chapitre 3

```yaml
id: REG-S77-DODGE-SOURCE-CANONIQUE
source_id: S77
source_id_requested: S04
source_label: "S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
type_unite: source_canonique
statut: integration_directe
fiabilite: forte
nature: "chapitre d’ouvrage / géographie historique urbaine"
chapitres:
  - Chapitre 1
  - Chapitre 9
```

## Identifiant canonique

L’identifiant demandé par erreur était **S04**. Il ne doit pas être utilisé pour ce fichier.

Dans le registre actuel, **S04** désigne déjà Alan J. Kidd, *Manchester: A History*, 2006. La source Dodge doit donc être séparée de S04.

Identifiant recommandé :

```text
S77
```

Cette recommandation est fondée sur le fait que S76 est déjà massivement utilisé dans les registres et qu’aucune entrée S77 n’a été retrouvée par recherche GitHub. Un contrôle local exhaustif du registre doit néanmoins être effectué avant application du patch.

## Libellé source

Libellé court :

```text
S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d.
```

Libellé long :

```text
DODGE, Martin, « Mapping the geographies of Manchester’s housing problems and the twentieth century solutions », Manchester Geographies, chapitre 3, p. 19-36, année et édition à confirmer.
```

## Dossier source

```text
sources/dodge_manchester_geographies/
```

Fichier PDF recommandé :

```text
sources/dodge_manchester_geographies/S77_dodge_manchester_geographies_housing_problems.pdf
```

## Entrée registre

L’entrée à ajouter au registre figure dans :

```text
sources/dodge_manchester_geographies/registre_patch_s77.json
```

Ne pas appliquer ce patch avant d’avoir vérifié l’absence de S77 dans `data/registre.json`.

## Risques de confusion

- Ne pas écraser S04 : S04 = Kidd, *Manchester: A History*, 2006.
- Ne pas confondre Dodge avec Kidd.
- Ne pas confondre *Manchester Geographies* avec *Manchester: A History*.
- Ne pas traiter cette source comme source directe sur Joy Division.
- Ne pas réduire Manchester aux taudis victoriens : Dodge suit les solutions de logement du XXe siècle.
- Ne pas confondre Wythenshawe, Hulme, Hattersley, Beswick, Moss Side, Angel Meadow et Little Ireland.
- Ne pas utiliser les cartes comme simples illustrations atmosphériques ; elles sont des instruments de spatialisation sociale et politique.
- Vérifier l’année et l’édition de *Manchester Geographies* avant citation finale.

## Consignes pour les futurs atomes

```yaml
source_id: S77
source_label: "S77 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
preuve: "source secondaire universitaire"
usage: "logement, morphologie urbaine, taudis, logement social, Wythenshawe, Hulme, Beswick, géographie historique de Manchester"
prudence: "ne pas utiliser comme source interne sur Joy Division ; ne pas confondre avec S04 Kidd ; vérifier année et édition avant citation finale"
```

Atomes prioritaires :

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
