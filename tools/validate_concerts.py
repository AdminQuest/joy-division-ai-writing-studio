#!/usr/bin/env python3
"""Validate the concert register (étape 7b).

Porte gate-able du registre concerts : exit 0 si errors == 0, sinon exit 1.

Deux strates coexistent :
  - identité canonique  CONCERT-<SLUG>  (registers/concerts/concert_canonical_units.md)
  - legacy joydiv        JD-CONCERT-…    (registers/concerts/00_canonical_concerts.md),
    réconciliée par `same_as` (porté côté legacy) vers son CONCERT-.

Invariants (severité ERROR sauf mention) :
  INV1 — same_as : toute cible `same_as` d'un legacy résout vers un CONCERT-
         existant ; un CONCERT- canonique est un point fixe (pas de same_as
         sortant : ni cycle ni chaîne) ; ≤ 1 same_as par legacy (mono-valué).
  INV2 — unicité : id CONCERT- unique ; tout legacy ∈ AU PLUS un canonique
         (`membres_reconcilies`) ; cohérence bijective legacy.same_as ⇄
         canonique.membres_reconcilies.
  INV3 — cohérence temporelle : `date` (ou `date_debut`/`date_fin`) bien formée
         et non impossible ; date_debut ≤ date_fin.
  INV4 — honnêteté date_precision : valeur ∈ vocabulaire fermé ; pas plus précise
         que la chaîne `date` (jour ⇒ AAAA-MM-JJ ; mois ⇒ AAAA-MM).
  INV5 — intégrité lieu : tout `lieu` d'un CONCERT- résout vers un PLACE- existant.
  INV6 — statut : statut ∈ {confirmé, annulé, douteux}.
  + schéma : champs requis de l'identité canonique (schema_validation.concert).

Usage : python3 tools/validate_concerts.py
"""
from __future__ import annotations
import glob
import re
import sys
import datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_against_schema  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONCERTS_DIR = ROOT / "registers" / "concerts"
YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

PRECISIONS = {"jour", "mois", "saison", "annee", "circa", "intervalle"}
STATUTS = {"confirmé", "annulé", "douteux"}


def iter_blocks(path: Path):
    for block in YAML_BLOCK.findall(path.read_text(encoding="utf-8")):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(data, list):
            for it in data:
                if isinstance(it, dict):
                    yield it
        elif isinstance(data, dict):
            if isinstance(data.get("places"), list):
                continue
            yield data


def collect_place_ids():
    ids = set()
    for path in glob.glob(str(ROOT / "registers" / "**" / "*.md"), recursive=True):
        for block in YAML_BLOCK.findall(Path(path).read_text(encoding="utf-8")):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError:
                continue
            items = data["places"] if isinstance(data, dict) and isinstance(data.get("places"), list) else (
                [data] if isinstance(data, dict) else [])
            for it in items:
                if isinstance(it, dict) and str(it.get("id", "")).startswith("PLACE-"):
                    if it.get("type_unite") in (None, "place"):
                        ids.add(str(it["id"]))
    return ids


def parse_iso(d: str):
    """Return a date object or None; accepts AAAA, AAAA-MM, AAAA-MM-JJ."""
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.datetime.strptime(d, fmt).date()
        except ValueError:
            continue
    return None


def date_granularity(d: str):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return "jour"
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return "mois"
    if re.fullmatch(r"\d{4}", d):
        return "annee"
    return None


