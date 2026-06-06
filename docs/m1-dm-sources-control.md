# Cadrage du contrôle M1 DM -> sources

## 1. Pourquoi un contrôle DM -> sources ?

Le contrôle `DM -> sources` doit vérifier que les documents maîtres restent reliés aux sources documentaires canoniques qu'ils mobilisent. Il complète les contrôles M1 déjà disponibles sans les remplacer.

`DM -> atomes` vérifie l'ancrage minimal des documents maîtres dans les unités documentaires exportées. Il répond à la question : les identifiants d'atomes visibles dans un document maître existent-ils dans `exports/generated/atoms.json` ?

`DM -> registres` vérifie la cohérence minimale entre les identifiants de registres visibles dans les documents maîtres et les exports de registres P0. Il répond à la question : les personnes, chansons, citations, événements chronologiques, concerts et sessions visibles sont-ils retrouvés dans les exports concernés ?

`DM -> sources` répond à une question différente : les sources citées ou mobilisées dans un document maître correspondent-elles à des sources canoniques connues du dépôt ?

Le besoin documentaire couvert est la traçabilité de la preuve source au niveau du document maître. Les documents maîtres ne sont pas des sources et ne doivent pas devenir des preuves autonomes. Le contrôle doit donc vérifier que la liste des sources mobilisées par un document maître reste rattachable au registre canonique des sources, sans conclure à la validité de chaque affirmation rédactionnelle.

Risques documentaires adressés :

- source mentionnée dans un document maître mais absente du registre canonique ;
- source inconnue ou mal identifiée ;
- source orpheline, présente dans un document maître mais non rattachable à un objet source conservé ;
- source mentionnée mais non déclarée dans les métadonnées ou la section de sources mobilisées ;
- divergence entre une source affichée dans un document maître et son libellé canonique.

Ce contrôle relève principalement de la traçabilité. Il contribue aussi à la dérivabilité, mais ne la démontre pas entièrement.

## 2. Niveaux de granularité possibles

### Niveau 1

```text
DM
↓
sources
```

Question : les sources mentionnées dans un document maître existent-elles dans le registre canonique ?

Le contrôle lit chaque document maître, extrait les identifiants de sources explicitement visibles, par exemple `S35` ou `S45`, puis vérifie leur présence dans le registre canonique des sources, actuellement `data/registre.json`. Les fichiers sous `registers/references/` peuvent fournir des notes ou dossiers complémentaires, mais ils ne doivent pas être utilisés comme registre canonique principal si `data/registre.json` reste la source de référence déclarée par le dépôt.

Avantages :

- périmètre simple et vérifiable ;
- cohérent avec les sections de sources mobilisées déjà présentes dans les documents maîtres ;
- complément direct de `DM -> atomes` et `DM -> registres` ;
- faible risque de surinterprétation historiographique ;
- coût d'implémentation raisonnable ;
- résultat lisible dans l'agrégation M1.

Limites :

- ne vérifie pas quelle source soutient quel passage ;
- ne prouve pas que chaque affirmation du document maître est sourcée ;
- ne distingue pas toujours source mobilisée, source citée et source seulement contextuelle ;
- ne qualifie pas la pertinence historiographique de la source.

Coût : faible à moyen. La difficulté principale consiste à définir la source canonique de comparaison et les libellés acceptables.

### Niveau 2

```text
Section DM
↓
sources
```

Question : chaque section documentaire est-elle reliée à une source ?

Le contrôle associerait chaque grande section d'un document maître à une ou plusieurs sources, puis vérifierait que les sources indiquées existent dans le registre canonique.

Avantages :

- granularité plus utile pour relire la construction documentaire d'un chapitre ;
- meilleure localisation des réserves de traçabilité ;
- prépare une future dérivabilité section par section ;
- permettrait de distinguer les zones bien sourcées des zones seulement synthétiques.

Limites :

- suppose une structure stable et homogène des sections dans tous les documents maîtres ;
- nécessite une convention explicite de rattachement section -> sources qui n'est pas encore stabilisée ;
- risque de produire de nombreux faux positifs si les sections sont rédactionnelles plutôt que documentaires ;
- demande une relecture humaine importante pour interpréter les cas ambigus.

Coût : moyen à élevé. Le contrôle deviendrait dépendant d'une convention documentaire qui n'existe pas encore de façon complète.

### Niveau 3

```text
Paragraphe
↓
atome
↓
source
```

Question : chaque affirmation peut-elle être rattachée à une source ?

