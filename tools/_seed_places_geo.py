#!/usr/bin/env python3
"""Injecteur de coordonnées (étape 12b-1.c) — usage unique, jetable.

Insère lat/lng/geo_precision[/reference_croisee/prudence_methodologique] juste
après la ligne `id:` du lieu CANONIQUE, en respectant l'indentation, une seule
fois par id (première occurrence). Ne reformate pas le YAML : insertion de
lignes uniquement. Idempotent (skip si lat déjà présent dans le bloc).

Curation hors-ligne recoupée Wikidata P625 (CC0). QID porté seulement là où la
confiance est élevée ; sinon backfill QID = suivi réseau-dépendant (host
query.wikidata.org hors allowlist dans cet environnement).
"""
import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# id -> (lat, lng, geo_precision, wikidata|None, prudence_methodologique|None)
SEED = {
    # — Repères majeurs, QID Wikidata recoupé (confiance élevée) —
    "PLACE-JODRELL-BANK": (53.2367, -2.3085, "exacte", "Q204686", None),
    "PLACE-FREE-TRADE-HALL": (53.4779, -2.2470, "exacte", "Q5500433",
        "Reconverti en hôtel (façade conservée, Peter Street)."),
    "PLACE-STRAWBERRY-STUDIOS": (53.4084, -2.1570, "exacte", "Q7622496",
        "Studio fermé en 1993 ; bâtiment conservé (Stockport)."),
    "PLACE-HACIENDA": (53.4746, -2.2503, "exacte", "Q1572261",
        "FAC 51 ; démolie en 2002, remplacée par des logements."),
    "PLACE-UNIVERSITY-OF-MANCHESTER": (53.4668, -2.2339, "exacte", "Q230899", None),
    "PLACE-MACCLESFIELD": (53.2581, -2.1255, "ville", "Q659804", None),
    "PLACE-MANCHESTER": (53.4808, -2.2426, "ville", "Q18125", None),
    "PLACE-BRITANNIA-ROW-STUDIOS": (51.5392, -0.0972, "exacte", "Q4970934", None),
    "PLACE-LONDON": (51.5074, -0.1278, "ville", "Q84", None),
    "PLACE-CHICAGO": (41.8781, -87.6298, "ville", "Q1297", None),
    "PLACE-DETROIT": (42.3314, -83.0458, "ville", "Q12439", None),

    # — Villes / quartiers (coord. solide, QID à recouper) —
    "PLACE-MANCHESTER-CITY": (53.4808, -2.2426, "ville", None, None),
    "PLACE-MANCHESTER-CENTRE": (53.4794, -2.2453, "quartier", None, None),
    "PLACE-GREATER-MANCHESTER": (53.5900, -2.3000, "approximative", None,
        "Comté métropolitain — centroïde approximatif, non un point."),
    "PLACE-BOLTON": (53.5780, -2.4290, "ville", None, None),
    "PLACE-OLDHAM": (53.5409, -2.1183, "ville", None, None),
    "PLACE-HYDE": (53.4510, -2.0810, "ville", None, None),
    "PLACE-BUXTON": (53.2590, -1.9110, "ville", None, None),
    "PLACE-HOLMES-CHAPEL": (53.1980, -2.3570, "ville", None, None),
    "PLACE-WYTHENSHAWE": (53.3920, -2.2640, "quartier", None, None),
    "PLACE-BOURNEMOUTH": (50.7200, -1.8800, "ville", None, None),
    "PLACE-ALTRINCHAM": (53.3870, -2.3490, "ville", None, None),
    "PLACE-SALE": (53.4240, -2.3220, "ville", None, None),
    "PLACE-HULME": (53.4640, -2.2470, "quartier", None, None),
    "PLACE-MOSS-SIDE": (53.4530, -2.2490, "quartier", None, None),
    "PLACE-ORDSALL": (53.4740, -2.2720, "quartier", None, None),
    "PLACE-BELLE-VUE": (53.4610, -2.1800, "quartier", None, None),
    "PLACE-VICTORIA-PARK-MANCHESTER": (53.4560, -2.2130, "quartier", None, None),
    "PLACE-HATTERSLEY": (53.4440, -2.0430, "quartier", None, None),

    # — Lieux JD avec caveat de provenance —
    "PLACE-HULME-CRESCENTS": (53.4610, -2.2520, "quartier", None,
        "Ensemble démoli (1991-1995) ; coordonnée du secteur, non d'un bâtiment."),
    "PLACE-TJ-DAVIDSONS": (53.4740, -2.2490, "rue", None,
        "Entrepôt de répétition, Little Peter Street ; bâtiment d'origine disparu."),
    "PLACE-CARGO-STUDIOS": (53.6170, -2.1560, "rue", None,
        "Kenion Street, Rochdale ; studio fermé."),
    "PLACE-LESSER-FREE-TRADE-HALL": (53.4779, -2.2470, "exacte", None,
        "Petite salle AU SEIN du Free Trade Hall — distincte du grand hall "
        "(PLACE-FREE-TRADE-HALL) ; même bâtiment, point partagé."),
    "PLACE-ELECTRIC-CIRCUS": (53.4930, -2.2210, "rue", None,
        "Collyhurst ; salle fermée en 1977, démolie."),
    "PLACE-KINGS-SCHOOL": (53.2520, -2.1370, "exacte", None,
        "King's School, Macclesfield."),
    "PLACE-SOUTHPORT-FLORAL-HALL": (53.6540, -3.0100, "exacte", None, None),
    "PLACE-SALFORD-GRAMMAR-SCHOOL": (53.4880, -2.2980, "approximative", None,
        "Localisation approximative (Salford)."),
}

