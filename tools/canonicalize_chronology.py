#!/usr/bin/env python3
"""Étape 6 — brique d'identité de la chronologie : canonicalisation EVENT-,
réconciliation same_as, classification (categorie) et précision de date
(date_precision). STRICTEMENT ADDITIF — aucun identifiant legacy n'est renommé,
aucune donnée existante n'est réécrite ; on insère des champs optionnels.

Le travail est découpé en trois phases idempotentes (commits distincts) :

  --phase classification  -> insère `categorie` sur chaque entrée (500)
  --phase canon           -> écrit registers/chronology/events_canonical.md et
                             insère `same_as: EVENT-…` sur les entrées legacy
                             des jalons réconciliés
  --phase precision       -> insère `date_precision` (+ `date_debut`/`date_fin`
                             pour les intervalles) sur chaque entrée

Conformité :
- forme canonique EVENT-<SLUG> : sémantique (l'événement, pas le lieu),
  source-agnostique, SANS date dans l'ID (NAMING_CONVENTIONS §10.2) ;
- same_as porté par le legacy, pointant vers le canonique (cross_registres §1) ;
- seuls les JALONS reçoivent un EVENT- ; les concerts ordinaires gardent leur
  ID et migreront vers CONCERT- (étape 10) ; la réception posthume est relocalisée
  en étape 11.

Le détail des règles de classification et d'inférence de précision est documenté
dans docs/audits/audit_unitaire_chronologie_12b-3.md (§ post-canonicalisation).
"""
from __future__ import annotations

import argparse
import collections
import glob
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CHRONO_DIR = REPO / "registers" / "chronology"
CANON_FILE = CHRONO_DIR / "events_canonical.md"

