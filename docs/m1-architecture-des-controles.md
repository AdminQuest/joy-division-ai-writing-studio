# Architecture des controles M1

# Objet du document

M1 dispose maintenant d'un premier controle implemente, DM -> atomes, et de plusieurs controles futurs deja identifies ou specifies. Avant de multiplier les scripts, rapports et indicateurs, une architecture commune devient necessaire.

Cette architecture doit eviter que chaque controle M1 invente son propre vocabulaire, son propre format de sortie, sa propre logique de statut ou son propre mode d'integration. Elle doit aussi proteger l'invariant M1 : un controle etablit des constats, mais ne corrige pas le corpus.

Stabiliser le modele avant de poursuivre l'implementation permet :

- de garder les controles comparables entre eux ;
- de preparer l'agregation des resultats sans dependance fragile ;
- de distinguer clairement controle, rapport, tableau de bord et decision humaine ;
- de limiter les effets de bord sur les documents maitres, registres, exports et roadmaps ;
- de faciliter les futures revues de PR.

Ce document prepare aussi les futurs tableaux de bord M1. Un tableau de bord ne doit pas recalculer directement toute la qualite documentaire : il devra s'appuyer sur des rapports de controles, eux-memes produits de facon reproductible et non destructive.

Ce document ne cree aucun controle, aucun script et aucun tableau de bord. Il definit uniquement l'architecture cible de cohabitation des controles M1.

# Principes

## Lecture seule

Un controle M1 doit lire les objets documentaires qu'il controle sans les modifier.

Objets proteges :

- documents maitres ;
- atomes ;
- registres ;
- sources ;
- exports ;
- manifestes ;
- roadmaps ;
- documents de doctrine.

Une PR de controle peut produire ou mettre a jour son propre rapport regenerable, mais elle ne doit pas corriger le corpus ni modifier les artefacts qu'elle controle.

## Aucune correction automatique

Un controle M1 produit des constats :

- presence ;
- absence ;
- divergence ;
- incoherence ;
- statut suspect ;
- limite methodologique.

La correction d'un ecart doit rester une PR separee, avec un perimetre explicite. Le controle ne doit jamais modifier un document maitre, un registre, un export, un atome ou une source pour faire disparaitre une alerte.

## Separation controle / rapport

Le controle est le mecanisme de verification.

Le rapport est l'artefact documentaire lisible qui expose les resultats.

Cette separation permet :

- de relancer le controle sans modifier sa logique ;
- de comparer les rapports dans le temps ;
- de faire relire les constats sans executer le code ;
- de preparer une future agregation.

## Reproductibilite

Un rapport M1 doit etre regenerable a partir de l'etat courant du depot et du controle qui le produit.

Le rapport doit indiquer :

- le controle concerne ;
- le perimetre controle ;
- les limites connues ;
- les resultats observes ;
- les ecarts detectes.

## Generation canonique

Lorsqu'un rapport M1 est produit par un script, ce script devient son producteur technique attendu.

Le rapport ne doit pas etre corrige manuellement si le controle est deja implemente. En cas d'ecart dans un rapport genere, la PR doit soit regenerer le rapport avec le producteur canonique, soit signaler pourquoi la regeneration n'est pas dans le perimetre.

## Agregation independante

L'agregation future ne doit pas etre integree directement dans chaque controle.

Chaque controle doit produire un resultat exploitable par un humain et, si necessaire plus tard, par un agregateur. L'agregateur devra lire les rapports ou formats d'echange, mais ne devra pas remplacer les controles.

## Absence d'effet de bord

Un controle M1 ne doit pas :

- regenerer les documents maitres ;
- regenerer les exports ;
- modifier les registres ;
- modifier les sources ;
- modifier la roadmap ;
- lancer un chantier M2 ;
- declencher une correction automatique ;
- integrer silencieusement un nouveau workflow CI.

# Modele M1

La chaine cible M1 est la suivante :

```text
Controle
↓
Rapport
↓
Agregation
↓
Tableau de bord
```

## Controle

Le controle execute une verification limitee et explicite.

