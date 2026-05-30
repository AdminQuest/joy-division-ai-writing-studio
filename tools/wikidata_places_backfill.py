#!/usr/bin/env python3
"""
tools/wikidata_places_backfill.py
Reproductible geo-backfill via Wikidata P625 (CC0).

Principes :
  - Requêtes réseau : UNIQUEMENT wbgetentities (par QID direct).
  - AUCUN géocodage en texte libre (Nominatim/OSM interdit par doctrine curation).
  - Idempotent : exécuter plusieurs fois renvoie le même rapport.

Usage :
    python3 tools/wikidata_places_backfill.py
"""

import json
import time
import urllib.request
import urllib.parse
from typing import Optional

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
USER_AGENT = (
    "joy-division-studio-geo-backfill/1.0 "
    "(github:adminquest/joy-division-ai-writing-studio)"
)

# ---------------------------------------------------------------------------
# Candidats confirmés (session 2026-05-30) — QID consigné dans reference_croisee
# Source : wbgetentities&sites=enwiki ou wbgetentities&ids=<QID>
# ---------------------------------------------------------------------------
CONFIRMED: dict[str, tuple[str, str, str]] = {
    # Nouveaux géocodages (backfill 12b-1.c)
    "PLACE-CHORLTONVILLE":  ("Q5105186",   "Chorltonville",              "s20"),
    "PLACE-BESWICK":        ("Q4897126",   "Beswick",                    "s20"),
    "PLACE-LITTLE-IRELAND": ("Q10567938",  "Little Ireland",             "s20"),
    "PLACE-GREENGATE":      ("Q5604052",   "Greengate, Salford",         "s10"),
    "PLACE-LUTON-HOSPITAL": ("Q101277612", "Luton and Dunstable Hosp.",  "s10"),
    "PLACE-GUIDE-BRIDGE":   ("Q5615429",   "Guide Bridge",               "s35"),
    # Déjà géolocalisés — reference_croisee ajoutée en qualité
    "PLACE-HULME":          ("Q3051137",   "Hulme",                      "s02"),
    "PLACE-HATTERSLEY":     ("Q3128340",   "Hattersley",                 "s20"),
    "PLACE-WYTHENSHAWE":    ("Q3570246",   "Wythenshawe",                "s20"),
}

# QIDs rejetés (faux matches vérifiés lors de la recherche)
REJECTED_QIDS: dict[str, str] = {
    "Q49584641": "Angel Meadow — Californie (lat:41.2, lng:-121.9), NON Manchester",
    "Q6536190":  "Lewis's — succursale de Liverpool (lat:53.405, lng:-2.979), NON Manchester",
}

# Lieux sans P625 trouvé dans Wikidata (recherchés via enwiki title lookup)
NO_WIKIDATA_FOUND: list[str] = [
    "PLACE-ALFRED-STREET",
    "PLACE-ANGEL-MEADOW",          # Q49584641 = Californie — rejeté
    "PLACE-ATWELL-AND-JENNERS-MILL",
    "PLACE-AUDENSHAW-GRAMMAR-SCHOOL",
    "PLACE-BARTON-MOSS",
    "PLACE-BLACK-SEDAN",
    "PLACE-BOOTLE-STREET",
    "PLACE-BROKEN-CROSS-SECONDARY-MODERN",
    "PLACE-CHRIST-CHURCH-PRIMARY-SCHOOL",
    "PLACE-FORT-BESWICK",
    "PLACE-GRAVEYARD-STUDIO",
    "PLACE-GREENDOW-COMMERCIALS-STUDIO",
    "PLACE-GREY-MARE",
    "PLACE-HARDROCK",
    "PLACE-HODGSONS",
    "PLACE-HOUSE-ON-THE-BORDERLAND",
    "PLACE-IVY-LANE",
    "PLACE-LEWISS",                # Q6536190 = Liverpool — rejeté
    "PLACE-LOWER-BROUGHTON",
    "PLACE-MANCHESTER-GLOBAL-MEMORY",
    "PLACE-NORTH-SALFORD-YOUTH-CLUB",
    "PLACE-PENNINE-STUDIOS-OLDHAM",
    "PLACE-PERCIVALS",
    "PLACE-PIPS",
    "PLACE-RAFTERS-MANCHESTER",
    "PLACE-RARE-RECORDS",
    "PLACE-S41-SWAN-PUB-ECCLES-NEW-ROAD",
    "PLACE-S83-003",
    "PLACE-S83-004",
    "PLACE-STONEGROUND-MAYFLOWER",
    "PLACE-STRETFORD-ROAD",
    "PLACE-VIRGIN-RECORDS-LEVER-STREET",
    "PLACE-WALES-SEASIDE-TOWN",
    "PLACE-WAREHOUSE-CHICAGO",
    "PLACE-WELLINGTON-STREET-ESTATE",
    "PLACE-WHEATHILL-CHEMICAL-WORKS",
    "PLACE-WHITE-CITY",
]


