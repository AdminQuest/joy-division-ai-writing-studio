# M2.11 - Contrat de formulaire d'enrichissement

## 1. Objet du formulaire

Le formulaire d'enrichissement existe pour donner un point d'entree unique aux
flux M2 deja definis.

Il doit permettre a un utilisateur de formuler une intention documentaire sans
editer manuellement plusieurs fichiers et sans connaitre toute la structure du
depot.

Le formulaire remplace :

- la saisie libre non structuree des parametres d'ajout ;
- la collecte manuelle dispersee des champs obligatoires ;
- la recherche manuelle des commandes de prototype a lancer ;
- une partie de la preparation du resume de proposition.

Le formulaire ne remplace pas :

- les contrats M2.1, M2.2, M2.3 et M2.4 ;
- les adaptateurs par famille documentaire ;
- les validateurs existants ;
- les controles M1 ;
- la revue humaine ;
- la decision historiographique ;
- la preparation explicite d'une PR relisible.

Le formulaire est donc une couche de saisie et d'orchestration. Il ne devient
pas une couche de validation documentaire.

## 2. Flux couverts

### Flux A - ajout unitaire

Objectif :

preparer l'ajout d'un objet documentaire unique deja qualifie.

Types concernes a terme :

- `PERSON` ;
- `ORG` ;
- autres familles seulement apres contrat et prototype dedies.

Entrees :

- type documentaire ;
- nom ou libelle canonique ;
- champs obligatoires de la famille ;
- sources documentaires ;
- alias ou variantes ;
- relations minimales ;
- commentaire utilisateur ;
- contexte de prudence ou d'arbitrage.

Sorties :

- entree candidate ;
- identifiant propose ;
- diagnostics classes ;
- cible d'ecriture probable ;
- controles a executer ;
- resume exploitable pour une PR.

Limites :

- le formulaire ne cree pas l'objet ;
- il ne modifie aucun registre ;
- il ne tranche pas les collisions ;
- il n'ouvre pas une famille non stabilisee ;
- il ne remplace pas l'adaptateur de la famille.

### Flux B - source longue

Objectif :

preparer la pre-validation d'une source longue candidate avant integration
documentaire.

Types de source couverts par M2.3 :

- `livre` ;
- `article` ;
- `interview` ;
- `fanzine` ;
- `archive` ;
- `memoire` ;
- `these` ;
- `dossier documentaire`.

Entrees :

- titre ;
- auteur ou responsable documentaire ;
- type de source ;
- annee ou date principale ;
- reference complete ;
- URL eventuelle ;
- edition ou version ;
- publication ou support parent ;
- pages utiles ;
- section utile ;
- commentaire utilisateur.

Sorties :

- diagnostic de source nouvelle, proche ou deja presente ;
- `Sxx` existant ou probable ;
- dossier source probable ;
- reserves de proximite ;
- metadonnees candidates ;
- resume d'arbitrage humain.

Limites :

- le formulaire ne cree pas de `Sxx` ;
- il ne cree pas de dossier `sources/<source>/` ;
- il ne genere pas d'atomes ;
- il ne genere pas de citations ;
- il ne genere pas de relations ;
- il ne decide pas qu'une source est historiographiquement suffisante.

## 3. Ce que le formulaire collecte

### Champs communs

Les champs communs servent a orienter le flux et a produire une sortie
reliable.

| Champ | Role |
| --- | --- |
| type de flux | Distinguer `ajout unitaire` et `source longue`. |
| type documentaire | Choisir la famille ou le type de source. |
| sources | Declarer les sources `Sxx` connues ou la source candidate. |
| commentaire utilisateur | Expliquer l'intention, la prudence ou l'arbitrage attendu. |
| contexte | Indiquer pourquoi l'enrichissement est propose. |
| niveau d'incertitude | Signaler ce qui doit rester en reserve. |

Ces champs communs ne suffisent jamais a produire une modification. Ils
orientent seulement l'adaptateur ou le flux applicable.

### Champs specifiques - PERSON

Exemples de champs que le formulaire pourrait collecter pour `PERSON` :

- nom ;
- categorie ;
- role ;
- sources `Sxx` ;
- alias eventuels ;
- `same_as` eventuel vers `PERS-*` ;
- origine si applicable ;
- commentaire d'arbitrage.

Ces champs reprennent le modele reel du contrat M2.1 et du prototype PERSON. Le
formulaire ne doit pas inventer de categorie ou de relation absente du schema.

### Champs specifiques - ORG

Exemples de champs que le formulaire pourrait collecter pour `ORG` :

- nom canonique ;
- categorie ;
- pays ;
- statut ;
- relation avec Joy Division ;
- sources `Sxx` ;
- alias ;
- identifiants externes eventuels ;
- commentaire d'arbitrage.

Ces champs doivent rester alignes avec le schema ORG, le validateur ORG et le
prototype ORG.

### Champs specifiques - SOURCE LONGUE

Exemples de champs que le formulaire pourrait collecter pour une source longue :

- titre ;
- auteur ;
- type M2.3 ;
- annee ;
- reference complete ;
- URL ;
- edition ;
- publication ;
- pages utiles ;
- section utile ;
- commentaire d'integration.

Ces champs servent a declencher une pre-validation de source longue. Ils ne
creent ni source canonique ni dossier source.

## 4. Ce que le formulaire declenche

Le formulaire doit declencher les etapes dans l'ordre suivant.

```text
saisie utilisateur
  ->
selection du flux
  ->
selection de l'adaptateur
  ->
normalisation minimale des entrees
  ->
pre-validation
  ->
diagnostics
  ->
proposition
  ->
resume
```