Il definit :

- une question de controle ;
- un perimetre ;
- des entrees ;
- une methode ;
- des types d'ecarts ;
- une grille de statut ou de gravite ;
- des limites.

Exemple deja implemente : `tools/check_dm_atoms_traceability.py`.

Exemple specifie mais non implemente dans cette PR : DM -> registres.

## Rapport

Le rapport expose les resultats du controle.

Il doit etre lisible sans executer le script. Il doit separer le resultat global, les ecarts, les limites et les conclusions.

Exemple deja present : `reports/m1/dm_atoms_traceability.md`.

## Agregation

L'agregation future consolidera plusieurs rapports ou resultats de controles.

Elle pourra produire :

- une vue globale des statuts ;
- des indicateurs transversaux ;
- une liste d'ecarts ouverts ;
- des tendances si des historiques sont conserves.

L'agregation n'est pas creee dans cette PR.

## Tableau de bord

Le tableau de bord M1 presentera les indicateurs de qualite documentaire.

Il devra s'appuyer sur les resultats des controles et de l'agregation future. Il ne devra pas devenir un controle cache ni une source documentaire.

Le tableau de bord n'est pas construit dans cette PR.

# Convention de nommage

## Scripts

Les scripts de controle M1 devraient etre places sous `tools/` avec un nom explicite.

Convention proposee :

```text
tools/check_<objet>_<relation>_<objectif>.py
```

Exemples :

- `tools/check_dm_atoms_traceability.py` ;
- `tools/check_dm_registers_consistency.py` ;
- `tools/check_dm_exports_traceability.py` ;
- `tools/check_dm_sources_traceability.py`.

Regles de nommage :

- commencer par `check_` pour signaler un controle non destructif ;
- nommer l'objet controle, par exemple `dm` ;
- nommer la cible, par exemple `atoms`, `registers`, `exports`, `sources` ;
- nommer l'objectif principal, par exemple `traceability`, `consistency`, `freshness` ;
- eviter les noms generiques comme `audit.py` ou `control.py` ;
- ne pas reutiliser le nom d'un script de generation pour un controle.

## Rapports

Les rapports M1 devraient etre places sous :

```text
reports/m1/
```

Convention proposee :

```text
reports/m1/<objet>_<relation>_<objectif>.md
```

Exemples :

- `reports/m1/dm_atoms_traceability.md` ;
- `reports/m1/dm_registers_consistency.md` ;
- `reports/m1/dm_exports_traceability.md`.

Regles de nommage :

- reprendre le vocabulaire du script producteur ;
- utiliser des noms stables et descriptifs ;
- reserver `.md` au rapport humain ;
- reserver d'eventuels `.json` ou `.csv` aux formats d'echange futurs ;
- ne pas stocker les rapports M1 dans `docs/`, qui reste l'espace de cadrage et de doctrine.

## Documents de cadrage

Les documents de conception M1 restent sous :

```text
docs/
```

Convention proposee :

```text
docs/m1-<objet-ou-sujet>.md
```

Exemples :

- `docs/m1-controle-p0-dm-vers-atomes.md` ;
- `docs/m1-controle-p0-dm-vers-registres.md` ;
- `docs/m1-architecture-des-controles.md`.

# Structure cible

La structure cible distingue les roles au lieu de tout melanger.

```text
tools/
reports/m1/
docs/
```

## `tools/`

Rôle : scripts executables de verification, generation ou audit.

Pour M1, les scripts de controle doivent :

- rester en lecture seule sur le corpus ;
- produire des constats ;
- ecrire uniquement leur rapport attendu, si un rapport est prevu ;
- refuser les chemins de sortie dangereux ;
- etre testables localement ;
- ne pas etre automatiquement integres au build global sans decision dediee.

## `reports/m1/`

Rôle : rapports regenerables des controles M1.

Un rapport M1 doit etre considere comme une vue de controle, pas comme une source ni comme un registre.

Les rapports M1 peuvent etre versionnes lorsque leur contenu sert a la revue documentaire. S'ils sont produits par script, ils doivent etre regeneres par le script canonique, pas corriges manuellement.

