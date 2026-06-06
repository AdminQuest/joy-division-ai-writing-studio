# M2 - Contrat de resume de PR

## 1. Objet

Ce document definit le format commun du resume de PR produit par les flux M2.

Le resume de PR sert a transformer un diagnostic M2 en document relisible par
un humain avant ouverture eventuelle d'une Pull Request.

Il ne cree pas :

- branche Git ;
- Pull Request GitHub ;
- commit ;
- merge ;
- validation historiographique ;
- modification de registre.

Le resume prepare la revue. Il ne remplace pas la revue.

## 2. Perimetre

Le contrat couvre les flux M2 actuellement actifs :

- ajout unitaire `PERSON` ;
- ajout unitaire `ORG` ;
- integration documentaire de source longue.

Le contrat stabilise seulement la structure du resume. Il ne modifie pas les
regles documentaires propres a chaque adaptateur.

Le moteur commun porte :

- la structure de donnees du resume ;
- la reprise des bloquants, reserves et informations ;
- le rendu Markdown deterministe ;
- l'ecriture du fichier de sortie.

Les adaptateurs portent :

- l'objet documentaire ;
- le perimetre metier ;
- les validations pertinentes ;
- les arbitrages humains attendus ;
- l'impact documentaire ;
- les commandes de verification utiles.

## 3. Format commun

Le resume de PR M2 doit contenir les sections suivantes, dans cet ordre.

### Objet

Decrit le changement propose.

Exemples :

- `Ajout PERSON : Test Person (PERSON-test-person)` ;
- `Ajout ORG : Factory Records (ORG-0009)` ;
- `Integration source longue : Ghosts of My Life`.

### Perimetre

Liste ce que le resume couvre et ce qu'il ne couvre pas implicitement.

Le perimetre doit indiquer le flux M2 et la famille documentaire lorsque cela
s'applique.

### Validations executees

Liste les validations ou pre-validations effectivement executees par le flux.

Cette section ne doit pas inventer de controle. Elle peut mentionner une
verification locale uniquement si l'adaptateur l'execute reellement.

### Bloquants

Reprend les bloquants du diagnostic M2.

Une PR ne doit pas etre consideree comme prete si cette section contient autre
chose que `aucun`.

### Reserves

Reprend les reserves du diagnostic M2.

Une reserve ne bloque pas techniquement la preparation du resume, mais elle doit
rester visible et conduire a un arbitrage humain.

### Informations

Reprend les informations utiles produites par le diagnostic.

Cette section peut contenir les cibles d'ecriture probables, le caractere
lecture seule ou les propositions de dossier source.

### Arbitrages humains

Liste les decisions que le reviewer doit explicitement prendre.

Exemples :

- validation humaine finale avant integration ;
- arbitrage des reserves ;
- correction des bloquants avant ouverture de PR.

### Impact documentaire

Decrit ce que la proposition changerait si elle etait acceptee.

Cette section doit aussi rappeler les limites importantes : aucun ajout effectif
tant que la PR n'est pas relue et validee.

### Commandes de verification

Liste les commandes utiles a relancer avant revue ou integration.

Les commandes sont informatives. Le resume ne les execute pas.

## 4. Regles de rendu

Le rendu Markdown commun est deterministe.

Regles :

- titre unique : `# Resume de PR M2` ;
- sections dans l'ordre defini par ce contrat ;
- listes Markdown simples ;
- liste vide rendue par `- aucun` ;
- commandes de verification rendues en code inline ;
- aucune date dynamique ;
- aucune dependance GitHub.

Les fichiers sont ecrits dans :

```text
exports/generated/pr_summary_*.md
```

Le nom exact du fichier reste choisi par l'adaptateur, car il depend de
l'identifiant ou de la source candidate.

## 5. Decisions

La decision de pre-validation reste celle du diagnostic M2 :

- `pre-validee` ;
- `pre-validee avec reserve` ;
- `non pre-validee`.

Le resume ne recalcule pas une decision documentaire separee. Il expose les
constats qui expliquent la decision.

## 6. Contraintes d'architecture

Le noyau commun ne doit contenir aucune logique specifique :

- `PERSON-<slug>` ;
- `ORG-NNNN` ;
- `same_as` `PERS-*` ;
- `joy_division_relation` ;
- Wikidata ;
- edition, traduction ou reedition de source longue.

Ces elements restent dans les adaptateurs.

Le noyau commun peut seulement manipuler :

- l'objet textuel ;
- les listes de perimetre ;
- les listes de validations ;
- les diagnostics deja produits ;
- les arbitrages humains ;
- l'impact documentaire ;
- les commandes de verification ;
- le rendu et l'ecriture Markdown.

## 7. Statut du contrat

Ce contrat est la reference minimale pour industrialiser la preparation de PR
M2 Phase 2 Priorite 1.

Il autorise une generation de resume Markdown. Il n'autorise aucune
automatisation GitHub.
