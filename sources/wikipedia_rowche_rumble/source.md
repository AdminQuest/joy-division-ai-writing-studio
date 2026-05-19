# S17 — Source canonique — Wikipedia, « Rowche Rumble »

```yaml
id: S17
source_id: S17
type_unite: source
source_label: "S17 — Wikipedia, Rowche Rumble, page consultée 2026"
source_short_title: "Wikipedia, Rowche Rumble"
auteur: "Wikipedia contributors"
titre: "Rowche Rumble"
annee: "s.d. / page consultée 2026"
dossier_source: "sources/wikipedia_rowche_rumble/"
source_url: "https://en.wikipedia.org/wiki/Rowche_Rumble"
statut: "source canonique refixée ; source web tertiaire ; informations à vérifier dans les sources discographiques et critiques"
```

## 1. Identifiant canonique

```text
S17
```

## 2. Libellé source

```text
S17 — Wikipedia, Rowche Rumble, page consultée 2026
```

## 3. Dossier source

```text
sources/wikipedia_rowche_rumble/
```

## 4. Référence complète

WIKIPEDIA CONTRIBUTORS, « Rowche Rumble », *Wikipedia, The Free Encyclopedia*, page web : https://en.wikipedia.org/wiki/Rowche_Rumble, consultée le 19 mai 2026.

Note bibliographique interne : il s’agit d’une source web encyclopédique, évolutive et tertiaire. La page porte sur « Rowche Rumble », chanson de The Fall sortie en single en 1979 chez Step-Forward, avec « In My Area » en face B. La page mentionne Mark E. Smith, Craig Scanlon et Marc Riley comme auteurs, Cargo Studios à Rochdale comme lieu d’enregistrement, Oz McCormick et The Fall comme producteurs, et un contexte d’anecdote pharmaceutique autour de Roche / Rowche. Ces informations doivent être vérifiées dans les sources citées par la page, notamment Discogs, The Fall Tracks A-Z / The Fall Live, AllMusic, NME, John Peel / Festive Fifty, et les sources primaires The Fall disponibles.

## 5. Décision canonique

S17 désigne exclusivement la page Wikipedia anglophone « Rowche Rumble ».

S17 ne désigne pas la chanson elle-même comme source primaire. La chanson, le single, les paroles, les crédits, les dates d’enregistrement et les positions de classement doivent être vérifiés dans des sources plus robustes : disque original, notices discographiques, Discogs, archives Step-Forward, The Fall Online / The Fall Tracks A-Z, AllMusic, presse musicale contemporaine, entretiens de Marc Riley et documentation John Peel.

S17 sert de point d’entrée secondaire et provisoire vers un corpus The Fall / Manchester post-punk, utile pour repérer des objets à vérifier : « Rowche Rumble », « In My Area », Step-Forward, Cargo Studios, Rochdale, Roche, barbiturates, indie chart, NME, Festive Fifty, et l’ancrage de The Fall dans le voisinage post-punk de Joy Division.

## 6. Entrée à ajouter dans `data/registre.json`

L’entrée complète est fixée dans :

```text
sources/wikipedia_rowche_rumble/registre_patch_s17.json
```

Elle est appliquée par :

```text
python3 tools/apply_s17_registre_patch.py
```

## 7. Fonction dans le livre

S17 est une source d’orientation et de comparaison. Elle ne doit pas soutenir seule une affirmation historique forte. Elle peut néanmoins aider à introduire The Fall comme voisin mancunien post-punk de Joy Division : même moment, même tension urbaine, même région industrielle, mais autre idiome esthétique, plus sarcastique, répétitif et verbalement abrasif.

La source est particulièrement utile pour :

- le chapitre 2, si l’on situe les formations post-punk de Manchester et les parallèles The Fall / Joy Division ;
- le chapitre 3, si l’on compare des idiomes sonores post-punk : répétition, sécheresse, guitare, voix, rythme ;
- le chapitre 10, si l’on traite la circulation numérique de notices encyclopédiques, de références discographiques et de mémoire post-punk ;
- le chapitre 11, si l’on articule The Fall, Roche / Rowche, médicament, contrôle, langage fragmenté et modernité pathologique, avec prudence ;
- le chapitre 14, si l’on évoque la patrimonialisation web des scènes post-punk et les voisinages de canonisation.

