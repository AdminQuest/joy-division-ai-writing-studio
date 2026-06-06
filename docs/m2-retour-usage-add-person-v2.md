# M2.5.2 - Retour d'usage V2 du prototype PERSON

## 1. Objet du retour d'usage

Le prototype `tools/m2_add_person.py` prepare un ajout unitaire `PERSON-` en lecture seule. Il propose un identifiant, verifie les sources, la categorie, les collisions, les rattachements `same_as`, la forme schema de l'entree candidate et classe les constats en `bloquant`, `reserve` ou `information`.

Le prototype ne modifie aucun registre, aucun schema, aucun export et n'ouvre aucune PR. Il ne remplace pas la validation humaine, ne choisit pas une decision historiographique et ne doit pas etre compris comme une implementation generale de M2.

Cette seconde evaluation verifie que les ameliorations implementees apres le premier retour d'usage repondent bien aux problemes observes :

- cible d'ecriture trop peu explicite ;
- messages redondants pour les categories invalides ;
- aide insuffisante sur le vocabulaire de categorie ;
- absence de cas reellement classe en `reserve` ;
- absence de test d'alias ambigu.

## 2. Verification des ameliorations attendues

### Cible d'ecriture

Question :

Le prototype explique-t-il desormais clairement la cible d'ecriture proposee ?

Constat :

Oui. Le message ne se limite plus a `same_as vide: cible d'ecriture a confirmer avant integration`. Il explique maintenant le cas observe.

Exemple observe, cas conforme sans `same_as` :

```text
Informations :
- Aucun PERS-* fourni. Aucune cible d'ecriture source/provisoire n'est identifiable. Validation humaine necessaire avant integration.
```

Le prototype distingue aussi le cas ou un `PERS-*` est fourni :

```text
Cible d'ecriture probable : registers/people/*.md puis regeneration controlee de registers/people/00_canonical_people.md. Pourquoi : PERS-* fourni. Il manque la confirmation humaine du fichier source/provisoire a modifier.
```

Conclusion :

Le probleme identifie en V1 est corrige. Le prototype n'ecrit toujours pas, mais il rend visible la cible probable ou l'absence de cible identifiable.

### Messages redondants

Question :

Les diagnostics sont-ils plus lisibles ?

Constat :

Oui. Une categorie invalide ne produit plus a la fois un diagnostic metier et le diagnostic schema equivalent pour la meme cause.

Exemple observe avec `--category manager` :

```text
Bloquants :
- categorie invalide: manager (categories autorisees: membre, entourage, industrie, critique_journaliste, auteur_secondaire, influence, theoricien_mobilise)
```

Le premier retour observait :

```text
categorie invalide: manager
schema invalide: Invalid value for categorie: manager
```

Conclusion :

La sortie est plus concise. L'information technique utile reste presente via la liste des categories autorisees, sans duplication inutile.

### Aide categorie

Question :

L'utilisateur est-il mieux guide ?

Constat :

Oui. `python3 tools/m2_add_person.py --help` affiche maintenant la liste complete des categories autorisees.

Exemple observe :

```text
Categories autorisees:
  - membre
  - entourage
  - industrie
  - critique_journaliste
  - auteur_secondaire
  - influence
  - theoricien_mobilise
```

Le message d'erreur de categorie invalide reprend egalement cette liste.

Conclusion :

Le prototype guide mieux l'utilisateur sans ajouter de logique metier. Le vocabulaire reste ferme et conforme au schema `PERSON`.

### Cas reserve

Question :

La categorie "reserve" est-elle reellement exercee ?

Constat :

Oui. Le cas `--identity-arbitration` produit maintenant une decision `pre-validee avec reserve`.

Exemple observe :

```text
Decision : pre-validee avec reserve
Reserves :
- identite a arbitrer: rattachement ou homonymie a confirmer
```

L'entree candidate porte bien :

```yaml
a_arbitrer: true
```

Conclusion :

