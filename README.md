# Joy Division — AI Writing Studio

Environnement local de pilotage documentaire et rédactionnel pour la production du livre *Joy Division, le son de l’éternel*.

Le projet combine deux fonctions distinctes :

- un **Prompt Studio**, destiné à construire des prompts contraints pour la rédaction, la relecture et le contrôle éditorial ;
- un **RAG Studio**, destiné à interroger localement le corpus atomisé : sources, citations, registres, chansons, personnes et événements.

Le système n’est pas conçu comme un générateur de texte autonome. Il vise à structurer le travail de recherche, sécuriser les sources et fournir à l’IA des matériaux contrôlés.

---

## 0. Règle impérative pour toute atomisation

Toute demande du type :

```text
Atomise cette source.
Atomise ce livre.
Ajoute cette source au repo.
```

signifie obligatoirement :

```text
Créer ou modifier directement les fichiers nécessaires dans le repo GitHub.
```

Il est interdit de répondre uniquement par une archive locale, un dossier local, un fichier temporaire ou un contenu à copier-coller. Le travail n’est considéré comme fait que lorsque les fichiers sont créés ou modifiés dans le repo avec des commits effectifs.

La procédure obligatoire est décrite ici :

```text
docs/ATOMISATION_SOURCE.md
```

Cette procédure prime sur toute pratique antérieure.

---

## 1. Convention unique de codification des sources

Toute source intellectuelle mobilisée dans le repo doit respecter le format suivant :

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

1. `SXX` est l’identifiant source canonique.
2. Si une source existe déjà dans le registre, son numéro est conservé.
3. Si une source nouvelle n’existe pas dans le registre, elle reçoit le prochain numéro libre.
4. Les anciens identifiants longs ou techniques sont traités comme alias de migration, jamais comme identifiants d’affichage.
5. Chaque atome, citation ou événement doit porter le champ `source_id` canonique.
6. Les interfaces doivent afficher le champ `source_label` lorsqu’il existe.
7. Toute nouvelle source doit être ajoutée à `data/registre.json`.

---

## 1 bis. Consolidation des registres

Les anciens registres de références ou de citations, les fichiers issus de l’atomisation et les exports générés sont tous des matériaux de travail.

Aucun n’est automatiquement canonique par nature.

La doctrine de consolidation est décrite ici :

```text
docs/CONSOLIDATION_REGISTRES.md
```

Principe : les références et les citations doivent être fusionnées par comparaison critique, avec traçabilité de leur origine, arbitrage des doublons, gestion des `legacy_id` et distinction entre citation candidate et citation validée.

---

## 2. Architecture générale

```text
joy-division-ai-writing-studio/

  index.html                     # portail général

  apps/
    prompt-studio/               # atelier de prompts rédactionnels
      index.html
      style.css
      app.js
      prompt-builder.js

    rag-studio/                  # interface RAG documentaire
      index.html
      style.css
      app.js

    quote-register/              # registre des citations
    chronology-register/         # registre chronologique
    people-register/             # registre des personnes
    song-register/               # registre des chansons
    concept-register/            # registre des concepts

  data/                          # données JSON du Prompt Studio et registre central
    chapitres.json
    ateliers.json
    niveaux.json
    registre.json

  sources/                       # sources atomisées en Markdown/YAML
    hook/
    deborah_curtis/
    marco_broll/
    greig_strong/

  registers/                     # registres transversaux
    chronology/
    songs/
    people/
    references/
    quotes/

  schemas/                       # schémas documentaires
    atom.schema.yaml
    quote.schema.yaml
    chronology.schema.yaml
    song.schema.yaml
    person.schema.yaml

  tools/
    convert_registre_xlsx.py     # conversion Excel → JSON
    build_registers.py           # parseur documentaire
    schema_validation.py         # règles de validation documentaire
    rag_search.py                # moteur RAG lexical local
    rag_server.py                # serveur web local

  exports/
    generated/                   # exports régénérables, ignorés par Git

  indexes/
    master_index.md              # index documentaire global

  docs/
    ATOMISATION_SOURCE.md        # procédure obligatoire d’atomisation
    CONSOLIDATION_REGISTRES.md   # doctrine de fusion références / citations
    RAG_SETUP.md
    WEB_INTERFACE.md
```

---

## 3. Installation locale

Créer un environnement Python, puis installer les dépendances :

```bash
pip install -r requirements.txt
```

Dépendances minimales :

```text
openpyxl
PyYAML
```

---

## 4. Lancer le studio local

Depuis la racine du repo :

```bash
python tools/build_registers.py
python tools/rag_server.py
```

Puis ouvrir :

```text
http://127.0.0.1:8765
```

Routes principales :

```text
/                       portail général
/prompt                 Prompt Studio
/rag                    RAG Studio
/apps/prompt-studio/    accès direct au Prompt Studio
/apps/rag-studio/       accès direct au RAG Studio
/api/status             état du corpus RAG
/api/search             recherche RAG
```

---

## 5. Pipeline documentaire

Le principe fondamental est le suivant :

```text
PDF OCR
→ atomisation Markdown/YAML dans le repo
→ schémas documentaires
→ parseur documentaire
→ exports JSON/CSV
→ RAG lexical
→ interfaces web
→ usage rédactionnel contrôlé
```

L’IA générative ne doit pas être branchée directement sur les PDF OCR bruts. Les PDF servent à produire des atomes documentaires contrôlés, qui alimentent ensuite les registres et le RAG.

---

## 6. Sources atomisées

Les sources principales sont stockées dans `sources/` sous forme de fichiers Markdown contenant des blocs YAML.

Chaque source doit comporter au minimum :

