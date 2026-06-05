# Architecture de l'agregation M1

# Objet du document

L'agregation M1 devient necessaire parce que les controles documentaires vont se multiplier. Le projet dispose deja d'un premier controle implemente, DM -> atomes, et plusieurs controles futurs sont specifies ou identifies. Sans modele commun d'agregation, chaque controle risquerait de produire des statuts, gravites et indicateurs difficiles a comparer.

L'agregation doit etre definie avant la multiplication des controles pour trois raisons :

- eviter que les rapports individuels restent isoles ;
- permettre une lecture transversale des ecarts M1 ;
- preparer le futur tableau de bord sans transformer celui-ci en controle cache.

L'agregation ne remplace pas les controles individuels. Elle consolide leurs constats afin de repondre a des questions globales : quels controles existent, lesquels ont ete executes, quels ecarts restent ouverts, quels objets sont les plus touches et quelles defaillances M1 reviennent le plus souvent.

Ce document ne cree aucun script, aucun controle, aucun rapport consolide et aucun tableau de bord. Il definit uniquement l'architecture documentaire de l'agregation future.

# Positionnement

La chaine cible M1 reste :

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

Un controle execute une verification limitee et explicite.

Il definit :

- une question de controle ;
- un perimetre ;
- des entrees ;
- une methode ;
- des types d'ecarts ;
- des statuts ou gravites ;
- des limites.

Exemple existant : `tools/check_dm_atoms_traceability.py`.

Exemples non implementes dans cette PR : DM -> registres, DM -> sources, DM -> exports.

## Rapport

Un rapport expose les resultats d'un controle donne.

Il doit rester le lieu du detail :

- perimetre exact ;
- resultats par objet controle ;
- ecarts detectes ;
- limites methodologiques ;
- faux positifs possibles ;
- conclusion du controle.

Exemple existant : `reports/m1/dm_atoms_traceability.md`.

## Agregation

L'agregation consolide les resultats de plusieurs rapports.

Elle doit permettre une lecture transversale :

- statuts par controle ;
- ecarts ouverts ;
- ecarts bloquants ;
- objets les plus touches ;
- familles de defaillances M1 ;
- limites recurrentes.

L'agregation ne doit pas recalculer elle-meme la logique metier des controles. Elle doit reprendre les resultats declares par les rapports ou par de futurs formats d'echange.

## Tableau de bord

Le futur tableau de bord M1 presentera les indicateurs globaux issus de l'agregation.

Il devra afficher des signaux de pilotage :

- controles executes ou non ;
- ecarts ouverts ;
- statuts consolides ;
- tendances ;
- zones de risque documentaire.

Le tableau de bord ne doit pas devenir une source, une preuve ou un controle autonome. Il ne sera pas construit dans cette PR.

# Principes

## Aucune correction automatique

L'agregation ne corrige aucun ecart.

Elle ne doit pas :

- modifier les documents maitres ;
- modifier les registres ;
- modifier les exports ;
- modifier les atomes ;
- modifier les rapports individuels ;
- declencher une regeneration ;
- masquer un ecart en le reclassant sans preuve.

## Lecture seule

L'agregation future devra lire les rapports et, si un format structure est defini plus tard, les fichiers d'echange associes.

Elle ne doit pas lire directement le corpus pour refaire les controles a la place des controles specialises.

## Agregation des constats

L'agregation consolide des constats deja produits :

- statut d'un controle ;
- statut d'un objet controle ;
- type d'ecart ;
- gravite ;
- limite methodologique ;
- reserve ;
- indicateur numerique.

Elle ne doit pas inventer un ecart qui n'apparait dans aucun controle.

## Reproductibilite

Un futur rapport consolide M1 devra etre reproductible a partir :

- des rapports individuels disponibles ;
- d'eventuels formats d'echange futurs ;
- d'une regle d'agregation documentee.

Si un rapport individuel manque ou est obsolet, l'agregation devra le signaler au lieu d'en supposer le contenu.

## Independance des controles

Chaque controle M1 doit pouvoir evoluer sans casser l'ensemble de l'agregation.

L'agregation doit donc s'appuyer sur un socle commun minimal :

- identifiant du controle ;
- statut global ;
- liste d'ecarts ;
- gravites ;
- perimetre ;
- limites.

Elle ne doit pas imposer un schema complexe avant que plusieurs controles soient stabilises.