Le contrôle chercherait à relier chaque paragraphe ou affirmation rédactionnelle à un ou plusieurs atomes, puis à la source portée par ces atomes.

Avantages :

- valeur historiographique maximale ;
- rapproche le contrôle d'une preuve documentaire fine ;
- permettrait de détecter les affirmations non dérivables ;
- pourrait réduire fortement les zones de traçabilité implicite.

Limites :

- nécessite une segmentation rédactionnelle robuste ;
- suppose une table explicite passage -> atome -> source qui n'existe pas aujourd'hui ;
- très fort risque de faux positifs sur les phrases de synthèse, transitions et interprétations ;
- automatisation difficile sans jugement humain ;
- pourrait transformer M1 en chantier de refonte documentaire, ce qui dépasserait le périmètre actuel.

Coût : élevé. Ce niveau est prématuré pour M1.3 et doit rester hors périmètre tant que la granularité passage par passage n'est pas documentée.

## 3. Comparaison des options

| Critère | Niveau 1 : DM -> sources | Niveau 2 : section DM -> sources | Niveau 3 : paragraphe -> atome -> source |
| --- | --- | --- | --- |
| Robustesse | Bonne si les identifiants `Sxx` et le registre canonique sont stables. | Moyenne, dépendante d'une structure de section homogène. | Faible à ce stade, faute de table passage -> atome -> source. |
| Complexité | Faible à moyenne. | Moyenne à élevée. | Élevée. |
| Risque de faux positifs | Limité aux libellés, alias et sources contextuelles. | Important si les sections ne déclarent pas explicitement leurs sources. | Très important pour les synthèses rédactionnelles et les transitions. |
| Maintenabilité | Bonne : le contrôle resterait comparable aux contrôles M1 existants. | Moyenne : nécessite de maintenir une convention de sections. | Faible sans refonte de la granularité documentaire. |
| Valeur historiographique | Moyenne : vérifie la présence canonique des sources mobilisées. | Bonne : localise mieux les zones documentaires. | Très forte en théorie, mais non atteignable proprement à court terme. |
| Alignement M1 actuel | Fort. | Partiel. | Faible pour M1.3. |
| Coût de revue | Modéré. | Élevé. | Très élevé. |

Le niveau 1 est le seul niveau qui combine utilité documentaire, faible ambiguïté et compatibilité avec l'architecture M1 déjà implémentée.

## 4. Recommandation

Décision recommandée : M1.3 retient le niveau 1.

```text
DM
↓
sources canoniques
```

Le futur contrôle `DM -> sources` doit vérifier uniquement que les sources citées ou mobilisées dans un document maître existent dans le registre canonique des sources.

Les niveaux 2 et 3 sont explicitement reportés hors du périmètre M1.3. Ils pourront être réexaminés après stabilisation d'une convention de rattachement plus fine, mais ils ne doivent pas être introduits comme exigences implicites dans le premier contrôle.

Cette recommandation maintient la doctrine M1 :

- le contrôle établit des constats ;
- il reste en lecture seule ;
- il ne corrige aucun document maître ;
- il ne crée pas de source ;
- il ne remplace pas l'audit humain ;
- il ne transforme pas les documents maîtres en sources ou preuves autonomes.

## 5. Périmètre proposé

### Ce qui sera contrôlé

Le futur contrôle `DM -> sources` devrait vérifier, pour chaque document maître :

- existence du fichier `chapters/*/document_maitre.md` ;
- extraction des identifiants de sources explicitement visibles dans le document maître ;
- présence de ces identifiants dans le registre canonique des sources ;
- cohérence minimale du libellé source lorsque le libellé canonique est objectivement disponible ;
- distinction entre source retrouvée, source absente, source inconnue et source non qualifiable ;
- comparaison éventuelle avec les sources déclarées dans `exports/generated/master_docs_index.json` si cet index expose une volumétrie ou une liste exploitable ;
- signalement des sources mentionnées dans le document maître mais absentes du registre canonique.

Écarts attendus :

- source absente du registre canonique ;
- source inconnue ou identifiant non conforme ;
- source orpheline, visible dans un document maître mais non rattachable à une source conservée ;
- source mentionnée dans le corps du document maître mais absente de la section des sources mobilisées ;
- libellé source divergent lorsque la divergence est objectivement vérifiable.

### Ce qui restera hors périmètre

Le contrôle ne devra pas vérifier :