ID_RE = re.compile(r'^(\s*)(?:- )?id:\s*("?)(PLACE-[A-Z0-9-]+)\2\s*$')

done = set()


def block_has_lat(lines, i):
    """True si le bloc YAML contenant la ligne i déclare déjà lat:."""
    # remonte/descend dans le même fence ```yaml ... ```
    start = i
    while start > 0 and not lines[start].strip().startswith("```yaml"):
        start -= 1
    end = i
    while end < len(lines) - 1 and not lines[end].strip() == "```":
        end += 1
    return any(re.match(r'\s*lat:', l) for l in lines[start:end + 1])


for path in sorted(glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True)):
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines()
    out = []
    changed = False
    for i, line in enumerate(lines):
        out.append(line)
        m = ID_RE.match(line)
        if not m:
            continue
        pid = m.group(3)
        if pid not in SEED or pid in done:
            continue
        if block_has_lat(lines, i):
            done.add(pid)
            continue
        indent = m.group(1).replace("- ", "  ")  # champs alignés sous l'id
        # si la ligne est "  - id:", l'indent des champs = indent + 2
        field_indent = (" " * (len(line) - len(line.lstrip())))
        if line.lstrip().startswith("- "):
            field_indent += "  "
        lat, lng, prec, qid, prud = SEED[pid]
        ins = [f"{field_indent}lat: {lat}",
               f"{field_indent}lng: {lng}",
               f"{field_indent}geo_precision: {prec}"]
        if qid:
            ins.append(f'{field_indent}reference_croisee: ["wikidata:{qid}"]')
        if prud:
            ins.append(f'{field_indent}prudence_methodologique: >-')
            ins.append(f'{field_indent}  {prud}')
        out.extend(ins)
        done.add(pid)
        changed = True
    if changed:
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"injected -> {p.relative_to(ROOT)}")

missing = sorted(set(SEED) - done)
print(f"\nseeded {len(done)}/{len(SEED)} ids")
if missing:
    print("NOT FOUND (id absent du corpus) :")
    for m in missing:
        print("  -", m)
