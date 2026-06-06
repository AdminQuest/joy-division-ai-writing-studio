# M2.5.1 - Retour d'usage du prototype PERSON

## 1. Objet du retour d'usage

Le prototype CLI `tools/m2_add_person.py` a ete developpe pour tester le premier flux operationnel M2 sur un type documentaire limite : `PERSON`.

Le probleme a resoudre etait concret : verifier qu'un ajout de personne peut etre prepare sans edition manuelle immediate des registres, sans creation de branche automatique, sans PR automatique et sans decision historiographique implicite.

Le prototype couvre :

- proposition d'un identifiant `PERSON-<slug>` a partir du nom ;
- verification des sources `Sxx` contre `data/registre.json` ;
- verification de la categorie contre le vocabulaire canonique ;
- verification du schema de l'entree candidate ;
- detection des collisions d'identifiant, nom, alias et `same_as` ;
- sortie structuree en `bloquant`, `reserve` et `information` ;
- generation d'une entree candidate YAML en lecture seule.

Le prototype ne couvre pas :

- ecriture dans les registres ;
- modification des exports ;
- creation de branche ;
- ouverture de PR ;
- choix de cible d'ecriture automatise ;
- arbitrage documentaire ou historiographique.

## 2. Cas d'essai realises

Les essais ci-dessous ont ete executes avec le prototype actuel, sans modification des registres.

### Cas conforme

Entree :

| Champ | Valeur |
| --- | --- |
| nom | `Prototype Usage Person` |
| categorie | `industrie` |
| role | `producteur` |
| sources | `S41` |

Resultat :

| Element | Resultat observe |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-person` |
| decision | `pre-validee` |
| bloquants | aucun |
| reserves | aucune |
| informations | `same_as vide: cible d'ecriture a confirmer avant integration` |

Lecture : le prototype sait produire une proposition exploitable lorsque les champs minimaux sont corrects et la source connue. L'information sur `same_as` rappelle correctement qu'une cible d'ecriture reste a confirmer avant integration.

### Source inconnue

Entree :

| Champ | Valeur |
| --- | --- |
| nom | `Prototype Usage Person` |
| categorie | `industrie` |
| role | `producteur` |
| sources | `S999` |

Resultat :

| Element | Resultat observe |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-person` |
| decision | `non pre-validee` |
| bloquants | `source inconnue: S999` |
| reserves | aucune |
| informations | `same_as vide: cible d'ecriture a confirmer avant integration` |

Lecture : la source inconnue est bien bloquante, conformement a M2.2.

### Categorie invalide

Entree :

| Champ | Valeur |
| --- | --- |
| nom | `Prototype Usage Person` |
| categorie | `manager` |
| role | `producteur` |
| sources | `S41` |

Resultat :

| Element | Resultat observe |
| --- | --- |
| identifiant propose | `PERSON-prototype-usage-person` |
| decision | `non pre-validee` |
| bloquants | `categorie invalide: manager` ; `schema invalide: Invalid value for categorie: manager` |
| reserves | aucune |
| informations | `same_as vide: cible d'ecriture a confirmer avant integration` |

Lecture : la categorie invalide est bien bloquante. Le message est correct mais redondant, car le controle metier et le controle schema remontent la meme cause.

### Collision d'identifiant et de nom

Entree :

| Champ | Valeur |
| --- | --- |
| nom | `Martin Hannett` |
| categorie | `industrie` |
| role | `producteur` |
| sources | `S41,S74` |

Resultat :

| Element | Resultat observe |
| --- | --- |
| identifiant propose | `PERSON-martin-hannett` |
| decision | `non pre-validee` |
| bloquants | `identifiant deja utilise: PERSON-martin-hannett` ; `collision certaine de nom: Martin Hannett deja present dans PERSON-martin-hannett` |
| reserves | aucune |
| informations | `same_as vide: cible d'ecriture a confirmer avant integration` |