# --------------------------------------------------------------------------- #
# Canonical jalons (hand-curated from the audit clusters). members = legacy ids
# reconciled by same_as toward the canonical. Sex Pistols : deux gigs distincts,
# désambiguïsés par qualificateur ORDINAL sémantique (jamais par date).
# --------------------------------------------------------------------------- #
CANON = {
    "EVENT-NAISSANCE-IAN-CURTIS": dict(
        date="1956-07-15", precision="jour",
        label="Naissance de Ian Curtis",
        members=["CHR-1956-001", "CHR-S76-1956-001"]),
    "EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-PREMIER": dict(
        date="1976-06-04", precision="jour",
        label="Premier concert des Sex Pistols au Lesser Free Trade Hall",
        members=["CHR-1976-001", "CHR-S10-1976-001",
                 "CHR-S41-TL2-1976-06-04-LFTH",
                 "CHR-S41-1976-06-04-LESSER-FREE-TRADE-HALL"]),
    "EVENT-SEX-PISTOLS-LESSER-FREE-TRADE-HALL-SECOND": dict(
        date="1976-07-20", precision="jour",
        label="Second concert des Sex Pistols au Lesser Free Trade Hall",
        members=["CHR-S41-1976-07-20-SECOND-PISTOLS-LFTH",
                 "CHR-S45-1976-07-20-SEX-PISTOLS",
                 "CHR-S75-1976-002", "CHR-S76-1976-002"]),
    "EVENT-WARSAW-PREMIER-CONCERT-ELECTRIC-CIRCUS": dict(
        date="1977-05-29", precision="jour",
        label="Premier concert de Warsaw à l'Electric Circus",
        members=["CHR-S10-1977-001",
                 "CHR-S41-TL2-1977-05-29-FIRST-WARSAW-GIG-REVIEW",
                 "CHR-S41-1977-05-29-WARSAW-FIRST-GIG-ELECTRIC-CIRCUS",
                 "CHR-S45-1977-05-29-WARSAW-ELECTRIC-CIRCUS",
                 "CHR-S76-1977-003"]),
    "EVENT-PREMIER-CONCERT-JOY-DIVISION-PIPS": dict(
        date="1978-01-25", precision="jour",
        label="Premier concert sous le nom Joy Division (Pips)",
        members=["CHR-S10-1978-001",
                 "CHR-S41-1978-01-PIPS-FIRST-JOY-DIVISION-GIG",
                 "CHR-S41-TL3-1978-01-25-PIPS-JOY-DIVISION",
                 "CHR-S45-1978-01-25-PIPS-FIRST-JD",
                 "CHR-S76-1978-001"]),
    "EVENT-ARRIVEE-STEPHEN-MORRIS": dict(
        date="1977-08", precision="mois",
        label="Arrivée de Stephen Morris (batteur)",
        prudence=("S41 date l'arrivée à « 1977-08 » (mois), retenu comme date la "
                  "plus précise ; S45 ne donne que « 1977 » (année). "
                  "CHR-S35-P05-1977-ETE-001 (Morris voit l'annonce en vitrine de "
                  "Jones's) est un candidat-membre à arbitrer."),
        members=["CHR-S41-1977-08-STEVE-MORRIS-JOINS",
                 "CHR-S45-1977-STEPHEN-MORRIS-RECRUTEMENT"]),
    "EVENT-SORTIE-A-FACTORY-SAMPLE": dict(
        date="1979-01", precision="mois",
        label="Sortie de A Factory Sample (FAC 2)",
        members=["CHR-1979-001", "CHR-S41-1979-01-A-FACTORY-SAMPLE-RELEASE"]),
    "EVENT-SORTIE-UNKNOWN-PLEASURES": dict(
        date="1979-06-14", precision="jour",
        label="Sortie de l'album Unknown Pleasures (FACT 10)",
        prudence=("S41 porte deux entrées de sortie (1979-06 « critical acclaim » "
                  "et 1979-06-14 « FACT 10 release ») : duplication intra-source "
                  "réconciliée. Lecture critique de S34 conservée distincte "
                  "(reception_posthume)."),
        members=["CHR-1979-002",
                 "CHR-S41-1979-06-UP-RELEASE-CRITICAL-ACCLAIM",
                 "CHR-S41-1979-06-14-UP-FACT10-RELEASE",
                 "CHR-S75-1979-006"]),
    "EVENT-DERNIER-CONCERT-BIRMINGHAM": dict(
        date="1980-05-02", precision="jour",
        label="Dernier concert de Joy Division (Birmingham University)",
        members=["CHR-1980-002",
                 "CHR-S41-1980-05-02-BIRMINGHAM-HIGH-HALL-LAST-GIG",
                 "CHR-S45-1980-05-02-BIRMINGHAM-FINAL-GIG",
                 "CHR-S75-1980-008", "CHR-S76-1980-027"]),
    "EVENT-MORT-IAN-CURTIS": dict(
        date="1980-05-18", precision="jour",
        label="Mort de Ian Curtis",
        prudence=("Les entrées adjacentes du 16-18 mai (derniers jours, dernier "
                  "trajet, notification à Hook par la police, retour d'Annik "
                  "Honoré) sont conservées comme jalons-facettes distincts, non "
                  "fusionnés. CHR-S76-1980-031 (découverte du corps) est traité "
                  "comme la consignation S76 du décès."),
        members=["CHR-1980-003", "CHR-S41-1980-05-18-CURTIS-SUICIDE",
                 "CHR-S75-1980-009", "CHR-S76-1980-031"]),
    "EVENT-SORTIE-CLOSER": dict(
        date="1980-07-18", precision="jour",
        label="Sortie posthume de l'album Closer",
        members=["CHR-1980-004", "CHR-S41-1980-CLOSER-RELEASE-POSTHUMOUS"]),
}

# id legacy -> canonique
MEMBER_TO_CANON = {m: c for c, d in CANON.items() for m in d["members"]}

# --------------------------------------------------------------------------- #
# Classification (categorie) — règles documentées dans l'audit.
# --------------------------------------------------------------------------- #
URBAN_CONTEXT_SOURCES = {"S02", "S05", "S06", "S12", "S20"}
RECEPTION_SOURCES = {"S29", "S34"}
_milestone = re.compile(
    r"sex pistols|lesser free trade hall|premier concert|first gig|dernier concert|"
    r"last gig|avant-dernier|derni[eè]re soir|farewell|sous le nom joy division|"
    r"premier .*joy division|first .*joy division|dernier .*warsaw|last .*warsaw", re.I)
_notperf = re.compile(
    r"\b(fit|crise|overdose|van|accident|article|mentionne|presse|review|sounds|nme|"
    r"enregistre|enregistrement|session|sortie|publication|signe|signature|emprunte|"
    r"ach[eè]te|d[eé]m[eé]nage|assiste|assistent|voit|se rend)\b", re.I)
_perf = re.compile(r"\b(joue|jouent)\b|\bconcert (de|du|au|à|des|sous)\b|^concert\b", re.I)


