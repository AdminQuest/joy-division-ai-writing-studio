# Cloture formelle M1

## 1. Objet du document

M1 a pour role de fiabiliser le corpus documentaire avant tout chantier d'enrichissement. Son objectif n'est pas de produire un nouveau studio, ni de creer des formulaires d'ajout, mais de reduire le risque d'integration documentaire par des controles, des rapports, des audits, des corrections ciblees et une consolidation lisible.

La roadmap strategique 2026 pose un verrou explicite : M2 reste interdit tant que M0 et M1 ne sont pas clotures. M0 est indique comme termine dans `reports/m1/status_m1.md`, mais l'ouverture de M2 depend encore de la cloture effective de M1.

Ce document evalue donc l'etat reel de M1 au regard des criteres de sortie de `docs/roadmap-strategique-2026.md`. Il distingue les criteres atteints, partiellement atteints et non atteints, documente les dettes residuelles, puis decide explicitement si M1 peut etre cloture.

## 2. État réel de M1

Les realisations suivantes sont effectivement disponibles dans le depot.

| Element | Etat reel |
| --- | --- |
| DM -> atomes | Controle implemente par `tools/check_dm_atoms_traceability.py`, rapport `reports/m1/dm_atoms_traceability.md`, statut consolide conforme. |
| DM -> registres | Controle implemente par `tools/check_dm_registers_consistency.py`, rapport `reports/m1/dm_registers_consistency.md`, statut consolide conforme avec reserve. |
| DM -> sources | Controle implemente par `tools/check_dm_sources_consistency.py`, rapport `reports/m1/dm_sources_consistency.md`, statut consolide conforme. |
| Agregateur M1 | `tools/aggregate_m1.py` lit les rapports M1 versionnes et genere `reports/m1/status_m1.md`. |
| Status consolide | `reports/m1/status_m1.md` existe et consolide les trois controles M1. Son etat global est `conforme avec réserve`. |
| Audits | `reports/m1/status_m1.md` valide l'audit `Atomes S35 source vide` et valide avec reserve l'audit `SONG-S45-SHADOWPLAY-RCA`. |
| Tests | Les tests unitaires des controles DM et de l'agregateur existent et passent. |

Resultats consolides observes :

| Controle | Statut | Donnees principales |
| --- | --- | --- |
| DM -> atomes | conforme | 2477 atomes visibles, 2477 retrouves, 0 ecart. |
| DM -> registres | conforme avec reserve | 0 identifiant introuvable, 0 registre absent, 0 compteur incoherent, 29 libelles divergents, 51 familles non couvertes. |
| DM -> sources | conforme | 536 sources visibles, 536 retrouvees, 0 source inconnue, 19 sources orphelines informatives, 0 ecart. |

Ces elements demontrent que la couche M1 centree sur les documents maitres est operationnelle pour trois relations P0 : documents maitres vers atomes, registres et sources canoniques.

## 3. Vérification des critères de sortie