## Tracabilite des resultats

Chaque resultat consolide doit pouvoir etre rattache a son rapport source.

L'agregation devra conserver :

- le nom du controle ;
- le chemin du rapport ;
- l'objet concerne ;
- le type d'ecart ;
- la gravite ;
- la preuve ou le champ de reference lorsque disponible.

Un indicateur global sans origine verifiable ne doit pas etre considere comme exploitable.

# Questions auxquelles doit repondre l'agregation

L'agregation future devra permettre de repondre aux questions suivantes.

## Etat des controles

- Combien de controles M1 existent ?
- Combien sont documentes seulement ?
- Combien sont implementes ?
- Combien ont ete executes ?
- Combien ont produit un rapport disponible ?
- Combien sont non executes, obsoletes ou non applicables ?

## Etat des resultats

- Combien de controles sont conformes ?
- Combien sont conformes avec reserve ?
- Combien presentent des ecarts ?
- Combien presentent des ecarts bloquants ?
- Combien presentent seulement des ecarts mineurs ou informationnels ?

## Etat des objets documentaires

- Quels documents maitres sont les plus touches ?
- Quels registres sont les plus touches ?
- Quels exports sont les plus touches ?
- Quels livrables ou rapports presentent des reserves recurrentes ?
- Quels objets apparaissent dans plusieurs ecarts ?

## Etat des defaillances M1

- Quelles defaillances M1 sont les plus frequentes ?
- Les ecarts relevent-ils plutot de la tracabilite, de la derivabilite, de l'obsolescence, de la coherence documentaire, du statut documentaire ou de la generation ?
- Les limites methodologiques concernent-elles un controle particulier ou un probleme transversal ?

# Modele d'agregation

## Ce qui est agrege

L'agregation peut consolider :

- statuts de controles ;
- statuts par objet controle ;
- ecarts detectes ;
- gravites ;
- indicateurs numeriques ;
- limites ;
- reserves methodologiques ;
- familles de defaillances M1 ;
- chemins des rapports sources ;
- date ou contexte d'execution si disponible.

## Ce qui ne doit pas etre agrege

L'agregation ne doit pas consolider :

- les contenus redactionnels des documents maitres ;
- les citations completes ;
- les textes sources ;
- les details volumineux deja presents dans un rapport individuel ;
- les hypotheses non qualifiees ;
- les faux positifs non confirmes ;
- les corrections recommandees comme si elles etaient deja realisees.

## Niveau de detail

L'agregation doit rester un niveau de synthese.

Le detail probatoire reste dans les rapports individuels. Le rapport consolide doit pointer vers ces rapports au lieu de recopier toutes les preuves.

# Statuts consolides

Les statuts consolides doivent permettre de comparer des controles differents sans effacer leurs specificites.

| Statut | Definition |
| --- | --- |
| Conforme | Le controle a ete execute et ne signale aucun ecart dans son perimetre. |
| Conforme avec reserve | Le controle ne signale pas d'ecart bloquant, mais documente une limite methodologique, un perimetre incomplet ou une reserve non bloquante. |
| Ecart mineur | Le controle signale au moins un ecart mineur sans ecart majeur ni bloquant. |
| Ecart majeur | Le controle signale au moins un ecart majeur, mais aucun ecart bloquant. |
| Bloquant | Le controle signale au moins un ecart qui empeche de considerer l'objet controle comme fiable dans le perimetre du controle. |
| Non execute | Le controle existe ou est attendu, mais aucun resultat courant n'est disponible. |

## Regle de consolidation

Par defaut, le statut consolide d'un controle doit suivre l'ecart le plus grave observe.

Ordre de priorite :

1. Bloquant ;
2. Ecart majeur ;
3. Ecart mineur ;
4. Conforme avec reserve ;
5. Conforme ;
6. Non execute.

`Non execute` est un statut d'absence de resultat, pas une preuve de conformite.

# Gravites consolidees

Les gravites consolidees reprennent la grille M1 commune.

| Gravite | Definition consolidee |
| --- | --- |
| Bloquant | L'ecart empeche de considerer un controle, un objet documentaire ou un livrable comme fiable dans le perimetre audite avant decision. |
| Majeur | L'ecart affecte un objet conserve, canonique ou fortement reutilise, mais peut etre isole ou traite dans une PR dediee. |
| Mineur | L'ecart est local, secondaire, non bloquant ou limite a une information peu structurante. |
| Informationnel | Le constat ameliore la comprehension du depot, du controle ou de ses limites sans exiger de correction immediate. |

