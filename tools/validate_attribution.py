#!/usr/bin/env python3
"""Validate le cablage des attributions citation -> PERSON- (etape 9, suite).

Porte gate-able : exit 0 si errors == 0, sinon exit 1.

Invariants (severite ERROR) :
  ATTR-a — couverture : toute citation a >= 1 arete d'attribution resolue OU un
           flag explicite (`attribution_non_personne` / `a_resoudre`).
  ATTR-b — narration : zero citation en narration d'auteur (locuteur anonyme +
           auteur_source present) sans arete `attribuee_a` resolue (sauf si
           l'auteur_source est lui-meme une non-personne deja flaggee).
  ATTR-c — non-personne : aucune entite non-personne (HM Treasury, Happy
           Mondays, MDMArchive, The Times) cablee en PERSON- ; flag pose et
           entite presente en pending_org.
  ATTR-d — auteurs-sources : tout PERSON- cree (origine=auteur_source) est
           autorise sans `same_as` (identite nee de l'attribution).
  XR-1   — resolution : toute cible d'arete resout vers un PERSON- existant.
  XR-3   — vocabulaire : tout predicat appartient au vocabulaire controle.
  + SSOT : sortie deterministe du generateur (option --check-drift).

Usage :
    python3 tools/validate_attribution.py
    python3 tools/validate_attribution.py --check-drift
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / "registers" / "relations" / "attribution_edges.json"
PEOPLE_JSON = ROOT / "exports" / "generated" / "people.json"
QUOTES_JSON = ROOT / "exports" / "generated" / "quotes.json"
PENDING_ORG = ROOT / "registers" / "people" / "pending_org.json"
AUTHORS_MD = ROOT / "registers" / "people" / "00_authors_canonical.md"
GENERATOR = ROOT / "tools" / "build_attribution_edges.py"

ANON = {"anonyme", "", "narration", "narrateur"}
# Vocabulaire controle des predicats d'attribution (cross_registres Sec.4 + 4.3).
PREDICATS = {"attribuee_a", "a_pour_auteur_source", "rapportee_par"}


def norm(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-drift", action="store_true")
    args = ap.parse_args(argv)

    errors = []

    if not EDGES.exists():
        print(f"ERROR: {EDGES} absent — lancer tools/build_attribution_edges.py", file=sys.stderr)
        return 1

    bundle = json.loads(EDGES.read_text(encoding="utf-8"))
    edges = {e["citation"]: e for e in bundle["edges"]}
    quotes = {r["id"]: r["data"] for r in json.loads(QUOTES_JSON.read_text(encoding="utf-8"))}

    person_ids = set()
    author_ids = set()
    id_to_name = {}
    raw_people = json.loads(PEOPLE_JSON.read_text(encoding="utf-8"))
    for p in raw_people:
        pid = p.get("id", "")
        if not str(pid).startswith("PERSON-"):
            continue
        person_ids.add(pid)
        id_to_name[pid] = p["data"].get("name", "")
        if p["data"].get("origine") == "auteur_source":
            author_ids.add(pid)

    org_names = {it.get("name") for it in json.loads(PENDING_ORG.read_text(encoding="utf-8")).get("items", [])}
    org_norm = {norm(n) for n in org_names}

    # parité couverture : toute citation de quotes.json a une entrée d'arête
    for cid in quotes:
        if cid not in edges:
            errors.append(f"[ATTR-a] citation sans entrée d'attribution : {cid}")

    n_narration = n_covered = 0
    for cid, e in edges.items():
        d = quotes.get(cid, {})
        liens = e.get("liens", [])

        # XR-3 vocabulaire + XR-1 résolution + ATTR-c (cible non-personne)
        for lk in liens:
            if lk.get("predicat") not in PREDICATS:
                errors.append(f"[XR-3] {cid}: prédicat hors vocabulaire : {lk.get('predicat')}")
            cible = lk.get("cible")
            if cible not in person_ids:
                errors.append(f"[XR-1] {cid}: cible non résolue : {cible}")
            if norm(id_to_name.get(cible, "")) in org_norm:
                errors.append(f"[ATTR-c] {cid}: entité non-personne câblée en PERSON- : {cible}")

        # ATTR-a couverture
        if liens or "attribution_non_personne" in e["flags"] or "a_resoudre" in e["flags"]:
            n_covered += 1
        else:
            errors.append(f"[ATTR-a] {cid}: ni arête résolue ni flag explicite.")

        # ATTR-b narration d'auteur reliée
        loc = (d.get("locuteur") or "").strip()
        auteur = (d.get("auteur_source") or "").strip()
        if norm(loc) in ANON and auteur:
            # narration : l'auteur_source porte la voix. Reliée sauf si l'auteur
            # est une non-personne (alors flag attendu).
            auteur_is_org = any(norm(part) in org_norm for part in re.split(r"[;,]", auteur))
            if not auteur_is_org:
                n_narration += 1
                has_attr = any(lk["predicat"] == "attribuee_a" for lk in liens)
                if not has_attr:
                    errors.append(f"[ATTR-b] narration d'auteur non reliée : {cid} (auteur_source={auteur!r}).")

    # ATTR-d : PERSON- auteurs-sources autorisés sans same_as ; un same_as non
    # vide sur une identité née de l'attribution serait une incohérence.
    for p in raw_people:
        if p.get("id") in author_ids and p["data"].get("same_as"):
            errors.append(f"[ATTR-d] {p['id']}: auteur-source créé mais same_as non vide.")

    # rapport
    st = bundle.get("stats", {})
    print(f"citations          : {len(quotes)}")
    print(f"couvertes          : {n_covered}/{len(edges)}")
    print(f"attribuee_a        : {st.get('attribue_a','?')} (narration {st.get('narration_reliee','?')}, "
          f"locuteur {st.get('locuteur_resolu','?')})")
    print(f"auteur_source edges: {st.get('auteur_source_edges','?')} | rapporteur : {st.get('rapporteur_edges','?')}")
    print(f"PERSON- créés      : {len(author_ids)}")
    print(f"a_resoudre         : {st.get('citations_a_resoudre','?')} | non_personne : {st.get('citations_non_personne','?')}")
    print(f"errors             : {len(errors)}")

    if args.check_drift:
        snap_edges = EDGES.read_text(encoding="utf-8")
        snap_auth = AUTHORS_MD.read_text(encoding="utf-8") if AUTHORS_MD.exists() else ""
        proc = subprocess.run([sys.executable, str(GENERATOR)], capture_output=True, text=True)
        if proc.returncode != 0:
            errors.append(f"[SSOT] générateur en échec : {proc.stderr.strip()[:200]}")
        else:
            if EDGES.read_text(encoding="utf-8") != snap_edges:
                errors.append("[SSOT] DRIFT : attribution_edges.json diffère de la sortie du générateur.")
            if AUTHORS_MD.exists() and AUTHORS_MD.read_text(encoding="utf-8") != snap_auth:
                errors.append("[SSOT] DRIFT : 00_authors_canonical.md diffère de la sortie du générateur.")

    if errors:
        for e in errors[:100]:
            print(f"  - ERROR {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
