# S16 — Source canonique — Songfacts, « Boredom by Buzzcocks »

```yaml
id: S16
source_id: S16
type_unite: source
source_label: "S16 — Songfacts, Boredom by Buzzcocks, page consultée 2026"
source_short_title: "Songfacts, Boredom by Buzzcocks"
auteur: "Songfacts"
titre: "Boredom by Buzzcocks"
annee: "s.d. / page consultée 2026"
dossier_source: "sources/songfacts_buzzcocks_boredom/"
source_url: "https://www.songfacts.com/facts/buzzcocks/boredom"
statut: "source canonique refixée ; source web secondaire/tertiaire ; informations à vérifier dans les sources discographiques et critiques"
```

## 1. Identifiant canonique

```text
S16
```

## 2. Libellé source

```text
S16 — Songfacts, Boredom by Buzzcocks, page consultée 2026
```

## 3. Dossier source

```text
sources/songfacts_buzzcocks_boredom/
```

## 4. Référence complète

SONGFACTS, « Boredom by Buzzcocks », *Songfacts*, page web : https://www.songfacts.com/facts/buzzcocks/boredom, consultée le 19 mai 2026.

Note bibliographique interne : il s’agit d’une page web Songfacts consacrée à « Boredom » de Buzzcocks. La source doit être traitée comme une notice d’orientation : utile pour repérer des informations, anecdotes, interprétations ou sources secondaires, mais insuffisante comme preuve autonome sur les crédits, la date, les paroles, l’enregistrement ou la réception critique.

## 5. Décision canonique

S16 désigne exclusivement la page Songfacts « Boredom by Buzzcocks ».

S16 ne désigne pas la chanson elle-même comme source primaire. La chanson « Boredom », l’EP *Spiral Scratch*, les crédits Devoto / Shelley, la session d’enregistrement, la production par Martin Hannett, le label New Hormones, l’éthique DIY, l’auto-publication et la réception critique doivent être vérifiés dans des sources plus robustes : support original, notices discographiques, Discogs, liner notes, *Spiral Scratch*, Jon Savage, Simon Reynolds, David Nolan, Richard Boon, entretiens Howard Devoto / Pete Shelley, presse musicale contemporaine et archives Buzzcocks.

S16 sert de point d’entrée secondaire pour un objet punk mancunien décisif : « Boredom » comme chanson de rupture, minimalisme volontaire, anti-virtuosité, ironie contre la scène punk elle-même, et prélude aux divergences entre punk, post-punk, Buzzcocks, Magazine et Joy Division.

## 6. Entrée à ajouter dans `data/registre.json`

L’entrée complète est fixée dans :

```text
sources/songfacts_buzzcocks_boredom/registre_patch_s16.json
```

Elle est appliquée par :

```text
python3 tools/apply_s16_registre_patch.py
```

## 7. Fonction dans le livre

S16 est une source d’orientation et de comparaison. Elle peut aider à situer « Boredom » comme jalon punk mancunien immédiatement antérieur à Joy Division : un morceau simple, sec, sarcastique, anti-spectaculaire, qui annonce une sortie de l’orthodoxie punk au moment même où elle se cristallise.

La source est particulièrement utile pour :

- le chapitre 2, si l’on situe la scène punk mancunienne de 1976-1977, les Buzzcocks, Howard Devoto, Pete Shelley, *Spiral Scratch* et l’éthique DIY ;
- le chapitre 3, si l’on compare minimalisme musical, anti-solo, répétition, sécheresse rythmique et refus de la virtuosité ;
- le chapitre 4, si l’on traite les ruptures de posture entre Devoto, Shelley, Curtis et les écritures post-punk ;
- le chapitre 10, si l’on analyse la mémoire web des chansons punk et post-punk ;
- le chapitre 14, si l’on examine la canonisation rétrospective de « Boredom », de *Spiral Scratch* et de l’indépendance DIY.

## 8. Risques de confusion

