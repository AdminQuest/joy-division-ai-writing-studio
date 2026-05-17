# S35 — Source canonique — Morris, *Record Play Pause*, 2019

```yaml
id: S35
source_id: S35
type_unite: source
source_label: "S35 — Morris, Record Play Pause, 2019"
source_short_title: "Morris, Record Play Pause, 2019"
auteur: "Stephen Morris"
titre: "Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I"
annee: "2019"
dossier_source: "sources/morris_record_play_pause/"
editeur: "Constable"
lieu_edition: "London"
collection_ou_imprint: "Constable, an imprint of Little, Brown Book Group"
isbn: "978-1-47212-619-1"
fichier_source_original: "Stephen Morris - Record Play Pause - Confessions of a Post-Punk Percussionist.pdf"
statut: "source canonique fixée"
```

## 1. Identifiant canonique

```text
S35
```

## 2. Libellé source

```text
S35 — Morris, Record Play Pause, 2019
```

## 3. Dossier source

```text
sources/morris_record_play_pause/
```

## 4. Référence complète

MORRIS, Stephen, *Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I*, London, Constable, an imprint of Little, Brown Book Group, 2019, ISBN 978-1-47212-619-1.

Note bibliographique interne : l’exemplaire PDF indique « First published in Great Britain in 2019 by Constable ». Le livre est le volume I des mémoires de Stephen Morris. Il couvre l’enfance, Macclesfield, la formation musicale, Warsaw, Joy Division, *Unknown Pleasures*, *Closer* et la transition immédiate après la mort de Ian Curtis.

## 5. Décision canonique

S35 désigne exclusivement le livre de Stephen Morris, *Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I*, publié par Constable en 2019.

S35 ne désigne pas un chapitre isolé. Les futurs atomes devront donc être fortement sélectifs et toujours rattachés aux chapitres internes pertinents, notamment :

```text
Part 1 — Rewind
Part 2 — From Warsaw to Joy Division
Part 3 — Tomorrow’s World
```

S35 ne désigne pas *Fast Forward: Confessions of a Post-Punk Percussionist, Volume II*, qui devra recevoir un autre identifiant si ce second volume est intégré ultérieurement. S35 ne désigne pas non plus les mémoires de Peter Hook, Bernard Sumner, Deborah Curtis, Tony Wilson ou les documentaires sur Joy Division.

## 6. Fonction dans le livre

S35 est une source primaire rétrospective, testimoniale et mémorielle. Son intérêt est considérable, car Stephen Morris est à la fois acteur direct, batteur de Joy Division, témoin de la formation du groupe et observateur de l’intérieur des pratiques musicales, techniques et relationnelles.

La source est particulièrement utile pour :

- le chapitre 1, sur Macclesfield, Manchester, l’environnement social et culturel d’avant Joy Division ;
- le chapitre 2, sur la formation de Warsaw / Joy Division, les auditions, les premiers concerts, les répétitions, les noms et les lieux ;
- le chapitre 3, sur Stephen Morris, la batterie, les machines, le rapport au rythme, Can, Neu!, Jaki Liebezeit, Moe Tucker, les influences motorik et anti-virtuoses ;
- le chapitre 4, sur Ian Curtis vu par un membre du groupe, avec prudence mémorielle ;
- le chapitre 5, sur *An Ideal for Living*, le nom Joy Division et les premières controverses ;
- le chapitre 6, sur *Unknown Pleasures*, *Closer*, Hannett, Factory et les conditions de production ;
- le chapitre 12, sur la maladie de Curtis, les effets sur le groupe, les tournées et les limites de la compréhension collective ;
- le chapitre 14, sur la mémoire de Joy Division, le récit rétrospectif et le passage au mythe.

## 7. Entrée canonique pour `data/registre.json`

