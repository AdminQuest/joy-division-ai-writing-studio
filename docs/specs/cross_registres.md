# Spécification cross-registres — Joy Division AI Writing Studio

> **Version** : 31 mai 2026 (squelette initial)
> **Étape** : 5 (Phase B) — passe de *design*.
> **Statut** : ⚠️ **SPÉCIFICATION DE CONCEPTION — AUCUNE IMPLÉMENTATION.** Les champs, schémas et validateurs décrits ici ne sont pas écrits à ce stade. Ils sont câblés par les refontes (étapes 6-10), chacune pour sa tranche, puis par le maillage profond (étape 11).
> **Référence** : ce document fait foi pour toute liaison entre registres. Une refonte ne crée pas de convention de liaison concurrente ; elle applique, et au besoin étend additivement, la présente spécification.
> **Filiation** : généralise les primitives éprouvées en étape 4 (registre des lieux) — voir `NAMING_CONVENTIONS`.

---

## 1. Modèle à deux couches

Le modèle distingue strictement deux couches, traitées dans cet ordre par tout chargeur :

1. **Couche d'identité** — le champ `same_as` (hérité de l'étape 4). Il déclare l'équivalence d'identité entre un identifiant *legacy* et sa forme canonique. Il est **résolu en premier** : toute cible de lien est évaluée *après* canonicalisation.
2. **Couche de relation** — le champ `liens` (défini ici). Il déclare les relations sémantiques entre entités de registres différents.

> **Encadré — pourquoi deux couches**
> `same_as` répond à la question « ces deux identifiants désignent-ils la même chose ? » ; `liens` répond à « quelle relation cette entité entretient-elle avec une autre ? ». Les confondre obligerait à valider des relations sur des identifiants non encore canonicalisés. En séparant, on garantit que les liens pointent toujours, après résolution, vers une entité canonique unique.

## 2. Classes d'entités et identifiants

**2.1. Schéma uniforme.** Tout identifiant suit la forme `<TYPE>-<SLUG>`, source-agnostique et canonique, selon la règle de slugification déterministe de `NAMING_CONVENTIONS` (§ forme canonique des lieux), généralisée à chaque classe.

| Type | Préfixe | Registre | Rôle dans le graphe |
|---|---|---|---|
| Événement | `EVENT-` | chronologie (ét. 6) | Fondateur — ancre temporelle, peu de liens sortants |
| Personne | `PERSON-` | acteurs (ét. 8) | Nœud central |
| Organisation | `ORG-` | organisations (ét. 9) | Nœud central |
| Lieu | `PLACE-` | lieux (ét. 4 ✅) | Fondateur — cible, peu de liens sortants |
| Concert | `CONCERT-` | concerts (ét. 10) | Contingent riche — nombreux liens sortants |
| Session | `SESSION-` | concerts/sessions (ét. 10) | Contingent |
| Chanson | `SONG-` | chansons (refondu) | Nœud |
| Citation | `QUOTE-` | citations (ét. 7) | Contingent — porte locuteur et sujet |
| Concept | `CONCEPT-` | concepts (ét. 11) | Transversal |

**2.2. Réconciliation des schémas hérités.** Première tâche de chaque refonte : inventorier le schéma d'identifiants réellement en place dans son registre. Là où il diverge de `<TYPE>-<SLUG>`, on **réconcilie par `same_as`, jamais par renommage** (gel des schémas) — manœuvre identique à celle du registre des lieux.

## 3. Format des liens

**3.1. Représentation retenue : liste d'arêtes typées.** Sur l'entité source, un champ optionnel `liens` liste des arêtes. Chaque arête a deux clés obligatoires et des qualificateurs optionnels :

```yaml
liens:
  - predicat: membre_de            # obligatoire — issu du vocabulaire contrôlé (§4)
    cible: ORG-JOY-DIVISION        # obligatoire — identifiant interne <TYPE>-<SLUG>
    debut: 1976                    # optionnel — validité temporelle
    fin: 1980                      # optionnel
    role: bassiste                 # optionnel — qualificateur de rôle
    prudence_methodologique: "…"   # optionnel — réserve
```

