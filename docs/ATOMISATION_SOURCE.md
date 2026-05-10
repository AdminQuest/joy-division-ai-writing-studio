# Procédure obligatoire — Atomiser une source ou un livre

Cette procédure s’impose à toute IA ou tout opérateur qui atomise une nouvelle source dans le repo `joy-division-ai-writing-studio`.

Elle vaut pour un livre complet, un article, un chapitre, un entretien, une notice critique, un document audiovisuel transcrit ou toute autre source intellectuelle.

---

## 1. Principe impératif

L’atomisation doit être faite **directement dans le repo GitHub**.

Il est interdit de répondre au demandeur par une archive locale, un dossier local, un fichier temporaire ou une proposition à copier-coller.

Le travail est considéré comme réalisé uniquement lorsque les fichiers utiles ont été créés ou modifiés dans le repo, sur la branche cible, avec des commits GitHub effectifs.

Formulation attendue en fin de tâche :

```text
Atomisation effectuée directement dans le repo.
Fichiers créés ou modifiés : ...
Commits : ...
```

Formulations interdites :

```text
J’ai préparé une archive.
Vous pouvez télécharger le dossier.
Je vous fournis le contenu à déposer dans le repo.
```

---

## 2. Règle sur les PDF et OCR

Les PDF, scans, OCR complets et fichiers sources volumineux ne doivent pas être versionnés dans Git.

Le repo ne stocke que les produits documentaires contrôlés : Markdown, YAML, JSON éditorial et scripts.

Le PDF ou l’OCR peut servir à produire les atomes, mais ne doit pas être ajouté dans `sources/`, `data/` ou `exports/`.

---

## 3. Identifiant canonique de source

Toute source reçoit un identifiant canonique au format :

```text
SXX
```

et un libellé lisible au format :

```text
SXX — Auteur, Titre court, Année
```

Exemples :

```text
S41 — Hook, Unknown Pleasures, 2012
S45 — Curtis, Touching from a Distance, 1995
S68 — Broll, Joy Division, s.d.
S69 — Greig & Strong, But We Remember When We Were Young, 2014
```

Règles :

1. Vérifier d’abord `data/registre.json`.
2. Si la source existe déjà, conserver son identifiant.
3. Si la source n’existe pas, attribuer le prochain `SXX` libre.
4. Ne jamais créer d’identifiant long du type `S-AUTEUR-TITRE-001`.
5. Les anciens identifiants techniques ne peuvent être conservés que comme `legacy_id`.
6. Tous les atomes, citations et événements doivent utiliser le `source_id` canonique.

---

## 4. Dossier source obligatoire

Chaque source atomisée doit disposer d’un dossier propre :

```text
sources/<auteur_court>/
```

Exemples :

```text
sources/hook/
sources/deborah_curtis/
sources/marco_broll/
sources/greig_strong/
```

Pour une source nouvelle, créer au minimum :

```text
sources/<auteur_court>/source.md
sources/<auteur_court>/citations_exactes.md
sources/<auteur_court>/README.md
```

Pour un livre volumineux, il est possible de découper en fichiers complémentaires :

```text
sources/<auteur_court>/source.md
sources/<auteur_court>/atomes_ch01_ch03.md
sources/<auteur_court>/atomes_ch04_ch06.md
sources/<auteur_court>/citations_exactes.md
sources/<auteur_court>/README.md
```

Le découpage est autorisé seulement s’il respecte les mêmes identifiants et les mêmes champs YAML.

---

## 5. Fichier `source.md`

Le fichier `source.md` doit commencer par une fiche source YAML.

Modèle :

```yaml
id: SXX
source_id: SXX
source_label: "SXX — Auteur, Titre court, Année"
source_short_title: "Auteur, Titre court, Année"
source_year: "Année"
auteur: Auteur complet
titre: Titre complet
type_unite: source
concepts:
  - concept principal
  - concept secondaire
chapitres:
  - Chapitre N
statut: verifie | a_verifier | a_consolider
fiabilite: forte | moyenne | faible
citation_directe: false
```

Ajouter ensuite :

1. référence complète ;
2. fonction documentaire ;
3. règle d’usage ;
4. atomes documentaires ;
5. événements chronologiques si nécessaire.

---

## 6. Identifiants des atomes

Les atomes d’une source sont numérotés :

```text
SXX-A001
SXX-A002
SXX-A003
```

