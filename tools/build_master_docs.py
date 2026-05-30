#!/usr/bin/env python3
"""
Generate chapter master documents from documentary exports.

The generated master documents are not draft chapters. They are structured
working files for writing: they consolidate atoms, sources, citations, chronology,
people, songs, concepts, motifs and warnings by chapter.

Inputs:
    exports/generated/*.json
    chapters/master_docs.json

Outputs:
    chapters/XX/document_maitre.md
    chapters/master_docs.json
    exports/generated/master_docs_index.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buildlib import resolved_generated_at  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "exports" / "generated"
CHAPTERS_DIR = REPO_ROOT / "chapters"
MANIFEST_PATH = CHAPTERS_DIR / "master_docs.json"
MASTER_INDEX_PATH = EXPORT_DIR / "master_docs_index.json"

MAX_CRITICAL_ATOMS = 60
MAX_OTHER_ATOMS = 80
MAX_CONCEPTS = 80
MAX_QUOTES = 40
MAX_CHRONOLOGY = 40
MAX_PEOPLE = 40
MAX_SONGS = 40

CHAPTERS = {
    1: "Manchester année zéro : le terreau de la colère",
    2: "Les années d'apprentissage : quand quatre furieux décident de faire de la musique (1976-1978)",
    3: "La première racine du son de l’éternel : les innovations sonores",
    4: "La deuxième racine : la poésie de l’aliénation de Ian Curtis",
    5: "La troisième racine : Peter Saville et l'esthétique du vide",
    6: "L’arbre se dresse : quand l’architecture sonore devient cathédrale (1979-1980)",
    7: "L'héritage musical à travers les décennies",
    8: "Joy Division underground : la culture bootleg comme mémoire alternative",
    9: "Résonances globales : l’influence internationale de Joy Division",
    10: "Joy Division à l'ère numérique : perpétuation et réinvention du mythe",
    11: "Joy Division et la condition humaine moderne",
    12: "L’expression du trauma : Joy Division et le dialogue sur la santé mentale",
    13: "Les territoires de la mélancolie : Joy Division et la géographie émotionnelle",
    14: "L’éternel retour : Joy Division dans la culture contemporaine",
}

CHAPTER_FUNCTIONS = {
    1: "Établir Manchester comme matrice urbaine, sociale et affective du livre.",
    2: "Décrire la mutation de Warsaw en Joy Division, depuis l’apprentissage punk jusqu’à la stabilisation d’un langage.",
    3: "Isoler les innovations sonores qui permettent au groupe de rompre avec la simple énergie punk.",
    4: "Étudier l’écriture de Curtis comme poésie de l’aliénation, sans rabattre les textes sur une lecture strictement biographique.",
    5: "Analyser l’identité visuelle, Peter Saville, Factory et l’esthétique du vide comme architecture parallèle au son.",
    6: "Montrer comment la production, l’espace sonore et la forme-album transforment Joy Division en cathédrale noire.",
    7: "Cartographier les héritages musicaux et les reprises esthétiques de Joy Division.",
    8: "Traiter la culture bootleg comme mémoire parallèle, archive souterraine et contre-récit de la canonisation.",
    9: "Étudier la diffusion internationale du groupe et ses réceptions hors du cadre britannique.",
    10: "Examiner la perpétuation numérique du mythe, ses réemplois et ses mutations d’archive.",
    11: "Interroger la persistance existentielle de Joy Division dans la condition humaine moderne.",
    12: "Analyser le trauma, la santé mentale, l’éthique de la réception et la difficulté de parler de Curtis sans réduction clinique.",
    13: "Lire Joy Division à travers la géographie émotionnelle, les espaces vécus et les territoires de la mélancolie.",
    14: "Suivre la patrimonialisation contemporaine, les détournements visuels, la culture populaire et l’éternel retour du mythe.",
}

CHAPTER_QUESTIONS = {
    1: ["Qu’est-ce que Manchester apporte que Londres ne peut pas produire ?", "Comment éviter le déterminisme urbain ?"],
    2: ["Comment Warsaw devient-il Joy Division ?", "Quels échecs rendent possible la bifurcation Factory ?"],
    3: ["Quels gestes sonores distinguent Joy Division du punk ?", "Comment articuler Hook, Morris, Hannett et l’espace sonore ?"],
    4: ["Comment lire Curtis sans réduire les chansons à sa biographie ?", "Quels textes relèvent de l’aliénation, du contrôle, de la crise ?"],
    5: ["Comment Factory fabrique-t-elle une esthétique du vide ?", "Quelles attributions Saville faut-il vérifier ?"],
    6: ["Comment le groupe devient-il architecture sonore ?", "Comment traiter *Closer* sans téléologie morbide ?"],
    7: ["Quels héritages sont musicaux plutôt que seulement visuels ?", "Quels prolongements relèvent d’une influence documentée ?"],
    8: ["Que conserve le bootleg que l’archive officielle ne conserve pas ?", "Comment éviter la fascination pure pour l’objet rare ?"],
    9: ["Comment Joy Division circule-t-il hors de Manchester ?", "Quelles réceptions étrangères modifient le mythe ?"],
    10: ["Que transforme l’ère numérique dans la mémoire du groupe ?", "Comment distinguer archive, fétiche et circulation algorithmique ?"],
    11: ["Pourquoi Joy Division parle-t-il encore à la condition moderne ?", "Comment éviter les généralités existentielles ?"],
    12: ["Comment écrire la santé mentale sans diagnostic réducteur ?", "Quelles sources protègent contre la romantisation ?"],
    13: ["Quels lieux deviennent des opérateurs émotionnels ?", "Comment éviter de faire des lieux des causes directes ?"],
    14: ["Comment le groupe devient-il patrimoine culturel ?", "Quels usages contemporains trahissent, prolongent ou simplifient Joy Division ?"],
}


def load_json(name: str, default: Any = None) -> Any:
    path = EXPORT_DIR / name
    if default is None:
        default = []
    if not path.exists():
        return default
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return default
    return json.loads(text)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def value_at(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    cursor: Any = data
    for part in path.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            return default
        cursor = cursor[part]
    return cursor


def chapter_label(number: int) -> str:
    return f"Chapitre {number}"


def chapter_match(record: Dict[str, Any], chapter_number: int) -> bool:
    data = record.get("data", {})
    target = chapter_label(chapter_number)
    target_short = f"CH{chapter_number:02d}"

    # The v2 atom schema often uses `usage_livre` rather than `chapitres`
    # to indicate chapter use. Master docs must therefore project atoms from
    # all explicit chapter-use fields, not only from legacy chapter fields.
    values = (
        as_list(data.get("chapitres"))
        + as_list(data.get("chapters"))
        + as_list(data.get("usage_livre"))
        + as_list(data.get("liens_interchapitres"))
    )

    normalized = {text(value) for value in values if text(value)}
    normalized_lower = {value.lower() for value in normalized}

    return (
        target in normalized
        or target.lower() in normalized_lower
        or target_short in normalized
        or target_short.lower() in normalized_lower
        or str(chapter_number) in normalized
    )


def md_escape(value: Any) -> str:
    return text(value).replace("\n", " ").replace("|", "\\|")


def bullets(values: Iterable[Any], empty: str = "À compléter.", limit: Optional[int] = None) -> str:
    cleaned: List[str] = []
    for value in values:
        item = text(value)
        if item and item not in cleaned:
            cleaned.append(item)
        if limit and len(cleaned) >= limit:
            break
    if not cleaned:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in cleaned)


def markdown_list(items: Iterable[Any], empty: str = "À compléter.", limit: Optional[int] = None) -> str:
    """Return already formatted Markdown list items without adding bullets twice."""
    cleaned: List[str] = []
    for value in items:
        item = text(value)
        if item and item not in cleaned:
            cleaned.append(item)
        if limit and len(cleaned) >= limit:
            break
    if not cleaned:
        return f"- {empty}"
    return "\n".join(cleaned)


def atom_title(atom: Dict[str, Any]) -> str:
    heading = text(atom.get("heading"))
    if heading:
        return heading
    data = atom.get("data", {})
    summary = text(data.get("resume") or data.get("citation_directe") or data.get("titre"))
    return summary[:120] + ("…" if len(summary) > 120 else "")


def source_label(source_id: str, source_index: Dict[str, Dict[str, Any]]) -> str:
    source = source_index.get(source_id)
    if not source:
        return source_id
    return text(source.get("source_label") or source_id)


def importance_rank(atom: Dict[str, Any]) -> int:
    data = atom.get("data", {})
    niveau = text(value_at(data, "importance.niveau") or data.get("importance")).lower()
    if niveau == "critique":
        return 0
    if niveau == "majeure":
        return 1
    if niveau == "utile":
        return 2
    if niveau:
        return 3
    return 4


def is_critical_atom(atom: Dict[str, Any]) -> bool:
    data = atom.get("data", {})
    niveau = text(value_at(data, "importance.niveau") or data.get("importance")).lower()
    role = " ".join(text(x).lower() for x in as_list(data.get("role_argumentatif")))
    return niveau in {"critique", "majeure"} or any(keyword in role for keyword in ["central", "pivot", "nœud", "noeud", "structurant"])


def atom_line(atom: Dict[str, Any], source_index: Dict[str, Dict[str, Any]]) -> str:
    data = atom.get("data", {})
    atom_id = text(atom.get("id"))
    source_id = text(data.get("source_id"))
    type_unite = text(data.get("type_unite") or "analyse")
    importance = text(value_at(data, "importance.niveau") or data.get("importance") or "non qualifiée")
    proof = text(value_at(data, "niveau_preuve.statut") or data.get("fiabilite") or "non qualifié")
    title = atom_title(atom)
    return f"- **{atom_id}** — {title}  \n  Source : {source_label(source_id, source_index)} ; type : `{type_unite}` ; importance : `{importance}` ; preuve : `{proof}`."


def table(rows: List[List[Any]], headers: List[str]) -> str:
    if not rows:
        return "- À compléter."
    output = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        output.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(output)


def source_rows(atoms: List[Dict[str, Any]], quotes: List[Dict[str, Any]], source_index: Dict[str, Dict[str, Any]]) -> List[List[Any]]:
    counts: Dict[str, Counter] = defaultdict(Counter)
    for atom in atoms:
        sid = text(atom.get("data", {}).get("source_id"))
        if sid:
            counts[sid]["atomes"] += 1
    for quote in quotes:
        sid = text(quote.get("data", {}).get("source_id"))
        if sid:
            counts[sid]["citations"] += 1
    rows = []
    for sid in sorted(counts):
        rows.append([sid, source_label(sid, source_index), counts[sid]["atomes"], counts[sid]["citations"]])
    return rows


def quote_line(quote: Dict[str, Any], source_index: Dict[str, Dict[str, Any]]) -> str:
    data = quote.get("data", {})
    quote_id = text(quote.get("id"))
    sid = text(data.get("source_id"))
    original = text(data.get("citation_originale") or data.get("citation_directe") or data.get("traduction_editoriale_fr"))
    status = text(data.get("statut_verification") or data.get("statut") or "à vérifier")
    if len(original) > 220:
        original = original[:220] + "…"
    return f"- **{quote_id}** — {source_label(sid, source_index)} — statut : `{status}` — « {original} »"


def record_label(record: Dict[str, Any]) -> str:
    data = record.get("data", {})
    rid = text(record.get("id") or data.get("id") or data.get("song") or data.get("name"))
    title = text(data.get("event") or data.get("name") or data.get("full_name") or data.get("song") or record.get("heading"))
    return f"{rid} — {title}" if title and rid and title != rid else rid or title


def people_table_rows(records: List[Dict[str, Any]]) -> List[List[str]]:
    """Return table rows [ID, Nom, Description] for people records."""
    rows = []
    for record in records:
        data = record.get("data", {})
        rid = text(record.get("id") or data.get("id") or data.get("name"))
        name = text(data.get("full_name") or data.get("name") or record.get("heading") or "")
        if not name or name == rid:
            label = record_label(record)
            if " — " in label:
                rid, name = label.split(" — ", 1)
            else:
                rid = label
                name = ""
        description = text(data.get("description") or data.get("role") or data.get("role_dans_chapitre") or "")
        if not description:
            description = "description à compléter"
        rows.append([rid, name, description])
    return rows


def motif_values(atoms: List[Dict[str, Any]]) -> List[str]:
    counter: Counter[str] = Counter()
    for atom in atoms:
        for motif in as_list(atom.get("data", {}).get("motifs")):
            item = text(motif)
            if item:
                counter[item] += 1
    return [f"{name} ({count})" for name, count in counter.most_common(40)]


def concept_values(atoms: List[Dict[str, Any]]) -> List[str]:
    counter: Counter[str] = Counter()
    for atom in atoms:
        data = atom.get("data", {})
        values = as_list(data.get("concepts")) + as_list(data.get("concepts_derives"))
        for concept in values:
            item = text(concept)
            if item:
                counter[item] += 1
    return [f"{name} ({count})" for name, count in counter.most_common(MAX_CONCEPTS)]


def warning_values(atoms: List[Dict[str, Any]]) -> List[str]:
    warnings: List[str] = []
    for atom in atoms:
        data = atom.get("data", {})
        atom_id = text(atom.get("id"))
        risk = text(value_at(data, "risque_surinterpretation.raison") or data.get("limites_usage") or data.get("contradictions"))
        level = text(value_at(data, "risque_surinterpretation.niveau"))
        if risk:
            prefix = f"{atom_id}"
            if level:
                prefix += f" [{level}]"
            warnings.append(f"{prefix} — {risk}")
    return warnings[:60]


def relation_values(atoms: List[Dict[str, Any]]) -> List[str]:
    values: List[str] = []
    for atom in atoms:
        data = atom.get("data", {})
        atom_id = text(atom.get("id"))
        for relation in as_list(data.get("relations")):
            if isinstance(relation, dict):
                relation_type = text(relation.get("type"))
                target = text(relation.get("cible") or relation.get("target"))
                if relation_type or target:
                    values.append(f"{atom_id} — {relation_type} → {target}")
    return values[:80]


def chapter_document(chapter_number: int, title: str, context: Dict[str, Any]) -> str:
    atoms = context["atoms"]
    quotes = context["quotes"]
    chronology = context["chronology"]
    songs = context["songs"]
    people = context["people"]
    source_index = context["source_index"]
    generated_at = context["generated_at"]

    critical = sorted([atom for atom in atoms if is_critical_atom(atom)], key=lambda a: (importance_rank(a), text(a.get("id"))))[:MAX_CRITICAL_ATOMS]
    other = [atom for atom in sorted(atoms, key=lambda a: text(a.get("id"))) if atom not in critical][:MAX_OTHER_ATOMS]

    type_counts = Counter(text(atom.get("data", {}).get("type_unite") or "non qualifié") for atom in atoms)
    importance_counts = Counter(text(value_at(atom.get("data", {}), "importance.niveau") or atom.get("data", {}).get("importance") or "non qualifiée") for atom in atoms)

    lines: List[str] = [
        f"# Chapitre {chapter_number} — {title}",
        "",
        "```yaml",
        f"id: DM-CH{chapter_number:02d}",
        "type_unite: document_maitre",
        f"chapitre: \"Chapitre {chapter_number}\"",
        "source_generation: \"tools/build_master_docs.py\"",
        "statut: genere",
        f"generated_at: \"{generated_at}\"",
        "```",
        "",
        "## 1. Fonction du chapitre",
        "",
        CHAPTER_FUNCTIONS.get(chapter_number, "À compléter."),
        "",
        "## 2. Questions directrices",
        "",
        bullets(CHAPTER_QUESTIONS.get(chapter_number, [])),
        "",
        "## 3. Tableau de bord documentaire",
        "",
        table([
            ["Atomes", len(atoms)],
            ["Atomes critiques / majeurs", len(critical)],
            ["Citations", len(quotes)],
            ["Événements chronologiques", len(chronology)],
            ["Personnes", len(people)],
            ["Chansons", len(songs)],
            ["Sources mobilisées", len({text(atom.get('data', {}).get('source_id')) for atom in atoms if text(atom.get('data', {}).get('source_id'))})],
        ], ["Indicateur", "Valeur"]),
        "",
        "## 4. Sources mobilisées",
        "",
        table(source_rows(atoms, quotes, source_index), ["ID", "Source", "Atomes", "Citations"]),
        "",
        "## 5. Atomes critiques ou majeurs",
        "",
        markdown_list([atom_line(atom, source_index) for atom in critical], "Aucun atome critique ou majeur n’est encore qualifié."),
        "",
        "## 6. Autres atomes utiles",
        "",
        markdown_list([atom_line(atom, source_index) for atom in other], "Aucun autre atome rattaché.", MAX_OTHER_ATOMS),
        "",
        "## 7. Citations disponibles",
        "",
        markdown_list([quote_line(quote, source_index) for quote in quotes[:MAX_QUOTES]], "Aucune citation rattachée."),
        "",
        "## 8. Chronologie rattachée",
        "",
        bullets([record_label(record) for record in chronology[:MAX_CHRONOLOGY]], "Aucun événement chronologique rattaché."),
        "",
        "## 9. Personnes et acteurs",
        "",
        table(people_table_rows(people[:MAX_PEOPLE]), ["ID", "Nom", "Description"]) if people else "Aucune personne rattachée.",
        "",
        "## 10. Chansons rattachées",
        "",
        bullets([record_label(record) for record in songs[:MAX_SONGS]], "Aucune chanson rattachée."),
        "",
        "## 11. Concepts récurrents",
        "",
        bullets(concept_values(atoms), "Aucun concept rattaché.", MAX_CONCEPTS),
        "",
        "## 12. Motifs et chaînes relationnelles",
        "",
        "### 12.1. Motifs dominants",
        "",
        bullets(motif_values(atoms), "Aucun motif rattaché."),
        "",
        "### 12.2. Relations déclarées entre atomes, mythes et concepts",
        "",
        bullets(relation_values(atoms), "Aucune relation déclarée."),
        "",
        "## 13. Distribution documentaire",
        "",
        "### 13.1. Types d’atomes",
        "",
        table([[key, value] for key, value in type_counts.most_common()], ["Type", "Nombre"]),
        "",
        "### 13.2. Importance documentaire",
        "",
        table([[key, value] for key, value in importance_counts.most_common()], ["Importance", "Nombre"]),
        "",
        "## 14. Risques de surinterprétation et points de vigilance",
        "",
        bullets(warning_values(atoms), "Aucun risque explicite n’est encore qualifié."),
        "",
        "## 15. Lacunes et prochaines vérifications",
        "",
        bullets([
            "Vérifier les atomes anciens encore incomplets au regard du schéma v2.",
            "Contrôler les citations avant toute insertion dans le manuscrit.",
            "Éviter les doublons avec les chapitres voisins en consultant les champs `liens_interchapitres`.",
            "Ne pas transformer ce document maître en texte final : il sert de dossier documentaire de rédaction.",
        ]),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate chapter master documents from documentary exports.",
    )
    parser.add_argument(
        "--chapters-dir",
        type=Path,
        default=None,
        help=(
            "Target directory for generated document_maitre.md files and master_docs.json. "
            "Defaults to <repo_root>/chapters/ (public repo). "
            "Use ~/repos/joy-division-studio-private/chapters for the private repo."
        ),
    )
    args = parser.parse_args()

    # Resolve target chapters directory
    if args.chapters_dir is not None:
        target_chapters_dir = args.chapters_dir.expanduser().resolve()
        target_manifest_path = target_chapters_dir / "master_docs.json"
    else:
        target_chapters_dir = CHAPTERS_DIR
        target_manifest_path = MANIFEST_PATH

    atoms = load_json("atoms.json")
    quotes = load_json("quotes.json")
    chronology = load_json("chronology.json")
    songs = load_json("songs.json")
    people = load_json("people.json")
    sources = load_json("sources.json")
    source_index = {text(source.get("source_id")): source for source in sources if text(source.get("source_id"))}
    generated_at = resolved_generated_at()

    manifest = {"documents": []}
    index: Dict[str, Any] = {"generated_at": generated_at, "chapters": []}

    for chapter_number, title in CHAPTERS.items():
        context = {
            "atoms": [record for record in atoms if chapter_match(record, chapter_number)],
            "quotes": [record for record in quotes if chapter_match(record, chapter_number)],
            "chronology": [record for record in chronology if chapter_match(record, chapter_number)],
            "songs": [record for record in songs if chapter_match(record, chapter_number)],
            "people": [record for record in people if chapter_match(record, chapter_number)],
            "source_index": source_index,
            "generated_at": generated_at,
        }

        content = chapter_document(chapter_number, title, context)
        chapter_dir = target_chapters_dir / f"{chapter_number:02d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        rel_path = f"chapters/{chapter_number:02d}/document_maitre.md"
        (chapter_dir / "document_maitre.md").write_text(content, encoding="utf-8")

        manifest["documents"].append({"chapter": chapter_number, "title": title, "path": rel_path})
        index["chapters"].append({
            "chapter": chapter_number,
            "title": title,
            "path": rel_path,
            "atoms": len(context["atoms"]),
            "quotes": len(context["quotes"]),
            "chronology": len(context["chronology"]),
            "songs": len(context["songs"]),
            "people": len(context["people"]),
        })

    write_json(target_manifest_path, manifest)
    write_json(MASTER_INDEX_PATH, index)
    print("Master documents generated from atoms.")
    print(f"Manifest: {target_manifest_path}")
    print(f"Index: {MASTER_INDEX_PATH.relative_to(REPO_ROOT)}")
    if args.chapters_dir is not None:
        print(f"Note: chapters written to custom target: {target_chapters_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
