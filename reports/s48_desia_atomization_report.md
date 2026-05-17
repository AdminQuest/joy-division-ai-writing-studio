# Rapport d’atomisation — S48 — De Sia, *Il segno, la grafica, la visione*, 2021

## Passage traité

Chapitre complet d’Alfredo De Sia, « Il segno, la grafica, la visione », dans Alfonso Amendola et Linda Barone (dir.), *Our Vision Touched the Sky: Fenomenologia dei Joy Division*, Roma, Rogas Edizioni, 2021, p. PDF 94-98 de l’exemplaire de travail.

## Fichiers écrits dans le repo

```text
sources/desia_segno_grafica_visione/source.md
sources/desia_segno_grafica_visione/registre_patch_s48.json
sources/desia_segno_grafica_visione/atomes_s48_segno_grafica_visione.md
sources/desia_segno_grafica_visione/relations_stabilisees.md
sources/desia_segno_grafica_visione/registres_specialises_s48.md
registers/references/s48_desia_segno_grafica_visione_source_canonique.md
tools/apply_s48_registre_patch.py
master_docs/s48_desia_segno_grafica_visione_master.md
chapters/05/s48_desia_complement.md
chapters/07/s48_desia_complement.md
chapters/10/s48_desia_complement.md
chapters/14/s48_desia_complement.md
rag/fragments/s48_desia_segno_grafica_visione.jsonl
reports/s48_desia_atomization_report.md
```

## Synthèse de la passe

La passe crée treize atomes v2 et dix relations stabilisées. Elle ajoute des entrées de travail pour les registres concepts, motifs, mythes, références à vérifier, citations à contrôler, chronologie à croiser, acteurs, lieux, organisations, albums, chansons et objets visuels.

S48 est intégrée comme source secondaire critique. Elle ne doit pas être utilisée comme source primaire sur les crédits de design, les droits iconographiques, les matrices, les éditions ou les dates de sortie.

## Commandes recommandées

```bash
cd ~/Documents/joy-division-ai-writing-studio

git pull

python3 tools/apply_s48_registre_patch.py

python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py

grep -R "S48 — De Sia" -n data sources registers chapters master_docs rag exports | head -50
grep -R "S48-A0" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Il segno, la grafica, la visione" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Alfredo De Sia" -n data sources registers chapters master_docs rag exports | head -50
grep -R "pulsar" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Staglieno" -n data sources registers chapters master_docs rag exports | head -50
grep -R "An Ideal for Living" -n sources/desia_segno_grafica_visione registers chapters master_docs rag | head -50
grep -R "Love Will Tear Us Apart" -n sources/desia_segno_grafica_visione registers chapters master_docs rag | head -50

git status

git add data/registre.json \
  sources/desia_segno_grafica_visione/ \
  registers/references/s48_desia_segno_grafica_visione_source_canonique.md \
  tools/apply_s48_registre_patch.py \
  master_docs/s48_desia_segno_grafica_visione_master.md \
  chapters/05/s48_desia_complement.md \
  chapters/07/s48_desia_complement.md \
  chapters/10/s48_desia_complement.md \
  chapters/14/s48_desia_complement.md \
  rag/fragments/s48_desia_segno_grafica_visione.jsonl \
  reports/s48_desia_atomization_report.md \
  registers/ \
  chapters/

git add -f exports/generated/*.json exports/generated/*.csv

git commit -m "Atomize S48 De Sia graphic vision chapter"
git push
```

## Contrôle attendu

Les grep doivent faire ressortir :

- la source canonique S48 ;
- les atomes S48-A001 à S48-A013 ;
- les relations REL-S48-001 à REL-S48-010 ;
- les notions « triptyque graphique Joy Division », « pulsar comme brand identificatoire », « décontextualisation / recontextualisation graphique », « pochette comme épitaphe visuelle » ;
- les compléments des chapitres 5, 7, 10 et 14 ;
- les fragments RAG S48.
