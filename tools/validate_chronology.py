#!/usr/bin/env python3
"""Validateur dédié du registre chronologique — PORTE DU GEL (étape 6).

Sortie gate-able comme ``build_registers --strict`` : exit 0 si errors == 0,
exit 1 si au moins une violation bloquante (errors), exit 2 sur échec interne.
Les *warnings* (doublons potentiels, écarts de dates) ne bloquent pas.

Invariants (cf. cahier des charges étape 6) :
  1. same_as : cible un EVENT- canonique existant ; pas de cycle ; pas de chaîne
     (legacy -> canonique direct, jamais canonique -> canonique) ; un legacy
     porte au plus un same_as.
  2. Unicité : aucun legacy membre de deux canoniques ; aucun slug EVENT-
     dupliqué ; heuristique de doublon (même date + chevauchement de label ->
     warning « doublon potentiel »).
  3. Cohérence temporelle : date_debut <= date_fin ; aucune date impossible ;
     dates des membres d'un même EVENT- non contradictoires (écart aberrant).
  4. Honnêteté de date_precision : précision déclarée <= granularité réelle de
     la date (jour => AAAA-MM-JJ complet ; annee => pas de faux mois/jour) ;
     cohérence précision vs intervalle.
  5. Catégorie : EVENT- canoniques en `jalon` ; `a_scinder_concert` =>
     `concert_a_migrer` ou jalon ; `contexte`/`reception_posthume` sans
     canonique (pas de same_as) ; `concert_migre` => same_as vers un CONCERT-.
"""
from __future__ import annotations

import glob
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CHRONO_DIR = REPO / "registers" / "chronology"
FENCE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)

PREC_RANK = {"circa": 1, "annee": 1, "saison": 1, "mois": 2, "jour": 3, "intervalle": 0}


class Diag:
    __slots__ = ("level", "code", "rid", "msg")

    def __init__(self, level, code, rid, msg):
        self.level, self.code, self.rid, self.msg = level, code, rid, msg

    def __str__(self):
        return f"[{self.level.upper():7}] {self.code} {self.rid or ''}: {self.msg}"


def load_records():
    """Return (records, canonicals). records: list of dicts with file. canonicals:
    dict id -> record for EVENT- identities."""
    records = []
    for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
        fname = Path(f).name
        for blk in FENCE.findall(Path(f).read_text(encoding="utf-8")):
            try:
                d = yaml.safe_load(blk)
            except Exception:
                continue
            if not isinstance(d, dict) or "schema" in d:
                continue
            items = []
            for k, v in d.items():
                if isinstance(v, list) and any(isinstance(x, dict) and "id" in x for x in v):
                    items += [x for x in v if isinstance(x, dict) and "id" in x]
            if not items and "id" in d and (d.get("date") or d.get("date_debut")
                                            or d.get("event") or d.get("evenement") or d.get("label")):
                items = [d]
            for it in items:
                rid = str(it.get("id", ""))
                if rid.startswith("CHR-") or rid.startswith("EVENT-"):
                    it["__file"] = fname
                    records.append(it)
    canonicals = {str(r["id"]): r for r in records if str(r["id"]).startswith("EVENT-")}
    return records, canonicals


def load_concert_ids():
    """Identités canoniques CONCERT- (registre concerts) — cibles cross-registres
    légitimes d'un `same_as` porté par une entrée chronologie concert (étape 7b-2)."""
    ids = set()
    cdir = CHRONO_DIR.parent / "concerts"
    for f in glob.glob(str(cdir / "*.md")):
        for blk in FENCE.findall(Path(f).read_text(encoding="utf-8")):
            try:
                d = yaml.safe_load(blk)
            except Exception:
                continue
            items = d if isinstance(d, list) else [d]
            for it in items:
                if isinstance(it, dict) and str(it.get("id", "")).startswith("CONCERT-"):
                    ids.add(str(it["id"]))
    return ids


