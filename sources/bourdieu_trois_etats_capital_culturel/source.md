# S19 — Source canonique — Bourdieu, « Les trois états du capital culturel », 1979

```yaml
id: S19
source_id: S19
type_unite: source
source_label: "S19 — Bourdieu, Les trois états du capital culturel, 1979"
source_short_title: "Bourdieu, Les trois états du capital culturel, 1979"
auteur: "Pierre Bourdieu"
titre: "Les trois états du capital culturel"
annee: "1979"
dossier_source: "sources/bourdieu_trois_etats_capital_culturel/"
fichier_source_original: "arss_0335-5322_1979_num_30_1_2654.pdf"
pages_pdf_exemplaire: "7 pages ; article p. 3-6 de la revue"
statut: "source canonique refixée"
```

## 1. Identifiant canonique

```text
S19
```

## 2. Libellé source

```text
S19 — Bourdieu, Les trois états du capital culturel, 1979
```

## 3. Dossier source

```text
sources/bourdieu_trois_etats_capital_culturel/
```

## 4. Référence complète

BOURDIEU, Pierre, « Les trois états du capital culturel », *Actes de la recherche en sciences sociales*, vol. 30, novembre 1979, « L’institution scolaire », p. 3-6. DOI : 10.3406/arss.1979.2654. Version de travail : fichier Persée `arss_0335-5322_1979_num_30_1_2654.pdf`, généré le 22 février 2024, 7 p.

Note bibliographique interne : la page 1 du PDF identifie clairement l’article, la revue, le volume, le numéro, la date, la pagination et le DOI. Les pages 4-7 du PDF contiennent le texte de l’article, correspondant aux pages 3-6 de la revue.

## 5. Décision canonique

S19 désigne exclusivement l’article de Pierre Bourdieu « Les trois états du capital culturel », publié en 1979 dans *Actes de la recherche en sciences sociales*.

La source ne désigne pas l’ensemble de l’œuvre de Bourdieu, ni *La Distinction*, ni *La Reproduction*, ni une théorie générale de la culture populaire. Elle fixe un article théorique court sur le capital culturel sous trois formes :

```text
capital culturel incorporé
capital culturel objectivé
capital culturel institutionnalisé
```

S19 doit être utilisée comme source conceptuelle pour comprendre la transmission des dispositions, l’appropriation des biens culturels, les conditions sociales de la compétence culturelle, la transformation du capital économique en capital culturel, le rôle du temps d’acquisition, les titres scolaires et les stratégies de reproduction.

## 6. Entrée à ajouter dans `data/registre.json`

L’entrée complète est fixée dans :

```text
sources/bourdieu_trois_etats_capital_culturel/registre_patch_s19.json
```

Elle est appliquée par :

```text
python3 tools/apply_s19_registre_patch.py
```

## 7. Fonction dans le livre

S19 sert à penser les conditions sociales d’accès aux biens culturels et aux avant-gardes. Dans le projet Joy Division, elle n’explique pas le groupe ; elle permet de qualifier les différences d’appropriation entre possession matérielle, compétence incorporée et reconnaissance institutionnelle.

La source est particulièrement utile pour :

- le chapitre 2, si l’on analyse les trajectoires de formation, les capitaux scolaires, les autodidaxies, les bibliothèques, les goûts et les conditions sociales de l’appropriation culturelle ;
- le chapitre 4, pour penser Ian Curtis comme lecteur sans naturaliser son « don » ou son intensité poétique ;
- le chapitre 5, pour distinguer la possession d’objets culturels, leur appropriation symbolique et la compétence requise pour lire les signes graphiques ;
- le chapitre 10, pour traiter la circulation des biens culturels Joy Division, leur reproduction marchande et les écarts de compétence dans l’appropriation ;
- le chapitre 14, pour analyser la patrimonialisation, la légitimation et les profits symboliques attachés au capital culturel Joy Division.

## 8. Risques de confusion