def source_of(rid):
    m = re.match(r"CHR-(S\d+)", rid)
    return m.group(1) if m else "MASTER"


def year_of(date, rid):
    m = re.search(r"(\d{4})", date) or re.search(r"-(\d{4})", rid)
    return int(m.group(1)) if m else None


def classify(rid, date, event, certainty, types):
    """Return (categorie, flag_or_None). Members of a canonical jalon are forced
    jalon (identity overrides heuristic)."""
    if rid in MEMBER_TO_CANON:
        return "jalon", None
    src = source_of(rid)
    cert = (certainty or "").lower()
    if src in RECEPTION_SOURCES or cert.startswith("interpretation") or "source_secondaire" in cert:
        return "reception_posthume", None
    y = year_of(date, rid)
    if y and y > 1980:
        return "reception_posthume", None
    if src == "MASTER":
        return "jalon", None
    if src in URBAN_CONTEXT_SOURCES:
        return "jalon", "context_urbain"
    is_perf = ("concert" in (types or "")) or bool(_perf.search(event or ""))
    is_mile = bool(_milestone.search(event or "") or _milestone.search(rid))
    if is_perf and _notperf.search(event or ""):
        return "jalon", "perf_mixte"
    if is_perf and not is_mile:
        return "concert_a_migrer", None
    if is_perf and is_mile:
        return "jalon", "jalon_concert_significatif"
    return "jalon", None


# --------------------------------------------------------------------------- #
# Reclassements (passe d'arbitrage) — décisions validées, appliquées par
# --phase reclassify. Réécrit la valeur de `categorie` (jamais en double).
#  (a) context_urbain -> nouvelle catégorie `contexte` (dérivé du flag) ;
#  (b)/(c) basculement explicite vers concert_a_migrer, entrée par entrée.
# Les entrées NON listées ici restent dans leur catégorie courante (jalon).
# --------------------------------------------------------------------------- #
CATEGORIES = ("jalon", "concert_a_migrer", "reception_posthume", "contexte")

# (b) perf_mixte -> concert_a_migrer : gigs ordinaires (la remarque accolée
#     ne porte pas un fait marquant distinct).
PERF_TO_CONCERT = {
    "CHR-S41-1977-09-14-MIDDLESBROUGH-BOB-LAST",
    "CHR-S41-1979-08-02-YMCA-LONDON",
    "CHR-S41-1979-10-03-LEEDS-UNIVERSITY-BUZZCOCKS",
    "CHR-S41-1979-10-16-PLAN-K-BRUSSELS",
    "CHR-S45-1978-11-CHECK-INN-ALTRINCHAM",
    "CHR-S45-1980-04-02-04-MOONLIGHT-RAINBOW",
    "CHR-S76-1978-011",
    "CHR-S76-1976-003",
}
# (c) jalon_concert_significatif -> concert_a_migrer : simple proximité ordinale,
#     pas de transition de signification réelle (décisions validées).
SIG_TO_CONCERT = {
    "CHR-S41-1980-04-19-DERBY-AJANTA-ANNIK",
    "CHR-S41-1976-12-09-ELECTRIC-CIRCUS-HATE-COAT",
    "CHR-S41-1978-01-03-PIPS-AFTERGAP",
    "CHR-S41-TL2-1977-06-SQUAT-SEQUENCE",
}


def reclass_target(rid, date, event, cert, types):
    """Nouvelle catégorie si l'entrée est reclassée, sinon None (inchangée)."""
    _, flag = classify(rid, date, event, cert, types)
    if flag == "context_urbain":
        return "contexte"
    if rid in PERF_TO_CONCERT or rid in SIG_TO_CONCERT:
        return "concert_a_migrer"
    return None



# --------------------------------------------------------------------------- #
# date_precision — inférence honnête depuis la date (jamais plus précis que la
# source). Énum : {jour, mois, saison, annee, circa, intervalle}.
# --------------------------------------------------------------------------- #
_MONTHS = {"janvier", "février", "fevrier", "mars", "avril", "mai", "juin",
           "juillet", "août", "aout", "septembre", "octobre", "novembre",
           "décembre", "decembre"}
_season = re.compile(r"\b(été|ete|hiver|printemps|automne|noël|noel|summer|spring|winter|autumn|fall)\b", re.I)
_approx = re.compile(r"approx|circa|inferred|to_verify|overnight|^after_|^before_|during_|same_|around|environ|vers|fin |début |debut |milieu", re.I)


