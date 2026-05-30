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
    """Normalise le champ same_as en liste d'identifiants.

    Le schéma impose désormais une valeur MONO-VALUÉE (chaîne). On tolère ici
    une liste de façon DÉFENSIVE : cela permet à INV-4 (convergence unique) de
    rester un garde réel et testable même si une donnée mal formée contournait
    le schéma.
    """
    v = record.get("same_as")
    if v is None:
        return []
    return [v] if isinstance(v, str) else list(v)


def check_same_as(records):
    """Vérifie les invariants du graphe same_as et calcule la clôture transitive.

    Invariants (cf. docs/NAMING_CONVENTIONS.md §10, docs/conventions/identifiants_lieux.md) :
      INV-1 (ERREUR)  toute cible same_as résout vers un PLACE-* existant ;
      INV-2 (ERREUR)  aucun cycle dans le graphe same_as ;
      INV-3 (ERREUR)  un canonique est un point fixe (pas de same_as sortant) ;
      INV-4 (ERREUR)  toute chaîne converge vers un canonique UNIQUE ;
      INV-5 (AVERT.)  tout PLACE-* référencé hors registre lieux est résoluble — TODO ;
      INV-6 (AVERT.)  deux canoniques ne partagent pas des coordonnées identiques
                      sans justification (prudence_methodologique).

    Renvoie (erreurs, avertissements, représentant_par_id). Le représentant est
    le point fixe (identifiant canonique) de chaque composante.
    """
    ids = {r.get("id") for r, _ in records}
    edges = {}            # id -> [cibles] (liste tolérée défensivement)
    for r, _ in records:
        t = same_as_targets(r)
        if t:
            edges.setdefault(r.get("id"), []).extend(t)

    errors, warnings = [], []

    # INV-1 : cible existante.  INV-3 : la cible est un point fixe.
    for src, targets in edges.items():
        for tgt in targets:
            if tgt not in ids:
                errors.append(f"INV-1 — {src}: same_as -> {tgt} (cible inexistante)")
            elif tgt in edges:
                errors.append(
                    f"INV-3 — {src}: same_as -> {tgt}, mais {tgt} porte lui-meme "
                    f"un same_as (le canonique doit etre un point fixe)")

    # INV-2 : detection de cycle.  Resolution d'un noeud par sa 1re arete.
    def resolve(node):
        seen, cur = set(), node
        while cur in edges and cur not in seen:
            seen.add(cur)
            nxt = edges[cur][0]
            if nxt not in ids:
                return cur          # cible inexistante (deja signalee INV-1)
            cur = nxt
        if cur in seen:
            errors.append(f"INV-2 — cycle d'equivalence same_as detecte en {cur}")
        return cur

    rep = {i: resolve(i) for i in ids}

    # INV-4 : convergence unique. Defensif — si un noeud porte plusieurs cibles
    # (donnee hors-schema), toutes doivent resoudre vers le meme canonique.
    for src, targets in edges.items():
        canon = {resolve(t) for t in targets if t in ids}
        if len(canon) > 1:
            errors.append(
                f"INV-4 — {src}: same_as diverge vers plusieurs canoniques "
                f"{sorted(canon)} (une equivalence d'identite doit etre unique)")

    # INV-5 (AVERTISSEMENT) : references PLACE-* depuis d'autres registres
    # resolubles vers un canonique. Balayage cross-registres non implemente ici
    # (cf. apps/lib/dynamic-registers.js au runtime) — marque TODO plutot
    # qu'implemente a moitie.
    warnings.append(
        "INV-5 — TODO : verification cross-registres des references PLACE-* "
        "non implementee dans ce validateur (resolue au runtime par le loader).")

    # INV-6 (AVERTISSEMENT) : collisions de coordonnees entre canoniques sans
    # justification consignee (prudence_methodologique).
    coord_groups = {}
    for r, _ in records:
        rid = r.get("id")
        if rep.get(rid) != rid:
            continue            # uniquement les canoniques (points fixes)
        lat, lng = r.get("lat"), r.get("lng")
        if isinstance(lat, (int, float)) and isinstance(lng, (int, float)):
            coord_groups.setdefault((round(lat, 5), round(lng, 5)), []).append(r)
    for (lat, lng), grp in coord_groups.items():
        canon_ids = {r.get("id") for r in grp}
        if len(canon_ids) > 1 and not any(r.get("prudence_methodologique") for r in grp):
            warnings.append(
                f"INV-6 — coordonnee partagee ({lat}, {lng}) par {sorted(canon_ids)} "
                f"sans justification (prudence_methodologique).")

    return errors, warnings, rep


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
    sa_errors, sa_warnings, rep = check_same_as(records)
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

    if sa_warnings:
        print(f"\nAVERTISSEMENTS ({len(sa_warnings)}) — non bloquants :")
        for m in sa_warnings:
            print(f"  - {m}")

    if sa_errors:
        print(f"\nSAME_AS INVALIDE ({len(sa_errors)}):")
        for m in sa_errors:
            print(f"  - {m}")

    if invalid:
        print(f"\nINVALID ({len(invalid)}):")
        for pid, rel, msgs in invalid:
            print(f"  {pid}  ({rel})")
            for m in msgs:
                print(f"       - {m}")

    if invalid or sa_errors:
        return 1

    print("\nAll place records are valid (schéma + same_as INV-1..4).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