Le probleme V1 est corrige. La classe `reserve` n'est plus seulement theorique ; elle correspond a un champ existant du modele reel.

### Alias ambigu

Question :

Le prototype reagit-il correctement aux ambiguites ?

Constat :

Oui pour le cas teste. Un alias proche d'un nom canonique existant n'est ni accepte silencieusement ni refuse systematiquement. Il devient une reserve.

Exemple observe avec `--aliases "Iain Curtis"` :

```text
Decision : pre-validee avec reserve
Reserves :
- alias proche d'un nom a arbitrer: Iain Curtis ~ Ian Curtis (PERSON-ian-curtis)
```

Conclusion :

Le comportement est conforme a M2.2 : une collision probable de libelle ou d'alias devient une reserve visible, tandis qu'une collision exacte reste bloquante.

## 3. Nouveaux cas d'essai

Les cas ci-dessous ont ete executes sur l'etat courant du depot, sans modification des registres.

### Cas conforme

Commande :

```bash
python3 tools/m2_add_person.py --name "Prototype Usage V2 Person" --category industrie --role producteur --sources S41
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-v2-person` |
| decision | `pre-validee` |
| bloquants | aucun |
| reserves | aucune |
| information principale | `Aucun PERS-* fourni. Aucune cible d'ecriture source/provisoire n'est identifiable. Validation humaine necessaire avant integration.` |

Lecture :

Le cas minimal reste exploitable. Le prototype prepare une proposition relisible sans ecrire dans le depot.

### Source inconnue

Commande :

```bash
python3 tools/m2_add_person.py --name "Prototype Usage V2 Person" --category industrie --role producteur --sources S999
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-v2-person` |
| decision | `non pre-validee` |
| bloquants | `source inconnue: S999` |
| reserves | aucune |

Lecture :

La source inconnue reste bloquante. La reserve n'est pas utilisee pour masquer une source absente du registre canonique.

### Categorie invalide

Commande :

```bash
python3 tools/m2_add_person.py --name "Prototype Usage V2 Person" --category manager --role producteur --sources S41
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-v2-person` |
| decision | `non pre-validee` |
| bloquants | `categorie invalide: manager (categories autorisees: membre, entourage, industrie, critique_journaliste, auteur_secondaire, influence, theoricien_mobilise)` |
| reserves | aucune |

Lecture :

Le diagnostic est plus lisible qu'en V1. La categorie invalide reste bloquante.

### Collision

Commande :

```bash
python3 tools/m2_add_person.py --name "Martin Hannett" --category industrie --role producteur --sources S41,S74
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-martin-hannett` |
| decision | `non pre-validee` |
| bloquants | `identifiant deja utilise: PERSON-martin-hannett` ; `collision certaine de nom: Martin Hannett deja present dans PERSON-martin-hannett` |
| reserves | aucune |

Lecture :

La collision certaine reste bloquante, comme attendu. Le prototype ne transforme pas un doublon manifeste en reserve.

### Reserve

Commande :

```bash
python3 tools/m2_add_person.py --name "Usage Reserve V2 Person" --category industrie --role producteur --sources S41 --identity-arbitration
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-usage-reserve-v2-person` |
| decision | `pre-validee avec reserve` |
| bloquants | aucun |
| reserves | `identite a arbitrer: rattachement ou homonymie a confirmer` |

Lecture :

La reserve est correctement exercee sur un champ du schema reel : `a_arbitrer: true`.

### Alias ambigu

Commande :

```bash
python3 tools/m2_add_person.py --name "Alias Ambigu V2 Usage" --category industrie --role producteur --sources S41 --aliases "Iain Curtis"
```

Resultat observe :

| Element | Resultat |
| --- | --- |
| identifiant propose | `PERSON-alias-ambigu-v2-usage` |
| decision | `pre-validee avec reserve` |
| bloquants | aucun |
| reserves | `alias proche d'un nom a arbitrer: Iain Curtis ~ Ian Curtis (PERSON-ian-curtis)` |