def precision(date, prec):
    """Return (date_precision, debut, fin)."""
    d = (date or "").strip().strip('"')
    p = (prec or "").strip().lower()
    # intervals (ISO or decade-as-range)
    m = (re.match(r"^(\d{4}-\d{2}-\d{2})\s*[/]\s*(\d{4}-\d{2}-\d{2})$", d)
         or re.match(r"^(\d{4}-\d{2})\s*[/]\s*(\d{4}-\d{2})$", d)
         or re.match(r"^(\d{4})[/](\d{4})$", d))
    if m:
        return "intervalle", m.group(1), m.group(2)
    m = re.match(r"^(\d{4})-(\d{4})$", d)
    if m:
        return "intervalle", m.group(1), m.group(2)
    if re.search(r"\d{4}.*[/].*\d{4}", d):
        parts = re.split(r"[/]", d)
        return "intervalle", parts[0].strip(), parts[-1].strip()
    if "range" in p or p in ("exact_range", "date_range", "month_range", "approximate_range"):
        return "intervalle", "", ""
    if _season.search(d) or p in ("saison", "season") or "spring" in p or "summer" in p or "winter" in p or "autumn" in p:
        return "saison", "", ""
    md = re.search(r"années?\s*(\d{4})", d)
    if "décennie" in p or "decade" in p or md:
        if md and re.fullmatch(r"années\s*\d{4}", d.strip()):
            y = int(md.group(1))
            return "intervalle", str(y), str(y + 9)
        return "circa", "", ""
    if re.search(r"xxe|seconde moitié|moitié", d, re.I) or "à préciser" in d.lower() or "a preciser" in d.lower():
        return "circa", "", ""
    if _approx.search(p):
        return "circa", "", ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return "jour", "", ""
    if re.fullmatch(r"\d{4}-\d{2}", d):
        return "mois", "", ""
    if re.fullmatch(r"\d{4}", d):
        return "annee", "", ""
    if re.match(r"^\d{1,2}\s+[a-zéûôA-Za-zàâ]+\s+\d{4}$", d):
        return "jour", "", ""
    if re.match(r"^[A-Za-zéûôàâ]+\s+\d{4}$", d) and d.split()[0].lower() in _MONTHS:
        return "mois", "", ""
    if re.search(r"fin |début |debut |milieu|circa|environ|vers", d, re.I):
        return "circa", "", ""
    return "circa", "", ""


# --------------------------------------------------------------------------- #
# Parse: collect every entry's id/date/precision_date/event/certainty/type.
# --------------------------------------------------------------------------- #
FENCE = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def parse_entries():
    entries = {}  # id -> dict(date, prec, event, cert, types)
    for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
        if Path(f).name == CANON_FILE.name:
            continue
        md = Path(f).read_text(encoding="utf-8")
        for blk in FENCE.findall(md):
            try:
                data = yaml.safe_load(blk)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            items = []
            for k, v in data.items():
                if isinstance(v, list) and any(isinstance(x, dict) and "id" in x for x in v):
                    items += [x for x in v if isinstance(x, dict) and "id" in x]
            if not items and "id" in data and (data.get("date") or data.get("event")
                                               or data.get("evenement") or data.get("label")):
                items = [data]
            for it in items:
                rid = str(it["id"])
                if not rid.startswith("CHR-"):
                    continue
                ev = str(it.get("event") or it.get("evenement") or it.get("label") or "").replace("\n", " ")
                t = it.get("type")
                t = "|".join(t) if isinstance(t, list) else str(t or "")
                entries[rid] = dict(
                    date=str(it.get("date", "")).strip(),
                    prec=str(it.get("precision_date", "")).strip(),
                    event=ev,
                    cert=str(it.get("certainty") or it.get("statut") or "").strip(),
                    types=t)
    return entries


# --------------------------------------------------------------------------- #
# Line-splice insertion (append-only, minimal diff, idempotent).
# --------------------------------------------------------------------------- #
ID_LINE = re.compile(r"^(\s*)(- )?id:\s*(\S+)\s*$")


