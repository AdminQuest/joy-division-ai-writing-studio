# Rapport — Toilettage canonique du registre des chansons

```yaml
type_unite: cleanup_report
scope: "apps/song-register ; registers/songs/*.md ; chansons atomisées"
status: "integrated_conservative_first_pass"
canon_file: "registers/songs/00_canonical_joy_division_songs.md"
app_files:
  - "apps/song-register/index.html"
  - "apps/song-register/app.js"
  - "apps/song-register/style.css"
audit_tool: "tools/audit_song_canon.py"
```

## 1. Objectif

Le registre public des chansons doit afficher un menu déroulant limité aux chansons originales Joy Division / Warsaw, en agrégeant les variantes, démos, répétitions, Peel/BBC, live et mentions atomisées sous un titre canonique.

Le registre ne doit plus présenter comme chansons Joy Division des titres contextuels issus des sources : Buzzcocks, New Order hors corpus Joy Division, reprises, titres de groupes voisins, objets de comparaison ou simples chansons citées dans les atomes.

## 2. Décision canonique

Un fichier canonique interne est créé :

```text
registers/songs/00_canonical_joy_division_songs.md
```

Il contient 50 titres affichables :

- œuvre originale complète Joy Division ;
- corpus Warsaw / pré-Joy Division ;
- quelques démos et répétitions utiles ;
- Peel/BBC, inédits et instrumentaux ;
- deux cas-limites terminaux : `Ceremony` et `In a Lonely Place`.

Les variantes sont rattachées au titre canonique : par exemple `Chance` à `Atmosphere`, `They Walked in Line` à `Walked in Line`, `24 Hours` à `Twenty Four Hours`, `Sound of Music` à `The Sound of Music`.

## 3. Exclusions contrôlées

Le canon interne exclut explicitement de l’affichage principal :

```text
Blue Monday
Boredom
Love Battery
Louie Louie
Sister Ray
The Passenger
```

Ces titres peuvent rester dans les atomes comme contexte, comparaison ou relation, mais ne doivent pas apparaître comme œuvres Joy Division dans le menu déroulant.

## 4. Modification de l’application

L’application `apps/song-register/` est modifiée comme suit :

- ajout d’un menu déroulant `Chanson canonique` ;
- chargement prioritaire du fichier canonique ;
- affichage de 50 cartes canoniques, et non de toutes les entrées `song` trouvées dans le repo ;
- agrégation des mentions atomisées rattachées au titre canonique ;
- conservation des filtres source, type, thème, chapitre ;
- export CSV du registre canonique plutôt que de la liste brute ;
- indication du nombre de mentions rattachées, exclues ou hors canon.

## 5. Toilettage des fichiers `registers/songs/*.md`

La passe est volontairement conservatoire : les fichiers sources existants ne sont pas supprimés ni réécrits massivement. Le nettoyage se fait par couche canonique.

Cette méthode évite de perdre des informations utiles dans les sources, tout en empêchant les faux positifs d’apparaître dans l’interface publique comme œuvres Joy Division.

Les prochaines passes pourront ensuite modifier les fichiers spécialisés en ajoutant, quand nécessaire :

```yaml
canonical_song_id: JD-SONG-020
canonical_song: "Transmission"
variant_type: "Peel | BBC | live | demo | studio | lyrics_divergence"
exclude_from_song_menu: false
```

ou, pour les faux positifs :

```yaml
exclude_from_song_menu: true
exclusion_reason: "titre contextuel / reprise / New Order hors corpus Joy Division"
```

## 6. Outil d’audit

Un outil d’audit est ajouté :

```text
tools/audit_song_canon.py
```

Il lit le canon, scanne les chansons générées et les fichiers Markdown, puis signale :

- les titres canoniques sans mention rattachée ;
- les titres explicitement exclus rencontrés dans les sources ;
- les titres possibles hors canon à inspecter.

L’outil ne réécrit rien. Il sert à guider les passes ultérieures de toilettage.

## 7. Prudences

Le canon interne n’est pas un jugement discographique définitif. Il sert à stabiliser l’interface de travail.

Les reprises peuvent rester dans des atomes ou des relations si elles servent l’histoire du groupe, mais elles ne doivent pas être affichées comme chansons originales Joy Division.

`Ceremony` et `In a Lonely Place` restent inclus comme cas-limites, car le repo les utilise comme objets de transition Joy Division / New Order.

Les titres Warsaw issus de démos et répétitions restent volontairement limités, afin de ne pas transformer le menu en inventaire bootleg exhaustif.