- une fiche `source.md` ;
- un fichier `citations_exactes.md` ;
- un fichier `README.md` ;
- des identifiants stables ;
- des rattachements aux chapitres ;
- des liens vers personnes, chansons, événements ou concepts ;
- une entrée dans `data/registre.json`.

Pour les livres longs, des fichiers d’atomes complémentaires peuvent être créés, mais ils doivent rester dans le dossier source et respecter la procédure `docs/ATOMISATION_SOURCE.md`.

---

## 7. Registres transversaux

Les registres maîtres existants sont :

```text
registers/chronology/master_chronology.md
registers/songs/master_songs.md
registers/people/master_people.md
```

Les registres consolidés à créer ou alimenter sont :

```text
registers/references/master_references.md
registers/quotes/master_quotes.md
```

Ils servent à croiser les sources et à éviter une simple accumulation de notes.

Leur fonction :

- stabiliser la chronologie ;
- relier chansons, événements et personnes ;
- identifier les contradictions entre sources ;
- consolider les références issues de l’atomisation et des documents de travail ;
- distinguer citations candidates et citations validées ;
- préparer les exports et le RAG ;
- sécuriser la rédaction des chapitres.

Toute atomisation doit alimenter tous les registres pertinents, soit directement par modification d’un registre maître, soit indirectement par les champs YAML `related_people`, `related_songs`, `related_events`, `concepts`, `sources` et `chapitres`.

---

## 8. Schémas documentaires

Les schémas dans `schemas/` définissent les formats attendus pour :

- les atomes ;
- les citations ;
- les événements chronologiques ;
- les chansons ;
- les personnes.

Ils empêchent la dérive progressive des fichiers Markdown : champs variables, statuts incohérents, citations sans original, atomes sans rattachement au livre.

---

## 9. Parseur documentaire

Le parseur est lancé avec :

```bash
python tools/build_registers.py
```

Il scanne :

```text
sources/
registers/
```

Il extrait les blocs YAML et génère :

```text
exports/generated/atoms.json
exports/generated/quotes.json
exports/generated/chronology.json
exports/generated/songs.json
exports/generated/people.json
exports/generated/sources.json
exports/generated/all_records.json
exports/generated/index_by_id.json
exports/generated/diagnostics.json
```

Des exports CSV sont également produits.

Mode strict :

```bash
python tools/build_registers.py --strict
```

---

## 10. RAG local

Le moteur RAG lexical est disponible en ligne de commande :

```bash
python tools/rag_search.py "Ian Curtis epilepsy domestic life"
```

Exemples :

```bash
python tools/rag_search.py "Hannett live sound studio frustration"
python tools/rag_search.py "Transmission first real Joy Division song" --kind song
python tools/rag_search.py "Love Will Tear Us Apart" --json
```

Le RAG Studio web utilise les mêmes données via :

```text
/api/status
/api/search
```

---

## 11. Prompt Studio

Le Prompt Studio aide à construire des prompts contraints selon :

- le niveau IA ;
- le chapitre ;
- l’atelier ;
- le mode de sortie ;
- le matériau collé par l’utilisateur.

Il repose sur les fichiers JSON du dossier `data/`.

---

## 12. Registre des sources Excel → JSON

Le registre Excel peut être converti en JSON avec :

```bash
python tools/convert_registre_xlsx.py mon_registre.xlsx
```

Le fichier produit est :

```text
data/registre.json
```

Ce fichier est ensuite utilisé par toutes les interfaces pour afficher les titres complets des sources.

À terme, `data/registre.json` peut devenir un export dérivé du registre consolidé `registers/references/master_references.md`.

---

## 13. Règles méthodologiques permanentes

1. Atomiser directement dans le repo GitHub.
2. Ne jamais livrer uniquement une archive locale ou un dossier local.
3. Ne pas stocker les PDF, OCR complets ou scans dans Git.
4. Conserver les citations originales en langue source.
5. Distinguer citation originale, traduction littérale, traduction éditoriale et interprétation.
6. Ne pas utiliser les atomes comme texte final du livre.
7. Ne pas interroger directement des PDF OCR bruts avec l’IA générative.
8. Toute nouvelle source doit être atomisée avant d’alimenter le RAG.
9. Tout nouveau fichier structuré doit respecter les schémas de `schemas/`.
10. Les exports de `exports/generated/` sont régénérables et ne doivent pas être versionnés.
11. Toute nouvelle source doit recevoir un identifiant `SXX` unique et un `source_label` lisible.
12. Toute nouvelle source doit être ajoutée à `data/registre.json`.
13. Toute atomisation doit viser tous les registres pertinents : sources, atomes, citations, chronologie, personnes, chansons, concepts.
14. Les anciens registres et les fichiers issus de l’atomisation sont des matériaux de travail ; la consolidation résulte d’une comparaison critique documentée.

---

## 14. État actuel

```text
sources atomisées : Hook, Deborah Curtis, Marco Broll, Greig & Strong, Suatoni, Flowers, Reynolds
citations exactes/candidates : fichiers locaux par source
registres : chronologie, chansons, personnes, concepts via atomes
schémas : présents
parseur : présent, avec normalisation des sources
RAG lexical : présent
interface web : portail + Prompt Studio + RAG Studio + registres spécialisés
registre consolidé des références : à créer
registre consolidé des citations : à créer
RAG vectoriel : non encore implémenté
synthèse IA automatique : non encore implémentée
```

---

## 15. Prochaines évolutions probables

- créer `registers/references/master_references.md` ;
- créer `registers/quotes/master_quotes.md` ;
- produire un rapport de divergence références / citations ;
- créer un registre des lieux ;
- créer un registre des contradictions ;
- ajouter une recherche vectorielle ;
- construire un mode de synthèse documentaire sourcée ;
- intégrer un export Word pour les dossiers de rédaction.