def main() -> int:
    place_ids = collect_place_ids()

    canon = {}     # CONCERT- id -> record
    legacy = {}    # JD-CONCERT- id -> record
    for path in sorted(CONCERTS_DIR.glob("*.md")):
        for rec in iter_blocks(path):
            rid = str(rec.get("id", ""))
            if rid.startswith("CONCERT-"):
                canon[rid] = rec
            elif rid.startswith("JD-CONCERT-") and "YYYYMMDD" not in rid:
                legacy[rid] = rec

    errors, warnings = [], []

    # ---- INV2 : unicité des CONCERT- (le parse écrase les doublons : on
    # recompte sur les occurrences brutes pour détecter une collision d'id). ----
    raw_ids = []
    for path in sorted(CONCERTS_DIR.glob("*.md")):
        for rec in iter_blocks(path):
            rid = str(rec.get("id", ""))
            if rid.startswith("CONCERT-"):
                raw_ids.append(rid)
    seen = set()
    for rid in raw_ids:
        if rid in seen:
            errors.append(f"INV2 — id CONCERT- dupliqué : {rid}")
        seen.add(rid)

    # membership map : legacy -> set(canonique le listant)
    member_of = {}
    for cid, rec in canon.items():
        membres = rec.get("membres_reconcilies") or []
        if not isinstance(membres, list) or not membres:
            errors.append(f"INV2 — {cid} : membres_reconcilies vide ou absent")
            continue
        for m in membres:
            member_of.setdefault(str(m), set()).add(cid)
    for m, owners in member_of.items():
        if len(owners) > 1:
            errors.append(f"INV2 — legacy {m} listé par plusieurs canoniques {sorted(owners)}")
        if m not in legacy and m.startswith("JD-CONCERT-"):
            errors.append(f"INV2 — membre {m} de {sorted(owners)} introuvable parmi les legacy")

    # ---- INV1 : same_as côté legacy ----
    for lid, rec in legacy.items():
        sa = rec.get("same_as")
        if sa is None:
            continue  # legacy non réconcilié (toléré : périmètre partiel 7b-1)
        if isinstance(sa, list):
            errors.append(f"INV1 — {lid} : same_as multivalué {sa} (mono-valué requis)")
            targets = sa
        else:
            targets = [sa]
        for t in targets:
            t = str(t)
            if t not in canon:
                errors.append(f"INV1 — {lid} : same_as -> {t} (cible CONCERT- inexistante)")
            else:
                # INV1 : pas de chaîne — la cible ne doit pas elle-même porter same_as
                if canon[t].get("same_as") is not None:
                    errors.append(f"INV1 — {lid} -> {t}, mais {t} porte un same_as (chaîne interdite)")
                # INV2 : cohérence bijective
                if lid not in (str(x) for x in (canon[t].get("membres_reconcilies") or [])):
                    errors.append(
                        f"INV2 — {lid}.same_as={t} mais {lid} absent de "
                        f"{t}.membres_reconcilies")

    # un CONCERT- canonique ne doit pas porter de same_as (point fixe)
    for cid, rec in canon.items():
        if rec.get("same_as") is not None:
            errors.append(f"INV1 — {cid} (canonique) porte un same_as : doit être un point fixe")

    # ---- INV3/INV4/INV5/INV6 + schéma sur les canoniques ----
    for cid, rec in canon.items():
        # schéma (champs requis, date XOR intervalle, membres non vide)
        for msg in validate_against_schema("concert", rec):
            errors.append(f"SCHEMA — {cid} : {msg}")

        # INV6 statut
        statut = rec.get("statut")
        if statut is not None and statut not in STATUTS:
            errors.append(f"INV6 — {cid} : statut '{statut}' hors {sorted(STATUTS)}")

        # INV5 lieu
        lieu = rec.get("lieu")
        if lieu is None:
            pass  # déjà signalé par le schéma (champ requis)
        elif str(lieu) not in place_ids:
            errors.append(f"INV5 — {cid} : lieu {lieu} ne résout vers aucun PLACE- existant")

        # INV4 precision
        prec = rec.get("date_precision")
        if prec is not None and prec not in PRECISIONS:
            errors.append(f"INV4 — {cid} : date_precision '{prec}' hors {sorted(PRECISIONS)}")

        # INV3 temporel + INV4 honnêteté
        has_date = "date" in rec
        has_interval = "date_debut" in rec and "date_fin" in rec
        if has_interval:
            d0, d1 = parse_iso(str(rec["date_debut"])), parse_iso(str(rec["date_fin"]))
            if d0 is None or d1 is None:
                errors.append(f"INV3 — {cid} : intervalle mal formé ({rec.get('date_debut')}/{rec.get('date_fin')})")
            elif d0 > d1:
                errors.append(f"INV3 — {cid} : date_debut > date_fin")
        elif has_date:
            dstr = str(rec["date"])
            if parse_iso(dstr) is None:
                errors.append(f"INV3 — {cid} : date impossible/mal formée '{dstr}'")
            else:
                gran = date_granularity(dstr)
                # honnêteté : 'jour' exige AAAA-MM-JJ ; 'mois' exige AAAA-MM
                if prec == "jour" and gran != "jour":
                    errors.append(f"INV4 — {cid} : date_precision=jour mais date='{dstr}' (granularité {gran})")
                if prec == "mois" and gran not in ("mois",):
                    errors.append(f"INV4 — {cid} : date_precision=mois mais date='{dstr}' (granularité {gran})")

    # ---- report ----
    print(f"PLACE- existants                : {len(place_ids)}")
    print(f"Identités canoniques CONCERT-   : {len(canon)}")
    print(f"Legacy JD-CONCERT-              : {len(legacy)}")
    print(f"  dont réconciliés (same_as)    : {sum(1 for r in legacy.values() if r.get('same_as') is not None)}")
    print(f"Invariants : errors={len(errors)} warnings={len(warnings)}")
    if warnings:
        print("\nAVERTISSEMENTS :")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("\nERREURS :")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nTous les invariants concerts sont vérifiés (INV1..6 + schéma).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