## Utilisation par les controles

Chaque controle doit :

- qualifier ses ecarts avec une gravite lorsque c'est possible ;
- expliquer les criteres de gravite propres a son perimetre ;
- distinguer reserve methodologique et defaillance demontree ;
- eviter de promouvoir automatiquement une limite en ecart.

L'agregation ne doit pas durcir la gravite sans preuve issue du rapport individuel.

# Rapport consolide M1

Un futur rapport consolide M1 pourrait etre produit sous :

```text
reports/m1/
```

Nom possible :

```text
reports/m1/m1_controls_summary.md
```

Ce rapport n'est pas cree dans cette PR.

## Resume global

Le resume global devrait presenter :

- nombre total de controles connus ;
- nombre de controles executes ;
- nombre de controles non executes ;
- nombre de controles conformes ;
- nombre de controles avec reserve ;
- nombre de controles avec ecarts ;
- nombre d'ecarts bloquants.

## Controles executes

Cette section devrait lister :

- controle ;
- rapport source ;
- statut consolide ;
- nombre d'ecarts ;
- gravite maximale ;
- date ou contexte si disponible.

## Ecarts ouverts

Cette section devrait consolider les ecarts non resolus.

Elle devrait indiquer :

- type d'ecart ;
- gravite ;
- objet touche ;
- controle source ;
- rapport source ;
- action ou suite documentaire possible.

## Ecarts bloquants

Cette section devrait isoler les ecarts bloquants pour permettre une decision rapide.

S'il n'y en a pas, le rapport devrait le dire explicitement.

## Limites

Cette section devrait consolider :

- controles incomplets ;
- controles non executes ;
- rapports manquants ;
- limites methodologiques recurrentes ;
- familles hors perimetre.

## Tendances

Cette section est optionnelle et prematuree tant que les resultats ne sont pas historises.

Elle pourrait plus tard indiquer :

- evolution du nombre d'ecarts ;
- evolution des ecarts bloquants ;
- controles devenus stables ;
- controles devenus obsoletes.

# Indicateurs globaux

Les indicateurs suivants pourraient etre calcules plus tard.

## Indicateurs de controles

- nombre de controles M1 connus ;
- nombre de controles documentes ;
- nombre de controles implementes ;
- nombre de controles executes ;
- nombre de controles non executes ;
- nombre de rapports disponibles ;
- nombre de rapports manquants.

## Indicateurs d'ecarts

- nombre total d'ecarts ;
- nombre d'ecarts bloquants ;
- nombre d'ecarts majeurs ;
- nombre d'ecarts mineurs ;
- nombre de constats informationnels ;
- nombre de reserves methodologiques ;
- nombre d'ecarts par type de defaillance M1.

## Indicateurs d'objets

- nombre de documents maitres tracables ;
- nombre de documents maitres avec reserve ;
- nombre de documents maitres avec ecart ;
- nombre de divergences DM / registres ;
- nombre de divergences DM / exports ;
- nombre de divergences DM / sources ;
- nombre d'artefacts desynchronises ;
- nombre de livrables non qualifies.

## Indicateurs de pilotage

- nombre d'ecarts ouverts ;
- nombre d'ecarts consideres comme non bloquants ;
- nombre d'ecarts necessitant une PR dediee ;
- nombre de controles a reexecuter ;
- nombre de controles a definir.

Ces indicateurs ne sont pas calcules dans cette PR.

# Relations avec les rapports individuels

## Ce qui reste dans les rapports individuels

Les rapports individuels doivent conserver :

- la methode detaillee ;
- le perimetre exact ;
- les resultats par objet ;
- les preuves ;
- les faux positifs possibles ;
- les limites propres au controle ;
- les recommandations documentaires detaillees.

## Ce qui remonte dans l'agregation

L'agregation doit remonter :

- identifiant du controle ;
- chemin du rapport ;
- statut global ;
- gravite maximale ;
- nombre d'ecarts ;
- liste courte des ecarts ouverts ;
- objets touches ;
- familles de defaillances M1 ;
- limites ou reserves structurantes.