Role des composants :

| Composant | Role |
| --- | --- |
| formulaire | Collecter les champs et choisir le flux. |
| adaptateur | Appliquer la logique de la famille ou de la source longue. |
| moteur commun | Classer bloquants, reserves et informations ; calculer la decision. |
| diagnostics | Rendre visibles erreurs, collisions, sources inconnues et reserves. |
| proposition | Presenter l'entree candidate ou la source candidate. |
| resume | Preparer un texte exploitable pour revue ou PR. |

Le formulaire ne doit pas court-circuiter l'adaptateur. La logique specifique
reste dans l'adaptateur, pas dans l'interface.

## 5. Ce que le formulaire produit

Sortie minimale attendue :

- decision de pre-validation ;
- entree candidate ;
- diagnostics ;
- bloquants ;
- reserves ;
- informations ;
- sources declarees ;
- relations declarees ;
- fichiers potentiellement concernes ;
- controles a executer ;
- resume de PR ;
- arbitrages humains restants.

La sortie doit rester relisible sans ouvrir l'interface. Elle doit pouvoir etre
copiee dans un retour d'usage, une PR ou un document d'audit.

La sortie doit distinguer explicitement :

- proposition recevable ;
- proposition recevable avec reserve ;
- proposition non recevable en l'etat.

## 6. Ce qu'il ne doit jamais produire

Le formulaire ne doit jamais produire directement :

- modification de registre ;
- creation de `Sxx` ;
- creation d'atome ;
- creation de citation ;
- creation de relation ;
- creation de dossier source ;
- modification de schema ;
- modification d'export ;
- commit sur `main` ;
- merge ;
- publication ;
- validation historiographique ;
- fusion automatique d'identites ;
- correction silencieuse de donnees ;
- contournement des controles M1 ou M2.

Le formulaire peut proposer. Il ne doit pas appliquer.

## 7. Architecture logique

Architecture attendue :

```text
utilisateur
  |
  v
formulaire
  |
  v
adaptateur
  |
  v
moteur commun
  |
  v
diagnostics
  |
  v
resultat
```

Lecture par couche :

| Couche | Responsabilite |
| --- | --- |
| utilisateur | Fournir une intention documentaire et les informations connues. |
| formulaire | Encadrer la saisie, rappeler les champs attendus, transmettre au bon flux. |
| adaptateur | Interpreter la famille ou la source longue selon le modele reel. |
| moteur commun | Harmoniser decision, classification et rendu des diagnostics. |
| diagnostics | Exposer bloquants, reserves et informations. |
| resultat | Donner une proposition relisible, sans ecriture automatique. |

Cette architecture respecte `docs/m2-architecture-adaptateurs.md` :

- le moteur commun porte les invariants ;
- les adaptateurs portent la logique documentaire ;
- le formulaire reste une couche d'entree ;
- l'humain conserve la validation.

## 8. Conditions de passage a l'UI

Une interface pourra etre construite seulement lorsque les criteres suivants
seront atteints.

### Criteres fonctionnels

- le contrat du formulaire est accepte ;
- les flux `ajout unitaire` et `source longue` sont clairement separes ;
- chaque flux dispose d'une sortie textuelle relisible hors interface ;
- les champs obligatoires par famille sont documentes ;
- les champs facultatifs ne sont pas presentes comme preuves.

### Criteres techniques

- les adaptateurs utilises par l'interface sont stabilises ;
- le moteur commun conserve une sortie deterministe ;
- les erreurs, reserves et informations sont serialisables ;
- les tests des prototypes concernes restent verts ;
- l'interface ne devient pas source de verite.

### Criteres de gouvernance

- aucune ecriture automatique dans `main` ;
- aucun merge automatique ;
- aucune creation implicite de source canonique ;
- reserves visibles avant PR ;
- validation humaine maintenue ;
- revue obligatoire conservee.

Tant que ces criteres ne sont pas atteints, le formulaire doit rester un contrat
documentaire, pas une implementation.

## 9. Risques

### Risques techniques

- dupliquer de la logique deja portee par les adaptateurs ;
- figer trop tot des champs encore experimentaux ;
- produire une interface qui masque les diagnostics textuels ;
- rendre les sorties moins deterministes ;
- melanger flux unitaire et flux source longue dans un meme ecran trop ambigu.

### Risques documentaires

- presenter une proposition comme une validation ;
- sous-documenter les reserves ;
- confondre source canonique, URL, provenance et identifiant interne ;
- creer des doublons par saisie guidee trop permissive ;
- encourager une atomisation trop rapide depuis une source longue.

### Risques de gouvernance

- banaliser le contournement des PR ;
- rendre moins visible la responsabilite humaine ;
- automatiser des decisions de merge ;
- faire du formulaire une source de verite concurrente ;
- ouvrir des familles non stabilisees parce qu'elles semblent faciles a saisir.

## 10. Decision proposee

Le contrat est-il suffisamment stable pour lancer une interface ?

```text
non
```

Le contrat est suffisamment stable pour cadrer une future interface. Il n'est
pas encore suffisant pour lancer son implementation.

Decision proposee :

- conserver ce document comme contrat fonctionnel ;
- ne pas creer d'interface immediate ;
- consolider d'abord les adaptateurs et sorties textuelles ;
- verifier que le flux source longue reste stable apres les ameliorations de
  proximite ;
- lancer l'UI seulement lorsque le formulaire peut rester une couche de saisie,
  sans absorber la logique documentaire.
