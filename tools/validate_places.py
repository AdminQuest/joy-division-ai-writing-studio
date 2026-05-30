#!/usr/bin/env python3
"""Validate the places register against schemas/places.schema.yaml.

Replicates the runtime pipeline of apps/lib/dynamic-registers.js:
  1. parse every YAML block under registers/**.md
  2. keep place records (places: container items + standalone PLACE-* blocks)
  3. drop document-header parasites (type_unite present and != "place")
  4. validate each source record against the JSON Schema (Draft 2020-12,
     FormatChecker active)
  5. report the distinct count after id-deduplication (what the UI displays)

Usage: python3 tools/validate_places.py
Exit code 1 if any record is invalid.
"""
import glob
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "schemas" / "places.schema.yaml").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def is_place(record: dict, path: str) -> bool:
    return str(record.get("id", "")).startswith("PLACE-") or "/places/" in path.replace("\\", "/")


def is_parasite(record: dict) -> bool:
    tu = record.get("type_unite")
    return tu is not None and tu != "place"


def find_rogue_lieux_containers():
    """Locate any remaining French `lieux:` container blocks under registers/**.

    dynamic-registers.js only recognizes the canonical `places:` container, so a
    surviving `lieux:` key means a file was never normalized and its places are
    silently dropped (neither displayed nor validated). Such a file must fail
    loudly rather than pass as a false positive.
    """
    offenders = []
    for path in sorted(glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True)):
        rel = path.replace(str(ROOT) + "/", "")
        for block in YAML_BLOCK.findall(Path(path).read_text(encoding="utf-8")):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                continue
            if isinstance(data, dict) and isinstance(data.get("lieux"), list):
                offenders.append((rel, len(data["lieux"])))
    return offenders


def collect_records():
    records = []
    for path in sorted(glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True)):
        rel = path.replace(str(ROOT) + "/", "")
        for block in YAML_BLOCK.findall(Path(path).read_text(encoding="utf-8")):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                continue
            if not isinstance(data, dict):
                continue
            items = data["places"] if isinstance(data.get("places"), list) else (
                [data] if str(data.get("id", "")).startswith("PLACE-") else []
            )
            for item in items:
                if isinstance(item, dict) and is_place(item, rel) and not is_parasite(item):
                    records.append((item, rel))
    return records


def same_as_targets(record: dict):
    """Normalise le champ same_as (string | array) en liste d'identifiants."""
    v = record.get("same_as")
    if v is None:
        return []
    return [v] if isinstance(v, str) else list(v)


def check_same_as(records):
    """Valide les arêtes d'équivalence same_as et calcule la clôture transitive.

    Contraintes imposées (cf. docs/conventions/identifiants_lieux.md) :
      - cible existante : tout same_as pointe vers un id de lieu présent ;
      - canonique = point fixe : la cible ne porte pas elle-même de same_as ;
      - absence de cycle : pas de chaîne d'équivalence qui se referme.

    Renvoie (problèmes, représentant_par_id). Le représentant est le point fixe
    (l'identifiant canonique) de chaque composante union-find.
    """
    ids = {r.get("id") for r, _ in records}
    edges = {}            # id -> [cibles]
    for r, _ in records:
        t = same_as_targets(r)
        if t:
            edges.setdefault(r.get("id"), []).extend(t)

    problems = []
    # 1. cible existante + 2. canonique = point fixe
    for src, targets in edges.items():
        for tgt in targets:
            if tgt not in ids:
                problems.append(f"{src}: same_as -> {tgt} (cible inexistante)")
            elif tgt in edges:
                problems.append(
                    f"{src}: same_as -> {tgt}, mais {tgt} porte lui-même un "
                    f"same_as (le canonique doit etre un point fixe)")

    # 3. resolution + detection de cycle ; representant = point fixe
    rep = {}

    def resolve(node, seen):
        if node in seen:
            problems.append(f"cycle d'equivalence same_as detecte en {node}")
            return node
        nxt = edges.get(node)
        if not nxt or nxt[0] not in ids:
            return node
        return resolve(nxt[0], seen | {node})

    for i in ids:
        rep[i] = resolve(i, set())
    return problems, rep


def main() -> int:
    rogue = find_rogue_lieux_containers()
    if rogue:
        print("FAIL: residual legacy `lieux:` container(s) found — these files were not")
        print("normalized to `places:` and their places are silently dropped:")
        for rel, count in rogue:
            print(f"  - {rel}  ({count} entries under lieux:)")
        print("\nNormalize them (lieux: -> places:) before validation can pass.")
        return 1

    records = collect_records()
    invalid = []
    for record, rel in records:
        errors = sorted(VALIDATOR.iter_errors(record), key=str)
        if errors:
            invalid.append((record.get("id"), rel, [e.message for e in errors]))

    distinct_ids = {r.get("id") for r, _ in records}

    # Réconciliation des équivalences same_as (clôture transitive, union-find).
    sa_problems, rep = check_same_as(records)
    canonical = {rep[i] for i in distinct_ids}
    aliased = {i for i in distinct_ids if rep[i] != i}

    print(f"Source place records (parasites excluded) : {len(records)}")
    print(f"Distinct ids after id-deduplication        : {len(distinct_ids)}")
    print(f"  dont alias legacy (same_as)              : {len(aliased)}")
    print(f"Canonical places after same_as merge       : {len(canonical)}")
    print(f"Valid against schema                        : {len(records) - len(invalid)}/{len(records)}")

    if aliased:
        print("\nÉquivalences same_as résolues :")
        for a in sorted(aliased):
            print(f"  {a}  ->  {rep[a]}")

    if sa_problems:
        print(f"\nSAME_AS INVALIDE ({len(sa_problems)}):")
        for m in sa_problems:
            print(f"  - {m}")

    if invalid:
        print(f"\nINVALID ({len(invalid)}):")
        for pid, rel, msgs in invalid:
            print(f"  {pid}  ({rel})")
            for m in msgs:
                print(f"       - {m}")

    if invalid or sa_problems:
        return 1

    print("\nAll place records are valid (schéma + same_as).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