## `docs/`

Rôle : doctrine, cadrage, architecture et decisions documentaires.

Les documents sous `docs/` definissent :

- les objectifs M1 ;
- les defaillances ;
- les controles attendus ;
- les architectures ;
- les limites ;
- les decisions de perimetre.

Ils ne doivent pas contenir les resultats regenerables d'un controle lorsque ces resultats appartiennent a `reports/m1/`.

# Format des rapports

Un rapport M1 doit contenir au minimum les sections suivantes.

## Objet

La section indique :

- le controle concerne ;
- la question de controle ;
- le producteur technique si le controle est implemente ;
- la date ou le contexte d'execution si pertinent.

## Perimetre

La section precise :

- les objets controles ;
- les fichiers lus ;
- les familles ou champs couverts ;
- les exclusions explicites.

## Resume global

La section donne une vue synthetique.

Format recommande :

```text
| Indicateur | Valeur |
|------------|--------|
```

Le resume doit permettre de comprendre rapidement si le controle a trouve des ecarts.

## Resultats

La section presente les resultats par unite controlee.

Exemples d'unites :

- document maitre ;
- registre ;
- export ;
- livrable ;
- famille documentaire.

## Ecarts

La section liste les ecarts detectes avec :

- type d'ecart ;
- objet concerne ;
- preuve ou champ observe ;
- gravite si disponible ;
- recommandation documentaire eventuelle.

## Limites

La section doit separer clairement :

- ce qui n'est pas controle ;
- ce qui pourrait produire des faux positifs ;
- ce qui necessite une verification humaine ;
- ce qui releve d'un controle futur.

Une limite methodologique ne doit pas etre presentee comme une defaillance demontree.

## Conclusion

La section repond explicitement a la question de controle.

Elle doit indiquer :

- le statut global ;
- le caractere bloquant ou non des ecarts ;
- les suites M1 possibles ;
- les sujets hors perimetre.

# Format d'echange futur

## Markdown

Recommande pour les rapports humains.

Le Markdown est adapte pour :

- revue de PR ;
- lecture documentaire ;
- synthese des ecarts ;
- conservation dans `reports/m1/`.

Le Markdown doit rester le format principal tant que les controles M1 sont peu nombreux.

## JSON

Optionnel pour les futurs besoins d'agregation.

Le JSON pourrait contenir :

- identifiant du controle ;
- version ou date d'execution ;
- statut global ;
- indicateurs numeriques ;
- liste structuree des ecarts ;
- chemins des objets concernes.

Ce format est premature dans cette PR. Il devra etre defini lorsque l'agregateur sera decide.

## CSV

Optionnel pour les listes tabulaires simples.

Le CSV pourrait etre utile pour :

- ecarts exportables ;
- suivi manuel ;
- comparaison de listes ;
- exploration ponctuelle.

Il ne doit pas remplacer le rapport Markdown.

## Recommandation actuelle

Pour l'etat actuel de M1 :

- Markdown : recommande ;
- JSON : optionnel mais premature ;
- CSV : optionnel pour des listes futures ;
- schema formel commun : premature.

# Agregation

L'agregation future devra repondre a plusieurs questions.

## Un rapport par controle ?

Oui, par defaut.

Chaque controle doit produire son propre rapport pour garder :

- un perimetre clair ;
- une responsabilite technique claire ;
- une relecture humaine simple ;
- une evolution independante.

## Un rapport consolide ?

Possible plus tard.

Un rapport consolide pourrait synthétiser :

- les statuts par controle ;
- les ecarts ouverts ;
- les controles non executes ;
- les indicateurs transversaux.

Il ne doit pas remplacer les rapports sources.

## Indicateurs globaux

Les indicateurs globaux pourraient inclure :

- nombre de controles M1 executes ;
- nombre de documents maitres controles ;
- nombre d'ecarts detectes ;
- nombre d'ecarts bloquants ;
- nombre de documents maitres tracables ;
- nombre de divergences DM / registres ;
- nombre d'artefacts desynchronises ;
- nombre de livrables non qualifies.