Chaque atome doit contenir un bloc YAML complet.

Modèle :

```yaml
id: SXX-A001
source_id: SXX
source_label: "SXX — Auteur, Titre court, Année"
source_short_title: "Auteur, Titre court, Année"
source_year: "Année"
auteur: Auteur complet
titre: Titre complet
pages_pdf: 12-14
type_unite: analyse | biographie | reception | concert | production | memoire | marketing | sociologie | archive | synthese
concepts:
  - concept 1
  - concept 2
chapitres:
  - Chapitre N
statut: verifie | a_verifier | a_consolider
fiabilite: forte | moyenne | faible
citation_directe: true | false
related_people:
  - Personne
related_songs:
  - Chanson
related_events:
  - CHR-SXX-001
methodological_warnings:
  - précaution utile
notes: >
  Note de travail courte.
```

Après le bloc YAML, ajouter un court paragraphe de contenu atomisé, rédigé en prose claire.

L’atome ne doit pas être un résumé vague. Il doit isoler une unité exploitable : fait, interprétation, contradiction, concept, événement, relation, usage critique.

---

## 7. Citations candidates

Les citations sont placées dans :

```text
sources/<auteur_court>/citations_exactes.md
```

Identifiants :

```text
SXX-Q001
SXX-Q002
```

Modèle :

```yaml
id: SXX-Q001
source_id: SXX
source_label: "SXX — Auteur, Titre court, Année"
source_short_title: "Auteur, Titre court, Année"
source_year: "Année"
citation_originale: "Texte original court"
langue_originale: fr | en | it | autre
statut_verification: verifie | a_reverifier | a_verifier
traduction_litterale_fr: "..."
traduction_editoriale_fr: "..."
enjeu_traduction: "..."
atomes_lies:
  - SXX-A001
usage_recommande: "..."
risques: "..."
page_pdf: 12
importance: faible | moyenne | forte
```

Règles :

1. Ne pas créer de citations longues inutiles.
2. Respecter les limites de citation et les droits d’auteur.
3. Pour les paroles de chansons, ne jamais dépasser les limites autorisées.
4. Distinguer citation originale, traduction littérale et traduction éditoriale.
5. Signaler les citations indirectement rapportées comme `a_reverifier`.

---

## 8. Chronologie

Les événements nouveaux sont placés dans `source.md` ou dans un fichier d’atomes de la source.

Identifiants :

```text
CHR-SXX-001
CHR-SXX-002
```

Modèle :

```yaml
id: CHR-SXX-001
date: YYYY-MM-DD | YYYY-MM | YYYY
precision_date: jour | mois | annee | approximative
event: Description courte de l’événement.
type: publication | concert | enregistrement | film | documentaire | marketing | biographie | management | archive | reception
location: Lieu si connu
people:
  - Personne
songs:
  - Chanson
sources:
  - SXX
certainty: strong | medium | weak
related_atoms:
  - SXX-A001
```

Ne créer un événement chronologique que si l’information a une valeur transversale réelle.

---

## 9. Personnes

Si la source apporte un portrait nouveau, une contradiction ou un rôle significatif concernant une personne, créer un bloc conforme au schéma `person` dans :

```text
registers/people/master_people.md
```

ou compléter une personne existante si elle existe déjà.

Règles :

1. Ne pas créer de doublon pour une personne déjà présente.
2. Ajouter `SXX` dans `sources`.
3. Ajouter les atomes `SXX-A...` dans `related_atoms`.
4. Ajouter les citations `SXX-Q...` dans `related_quotes` si nécessaire.
5. Ajouter ou compléter `portraits_by_source`.
6. Ajouter les contradictions mémorielles si la source en apporte.

Si la personne est seulement mentionnée sans apport interprétatif, utiliser `related_people` dans les atomes, sans modifier le registre maître des personnes.

---

## 10. Chansons

Si la source apporte une information utile sur une chanson, compléter :

```text
registers/songs/master_songs.md
```

Règles :

1. Ne pas créer de doublon pour une chanson déjà présente.
2. Ajouter `SXX` dans `sources`.
3. Ajouter les atomes `SXX-A...` dans `related_atoms`.
4. Ajouter les citations `SXX-Q...` dans `related_quotes` si nécessaire.
5. Compléter `themes`, `contradictions`, `notes` ou `live_history` seulement si la source apporte réellement quelque chose.

