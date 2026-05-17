# Rapport d’atomisation — S43 — Capozzi, *The weight on their shoulders*, 2021

## Passage traité

Chapitre complet d’Eugenio Capozzi, « The weight on their shoulders. Ian Curtis e la metamorfosi dei baby boomers », dans Alfonso Amendola et Linda Barone (dir.), *Our Vision Touched the Sky: Fenomenologia dei Joy Division*, Roma, Rogas Edizioni, 2021, p. PDF 64-75 de l’exemplaire de travail.

## Fichiers écrits dans le repo

```text
sources/capozzi_weight_on_their_shoulders/atomes_s43_weight_shoulders.md
sources/capozzi_weight_on_their_shoulders/relations_stabilisees.md
sources/capozzi_weight_on_their_shoulders/registres_specialises_s43.md
registers/references/s43_capozzi_weight_on_their_shoulders_source_canonique.md
master_docs/s43_capozzi_weight_shoulders_master.md
chapters/04/s43_capozzi_complement.md
chapters/11/s43_capozzi_complement.md
chapters/12/s43_capozzi_complement.md
chapters/14/s43_capozzi_complement.md
rag/fragments/s43_capozzi_weight_shoulders.jsonl
reports/s43_capozzi_atomization_report.md
```

## Synthèse de la passe

La passe crée quinze atomes v2 et neuf relations stabilisées. Elle ajoute des entrées de travail pour les registres concepts, motifs, mythes, citations à contrôler, chronologie à croiser, acteurs, lieux, organisations, chansons et albums.

La source est intégrée comme source secondaire critique. Elle ne doit pas être utilisée comme preuve primaire sur les faits biographiques, les paroles ou la santé de Curtis.

## Commandes recommandées

```bash
cd ~/Documents/joy-division-ai-writing-studio

git pull

python3 tools/apply_s43_registre_patch.py

python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py

grep -R "S43 — Capozzi" -n data sources registers chapters master_docs rag exports | head -50
grep -R "S43-A0" -n data sources registers chapters master_docs rag exports | head -50
grep -R "The weight on their shoulders" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Eugenio Capozzi" -n data sources registers chapters master_docs rag exports | head -50
grep -R "seconde génération des baby-boomers" -n data sources registers chapters master_docs rag exports | head -50
grep -R "sympathie comme thérapie impossible" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Decades" -n sources/capozzi_weight_on_their_shoulders registers chapters master_docs rag | head -50

git status

git add data/registre.json \
  sources/capozzi_weight_on_their_shoulders/ \
  registers/references/s43_capozzi_weight_on_their_shoulders_source_canonique.md \
  master_docs/s43_capozzi_weight_shoulders_master.md \
  chapters/04/s43_capozzi_complement.md \
  chapters/11/s43_capozzi_complement.md \
  chapters/12/s43_capozzi_complement.md \
  chapters/14/s43_capozzi_complement.md \
  rag/fragments/s43_capozzi_weight_shoulders.jsonl \
  reports/s43_capozzi_atomization_report.md \
  registers/ \
  chapters/

git add -f exports/generated/*.json exports/generated/*.csv

git commit -m "Atomize S43 Capozzi weight on their shoulders"
git push
```

## Contrôle attendu

Les grep doivent faire ressortir :

- la source canonique S43 ;
- les atomes S43-A001 à S43-A015 ;
- les relations REL-S43-001 à REL-S43-009 ;
- les notions « seconde génération des baby-boomers », « révolte sans utopie », « sympathie comme thérapie impossible », « communion perdue », « dernière parole au nous » ;
- les compléments des chapitres 4, 11, 12 et 14 ;
- les fragments RAG S43.
