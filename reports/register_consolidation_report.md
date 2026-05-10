# Rapport de consolidation — références et citations

Date de création : 2026-05-10

Objet : tracer les écarts entre les matériaux de travail historiques, le registre JSON, les atomisations par source et les futurs registres consolidés.

Ce rapport ne tranche pas tous les arbitrages. Il fixe les divergences à instruire.

---

## 1. Principe retenu

Aucun fichier n’est canonique par nature.

Les matériaux suivants sont traités comme documents de travail :

```text
anciens registres de références
anciens registres de citations
data/registre.json
sources/*/source.md
sources/*/citations_exactes.md
exports/generated/*
```

La consolidation se fait par fusion critique dans :

```text
registers/references/master_references.md
registers/quotes/master_quotes.md
```

---

## 2. Références actuellement connues dans `data/registre.json`

```yaml
references_from_data_registre:
  - S01
  - S02
  - S03
  - S04
  - S05
  - S06
  - S41
  - S45
  - S46
  - S47
  - S68
  - S69
  - S70
  - S71
  - S72
```

Constat : le registre JSON ne contient pas une séquence complète `S01-S72`. Il contient le noyau importé ou atomisé, mais pas toutes les références historiques.

---

## 3. Sources atomisées connues

```yaml
atomized_sources_known:
  - S41: Hook, Unknown Pleasures, 2012
  - S45: Curtis, Touching from a Distance, 1995
  - S68: Broll, Joy Division, s.d.
  - S69: Greig & Strong, But We Remember When We Were Young, 2014
  - S70: Suatoni, Joy Division, s.d.
  - S71: Flowers, Dreams Never End, 1995/2012
  - S72: Reynolds, Rip It Up and Start Again, 2005/2006
```

À vérifier : la présence effective et l’état des dossiers `sources/hook`, `sources/deborah_curtis`, `sources/marco_broll` dans une passe ultérieure.

---

## 4. Sources présentes dans le registre mais non atomisées ou non consolidées

```yaml
references_not_yet_atomized_or_incomplete:
  - S01
  - S02
  - S03
  - S04
  - S05
  - S06
  - S46
  - S47
```

Traitement recommandé :

```text
S01-S06 : consolider références complètes et usage chapitre 1 ; atomisation seulement si documents complets disponibles.
S46 : atomiser Mark Johnson si le fichier source est disponible.
S47 : atomiser Mike West si le fichier source est disponible.
```

---

## 5. Trou dans la numérotation S07-S40

```yaml
range: S07-S40
status: missing_from_data_registre
hypothesis: "Sources historiques probablement présentes dans les documents maîtres ou anciens registres, mais absentes du registre JSON actuel."
risk: "Réutilisation accidentelle d’un identifiant déjà utilisé dans les anciens travaux."
decision: "Ne pas attribuer de nouveaux numéros S07-S40 avant examen des anciens registres."
```

Action : importer ou consulter les anciens registres et compléter `registers/references/master_references.md`.

---

## 6. Identifiants divergents connus

```yaml
known_identifier_conflicts:
  - canonical_id: S72
    legacy_id: S20
    source: Simon Reynolds, Rip It Up and Start Again
    decision: "S72 conservé comme identifiant repo ; S20 conservé en legacy_id."
  - canonical_id: S68
    legacy_id: S-BROLL-JOY-001
    source: Marco Broll, Joy Division
    decision: "S68 conservé comme identifiant repo ; identifiant long conservé en legacy_id."
```

Action : si les anciens fichiers contiennent d’autres doublons, les ajouter ici avant migration.

---

## 7. Citations consolidées à ce stade

Le registre `registers/quotes/master_quotes.md` contient une première sélection de citations candidates issues des atomisations suivantes :

```yaml
quotes_first_batch:
  - S69-Q001
  - S69-Q002
  - S70-Q005
  - S70-Q008
  - S71-Q003
  - S71-Q006
  - S71-Q012
  - S72-Q002
  - S72-Q007
  - S72-Q009
```

Constat : ce registre ne contient pas encore toutes les citations locales des fichiers `sources/*/citations_exactes.md`. Il fixe la méthode et commence l’arbitrage.

---

## 8. Citations atomisées restant à importer

```yaml
quotes_to_import_from_atomization:
  - sources/hook/citations_exactes.md
  - sources/deborah_curtis/citations_exactes.md
  - sources/marco_broll/citations_exactes.md
  - sources/greig_strong/citations_exactes.md
  - sources/suatoni/citations_exactes.md
  - sources/flowers/citations_exactes.md
  - sources/reynolds_rip_it_up/citations_exactes.md
```

Priorité recommandée :

```text
1. Hook et Deborah Curtis : sources primaires.
2. Reynolds : cadre critique déjà utilisé dans les chapitres.
3. Greig & Strong : chapitre 14.
4. Flowers : transition Joy Division / New Order.
5. Suatoni et Broll : sources à consolider, OCR ou référence incomplète.
```

---

## 9. Citations historiques restant à importer

```yaml
historical_quotes_to_import:
  - 00_Citations.xlsx
  - fichier de citations vérifiées éventuel
  - citations contenues dans les documents maîtres de chapitres
```

Règle : importer sans présumer le statut. Chaque citation doit recevoir :

```yaml
statut_consolidation: candidate | verified | rejected
source_origin:
  - registre historique
arbitrage: "..."
```

---

## 10. Décisions à prendre avant suppression des anciens fichiers de sources ChatGPT

```yaml
before_deleting_historical_files:
  - importer S07-S40 ou documenter leur abandon
  - consolider les références complètes S01-S06
  - arbitrer S20/S72 définitivement ou maintenir legacy_id
  - importer les citations historiques
  - importer les citations atomisées restantes
  - vérifier les citations candidates marquées a_reverifier
  - confirmer que quote-register lit master_quotes.md ou un export dérivé
  - confirmer que prompt-studio et rag-studio utilisent les libellés consolidés
```

---

## 11. Conclusion opérationnelle

Le repo dispose désormais d’une couche de consolidation, mais elle est initiale.

Les anciens fichiers peuvent être retirés de l’espace source seulement après :

1. migration de leurs références utiles ;
2. migration de leurs citations utiles ;
3. mention explicite des éléments écartés ;
4. génération d’exports propres ;
5. vérification des interfaces.
