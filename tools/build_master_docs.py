#!/usr/bin/env python3
"""
Generate chapter master documents from documentary exports and a static fallback registry.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "exports" / "generated"
CHAPTERS_DIR = REPO_ROOT / "chapters"
TEMPLATE_PATH = REPO_ROOT / "templates" / "document_maitre_template.md"
MANIFEST_PATH = CHAPTERS_DIR / "master_docs.json"

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


def load_json(name: str):
    path = EXPORT_DIR / name
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = str(value)
    text = text.strip()
    return text or None


def chapter_match(record, chapter_number):
    data = record.get("data", {})
    chapters = [clean_text(item) for item in as_list(data.get("chapitres") or data.get("chapters"))]
    target = f"Chapitre {chapter_number}"
    return target in chapters


def bullet(lines):
    cleaned = []
    for line in lines:
        text = clean_text(line)
        if text:
            cleaned.append(text)
    return "\n".join(f"- {line}" for line in cleaned) if cleaned else "- À compléter"


def main() -> int:
    atoms = load_json("atoms.json")
    quotes = load_json("quotes.json")
    sources = load_json("sources.json")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    manifest = {"documents": []}

    for chapter_number, chapter_title in CHAPTERS.items():
        related_atoms = [a for a in atoms if chapter_match(a, chapter_number)]
        related_quotes = [q for q in quotes if chapter_match(q, chapter_number)]

        concepts = sorted({
            text
            for atom in related_atoms
            for raw in as_list(atom.get("data", {}).get("concepts"))
            if (text := clean_text(raw))
        }, key=str.casefold)
        source_ids = sorted({
            text
            for atom in related_atoms
            if (text := clean_text(atom.get("data", {}).get("source_id")))
        }, key=str.casefold)
        source_lines = [src.get("source_label") for src in sources if clean_text(src.get("source_id")) in source_ids]
        atom_lines = [f"{clean_text(atom.get('id')) or 'NO_ID'} — {clean_text(atom.get('data', {}).get('type_unite')) or 'analyse'}" for atom in related_atoms[:100]]
        quote_lines = [clean_text(quote.get("id")) for quote in related_quotes[:50]]

        content = template.format(
            chapter_number=chapter_number,
            chapter_number_padded=str(chapter_number).zfill(2),
            chapter_title=chapter_title,
            function_section=CHAPTER_FUNCTIONS[chapter_number],
            included_section="Périmètre documentaire propre au chapitre, sources rattachées, motifs conceptuels et éléments utiles à la rédaction.",
            excluded_section="Les développements relevant d’un autre chapitre doivent être renvoyés au document maître correspondant.",
            questions_section=bullet(["Quel problème le chapitre résout-il dans l’économie générale du livre ?", "Quelles sources permettent de stabiliser le propos ?", "Quels risques de doublons doivent être maîtrisés ?"]),
            hypotheses_section=bullet(["Le chapitre doit rester une vue de consolidation, non un texte final.", "Les sources rattachées orientent la rédaction mais ne remplacent pas la vérification."]),
            primary_sources_section=bullet(source_lines),
            secondary_sources_section="- À compléter depuis le registre consolidé des références.",
            atoms_section=bullet(atom_lines),
            quotes_section=bullet(quote_lines),
            chronology_section="- À compléter depuis `exports/generated/chronology.json`.",
            songs_section="- À compléter depuis `exports/generated/songs.json`.",
            people_section="- À compléter depuis `exports/generated/people.json`.",
            concepts_section=bullet(concepts),
            articulation_section="- À consolider au regard du tableau de cohérence thématique.",
            warnings_section="- Vérifier les recouvrements avec les chapitres voisins.\n- Ne pas confondre document maître et texte rédigé.",
            gaps_section="- À renseigner après nouvelle génération des registres et consolidation des sources.",
            draft_state_section="- Fichier généré et versionné pour consultation statique GitHub Pages."
        )

        chapter_dir = CHAPTERS_DIR / f"{chapter_number:02d}"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        rel_path = f"chapters/{chapter_number:02d}/document_maitre.md"
        (chapter_dir / "document_maitre.md").write_text(content, encoding="utf-8")
        manifest["documents"].append({"chapter": chapter_number, "title": chapter_title, "path": rel_path})

    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Master documents generated and manifest updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
