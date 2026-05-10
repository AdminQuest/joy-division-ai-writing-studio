# Doctrine — Consolidation des registres de références et de citations

Ce document corrige une ambiguïté importante : les fichiers historiques de références et de citations ne sont pas plus canoniques que les fichiers issus de l’atomisation.

Ils sont des documents de travail, au même titre que les atomes, les citations candidates, les registres générés et les exports.

La vérité documentaire du repo ne doit pas être confondue avec l’origine d’un fichier. Elle résulte d’une **consolidation critique**.

---

## 1. Principe général

Le repo contient plusieurs familles de matériaux :

```text
sources/<source>/...                  atomisations par source
sources/<source>/citations_exactes.md citations candidates locales
registers/...                         registres transversaux de travail
data/registre.json                    registre central d’affichage des sources
exports/generated/...                 exports régénérables
fichiers historiques importés          anciens registres de travail, si présents
```

Aucune famille n’est canoniquement supérieure par nature.

Le caractère canonique doit être attribué **après fusion, arbitrage et validation**, non en fonction de l’ancienneté ou du mode de production du fichier.

---

## 2. Ce que signifie « consolider »

Consolider ne signifie pas recopier un registre historique dans le repo.

Consolider signifie :

1. comparer les références issues des anciens documents de travail avec celles issues de l’atomisation ;
2. détecter les doublons, divergences, erreurs, lacunes et changements d’identifiants ;
3. arbitrer un identifiant unique `SXX` pour chaque source réellement retenue ;
4. conserver les anciens identifiants comme `legacy_id` lorsqu’ils existent ;
5. distinguer les références complètes, les références incomplètes et les sources à vérifier ;
6. distinguer les citations candidates des citations validées ;
7. produire des exports propres pour les interfaces.

---

## 3. Références : cible fonctionnelle

La cible fonctionnelle est un registre consolidé des références.

Fichier recommandé :

```text
registers/references/master_references.md
```

Ce fichier ne doit pas être une simple copie de l’ancien registre des références.

Il doit fusionner :

```text
data/registre.json
sources/*/source.md
sources/*/README.md
anciens registres de références, s’ils sont fournis comme matériaux de travail
références issues des documents maîtres de chapitres, si elles sont importées
```

Chaque entrée doit contenir, si disponible :

```yaml
id: SXX
legacy_id:
  - SYY
auteur: Auteur complet
titre: Titre complet
annee: Année
reference_complete: Référence bibliographique complète
source_label: "SXX — Auteur, Titre court, Année"
nature: livre | article | entretien | archive | site | film | documentaire | autre
statut: verifie | a_verifier | a_consolider
fiabilite: forte | moyenne | faible
usage:
  - usage documentaire
chapitres:
  - Chapitre N
source_origin:
  - atomisation
  - registre historique
  - document maître
arbitrage: "Décision de consolidation"
```

---

## 4. Citations : cible fonctionnelle

La cible fonctionnelle est un registre consolidé des citations.

Fichier recommandé :

```text
registers/quotes/master_quotes.md
```

Ce fichier ne doit pas être une simple copie de l’ancien fichier de citations.

Il doit fusionner :

```text
sources/*/citations_exactes.md
anciens fichiers de citations, s’ils sont fournis comme matériaux de travail
citations repérées dans les documents maîtres
citations ajoutées lors des contrôles de chapitres
```

Deux statuts doivent être strictement distingués :

```text
candidate      citation repérée, utile, mais pas encore validée pour le manuscrit
verified       citation vérifiée, sourcée et utilisable dans le manuscrit
rejected       citation écartée ou remplacée
```

Modèle recommandé :

```yaml
id: SXX-Q001
source_id: SXX
legacy_id:
  - ancien identifiant éventuel
source_label: "SXX — Auteur, Titre court, Année"
citation_originale: "Texte original court"
langue_originale: en | fr | autre
traduction_litterale_fr: "..."
traduction_editoriale_fr: "..."
page_pdf: 12
page_imprimee: 10
statut_consolidation: candidate | verified | rejected
statut_verification: verifie | a_reverifier | a_verifier
atomes_lies:
  - SXX-A001
chapitres:
  - Chapitre N
usage_recommande: "..."
risques: "..."
source_origin:
  - atomisation
  - registre historique
arbitrage: "Décision de consolidation"
```

---

## 5. Règle sur les identifiants divergents

Lorsqu’une même source possède deux identifiants, il ne faut pas renommer brutalement tous les fichiers.

Procédure :

1. repérer les identifiants concurrents ;
2. choisir un identifiant canonique pour le repo ;
3. conserver les autres comme `legacy_id` ;
4. signaler la décision dans le registre consolidé ;
5. ne migrer les fichiers sources que par script ou opération dédiée.

Exemple :

```yaml
id: S72
legacy_id:
  - S20
source_label: "S72 — Reynolds, Rip It Up and Start Again, 2005/2006"
arbitrage: "S72 conservé comme identifiant repo ; S20 conservé comme identifiant historique issu des anciens documents de travail."
```

Cette méthode évite la casse dans les atomes, les citations, les exports et les interfaces.

---

## 6. Rôle de `data/registre.json`

`data/registre.json` reste utile pour les interfaces.

Mais il ne doit pas être traité comme registre intellectuel complet.

Son rôle est :

```text
fournir des libellés propres aux interfaces ;
permettre les filtres par source ;
stabiliser l’affichage SXX — Auteur, Titre court, Année.
```

À terme, il peut être généré depuis `registers/references/master_references.md`.

---

## 7. Rôle des exports générés

Les fichiers dans :

```text
exports/generated/
```

sont des produits techniques.

Ils peuvent servir à contrôler, filtrer, visualiser ou alimenter le RAG, mais ils ne doivent pas être corrigés manuellement.

Toute correction doit se faire dans les sources Markdown/YAML ou dans les registres consolidés.

---

## 8. Suppression des anciens fichiers de sources ChatGPT

Les anciens fichiers historiques ne doivent être supprimés de l’espace source qu’après migration ou arbitrage.

Séquence correcte :

1. importer ou consulter les anciens fichiers comme matériaux de travail ;
2. créer les registres consolidés dans le repo ;
3. produire un rapport de divergence ;
4. arbitrer les doublons et les identifiants ;
5. vérifier que les interfaces lisent les registres consolidés ;
6. seulement ensuite supprimer les anciens fichiers de l’espace source, s’ils ne servent plus.

---

## 9. Rapport de divergence attendu

Avant toute suppression, produire un rapport de divergence :

```text
exports/generated/reference_divergences.json
exports/generated/quote_divergences.json
```

ou un rapport Markdown :

```text
reports/register_consolidation_report.md
```

Le rapport doit lister :

```text
sources présentes seulement dans les anciens fichiers ;
sources présentes seulement dans l’atomisation ;
sources présentes dans les deux mais avec identifiants différents ;
sources présentes dans les deux mais avec références bibliographiques divergentes ;
citations candidates non validées ;
citations vérifiées non encore reliées à des atomes ;
doublons probables ;
décisions d’arbitrage à prendre.
```

---

## 10. Règle pour l’IA

Lorsqu’un utilisateur demande de « fusionner les registres », l’IA doit comprendre :

```text
Créer une couche consolidée issue de la comparaison de tous les matériaux disponibles.
```

Elle ne doit pas supposer que les anciens fichiers sont canoniques.

Elle ne doit pas supposer que les fichiers issus de l’atomisation sont canoniques.

Elle doit produire ou mettre à jour des registres consolidés, avec traçabilité des origines et décisions d’arbitrage.
