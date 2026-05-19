# S21 — Source canonique — Manchester Digital Music Archive, « City Fun: The Hidden History of Manchester's Favourite Fanzine »

```yaml
id: S21
source_id: S21
type_unite: source
source_label: "S21 — MDMArchive, City Fun: The Hidden History of Manchester's Favourite Fanzine, page consultée 2026"
source_short_title: "MDMArchive, City Fun: The Hidden History, page consultée 2026"
auteur: "Manchester Digital Music Archive"
titre: "City Fun: The Hidden History of Manchester's Favourite Fanzine"
annee: "s.d. / page consultée 2026"
dossier_source: "sources/mdmarchive_city_fun_hidden_history/"
source_url: "https://www.mdmarchive.co.uk/exhibition/city-fun:-the-hidden-history-of-manchester's-favourite-fanzine"
statut: "source canonique refixée ; exposition web / archive numérique ; contenu à vérifier par captures et notices d’items"
```

## 1. Identifiant canonique

```text
S21
```

## 2. Libellé source

```text
S21 — MDMArchive, City Fun: The Hidden History of Manchester's Favourite Fanzine, page consultée 2026
```

## 3. Dossier source

```text
sources/mdmarchive_city_fun_hidden_history/
```

## 4. Référence complète

MANCHESTER DIGITAL MUSIC ARCHIVE, « City Fun: The Hidden History of Manchester's Favourite Fanzine », *Manchester Digital Music Archive*, exposition web, URL : https://www.mdmarchive.co.uk/exhibition/city-fun:-the-hidden-history-of-manchester's-favourite-fanzine, page consultée le 19 mai 2026.

Note bibliographique interne : la page cible est une exposition web de Manchester Digital Music Archive consacrée à *City Fun*, fanzine mancunien. La page doit être traitée comme une source archivistique numérique et curatoriale. Elle peut inclure des notices, scans, images, commentaires, crédits et éléments éditoriaux. Comme les pages MDMArchive sont susceptibles d’évoluer et de comporter des items individuels, les citations finales devront être rattachées autant que possible à l’item précis, à sa légende, à sa date, à son crédit et à sa capture.

## 5. Décision canonique

S21 désigne exclusivement l’exposition web MDMArchive « City Fun: The Hidden History of Manchester's Favourite Fanzine ».

S21 ne désigne pas l’intégralité du fanzine *City Fun*, sauf si l’exposition donne accès à des scans complets clairement identifiés. S21 ne désigne pas non plus l’article universitaire de David Wilkinson sur *City Fun*, qui reste **S22**. S21 est la source archivistique / curatoriale ; S22 est la source secondaire interprétative.

S21 est donc à traiter comme un point d’accès primaire ou quasi primaire à des objets du fanzine : couvertures, pages scannées, notices, récits curatoriaux, noms de contributeurs, mémoire matérielle et circulation locale. Lorsque l’exposition présente un scan d’un numéro de *City Fun*, le scan peut servir de source primaire pour cet item précis, mais la notice d’exposition reste une médiation archivistique.

## 6. Entrée à ajouter dans `data/registre.json`

L’entrée complète est fixée dans :

```text
sources/mdmarchive_city_fun_hidden_history/registre_patch_s21.json
```

Elle est appliquée par :

```text
python3 tools/apply_s21_registre_patch.py
```

## 7. Fonction dans le livre

S21 sert à documenter *City Fun* comme objet médiatique local, matériel, collectif et contre-culturel. La source est utile pour passer de l’analyse secondaire de Wilkinson à des traces concrètes : images du fanzine, mise en page, ton, graphisme, ironie, réseau de contributeurs, sociabilité de la scène et inscription locale.

La source est particulièrement utile pour :

- le chapitre 2, si l’on situe les médias, fanzines, lieux et acteurs de la scène punk / post-punk mancunienne ;
- le chapitre 3, si l’on analyse les discours locaux sur les groupes, les concerts et l’écoute en train de se faire ;
- le chapitre 7, si l’on étudie la culture matérielle, les supports imprimés, le DIY, le photocopié et les économies pauvres de publication ;
- le chapitre 8, si l’on traite les médiations, critiques, fanzines et conflits de réception ;
- le chapitre 9, si l’on aborde Manchester comme scène locale, réseau social et infrastructure culturelle ;
- le chapitre 14, si l’on analyse la patrimonialisation numérique de la contre-culture mancunienne.

## 8. Risques de confusion

