#!/usr/bin/env python3
"""Injecteur lot 3 — phase 1 : 11 PLACE- existantes. Usage unique, jetable.

Insère lat/lng/geo_precision/prudence_methodologique[/reference_croisee] juste
après la ligne `- id:` du lieu (placement uniforme avec les 36 entrées déjà
géocodées). Idempotent (skip si lat déjà présent dans le bloc). N'altère aucun
autre champ.
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# id -> (lat, lng, geo_precision, prudence, reference_croisee|None)
SEED = {
    "PLACE-ALFRED-STREET": (53.49900, -2.26000, "rue",
        "Alfred Street, Lower Broughton, Salford. Rue liée au secteur d'enfance "
        "de Bernard Sumner / Wheathill Chemical Works. Coordonnée de rue, pas de bâtiment.", None),
    "PLACE-GREENDOW-COMMERCIALS-STUDIO": (53.47938, -2.24773, "exacte",
        "Arrow Studios / Greendow, 6 Jackson's Row, Manchester. Sessions RCA.", None),
    "PLACE-LOWER-BROUGHTON": (53.49900, -2.26000, "quartier",
        "Quartier d'enfance de Bernard Sumner, Lower Broughton, Salford.", None),
    "PLACE-VIRGIN-RECORDS-LEVER-STREET": (53.48270, -2.23570, "rue",
        "Virgin Records, Lever Street, Manchester. Disquaire de la scène "
        "post-punk mancunienne. Adresse exacte à confirmer.", None),
    "PLACE-ANGEL-MEADOW": (53.49020, -2.23870, "quartier",
        "Quartier historique de Manchester, pas une salle de concert.",
        ["wikidata:Q4760268"]),
    "PLACE-WELLINGTON-STREET-ESTATE": (53.47430, -2.20070, "quartier",
        "Wellington Street Estate / Fort Beswick, Beswick, Manchester. "
        "Coordonnée de secteur, non du bloc exact.",
        ["wikidata:Q4897126"]),
    "PLACE-BROKEN-CROSS-SECONDARY-MODERN": (53.25760, -2.15500, "quartier",
        "Broken Cross, Macclesfield. Établissement à confirmer par archives scolaires locales.", None),
    "PLACE-CHRIST-CHURCH-PRIMARY-SCHOOL": (53.25880, -2.12210, "quartier",
        "Christ Church Primary School, Macclesfield. Lié à l'enfance de Ian "
        "Curtis. Adresse fine à confirmer par archives scolaires.", None),
    "PLACE-BOOTLE-STREET": (53.47815, -2.24756, "rue",
        "Bootle Street, Manchester. Rue, pas un bâtiment.", None),
    "PLACE-IVY-LANE": (53.25800, -2.12650, "rue",
        "Ivy Lane, Macclesfield. Rue, pas un bâtiment.", None),
    "PLACE-RARE-RECORDS": (53.48018, -2.24714, "exacte",
        "Rare Records, 36 John Dalton Street, Manchester. Ian Curtis y travailla.", None),
}

ID_RE = re.compile(r'^(\s*)- id:\s*("?)(PLACE-[A-Z0-9-]+)\2\s*$')
done = set()


def entry_has_lat(lines, i):
    """True si l'entrée commençant à la ligne i (`- id:`) déclare déjà lat.

    Scanne uniquement CETTE entrée : de i+1 jusqu'au prochain `- id:` de même
    indentation (ou fin de bloc ```), sans déborder sur les entrées voisines.
    """
    base = len(lines[i]) - len(lines[i].lstrip())
    for j in range(i + 1, len(lines)):
        l = lines[j]
        if l.strip() == "```":
            break
        indent = len(l) - len(l.lstrip())
        if l.lstrip().startswith("- id:") and indent <= base:
            break
        if re.match(r'\s*lat:', l):
            return True
    return False


def yaml_str(s):
    return '"' + s.replace('"', '\\"') + '"'


for path in sorted(glob.glob(str(ROOT / "registers" / "places" / "*.md"))):
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines()
    out, changed = [], False
    for i, line in enumerate(lines):
        out.append(line)
        m = ID_RE.match(line)
        if not m:
            continue
        pid = m.group(3)
        if pid not in SEED or pid in done:
            continue
        if entry_has_lat(lines, i):
            done.add(pid)   # déjà géocodé, rien à faire
            continue
        fi = (" " * (len(line) - len(line.lstrip()))) + "  "  # champs sous l'item
        lat, lng, prec, prud, refs = SEED[pid]
        ins = [f"{fi}lat: {lat}", f"{fi}lng: {lng}", f"{fi}geo_precision: {prec}",
               f"{fi}prudence_methodologique: {yaml_str(prud)}"]
        if refs:
            ins.append(f"{fi}reference_croisee: {refs}".replace("'", '"'))
        out.extend(ins)
        done.add(pid)
        changed = True
    if changed:
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"patched -> {p.relative_to(ROOT)}")

missing = sorted(set(SEED) - done)
print(f"\nseeded {len(done)}/{len(SEED)}")
if missing:
    print("NON TROUVÉS :", missing)
