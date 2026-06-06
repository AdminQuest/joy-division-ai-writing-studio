# M2.10.2 - Campagne d'observation des sources longues

## 1. Objet de la campagne

Cette campagne existe pour observer le comportement reel du prototype
`tools/m2_integrate_source.py` sur des sources longues representatives du
corpus Joy Division.

Le prototype a deja ete specifie, implemente, teste, documente et evalue par un
premier retour d'usage. Ce retour a confirme sa valeur documentaire pour une
pre-validation courte, mais il a aussi laisse plusieurs points insuffisamment
observes :

- detection de proximite ;
- editions ;
- reeditions ;
- traductions ;
- faux positifs ;
- faux negatifs ;
- qualite des propositions de dossier source ;
- qualite des propositions de `Sxx`.

La campagne cherche a mesurer si les diagnostics produits sont utiles avant une
integration documentaire longue.

Elle ne cherche pas a demontrer :

- la qualite historiographique des sources ;
- la pertinence d'une atomisation ;
- la validite de citations ;
- la creation correcte d'une source canonique ;
- la suffisance d'une future PR ;
- la superiorite d'une heuristique de proximite.

Le prototype reste en lecture seule. La campagne n'implique aucune modification
du registre, des schemas, des controles M1 ou du corpus.

## 2. Familles de cas a observer

### Cas A - Source reellement nouvelle

Source absente de `data/registre.json`.

Objectif :

- observer une decision `pre-validee` ;
- verifier que le `Sxx` propose est lisible comme identifiant probable et non
  attribue ;
- verifier que le dossier source propose est comprehensible ;
- relever si une reserve de proximite apparait alors que la source semble
  nouvelle.

Ce cas sert a reperer les faux positifs de proximite.

### Cas B - Source deja presente

Meme auteur, meme titre et meme edition qu'une source canonique existante.

Objectif :

- observer une decision `non pre-validee` ;
- verifier que le bloquant de source deja presente pointe vers le bon `Sxx` ;
- verifier que le dossier source canonique est repris lorsqu'il existe ;
- relever les cas ou le prototype proposerait a tort un nouveau `Sxx`.

Ce cas sert a mesurer la detection des doublons certains.

### Cas C - Reedition

Meme auteur et meme titre qu'une source existante, mais annee, edition ou tirage
different.

Objectif :

- observer une decision `pre-validee avec reserve` ;
- verifier que la reserve signale bien une autre edition ou reedition possible ;
- verifier que le diagnostic n'est ni un blocage automatique ni une acceptation
  silencieuse ;
- relever si le dossier source propose permet de comprendre le rattachement
  possible a une source existante.

Ce cas sert a mesurer la qualite de l'arbitrage humain prepare par le prototype.

### Cas D - Traduction

Version traduite d'une source existante ou source existante presente dans une
autre langue.

Objectif :

- observer si le prototype produit une reserve ou une proposition nouvelle ;
- verifier si le titre traduit reste rapproche de la source canonique ;
- relever les faux negatifs lorsque la traduction est traitee comme une source
  completement nouvelle ;
- relever les faux positifs lorsque deux sources distinctes sont rapprochees a
  tort.

Ce cas est important parce que le prototype ne possede pas de logique
linguistique dediee.

### Cas E - Metadonnees imparfaites

Source candidate avec titre incomplet, annee approximative, reference partielle
ou auteur presente sous une forme bibliographique differente.

Objectif :

- observer la decision produite ;
- verifier si les bloquants concernent uniquement les metadonnees vraiment
  absentes ;
- verifier si les reserves restent actionnables ;
- relever les cas ou une source proche connue n'est pas detectee.

Ce cas sert a observer le comportement du prototype dans les conditions d'un
premier reperage documentaire, avant qualification complete.

## 3. Sources candidates recommandees

Les sources ci-dessous sont presentes dans `data/registre.json` et peuvent
servir de points d'observation. La campagne ne lance pas encore l'analyse : elle
definit seulement les candidats a tester.