## 8. Risques de confusion

1. Ne pas utiliser S17 comme source primaire sur The Fall, Mark E. Smith, Step-Forward ou la discographie du single.
2. Ne pas utiliser Wikipedia comme autorité finale pour les dates, crédits, lieux d’enregistrement, classements ou citations.
3. Ne pas confondre « Rowche Rumble » et Roche : le titre est une graphie stylisée qui appelle vérification dans les sources The Fall.
4. Ne pas plaquer The Fall sur Joy Division. Les deux groupes appartiennent au même paysage post-punk mancunien, mais leurs écritures, leurs mythologies et leurs régimes sonores diffèrent.
5. Ne pas traiter l’anecdote des barbituriques comme fait stabilisé sans source primaire ou témoignage vérifié.
6. Ne pas citer les paroles de « Rowche Rumble » depuis Wikipedia ; vérifier les lyrics dans une source autorisée ou dans le support discographique.
7. Ne pas transformer l’article Wikipedia en source sur la santé mentale, l’industrie pharmaceutique ou Roche Products Limited.
8. Ne pas confondre réception critique, classement indie et importance historique.
9. Ne pas utiliser S17 pour faire une histoire générale de The Fall ; créer une source plus solide si l’analyse de The Fall devient structurante.
10. Ne pas faire de S17 une source canonique forte : son statut doit rester celui d’une source web tertiaire, utile pour orientation, repérage et contrôle initial.

## 9. Consignes pour les futurs atomes

Les futurs atomes S17 doivent être rares et prudents. Ils doivent documenter uniquement les nœuds utiles au manuscrit et signaler systématiquement les vérifications à faire.

```text
S17-A001 — S17 comme source web tertiaire, non comme preuve primaire sur The Fall
S17-A002 — « Rowche Rumble » : single post-punk de The Fall, 1979, à vérifier discographiquement
S17-A003 — The Fall comme voisin mancunien de Joy Division : proximité de scène, divergence d’idiome
S17-A004 — Cargo Studios, Rochdale : lieu d’enregistrement à vérifier
S17-A005 — Step-Forward Records : label du single à vérifier
S17-A006 — Roche / Rowche, barbituriques et anecdote pharmaceutique : matériau à manier prudemment
S17-A007 — « In My Area » : face B et territorialité locale, à vérifier
S17-A008 — Indie chart, NME, Festive Fifty : réception et classement à croiser
S17-A009 — Marc Riley et « Tight Pants » : influence musicale alléguée à vérifier
S17-A010 — Usage final : comparer The Fall et Joy Division sans les fusionner
```

Bloc d’usage recommandé :

```yaml
source_id: S17
source_label: "S17 — Wikipedia, Rowche Rumble, page consultée 2026"
source_author: "Wikipedia contributors"
source_title: "Rowche Rumble"
preuve: "source web tertiaire / orientation discographique et critique sur un single de The Fall"
usage: "The Fall ; Rowche Rumble ; In My Area ; Mark E. Smith ; Manchester post-punk ; Cargo Studios ; Rochdale ; Step-Forward ; Roche ; barbiturates ; indie chart ; NME ; Festive Fifty"
prudence: "ne pas utiliser comme source primaire ; vérifier dates, crédits, paroles, anecdotes et classements dans des sources discographiques, journalistiques ou testimoniales robustes"
```

Formules utilisables :

```text
source web tertiaire
point d’entrée discographique
voisinage post-punk mancunien
The Fall comme contrepoint à Joy Division
mémoire encyclopédique du post-punk
Rowche / Roche : graphie, médicament, satire sociale
réception indie et patrimonialisation web
```

Formules à proscrire :

```text
Wikipedia prouve
S17 établit définitivement
The Fall et Joy Division disent la même chose
Rowche Rumble explique Joy Division
l’anecdote pharmaceutique est certaine
Wikipedia suffit pour les paroles
Wikipedia suffit pour les crédits discographiques
The Fall remplace les sources sur Joy Division
```