| Critère | État | Justification |
| --- | --- | --- |
| le nombre de liens inter-registres orphelins est nul sur le perimetre publie | partiellement atteint | `reports/m1/dm_registers_consistency.md` indique `Relations non résolues = 0` dans le perimetre DM -> registres P0. Le rapport signale toutefois 51 familles non couvertes, dont des relations hors MVP, et ne constitue pas une mesure complete des liens inter-registres orphelins sur tout le perimetre publie. |
| le nombre d'identifiants canoniques dupliques est nul | partiellement atteint | Des validateurs et tests existent dans le depot, mais `reports/m1/status_m1.md` ne publie pas encore un indicateur consolide des identifiants canoniques dupliques. Le critere n'est donc pas demontre par le status M1. |
| les invariants critiques sont au vert | partiellement atteint | Les controles DM sont au vert ou conformes avec reserve, et les tests M1 passent. En revanche, `reports/m1/status_m1.md` ne consolide pas l'ensemble des invariants critiques de la roadmap, notamment au-dela du perimetre DM. |
| la validation de schema atteint le seuil attendu | partiellement atteint | Des validateurs de schema existent et les tests executes passent, mais le status M1 ne publie pas de taux de validation de schema a 100 %. Le seuil attendu n'est pas encore prouve par un tableau de bord M1. |
| le tableau de bord qualite est genere et publie | non atteint | `reports/m1/status_m1.md` est un status consolide genere, mais il indique explicitement qu'il n'est pas un tableau de bord M1 et ne couvre pas les blocs de volumetrie, integrite et verification definis par la roadmap. |
| l'audit du cas Pennie Smith est clos et documente | non atteint | Les documents et rapports M1 examines ne contiennent pas de document de cloture d'audit Pennie Smith comparable aux audits S35 ou `SONG-S45-SHADOWPLAY-RCA`. Le critere n'est pas demontre dans les artefacts M1 consolides. |
| les regles de source, de provenance et de droits sont ecrites et appliquees | partiellement atteint | `DM -> sources` applique une regle de coherence d'identifiants source contre `data/registre.json`. Les regles de provenance et de droits restent plus larges que ce controle, notamment pour l'iconographie et le multimedia, et ne sont pas consolidees comme appliquees dans `status_m1.md`. |
| les champs de provenance sont isoles des facettes documentaires, verification a l'appui | partiellement atteint | Le depot contient des conventions et des validateurs portant sur la provenance, mais `reports/m1/status_m1.md` ne publie pas encore de verification dediee attestant l'isolation des champs de provenance des facettes documentaires sur le perimetre M1. |
| aucun champ de type sources ne contient d'identifiant interne inadapte comme IMAGE-* lorsqu'il doit contenir des sources documentaires SNN | partiellement atteint | Le controle `DM -> sources` verifie les references source visibles dans les documents maitres contre les identifiants `Sxx` de `data/registre.json`. Il ne verifie pas encore tous les champs `sources` du corpus ni tous les cas `IMAGE-*` hors documents maitres. |
| Liens inter-registres orphelins sur le perimetre publie : 0 | partiellement atteint | Le seuil est atteint pour `Relations non résolues = 0` dans le rapport DM -> registres, mais pas encore mesure comme indicateur global du perimetre publie. |
| Identifiants canoniques dupliques : 0 | partiellement atteint | Aucun indicateur M1 consolide ne publie cette valeur. Les tests passes ne remplacent pas un indicateur de sortie publie. |
| Validation de schema : 100 % | partiellement atteint | Les validations disponibles passent dans les tests executes, mais aucun taux global `100 %` n'est publie dans le status M1. |

Synthese : les controles P0 centres sur les documents maitres sont stabilises, mais les criteres de sortie M1 de la roadmap ne sont pas tous atteints au niveau exige pour une cloture formelle.

## 4. Dette résiduelle acceptée

La dette suivante est acceptee comme dette documentee de M1, mais elle ne suffit pas a autoriser M2 tant que les criteres de sortie restent incomplets.

| Dette | Statut |
| --- | --- |
| Divergences de libelles dans DM -> registres | Reserve acceptee par l'agregateur : 29 libelles divergents, non traites comme corrections automatiques. |
| Familles hors MVP dans DM -> registres | Reserve acceptee par l'agregateur : 51 familles non couvertes, notamment concepts, motifs, mythes, organisations et relations hors MVP. |
| Sources orphelines | Information non bloquante dans DM -> sources : 19 sources canoniques presentes dans `data/registre.json` mais non mobilisees par les documents maitres. |
| DM -> exports | Chantier non implemente dans `reports/m1/status_m1.md`. |
| DM -> generation | Chantier non implemente dans `reports/m1/status_m1.md`. |
| DM -> obsolescence | Chantier non implemente dans `reports/m1/status_m1.md`. |
| DM -> statut documentaire | Chantier non implemente dans `reports/m1/status_m1.md`. |
| Alias avances et libelles d'usage | Dette de qualification documentaire. Elle peut relever d'un approfondissement ulterieur des regles d'alias, pas d'une correction automatique M1. |
| Tableau de bord enrichi | Hors du status consolide actuel. Le tableau de bord qualite complet ou enrichi reste a concevoir dans une PR separee. |
| Historisation et tendances | Hors du perimetre des rapports M1 actuels. La roadmap mentionne le suivi de tendance, mais `status_m1.md` ne l'implemente pas. |
| CI GitHub comme seuil de passage M1 | Hors perimetre de l'agregateur minimal. Les checks peuvent verifier le depot, mais M1 n'a pas encore defini une politique CI de blocage documentaire. |

Ce qui releve de M2 ou des jalons ulterieurs :

- formulaires d'ajout documentaire ;
- studio d'enrichissement documentaire ;
- generation automatique d'identifiants pour ajouts courants ;
- interfaces d'enrichissement ou de correction ;
- politique multimedia complete, droits et republication, rattachee notamment a M5 ;
- migration Cloudflare ou architecture unifiee, rattachees a M3 ou au-dela.

