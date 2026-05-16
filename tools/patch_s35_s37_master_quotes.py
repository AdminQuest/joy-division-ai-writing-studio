#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "registers" / "quotes" / "master_quotes.md"

if not PATH.exists():
    raise SystemExit("registers/quotes/master_quotes.md introuvable")

text = PATH.read_text(encoding="utf-8")
new = text.replace(
    "Les identifiants historiques S20, S35 et S37 sont à lire comme legacy_id pointant\n  respectivement vers S72, S41 et S45.",
    "Les identifiants historiques migrés ne doivent pas être réexportés comme sources actives.\n  Utiliser directement S72 pour Reynolds, S41 pour Hook et S45 pour Curtis."
)
new = new.replace("S72 legacy S20", "S72")

if new != text:
    PATH.write_text(new, encoding="utf-8")
    print("master_quotes.md patched")
else:
    print("no S35/S37 legacy mention found in master_quotes.md")