1. Ne pas utiliser S16 comme source primaire sur Buzzcocks, Howard Devoto, Pete Shelley, Martin Hannett, New Hormones ou *Spiral Scratch*.
2. Ne pas utiliser Songfacts comme autorité finale pour les paroles, crédits, dates, sessions ou citations.
3. Ne pas citer les paroles de « Boredom » depuis Songfacts sans vérification dans une source autorisée ou dans le support discographique.
4. Ne pas confondre la chanson « Boredom » avec l’ensemble de l’EP *Spiral Scratch*.
5. Ne pas réduire « Boredom » à une chanson comique ou anecdotique : elle a une fonction critique dans la sortie du punk comme formule.
6. Ne pas faire de « Boredom » une cause directe de Joy Division. La chanson appartient à l’environnement punk mancunien ; elle sert de contrepoint et de seuil, non d’origine unique.
7. Ne pas confondre Buzzcocks, Magazine et Joy Division. Howard Devoto relie ces histoires, mais les idiomes musicaux divergent.
8. Ne pas confondre réception critique, canonisation ultérieure et effet historique immédiat.
9. Ne pas utiliser S16 pour écrire une histoire générale de Buzzcocks ; créer une source plus solide si Buzzcocks devient un axe structurant.
10. Ne pas ignorer le statut fragile d’une notice web : tout fait utilisable dans le manuscrit doit être contrôlé.

## 9. Consignes pour les futurs atomes

Les futurs atomes S16 doivent être rares et prudents. Ils doivent documenter uniquement les nœuds utiles au manuscrit et signaler les vérifications à faire.

```text
S16-A001 — S16 comme source web secondaire/tertiaire, non comme preuve primaire sur Buzzcocks
S16-A002 — « Boredom » comme jalon punk mancunien de 1977, à vérifier discographiquement
S16-A003 — *Spiral Scratch*, New Hormones et l’éthique DIY : matériau à croiser avec Reynolds, Savage et les supports originaux
S16-A004 — Howard Devoto : ennui, rupture et sortie de l’orthodoxie punk
S16-A005 — Pete Shelley, anti-virtuosité et minimalisme ironique
S16-A006 — Martin Hannett avant Joy Division : production à vérifier dans sources discographiques
S16-A007 — « Boredom » comme seuil entre punk et post-punk
S16-A008 — Buzzcocks / Magazine / Joy Division : voisinage mancunien, non filiation simple
S16-A009 — Mémoire web et canonisation de « Boredom »
S16-A010 — Usage final : comparer la sécheresse critique de « Boredom » et la gravité poétique de Joy Division sans les fusionner
```

Bloc d’usage recommandé :

```yaml
source_id: S16
source_label: "S16 — Songfacts, Boredom by Buzzcocks, page consultée 2026"
source_author: "Songfacts"
source_title: "Boredom by Buzzcocks"
preuve: "source web secondaire/tertiaire / orientation sur une chanson de Buzzcocks"
usage: "Buzzcocks ; Boredom ; Spiral Scratch ; Howard Devoto ; Pete Shelley ; New Hormones ; Martin Hannett ; Manchester punk ; DIY ; anti-virtuosité ; minimalisme ; seuil punk/post-punk"
prudence: "ne pas utiliser comme source primaire ; vérifier crédits, dates, paroles, production, anecdotes et réception dans des sources discographiques, journalistiques ou testimoniales robustes"
```

Formules utilisables :

```text
source web d’orientation
jalon punk mancunien
anti-virtuosité punk
ennui comme principe critique
minimalisme ironique
seuil punk / post-punk
éthique DIY de Spiral Scratch
contrepoint à Joy Division
mémoire web des chansons punk
```

Formules à proscrire :

```text
Songfacts prouve
S16 établit définitivement
Boredom explique Joy Division
Buzzcocks et Joy Division relèvent du même idiome
le punk mancunien mène mécaniquement au post-punk
les paroles peuvent être reprises depuis Songfacts
Songfacts suffit pour les crédits discographiques
```
