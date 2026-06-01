#!/usr/bin/env python3
"""Câble place_id dans registers/concerts/00_canonical_concerts.md (étape 10).

Insère `  place_id: PLACE-XXX` après la ligne `lieu:` de chaque fiche concert
dont (lieu, ville) correspond à un PLACE- disponible. Ne modifie QUE place_id
(idempotent : skip si déjà présent). Mapping déterministe, ville-scopé.

Décisions humaines intégrées :
  - « The Factory I » (+ variante « Russell Club ») -> PLACE-RUSSELL-CLUB ;
    « The Factory II » EXCLU (venue distincte).
  - « Salford College of Technology » -> PLACE-SALFORD-TECHNICAL-COLLEGE
    (alias same_as -> PLACE-S83-004).
Venues existantes câblées aussi : Electric Circus, Rafters, Free Trade Hall, Pips.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "registers" / "concerts" / "00_canonical_concerts.md"


def n(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


# place_id -> (ville_norm, set/predicate de lieu_norm)
# Les 60 venues du lot 3 (ville, mots-clés) :
KW = {
"PLACE-9-30-CLUB-WASHINGTON":("washington",["9 30"]),
"PLACE-ACTIONSPACE-LONDON":("london",["actionspace"]),
"PLACE-AJANTA-THEATRE-DERBY":("derby",["ajanta"]),
"PLACE-AMERICAN-INDIAN-CENTER-SF":("san francisco",["american indian"]),
"PLACE-ASTORIA-EDINBURGH":("edinburgh",["astoria"]),
"PLACE-BAND-ON-THE-WALL":("manchester",["band on the wall"]),
"PLACE-BOLTON-INSTITUTE-OF-TECHNOLOGY":("bolton",["institute of technology"]),
"PLACE-BOOKIES-DETROIT":("detroit",["bookies"]),
"PLACE-BOWDON-VALE-YOUTH-CLUB":("altrincham",["bowdon vale"]),
"PLACE-BRUNEL-UNIVERSITY":("uxbridge",["brunel"]),
"PLACE-CAIRD-HALL-DUNDEE":("dundee",["caird"]),
"PLACE-CAPITOL-ABERDEEN":("aberdeen",["capitol"]),
"PLACE-CITY-HALL-CORK":("cork",["city hall"]),
"PLACE-DUFFYS-MINNEAPOLIS":("minneapolis",["duffy"]),
"PLACE-FAN-CLUB-LEEDS":("leeds",["fan club"]),
"PLACE-FLIPPERS-LOS-ANGELES":("los angeles",["flipper"]),
"PLACE-HIGH-WYCOMBE-TOWN-HALL":("high wycombe",["town hall"]),
"PLACE-HURRAH-NEW-YORK":("new york",["hurrah"]),
"PLACE-KELLYS-MANCHESTER":("manchester",["kelly"]),
"PLACE-LANTAREN-ROTTERDAM":("rotterdam",["lantaren"]),
"PLACE-LEEDS-UNIVERSITY":("leeds",["leeds university"]),
"PLACE-LIMIT-CLUB-SHEFFIELD":("sheffield",["limit"]),
"PLACE-LOCARNO-BRISTOL":("bristol",["locarno"]),
"PLACE-MANCHESTER-APOLLO":("manchester",["apollo"]),
"PLACE-MOUNTFORD-HALL-LIVERPOOL":("liverpool",["mountford"]),
"PLACE-NEW-THEATRE-OXFORD":("oxford",["new theatre"]),
"PLACE-NEWCASTLE-CITY-HALL":("newcastle",["city hall"]),
"PLACE-NEWCASTLE-GUILDHALL":("newcastle",["guild hall","guildhall"]),
"PLACE-ODEON-BIRMINGHAM":("birmingham",["odeon"]),
"PLACE-ODEON-CANTERBURY":("canterbury",["odeon"]),
"PLACE-ODEON-EDINBURGH":("edinburgh",["odeon"]),
"PLACE-OLYMPIA-DUBLIN":("dublin",["olympia"]),
"PLACE-PAARD-VAN-TROJE-THE-HAGUE":("the hague",["paard"]),
"PLACE-PAVILION-HEMEL-HEMPSTEAD":("hemel hempstead",["pavilion"]),
"PLACE-PIPERS-CYPRUS-TAVERN":("manchester",["pipers"]),
"PLACE-PLAYHOUSE-THEATRE-NOTTINGHAM":("nottingham",["playhouse"]),
"PLACE-ROCK-GARDEN-MIDDLESBROUGH":("middlesbrough",["rock garden"]),
"PLACE-ROYALTY-THEATRE-LONDON":("london",["royalty"]),
"PLACE-SCALA-CINEMA-LONDON":("london",["scala"]),
"PLACE-SHEFFIELD-POLYTECHNIC":("sheffield",["polytechnic"]),
"PLACE-SOPHIA-GARDENS-CARDIFF":("cardiff",["sophia"]),
"PLACE-SOUTHAMPTON-UNIVERSITY":("southampton",["southampton university"]),
"PLACE-ST-ANDREWS-UNIVERSITY":("st andrews",["st andrews"]),
"PLACE-ST-GEORGES-HALL-BRADFORD":("bradford",["george"]),
"PLACE-STARWOOD-LOS-ANGELES":("los angeles",["starwood"]),
"PLACE-STOCKPORT-COLLEGE":("stockport",["stockport"]),
"PLACE-TIER-3-NEW-YORK":("new york",["tier 3"]),
"PLACE-TIFFANYS-LEICESTER":("leicester",["tiffany"]),
"PLACE-TOP-RANK-READING":("reading",["top rank"]),
"PLACE-TOP-RANK-SHEFFIELD":("sheffield",["top rank"]),
"PLACE-ULSTER-HALL-BELFAST":("belfast",["ulster"]),
"PLACE-UNIVERSITY-OF-KENT":("canterbury",["university of kent"]),
"PLACE-UNIVERSITY-OF-LONDON-UNION":("london",["university of london"]),
"PLACE-WEST-RUNTON-PAVILION":("west runton",["pavilion"]),
"PLACE-WINTER-GARDENS-MALVERN":("malvern",["winter gardens"]),
"PLACE-YMCA-LONDON":("london",["ymca"]),
# Venues DÉJÀ présentes dans registers/places/ (câblées aussi) :
"PLACE-ELECTRIC-CIRCUS":("manchester",["electric circus"]),
"PLACE-RAFTERS-MANCHESTER":("manchester",["rafters"]),
"PLACE-FREE-TRADE-HALL":("manchester",["free trade hall"]),
"PLACE-PIPS":("manchester",["pips"]),
}
# LIVERPOOL-EMPIRE et OLDHAM-TOWER-CLUB : créés sans câblage (aucun concert).


def place_for(lieu, ville):
    ln, vn = n(lieu), n(ville)
    # Cas spéciaux tranchés
    if vn == "manchester" and ln in ("the factory i", "the factory i russell club"):
        return "PLACE-RUSSELL-CLUB"
    if vn == "manchester" and ln == "the factory ii":
        return None  # venue distincte, hors lot
    if vn == "salford" and "college of technology" in ln:
        return "PLACE-SALFORD-TECHNICAL-COLLEGE"
    # Mapping général ville-scopé
    for pid, (pville, kws) in KW.items():
        if vn == pville and any(k in ln for k in kws):
            return pid
    return None


lines = MD.read_text(encoding="utf-8").splitlines()
# Index json pour (cid -> lieu,ville)
meta = {r["data"]["id"]: (r["data"].get("lieu", ""), r["data"].get("ville", ""))
        for r in json.load(open(ROOT / "exports/generated/concerts.json"))}

out, report = [], []
cur_id = None
i = 0
while i < len(lines):
    line = lines[i]
    out.append(line)
    m = re.match(r"^- id:\s*(JD-CONCERT-\S+)", line.strip()) or re.match(r"^-\s*id:\s*(JD-CONCERT-\S+)", line)
    mm = re.match(r"^\s*-?\s*id:\s*(JD-CONCERT-\S+)\s*$", line)
    if mm:
        cur_id = mm.group(1)
    # ligne lieu d'une fiche : insérer place_id juste après
    lm = re.match(r"^(\s*)lieu:\s*", line)
    if lm and cur_id and cur_id in meta:
        # éviter doublon : place_id déjà présent dans les lignes suivantes du bloc ?
        already = False
        for j in range(i + 1, min(i + 14, len(lines))):
            if re.match(r"^\s*-?\s*id:\s*JD-CONCERT", lines[j]):
                break
            if re.match(r"^\s*place_id:", lines[j]):
                already = True
                break
        lieu, ville = meta[cur_id]
        pid = place_for(lieu, ville)
        if pid and not already:
            out.append(f"{lm.group(1)}place_id: {pid}")
            report.append((cur_id, lieu, ville, pid))
        cur_id_used = True
    i += 1

MD.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"câblés : {len(report)} concerts")
from collections import Counter
by = Counter(r[3] for r in report)
for pid, c in sorted(by.items(), key=lambda x: (-x[1], x[0])):
    print(f"  {c:2}  {pid}")