- le rattachement passage par passage ;
- la pertinence historiographique d'une source ;
- la validité d'une interprétation rédactionnelle ;
- l'exhaustivité de toutes les sources possibles du chapitre ;
- la présence d'une source pour chaque paragraphe ;
- la correspondance fine citation -> source ;
- la dérivabilité complète d'une affirmation ;
- les sources de livrables RAG conservés ;
- les sources non explicitement visibles dans le document maître ;
- les corrections à appliquer aux registres, sources, atomes ou documents maîtres.

Les sources à 0 atome mais porteuses de citations ne doivent pas être exclues par principe. Si elles sont explicitement listées dans un document maître et présentes dans le registre canonique, elles doivent être considérées comme sources retrouvées dans le périmètre du niveau 1.

## 6. Intégration dans l'architecture M1

Le futur contrôle s'insère dans la chaîne M1 stabilisée :

```text
Contrôle
↓
Rapport
↓
Agrégation
↓
Tableau de bord
```

Positionnement des contrôles :

| Contrôle | Rôle | État |
| --- | --- | --- |
| DM -> atomes | Vérifie l'ancrage minimal des documents maîtres dans les atomes exportés. | Implémenté. |
| DM -> registres | Vérifie la cohérence minimale des identifiants de registres P0 visibles. | Implémenté. |
| DM -> sources | Vérifiera la présence canonique des sources citées ou mobilisées par les documents maîtres. | Cadré par ce document, non implémenté. |

Complémentarité :

- `DM -> atomes` répond à la question des unités documentaires visibles ;
- `DM -> registres` répond à la question des objets canoniques structurés ;
- `DM -> sources` répond à la question de l'ancrage source au niveau du document maître.

Ordre logique :

1. conserver `DM -> atomes` comme contrôle de base de la traçabilité des unités ;
2. conserver `DM -> registres` comme contrôle de cohérence des objets structurés ;
3. ajouter `DM -> sources` seulement après décision de granularité, en niveau 1 ;
4. intégrer le futur rapport à l'agrégation M1 uniquement dans une PR dédiée.

Dépendances probables :

- `chapters/master_docs.json` ;
- `chapters/*/document_maitre.md` ;
- `exports/generated/master_docs_index.json`, si ses champs sources sont exploitables ;
- registre canonique des sources `data/registre.json` ;
- éventuellement fichiers sous `registers/references/` et `sources/` comme éléments complémentaires, sans les traiter comme registre canonique principal ni les utiliser pour refaire une atomisation.

## 7. Conditions d'ouverture du chantier

Prérequis :

- confirmer que `data/registre.json` reste le registre canonique à utiliser pour les sources ;
- définir le motif d'identifiant source accepté, par exemple `Sxx` ou `Sxxx` ;
- décider si le contrôle compare seulement les identifiants ou aussi les libellés ;
- identifier les champs disponibles dans `master_docs_index.json` ;
- conserver les règles de sécurité déjà appliquées aux contrôles M1 existants pour les chemins de documents maîtres ;
- définir le rapport attendu sous `reports/m1/` avant implémentation.

Données nécessaires :

- documents maîtres ;
- manifeste des documents maîtres ;
- index généré des documents maîtres ;
- registre canonique des sources `data/registre.json` ;
- éventuels exports ou index sources disponibles ;
- conventions existantes de section "Sources mobilisées".

Difficultés anticipées :

- sources citées avec un libellé légèrement différent du libellé canonique ;
- sources présentes dans les documents maîtres avec 0 atome mais avec citation ;
- sources mentionnées dans un passage mais absentes de la section des sources mobilisées ;
- anciens identifiants ou alias de sources ;
- différence entre source mobilisée, source citée et source contextuelle ;
- absence d'un export source unique si le registre canonique n'est pas exposé comme JSON consolidé.

Risques méthodologiques :

- confondre absence de rattachement fin et défaillance démontrée ;
- classer comme erreur une source contextuelle correctement déclarée ;
- transformer le contrôle en évaluation historiographique ;
- rendre bloquant un écart de libellé non significatif ;
- laisser croire que le niveau 1 valide la dérivabilité passage par passage.

## 8. Décision proposée

Décision recommandée :

M1.3 retient le niveau 1 :

```text
DM
↓
sources canoniques
```

Le contrôle vérifie uniquement que les sources citées ou mobilisées dans un document maître existent dans le registre canonique.

Il ne vérifie pas encore le rattachement section par section, paragraphe par paragraphe ou affirmation par affirmation. Les niveaux 2 et 3 sont reportés hors du périmètre M1.3.

Le futur chantier d'implémentation devra être une PR distincte. Cette PR de cadrage ne crée aucun script, aucun contrôle opérationnel et aucun rapport généré.