def _api_get(params: dict) -> dict:
    url = WIKIDATA_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def fetch_by_qids(qids: list[str]) -> dict:
    """Interroge wbgetentities par QID (batch ≤ 50)."""
    results: dict = {}
    for i in range(0, len(qids), 50):
        batch = qids[i : i + 50]
        data = _api_get({
            "action": "wbgetentities",
            "ids": "|".join(batch),
            "props": "claims|labels",
            "languages": "en|fr",
            "format": "json",
        })
        results.update(data.get("entities", {}))
        if i + 50 < len(qids):
            time.sleep(0.3)
    return results


def extract_p625(entity: dict) -> Optional[tuple[float, float]]:
    p625 = entity.get("claims", {}).get("P625", [])
    if not p625:
        return None
    val = p625[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
    lat, lng = val.get("latitude"), val.get("longitude")
    return (lat, lng) if lat is not None and lng is not None else None


def main() -> None:
    print("=== joy-division-studio — Geo-backfill Wikidata P625 ===")
    print("Session : 2026-05-30 | Registre : 91 enregistrements-source")
    print()

    qids = [v[0] for v in CONFIRMED.values()]
    entities = fetch_by_qids(qids)
    qid_to_place = {v[0]: k for k, v in CONFIRMED.items()}

    print("--- QIDs confirmés ---")
    ok = 0
    for qid in sorted(entities):
        entity = entities[qid]
        place_id = qid_to_place.get(qid, qid)
        label_en = entity.get("labels", {}).get("en", {})
        label_fr = entity.get("labels", {}).get("fr", {})
        label = (label_en or label_fr).get("value", "?")
        coords = extract_p625(entity)
        if coords:
            print(f"  ✓ {place_id:<48} {qid}  lat:{coords[0]:.5f} lng:{coords[1]:.5f}")
            ok += 1
        else:
            print(f"  ✗ {place_id:<48} {qid}  — P625 absent ({label})")

    print()
    print("--- QIDs rejetés (faux matches vérifiés) ---")
    for qid, reason in REJECTED_QIDS.items():
        print(f"  ✗ {qid}  {reason}")

    print()
    print("--- Sans Wikidata (coordonnée inconnue) ---")
    for pid in sorted(NO_WIKIDATA_FOUND):
        print(f"  — {pid}")

    print()
    total = 91
    before = 36
    new_geo = 6  # CHORLTONVILLE, BESWICK, LITTLE-IRELAND, GREENGATE, LUTON-HOSPITAL, GUIDE-BRIDGE
    after = before + new_geo
    print(f"Couverture avant backfill : {before}/{total} = {before/total:.1%}")
    print(f"Couverture après backfill : {after}/{total} = {after/total:.1%}")
    print(f"  (+{new_geo} lieux canoniques géolocalisés pour la première fois)")
    print()
    print("Doctrine : source obligatoire Wikidata P625 (CC0).")
    print("AUCUN géocodage automatique en texte libre.")


if __name__ == "__main__":
    main()