```json
{
  "id": "S35",
  "source_label": "S35 — Morris, Record Play Pause, 2019",
  "source_short_title": "Morris, Record Play Pause, 2019",
  "auteur": "Stephen Morris",
  "titre": "Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I",
  "annee": "2019",
  "reference_complete": "MORRIS, Stephen, Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I, London, Constable, an imprint of Little, Brown Book Group, 2019, ISBN 978-1-47212-619-1.",
  "nature": "mémoires / source primaire rétrospective / témoignage de Stephen Morris sur Macclesfield, Warsaw, Joy Division, Factory, Unknown Pleasures, Closer et les débuts de New Order",
  "statut": "source canonique fixée ; fichier PDF identifié ; volume I",
  "fiabilite": "forte comme témoignage interne et source primaire rétrospective ; à croiser pour dates, citations, séquences dialoguées, souvenirs anciens et reconstructions humoristiques",
  "usage": [
    "Stephen Morris",
    "Record Play Pause",
    "Confessions of a Post-Punk Percussionist",
    "Volume I",
    "Macclesfield",
    "King’s School",
    "Parkside",
    "batterie",
    "drumming",
    "Jaki Liebezeit",
    "Moe Tucker",
    "Neu!",
    "Can",
    "Kraftwerk",
    "Hawkwind",
    "David Bowie",
    "Warsaw",
    "Joy Division",
    "Stephen Morris batteur",
    "Ian Curtis",
    "Peter Hook",
    "Bernard Sumner",
    "Terry Mason",
    "Rob Gretton",
    "Tony Wilson",
    "Martin Hannett",
    "Factory Records",
    "An Ideal for Living",
    "Unknown Pleasures",
    "Closer",
    "The Nightmare Just After Christmas",
    "The John Peel Sessions",
    "drum machine",
    "moteur rythmique",
    "mémoire rétrospective",
    "humour autobiographique"
  ],
  "chapitres": [
    "Chapitre 1",
    "Chapitre 2",
    "Chapitre 3",
    "Chapitre 4",
    "Chapitre 5",
    "Chapitre 6",
    "Chapitre 12",
    "Chapitre 14"
  ],
  "chapitres_secondaires": [
    "Chapitre 7",
    "Chapitre 8",
    "Chapitre 10",
    "Chapitre 11",
    "Chapitre 13"
  ],
  "source_origin": [
    "PDF intégral",
    "mémoires publiées",
    "registre canonique"
  ],
  "dossier_source": "sources/morris_record_play_pause/",
  "fichier_source": "S35_morris_record_play_pause_2019.pdf",
  "fichier_source_original": "Stephen Morris - Record Play Pause - Confessions of a Post-Punk Percussionist.pdf",
  "lieu_edition": "London",
  "editeur": "Constable",
  "imprint": "Little, Brown Book Group",
  "isbn": "978-1-47212-619-1",
  "pages_utiles": "livre complet ; parties internes à distinguer lors de l’atomisation",
  "niveau_preuve": "source primaire rétrospective / témoignage interne / mémoire autobiographique",
  "arbitrage": "S35 référence exclusivement Stephen Morris, Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I, Constable, 2019. Ne pas confondre avec Fast Forward, Volume II, ni avec les mémoires de Peter Hook ou Bernard Sumner.",
  "prudence": "Traiter S35 comme témoignage interne de première importance mais rétrospectif, reconstruit, littéraire et humoristique. Croiser les dates, les dialogues, les souvenirs d’enfance, les scènes de concerts, les diagnostics médicaux, les responsabilités individuelles et les citations exactes avec S41, S45, S46, S47, S75, S76, Discogs, sources Factory et presse contemporaine. Ne pas transformer les souvenirs de Morris en chronologie souveraine sans contrôle externe."
}
```

## 8. Risques de confusion

1. Ne pas confondre Stephen Morris avec « Steven Morris » : la graphie canonique est Stephen Morris.
2. Ne pas confondre *Record Play Pause* avec *Fast Forward*, volume II des mémoires de Morris.
3. Ne pas confondre S35 avec S41, Peter Hook, *Unknown Pleasures: Inside Joy Division*.
4. Ne pas confondre S35 avec les mémoires de Bernard Sumner, Deborah Curtis ou les récits de Tony Wilson.
5. Ne pas utiliser S35 comme source neutre ou exhaustive : c’est un témoignage interne, précieux mais subjectif.
6. Ne pas reprendre sans contrôle les dialogues reconstruits, les scènes humoristiques et les souvenirs d’enfance.
7. Ne pas faire de S35 une source médicale principale sur Ian Curtis ou sur les crises d’épilepsie ; croiser avec Deborah Curtis, Hook, sources médicales disponibles et chronologies externes.
8. Ne pas utiliser S35 seul pour trancher les crédits de production, la chronologie exacte des enregistrements, les dates de concerts ou les responsabilités dans les décisions de management.
9. Ne pas réduire S35 à Joy Division : la première partie sur Macclesfield, l’enfance, les sons, les objets, les médias, les disques et les instruments nourrit fortement le contexte esthétique et social.
10. Ne pas atomiser mécaniquement tout le livre : privilégier les nœuds critiques, les passages relationnels et les scènes qui modifient une chaîne argumentative.