def real_granularity(date_str):
    """Granularité réelle d'une chaîne de date -> rang PREC_RANK (jour/mois/annee)
    ou 'intervalle' / None (indéterminé : prose)."""
    d = str(date_str if date_str is not None else "").strip().strip('"')
    if not d:
        return None
    if re.search(r"/", d) or re.fullmatch(r"\d{4}-\d{4}", d):
        return "intervalle"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return 3  # jour
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return 2  # mois
    if re.fullmatch(r"\d{4}", d):
        return 1  # annee
    if re.match(r"^\d{1,2}\s+\w+\s+\d{4}$", d):
        return 3  # date FR complète
    return None  # prose (saison, décennie, vague) : non contraignant


def impossible_iso(date_str):
    bad = []
    for iso in re.findall(r"\d{4}-\d{2}-\d{2}", str(date_str or "")):
        y, m, dd = (int(x) for x in iso.split("-"))
        if not (1 <= m <= 12 and 1 <= dd <= 31):
            bad.append(iso)
    return bad


def year_of(s):
    m = re.search(r"\d{4}", str(s or ""))
    return int(m.group()) if m else None


def validate():
    records, canon = load_records()
    diags = []
    canon_ids = set(canon)
    concert_ids = load_concert_ids()

    # ---- Invariant 1 : same_as ------------------------------------------- #
    member_to_canon = defaultdict(list)  # member id -> [canonical ids declaring it]
    for cid, c in canon.items():
        for m in (c.get("membres_reconcilies") or []):
            member_to_canon[str(m)].append(cid)

    for r in records:
        rid = str(r["id"])
        sa = r.get("same_as")
        if sa is None:
            continue
        if isinstance(sa, list):
            if len(sa) > 1:
                diags.append(Diag("error", "INV1-multi", rid, f"plusieurs same_as : {sa}"))
            sa = sa[0] if sa else None
        if sa is None:
            continue
        sa = str(sa)
        if rid.startswith("EVENT-"):
            diags.append(Diag("error", "INV1-chain", rid, "un canonique ne doit pas porter de same_as (pas de chaîne)"))
        # Cross-registres (étape 7b-2) : une entrée chronologie « concert » peut
        # porter un same_as vers une identité CONCERT- (migration vers le registre
        # concerts), pas seulement vers un EVENT-. On valide l'existence de la
        # cible CONCERT- et on sort (les invariants membre/chaîne sont propres au
        # graphe EVENT-).
        if sa.startswith("CONCERT-"):
            if sa not in concert_ids:
                diags.append(Diag("error", "INV1-target-concert", rid, f"same_as cible un CONCERT- inexistant : {sa}"))
            continue
        if sa not in canon_ids:
            diags.append(Diag("error", "INV1-target", rid, f"same_as cible un EVENT- inexistant : {sa}"))
        elif canon[sa].get("same_as"):
            diags.append(Diag("error", "INV1-chain", rid, f"same_as pointe vers un canonique qui porte lui-même un same_as : {sa}"))

    # ---- Invariant 2 : unicité ------------------------------------------- #
    for m, cs in member_to_canon.items():
        if len(cs) > 1:
            diags.append(Diag("error", "INV2-multi-canon", m, f"membre de plusieurs canoniques : {cs}"))
    dup_slugs = [s for s, n in Counter(canon_ids).items() if n > 1]
    # (canon dict dédoublonne déjà ; détecter les doublons d'ID au parse)
    all_event_ids = [str(r["id"]) for r in records if str(r["id"]).startswith("EVENT-")]
    for s, n in Counter(all_event_ids).items():
        if n > 1:
            diags.append(Diag("error", "INV2-dup-slug", s, f"slug EVENT- dupliqué ({n} blocs)"))
    # heuristique doublon : canoniques de même date avec chevauchement de label
    STOP = {"de", "la", "le", "les", "des", "du", "à", "et", "un", "une", "joy", "division",
            "ian", "curtis", "sous", "nom", "au", "aux", "the", "of"}
    def tokens(lab):
        return {t for t in re.findall(r"[a-zA-ZÀ-ÿ]+", (lab or "").lower()) if t not in STOP and len(t) > 2}
    by_date = defaultdict(list)
    for cid, c in canon.items():
        key = str(c.get("date") or f"{c.get('date_debut')}/{c.get('date_fin')}")
        by_date[key].append(cid)
    for key, cids in by_date.items():
        for i in range(len(cids)):
            for j in range(i + 1, len(cids)):
                a, b = canon[cids[i]], canon[cids[j]]
                if len(tokens(a.get("label")) & tokens(b.get("label"))) >= 2:
                    diags.append(Diag("warning", "INV2-dup-heur", cids[i],
                                      f"doublon potentiel avec {cids[j]} (même date {key}, labels proches)"))

    # ---- Invariants 3 & 4 : temps & honnêteté ---------------------------- #
    for r in records:
        rid = str(r["id"])
        for bad in impossible_iso(r.get("date")) + impossible_iso(r.get("date_debut")) + impossible_iso(r.get("date_fin")):
            diags.append(Diag("error", "INV3-impossible", rid, f"date impossible : {bad}"))
        db, fi = r.get("date_debut"), r.get("date_fin")
        if db and fi and str(db) > str(fi):
            diags.append(Diag("error", "INV3-interval", rid, f"date_debut > date_fin : {db} > {fi}"))
        dp = str(r.get("date_precision") or "").strip()
        if dp:
            if dp == "intervalle":
                if not (db and fi):
                    diags.append(Diag("error", "INV4-interval", rid, "date_precision=intervalle sans date_debut/date_fin"))
            else:
                gran = real_granularity(r.get("date"))
                if gran == "intervalle":
                    diags.append(Diag("warning", "INV4-interval", rid, f"date en intervalle mais date_precision={dp}"))
                elif isinstance(gran, int) and dp in PREC_RANK and PREC_RANK[dp] > gran:
                    diags.append(Diag("error", "INV4-honnete", rid,
                                      f"date_precision={dp} plus précise que la date « {r.get('date')} »"))

    # dates des membres d'un canonique non contradictoires
    rec_by_id = {str(r["id"]): r for r in records}
    for cid, c in canon.items():
        cy = year_of(c.get("date") or c.get("date_debut"))
        for m in (c.get("membres_reconcilies") or []):
            mr = rec_by_id.get(str(m))
            if not mr:
                continue
            my = year_of(mr.get("date") or mr.get("date_debut"))
            if cy and my and abs(cy - my) > 1:
                diags.append(Diag("warning", "INV3-membre", cid,
                                  f"date du membre {m} ({my}) s'écarte de l'événement ({cy})"))

    # ---- Invariant 5 : catégorie ----------------------------------------- #
    for cid, c in canon.items():
        if str(c.get("categorie")) != "jalon":
            diags.append(Diag("error", "INV5-canon-cat", cid, f"canonique EVENT- doit être jalon (categorie={c.get('categorie')})"))
    for r in records:
        rid = str(r["id"])
        cat = str(r.get("categorie") or "")
        if r.get("a_scinder_concert") and cat not in ("concert_a_migrer", "jalon"):
            diags.append(Diag("warning", "INV5-scinder", rid, f"a_scinder_concert mais categorie={cat}"))
        if cat in ("contexte", "reception_posthume") and r.get("same_as"):
            diags.append(Diag("error", "INV5-cat-canon", rid, f"{cat} ne doit pas porter de same_as vers un EVENT-"))
        # concert_migre (étape 7b-2) : entrée concert réconciliée vers le registre
        # concerts -> DOIT porter un same_as vers un CONCERT-.
        if cat == "concert_migre":
            sa = str(r.get("same_as") or "")
            if not sa.startswith("CONCERT-"):
                diags.append(Diag("error", "INV5-migre", rid, "concert_migre sans same_as vers un CONCERT-"))

    return diags, len(records), len(canon)


def main():
    diags, n, nc = validate()
    errors = [d for d in diags if d.level == "error"]
    warnings = [d for d in diags if d.level == "warning"]
    by_code = Counter(d.code for d in diags)
    for d in diags:
        print(str(d), file=sys.stderr if d.level == "error" else sys.stdout)
    print("\n=== validate_chronology — synthèse ===")
    print(f"enregistrements : {n} (dont {nc} canoniques EVENT-)")
    print(f"violations par invariant : {dict(by_code)}")
    print(f"errors : {len(errors)} | warnings : {len(warnings)}")
    if errors:
        print("PORTE DU GEL : FERMÉE (errors > 0)", file=sys.stderr)
        return 1
    print("PORTE DU GEL : OUVERTE (errors = 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
