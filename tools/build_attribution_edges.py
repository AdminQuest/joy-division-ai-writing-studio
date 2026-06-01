#!/usr/bin/env python3
"""Cablage des attributions de citations vers PERSON- (etape 9, suite).

SSOT : unique normalisation des aretes d'attribution citation -> PERSON-,
conforme a docs/specs/cross_registres.md (XR-1..7). Lit :

  - registre canonique  registers/people/00_canonical_people.md (#47, via
    exports/generated/people.json) -- resolution nom + alt_names + same_as ;
  - attributions des 962 citations exports/generated/quotes.json
    (locuteur, auteur_source, rapporteur, attribution_a_arbitrer) ;
  - verite-terrain source->auteur data/registre.json (pour confirmer et creer
    additivement les PERSON- auteurs-sources manquants).

Emet, de facon DETERMINISTE :

  - registers/relations/attribution_edges.json : aretes typees par citation
    (attribue_a n->1 ; auteur_source, rapporteur n->m) + flags
    (attribution_non_personne, a_resoudre). NB : la cle JSON publique du role
    locuteur est `attribue_a` (= XR `attribué_à`, ecrite avec l'accent) ;
  - registers/people/00_authors_canonical.md : bloc DELIMITE des PERSON-
    auteurs-sources crees additivement (categorie=auteur_secondaire,
    origine=auteur_source, same_as=[]) -- ingere comme person par le build ;
  - met a jour registers/people/pending_org.json (HM Treasury, Happy Mondays,
    Manchester Digital Music Archive) ;
  - exports/generated/attribution_edges.json (copie fetchee par le graphe).

Gel additif : les 166 PERSON- de #47 ne sont NI renommes NI fusionnes ; on
n'AJOUTE que des PERSON- auteurs-sources. Les id PERS-* restent intacts.

Usage :
    python3 tools/build_attribution_edges.py            # ecrit les livrables
    python3 tools/build_attribution_edges.py --stats    # stats JSON sur stdout
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
PEOPLE_JSON = ROOT / "exports" / "generated" / "people.json"
QUOTES_JSON = ROOT / "exports" / "generated" / "quotes.json"
REGISTRE = ROOT / "data" / "registre.json"
OUT_EDGES = ROOT / "registers" / "relations" / "attribution_edges.json"
OUT_EXPORT = ROOT / "exports" / "generated" / "attribution_edges.json"
OUT_AUTHORS = ROOT / "registers" / "people" / "00_authors_canonical.md"
PENDING_ORG = ROOT / "registers" / "people" / "pending_org.json"

# Cle publique XR pour le role `locuteur` (ecrite avec l'accent dans le JSON).
ATTR_KEY = "attribué_à"  # "attribué_à"

ANON = {"anonyme", "", "narration", "narrateur"}

# Résolutions de rapporteur arbitrées explicitement (audit §6). Le champ brut
# « entretien McCullough » est ambigu par chaîne seule (Dave vs Paul McCullough),
# mais l'audit tranche : interview Dave McCullough rapportée par Middles & Reade.
# Override traçable, limité aux citations arbitrées — jamais une heuristique large.
ARBITRAGE_RAPPORTEUR = {
    "S76-Q116": ["Dave McCullough", "Mick Middles", "Lindsay Reade"],
}

# Entites NON-personnes en attribution -> hand-off ORG- (etape 10). Jamais
# creees en PERSON- (XR-6). Cle = forme normalisee.
NON_PERSON = {
    "hm treasury": "HM Treasury",
    "happy mondays": "Happy Mondays",
    "manchester digital music archive": "Manchester Digital Music Archive",
    "the times": "The Times",
}
# Fragments d'attribution non exploitables -> a_resoudre, jamais crees.
JUNK = {
    "auteurs multiples", "propos rapportes dans la presse",
    "commentaire rapporte par la presse", "cite par les editeurs",
    "description officielle du produit", "editeurs", "dir",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def split_components(s: str) -> List[str]:
    """Eclate « A ; B » (separateur fiable), puis « A, B » SEULEMENT quand chaque
    fragment a >= 2 mots (vraie liste de co-auteurs), pour ne pas casser
    « Nom, Prenom » / « Adorno, Theodor W. »."""
    s = re.sub(r"\(dir\.?\)", "", s or "").strip()
    out: List[str] = []
    for part in re.split(r";", s):
        part = part.strip()
        if not part:
            continue
        if "," in part:
            frags = [f.strip() for f in part.split(",") if f.strip()]
            if frags and all(len(f.split()) >= 2 for f in frags):
                out.extend(frags)
            else:
                out.append(part)
        else:
            out.append(part)
    return out


def load_canonical_index() -> Tuple[Dict[str, str], set]:
    raw = json.loads(PEOPLE_JSON.read_text(encoding="utf-8"))
    idx: Dict[str, str] = {}
    person_ids = set()
    for rec in raw:
        pid = rec.get("id", "")
        if not str(pid).startswith("PERSON-"):
            continue
        person_ids.add(pid)
        d = rec.get("data", {})
        idx.setdefault(norm(d.get("name", "")), pid)
        for a in d.get("alt_names", []) or []:
            idx.setdefault(norm(a), pid)
    return idx, person_ids


def source_authors_map() -> Dict[str, List[str]]:
    reg = json.loads(REGISTRE.read_text(encoding="utf-8"))
    out: Dict[str, List[str]] = {}
    for e in reg:
        if isinstance(e, dict) and e.get("id"):
            out[e["id"]] = split_components(e.get("auteur", ""))
    return out


def build_creation_list(quotes, idx, src_auth):
    """to_create : norm -> {name, slug, id, sources:set} pour auteurs publies
    non resolus, confirmes comme auteurs d'une source (registre.json)."""
    attested: Dict[str, Any] = {}
    for sid, comps in src_auth.items():
        for c in comps:
            attested.setdefault(norm(c), [c, set()])[1].add(sid)

    to_create: Dict[str, Dict[str, Any]] = {}
    non_person_seen: set = set()

    def consider(component: str):
        n = norm(component)
        if not n or n in idx or n in JUNK:
            return
        if n in NON_PERSON:
            non_person_seen.add(n)
            return
        if n in attested:
            disp = attested[n][0]
            slug = slugify(disp)
            entry = to_create.setdefault(n, {
                "name": disp, "slug": slug, "id": "PERSON-" + slug, "sources": set()})
            entry["sources"] |= attested[n][1]

    for r in quotes:
        d = r["data"]
        for c in split_components(d.get("auteur_source", "")):
            consider(c)
        loc = (d.get("locuteur") or "").strip()
        if norm(loc) not in ANON:
            for c in split_components(loc):
                consider(c)
        for c in split_components(d.get("rapporteur", "")):
            consider(c)
    return to_create, non_person_seen


