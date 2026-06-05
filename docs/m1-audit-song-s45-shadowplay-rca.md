# Audit M1 - SONG-S45-SHADOWPLAY-RCA

# Objet de l'audit

Cet audit cible l'anomalie `SONG-S45-SHADOWPLAY-RCA` detectee par le controle M1 `tools/check_dm_registers_consistency.py`.

Le rapport `reports/m1/dm_registers_consistency.md` signale que cet identifiant est visible dans `chapters/01/document_maitre.md`, mais absent de `exports/generated/songs.json`. Le controle DM -> registres le classe donc comme `identifiant introuvable` dans la famille `songs`.

Ce cas constitue un bon pilote M1 parce qu'il suit la boucle complete attendue :

- un controle documentaire detecte un ecart reproductible ;
- l'audit isole un seul identifiant ;
- le diagnostic distingue document maitre, registre source, export et pipeline ;
- aucune correction n'est effectuee dans la PR d'audit.

# Perimetre

Le perimetre est strictement limite a :

- l'identifiant `SONG-S45-SHADOWPLAY-RCA` ;
- le document maitre ou il apparait ;
- les exports chansons, notamment `exports/generated/songs.json` ;
- les registres chansons sous `registers/songs/` ;
- les atomes ou sources necessaires pour comprendre l'origine de l'identifiant ;
- les index generes permettant de verifier si l'identifiant est connu ailleurs.

L'audit ne couvre pas les autres chansons `Shadowplay`, les autres identifiants `SONG-S45-*`, les divergences de libelles, les familles P1, ni la correction du registre.

# Methode

La demarche appliquee est la suivante :

1. rechercher l'identifiant exact `SONG-S45-SHADOWPLAY-RCA` dans les documents maitres, registres, sources, exports et rapports ;
2. verifier si l'identifiant est present dans `chapters/*/document_maitre.md` ;
3. verifier s'il existe dans `registers/songs/` ;
4. verifier s'il est exporte dans `exports/generated/songs.json` ;
5. verifier s'il est connu par les index transversaux generes ;
6. comparer la forme de l'entree S45 avec des entrees chansons exportees comme `SONG-S34-001` ou `SONG-S75-009` ;
7. verifier la regle d'inference de type dans `tools/build_registers.py`, sans modifier le script.

Questions traitees :

- ou l'identifiant apparait-il ?
- dans quels documents maitres ?
- est-il present dans les atomes ?
- est-il present dans les registres ?
- est-il present dans les exports ?
- correspond-il a un alias ?
- correspond-il a un ancien identifiant ?
- correspond-il a un objet supprime ?
- correspond-il a une erreur documentaire ?

# Tableau d'audit

| Objet | Present ? | Emplacement | Observations |
|--------|----------|-------------|--------------|
| Document maitre | Oui | `chapters/01/document_maitre.md`, relation visible `S45-A056 -> SONG-S45-SHADOWPLAY-RCA` | L'identifiant apparait comme cible relationnelle issue de l'atome `S45-A056`. Aucun autre document maitre n'a ete identifie avec cet identifiant exact. |
| Registre chanson | Oui | `registers/songs/s45_curtis_songs_1977_1978_an_ideal_rca.md`, bloc YAML `id: SONG-S45-SHADOWPLAY-RCA` | L'entree existe dans un registre chanson S45, avec `titre: "Shadowplay"` et `source_id: S45`. |
| Export chanson | Non | `exports/generated/songs.json` | L'identifiant exact est absent de l'export chansons. Aucun identifiant `SONG-S45-*` n'est exporte dans `songs.json`. |
| Atomes | Oui, par relation | `sources/curtis_touching_from_a_distance/source_part_1978_wilson_gretton_band_on_the_wall.md`, atome `S45-A056` | L'atome declare une relation `prolonge` vers `SONG-S45-SHADOWPLAY-RCA`. |
| Index transversal | Oui, mais avec type inattendu | `exports/generated/index_by_id.json` | L'identifiant est present, mais classe avec `kind: "atom"` et non `kind: "song"`. |
| Index des documents maitres | Non pertinent | `exports/generated/master_docs_index.json` | L'index de volumetrie ne contient pas l'identifiant exact ; il sert aux compteurs, non a la resolution fine de chaque identifiant chanson. |
| Regle d'export | Oui | `tools/build_registers.py` | `songs.json` est construit a partir des records de kind `song`. L'inference actuelle classe comme `song` un bloc contenant le champ `song`. |
| Entrees chansons comparables | Oui | `registers/songs/s34_fraser_fuoto_songs.md`, `registers/songs/s75_ott_songs_part_02.md` | Les entrees exportees contiennent `type_unite: song` et `song: Shadowplay`, en plus de leur identifiant. |

# Analyse

## 1. Identifiant valide absent du registre

Hypothese non retenue.

`SONG-S45-SHADOWPLAY-RCA` est present dans `registers/songs/s45_curtis_songs_1977_1978_an_ideal_rca.md`. Le probleme n'est donc pas une absence totale du registre source.

## 2. Identifiant valide absent de l'export

