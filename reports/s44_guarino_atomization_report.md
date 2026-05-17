# Rapport d’atomisation — S44 — Guarino, *I Joy Division tra vomito culturale e ideali sottoculturali*, 2021

## Passage traité

Chapitre complet de Donato Guarino, « I Joy Division tra vomito culturale e ideali sottoculturali », dans Alfonso Amendola et Linda Barone (dir.), *Our Vision Touched the Sky: Fenomenologia dei Joy Division*, Roma, Rogas Edizioni, 2021, p. PDF 76-92 de l’exemplaire de travail.

## Fichiers écrits dans le repo

```text
sources/guarino_vomito_culturale_ideali_sottoculturali/source.md
sources/guarino_vomito_culturale_ideali_sottoculturali/registre_patch_s44.json
sources/guarino_vomito_culturale_ideali_sottoculturali/atomes_s44_vomito_culturale.md
sources/guarino_vomito_culturale_ideali_sottoculturali/relations_stabilisees.md
sources/guarino_vomito_culturale_ideali_sottoculturali/registres_specialises_s44.md
registers/references/s44_guarino_vomito_culturale_source_canonique.md
tools/apply_s44_registre_patch.py
master_docs/s44_guarino_vomito_culturale_master.md
chapters/01/s44_guarino_complement.md
chapters/02/s44_guarino_complement.md
chapters/03/s44_guarino_complement.md
chapters/04/s44_guarino_complement.md
chapters/05/s44_guarino_complement.md
chapters/12/s44_guarino_complement.md
chapters/14/s44_guarino_complement.md
rag/fragments/s44_guarino_vomito_culturale.jsonl
reports/s44_guarino_atomization_report.md
```

## Synthèse de la passe

La passe crée seize atomes v2 et dix relations stabilisées. Elle ajoute des entrées de travail pour les registres concepts, motifs, mythes, références à vérifier, citations à contrôler, chronologie à croiser, acteurs, lieux, organisations, chansons et albums.

S44 est intégrée comme source secondaire critique. Elle ne doit pas être utilisée comme source primaire sur les concerts, dates, faits médicaux, discographie ou citations de paroles.

## Commandes recommandées

```bash
cd ~/Documents/joy-division-ai-writing-studio

git pull

python3 tools/apply_s44_registre_patch.py

python3 tools/build_registers.py --strict
python3 tools/audit_repo.py
python3 tools/build_master_docs.py

grep -R "S44 — Guarino" -n data sources registers chapters master_docs rag exports | head -50
grep -R "S44-A0" -n data sources registers chapters master_docs rag exports | head -50
grep -R "I Joy Division tra vomito culturale" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Donato Guarino" -n data sources registers chapters master_docs rag exports | head -50
grep -R "vomito culturale" -n data sources registers chapters master_docs rag exports | head -50
grep -R "non-savoir jouer" -n data sources registers chapters master_docs rag exports | head -50
grep -R "Lesser Free Trade Hall" -n sources/guarino_vomito_culturale_ideali_sottoculturali registers chapters master_docs rag | head -50
grep -R "Stiff Kittens" -n sources/guarino_vomito_culturale_ideali_sottoculturali registers chapters master_docs rag | head -50

git status

git add data/registre.json \
  sources/guarino_vomito_culturale_ideali_sottoculturali/ \
  registers/references/s44_guarino_vomito_culturale_source_canonique.md \
  tools/apply_s44_registre_patch.py \
  master_docs/s44_guarino_vomito_culturale_master.md \
  chapters/01/s44_guarino_complement.md \
  chapters/02/s44_guarino_complement.md \
  chapters/03/s44_guarino_complement.md \
  chapters/04/s44_guarino_complement.md \
  chapters/05/s44_guarino_complement.md \
  chapters/12/s44_guarino_complement.md \
  chapters/14/s44_guarino_complement.md \
  rag/fragments/s44_guarino_vomito_culturale.jsonl \
  reports/s44_guarino_atomization_report.md \
  registers/ \
  chapters/

git add -f exports/generated/*.json exports/generated/*.csv

git commit -m "Atomize S44 Guarino vomito culturale chapter"
git push
```

## Contrôle attendu

Les grep doivent faire ressortir :

- la source canonique S44 ;
- les atomes S44-A001 à S44-A016 ;
- les relations REL-S44-001 à REL-S44-010 ;
- les notions « sous-culture comme rempart contre le sens commun », « Cottonopolis », « non-savoir jouer comme moteur créatif », « intention avant maîtrise » ;
- les compléments des chapitres 1, 2, 3, 4, 5, 12 et 14 ;
- les fragments RAG S44.
