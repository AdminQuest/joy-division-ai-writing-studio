#!/usr/bin/env python3
"""Validate the quote register (étape 8b-1 — backbone structurel).

Porte gate-able du registre citations : exit 0 si errors == 0, sinon exit 1.

L'identité d'une citation est **source + ordinal**, CONSERVÉE (aucun renommage) :
trois conventions legacy coexistent, toutes reconnues comme `quote` —
`S\\d+-Q\\d+`, `S\\d+-CIT-\\d+`, `CIT-S\\d+-\\d+`. Le backbone
(`kind/texte/type/page`) est dérivé par `build_registers.normalize_quote_record`
(parité stricte avec le build et le loader runtime). L'attribution et le split
fin paraphrase/concept relèvent de l'étape 8b-2 et ne sont PAS contrôlés ici.

Invariants (sévérité ERROR sauf mention) :
  INV1 — schéma : champs requis du backbone présents (id, kind, source_id,
         texte, type) ; `type` ∈ {verbatim, non_verbatim}.
  INV2 — convention d'id : ∈ {S\\d+-Q\\d+, S\\d+-CIT-\\d+, CIT-S\\d+-\\d+}.
  INV3 — provenance : `source_id` présent ; `page` présent OU « inconnue »
         (pas de fabrication).
  INV4 — type : redondant avec INV1 (contrôle explicite de la valeur).
  INV5 — same_as : mono-valué (chaîne) ; cible ∈ ids citations existants ;
         pas d'auto-référence ; point fixe (la cible ne porte pas elle-même de
         same_as : ni chaîne ni cycle).
  INV6 — gel EVENT-/CONCERT- : aucun id de citation n'empiète sur les espaces
         EVENT-/CONCERT- ; aucune cible same_as hors du registre citations.

Usage : python3 tools/validate_quotes.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_against_schema  # noqa: E402
import build_registers as br  # noqa: E402

ID_CONVENTIONS = re.compile(r"^(?:S\d+-Q\d+|S\d+-CIT-\d+|CIT-S\d+-\d+)$")
VALID_PAGE_SENTINEL = "inconnue"
FROZEN_PREFIXES = ("EVENT-", "CONCERT-")


def collect_quotes():
    """Parcourt les sources comme le build, normalise, retourne les records quote."""
    br.ensure_source_labels_loaded()
    records = {}
    for path in br.iter_markdown_files():
        for data, _heading in br.extract_yaml_blocks(path):
            if br.infer_kind(data, path) != "quote":
                continue
            br.normalize_quote_record(data)
            rid = str(data.get("id") or "")
            records[rid] = (data, br.rel(path))
    return records


def _has_page(data) -> bool:
    page = data.get("page")
    if isinstance(page, str) and page.strip():
        return True
    if page not in (None, "", [], {}):
        return True
    return br._quote_has_real_page(data)


def main() -> int:
    records = collect_quotes()
    errors: list[str] = []
    warnings: list[str] = []
    ids = set(records)

    for rid, (data, path) in sorted(records.items()):
        loc = f"{path} [{rid or '?'}]"

        # INV1 — schéma backbone
        for message in validate_against_schema("quote", data):
            errors.append(f"INV1 schéma — {loc} : {message}")

        # INV2 — convention d'id
        if not rid or not ID_CONVENTIONS.match(rid):
            errors.append(f"INV2 id — {loc} : identifiant hors convention citation")

        # INV3 — provenance
        if not data.get("source_id"):
            errors.append(f"INV3 provenance — {loc} : source_id manquant")
        if not _has_page(data):
            errors.append(f"INV3 provenance — {loc} : ni page réelle ni « {VALID_PAGE_SENTINEL} »")

        # INV4 — type
        if data.get("type") not in {"verbatim", "non_verbatim"}:
            errors.append(f"INV4 type — {loc} : type={data.get('type')!r} ∉ {{verbatim, non_verbatim}}")

        # INV5 — same_as
        same_as = data.get("same_as")
        if same_as not in (None, "", [], {}):
            if not isinstance(same_as, str):
                errors.append(f"INV5 same_as — {loc} : doit être mono-valué (chaîne), pas {type(same_as).__name__}")
            else:
                if same_as == rid:
                    errors.append(f"INV5 same_as — {loc} : auto-référence")
                elif same_as not in ids:
                    errors.append(f"INV5 same_as — {loc} : cible {same_as} introuvable dans le registre citations")
                else:
                    target_data = records[same_as][0]
                    if target_data.get("same_as") not in (None, "", [], {}):
                        errors.append(
                            f"INV5 same_as — {loc} : la cible {same_as} porte elle-même un same_as "
                            f"(chaîne/cycle ; le retenu doit être un point fixe)"
                        )
                # INV6 — la cible reste dans le registre citations
                if isinstance(same_as, str) and same_as.startswith(FROZEN_PREFIXES):
                    errors.append(f"INV6 gel — {loc} : same_as pointe un espace gelé {same_as}")

        # INV6 — gel : un id de citation ne doit pas empiéter sur EVENT-/CONCERT-
        if rid.startswith(FROZEN_PREFIXES):
            errors.append(f"INV6 gel — {loc} : id de citation empiète sur un espace gelé")

    total = len(records)
    print("Validation du registre citations (étape 8b-1)")
    print("-" * 48)
    print(f"Records quote        : {total}")
    print(f"Erreurs              : {len(errors)}")
    print(f"Avertissements       : {len(warnings)}")
    if errors:
        print("\nErreurs :")
        for e in errors[:60]:
            print(f"  - {e}")
        if len(errors) > 60:
            print(f"  … {len(errors) - 60} autre(s)")
        print("\nPORTE DU REGISTRE CITATIONS : FERMÉE (errors > 0)")
        return 1
    print("\nPORTE DU REGISTRE CITATIONS : OUVERTE (errors = 0)")
    print("Backbone vérifié : INV1..6 (schéma, id, provenance, type, same_as, gel).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