def resolve_one(component: str, idx: Dict[str, str]) -> Optional[str]:
    return idx.get(norm(component))


def build_edges(quotes, idx):
    edges = []
    stats: Dict[str, int] = defaultdict(int)
    a_resoudre_rows: List[Dict[str, str]] = []
    non_person_rows: List[Dict[str, str]] = []

    for r in quotes:
        d = r["data"]
        cid = r["id"]
        sid = d.get("source_id", "") or ""
        attribue_a: Optional[str] = None
        auteurs: List[str] = []
        rapporteurs: List[str] = []
        flags: List[str] = []

        loc = (d.get("locuteur") or "").strip()
        auteur = d.get("auteur_source") or ""
        rapp = d.get("rapporteur") or ""

        # auteur_source (n->m)
        for c in split_components(auteur):
            pid = resolve_one(c, idx)
            if pid:
                if pid not in auteurs:
                    auteurs.append(pid)
            elif norm(c) in NON_PERSON:
                flags.append("attribution_non_personne")
                non_person_rows.append({"citation": cid, "name": NON_PERSON[norm(c)], "role": "auteur_source"})
            elif c.strip():
                flags.append("a_resoudre")
                a_resoudre_rows.append({"citation": cid, "value": c, "role": "auteur_source"})

        # rapporteur (n->m). Override d'arbitrage explicite si présent (audit §6).
        rapp_components = ARBITRAGE_RAPPORTEUR.get(cid) or split_components(rapp)
        for c in rapp_components:
            pid = resolve_one(c, idx)
            if pid:
                if pid not in rapporteurs:
                    rapporteurs.append(pid)
            elif norm(c) in NON_PERSON:
                flags.append("attribution_non_personne")
                non_person_rows.append({"citation": cid, "name": NON_PERSON[norm(c)], "role": "rapporteur"})
            elif c.strip():
                flags.append("a_resoudre")
                a_resoudre_rows.append({"citation": cid, "value": c, "role": "rapporteur"})

        # attribue_a (n->1)
        if norm(loc) in ANON:
            # Narration d'auteur (cas 5a) : attribue_a = PERSON- du 1er auteur_source.
            if auteurs:
                attribue_a = auteurs[0]
                stats["narration_reliee"] += 1
        else:
            comps = split_components(loc)
            pid = resolve_one(loc, idx)
            if not pid and comps:
                pid = resolve_one(comps[0], idx)
            if pid:
                attribue_a = pid
                stats["locuteur_resolu"] += 1
            elif norm(loc) in NON_PERSON:
                flags.append("attribution_non_personne")
                non_person_rows.append({"citation": cid, "name": NON_PERSON[norm(loc)], "role": "locuteur"})
            else:
                flags.append("a_resoudre")
                a_resoudre_rows.append({"citation": cid, "value": loc, "role": "locuteur"})

        flags = sorted(set(flags))
        # Arêtes typées au format XR (docs/specs/cross_registres.md §3.1) : portées
        # par l'entité contingente (la citation) vers le nœud PERSON-. Prédicats du
        # vocabulaire contrôlé §4 : `attribuee_a` (0..1, noyau), `a_pour_auteur_source`
        # (0..n, extension §4.3), `rapportee_par` (0..n, extension §4.3).
        liens = []
        if attribue_a:
            liens.append({"predicat": "attribuee_a", "cible": attribue_a})
        for pid in auteurs:
            liens.append({"predicat": "a_pour_auteur_source", "cible": pid})
        for pid in rapporteurs:
            liens.append({"predicat": "rapportee_par", "cible": pid})
        rec = {
            "citation": cid,
            "source_id": sid,
            "liens": liens,
            # vues plates (commodité de lecture, dérivées des liens ci-dessus) :
            "attribuee_a": attribue_a,
            "auteur_source": auteurs,
            "rapporteur": rapporteurs,
            "flags": flags,
        }
        if cid == "S76-Q116":
            rec["arbitrage_resolu"] = True  # parole rapportee de Ian Curtis (audit Sec.6)
        edges.append(rec)

        if attribue_a:
            stats["attribue_a"] += 1
        stats["auteur_source_edges"] += len(auteurs)
        stats["rapporteur_edges"] += len(rapporteurs)
        if "a_resoudre" in flags:
            stats["citations_a_resoudre"] += 1
        if "attribution_non_personne" in flags:
            stats["citations_non_personne"] += 1

    return edges, dict(stats), a_resoudre_rows, non_person_rows