## 5. Tableau de bord qualité minimal

Question : le fichier `reports/m1/status_m1.md` satisfait-il la definition du tableau de bord qualite minimal figurant dans la roadmap ?

Reponse : non.

Argumentation :

- `reports/m1/status_m1.md` est bien genere par `tools/aggregate_m1.py` et publie dans `reports/m1/`.
- Il consolide les controles DM -> atomes, DM -> registres et DM -> sources.
- Il liste des audits M1 et une dette documentaire connue.
- Il ne publie pas les blocs demandes par la roadmap pour le tableau de bord qualite minimal : volumetrie, integrite et verification.
- Il ne calcule pas les metriques de volumetrie sur sources, personnes, organisations, lieux, concerts, images, variantes de releases, possessions et chansons.
- Il ne publie pas de synthese d'integrite couvrant liens casses, identifiants dupliques, exports en echec et schemas invalides.
- Il ne publie pas de taux global de verification ni de taux par registre.
- Il indique explicitement dans sa section `Limites` : `Ce fichier n'est pas un tableau de bord M1 et ne definit aucun seuil CI.`

Conclusion : non.

`reports/m1/status_m1.md` est un status consolide utile et regenerable. Il prepare un tableau de bord qualite minimal, mais il ne le satisfait pas encore au sens de la roadmap.

## 6. Évaluation finale

M1 demontre desormais une capacite reelle de controle documentaire sur les documents maitres :

- les atomes visibles dans les documents maitres sont retrouves dans l'export attendu ;
- les identifiants P0 de registres visibles dans les documents maitres sont retrouves dans les exports disponibles ;
- les sources visibles dans les documents maitres sont retrouvees dans le registre canonique `data/registre.json` ;
- les rapports M1 sont agreges dans un status consolide ;
- les audits S35 et `SONG-S45-SHADOWPLAY-RCA` sont relies a des controles qui valident leur correction ou leur reserve.

Ce qui a ete valide :

- la chaine controle -> rapport -> agregation -> status consolide ;
- la lecture seule des controles M1 ;
- l'absence de correction automatique ;
- la detection de rapports absents, illisibles ou non conformes dans l'agregateur ;
- le traitement des sources canoniques au niveau DM -> sources, niveau 1.

Ce qui reste hors perimetre ou incomplet :

- derivabilite passage par passage ;
- controle section -> source ;
- controle paragraphe -> atome -> source ;
- tableau de bord qualite minimal au sens de la roadmap ;
- consolidation globale des liens inter-registres orphelins ;
- publication d'un compteur consolide d'identifiants canoniques dupliques ;
- publication d'un taux global de validation de schema a 100 % ;
- audit Pennie Smith clos et documente dans les artefacts M1 ;
- verification consolidee des champs de provenance, droits et champs `sources` hors documents maitres.

Vérifications executees pour cette evaluation :

| Commande | Resultat |
| --- | --- |
| `python3 tools/check_dm_atoms_traceability.py` | OK : 14/14 DM tracables, 2477/2477 atomes retrouves, 0 ecart. |
| `python3 tools/check_dm_registers_consistency.py` | OK avec reserve : 0 identifiant introuvable, 0 compteur incoherent, 80 ecarts de reserve. |
| `python3 tools/check_dm_sources_consistency.py` | OK : 14/14 DM coherents, 536/536 sources retrouvees, 0 source inconnue, 0 ecart. |
| `python3 tools/aggregate_m1.py` | OK : status consolide conforme avec reserve. |
| `python3 -m unittest tools.test_aggregate_m1` | OK : 17 tests passes. |
| `python3 -m unittest tools.test_check_dm_atoms_traceability` | OK : 17 tests passes. |
| `python3 -m unittest tools.test_check_dm_registers_consistency` | OK : 12 tests passes. |
| `python3 -m unittest tools.test_check_dm_sources_consistency` | OK : 8 tests passes. |

Appreciation synthetique : M1 a atteint une maturite operationnelle pour les controles P0 des documents maitres, mais il ne satisfait pas encore tous les criteres de sortie de la roadmap. Le jalon ne peut donc pas etre cloture formellement sans abaisser les criteres de sortie.

## 7. Décision

Décision :
M1 reste ouvert.
L'ouverture de M2 n'est pas autorisée.