Ces indicateurs devront etre rattaches a leur controle producteur.

## Stockage des resultats

Options futures :

- conserver uniquement les rapports Markdown ;
- ajouter des fichiers JSON par controle ;
- produire un fichier consolide sous `reports/m1/` ;
- alimenter un tableau de bord documentaire.

Decision actuelle : ne pas creer d'agregateur et ne pas definir de schema obligatoire avant d'avoir au moins plusieurs controles M1 stabilises.

# Tableau de bord M1

Le futur tableau de bord M1 devra consommer les resultats de controles plutot que recalculer toute la logique documentaire.

Il pourra s'appuyer sur :

- rapports Markdown pour la lecture humaine ;
- eventuels formats JSON pour l'agregation ;
- conventions de statuts et de gravite ;
- indicateurs definis dans `docs/m1-tableau-de-bord-qualite.md`.

Le tableau de bord devra distinguer :

- controles executes ;
- controles non encore implementes ;
- resultats sans ecart ;
- ecarts bloquants ;
- ecarts non bloquants ;
- limites methodologiques ;
- sujets reportes.

Cette PR ne construit pas le tableau de bord. Elle prepare seulement les regles de cohabitation qui permettront de l'alimenter plus tard.

# Integration future

Les controles M1 peuvent etre integres de plusieurs manieres, chacune devant faire l'objet d'une PR dediee.

## Execution manuelle

Option initiale recommandee.

Elle permet :

- de stabiliser le controle ;
- de relire les rapports ;
- de reduire les faux positifs ;
- d'eviter une CI bruyante tant que les formats ne sont pas stabilises.

## Build local

Option possible apres stabilisation.

Un build local pourrait executer plusieurs controles M1, mais seulement lorsque :

- les rapports sont stables ;
- les sorties sont reproductibles ;
- les echecs sont clairement interpretes ;
- les controles n'ont pas d'effet de bord.

## CI

Option possible mais non decidee.

La CI pourrait verifier que certains controles restent verts. Elle ne doit pas etre activee tant que les criteres bloquants et non bloquants ne sont pas arbitres.

## GitHub Actions

Option future.

Un workflow GitHub Actions pourrait executer un ou plusieurs controles M1, mais cette integration devra preciser :

- les controles inclus ;
- les conditions d'echec ;
- les artefacts conserves ;
- la relation avec `tools/check_generated_sync.py` ;
- la responsabilite des corrections.

Aucune integration n'est realisee dans cette PR.

# Hors perimetre

Les sujets suivants sont explicitement hors perimetre :

- nouveaux controles ;
- implementation de DM -> registres ;
- implementation de DM -> sources ;
- implementation de DM -> exports ;
- modification de `tools/check_dm_atoms_traceability.py` ;
- modification de rapports existants ;
- creation d'un agregateur ;
- creation d'un tableau de bord ;
- modification de `build_all.py` ;
- modification de GitHub Actions ;
- Cloudflare ;
- M2 ;
- enrichissement documentaire ;
- formulaires ;
- nouvelles applications ;
- correction du corpus ;
- correction des documents maitres ;
- correction des registres ;
- correction des exports ;
- modification de la roadmap.

# Conclusion

L'architecture M1 est suffisamment stable pour poursuivre l'implementation progressive des controles, sous reserve de conserver des PR separees pour chaque composant technique.

Les principes principaux sont poses :

- controles en lecture seule ;
- rapports regenerables ;
- separation entre controle, rapport, agregation et tableau de bord ;
- absence de correction automatique ;
- conventions de nommage ;
- integration future non automatique.

Il reste des arbitrages, mais ils ne bloquent pas la suite immediate :

- format JSON eventuel ;
- schema d'agregation ;
- criteres CI ;
- seuils bloquants ;
- forme exacte du tableau de bord.

Ces arbitrages doivent etre traites plus tard, lorsque plusieurs controles M1 auront produit des rapports comparables. A ce stade, l'architecture commune suffit pour continuer sans ouvrir M2.