def _q(s: str) -> str:
    s = str(s)
    if re.search(r'[:#"\'\[\]{}]|^\s|\s$', s) or s == "":
        return '"' + s.replace('"', '\\"') + '"'
    return s


def render_authors_md(to_create: Dict[str, Dict[str, Any]]) -> str:
    recs = sorted(to_create.values(), key=lambda x: x["id"])
    L: List[str] = []
    L.append("# Registre canonique des acteurs — `PERSON-` auteurs-sources (création additive)")
    L.append("")
    L.append("> **Étape 9 (câblage).** `PERSON-` créés additivement pour les "
             "auteurs-sources non couverts par la couche `PERS-*`. Identité née de "
             "l'attribution : `categorie=auteur_secondaire`, `origine=auteur_source`, "
             "`same_as=[]` (aucun backing `PERS-*` — autorisé par le validateur).")
    L.append("> **GÉNÉRÉ** par `tools/build_attribution_edges.py`. Ne pas éditer à la main.")
    L.append("> **Gel additif** : n'ajoute QUE de nouveaux `PERSON-` ; les 166 de #47 "
             "et les id `PERS-*` restent intacts.")
    L.append("")
    L.append(f"Total créés : **{len(recs)}**.")
    L.append("")
    for r in recs:
        L.append(f"## {r['id']} — {r['name']}")
        L.append("")
        L.append("```yaml")
        L.append(f"id: {r['id']}")
        L.append("type_unite: person")
        L.append(f"name: {_q(r['name'])}")
        L.append("categorie: auteur_secondaire")
        L.append("origine: auteur_source")
        L.append("role:")
        L.append("  - auteur")
        L.append("sources:")
        for s in sorted(r["sources"]):
            L.append(f"  - {s}")
        L.append("same_as: []")
        L.append("alt_names: []")
        L.append("categorie_a_arbitrer: false")
        L.append("a_arbitrer: false")
        L.append("```")
        L.append("")
    return "\n".join(L) + "\n"