**3.2. Règles.**
- `predicat` appartient au vocabulaire contrôlé fermé (§4). Aucun prédicat hors liste.
- `cible` est un identifiant interne ; la résolution `same_as` s'applique avant toute évaluation.
- Les qualificateurs admis (`debut`, `fin`, `role`, `prudence_methodologique`, `reference_croisee`) sont des clés plates : pas de réification d'arête en entité de premier ordre à ce stade.
- `liens` ne contient **que** des relations sémantiques internes. Les autorités externes restent dans `reference_croisee` (préfixées : `wikidata:`, `osm:`, `gias:`…) ; l'identité reste dans `same_as`.

**3.3. Direction et inverses.** L'arête est portée par l'entité **contingente** et pointe vers la **fondatrice** (cf. encadré ci-dessous). L'inverse n'est **pas** stocké : il est reconstruit à la lecture. Pour une relation symétrique, une direction canonique déterministe (ordre lexical des identifiants) fixe le côté unique de stockage.

> **Encadré — règle de direction**
> L'entité la plus composite porte ses liens sortants vers les entités plus fondamentales. Un concert référence son lieu, sa date, ses interprètes, ses morceaux ; le lieu et la date ne référencent personne. La chronologie est la couche la plus profonde — tout s'y ancre, elle ne sort pas de liens. Cette règle protège les nœuds fondateurs (les plus référencés) du *churn*, et préserve la provenance sur l'entité contingente.

## 4. Vocabulaire contrôlé des prédicats

**4.1. Noyau (figé en étape 5).** Matrice des triplets autorisés :

| Prédicat | Source → Cible | Cardinalité | Inverse (reconstruit) | Refonte d'entrée |
|---|---|---|---|---|
| `same_as` | X → X | 0..1 | *(identité, voir §1)* | ét. 4 ✅ |
| `a_pour_lieu` | CONCERT/SESSION → PLACE | 1 | `accueille` | ét. 10 |
| `a_pour_date` | CONCERT/SESSION → EVENT | 1 | `ancre` | ét. 10 |
| `a_pour_interprete` | CONCERT/SESSION → PERSON | 1..n | `a_participe_a` | ét. 10 |
| `a_pour_morceau` | CONCERT → SONG | 0..n | `joue_lors_de` | ét. 10 |
| `a_pour_organisateur` | CONCERT → ORG | 0..n | `organise` | ét. 10 |
| `membre_de` | PERSON → ORG | 0..n | `a_pour_membre` | ét. 8/9 |
| `a_pour_auteur` | SONG → PERSON | 1..n | `auteur_de` | ét. 8 |
| `edite_par` | SONG/ORG → ORG | 0..1 | `edite` | ét. 9 |
| `attribuee_a` | QUOTE → PERSON | 0..1 | `cite` | ét. 7 |
| `porte_sur` | QUOTE → (toute classe) | 0..n | `evoque_par` | ét. 7 |
| `associe_a` | PERSON → PERSON/PLACE | 0..n | `associe_a` *(symétrique)* | ét. 8 |

