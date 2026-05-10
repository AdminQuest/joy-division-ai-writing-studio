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
  - S73
```

Constat : le registre JSON contient désormais `S41` comme entrée historique Blue Orchids à consolider et `S73` comme entrée canonique repo pour Peter Hook.

---

## 3. Sources atomisées connues

```yaml
atomized_sources_known:
  - S45: Curtis, Touching from a Distance, 1995
  - S68: Broll, Joy Division, s.d.
  - S69: Greig & Strong, But We Remember When We Were Young, 2014
  - S70: Suatoni, Joy Division, s.d.
  - S71: Flowers, Dreams Never End, 1995/2012
  - S72: Reynolds, Rip It Up and Start Again, 2005/2006
  - S73: Hook, Unknown Pleasures, 2012
```

À vérifier : les fichiers `sources/hook/*` contiennent encore des identifiants internes `S41-*` et `S41-Q*`. Ils doivent être migrés vers `S73-*` et `S73-Q*` par opération dédiée.

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
  - S07-S34
  - S36
  - S38-S41
  - S46
  - S47
```

Traitement recommandé :

```text
S01-S06 : consolider références complètes et usage chapitre 1 ; atomisation seulement si documents complets disponibles.
S07-S41 : compléter depuis les registres historiques et sources disponibles.
S46 : atomiser Mark Johnson si le fichier source est disponible.
S47 : atomiser Mike West si le fichier source est disponible.
```

---

## 5. Import historique S07-S41

```yaml
range: S07-S41
status: imported_in_master_references
risk: "Références incomplètes, souvent conceptuelles ou génériques, nécessitant consolidation bibliographique."
decision: "Les identifiants S07-S41 ne doivent plus être réattribués. S41 est réservé à Blue Orchids ; Peter Hook est déplacé vers S73."
```

---

## 6. Identifiants divergents connus

```yaml
known_identifier_conflicts:
  - canonical_id: S72
    legacy_id: S20
    source: Simon Reynolds, Rip It Up and Start Again
    decision: "S72 conservé comme identifiant repo ; S20 conservé en legacy_id."
  - canonical_id: S73
    legacy_id:
      - S41-REPO
      - S35
    source: Peter Hook, Unknown Pleasures
    decision: "S73 devient l’identifiant canonique repo pour Hook ; S41 est libéré pour Blue Orchids."
  - canonical_id: S45
    legacy_id: S37
    source: Deborah Curtis, Touching from a Distance
    decision: "S45 conservé comme identifiant repo ; S37 conservé comme legacy historique."
  - canonical_id: S68
    legacy_id: S-BROLL-JOY-001
    source: Marco Broll, Joy Division
    decision: "S68 conservé comme identifiant repo ; identifiant long conservé en legacy_id."
```

Action : migrer les fichiers locaux de Hook de `S41` vers `S73` pour éviter les collisions dans les exports.

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
1. Migrer Hook de S41-Q vers S73-Q, puis importer.
2. Deborah Curtis : source primaire.
3. Reynolds : cadre critique déjà utilisé dans les chapitres.
4. Greig & Strong : chapitre 14.
5. Flowers : transition Joy Division / New Order.
6. Suatoni et Broll : sources à consolider, OCR ou référence incomplète.
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
  - compléter les références importées S07-S41
  - consolider les références complètes S01-S06
  - migrer les fichiers Hook de S41 vers S73
  - importer les citations historiques
  - importer les citations atomisées restantes
  - vérifier les citations candidates marquées a_reverifier
  - confirmer que quote-register lit master_quotes.md ou un export dérivé
  - confirmer que prompt-studio et rag-studio utilisent les libellés consolidés
```

---

## 11. Conclusion opérationnelle

Le repo dispose désormais d’une couche de consolidation plus cohérente.

La collision `S41` est corrigée au niveau des registres :

```text
S41 = Blue Orchids, entrée historique à consolider
S73 = Peter Hook, Unknown Pleasures, 2012
```

Il reste une opération technique à effectuer : migrer les identifiants internes des fichiers `sources/hook/*` de `S41` vers `S73`.