Lecture : le prototype detecte correctement une personne deja existante. L'ajout manuel aurait expose un risque de doublon ; ici le refus est immediat.

### Auteur-source avec `same_as`

Entree :

| Champ | Valeur |
| --- | --- |
| nom | `Author Source Usage` |
| categorie | `auteur_secondaire` |
| role | `auteur` |
| sources | `S41` |
| origin | `auteur_source` |
| same_as | `PERS-S41-001` |

Resultat :

| Element | Resultat observe |
| --- | --- |
| identifiant propose | `PERSON-author-source-usage` |
| decision | `non pre-validee` |
| bloquants | `same_as PERS introuvable: PERS-S41-001` ; `auteur_source exige same_as vide` |
| reserves | aucune |
| informations | `auteur-source: verifier le pipeline d'attribution avant integration` |

Lecture : le prototype applique la correction issue de la revue Codex du prototype CLI. Un auteur-source ne doit pas porter de `same_as` non vide.

## 3. Ergonomie

Le prototype est facile a utiliser pour un utilisateur qui connait deja les identifiants `Sxx` et les categories `PERSON`.

Points positifs :

- commande courte pour le cas minimal ;
- parametres explicites : `--name`, `--category`, `--role`, `--sources` ;
- aide CLI disponible avec `--help` ;
- sortie stable et lisible ;
- separation claire entre decision, bloquants, reserves, informations et entree candidate.

Points moins confortables :

- l'utilisateur doit connaitre le vocabulaire exact des categories ;
- l'utilisateur doit connaitre les identifiants sources `Sxx` ;
- l'information `same_as vide` est utile mais ne dit pas comment choisir la cible d'ecriture ;
- les erreurs peuvent etre redondantes, comme pour la categorie invalide ;
- la sortie YAML est utile pour la revue mais un peu verbeuse pour un simple diagnostic.

Conclusion ergonomique :

Le prototype est utilisable en ligne de commande. Il est plus clair qu'une verification manuelle dispersee, mais il reste destine a un utilisateur deja familier du depot.

## 4. Valeur documentaire

Le prototype apporte une valeur reelle par rapport a l'ajout manuel actuel.

Gains observes :

- propose automatiquement un identifiant canonique coherent ;
- bloque les sources inconnues avant toute edition ;
- bloque les categories hors vocabulaire ;
- detecte les doublons `PERSON-` evidents ;
- detecte les collisions de nom ;
- produit une entree candidate directement relisible ;
- applique la classification M2.2 sans modifier le corpus ;
- garde visibles les limites, notamment `same_as` et auteur-source.

Comparaison avec l'ajout manuel :

| Sujet | Ajout manuel | Prototype |
| --- | --- | --- |
| identifiant | A construire et verifier a la main. | Propose automatiquement puis verifie. |
| source `Sxx` | Recherche manuelle dans `data/registre.json`. | Verification automatique. |
| categorie | Risque de faute ou vocabulaire approximatif. | Vocabulaire ferme controle. |
| collision | Recherche manuelle dans plusieurs fichiers. | Detection automatique dans les registres canoniques charges. |
| schema | Verification tardive par validateur. | Diagnostic direct sur l'entree candidate. |
| trace de decision | A rediger manuellement. | Sortie structuree reutilisable. |

Limites :

- le prototype ne choisit pas la cible d'ecriture ;
- il ne genere pas de patch ;
- il ne remplace pas `validate_people.py` ni `validate_attribution.py` ;
- il ne dit pas si une source est historiographiquement suffisante ;
- il ne resout pas les cas ambigus de personne, alias ou categorie.

Risques :

- croire qu'une sortie `pre-validee` vaut validation documentaire ;
- copier l'entree YAML dans un fichier genere au lieu de passer par le pipeline maintenu ;
- ignorer l'information `same_as vide`.

## 5. Qualite des controles

### Sources inconnues

La detection est bonne. `S999` produit `non pre-validee` avec un bloquant explicite. Le prototype respecte la doctrine M2.2 : une source inconnue n'est jamais une reserve.

