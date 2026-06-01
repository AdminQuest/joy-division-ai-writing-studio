#!/usr/bin/env python3
"""Validate le cablage des attributions citation -> PERSON- (etape 9, suite).

Porte gate-able : exit 0 si errors == 0, sinon exit 1.

Resolution NON CIRCULAIRE : l'ensemble des PERSON- est reconstruit depuis les
DEUX registers SSOT — couche canonique #47 (registers/people/00_canonical_people.md)
UNION le register des auteurs-sources (registers/people/00_authors_canonical.md).
On ne lit JAMAIS exports/generated/people.json (potentiellement perime ou
auto-referentiel).

Invariants (severite ERROR) :
  ATTR-a — couverture : toute citation a >= 1 arete d'attribution resolue OU un
           flag explicite (`attribution_non_personne` / `a_resoudre`).
  ATTR-b — narration : zero citation en narration d'auteur (locuteur anonyme +
           auteur_source present) sans arete `attribuee_a` resolue (sauf si
           l'auteur_source est lui-meme une non-personne deja flaggee).
  ATTR-c — non-personne : aucune entite non-personne (HM Treasury, Happy
           Mondays, MDMArchive, The Times) cablee en PERSON-.
  ATTR-d — auteurs-sources : tout PERSON- du register des auteurs porte
           origine=auteur_source et same_as vide.
  XR-1   — resolution : toute cible d'arete resout vers un PERSON- des registers.
  XR-3   — vocabulaire : tout predicat appartient au vocabulaire controle.

Sentinelle anti-recidive (--check-drift) — Correctif 4 de la revue Codex :
  Execute build_registers DEUX FOIS (avec build_attribution_edges entre) et
  verifie :
    (a) 00_authors_canonical.md byte-identique au 2e passage (aucun
        « Total créés : 0 » parasite, aucun auteur supprime) ;
    (b) les 38 PERSON- origine=auteur_source toujours presents apres le 2e build ;
    (c) validate_attribution = 0 cible non resolue apres le 2e build.
  C'est ce double passage qui manquait et qui aurait du attraper le bug
  d'oscillation 38<->0 du register des auteurs.

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
from typing import Dict, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / "registers" / "relations" / "attribution_edges.json"
QUOTES_JSON = ROOT / "exports" / "generated" / "quotes.json"
PENDING_ORG = ROOT / "registers" / "people" / "pending_org.json"
CANON_MD = ROOT / "registers" / "people" / "00_canonical_people.md"
AUTHORS_MD = ROOT / "registers" / "people" / "00_authors_canonical.md"
PEOPLE_JSON = ROOT / "exports" / "generated" / "people.json"  # checks (b) only
GEN = ROOT / "tools" / "build_attribution_edges.py"
BUILD_REGISTERS = ROOT / "tools" / "build_registers.py"

ANON = {"anonyme", "", "narration", "narrateur"}
PREDICATS = {"attribuee_a", "a_pour_auteur_source", "rapportee_par"}
YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def norm(s):
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def parse_person_register(path: Path):
    """Parse un register de PERSON- (md a blocs YAML). Retourne la liste des dicts."""
    out = []
    if not path.exists():
        return out
    for block in YAML_BLOCK.findall(path.read_text(encoding="utf-8")):
        try:
            d = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(d, dict) and str(d.get("id", "")).startswith("PERSON-"):
            out.append(d)
    return out


def load_person_universe() -> Tuple[Set[str], Dict[str, str], Set[str]]:
    """Univers PERSON- = registre #47 UNION registre des auteurs (depuis les md).

    Retourne (person_ids, id_to_name, author_ids).
    """
    person_ids: Set[str] = set()
    id_to_name: Dict[str, str] = {}
    author_ids: Set[str] = set()
    for rec in parse_person_register(CANON_MD):
        person_ids.add(rec["id"])
        id_to_name[rec["id"]] = rec.get("name", "")
    for rec in parse_person_register(AUTHORS_MD):
        person_ids.add(rec["id"])
        id_to_name[rec["id"]] = rec.get("name", "")
        author_ids.add(rec["id"])
    return person_ids, id_to_name, author_ids


def run_gate() -> Tuple[int, dict]:
    """Exécute les invariants ATTR/XR. Retourne (n_errors, infos)."""
    errors = []
    if not EDGES.exists():
        return 1, {"fatal": f"{EDGES} absent"}

    bundle = json.loads(EDGES.read_text(encoding="utf-8"))
    edges = {e["citation"]: e for e in bundle["edges"]}
    quotes = {r["id"]: r["data"] for r in json.loads(QUOTES_JSON.read_text(encoding="utf-8"))}

    person_ids, id_to_name, author_ids = load_person_universe()
    org_names = {it.get("name") for it in json.loads(PENDING_ORG.read_text(encoding="utf-8")).get("items", [])}
    org_norm = {norm(n) for n in org_names}

    # parité couverture
    for cid in quotes:
        if cid not in edges:
            errors.append(f"[ATTR-a] citation sans entrée d'attribution : {cid}")

    n_unresolved = n_covered = n_narration = 0
    for cid, e in edges.items():
        d = quotes.get(cid, {})
        liens = e.get("liens", [])
        for lk in liens:
            if lk.get("predicat") not in PREDICATS:
                errors.append(f"[XR-3] {cid}: prédicat hors vocabulaire : {lk.get('predicat')}")
            cible = lk.get("cible")
            if cible not in person_ids:
                errors.append(f"[XR-1] {cid}: cible non résolue : {cible}")
                n_unresolved += 1
            if norm(id_to_name.get(cible, "")) in org_norm:
                errors.append(f"[ATTR-c] {cid}: entité non-personne câblée en PERSON- : {cible}")

        if liens or "attribution_non_personne" in e["flags"] or "a_resoudre" in e["flags"]:
            n_covered += 1
        else:
            errors.append(f"[ATTR-a] {cid}: ni arête résolue ni flag explicite.")

        loc = (d.get("locuteur") or "").strip()
        auteur = (d.get("auteur_source") or "").strip()
        if norm(loc) in ANON and auteur:
            auteur_is_org = any(norm(part) in org_norm for part in re.split(r"[;,]", auteur))
            if not auteur_is_org:
                n_narration += 1
                if not any(lk["predicat"] == "attribuee_a" for lk in liens):
                    errors.append(f"[ATTR-b] narration d'auteur non reliée : {cid} (auteur_source={auteur!r}).")

    # ATTR-d : register des auteurs — origine=auteur_source, same_as vide.
    for rec in parse_person_register(AUTHORS_MD):
        if rec.get("origine") != "auteur_source":
            errors.append(f"[ATTR-d] {rec['id']}: register auteurs sans origine=auteur_source.")
        if rec.get("same_as"):
            errors.append(f"[ATTR-d] {rec['id']}: auteur-source avec same_as non vide.")

    infos = {
        "n_quotes": len(quotes), "n_covered": n_covered, "n_unresolved": n_unresolved,
        "n_authors": len(author_ids), "n_person": len(person_ids), "n_narration": n_narration,
        "stats": bundle.get("stats", {}), "errors": errors,
    }
    return len(errors), infos


def _run(cmd) -> int:
    return subprocess.run(cmd, capture_output=True, text=True).returncode


def check_drift() -> Tuple[int, list]:
    """Correctif 4 — garde anti-recidive par regeneration complete + double passage.

    Robuste par construction : on capture l'etat COMMITTE avant tout build, puis
    on regenere integralement (build_registers -> build_attribution_edges ->
    build_registers, double passage) et on compare :
      - drift : le register/les aretes COMMITES == la regeneration fraiche ;
      - (a) idempotence : 2e regeneration byte-identique a la 1re ;
      - (b) 38 PERSON- origine=auteur_source apres le 2e build ;
      - (c) 0 cible non resolue apres le 2e build.
    Laisse l'arbre en etat regenere (corrige) si une divergence est trouvee.
    """
    errs = []
    py = sys.executable

    committed_authors = AUTHORS_MD.read_text(encoding="utf-8") if AUTHORS_MD.exists() else ""
    committed_edges = EDGES.read_text(encoding="utf-8") if EDGES.exists() else ""

    def regen():
        # GEN (ecrit le register des auteurs + les aretes) puis build_registers
        # (people.json ingere les auteurs). DOUBLE PASSAGE build_registers : un
        # 1er build avant GEN garantit que people.json reflete l'etat courant.
        _run([py, str(BUILD_REGISTERS), "--strict"])
        rc = _run([py, str(GEN)])
        _run([py, str(BUILD_REGISTERS), "--strict"])
        return rc

    rc1 = regen()
    if rc1 != 0:
        errs.append("[SSOT] build_attribution_edges a echoue (1re regeneration).")
    regen1_authors = AUTHORS_MD.read_text(encoding="utf-8") if AUTHORS_MD.exists() else ""
    regen1_edges = EDGES.read_text(encoding="utf-8") if EDGES.exists() else ""

    # drift : l'etat committe doit egaler une regeneration fraiche (SSOT)
    if committed_authors != regen1_authors:
        errs.append("[SSOT] 00_authors_canonical.md committe != regeneration deterministe "
                    "(register perime ; regenerer et committer).")
    if committed_edges != regen1_edges:
        errs.append("[SSOT] attribution_edges.json committe != regeneration deterministe.")

    # (a) idempotence : 2e regeneration identique a la 1re
    rc2 = regen()
    if rc2 != 0:
        errs.append("[SSOT] build_attribution_edges a echoue (2e regeneration).")
    regen2_authors = AUTHORS_MD.read_text(encoding="utf-8") if AUTHORS_MD.exists() else ""
    if regen2_authors != regen1_authors:
        errs.append("[SSOT-a] 00_authors_canonical.md non idempotent au 2e passage "
                    "(auteurs supprimes / oscillation 38<->0).")
    if "Total créés : 0" in regen2_authors:
        errs.append("[SSOT-a] « Total créés : 0 » parasite dans le register des auteurs.")

    # (b) 38 PERSON- origine=auteur_source presents apres le 2e build
    n_auth_md = len([r for r in parse_person_register(AUTHORS_MD) if r.get("origine") == "auteur_source"])
    if n_auth_md != 38:
        errs.append(f"[SSOT-b] {n_auth_md} auteurs-sources dans le register (attendu 38).")
    if PEOPLE_JSON.exists():
        people = json.loads(PEOPLE_JSON.read_text(encoding="utf-8"))
        n_pj = len([x for x in people if x.get("data", {}).get("origine") == "auteur_source"])
        if n_pj != 38:
            errs.append(f"[SSOT-b] {n_pj} PERSON- origine=auteur_source dans people.json (attendu 38).")

    # (c) 0 cible non resolue apres le 2e build
    _n, infos = run_gate()
    if infos.get("n_unresolved", 1) != 0:
        errs.append(f"[SSOT-c] {infos['n_unresolved']} cible(s) non resolue(s) apres le 2e build.")

    return len(errs), errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-drift", action="store_true",
                    help="Sentinelle anti-récidive : double build_registers + invariants SSOT.")
    args = ap.parse_args(argv)

    n_err, infos = run_gate()
    if "fatal" in infos:
        print(f"ERROR: {infos['fatal']}", file=sys.stderr)
        return 1

    st = infos["stats"]
    print(f"citations          : {infos['n_quotes']}")
    print(f"couvertes          : {infos['n_covered']}/{infos['n_quotes']}")
    print(f"PERSON- (registers): {infos['n_person']} (dont auteurs {infos['n_authors']})")
    print(f"cibles non résolues: {infos['n_unresolved']}")
    print(f"attribuee_a        : {st.get('attribue_a','?')} (narration {st.get('narration_reliee','?')}, "
          f"locuteur {st.get('locuteur_resolu','?')})")
    print(f"errors             : {n_err}")

    drift_errs = []
    if args.check_drift:
        n_drift, drift_errs = check_drift()
        print(f"sentinelle double-passage : {'OK' if n_drift == 0 else f'{n_drift} échec(s)'}")

    all_errs = infos["errors"] + drift_errs
    if all_errs:
        for e in all_errs[:100]:
            print(f"  - ERROR {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
