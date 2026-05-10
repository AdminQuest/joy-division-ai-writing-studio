# Joy Division — AI Writing Studio

Environnement local de pilotage documentaire et rédactionnel pour la production du livre *Joy Division, le son de l’éternel*.

Le projet combine désormais deux fonctions distinctes :

- un **Prompt Studio**, destiné à construire des prompts contraints pour la rédaction, la relecture et le contrôle éditorial ;
- un **RAG Studio**, destiné à interroger localement le corpus atomisé : sources, citations, registres, chansons, personnes et événements.

Le système n’est pas conçu comme un générateur de texte autonome. Il vise à structurer le travail de recherche, sécuriser les sources et fournir à l’IA des matériaux contrôlés.

---

## 1. Architecture générale

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

  data/                          # données JSON du Prompt Studio
    chapitres.json
    ateliers.json
    niveaux.json
    registre.json

  sources/                       # sources atomisées en Markdown/YAML
    hook/
    deborah_curtis/

  registers/                     # registres transversaux
    chronology/
    songs/
    people/

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
    RAG_SETUP.md
    WEB_INTERFACE.md
```

---

## 2. Installation locale

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

## 3. Lancer le studio local

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

## 4. Pipeline documentaire

Le principe fondamental est le suivant :

```text
PDF OCR
→ atomisation Markdown/YAML
→ schémas documentaires
→ parseur documentaire
→ exports JSON/CSV
→ RAG lexical
→ interface web locale
→ usage rédactionnel contrôlé
```

L’IA générative ne doit pas être branchée directement sur les PDF OCR bruts. Les PDF servent à produire des atomes documentaires contrôlés, qui alimentent ensuite les registres et le RAG.

---

## 5. Sources atomisées

Les sources principales sont stockées dans `sources/` sous forme de fichiers Markdown contenant des blocs YAML.

Sources actuellement structurées :

```text
sources/hook/
sources/deborah_curtis/
```

Chaque source doit idéalement comporter :

- une fiche `source.md` ;
- des fichiers d’atomisation ;
- un fichier `citations_exactes.md` ;
- des identifiants stables ;
- des rattachements aux chapitres ;
- des liens vers personnes, chansons, événements ou concepts.

---

## 6. Registres transversaux

Trois registres maîtres existent actuellement :

```text
registers/chronology/master_chronology.md
registers/songs/master_songs.md
registers/people/master_people.md
```

Ils servent à croiser les sources et à éviter une simple accumulation de notes.

Leur fonction :

- stabiliser la chronologie ;
- relier chansons, événements et personnes ;
- identifier les contradictions entre sources ;
- préparer les exports et le RAG ;
- sécuriser la rédaction des chapitres.

---

## 7. Schémas documentaires

Les schémas dans `schemas/` définissent les formats attendus pour :

- les atomes ;
- les citations ;
- les événements chronologiques ;
- les chansons ;
- les personnes.

Ils empêchent la dérive progressive des fichiers Markdown : champs variables, statuts incohérents, citations sans original, atomes sans rattachement au livre.

---

## 8. Parseur documentaire

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

## 9. RAG local

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

## 10. Prompt Studio

Le Prompt Studio aide à construire des prompts contraints selon :

- le niveau IA ;
- le chapitre ;
- l’atelier ;
- le mode de sortie ;
- le matériau collé par l’utilisateur.

Il repose sur les fichiers JSON du dossier `data/`.

Il sert à produire des demandes de travail plus fiables pour :

- extraction documentaire ;
- recherche ;
- rédaction ;
- relecture ;
- contrôle ;
- anti-doublons ;
- mise à jour de registres.

---

## 11. Registre des sources Excel → JSON

Le registre Excel peut être converti en JSON avec :

```bash
python tools/convert_registre_xlsx.py mon_registre.xlsx
```

Le fichier produit est :

```text
data/registre.json
```

Ce fichier est ensuite utilisé par le Prompt Studio.

---

## 12. Règles méthodologiques permanentes

1. Ne pas stocker les PDF, OCR complets ou scans dans Git.
2. Conserver les citations originales en langue source.
3. Distinguer citation originale, traduction littérale, traduction éditoriale et interprétation.
4. Ne pas utiliser les atomes comme texte final du livre.
5. Ne pas interroger directement des PDF OCR bruts avec l’IA générative.
6. Toute nouvelle source doit être atomisée avant d’alimenter le RAG.
7. Tout nouveau fichier structuré doit respecter les schémas de `schemas/`.
8. Les exports de `exports/generated/` sont régénérables et ne doivent pas être versionnés.

---

## 13. État actuel

```text
sources atomisées : Hook, Deborah Curtis
citations exactes : Hook, Deborah Curtis
registres : chronologie, chansons, personnes
schémas : présents
parseur : présent
RAG lexical : présent
interface web : portail + Prompt Studio + RAG Studio
RAG vectoriel : non encore implémenté
synthèse IA automatique : non encore implémentée
```

---

## 14. Prochaines évolutions probables

- brancher effectivement `schema_validation.py` dans `build_registers.py` ;
- supprimer les anciens reliquats d’interface après vérification ;
- créer un registre des lieux ;
- créer un registre des contradictions ;
- ajouter une recherche vectorielle ;
- construire un mode de synthèse documentaire sourcée ;
- intégrer un export Word pour les dossiers de rédaction.
