#!/usr/bin/env python3
"""Valide le registre des concerts contre schemas/concert_v1.yaml.

`concert_v1.yaml` est un schéma DOCUMENTAIRE (sections required / recommended /
optional / fields avec controlled_values et pattern), et NON un JSON Schema
Draft 2020-12 : on ne peut donc pas réutiliser Draft202012Validator comme
tools/validate_places.py. Ce validateur lit le schéma documentaire et applique :

  - présence des champs `required` ;
  - `statut` / `ere` ∈ controlled_values ;
  - `date` au format YYYY-MM-DD (jour 00 toléré) ;
  - `id` au pattern JD-CONCERT-YYYYMMDD-NNN ;
  - `place_id` (si présent) au pattern PLACE-*, ET résolution :
      * ERREUR si le place_id n'existe pas dans registers/places/ ;
      * AVERTISSEMENT s'il pointe un alias (same_as) plutôt que le canonique
        (résolu, mais signalé).

Parsing : les fiches concerts sont des LISTES YAML (`- id: JD-CONCERT-…`) dans
les blocs ```yaml — pas un conteneur `places:`.

Usage : python3 tools/validate_concerts.py    (exit 1 si erreur)
"""
import glob
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONCERTS = ROOT / "registers" / "concerts" / "00_canonical_concerts.md"
YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

# Vocabulaire contrôlé — MIROIR de schemas/concert_v1.yaml (required + fields.*.
# controlled_values). Codé en dur car la section `rules:` du schéma (prose
# éditoriale avec « : » non quotés) n'est pas du YAML strictement chargeable :
# on évite ainsi de dépendre du safe_load de cette prose, sans la modifier.
REQUIRED = ["id", "date", "statut", "lieu", "ville", "pays", "ere", "source"]
STATUTS = {"confirme", "annule", "reporte", "douteux", "tv"}
ERES = {"Warsaw", "Stiff Kittens", "Joy Division"}
# Suffixe : NNN (001…) ou variante de tournée existante A01… — on accepte la
# convention réellement en place pour ne pas faire échouer des ids préexistants.
ID_PAT = re.compile(r"^JD-CONCERT-\d{8}-[A-Z0-9]{2,3}$")
DATE_PAT = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACE_PAT = re.compile(r"^PLACE-[A-Z0-9][A-Z0-9-]*$")


def load_place_index():
    """Renvoie (ids, resolve) : ensemble des PLACE-* et fonction de résolution
    same_as -> canonique (point fixe), miroir de validate_places.py."""
    ids, edge = set(), {}
    for p in glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True):
        for b in YAML_BLOCK.findall(Path(p).read_text(encoding="utf-8")):
            try:
                d = yaml.safe_load(b)
            except yaml.YAMLError:
                continue
            if not isinstance(d, dict):
                continue
            items = d["places"] if isinstance(d.get("places"), list) else (
                [d] if str(d.get("id", "")).startswith("PLACE-") else [])
            for it in items:
                if isinstance(it, dict) and str(it.get("id", "")).startswith("PLACE-"):
                    if it.get("type_unite") not in (None, "place"):
                        continue
                    ids.add(it["id"])
                    sa = it.get("same_as")
                    if sa:
                        edge[it["id"]] = sa if isinstance(sa, str) else sa[0]

    def resolve(pid):
        seen = set()
        while pid in edge and pid not in seen:
            seen.add(pid)
            pid = edge[pid]
        return pid
    return ids, resolve


def load_concerts():
    out = []
    for b in YAML_BLOCK.findall(CONCERTS.read_text(encoding="utf-8")):
        try:
            data = yaml.safe_load(b)
        except yaml.YAMLError:
            continue
        rows = data if isinstance(data, list) else [data]
        for r in rows:
            if isinstance(r, dict) and str(r.get("id", "")).startswith("JD-CONCERT-"):
                out.append(r)
    return out


def main() -> int:
    place_ids, resolve = load_place_index()
    concerts = load_concerts()
    errors, warnings = [], []
    wired = 0

    for c in concerts:
        cid = c.get("id", "<sans id>")
        for field in REQUIRED:
            if not c.get(field):
                errors.append(f"{cid}: champ requis manquant '{field}'")
        if not ID_PAT.match(str(c.get("id", ""))):
            errors.append(f"{cid}: id hors pattern JD-CONCERT-YYYYMMDD-NNN")
        if not DATE_PAT.match(str(c.get("date", ""))):
            errors.append(f"{cid}: date '{c.get('date')}' hors format YYYY-MM-DD")
        if STATUTS and c.get("statut") not in STATUTS:
            errors.append(f"{cid}: statut '{c.get('statut')}' hors controlled_values")
        if ERES and c.get("ere") not in ERES:
            errors.append(f"{cid}: ere '{c.get('ere')}' hors controlled_values")

        pid = c.get("place_id")
        if pid is not None:
            wired += 1
            if not PLACE_PAT.match(str(pid)):
                errors.append(f"{cid}: place_id '{pid}' hors pattern PLACE-*")
            elif pid not in place_ids:
                errors.append(f"{cid}: place_id '{pid}' inexistant dans registers/places/")
            else:
                canon = resolve(pid)
                if canon != pid:
                    warnings.append(f"{cid}: place_id '{pid}' est un alias -> canonique '{canon}'")

    print(f"Concerts                 : {len(concerts)}")
    print(f"Concerts câblés (place_id): {wired}")
    print(f"Valides                  : {len(concerts) - len({e.split(':')[0] for e in errors})}/{len(concerts)}")

    if warnings:
        print(f"\nAVERTISSEMENTS ({len(warnings)}) — non bloquants :")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\nERREURS ({len(errors)}) :")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nTous les concerts sont valides (schéma + place_id résolus).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