def entry_span_end(lines, start):
    """Index (exclusive) where the entry starting at `start` ends: next id-line,
    closing fence, or dedent below the id's field indent."""
    field_indent = lines[start].index("id:")
    i = start + 1
    while i < len(lines):
        ln = lines[i]
        if ID_LINE.match(ln):
            break
        if ln.strip() == "```":
            break
        if ln.strip() and (len(ln) - len(ln.lstrip())) < field_indent and not ln.lstrip().startswith("- "):
            break
        i += 1
    return i


def has_field(lines, start, end, indent, key):
    pat = re.compile(r"^\s*" + re.escape(key) + r":")
    for i in range(start, end):
        if pat.match(lines[i]) and (len(lines[i]) - len(lines[i].lstrip())) == indent:
            return True
    return False


def transform_file(path, entries, phase, stats):
    lines = path.read_text(encoding="utf-8").split("\n")
    out = []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        m = ID_LINE.match(lines[i])
        if not m:
            i += 1
            continue
        rid = m.group(3).strip('"')
        if not rid.startswith("CHR-") or rid not in entries:
            i += 1
            continue
        indent = lines[i].index("id:")
        end = entry_span_end(lines, i)
        e = entries[rid]
        inserts = []
        if phase == "classification":
            cat, _ = classify(rid, e["date"], e["event"], e["cert"], e["types"])
            if not has_field(lines, i, end, indent, "categorie"):
                inserts.append(("categorie", cat))
        elif phase == "canon":
            if rid in MEMBER_TO_CANON and not has_field(lines, i, end, indent, "same_as"):
                inserts.append(("same_as", MEMBER_TO_CANON[rid]))
                stats["same_as"] += 1
        elif phase == "precision":
            dp, db, fi = precision(e["date"], e["prec"])
            if not has_field(lines, i, end, indent, "date_precision"):
                inserts.append(("date_precision", dp))
                if dp == "intervalle" and db:
                    inserts.append(("date_debut", db))
                    inserts.append(("date_fin", fi))
        for key, val in inserts:
            out.append(" " * indent + f"{key}: {val}")
        i += 1
    new = "\n".join(out)
    if new != path.read_text(encoding="utf-8"):
        path.write_text(new, encoding="utf-8")
        stats["files"] += 1


def reclassify_file(path, entries, stats):
    """Réécrit la valeur des lignes `categorie:` selon reclass_target (pas
    d'insertion : la catégorie existe déjà depuis la phase classification)."""
    lines = path.read_text(encoding="utf-8").split("\n")
    cur_id = None
    cur_indent = None
    changed = False
    cat_pat = re.compile(r"^(\s*)categorie:\s*(\S+)\s*$")
    for idx, ln in enumerate(lines):
        m = ID_LINE.match(ln)
        if m:
            cur_id = m.group(3).strip('"')
            cur_indent = ln.index("id:")
            continue
        cm = cat_pat.match(ln)
        if cm and cur_id in entries and len(cm.group(1)) == cur_indent:
            e = entries[cur_id]
            tgt = reclass_target(cur_id, e["date"], e["event"], e["cert"], e["types"])
            if tgt and tgt != cm.group(2):
                lines[idx] = " " * cur_indent + f"categorie: {tgt}"
                changed = True
                stats[tgt] += 1
    if changed:
        path.write_text("\n".join(lines), encoding="utf-8")
        stats["files"] += 1