| Source | Auteur ou responsable | Titre | Usage recommande |
| --- | --- | --- | --- |
| `S90` | Mark Fisher | `Ghosts of My Life: Writings on Depression, Hauntology and Lost Futures` | Cas B, source deja presente avec dossier source canonique. |
| `S91` | Simon Reynolds | `Retromania: Pop Culture's Addiction to Its Own Past` | Cas C, autre edition ou reedition possible. |
| `S72` | Simon Reynolds | `Rip It Up and Start Again: Postpunk 1978-1984` | Cas C ou D, source avec annee `2005/2006` utile pour observer editions et variantes. |
| `S74` | Mick Middles | `From Joy Division to New Order` | Cas B ou E, source biographique sans dossier source canonique declare. |
| `S76` | Mick Middles ; Lindsay Reade | `Torn Apart: The Life of Ian Curtis` | Cas B ou C, source biographique proche d'autres ouvrages sur Ian Curtis. |
| `S41` | Peter Hook | `Unknown Pleasures: Inside Joy Division` | Cas B ou C, source memoire avec edition potentielle a observer. |
| `S10` | Bernard Sumner | `Chapter and Verse: New Order, Joy Division and Me` | Cas C, annee `2014/2015` utile pour observer edition ou publication differente. |
| `S45` | Deborah Curtis | `Touching from a Distance: Ian Curtis and Joy Division` | Cas B, C ou D, source biographique susceptible d'exister en traductions ou reeditions. |
| `S75` | Chris Ott | `Joy Division's Unknown Pleasures` | Cas B ou E, titre court avec risque de proximite avec `Unknown Pleasures`. |
| `S46` | Mark Johnson ; David Lees ; Paul Morley ; Jon Wozencroft | `An Ideal for Living: An History of Joy Division` | Cas B ou E, source collective avec auteur multiple. |
| `S47` | Mike West | `Joy Division` | Cas E, titre tres court utile pour observer faux positifs de proximite. |
| `S09` | Kevin Cummins | `Joy Division` | Cas E, titre tres court et auteur distinct de `S47`. |
| `S79` | Ian Curtis | `So This Is Permanence: Joy Division Lyrics and Notebooks` | Cas B ou C, source avec dossier canonique et edition possible. |
| `S26` | Gavin Butt ; Kodwo Eshun ; Mark Fisher (dir.) | `Post-Punk Then and Now` | Cas B ou E, source collective avec directeur et dossier canonique. |
| `S93` | James Parker | `Simon Reynolds, Retromania and the Atemporality of Contemporary Pop` | Cas E, source critique proche de `S91` sans etre la meme source. |
| `S94` | James Weissinger | `Retromania: Pop Culture's Addiction to Its Own Past (Book Review)` | Cas E, critique de livre susceptible de provoquer une proximite avec `S91`. |

Pour le cas A, la source candidate doit etre une source reelle absente du
registre au moment de la campagne. Elle doit etre choisie manuellement avant
execution et documentee comme absente de `data/registre.json`.

Pour le cas D, la traduction candidate doit etre choisie a partir d'une source
existante du registre. Les candidats les plus pertinents sont `S45`, `S72`,
`S90` et `S91`, car leurs titres, editions ou circulations peuvent produire des
rapprochements utiles a observer.

## 4. Metriques observees

Chaque execution de la campagne doit relever les elements suivants, sans
produire de correction automatique :

| Metrique | Observation attendue |
| --- | --- |
| `decision` | Decision exacte produite : `pre-validee`, `pre-validee avec reserve` ou `non pre-validee`. |
| `bloquants` | Liste des bloquants et pertinence documentaire du blocage. |
| `reserves` | Liste des reserves et clarte de l'arbitrage demande. |
| `informations` | Utilite des informations, notamment `Sxx` probable ou existant et dossier source probable. |
| `Sxx propose` | Coherence du `Sxx` affiche comme existant ou probable. |
| `dossier source propose` | Lisibilite du slug et reprise correcte d'un dossier canonique lorsqu'il existe. |
| `qualite du diagnostic` | Diagnostic actionnable ou non pour un humain avant integration. |
| `temps d'analyse` | Temps necessaire pour preparer les parametres, executer le prototype et comprendre la sortie. |
| `risque observe` | Faux positif, faux negatif, ambiguite ou absence de probleme. |