1. Ne pas confondre S21 et S22 : S21 est l’exposition web / corpus archivistique MDMArchive ; S22 est l’article universitaire de David Wilkinson.
2. Ne pas citer l’exposition comme si elle était un numéro complet de *City Fun* sans identifier l’item exact.
3. Ne pas traiter MDMArchive comme source strictement neutre : c’est une archive communautaire et curatoriale, avec sélection, mise en récit et patrimonialisation.
4. Ne pas faire de *City Fun* une source directe sur Joy Division sans vérifier que l’item cité parle effectivement de Joy Division, Factory, Tony Wilson ou d’un acteur pertinent.
5. Ne pas confondre mémoire de scène et preuve factuelle : les notices et souvenirs doivent être croisés.
6. Ne pas oublier la matérialité du fanzine : graphisme, bricolage, photocopie, ton, mise en page, annonces, courriers et sociabilité sont aussi importants que les seules informations factuelles.
7. Ne pas confondre opposition à Factory avec histoire complète de *City Fun*. L’exposition peut montrer une diversité d’objets et de voix.
8. Ne pas citer des scans ou images sans vérifier droits, crédit, date, numéro, contributeur et contexte.
9. Ne pas utiliser S21 comme source unique sur la chronologie de *City Fun*. Croiser avec S22, les numéros originaux, les contributeurs, MDMArchive, les catalogues et les sources presse.
10. Ne pas utiliser S21 comme preuve générale sur le post-punk mancunien sans distinguer l’objet *City Fun*, la scène qu’il documente et la patrimonialisation actuelle de cette scène.

## 9. Consignes pour les futurs atomes

Les futurs atomes S21 doivent être construits item par item. Chaque atome doit préciser le type d’objet : notice d’exposition, scan de couverture, page intérieure, photographie, commentaire, témoignage, élément éditorial ou document dérivé.

```text
S21-A001 — S21 comme exposition web archivistique, non comme article universitaire
S21-A002 — City Fun comme fanzine mancunien : source primaire locale à documenter item par item
S21-A003 — Matérialité de City Fun : photocopie, graphisme, ton, bricolage, économie DIY
S21-A004 — City Fun comme réseau de contributeurs, lecteurs, lieux et scènes
S21-A005 — City Fun comme observatoire de la scène punk / post-punk en train de se faire
S21-A006 — City Fun, Factory et Tony Wilson : n’utiliser que les items explicitement concernés
S21-A007 — Liz Naylor, Cath Carroll, Andy Zero, Martin X, Neil Hargreaves : acteurs à vérifier selon les items
S21-A008 — City Fun et la critique locale : humour, satire, camp, classe, genre, politique
S21-A009 — City Fun comme objet de patrimonialisation numérique par MDMArchive
S21-A010 — Usage final : articuler S21 corpus primaire / S22 interprétation universitaire
```

Bloc d’usage recommandé :

```yaml
source_id: S21
source_label: "S21 — MDMArchive, City Fun: The Hidden History of Manchester's Favourite Fanzine, page consultée 2026"
source_author: "Manchester Digital Music Archive"
source_title: "City Fun: The Hidden History of Manchester's Favourite Fanzine"
preuve: "source archivistique numérique / exposition web ; accès curatoriel à des traces, scans et notices autour du fanzine City Fun"
usage: "City Fun ; fanzine ; Manchester post-punk ; MDMArchive ; DIY ; culture matérielle ; contre-culture locale ; scène punk/post-punk ; Factory ; Tony Wilson ; Liz Naylor ; Cath Carroll ; Andy Zero ; Martin X ; patrimonialisation numérique"
prudence: "ne pas utiliser comme source unique ; citer item précis, date, numéro, crédit et capture ; croiser avec S22 Wilkinson et les numéros originaux de City Fun"
```

Formules utilisables :

```text
source archivistique numérique
exposition web curatoriale
fanzine comme trace matérielle
City Fun comme observatoire local
mémoire communautaire de la scène
patrimonialisation numérique du post-punk mancunien
corpus primaire médiatisé
objet DIY imprimé
```

Formules à proscrire :

```text
S21 prouve tout City Fun
MDMArchive est une source neutre exhaustive
l’exposition remplace les numéros originaux
City Fun parle toujours de Joy Division
City Fun est seulement anti-Factory
S21 remplace S22
un scan sans légende suffit pour citer
la mémoire patrimoniale vaut preuve directe
```