Lecture :

Le prototype signale l'ambiguite sans forcer une fusion et sans refuser tout ajout. La validation humaine reste necessaire.

## 4. Qualite documentaire

### Robustesse

Le prototype est plus robuste qu'en V1 sur les cas documentaires les plus sensibles :

- source inconnue : bloquant ;
- categorie invalide : bloquant concis ;
- collision exacte : bloquant ;
- arbitrage d'identite : reserve ;
- alias proche : reserve ;
- cas conforme : pre-validation sans ecriture.

Les tests automatises couvrent desormais ces comportements et la sortie reste deterministe.

### Lisibilite

La lisibilite progresse nettement :

- la cible d'ecriture ou son absence est explicite ;
- les categories autorisees sont visibles dans l'aide et dans l'erreur ;
- les messages redondants ont ete reduits ;
- la reserve est visible dans une section separee de la sortie.

La sortie YAML reste volontairement complete. Elle est plus verbeuse qu'un simple diagnostic, mais elle sert la relecture documentaire et la future preparation de PR.

### Coherence avec M2.1

Le comportement actuel reste conforme au contrat d'ajout unitaire :

- un seul objet `PERSON` est prepare ;
- les champs minimaux du modele reel sont presents ;
- au moins une source documentaire est requise ;
- les collisions d'identifiant ou de nom ne sont pas acceptees ;
- le prototype ne modifie pas les registres.

### Coherence avec M2.2

La classification applique correctement la doctrine de pre-validation commune :

- `bloquant` pour source inconnue, categorie invalide, schema incompatible ou collision certaine ;
- `reserve` pour arbitrage humain explicite ou alias proche ;
- `information` pour cible d'ecriture a confirmer ou absente.

Le prototype ne reclasse pas un bloquant en reserve pour faciliter une PR.

### Coherence avec M2.4

La sortie est exploitable pour une future preparation de PR :

- decision visible ;
- identifiant propose ;
- bloquants, reserves et informations separes ;
- entree candidate YAML relisible ;
- validations reproductibles par commande.

Le prototype ne cree pas de branche, n'ouvre pas de PR et ne suppose pas de merge.

## 5. Limites restantes

Limites reellement observees :

- le prototype reste un outil CLI destine a un utilisateur connaissant les sources `Sxx` ;
- la cible d'ecriture avec `same_as` reste probable, pas resolue jusqu'au fichier exact ;
- la detection de proximite d'alias signale une ambiguite mais ne l'explique pas historiographiquement ;
- la sortie YAML reste longue pour un diagnostic rapide ;
- le prototype ne produit pas de diff ni de patch, conformement a son perimetre actuel.

Critiques V1 corrigees et non retenues comme limites restantes :

- le message `same_as vide` n'est plus insuffisant ;
- la categorie invalide ne produit plus de doublon schema equivalent ;
- les categories autorisees sont visibles ;
- la classe `reserve` est exercee ;
- un alias ambigu est teste et signale.

## 6. Decision

Le prototype PERSON est-il suffisamment stable pour servir de modele a une autre famille documentaire ?

oui

## 7. Recommandation

La famille suivante la plus pertinente est `ORG`.

Justification :

- `ORG` est une famille d'entites structurees proche de `PERSON` par ses risques de collision de libelle, d'alias et de statut ;
- le retour V2 montre que le modele `bloquant` / `reserve` / `information` est exploitable en CLI ;
- les ameliorations necessaires avant extension de `PERSON` sont maintenant traitees ;
- `ORG` permettrait de reutiliser le patron de pre-validation sans basculer vers une famille plus complexe comme `CONCERT`, `IMAGE` ou `RELEASE`.

Cette recommandation ne cree pas le prototype `ORG`, ne modifie aucun schema et n'ouvre aucun chantier d'implementation. Elle conclut seulement que `PERSON` peut servir de reference pour definir le prochain prototype documentaire.