**4.2. Fiches des prédicats du noyau.** *(modèle ci-dessous ; à compléter prédicat par prédicat lors de la refonte d'entrée correspondante)*

> **`membre_de`**
> Sémantique : appartenance d'une personne à une organisation (groupe, label, collectif).
> Source : PERSON. Cible : ORG. Cardinalité : 0..n. Sens : porté par la personne. Inverse : `a_pour_membre`. Qualificateurs admis : `debut`, `fin`, `role`. Refonte d'entrée : 8 (acteurs) ou 9 (organisations).

> **`a_pour_lieu`**
> Sémantique : localisation d'un concert ou d'une session. Source : CONCERT/SESSION. Cible : PLACE. Cardinalité : 1. Inverse : `accueille`. Qualificateurs : `prudence_methodologique`. Refonte d'entrée : 10.

**4.3. Extension gouvernée.** Une refonte **peut ajouter** des prédicats et des lignes de matrice, sous conditions : ajout additif (jamais de renommage) ; déclaration complète (source-type, cible-type, cardinalité, sens, inverse) ; consignation **dans le présent document** ; aucun chevauchement sémantique avec un prédicat existant. Le vocabulaire reste fermé : tout prédicat employé dans les données figure ici.

## 5. Résolution

Avant toute validation ou tout rendu :
1. canonicaliser les identités via `same_as` (clôture transitive, *union-find*, comme en étape 4) ;
2. évaluer chaque `cible` de lien sur l'identité canonique résolue ;
3. reconstruire les inverses à la lecture pour les usages (graphe, fiches croisées).

## 6. Invariants de validation *(définis ici, implémentés ultérieurement)*

À implémenter par les refontes dans leur validateur, et consolidés à l'étape 11. Numérotés `XR-*` pour ne pas heurter les `INV-1..6` du registre des lieux.

| Code | Invariant | Sévérité |
|---|---|---|
| XR-1 | La cible de tout lien existe, après résolution `same_as`. | Erreur |
| XR-2 | Le type de la cible est compatible avec la cible-type déclarée du prédicat. | Erreur |
| XR-3 | Tout `predicat` employé appartient au vocabulaire contrôlé (§4). | Erreur |
| XR-4 | La cardinalité déclarée est respectée. | Erreur |
| XR-5 | Aucune arête réflexive sur un prédicat non réflexif. | Erreur |
| XR-6 | Les inverses reconstruits sont cohérents (aucune contradiction de sens). | Avertissement |
| XR-7 | Une relation symétrique n'est stockée qu'une fois (côté canonique déterministe). | Avertissement |

## 7. Articulation avec la doctrine et la suite

1. **Gel des schémas.** `liens` est un champ optionnel additif ; son introduction dans chaque registre est un enrichissement rétrocompatible. Aucun identifiant n'est renommé.
2. **Principe directeur n° 2.** La présente spécification précède les refontes ; son implémentation les suit. Elle est l'unique source des conventions de liaison.
3. **Séquencement.** Chaque refonte (6-10) câble sa tranche : déclaration de `liens` au schéma du registre, implémentation des invariants `XR-*` pertinents, peuplement des arêtes dont l'entité est source. L'étape 11 assemble le maillage complet et consolide la validation ; l'étape 13 (graphe) consomme directement `liens` et les inverses reconstruits.

### Conclusion intermédiaire

Cette spécification érige `same_as` — primitive d'équivalence née d'une nécessité de l'étape 4 — en une grammaire complète de liaison : un modèle à deux couches (identité / relation), un format unique d'arête typée, une règle de direction, un vocabulaire contrôlé extensible et une batterie d'invariants. Tout est arrêté au niveau de la conception ; rien n'est implémenté. Le critère de réussite est unique : aucune refonte ultérieure ne devra inventer de convention de liaison.

---

### Points d'extension balisés (à compléter par les refontes)

- [ ] **Étape 7 (citations)** : fiches `attribuee_a`, `porte_sur` ; cible-types admises de `porte_sur`.
- [ ] **Étape 8 (acteurs)** : fiches `a_pour_auteur`, `associe_a` ; direction canonique de `associe_a` PERSON↔PERSON.
- [ ] **Étape 9 (organisations)** : fiches `membre_de`, `edite_par` ; hiérarchies inter-organisations éventuelles.
- [ ] **Étape 10 (concerts/sessions)** : fiches `a_pour_lieu`, `a_pour_date`, `a_pour_interprete`, `a_pour_morceau`, `a_pour_organisateur` ; qualificateurs de setlist (ordre, rappel).
- [ ] **Étape 11 (maillage)** : prédicats transversaux `CONCEPT` ; consolidation des invariants `XR-*` ; vérification globale de cohérence des inverses.
