#!/usr/bin/env python3
"""Build the canonical `PERSON-` register (étape 9 — canonicalisation).

SSOT : ce script est l'UNIQUE normalisation. Il lit la couche provisoire agrégée
``exports/generated/people.json`` (préfixes ``PERS-*``), applique l'arbitrage
figé (grappes ``same_as``, décisions §2–§4, typage §5, cas sensibles §6) et
émet de façon DÉTERMINISTE :

  - ``registers/people/00_canonical_people.md`` : enregistrements d'identité
    ``PERSON-<slug>`` (blocs YAML ingérés par build_registers comme ``person``) ;
  - ``registers/people/pending_org.json``     : renvois hand-off vers ``ORG-`` ;
  - ``registers/people/pending_concept.json`` : renvois hand-off vers concept.

Gel additif : aucun ``PERS-*`` n'est renommé ni supprimé. Chaque ``PERS-*``
devient un alias résolu, porté en ``same_as`` par l'enregistrement canonique.
La couche provisoire (registers/people/*.md, people.json) persiste telle quelle.

Le validateur (``tools/validate_people.py``) et la sentinelle anti-drift
rejouent CE script et comparent : toute divergence substantielle échoue.

Usage :
    python3 tools/build_people_canon.py            # écrit les livrables
    python3 tools/build_people_canon.py --emit      # idem (explicite)
    python3 tools/build_people_canon.py --to-stdout # n'écrit rien, imprime le .md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
PEOPLE_JSON = ROOT / "exports" / "generated" / "people.json"
OUT_MD = ROOT / "registers" / "people" / "00_canonical_people.md"
OUT_ORG = ROOT / "registers" / "people" / "pending_org.json"
OUT_CONCEPT = ROOT / "registers" / "people" / "pending_concept.json"

CATEGORIES = {
    "membre", "entourage", "industrie", "critique_journaliste",
    "auteur_secondaire", "influence", "theoricien_mobilise",
}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s)).strip()


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def display_name(data: Dict[str, Any]) -> str:
    for k in ("name", "nom", "personne", "full_name"):
        if data.get(k):
            return str(data[k]).strip()
    return ""


def role_text(data: Dict[str, Any]) -> str:
    r = data.get("role") or data.get("type_unite") or data.get("statut") or ""
    if isinstance(r, list):
        r = "; ".join(str(x) for x in r)
    return str(r)


# --------------------------------------------------------------------------- #
# Arbitrage figé (cf. docs/audits/etape9_personnes_audit.md §2–§6 + consigne)
# --------------------------------------------------------------------------- #
# Fusions inter-clusters manquées par la détection automatique : on rattache
# l'id de gauche au cluster (clé = nom normalisé canonique) de droite.
FORCED_MEMBERSHIP = {
    "PERS-010": "annik honore",                       # Annick → Annik Honoré (§3)
    "PERS-S29-008": "franco berardi bifo",            # Franco Berardi → Bifo (§3)
    "PERS-S21-003": "andy zero andy waide",           # Andy Zero → Andy Waide (§3)
    "PERS-S76-009": "deborah curtis",                 # Deborah Woodruff → D. Curtis (§3)
    "PERS-S76-021": "stephen morris",                 # Steve Morris → Stephen Morris (§2)
    "PERS-S75-025": "tony davidson t j davidson",     # T.J. ↔ Tony Davidson (§2)
}

# Cas sensibles : ids tenus DISTINCTS de toute autre grappe (jamais fusionnés).
KEEP_DISTINCT = {"PERS-S76-003"}  # Kevin Curtis (père) ≠ Ian Kevin Curtis (§6)

# alt_names ajoutés (formes secondaires : variantes, noms de scène, naissance).
# Clé = nom normalisé du cluster cible.
EXTRA_ALT_NAMES = {
    "bernard sumner": ["Bernard Albrecht", "Bernard Dicken"],  # noms de scène (§6)
    "annik honore": ["Annick Honoré"],
    "franco berardi bifo": ["Franco Berardi", "Bifo"],
    "andy zero andy waide": ["Andy Waide"],
    "deborah curtis": ["Deborah Woodruff"],
    "stephen morris": ["Steve Morris"],
    "tony davidson t j davidson": ["Tony Davidson", "T. J. Davidson"],
    "eddie garrity ed banger": ["Ed Banger"],
}

# Nom canonique imposé (forme civile la plus complète ET usuelle) — sinon dérivé.
FORCED_CANON_NAME = {
    "annik honore": "Annik Honoré",
    "franco berardi bifo": "Franco Berardi",
    "andy zero andy waide": "Andy Zero",
    "deborah curtis": "Deborah Curtis",
    "stephen morris": "Stephen Morris",
    "tony davidson t j davidson": "Tony Davidson",
    "eddie garrity ed banger": "Eddie Garrity",
    "ian curtis": "Ian Curtis",
    "kevin curtis": "Kevin Curtis",
    "william s burroughs": "William S. Burroughs",
}

# Hand-offs : entités NON-personnes présentes dans la couche PERS-*.
PENDING_ORG = {
    "PERS-016": "Bedhead",
    "PERS-S76-068": "Buzzcocks",
    "PERS-S76-071": "Minny Pops",
    # « Oz PA » issu de l'éclatement de PERS-S76-052 (§4).
}
PENDING_CONCEPT = {
    "PERS-S76-082": "Perry Boys",  # sous-culture juvénile (ni ORG- ni PERSON-)
}

# Éclatements d'entrées mixtes (§4) : un id provisoire → plusieurs cibles.
#   PERS-S76-052 « Oz PA / Eddy et Oz » : Oz PA → ORG- ; Eddy, Oz → 2 PERSON- a_arbitrer.
#   PERS-S76-064 « Dave Pils et Jasmine » : Dave Pils → same_as de PERS-S76-077 ;
#                                            Jasmine → PERSON- neuf a_arbitrer.
SPLIT_NEW_PERSONS = [
    # (slug, name, categorie, same_as_ids, a_arbitrer, note)
    ("PERSON-eddy-oz-pa", "Eddy", "industrie", [], True,
     "Composante individuelle de PERS-S76-052 « Oz PA / Eddy et Oz » ; nom incomplet, contrôle S76 requis."),
    ("PERSON-oz-oz-pa", "Oz", "industrie", [], True,
     "Composante individuelle de PERS-S76-052 « Oz PA / Eddy et Oz » ; nom incomplet, contrôle S76 requis."),
    ("PERSON-jasmine", "Jasmine", "entourage", [], True,
     "Composante individuelle de PERS-S76-064 « Dave Pils et Jasmine » ; nom incomplet, contrôle S76 requis."),
]
ADDITIONAL_CANONICAL_PERSONS = [
    {
        "id": "PERSON-pennie-smith",
        "type_unite": "person",
        "name": "Pennie Smith",
        "categorie": "industrie",
        "role": ["photographe"],
        "sources": ["IMAGE-I-0004"],
        "same_as": [],
        "alt_names": [],
        "categorie_a_arbitrer": False,
        "a_arbitrer": False,
        "note": "Identite ajoutee depuis le registre iconographique pour une photographie attribuee a Pennie Smith ; aucun PERS-* source existant au moment de l'ajout.",
    }
]
# Dave Pils (composante de PERS-S76-064) est rabattu sur le PERSON- de PERS-S76-077.
DAVE_PILS_HOST_ID = "PERS-S76-077"

# Ids dont le rattachement reste incertain → categorie marquée mais a_arbitrer.
# Stephanie (PERS-S45-STEPHANIE-MORRIS) : compagne de Stephen Morris, personne
# réelle distincte (PAS un artefact de segmentation de « Stephen Morris ») mais
# au nom incomplet → PERSON- propre, a_arbitrer (§3).
A_ARBITRER_IDS = {"PERS-S45-STEPHANIE-MORRIS"}

# --------------------------------------------------------------------------- #
# Typage (§5). Priorité absolue aux classes non-actrices.
# --------------------------------------------------------------------------- #
CAT_INFLUENCE = {
    "william s burroughs", "j g ballard", "marcel proust", "nikolai gogol",
    "friedrich nietzsche", "arthur schopenhauer", "maurice blanchot",
    "brion gysin", "daniel odier",                 # cercle littéraire Burroughs
    "david bowie", "david byrne",                  # figures artistiques admirées
}
CAT_THEORICIEN = {
    "jacques derrida", "henri lefebvre", "georg simmel", "david harvey",
    "marshall berman", "henri bergson", "georg wilhelm friedrich hegel",
    "mark fisher", "franco berardi bifo", "franco berardi", "bifo",
    "christian norberg-schulz",
    "greil marcus", "aby warburg", "hito steyerl", "jacques attali",
    "jane jacobs",
}
# membres du groupe (noyau JD).
CAT_MEMBRE = {"ian curtis", "bernard sumner", "peter hook", "stephen morris"}

# Mots-clés de rôle pour les classes actrices (fallback déterministe).
ROLE_INDUSTRIE = re.compile(
    r"producteur|ingénieur|ingenieur|manager|label|design|graphiste|"
    r"\bdj\b|promoteur|rca|grapevine|factory|sonorisation|roadie|"
    r"directeur|a&r|exécutif|executif|investisseur|réalisateur|realisateur|"
    r"filmeur|opérateur|operateur|photographe|sono|studio", re.I)
ROLE_CRITIQUE = re.compile(
    r"\b(journaliste|critique|presse|nme|sounds|fanzine|zine|chroniqueur|"
    r"animateur radio|essayiste|biographe)\b", re.I)
ROLE_ENTOURAGE = re.compile(
    r"\b(proche|épouse|epouse|conjoint|compagne|compagnon|père|pere|mère|mere|"
    r"fille|fils|sœur|soeur|frère|frere|tante|oncle|parent|ami|amie|enfant|"
    r"voisin|voisine|fan|témoin familial|temoin familial|relation intime|"
    r"chien|animal)\b", re.I)


def categorise(canon_name_norm: str, role_blob: str, is_source_author: bool) -> Tuple[str, bool]:
    """Retourne (categorie, categorie_a_arbitrer).

    Priorité (politique §5) : classes non-actrices d'abord (influence,
    theoricien_mobilise, membre, auteur_secondaire), puis classes actrices du
    réseau JD. Parmi celles-ci, le rôle professionnel l'emporte sur le lien de
    parenté/amitié (un manager est `industrie`, pas `entourage`) ; une double
    appartenance (professionnel ET proche, ou critique ET industrie) lève
    `categorie_a_arbitrer`.
    """
    if canon_name_norm in CAT_INFLUENCE:
        return "influence", False
    if canon_name_norm in CAT_THEORICIEN:
        return "theoricien_mobilise", False
    if canon_name_norm in CAT_MEMBRE:
        return "membre", False
    rb = role_blob.lower()
    is_author_role = bool(re.search(r"auteur de s|autrice de s|co-auteur|co-autrice|"
                                    r"auteur du chapitre|chercheur|universit", rb))
    if is_source_author or is_author_role:
        # double appartenance critique/journaliste fréquente (Reynolds, Savage, Morley…)
        return "auteur_secondaire", bool(ROLE_CRITIQUE.search(rb))

    has_ind = bool(ROLE_INDUSTRIE.search(rb))
    has_crit = bool(ROLE_CRITIQUE.search(rb))
    has_ent = bool(ROLE_ENTOURAGE.search(rb))

    if has_ind:
        # professionnel de la musique/industrie ; flag si aussi proche ou critique.
        return "industrie", (has_ent or has_crit)
    if has_crit:
        return "critique_journaliste", has_ent
    if has_ent:
        return "entourage", False
    # défaut prudent : entourage du réseau JD, marqué à arbitrer.
    return "entourage", True


# --------------------------------------------------------------------------- #
# Construction
# --------------------------------------------------------------------------- #
def load_people() -> List[Dict[str, Any]]:
    raw = json.loads(PEOPLE_JSON.read_text(encoding="utf-8"))
    seen = set()
    rows = []
    for rec in raw:
        d = rec.get("data", {})
        pid = d.get("id", rec.get("id"))
        # N'ingérer QUE la couche provisoire PERS-* : ignorer nos propres
        # identités canoniques PERSON- (présentes dans people.json après un
        # build), sinon le générateur se nourrirait de sa propre sortie.
        if not str(pid).startswith("PERS-") or str(pid).startswith("PERSON-"):
            continue
        name = display_name(d)
        key = (pid, norm(name))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"id": pid, "name": name, "nn": norm(name),
                     "role": role_text(d), "data": d})
    return rows


def source_author_names(rows: List[Dict[str, Any]]) -> set:
    """Noms (normalisés) reconnus comme auteurs de sources du corpus.

    Dérivé de quotes.json (auteur_source) + rôle « Auteur de S… » ; sert à
    classer en `auteur_secondaire`.
    """
    names = set()
    q_path = ROOT / "exports" / "generated" / "quotes.json"
    if q_path.exists():
        for r in json.loads(q_path.read_text(encoding="utf-8")):
            a = (r.get("data", {}).get("auteur_source") or "").strip()
            # un auteur_source peut être composite (« A ; B » / « A, B ») : on
            # éclate sur ; et on garde chaque composante normalisée.
            for part in re.split(r"[;]", a):
                part = re.sub(r"\(dir\.\)", "", part).strip()
                if part:
                    names.add(norm(part))
    return names


def build_clusters(rows: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    clusters: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    # ids retirés du flux PERSON- (hand-offs + éclatements mixtes)
    excluded = set(PENDING_ORG) | set(PENDING_CONCEPT) | {"PERS-S76-052", "PERS-S76-064"}
    for r in rows:
        pid = r["id"]
        if pid in excluded:
            continue
        if pid in KEEP_DISTINCT:
            clusters[norm(r["name"])].append(r)  # cluster propre (Kevin Curtis)
            continue
        target = FORCED_MEMBERSHIP.get(pid, r["nn"])
        clusters[target].append(r)
    return clusters


def pick_canon_name(key: str, members: List[Dict[str, Any]]) -> str:
    if key in FORCED_CANON_NAME:
        return FORCED_CANON_NAME[key]
    # nom le plus complet et usuel : on écarte les formes mixtes « A / B » et on
    # prend, à longueur égale, le nom porté par l'id global le plus prioritaire.
    def score(m):
        nm = m["name"]
        mixed = " / " in nm or " et " in nm.lower()
        glob = bool(re.fullmatch(r"PERS-\d+", m["id"]))
        return (0 if mixed else 1, 1 if glob else 0, len(nm))
    best = sorted(members, key=score, reverse=True)[0]
    return best["name"].split(" / ")[0].strip()


def collect_alt_names(key: str, canon_name: str, members: List[Dict[str, Any]]) -> List[str]:
    alts: List[str] = []
    def add(x: str):
        x = (x or "").strip()
        if x and x != canon_name and x not in alts:
            alts.append(x)
    for m in members:
        # nom affiché s'il diffère du canonique. Une forme mixte « A / B » n'est
        # pas un alias en soi : on n'ajoute QUE ses composantes, pas la chaîne
        # combinée (qui n'est le nom de personne ni de A ni de B).
        if " / " in m["name"]:
            for part in m["name"].split(" / "):
                add(part.strip())
        else:
            add(m["name"])
        # full_name / alias portés par l'enregistrement provisoire
        d = m["data"]
        add(d.get("full_name", ""))
        al = d.get("aliases") or d.get("alias") or []
        if isinstance(al, str):
            al = [al]
        for a in al:
            add(a)
    for a in EXTRA_ALT_NAMES.get(key, []):
        add(a)
    return alts


def build_records(rows: List[Dict[str, Any]]):
    clusters = build_clusters(rows)
    src_authors = source_author_names(rows)
    records = []
    a_arbitrer_count = 0

    for key in sorted(clusters):
        members = clusters[key]
        canon_name = pick_canon_name(key, members)
        slug = slugify(canon_name)
        pid_slug = f"PERSON-{slug}"
        same_as = sorted({m["id"] for m in members})
        alt_names = collect_alt_names(key, canon_name, members)
        role_blob = " ; ".join(m["role"] for m in members if m["role"])
        is_src_author = norm(canon_name) in src_authors
        categorie, cat_arb = categorise(norm(canon_name), role_blob, is_src_author)

        a_arb = any(m["id"] in A_ARBITRER_IDS for m in members)
        if a_arb:
            a_arbitrer_count += 1

        # Dave Pils : on rattache la composante « Dave Pils » de PERS-S76-064.
        if DAVE_PILS_HOST_ID in same_as:
            same_as = sorted(set(same_as) | {"PERS-S76-064#dave-pils"})

        records.append({
            "id": pid_slug,
            "type_unite": "person",
            "name": canon_name,
            "categorie": categorie,
            "role": _roles_list(members),
            "sources": _sources_list(members),
            "same_as": same_as,
            "alt_names": alt_names,
            "categorie_a_arbitrer": cat_arb,
            "a_arbitrer": a_arb,
        })

    # Éclatements : nouveaux PERSON- distincts (Eddy, Oz, Jasmine).
    for slug, name, categorie, sa, a_arb, note in SPLIT_NEW_PERSONS:
        records.append({
            "id": slug, "type_unite": "person", "name": name,
            "categorie": categorie, "role": ["acteur (à préciser)"],
            "sources": ["S76"], "same_as": sa, "alt_names": [],
            "categorie_a_arbitrer": False, "a_arbitrer": a_arb, "note": note,
        })
        if a_arb:
            a_arbitrer_count += 1

    records.extend(ADDITIONAL_CANONICAL_PERSONS)

    records.sort(key=lambda r: r["id"])
    return records, a_arbitrer_count


def _roles_list(members: List[Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    for m in members:
        d = m["data"]
        r = d.get("role")
        if isinstance(r, list):
            for x in r:
                if x and x not in out:
                    out.append(x)
    return out or ["acteur"]


def _sources_list(members: List[Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    for m in members:
        d = m["data"]
        srcs = d.get("sources") or ([d.get("source_id")] if d.get("source_id") else [])
        if isinstance(srcs, str):
            srcs = [srcs]
        for s in srcs or []:
            if s and s not in out:
                out.append(s)
    return out or ["?"]


# --------------------------------------------------------------------------- #
# Rendu
# --------------------------------------------------------------------------- #
def _yaml_list(items: List[str]) -> str:
    if not items:
        return " []"
    return "\n" + "\n".join(f"  - {_q(x)}" for x in items)


def _q(s: str) -> str:
    s = str(s)
    if re.search(r'[:#"\'\[\]{}]|^\s|\s$', s) or s == "":
        return '"' + s.replace('"', '\\"') + '"'
    return s


def render_md(records: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
    L: List[str] = []
    L.append("# Registre canonique des acteurs — `PERSON-`")
    L.append("")
    L.append("> **Étape 9 — canonicalisation.** Identités canoniques des personnes, "
             "construites par `tools/build_people_canon.py` à partir de la couche "
             "provisoire `PERS-*` (`exports/generated/people.json`).")
    L.append("> **Gel additif** : chaque `PERS-*` est conservé tel quel et rabattu ici "
             "via `same_as` ; aucun id provisoire n'est renommé ni supprimé.")
    L.append("> **SSOT** : ce fichier est GÉNÉRÉ. Ne pas l'éditer à la main — modifier "
             "le générateur, puis `python3 tools/build_people_canon.py`. La sentinelle "
             "anti-drift (`tools/validate_people.py --check-drift`) rejoue le générateur "
             "et échoue sur toute divergence.")
    L.append(f"> **Schéma** : [`schemas/person_canonical.schema.json`](../../schemas/person_canonical.schema.json) "
             "(Draft 2020-12).")
    L.append("")
    L.append("## Statistiques")
    L.append("")
    L.append("| Indicateur | Valeur |")
    L.append("|------------|:------:|")
    L.append(f"| `PERSON-` canoniques | {stats['n_person']} |")
    L.append(f"| Liens `same_as` câblés (ids `PERS-*` rabattus) | {stats['n_same_as']} |")
    L.append(f"| `alt_names` (formes secondaires) | {stats['n_alt']} |")
    L.append(f"| Renvois `ORG-` (hand-off) | {stats['n_org']} |")
    L.append(f"| Renvois concept (hand-off) | {stats['n_concept']} |")
    L.append(f"| Items `a_arbitrer` | {stats['n_a_arbitrer']} |")
    L.append(f"| `categorie_a_arbitrer` (double appartenance) | {stats['n_cat_arb']} |")
    L.append("")
    L.append("## Répartition par `categorie`")
    L.append("")
    L.append("| Catégorie | Nb |")
    L.append("|-----------|:--:|")
    for cat, n in sorted(stats["by_cat"].items(), key=lambda x: (-x[1], x[0])):
        L.append(f"| {cat} | {n} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("# Identités canoniques")
    L.append("")
    for r in records:
        L.append(f"## {r['id']} — {r['name']}")
        L.append("")
        L.append("```yaml")
        L.append(f"id: {r['id']}")
        L.append(f"type_unite: {r['type_unite']}")
        L.append(f"name: {_q(r['name'])}")
        L.append(f"categorie: {r['categorie']}")
        L.append(f"role:{_yaml_list(r['role'])}")
        L.append(f"sources:{_yaml_list(r['sources'])}")
        L.append(f"same_as:{_yaml_list(r['same_as'])}")
        L.append(f"alt_names:{_yaml_list(r['alt_names'])}")
        L.append(f"categorie_a_arbitrer: {str(r['categorie_a_arbitrer']).lower()}")
        L.append(f"a_arbitrer: {str(r['a_arbitrer']).lower()}")
        if r.get("note"):
            L.append(f"note: {_q(r['note'])}")
        L.append("```")
        L.append("")
    return "\n".join(L) + "\n"


def build_handoffs(rows_by_id: Dict[str, Dict[str, Any]]):
    org = {
        "_comment": "Hand-off étape 10 — entités collectives à promouvoir en ORG-. "
                    "NE PAS créer ici. Issu de la canonicalisation PERSON- (étape 9).",
        "items": [],
    }
    for pid, name in sorted(PENDING_ORG.items()):
        org["items"].append({"from_pers": pid, "name": name, "target_kind": "ORG-"})
    # Oz PA, composante d'entité de l'éclatement de PERS-S76-052.
    org["items"].append({
        "from_pers": "PERS-S76-052#oz-pa", "name": "Oz PA",
        "target_kind": "ORG-",
        "note": "Équipe de sonorisation (entité) issue de l'éclatement de "
                "« Oz PA / Eddy et Oz » ; les individus Eddy et Oz sont des PERSON- (a_arbitrer).",
    })
    org["items"].sort(key=lambda x: x["from_pers"])

    concept = {
        "_comment": "Hand-off étape 10 — figures NI ORG- NI PERSON- (sous-cultures, "
                    "collectifs diffus) à verser en registre concept. NE PAS créer ici.",
        "items": [],
    }
    for pid, name in sorted(PENDING_CONCEPT.items()):
        concept["items"].append({
            "from_pers": pid, "name": name, "target_kind": "concept",
            "note": "Sous-culture juvénile mancunienne ; ni entité morale ni personne.",
        })
    return org, concept


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Génère le registre canonique PERSON-.")
    ap.add_argument("--to-stdout", action="store_true", help="Imprime le .md sans rien écrire.")
    ap.add_argument("--emit", action="store_true", help="Écrit les livrables (défaut).")
    args = ap.parse_args(argv)

    rows = load_people()
    rows_by_id = {r["id"]: r for r in rows}
    records, n_a_arb = build_records(rows)

    by_cat: Dict[str, int] = defaultdict(int)
    n_same_as = n_alt = n_cat_arb = 0
    for r in records:
        by_cat[r["categorie"]] += 1
        n_same_as += len([x for x in r["same_as"] if not x.endswith("#dave-pils")])
        n_alt += len(r["alt_names"])
        n_cat_arb += 1 if r["categorie_a_arbitrer"] else 0

    org, concept = build_handoffs(rows_by_id)
    n_org = len(org["items"])
    n_concept = len(concept["items"])

    stats = {
        "n_person": len(records), "n_same_as": n_same_as, "n_alt": n_alt,
        "n_org": n_org, "n_concept": n_concept, "n_a_arbitrer": n_a_arb,
        "n_cat_arb": n_cat_arb, "by_cat": dict(by_cat),
    }

    md = render_md(records, stats)
    if args.to_stdout:
        sys.stdout.write(md)
        return 0

    OUT_MD.write_text(md, encoding="utf-8")
    OUT_ORG.write_text(json.dumps(org, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_CONCEPT.write_text(json.dumps(concept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Identité de partition : 305 ids PERS-* = same_as câblés + hand-offs + composantes mixtes.
    total_pers = len([r for r in rows])
    print(f"PERSON- canoniques : {len(records)}")
    print(f"same_as câblés     : {n_same_as}")
    print(f"alt_names          : {n_alt}")
    print(f"renvois ORG-       : {n_org} | concept : {n_concept}")
    print(f"a_arbitrer         : {n_a_arb} | categorie_a_arbitrer : {n_cat_arb}")
    print(f"catégories         : {dict(by_cat)}")
    print(f"ids PERS-* en entrée : {total_pers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