Hypothese retenue.

L'identifiant existe dans un registre chanson, mais il est absent de `exports/generated/songs.json`. Le controle DM -> registres signale donc correctement un identifiant visible dans le document maitre mais non resoluble dans l'export P0 utilise pour les chansons.

## 3. Alias non resolu

Hypothese non demontree.

Plusieurs autres objets `Shadowplay` existent dans l'export chansons, par exemple `SONG-S34-001`, `SONG-S75-009`, `SONG-S50-SHADOWPLAY` ou `SONG-S78-SHADOWPLAY`. Aucun element observe ne montre cependant que `SONG-S45-SHADOWPLAY-RCA` serait un alias declare de l'un de ces objets dans `songs.json`.

## 4. Ancien identifiant

Hypothese non demontree.

L'identifiant est encore present dans le registre S45 et dans la relation de l'atome `S45-A056`. Aucun marqueur observe ne le qualifie comme ancien, obsolete ou remplace.

## 5. Objet supprime

Hypothese non retenue.

L'objet n'est pas supprime du depot : il existe dans un registre chanson source et reste reference par un atome. Il est seulement absent de l'export chansons.

## 6. Erreur documentaire

Hypothese peu probable pour le document maitre.

Le document maitre ne semble pas inventer l'identifiant : il reprend une relation deja presente dans l'atome `S45-A056`. L'ecart ne provient donc probablement pas d'une correction a faire directement dans `chapters/01/document_maitre.md`.

## 7. Faux positif du controle

Hypothese non retenue.

Le controle verifie la presence des identifiants chansons visibles dans `exports/generated/songs.json`. Comme `SONG-S45-SHADOWPLAY-RCA` est effectivement absent de cet export, la detection est correcte dans le perimetre du MVP DM -> registres.

# Diagnostic

La cause la plus probable est une divergence de schema dans le registre chanson S45.

L'entree `SONG-S45-SHADOWPLAY-RCA` existe bien dans `registers/songs/s45_curtis_songs_1977_1978_an_ideal_rca.md`, mais sa structure utilise notamment :

- `id: SONG-S45-SHADOWPLAY-RCA` ;
- `titre: "Shadowplay"` ;
- `source_id: S45`.

Elle ne contient pas le champ `song: Shadowplay` observe dans les entrees chansons exportees, ni `type_unite: song`.

Or `tools/build_registers.py` construit `exports/generated/songs.json` a partir des records de kind `song`, et l'inference actuelle identifie notamment les chansons par la presence du champ `song`. Dans `exports/generated/index_by_id.json`, `SONG-S45-SHADOWPLAY-RCA` est connu, mais classe comme `kind: "atom"` et non comme `kind: "song"`.

Le composant concerne est donc le registre chanson S45, plus precisement la conformite de schema de l'entree specialisee S45. La correction minimale probable serait de normaliser l'entree source du registre chanson pour qu'elle soit reconnue comme chanson par le pipeline canonique, puis de regenerer les exports et les documents maitres si necessaire.

Cette PR d'audit ne realise pas cette correction.

# Gravite

Gravite : majeur.

Justification :

- l'identifiant visible dans un document maitre ne se resout pas dans l'export P0 `songs.json` ;
- le controle DM -> registres detecte une rupture effective entre une vue redactionnelle persistante et un export de registre ;
- l'ecart est limite a un objet cible dans le rapport courant ;
- il ne bloque pas la poursuite de M1, car la cause probable est localisee et la correction peut etre traitee dans une PR separee.

# Recommandation

Oui, une PR de correction ciblee devrait etre ouverte apres cet audit.

La correction ne devrait pas porter sur :

- le document maitre, qui reprend une relation issue de l'atome ;
- l'export `songs.json`, qui ne doit pas etre corrige manuellement ;
- le controle DM -> registres, dont la detection est valide dans le perimetre MVP.

La correction devrait porter en priorite sur le registre chanson S45 :

- verifier la forme attendue pour les entrees chansons specialisees ;
- ajouter ou normaliser les champs necessaires a la classification `song`, probablement `type_unite: song` et `song: Shadowplay` ;
- regenerer ensuite les artefacts canoniques avec les outils existants ;
- verifier que `SONG-S45-SHADOWPLAY-RCA` apparait dans `exports/generated/songs.json` ;
- verifier que le rapport DM -> registres ne signale plus cet identifiant comme introuvable.

Si la correction du registre ne suffit pas, il faudra alors examiner le pipeline d'inference dans une PR distincte. A ce stade, rien ne justifie une correction du document maitre ni une modification du controle.

# Conclusion

`SONG-S45-SHADOWPLAY-RCA` est une anomalie reelle, pas un faux positif.

La detection M1 est validee : le controle DM -> registres a correctement identifie un identifiant chanson visible dans un document maitre mais absent de l'export chansons P0.

L'anomalie ne bloque pas la suite de M1. Elle justifie une correction ciblee ulterieure du registre chanson S45 et une regeneration canonique, sans ouvrir M2 et sans correction manuelle des exports ou documents maitres.