def write_canonical_file(entries):
    lines = [
        "# Registre chronologique — identités canoniques d'événements (EVENT-)",
        "",
        "> Brique d'identité (étape 6). Chaque entrée ci-dessous est un **jalon**",
        "> canonique `EVENT-<SLUG>` : slug sémantique, source-agnostique, **sans date",
        "> dans l'ID** (la date est un champ). Les identifiants legacy `CHR-…` qui",
        "> désignent le même jalon portent `same_as: EVENT-…` dans leur fichier source",
        "> (réconciliation additive, sans renommage — cf. cross_registres.md §1).",
        "> `membres_reconcilies` liste ces legacy à titre de traçabilité.",
        "",
        "---",
        "",
    ]
    for cid, d in CANON.items():
        srcs = sorted({source_of(m) for m in d["members"]},
                      key=lambda s: (s != "MASTER", s))
        lines.append(f"## {cid} — {d['label']}")
        lines.append("")
        lines.append("```yaml")
        lines.append(f"id: {cid}")
        lines.append("type_unite: chronology_event")
        lines.append("categorie: jalon")
        lines.append(f"date: \"{d['date']}\"")
        lines.append(f"date_precision: {d['precision']}")
        lines.append(f"event: >")
        lines.append(f"  {d['label']}.")
        lines.append("sources:")
        for s in srcs:
            lines.append(f"  - {s}")
        lines.append("membres_reconcilies:")
        for mem in d["members"]:
            lines.append(f"  - {mem}")
        if d.get("prudence"):
            lines.append(f"prudence_methodologique: >")
            lines.append(f"  {d['prudence']}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    CANON_FILE.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True,
                    choices=["classification", "canon", "precision", "reclassify",
                             "report", "check"])
    args = ap.parse_args()

    entries = parse_entries()

    # Integrity: every declared canonical member must exist.
    missing = [m for m in MEMBER_TO_CANON if m not in entries]
    if missing:
        print("ERREUR : membres canoniques introuvables :", missing, file=sys.stderr)
        return 2

    stats = collections.Counter()

    if args.phase == "check":
        # Vérification de cohérence légère (pas un validateur de schéma) :
        #  1. tout same_as résout vers un EVENT- canonique existant ;
        #  2. aucune date ISO impossible ; 3. aucun intervalle inversé.
        canon = set(CANON)
        edges = impossible = inverted = 0
        problems = []
        for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
            md = Path(f).read_text(encoding="utf-8")
            for blk in FENCE.findall(md):
                try:
                    data = yaml.safe_load(blk)
                except Exception:
                    continue
                if not isinstance(data, dict):
                    continue
                items = []
                for k, v in data.items():
                    if isinstance(v, list) and any(isinstance(x, dict) and "id" in x for x in v):
                        items += [x for x in v if isinstance(x, dict) and "id" in x]
                if not items and "id" in data:
                    items = [data]
                for it in items:
                    sa = it.get("same_as")
                    if sa:
                        edges += 1
                        if str(sa) not in canon:
                            problems.append(f"same_as non résolu: {it.get('id')} -> {sa}")
                    db, fi = str(it.get("date_debut", "")), str(it.get("date_fin", ""))
                    if db and fi and db > fi:
                        inverted += 1
                        problems.append(f"intervalle inversé: {it.get('id')} {db}/{fi}")
                    for iso in re.findall(r"\d{4}-\d{2}-\d{2}", str(it.get("date", ""))):
                        _, mo, da = (int(x) for x in iso.split("-"))
                        if not (1 <= mo <= 12 and 1 <= da <= 31):
                            impossible += 1
                            problems.append(f"date impossible: {it.get('id')} {iso}")
        print(f"same_as: {edges} | impossibles: {impossible} | inversés: {inverted}")
        for p in problems:
            print("  ✗", p)
        return 1 if problems else 0

    if args.phase == "report":
        cats = collections.Counter()
        flags = collections.defaultdict(list)
        precs = collections.Counter()
        for rid, e in entries.items():
            cat, fl = classify(rid, e["date"], e["event"], e["cert"], e["types"])
            cats[cat] += 1
            if fl:
                flags[fl].append(rid)
            dp, _, _ = precision(e["date"], e["prec"])
            precs[dp] += 1
        print("entrées            :", len(entries))
        print("categorie          :", dict(cats))
        print("date_precision     :", dict(precs))
        print("canoniques EVENT-  :", len(CANON))
        print("arêtes same_as     :", len(MEMBER_TO_CANON))
        print("flags (à arbitrer) :", {k: len(v) for k, v in flags.items()})
        for k, v in flags.items():
            print(f"\n--- flag: {k} ({len(v)}) ---")
            for rid in sorted(v):
                print("   ", rid)
        return 0

    if args.phase == "canon":
        write_canonical_file(entries)
        print(f"écrit {CANON_FILE.relative_to(REPO)} ({len(CANON)} EVENT-)")

    for f in sorted(glob.glob(str(CHRONO_DIR / "*.md"))):
        p = Path(f)
        if p.name == CANON_FILE.name:
            continue
        if args.phase == "reclassify":
            reclassify_file(p, entries, stats)
        else:
            transform_file(p, entries, args.phase, stats)

    if args.phase == "reclassify":
        moved = {k: stats[k] for k in CATEGORIES if stats[k]}
        print(f"phase reclassify : {stats['files']} fichier(s), reclassements -> {moved}")
    else:
        print(f"phase {args.phase} : {stats['files']} fichier(s) modifié(s)"
              + (f", {stats['same_as']} same_as" if args.phase == "canon" else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