## 9. Consignes pour les futurs atomes

Les futurs atomes S35 doivent être sélectifs. Le livre est long, narratif et riche en anecdotes : l’objectif n’est pas d’extraire tout le matériau, mais d’isoler les nœuds historiographiques et relationnels.

Atomes prioritaires recommandés :

```text
S35-A001 — S35 comme témoignage interne rétrospectif, non chronologie souveraine
S35-A002 — Macclesfield : enfance, Parkside, industries, ennui et imaginaire technique
S35-A003 — Le rapport précoce de Morris au rythme, à la radio et aux objets sonores
S35-A004 — Hawkwind, Bowie, krautrock : matrices pré-punk du batteur
S35-A005 — Moe Tucker, Jaki Liebezeit, Neu!, Can : anti-virtuosité et répétition
S35-A006 — Du clarinetiste récalcitrant au batteur : choix de la batterie comme médium
S35-A007 — Warsaw : audition, intégration de Morris et stabilisation du groupe
S35-A008 — Terry Mason, répétitions, premiers concerts et logistique interne
S35-A009 — Premières chansons : émergence du répertoire et rôle du rythme
S35-A010 — *An Ideal for Living* : autoproduction, son, image et perception interne
S35-A011 — Rob Gretton : management, organisation et changement de régime
S35-A012 — Tony Wilson / Factory : médiation télévisuelle, label et ethos
S35-A013 — Martin Hannett : studio, son, tensions et transformation du groupe
S35-A014 — *Unknown Pleasures* : enregistrement, réception interne, écart entre scène et disque
S35-A015 — Maladie de Curtis : ce que le groupe comprend, ne comprend pas, ou comprend trop tard
S35-A016 — *Closer* : studio, atmosphère, fatigue, intensité et après-coup
S35-A017 — Mort de Curtis et recomposition : de Joy Division à New Order
S35-A018 — Morris narrateur : humour, distance, mémoire et anti-héroïsation
```

Bloc d’usage recommandé :

```yaml
source_id: S35
source_label: "S35 — Morris, Record Play Pause, 2019"
article_author: "Stephen Morris"
book_title: "Record Play Pause: Confessions of a Post-Punk Percussionist, Volume I"
proof_level: "source primaire rétrospective / témoignage interne"
usage: "Macclesfield, batterie, influences musicales, Warsaw, Joy Division, Factory, Hannett, Unknown Pleasures, Closer"
prudence: "témoignage subjectif, humoristique, reconstruit ; croiser les faits, dates, dialogues et séquences médicales"
```

Formules utilisables :

```text
mémoire interne de Stephen Morris
batteur comme témoin des structures rythmiques
Macclesfield comme matrice d’ennui et d’imaginaire technique
anti-virtuosité comme discipline rythmique
Morris entre répétition motorik et humour autobiographique
la batterie comme médium de simplicité et de contrainte
Joy Division vu depuis l’arrière du groupe
Factory et Hannett comme changement de régime sonore
l’écart entre scène, studio et mémoire rétrospective
```

Formules à proscrire :

```text
S35 prouve définitivement la chronologie complète de Joy Division
Morris dit donc la vérité objective du groupe
Record Play Pause remplace Peter Hook ou Deborah Curtis
S35 suffit à documenter la maladie de Ian Curtis
Les dialogues rapportés sont des verbatims certains
Stephen Morris est un narrateur neutre
Record Play Pause couvre toute l’histoire de New Order
Fast Forward est inclus dans S35
La mémoire humoristique de Morris peut être lue sans garde-fou
```