def update_pending_org(non_person_seen: set) -> int:
    payload = json.loads(PENDING_ORG.read_text(encoding="utf-8"))
    existing = {it.get("name") for it in payload.get("items", [])}
    added = 0
    for n in sorted(non_person_seen):
        name = NON_PERSON.get(n, n)
        if name in existing:
            continue
        payload["items"].append({
            "from_attribution": True, "name": name, "target_kind": "ORG-",
            "note": "Attribution non-personne (institution/groupe/archive) reperee "
                    "au cablage etape 9 ; cablage des aretes reporte a l'etape 10.",
        })
        added += 1
    payload["items"].sort(key=lambda x: (str(x.get("from_pers", "")), str(x.get("name", ""))))
    PENDING_ORG.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added


def compute(argv_stats: bool = False):
    idx, _person_ids = load_canonical_index()
    quotes = json.loads(QUOTES_JSON.read_text(encoding="utf-8"))
    src_auth = source_authors_map()

    to_create, non_person_seen = build_creation_list(quotes, idx, src_auth)
    for n, info in to_create.items():
        idx.setdefault(n, info["id"])

    edges, stats, a_resoudre_rows, non_person_rows = build_edges(quotes, idx)

    n_quotes = len(quotes)
    covered = sum(1 for e in edges
                  if e["liens"]
                  or "attribution_non_personne" in e["flags"] or "a_resoudre" in e["flags"])
    stats_out = {
        "n_quotes": n_quotes,
        "person_created": len(to_create),
        "non_person_routed": len(non_person_seen),
        "attribue_a": stats.get("attribue_a", 0),
        "narration_reliee": stats.get("narration_reliee", 0),
        "locuteur_resolu": stats.get("locuteur_resolu", 0),
        "auteur_source_edges": stats.get("auteur_source_edges", 0),
        "rapporteur_edges": stats.get("rapporteur_edges", 0),
        "citations_a_resoudre": stats.get("citations_a_resoudre", 0),
        "citations_non_personne": stats.get("citations_non_personne", 0),
        "citations_couvertes": covered,
        "taux_couverture": round(covered / n_quotes, 4) if n_quotes else 0,
        "created_list": sorted(info["id"] for info in to_create.values()),
        "a_resoudre_distinct": sorted({row["value"] for row in a_resoudre_rows}),
        "non_person_distinct": sorted({NON_PERSON.get(n, n) for n in non_person_seen}),
    }
    return dict(idx=idx, quotes=quotes, to_create=to_create, non_person_seen=non_person_seen,
                edges=edges, stats_out=stats_out,
                a_resoudre_rows=a_resoudre_rows, non_person_rows=non_person_rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args(argv)

    r = compute()
    stats_out = r["stats_out"]

    if args.stats:
        print(json.dumps(stats_out, ensure_ascii=False, indent=1))
        return 0

    OUT_EDGES.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "_comment": "Aretes d'attribution citation->PERSON- (etape 9, XR-1..7). "
                    "GENERE par tools/build_attribution_edges.py -- SSOT.",
        "spec": "docs/specs/cross_registres.md",
        "stats": stats_out,
        "edges": r["edges"],
        "a_resoudre": r["a_resoudre_rows"],
        "attribution_non_personne": r["non_person_rows"],
    }
    text = json.dumps(bundle, ensure_ascii=False, indent=1) + "\n"
    OUT_EDGES.write_text(text, encoding="utf-8")
    OUT_EXPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_EXPORT.write_text(text, encoding="utf-8")
    OUT_AUTHORS.write_text(render_authors_md(r["to_create"]), encoding="utf-8")
    added_org = update_pending_org(r["non_person_seen"])

    # journal compact (ASCII) -> evite le bug d'affichage non-ASCII de l'env.
    print("person_created=%d" % stats_out["person_created"])
    print("non_person_routed=%d pending_org_added=%d" % (stats_out["non_person_routed"], added_org))
    print("attribue_a=%d narration=%d locuteur=%d" % (
        stats_out["attribue_a"], stats_out["narration_reliee"], stats_out["locuteur_resolu"]))
    print("auteur_source_edges=%d rapporteur_edges=%d" % (
        stats_out["auteur_source_edges"], stats_out["rapporteur_edges"]))
    print("a_resoudre=%d non_personne=%d" % (
        stats_out["citations_a_resoudre"], stats_out["citations_non_personne"]))
    print("couverture=%d/%d=%.4f" % (
        stats_out["citations_couvertes"], stats_out["n_quotes"], stats_out["taux_couverture"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
