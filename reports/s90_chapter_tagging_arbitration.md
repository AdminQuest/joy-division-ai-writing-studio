# S90 (Fisher, *Ghosts of My Life*) — Arbitrage de rattachement aux chapitres

> **Statut** : livrable de diagnostic, en attente d'arbitrage éditorial.
> **Date** : 2026-05-30.
> **Contexte** : la régénération de `chapters/XX/document_maitre.md` projette les atomes S90
> selon leur champ `chapitres` (tags réels). On compare ici ces tags au périmètre réel des
> chapitres et à l'intention de la fiche canonique, pour décider quoi garder / re-taguer.

## Écart constaté

- **Fiche canonique** (`registers/references/s90_fisher_ghosts_of_my_life_source_canonique.md`) :
  chapitres **6, 7, 9, 11, 12, 13, 14**.
- **Tags réels des atomes** (`sources/fisher_ghosts_of_my_life/atoms_dm_s90_no_longer_the_pleasures_v2.md`) :
  chapitres **1, 3, 4, 5, 11, 14**.
- **Grand absent à réconcilier** : le **chapitre 12 (santé mentale / trauma)** — listé en principal
  par la fiche canonique, mais **0 atome tagué** alors que plusieurs atomes y appartiennent typiquement.

## Périmètre des chapitres pertinents (rappel, d'après `build_master_docs.py`)

| Ch. | Titre | Fonction |
|---|---|---|
| 1 | Manchester année zéro | Matrice urbaine, sociale et affective. |
| 3 | Première racine : innovations sonores | Gestes sonores rompant avec le punk. |
| 4 | Deuxième racine : poésie de l'aliénation de Curtis | Écriture de Curtis, sans rabattre sur la biographie. |
| 5 | Troisième racine : Saville et l'esthétique du vide | Identité visuelle, Factory. |
| 6 | L'arbre se dresse : architecture sonore (1979-80) | Production, forme-album, *Closer*. |
| 7 | L'héritage musical à travers les décennies | Héritages musicaux et reprises. |
| 9 | Résonances globales | Diffusion et réceptions internationales. |
| 11 | Joy Division et la condition humaine moderne | Persistance existentielle. |
| 12 | L'expression du trauma : santé mentale | Trauma, éthique de réception, anti-réduction clinique. |
| 13 | Les territoires de la mélancolie | Géographie émotionnelle. |
| 14 | L'éternel retour : culture contemporaine | Patrimonialisation, détournements, mythe. |

## Tableau d'arbitrage atome par atome

| Atome | Titre court | Chap. tagués | Importance | Recommandation | Justification |
|---|---|---|---|---|---|
| **S90-A001** | JD capte par anticipation l'esprit dépressif ; 1979-80 comme seuil historique | 11, 14 | critique | **11** (garder) ; +1 envisageable | Hauntologie / *lost futures* = cœur de la condition moderne (11) ; le motif 1979-80 effleure le ch.1 mais reste subordonné. |
| **S90-A002** | Les trois films (Control vs doc de Gee) ; hauntologie du document | 14 | majeure | **14** (garder) | Réception filmique + patrimonialisation = périmètre exact du ch.14. |
| **S90-A003** | *She's Lost Control* : épilepsie comme unheimlich | 4, 5 | majeure | **4** (garder) ; **5 → 12** | Ch.4 (poésie de Curtis) juste ; tag 5 (Saville/visuel) hors-sujet ; l'épilepsie comme *holy sickness* relève du ch.12. |
| **S90-A004** | La « religion JD » comme affaire de garçons ; exclusion des femmes | 4, 14 | majeure | **14** (garder) ; **4 → 12** | Fandom/culte/genre = réception (14) ; tag 4 faible ; éthique de réception → ch.12. |
| **S90-A005** | Hannett+Saville : « neuromantiques en cyberpunks » ; plus Art que Rock | 3, 5 | majeure | **3 + 5** (garder) | Production sonore (Hannett→3) + identité visuelle (Saville→5) : double tag parfaitement justifié. |
| **S90-A006** | Le rapport occulté au Black Atlantic ; dub-méthodologie | 3 | utile | **3** (garder) ; **+9** envisageable | Innovation sonore (dub) = ch.3 ; le Black Atlantic (Gilroy) ouvre une résonance internationale → ch.9 possible. |
| **S90-A007** | Dépression vs tristesse ; mélancolie sans objet-cause ; zero affect | 4, 11 | critique | **11** (garder) ; **+12** ; 4 discutable | Ontologie dépressive = ch.11 ; **l'**atome santé mentale par excellence → ch.12 manquant. |
| **S90-A008** | « Le plus schopenhauerien des groupes » ; anti-rock | 4, 11 | majeure | **11** (garder) ; 4 faible | Cadre philosophique/existentiel = ch.11 ; « anti-rock » irait plutôt au ch.3 qu'au ch.4. |
| **S90-A009** | La voix de Curtis comme « déjà mort » ; fatalisme | 4, 14 | majeure | **4 + 14** (garder) | Analyse de la voix/écriture de Curtis (4) + *death-within-life* nourrissant le mythe posthume (14) : cohérent. |
| **S90-A010** | Le suicide comme garantie d'authenticité (« 4 Real ») ; mythe froid | 4, 14 | critique | **14** (garder) ; **4 → 12** | Mythe posthume = ch.14 ; mais la romantisation du suicide est la question éthique du ch.12. |
| **S90-A011** | Les deux JD (« Pure Art » vs « just a laff ») ; vérité du Laddism | 14 | majeure | **14** (garder) ; **+12** | Mythe vs quotidien = ch.14 ; « santé mentale des adolescents » est un fil ch.12 explicite. |
| **S90-A012** | Angleterre 1979 : « speed comedown » ; destruction de la communauté ouvrière | 1, 11 | majeure | **1 + 11** (garder) | Manchester/Thatcher/1979 = ch.1 (terreau) + *the void* = ch.11 : double tag solide. |

## Lecture d'ensemble

1. **Le vrai trou = chapitre 12 (santé mentale / trauma)** : 0 atome tagué, alors que la fiche
   canonique le classe en principal et que 4 atomes y appartiennent typiquement
   (A003 épilepsie, A007 dépression, A010 suicide, A011 ados). → C'est ici que le re-tag a le plus de valeur.
2. **Chapitres 6, 7, 13 de la fiche canonique : non soutenus par le contenu réel** des atomes.
   Seul A006 → 9 (Black Atlantic) est marginalement défendable. → Ici, c'est plutôt la fiche
   canonique qui est trop large et devrait être resserrée.
3. **Tags actuels globalement sains** sur l'axe son/visuel/Curtis (A005, A006, A009, A012) — peu ou pas à toucher.

## Orientation recommandée (un « mix »)

- **Re-taguer vers 12** : A003, A007, A010, A011 (et y déplacer les tags faibles 4/5 de A003/A004).
- **Accepter tel quel** : A001, A002, A005, A006, A008, A009, A012.
- **Resserrer la fiche canonique** : retirer 6, 7, 13 (garder 9 comme secondaire optionnel via A006).

## Procédure d'application (à exécuter après arbitrage)

1. Éditer le champ `chapitres` des atomes concernés dans
   `sources/fisher_ghosts_of_my_life/atoms_dm_s90_no_longer_the_pleasures_v2.md`.
2. `python3 tools/build_registers.py`
3. `python3 tools/build_master_docs.py` (puis éventuellement `inject_chapter_source_notes.py`).
4. Re-soumettre le diff `chapters/XX/document_maitre.md` pour validation avant tout commit.