Si la chanson est simplement citée, utiliser `related_songs` dans l’atome sans modifier le registre maître des chansons.

---

## 11. Concepts

Le registre des concepts est construit automatiquement depuis les champs `concepts` des atomes.

Pour alimenter correctement l’interface `concept-register`, chaque atome doit contenir des concepts normalisés, courts et réutilisables.

Exemples corrects :

```text
nostalgie ersatz
nostalgie comme mode
témoins d’autorité
authenticité
patrimonialisation
factory records
manchester
```

Éviter :

```text
idée générale très longue et unique
formule rhétorique non réutilisable
phrase complète de commentaire
```

---

## 12. Lieux

Si le registre des lieux existe, toute source apportant un lieu significatif doit l’alimenter.

En l’absence de registre maître des lieux, renseigner les lieux dans :

- `location` des événements chronologiques ;
- `concepts` si le lieu a une valeur analytique ;
- `notes` ou `related_events` si nécessaire.

Ne pas créer de registre des lieux ad hoc sans instruction spécifique.

---

## 13. Mise à jour du registre central des sources

Toute nouvelle source doit être ajoutée à :

```text
data/registre.json
```

Modèle :

```json
{
  "id": "SXX",
  "source_label": "SXX — Auteur, Titre court, Année",
  "auteur": "Auteur complet",
  "titre": "Titre court",
  "annee": "Année",
  "statut": "atomisée",
  "usage": "usages documentaires principaux"
}
```

Ce fichier alimente les interfaces :

```text
apps/prompt-studio/
apps/rag-studio/
apps/quote-register/
apps/chronology-register/
apps/people-register/
apps/song-register/
apps/concept-register/
```

Si `data/registre.json` n’est pas mis à jour, les interfaces ne pourront pas afficher correctement le titre de la source.

---

## 14. Registres et interfaces à satisfaire

Une atomisation complète doit alimenter tous les registres pertinents :

| Registre / interface | Alimentation attendue |
|---|---|
| `sources` | fiche source + `data/registre.json` |
| `atoms` | blocs `SXX-A...` |
| `quotes` | blocs `SXX-Q...` |
| `chronology` | blocs `CHR-SXX-...` |
| `people` | `related_people` et/ou `registers/people/master_people.md` |
| `songs` | `related_songs` et/ou `registers/songs/master_songs.md` |
| `concepts` | champ `concepts` de chaque atome |
| `RAG Studio` | `source_id`, `source_label`, atomes et registres |
| `Prompt Studio` | `data/registre.json` et exports régénérés |

Tous les registres ne reçoivent pas nécessairement un fichier modifié à chaque source. En revanche, chaque source doit contenir les champs permettant aux registres automatiques de la lire.

---

## 15. Validation après écriture

Après création ou modification des fichiers :

1. vérifier que les fichiers sont bien dans le repo ;
2. vérifier que `data/registre.json` contient la source ;
3. vérifier que les identifiants sont cohérents ;
4. vérifier que les champs `source_id` utilisent `SXX` ;
5. vérifier que les interfaces pourront afficher `source_label` ;
6. si possible, lancer ou recommander :

```bash
python tools/build_registers.py --strict
```

Les exports `exports/generated/` sont régénérables. Ils ne doivent pas être modifiés manuellement, sauf choix explicite du mainteneur.

---

## 16. Réponse finale attendue

La réponse finale doit indiquer :

1. l’identifiant retenu ;
2. les fichiers créés ou modifiés ;
3. les registres alimentés ;
4. les commits réalisés ;
5. les limites ou points à vérifier.

Modèle :

```text
Atomisation effectuée directement dans le repo.

Source : SXX — Auteur, Titre court, Année.

Fichiers créés ou modifiés :
- ...

Registres alimentés :
- sources
- atoms
- quotes
- chronology
- people via related_people
- songs via related_songs
- concepts via concepts

Commits :
- ...

Point à vérifier : ...
```

---

## 17. Règle de priorité pour l’IA

Si une demande utilisateur dit :

```text
Atomise cette source.
Atomise ce livre.
Ajoute cette source au repo.
```

l’IA doit comprendre :

```text
Créer ou modifier directement les fichiers nécessaires dans le repo GitHub, selon cette procédure.
```

Elle ne doit pas demander si l’utilisateur veut une archive locale, ni produire seulement du texte explicatif.