### Collisions

La collision `Martin Hannett` est correctement detectee sur l'identifiant et le nom canonique. La detection couvre aussi `00_authors_canonical.md` selon le code du prototype, ce qui evite les doublons avec les auteurs-sources.

La detection d'alias existe, mais elle n'a pas ete poussee ici avec un cas ambigu complexe. Elle doit donc etre consideree utile mais encore limitee.

### Categories invalides

La categorie invalide est bien bloquante. Le prototype remonte toutefois deux messages pour une meme cause : `categorie invalide` et `schema invalide`. C'est exact, mais moins ergonomique.

### Validation du schema

La validation du schema fonctionne comme filet de securite. Elle confirme que l'entree candidate reste compatible avec le modele `PERSON`.

### Classification

La classification est globalement bonne :

- `bloquant` est utilise pour source inconnue, categorie invalide, collision et `same_as` incompatible avec auteur-source ;
- `information` est utilise pour les points a confirmer, comme `same_as vide` ;
- `reserve` n'a pas ete observee dans les essais realises.

Limite observee : l'absence de cas `reserve` dans les essais rend la classe moins eprouvee que `bloquant` et `information`.

## 6. Limites observees

Limites effectivement observees :

- sortie parfois verbeuse, surtout lorsque l'entree candidate YAML est complete ;
- aide CLI utile mais sans aide contextuelle sur le choix d'une categorie ;
- message redondant pour la categorie invalide ;
- information `same_as vide` correcte mais encore peu guidante ;
- absence de proposition de cible d'ecriture concrete ;
- reserves peu illustrees par les cas actuels ;
- gestion des alias non testee sur un cas documentaire ambigu dans ce retour.

Limites non observees dans ce retour :

- ecriture accidentelle dans les registres ;
- modification d'export ;
- creation de branche ;
- ouverture automatique de PR ;
- decision historiographique automatique.

## 7. Decision sur l'avenir du prototype

Decision :

A ameliorer avant extension.

Justification :

Le prototype apporte deja une valeur documentaire reelle. Il bloque les erreurs les plus couteuses d'un ajout manuel : source inconnue, categorie invalide, identifiant duplique et collision evidente. Il produit aussi une entree candidate relisible et deterministe.

Cependant, il doit etre ameliore avant d'etre reproduit sur d'autres familles :

- clarifier la cible d'ecriture ;
- reduire les messages redondants ;
- mieux guider le choix de categorie ;
- produire au moins un exemple ou mecanisme clair de `reserve` ;
- documenter plus finement les cas d'alias ambigus.

## 8. Impact sur M2

Le modele PERSON est-il suffisamment mature pour servir de base a d'autres types ?

Reponse :

Oui avec conditions.

Conditions :

- conserver le principe lecture seule pour les prototypes locaux ;
- exiger un schema ou un validateur existant avant extension ;
- documenter les collisions propres a chaque famille ;
- rendre explicite la cible d'ecriture avant tout diff ;
- ne jamais assimiler `pre-validee` a validation humaine ;
- garder une PR humaine comme sortie de gouvernance.

Le prototype confirme que M2 peut produire de la valeur sans interface graphique. Il montre aussi qu'un assistant par type doit etre ancre dans le modele reel du depot, pas dans un modele generique.

## 9. Decision proposee

Faut-il etendre M2.5 a d'autres familles documentaires ?

Decision proposee :

Pas immediatement. Le prototype PERSON doit etre ameliore avant extension.

Apres ces ameliorations, l'extension peut etre envisagee avec prudence. Le premier candidat recommande serait `ORG`, car il s'agit d'une famille d'entites structurees, proche de `PERSON` par ses risques de collision et de categorie, avec un validateur existant.

Cette recommandation ne lance pas le chantier `ORG`. Elle fixe seulement une orientation conditionnelle pour la suite de M2 apres stabilisation du prototype `PERSON`.