1. Ne pas utiliser S19 comme source directe sur Joy Division, Manchester, Factory Records ou le post-punk.
2. Ne pas réduire le capital culturel à la culture générale ou au goût individuel.
3. Ne pas confondre capital culturel incorporé, capital culturel objectivé et capital culturel institutionnalisé.
4. Ne pas traiter l’article comme une simple typologie abstraite : Bourdieu l’inscrit dans une théorie des inégalités scolaires, de la transmission familiale et des stratégies de reproduction.
5. Ne pas transformer le « don » artistique ou l’« aptitude » en qualité naturelle ; S19 sert précisément à rompre avec cette vision.
6. Ne pas employer S19 pour juger la valeur esthétique de Joy Division. La source éclaire les conditions sociales d’appropriation, non la qualité de l’œuvre.
7. Ne pas confondre appropriation matérielle et appropriation symbolique : posséder un disque, un livre, une affiche ou une pochette ne signifie pas maîtriser les codes nécessaires à leur lecture.
8. Ne pas utiliser S19 pour remplacer des sources de sociologie des sous-cultures, de fan studies ou d’histoire de la musique. Croiser avec Hebdige, Hall, Reynolds, Frith, Bourdieu ailleurs si nécessaire, et les sources internes du projet.
9. Ne pas extraire des citations longues sans vérifier la pagination PDF et la pagination revue.
10. Ne pas plaquer mécaniquement la théorie scolaire de Bourdieu sur tous les usages culturels de Joy Division ; adapter l’usage au problème traité.

## 9. Consignes pour les futurs atomes

Les futurs atomes S19 doivent être sélectifs et orientés vers les usages réels du manuscrit. Ils doivent éviter l’extraction massive de théorie générale.

```text
S19-A001 — S19 comme source conceptuelle, non comme source directe sur Joy Division
S19-A002 — Le capital culturel comme hypothèse contre l’idéologie du don naturel
S19-A003 — Capital culturel incorporé : dispositions durables, temps d’acquisition, habitus
S19-A004 — Le temps d’acquisition comme lien entre capital économique et capital culturel
S19-A005 — Transmission domestique et dissimulation de l’héritage culturel
S19-A006 — Capital culturel objectivé : biens culturels, supports matériels, appropriation symbolique
S19-A007 — Possession matérielle et maîtrise des instruments d’appropriation
S19-A008 — Capital culturel institutionnalisé : titre scolaire, certification, convertibilité économique
S19-A009 — Valeur de rareté, inflation des titres et stratégies de reconversion
S19-A010 — Usage Joy Division : disques, livres, images et signes comme biens objectivés à appropriation différenciée
S19-A011 — Usage Curtis : ne pas naturaliser le lecteur-poète, mais penser dispositions, temps, acquisition et autodidaxie
S19-A012 — Usage final : capital culturel Joy Division entre objet, compétence, légitimation et patrimonialisation
```

Bloc d’usage recommandé :

```yaml
source_id: S19
source_label: "S19 — Bourdieu, Les trois états du capital culturel, 1979"
source_author: "Pierre Bourdieu"
source_title: "Les trois états du capital culturel"
preuve: "source théorique / sociologie de la culture, capital culturel, transmission, appropriation, titres scolaires, reproduction sociale"
usage: "capital culturel incorporé ; capital culturel objectivé ; capital culturel institutionnalisé ; habitus ; transmission domestique ; appropriation symbolique ; biens culturels ; titres scolaires ; distinction entre possession et compétence ; patrimonialisation culturelle"
prudence: "ne pas utiliser comme source directe sur Joy Division ; distinguer typologie théorique et application au corpus ; croiser les usages musicaux et sous-culturels avec les sources spécialisées"
```

Formules utilisables :

```text
capital culturel incorporé
capital culturel objectivé
capital culturel institutionnalisé
transmission domestique du capital culturel
avoir devenu être
propriété faite corps
temps d’acquisition
appropriation matérielle
appropriation symbolique
instruments d’appropriation
capital culturel comme capital symbolique méconnu
valeur de rareté
convertibilité entre capital culturel et capital économique
```

Formules à proscrire :

```text
Bourdieu explique Joy Division
le capital culturel est la culture générale
posséder un disque équivaut à le comprendre
Ian Curtis a du talent naturellement
le capital culturel suffit à expliquer la création
S19 remplace les sources musicales ou biographiques
S19 prouve la valeur esthétique de Joy Division
```