Les observations doivent etre qualitatives. La campagne ne definit pas de
seuils chiffres.

## 5. Faux positifs

Dans le contexte du prototype, un faux positif est un diagnostic de proximite ou
de blocage qui signale un risque documentaire alors que la source candidate
semble reellement distincte.

Exemples :

- source nouvelle mais decision `pre-validee avec reserve` sans proximite
  documentaire pertinente ;
- source nouvelle mais rapprochement avec une autre source uniquement parce que
  le titre contient `Joy Division` ;
- critique, compte rendu ou article rapproche a tort du livre qu'il commente ;
- dossier source propose qui entretient une confusion avec une source existante.

Un faux positif n'est pas necessairement une erreur grave : il peut etre
acceptable si la reserve reste claire et permet une validation humaine rapide.

## 6. Faux negatifs

Dans le contexte du prototype, un faux negatif est l'absence de signalement d'un
risque documentaire reel.

Exemples :

- reedition consideree comme source completement nouvelle ;
- traduction consideree comme source completement nouvelle ;
- source deja presente non detectee a cause d'une variante d'auteur ;
- source deja presente non detectee a cause d'un titre incomplet ;
- dossier source probable propose alors qu'un dossier canonique existant devrait
  etre repris.

Un faux negatif est plus critique qu'un faux positif lorsque le prototype
encourage la creation probable d'un nouveau `Sxx` alors qu'un rattachement ou un
arbitrage aurait du etre signale.

## 7. Criteres de reussite

La campagne pourra etre consideree comme suffisante si elle couvre au minimum :

- une source reellement nouvelle ;
- une source deja presente ;
- une reedition ou edition alternative ;
- une traduction ou variante linguistique ;
- un cas de metadonnees imparfaites ;
- un titre court ou generique susceptible de produire un faux positif ;
- une source critique proche d'une source primaire ou bibliographique.

Les criteres qualitatifs sont :

- aucun blocage critique du prototype pendant les essais ;
- decisions relisibles et coherentes avec les familles de cas ;
- bloquants reserves et informations clairement separables ;
- propositions de `Sxx` et de dossier source comprehensibles comme propositions
  non attribuees ;
- faux positifs et faux negatifs documentes ;
- limites observees suffisamment precises pour orienter une decision
  d'evolution.

La campagne n'est pas suffisante si elle ne teste que des cas evidents de source
deja presente ou de source nouvelle.

## 8. Decision attendue apres campagne

Apres la campagne, la decision devra choisir explicitement parmi trois options.

### Stabilisation

Condition :

- les diagnostics sont globalement coherents ;
- les faux positifs restent faibles ou utiles ;
- les faux negatifs ne concernent pas les cas documentaires majeurs ;
- la sortie est deja suffisante pour guider une validation humaine.

Effet attendu :

- conserver le prototype en lecture seule ;
- documenter les limites ;
- ne pas ajouter de nouvelle fonctionnalite immediate.

### Amelioration

Condition :

- les diagnostics sont utiles mais plusieurs faux positifs ou faux negatifs
  recurrent apparaissent ;
- les editions, reeditions ou traductions sont mal signalees ;
- les propositions de dossier source pretent a confusion ;
- les messages ne suffisent pas a guider l'arbitrage humain.

Effet attendu :

- definir une amelioration ciblee du prototype ;
- rester dans le perimetre M2.3 ;
- ne pas ouvrir d'atomisation automatique.

### Extension fonctionnelle

Condition :

- les diagnostics sont stables sur toutes les familles de cas ;
- les limites restantes sont documentees et acceptables ;
- la pre-validation de source longue est suffisamment fiable pour preparer une
  etape suivante.

Effet attendu :

- envisager une extension preparatoire du flux source longue ;
- documenter l'extension avant implementation ;
- conserver la validation humaine obligatoire.

Decision proposee avant execution :

```text
La campagne doit d'abord permettre de choisir entre stabilisation et
amelioration.

L'extension fonctionnelle ne doit etre envisagee que si les faux positifs et
faux negatifs observes restent limites et documentables.
```
