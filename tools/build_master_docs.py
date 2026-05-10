#!/usr/bin/env python3
"""
Generate chapter master documents from documentary exports.
"""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "exports" / "generated"
CHAPTERS_DIR = REPO_ROOT / "chapters"
TEMPLATE_PATH = REPO_ROOT / "templates" / "document_maitre_template.md"

CHAPTERS = {
    1: "Manchester, année zéro : le terreau de la colère",
    2: "Les années d'apprentissage : quand quatre furieux décident de faire de la musique",
    3: "Warsaw : le chaos initial",
    4: "La naissance de Joy Division",
    5: "Unknown Pleasures : le surgissement du noir",
    6: "Martin Hannett et l'invention du vide",
    7: "Closer : la désintégration intérieure",
    8: "Love Will Tear Us Apart : anatomie d'un adieu",
    9: "Ian Curtis : corps, scène et convulsions",
    10: "Factory Records et la mythologie mancunienne",
    11: "Joy Division et la condition humaine moderne",
    12: "Les héritiers du vide : l'onde post-punk",
    13: "Les territoires de la mélancolie : géographie émotionnelle",
    14: "L'éternel retour : Joy Division dans la culture contemporaine",
}


def load_json(name):
    path = EXPORT_DIR / name
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


atoms = load_json("atoms.json")
quotes = load_json("quotes.json")
chronology = load_json("chronology.json")
songs = load_json("songs.json")
people = load_json("people.json")
sources = load_json("sources.json")


def chapter_match(record, chapter_number):
    data = record.get("data", {})
    chapters = data.get("chapitres") or data.get("chapters") or []
    target = f"Chapitre {chapter_number}"
    return target in chapters


TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8")


for chapter_number, chapter_title in CHAPTERS.items():
    related_atoms = [a for a in atoms if chapter_match(a, chapter_number)]
    related_quotes = [q for q in quotes if chapter_match(q, chapter_number)]

    concepts = sorted({
        concept
        for atom in related_atoms
        for concept in atom.get("data", {}).get("concepts", [])
    })

    source_ids = sorted({
        atom.get("data", {}).get("source_id")
        for atom in related_atoms
        if atom.get("data", {}).get("source_id")
    })

    source_lines = []
    for src in sources:
        if src.get("source_id") in source_ids:
            source_lines.append(f"- {src.get('source_label')}")

    atom_lines = []
    for atom in related_atoms[:100]:
        atom_lines.append(
            f"- {atom.get('id')} — {atom.get('data', {}).get('type_unite', 'analyse')}"
        )

    quote_lines = []
    for quote in related_quotes[:50]:
        quote_lines.append(
            f"- {quote.get('id')}"
        )

    content = TEMPLATE.format(
        chapter_number=chapter_number,
        chapter_number_padded=str(chapter_number).zfill(2),
        chapter_title=chapter_title,
        function_section="Document maître de consolidation rédactionnelle et documentaire.",
        included_section="Atomes, citations, chronologie, chansons, personnes et concepts liés au chapitre.",
        excluded_section="Éléments hors période ou hors problématique principale.",
        questions_section="- Structuration analytique du chapitre\n- Vérification des contradictions\n- Consolidation des sources",
        hypotheses_section="- Les matériaux sont provisoires\n- Les contradictions doivent être tracées",
        primary_sources_section="\n".join(source_lines) if source_lines else "- Aucune source reliée",
        secondary_sources_section="- À compléter",
        atoms_section="\n".join(atom_lines) if atom_lines else "- Aucun atome relié",
        quotes_section="\n".join(quote_lines) if quote_lines else "- Aucune citation reliée",
        chronology_section="- À générer automatiquement",
        songs_section="- À générer automatiquement",
        people_section="- À générer automatiquement",
        concepts_section="\n".join(f"- {c}" for c in concepts) if concepts else "- Aucun concept",
        articulation_section="- À compléter",
        warnings_section="- Vérifier les doublons inter-chapitres",
        gaps_section="- Sources secondaires à enrichir",
        draft_state_section="- Document généré automatiquement"
    )

    chapter_dir = CHAPTERS_DIR / f"{str(chapter_number).zfill(2)}"
    chapter_dir.mkdir(parents=True, exist_ok=True)

    output_path = chapter_dir / "document_maitre.md"
    output_path.write_text(content, encoding="utf-8")

print("Master documents generated.")
