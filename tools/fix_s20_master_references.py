#!/usr/bin/env python3
"""
Corrige l'entrée S20 dans registers/references/master_references.md.

Problème traité : le registre maître contenait encore une entrée YAML active
`id: S20` pour Reynolds, même si elle indiquait une migration vers S72. Comme
`tools/build_registers.py` scanne tous les blocs YAML, cette entrée continuait
à polluer les exports RAG et le menu déroulant des sources.

Usage :
  python3 tools/fix_s20_master_references.py
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MASTER_REFS = REPO_ROOT / "registers" / "references" / "master_references.md"

OLD_HEADER = "## S20 — Reynolds, cadre historique post-punk, migré vers S72"
NEXT_HEADER = "## S21 — City Fun, corpus 1978-1983, s.d."

NEW_BLOCK = """## S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d.

```yaml
id: S20
source_label: "S20 — Dodge, Mapping Manchester’s housing problems, Manchester Geographies, s.d."
auteur: Martin Dodge
titre: Mapping the geographies of Manchester’s housing problems and the twentieth century solutions
annee: "s.d."
reference_complete: "DODGE, Martin, « Mapping the geographies of Manchester’s housing problems and the twentieth century solutions », Manchester Geographies, chapitre 3, p. 19-36, année et édition à confirmer."
nature: chapitre d’ouvrage / géographie historique urbaine
statut: a_consolider
fiabilite: forte pour le contenu ; référence bibliographique à compléter
usage: [Manchester industriel, logement ouvrier, taudis victoriens, Little Ireland, Angel Meadow, Victoria Park, cartographie sanitaire, Thomas Marr, ceinture de taudis, Chorltonville, Wythenshawe, Hulme, Hattersley, Beswick, Fort Beswick, streets-in-the-sky, logement social, urban renewal, deindustrialisation, city centre living]
chapitres: [Chapitre 1, Chapitre 9, Chapitre 14]
source_origin: [Google Drive, texte intégral, arbitrage utilisateur]
niveau_preuve: source secondaire universitaire
arbitrage: "S20 était occupé par Reynolds, Rip It Up and Start Again, considéré par l’utilisateur comme doublon de S72. L’ancien S20 est redirigé vers S72. S20 est réattribué à Martin Dodge, Manchester Geographies, chapitre 3."
prudence: "Ne pas écraser S04 Kidd. Ne pas réutiliser l’ancien S20 Reynolds : utiliser S72 pour Reynolds. Ne pas utiliser Dodge comme source interne sur Joy Division. Vérifier l’année et l’édition de Manchester Geographies avant citation finale."
```

"""


def main() -> None:
    text = MASTER_REFS.read_text(encoding="utf-8")
    start = text.find(OLD_HEADER)
    if start == -1:
        if "S20 — Dodge, Mapping Manchester’s housing problems" in text:
            print("master_references.md est déjà corrigé pour S20 Dodge")
            return
        raise SystemExit("Bloc S20 Reynolds introuvable et bloc S20 Dodge absent : arbitrage manuel requis")

    end = text.find(NEXT_HEADER, start)
    if end == -1:
        raise SystemExit("Bloc S21 introuvable : impossible de borner le remplacement S20")

    updated = text[:start] + NEW_BLOCK + text[end:]
    MASTER_REFS.write_text(updated, encoding="utf-8")
    print("Entrée S20 de master_references.md remplacée par Dodge")


if __name__ == "__main__":
    main()
