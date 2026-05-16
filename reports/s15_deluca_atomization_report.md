# Rapport d’atomisation — S15 — De Luca, *The Sound and the Fury*, 2021

```yaml
id: REPORT-S15-DELUCA-ATOMIZATION
source_id: S15
source_label: "S15 — De Luca, The Sound and the Fury, 2021"
statut: integration_directe
passage_atomise: "Article complet, p. PDF 54-63"
date: "2026-05-16"
```

## Passage atomisé

Article complet de Daniele De Luca, « The Sound and the Fury. Manchester, i Joy Division e la crisi sociopolitica dell’Inghilterra degli anni Settanta », dans Alfonso Amendola et Linda Barone (dir.), *Our Vision Touched the Sky: Fenomenologia dei Joy Division*, Roma, Rogas Edizioni, 2021, p. PDF 54-63.

## Fichiers créés ou modifiés

```text
sources/deluca_manchester_punk_threshold/source.md
sources/deluca_manchester_punk_threshold/README.md
sources/deluca_manchester_punk_threshold/atomes_s15_sound_fury.md
sources/deluca_manchester_punk_threshold/citations_exactes.md
sources/deluca_manchester_punk_threshold/relations_stabilisees.md
sources/deluca_manchester_punk_threshold/registres_structurants_s15.md
sources/deluca_manchester_punk_threshold/registres_specialises_s15.md
sources/deluca_manchester_punk_threshold/registre_patch_s15.json
registers/references/s15_deluca_source_canonique.md
master_docs/s15_deluca_sound_fury_master.md
chapters/01/s15_deluca_complement.md
chapters/02/s15_deluca_complement.md
chapters/03/s15_deluca_complement.md
rag/fragments/s15_deluca_sound_fury.jsonl
reports/s15_deluca_atomization_report.md
```

## Synthèse de la passe

- 15 atomes v2 créés : S15-A001 à S15-A015.
- 10 relations stabilisées créées : REL-S15-001 à REL-S15-010.
- 8 événements chronologiques créés : CHR-S15-001 à CHR-S15-008.
- Registres structurants complétés : concepts, motifs, mythes, références.
- Registres spécialisés complétés : citations candidates, chronologie, acteurs, lieux, organisations, chansons/disques.
- RAG enrichi par 15 fragments JSONL.
- Documents maîtres enrichis par un document maître source et trois compléments de chapitres.

## Commandes terminal

```bash
cd ~/Documents/joy-division-ai-writing-studio

git pull

python3 tools/apply_s15_registre_patch.py
python3 tools/build_registers.py --strict
python3 tools/build_master_docs.py
python3 tools/audit_repo.py
```

## Contrôles grep

```bash
cd ~/Documents/joy-division-ai-writing-studio

grep -R "S15 — De Luca, The Sound and the Fury, 2021" -n data/registre.json sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "S15-A001" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "S15-A015" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "REL-S15-001" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "REL-S15-010" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "CHR-S15-005" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "Lesser Free Trade Hall" -n data/registre.json sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "Politics of Boredom" -n data/registre.json sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "Spiral Scratch" -n data/registre.json sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "Salford" -n sources/deluca_manchester_punk_threshold/ master_docs/s15_deluca_sound_fury_master.md chapters/02/s15_deluca_complement.md rag/fragments/s15_deluca_sound_fury.jsonl
grep -R "Macclesfield" -n sources/deluca_manchester_punk_threshold/ master_docs/s15_deluca_sound_fury_master.md chapters/02/s15_deluca_complement.md rag/fragments/s15_deluca_sound_fury.jsonl
grep -R "Ian Curtis passeur" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
grep -R "unité Joy Division" -n sources/ registers/ master_docs/ chapters/ rag/ exports/generated/
```

## Commit local après génération

```bash
cd ~/Documents/joy-division-ai-writing-studio

git status --short

git add data/registre.json exports/generated/ chapters/ master_docs/ rag/ sources/ registers/ reports/

git commit -m "Build S15 De Luca generated registers and master docs"

git push
```

## Points de prudence

- S15 est une source critique, non une source primaire factuelle.
- Les dates, présences aux concerts et citations de témoins doivent être croisées.
- Le Lesser Free Trade Hall est traité comme seuil historiographique, non comme origine absolue.
- La lecture de Joy Division doit conserver la tension entre centralité de Curtis et unité collective du groupe.