## Ce qui ne doit jamais etre remonte

L'agregation ne doit jamais remonter comme indicateur global :

- une hypothese non qualifiee ;
- une correction suggeree comme si elle etait appliquee ;
- un succes CI non atteste par le contexte disponible ;
- un contenu source ou citation longue ;
- une interpretation redactionnelle ;
- une limite methodologique qualifiee a tort comme defaillance demontree.

# Preparation du futur tableau de bord

## Ce qui devra etre visible

Le futur tableau de bord M1 devrait afficher :

- controles connus ;
- controles executes ;
- statuts consolides ;
- ecarts ouverts ;
- ecarts bloquants ;
- indicateurs globaux ;
- controles non executes ;
- rapports manquants ;
- reserves methodologiques structurantes.

## Ce qui devra rester dans les rapports detailles

Les rapports detailles devront conserver :

- preuves ;
- listes completes d'objets ;
- observations par document maitre ou registre ;
- contexte methodologique ;
- faux positifs ;
- explications de perimetre.

## Ce qui devra rester dans les controles

Les controles devront conserver :

- logique de verification ;
- extraction ;
- comparaison ;
- qualification initiale ;
- production du rapport individuel.

Le tableau de bord ne doit pas executer les controles a leur place.

# Cas limites

## Controles non executes

Un controle non execute doit etre signale comme `Non execute`.

Il ne doit pas etre considere comme conforme.

## Controles obsoletes

Un controle peut devenir obsolete si :

- son perimetre ne correspond plus aux documents M1 ;
- son rapport n'a pas ete regenere apres changement important ;
- ses entrees ont change de format ;
- sa logique a ete remplacee par un controle plus recent.

L'agregation devra signaler l'obsolescence au lieu de reutiliser silencieusement le resultat.

## Rapports manquants

Un rapport attendu mais absent doit etre signale comme limite ou ecart de couverture, selon la maturite du controle.

Il ne doit pas bloquer automatiquement M1 tant qu'aucune regle de blocage n'a ete decidee.

## Controles contradictoires

Deux controles peuvent produire des constats differents sur le meme objet.

L'agregation ne doit pas arbitrer seule la contradiction. Elle doit :

- signaler les controles concernes ;
- pointer vers les rapports sources ;
- qualifier la contradiction comme sujet de revue humaine ;
- eviter de masquer l'un des deux constats.

## Reserves methodologiques

Une reserve methodologique doit rester distincte d'un ecart demontre.

Exemple : absence de tracabilite passage par passage peut limiter le niveau de confiance sans prouver qu'un passage precis est non tracable.

## Faux positifs

Les faux positifs doivent rester rattaches au controle qui les produit.

L'agregation peut les compter seulement si le rapport individuel les qualifie explicitement comme tels.

# Hors perimetre

Les sujets suivants sont explicitement hors perimetre :

- nouveaux controles ;
- implementation de DM -> registres ;
- implementation de DM -> sources ;
- implementation de DM -> exports ;
- scripts d'agregation ;
- rapport consolide genere ;
- tableau de bord ;
- GitHub Actions ;
- CI ;
- Cloudflare ;
- M2 ;
- nouvelles applications ;
- enrichissement documentaire ;
- formulaires ;
- correction du corpus ;
- correction des documents maitres ;
- correction des registres ;
- correction des exports ;
- modification de la roadmap.

# Conclusion

L'architecture de l'agregation est suffisamment definie pour permettre l'implementation du controle DM -> registres dans une PR separee.

Elle fixe :

- la place de l'agregation dans la chaine M1 ;
- les principes de lecture seule et d'absence de correction automatique ;
- les statuts consolides ;
- les gravites consolidees ;
- le role futur d'un rapport consolide ;
- les relations entre rapports individuels, agregation et tableau de bord.

Elle permet aussi de preparer la creation ulterieure d'un rapport consolide M1, mais ne suffit pas encore a l'implementer. Il restera a arbitrer, dans une PR dediee :

- le format d'echange structure eventuel ;
- le nom exact du rapport consolide ;
- le mode de collecte des rapports individuels ;
- les criteres de blocage ;
- l'integration eventuelle au build local ou a la CI.

Ces arbitrages ne bloquent pas la poursuite de M1. Ils devront toutefois etre traites avant de construire un tableau de bord M1 ou un mecanisme d'agregation executable.
