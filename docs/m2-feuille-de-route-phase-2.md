# M2 - Feuille de route Phase 2

## 1. Ce qui est acquis

M2 dispose maintenant d'un socle suffisant pour sortir de la phase de cadrage.

Acquis stabilises :

- doctrine : le Studio prepare, l'humain valide ;
- separation entre ajout unitaire et integration documentaire longue ;
- contrat d'ajout unitaire ;
- pre-validation commune ;
- contrat d'integration documentaire longue ;
- contrat de preparation de PR ;
- architecture moteur commun + adaptateurs ;
- noyau commun implemente ;
- prototypes `PERSON` et `ORG` valides ;
- prototype source longue implemente, observe et ameliore ;
- contrat fonctionnel du futur formulaire ;
- classification commune `bloquant`, `reserve`, `information` ;
- sorties deterministes et tests automatises sur les prototypes actifs.

Le projet sait donc produire des diagnostics utiles. Le point faible n'est plus
la doctrine, mais le passage controle vers une PR relisible.

## 2. Ce qui n'est plus prioritaire

Les nouveaux contrats ne sont plus prioritaires.

Raison : les contrats M2.1, M2.2, M2.3, M2.4, l'architecture adaptateurs et le
contrat de formulaire couvrent deja les decisions structurantes. Ajouter un
nouveau contrat retarderait l'industrialisation sans reduire le risque principal
actuel.

Les nouveaux bilans ne sont plus prioritaires.

Raison : les retours d'usage PERSON, ORG et source longue ont deja identifie les
invariants, les limites et les risques. Un nouveau bilan aurait moins de valeur
qu'une implementation mesurable.

Les nouvelles architectures ne sont plus prioritaires.

Raison : la decision moteur commun + adaptateurs est prise et le noyau commun
existe. La prochaine etape doit utiliser cette architecture, pas la rediscuter.

Les nouvelles familles documentaires ne sont plus prioritaires.

Raison : ouvrir `PLACE`, `IMAGE`, `CONCERT`, `RELEASE` ou `CITATION` ajouterait
du perimetre avant que le chemin diagnostic -> controles -> PR soit
industrialise. Cela augmenterait la duplication et le risque de propositions non
reliables.

## 3. Chantiers candidats

### A - Industrialisation de la preparation de PR

Valeur apportee :

- transforme les diagnostics M2 en PR relisibles ;
- reduit le travail manuel repetitif apres une pre-validation ;
- impose un format commun pour objet, perimetre, validations et reserves ;
- rend les arbitrages humains visibles ;
- beneficie a `PERSON`, `ORG` et source longue sans ouvrir une nouvelle famille.

Cout :

- moyen ;
- necessite de definir une sortie exploitable par les prototypes existants ;
- demande des tests de non-regression et quelques cas representatifs ;
- peut rester limite a la preparation de texte, sans automatiser GitHub.

Risque :

- automatiser trop vite branche, commit ou PR ;
- masquer les reserves dans un resume trop lisse ;
- produire des corps de PR generiques mais peu utiles.

Dependances :

- contrat M2.4 ;
- noyau commun M2 ;
- sorties actuelles des prototypes ;
- liste des validations pertinentes par type de changement.

### B - Industrialisation de l'integration documentaire longue

Valeur apportee :

- augmente la valeur du flux source longue ;
- permet de preparer plus efficacement source canonique, dossier source et
  propositions documentaires ;
- traite un besoin documentaire central du corpus ;
- capitalise sur la campagne d'observation et l'amelioration de proximite.

Cout :

- eleve ;
- touche des objets plus nombreux et plus sensibles ;
- demande de distinguer source canonique, dossier source, atomes, citations et
  relations ;
- necessite des garde-fous forts pour eviter une grosse PR opaque.

Risque :

- creer implicitement des `Sxx` ;
- melanger integration source, atomisation et enrichissements de registres ;
- produire trop de propositions en une seule fois ;
- rendre la validation humaine plus difficile.

Dependances :

- prototype source longue ;
- retour de campagne source longue ;
- amelioration de proximite ;
- preparation de PR assistee ;
- controles existants du depot.

### C - Interface formulaire

Valeur apportee :

- rend M2 plus accessible qu'une collection de CLI ;
- guide la saisie des champs ;
- peut reduire les erreurs d'entree ;
- donne un point d'entree unique aux flux M2.

Cout :

- eleve si l'interface doit couvrir plusieurs flux ;
- impose une stabilite des sorties et adaptateurs ;
- demande une discipline forte pour ne pas mettre de logique documentaire dans
  l'UI.

Risque :

- figer trop tot des champs encore mouvants ;
- masquer les diagnostics textuels ;
- presenter une proposition comme une validation ;
- encourager l'utilisateur a croire qu'un formulaire peut remplacer la revue.

Dependances :

- contrat de formulaire ;
- adaptateurs stabilises ;
- preparation de PR assistee ;
- sortie serialisable et deterministe ;
- gouvernance claire sur ce que l'UI ne fait jamais.

## 4. Classement

Priorite 1 : industrialisation de la preparation de PR.

Priorite 2 : industrialisation de l'integration documentaire longue.

Priorite 3 : interface formulaire.

Justification :

- la preparation de PR est le chainon commun qui manque a tous les flux ;
- l'integration documentaire longue est la plus forte valeur documentaire, mais
  elle doit d'abord disposer d'une sortie PR solide ;
- le formulaire doit attendre que le chemin textuel soit stable, sinon il
  figera trop tot les incertitudes.

## 5. Decision

Quelle est la prochaine implementation majeure de M2 ?

```text
Industrialisation de la preparation de PR
```

Cette implementation doit rester bornee :

- pas de merge automatique ;
- pas de commit sur `main` ;
- pas de creation automatique de registre ;
- pas de nouvelle famille documentaire ;
- pas d'interface ;
- generation d'un dossier de sortie ou d'un resume de PR relisible avant toute
  automatisation GitHub.

## 6. Critere de sortie

M2 Phase 2 pourra etre consideree comme achevee lorsque le projet disposera
d'un flux industrialise permettant de passer d'une pre-validation M2 a une PR
preparable et relisible.

Critere minimal :

- les prototypes `PERSON`, `ORG` et source longue peuvent produire ou alimenter
  un resume de PR commun ;
- le resume expose objet, perimetre, fichiers concernes, validations, bloquants,
  reserves, informations et arbitrages humains ;
- les commandes de validation pertinentes sont listees sans inventer de nouveau
  controle ;
- les tests couvrent au moins un cas `PERSON`, un cas `ORG` et un cas source
  longue ;
- aucune ecriture automatique sur `main` n'est possible ;
- aucune reserve n'est masquee ;
- une PR issue de ce flux peut etre relue sans reconstituer manuellement tout le
  diagnostic.

Une fois ce critere atteint, M2 pourra rouvrir la question de l'industrialisation
source longue ou de l'interface formulaire sur une base plus solide.
