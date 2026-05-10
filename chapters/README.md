# Documents maîtres des chapitres

Ce dossier contient les documents maîtres générés pour chacun des chapitres du livre.

Arborescence :

```text
chapters/
  01/document_maitre.md
  02/document_maitre.md
  ...
  14/document_maitre.md
```

Les documents sont générés automatiquement depuis :

```text
exports/generated/
```

Script de génération :

```bash
python tools/build_master_docs.py
```

Les documents maîtres servent de couche de consolidation rédactionnelle entre :

```text
atomisation documentaire
→ registres transversaux
→ RAG
→ rédaction du manuscrit
```
