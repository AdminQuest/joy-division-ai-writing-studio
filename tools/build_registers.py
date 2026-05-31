#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Documentary parser v0.10dd

This script scans Markdown files, extracts fenced YAML blocks, classifies records,
normalizes source identifiers, validates them through the schema validation layer,
and generates JSON/CSV exports for RAG and documentary control.

v0.5 makes data/registre.json the canonical source registry for source labels.
v0.6 produces a permanent, structured diagnostic report even when no error is found.
v0.7 fixes YAML normalization, source record classification, and duplicate checks.
v0.8 tolerates one-space legacy top-level indentation and avoids false source-usage alerts.
v0.9 classifies concepts, myths, motifs, rules, quote batches and metadata blocks.
v0.10d rewrites infer_kind without regex and classifies register templates.
v0.10b classifies empty register schema examples as template records.
v0.10 classifies empty register schema examples as template records.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buildlib import resolved_generated_at  # noqa: E402

try:
    import yaml
except ImportError as exc:
    print("Missing dependency: PyYAML. Install it with: pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2) from exc

try:
    from schema_validation import validate_against_schema
except ImportError as exc:
    print("Unable to import tools/schema_validation.py", file=sys.stderr)
    raise SystemExit(2) from exc

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "exports" / "generated"
SOURCE_REGISTRY_PATH = REPO_ROOT / "data" / "registre.json"

SCAN_DIRS = [REPO_ROOT / "sources", REPO_ROOT / "registers"]

SOURCE_ID_ALIASES = {
    "S-BROLL-JOY-001": "S68",
}

ID_PREFIX_ALIASES = {
    "S-BROLL-A": "S68-A",
    "S-BROLL-Q": "S68-Q",
    "CHR-BROLL-": "CHR-S68-",
    "CIT-BROLL-": "CIT-S68-",
    "BROLL-A": "S68-A",
}

FALLBACK_SOURCE_LABELS = {
    "S41": {"auteur": "Peter Hook", "titre": "Unknown Pleasures: Inside Joy Division", "annee": "2012", "label": "S41 — Hook, Unknown Pleasures, 2012"},
    "S45": {"auteur": "Deborah Curtis", "titre": "Touching from a Distance", "annee": "1995", "label": "S45 — Curtis, Touching from a Distance, 1995"},
    "S46": {"auteur": "Mark Johnson", "titre": "An Ideal for Living: An History of Joy Division", "annee": "1984", "label": "S46 — Johnson, An Ideal for Living, 1984"},
    "S68": {"auteur": "Marco Broll", "titre": "Joy Division", "annee": "s.d.", "label": "S68 — Broll, Joy Division, s.d."},
}

SOURCE_LABELS: Dict[str, Dict[str, str]] = {}

YAML_BLOCK_RE = re.compile(r"```yaml\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
KNOWN_TOPLEVEL_KEYS = {
    "id", "source_id", "auteur", "titre", "source_titre", "source_label", "source_short_title", "source_year",
    "pages_pdf", "page_pdf", "type_unite", "concepts", "chapitres", "statut", "fiabilite", "citation_directe",
    "citation_originale", "traduction_editoriale_fr", "langue_originale", "importance", "statut_verification",
    "date", "precision_date", "event", "type", "location", "people", "songs", "sources", "certainty", "song",
    "period", "themes", "chapters", "name", "full_name", "role", "notes",
    "role_argumentatif", "niveau_preuve", "stabilite", "risque_surinterpretation", "liens_interchapitres",
    "liens_citations", "motifs", "concepts_derives", "charge_emotionnelle", "nature_discursive",
    "usages_redactionnels", "contradictions", "limites_usage", "legacy_id", "related_places", "related_sources"
}

@dataclass
class ParsedRecord:
    kind: str
    id: str
    file: str
    heading: Optional[str]
    data: Dict[str, Any]

@dataclass
class Diagnostic:
    level: str
    file: str
    message: str
    record_id: Optional[str] = None

def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")

def normalize_identifier(value: str) -> str:
    if value in SOURCE_ID_ALIASES:
        return SOURCE_ID_ALIASES[value]
    for old, new in ID_PREFIX_ALIASES.items():
        if value.startswith(old):
            return new + value[len(old):]
    return value

def normalize_value(value: Any) -> Any:
    if isinstance(value, str):
        return normalize_identifier(value)
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_value(val) for key, val in value.items()}
    return value

def normalize_source_entry(entry: Dict[str, Any]) -> Optional[Tuple[str, Dict[str, str]]]:
    raw_id = entry.get("id") or entry.get("source_id")
    if not isinstance(raw_id, str) or not raw_id.strip():
        return None
    source_id = normalize_identifier(raw_id.strip())
    auteur = str(entry.get("auteur") or entry.get("author") or "Inconnu")
    titre = str(entry.get("titre") or entry.get("title") or source_id)
    annee = str(entry.get("annee") or entry.get("source_year") or "")
    label = str(entry.get("source_label") or f"{source_id} — {auteur}, {titre}, {annee}".rstrip(", "))
    return source_id, {"auteur": auteur, "titre": titre, "annee": annee, "label": label}

def load_source_registry_entries() -> List[Dict[str, Any]]:
    if not SOURCE_REGISTRY_PATH.exists():
        return []
    try:
        registry = json.loads(SOURCE_REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Warning: unable to parse {rel(SOURCE_REGISTRY_PATH)}: {exc}", file=sys.stderr)
        return []
    if not isinstance(registry, list):
        print(f"Warning: {rel(SOURCE_REGISTRY_PATH)} must contain a JSON list.", file=sys.stderr)
        return []
    return [entry for entry in registry if isinstance(entry, dict)]

def load_source_labels() -> Dict[str, Dict[str, str]]:
    labels: Dict[str, Dict[str, str]] = dict(FALLBACK_SOURCE_LABELS)
    for entry in load_source_registry_entries():
        normalized = normalize_source_entry(entry)
        if not normalized:
            continue
        source_id, label_entry = normalized
        labels[source_id] = label_entry
        legacy_ids = entry.get("legacy_id") or entry.get("legacy_ids") or []
        if isinstance(legacy_ids, str):
            legacy_ids = [legacy_ids]
        if isinstance(legacy_ids, list):
            for legacy_id in legacy_ids:
                if isinstance(legacy_id, str) and legacy_id.strip():
                    SOURCE_ID_ALIASES.setdefault(legacy_id.strip(), source_id)
                    labels[legacy_id.strip()] = label_entry
    return labels

def ensure_source_labels_loaded() -> None:
    global SOURCE_LABELS
    if not SOURCE_LABELS:
        SOURCE_LABELS = load_source_labels()

def enrich_source_label(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data
    ensure_source_labels_loaded()
    data = normalize_value(data)
    source_id = data.get("source_id") or (data.get("id") if str(data.get("id", "")).startswith("S") and "-" not in str(data.get("id")) else None)
    if source_id in SOURCE_LABELS:
        label = SOURCE_LABELS[source_id]
        data.setdefault("source_label", label["label"])
        data.setdefault("source_short_title", f"{label['auteur']}, {label['titre']}, {label['annee']}")
        data.setdefault("source_year", label["annee"])
    if data.get("id") in SOURCE_LABELS:
        label = SOURCE_LABELS[data["id"]]
        data.setdefault("auteur", label["auteur"])
        data.setdefault("titre", label["titre"])
        data.setdefault("source_label", label["label"])
        data.setdefault("source_short_title", f"{label['auteur']}, {label['titre']}, {label['annee']}")
        data.setdefault("source_year", label["annee"])
    return data

def iter_markdown_files() -> Iterable[Path]:
    for directory in SCAN_DIRS:
        if not directory.exists():
            continue
        # sorted() by POSIX-relative path: filesystem traversal order differs across
        # platforms (APFS vs ext4), which would otherwise leak into record order and
        # every downstream export. The key is locale-independent (str compare on the
        # already-normalised rel() path).
        for path in sorted(directory.rglob("*.md"), key=rel):
            if "exports/generated" not in rel(path):
                yield path

def nearest_heading(text: str, pos: int) -> Optional[str]:
    before = text[:pos]
    headings = re.findall(r"^(#{1,6})\s+(.+?)\s*$", before, flags=re.MULTILINE)
    return headings[-1][1].strip() if headings else None

def is_empty_template(data: Dict[str, Any]) -> bool:
    if not isinstance(data, dict) or not data:
        return False
    if data.get("id") or data.get("song"):
        return False
    non_empty = []
    for value in data.values():
        if value is None:
            continue
        if isinstance(value, list) and value:
            non_empty.extend(item for item in value if item not in (None, ""))
        elif isinstance(value, dict) and value:
            non_empty.extend(item for item in value.values() if item not in (None, ""))
        elif value not in (None, ""):
            non_empty.append(value)
    return not non_empty

def normalize_yaml(raw: str) -> str:
    """Normalize unsafe one-line scalars while preserving valid YAML nesting.

    The parser accepts a narrow legacy defect: exactly one accidental leading
    space before a known top-level key, for example ' type_unite: fait'.
    It does not de-indent valid nested fields, which normally use two spaces.
    """
    fixed_lines: List[str] = []
    mapping_line = re.compile(r"^(\s*)([A-Za-z_][A-Za-z0-9_\-]*:\s*)(.+?)\s*$")
    one_space_top_key = re.compile(r"^ ([A-Za-z_][A-Za-z0-9_\-]*):")
    for line in raw.splitlines():
        top_key = one_space_top_key.match(line)
        if top_key and top_key.group(1) in KNOWN_TOPLEVEL_KEYS:
            line = line[1:]
        match = mapping_line.match(line)
        if not match:
            fixed_lines.append(line)
            continue
        indent, key_prefix, value = match.groups()
        stripped = value.strip()
        if not stripped or stripped[0] in {'\"', "'", "[", "{", "|", ">"}:
            fixed_lines.append(line)
            continue
        if ": " not in stripped:
            fixed_lines.append(line)
            continue
        escaped = stripped.replace("\\", "\\\\").replace('"', '\\"')
        fixed_lines.append(f'{indent}{key_prefix}"{escaped}"')
    return "\n".join(fixed_lines)

def extract_yaml_blocks(path: Path) -> List[Tuple[Dict[str, Any], Optional[str]]]:
    text = path.read_text(encoding="utf-8")
    blocks: List[Tuple[Dict[str, Any], Optional[str]]] = []
    # Document-level source_id (a header block carrying source_id but no id) so
    # quote sub-records that omit their own source_id can inherit it, mirroring
    # the dynamic-registers.js loader.
    context_source_id: Optional[str] = None
    for match in YAML_BLOCK_RE.finditer(text):
        raw = match.group(1).strip()
        heading = nearest_heading(text, match.start())
        if not raw:
            continue
        try:
            loaded = yaml.safe_load(normalize_yaml(raw))
        except yaml.YAMLError as exc:
            blocks.append(({"__parse_error__": str(exc), "__raw__": raw}, heading))
            continue
        if isinstance(loaded, dict):
            if is_empty_template(loaded):
                continue
            if loaded.get("source_id") and not loaded.get("id"):
                context_source_id = str(loaded["source_id"])
            # First-level quote container: a block shaped `quotes:` / `citations:`
            # carrying a LIST OF OBJECTS is a set of sub-records, not one record.
            # The top-level list form (`- id: …`) is already split below; this
            # restores parity for the wrapped form, which was otherwise ingested
            # as a single id-less dict and dropped as a template — the citations
            # blind spot (step 8a). The guard requires at least one object in the
            # list so a record's homonymous string-list field (e.g.
            # `citations: [S12-A005]`) is not mistaken for a container. Scope is
            # deliberately limited to quote-bearing keys; other container keys
            # (people, places, chronology…) remain each register's own concern.
            container_key = next(
                (k for k in ("quotes", "citations")
                 if isinstance(loaded.get(k), list)
                 and any(isinstance(x, dict) for x in loaded[k])),
                None,
            )
            if container_key:
                for item in loaded[container_key]:
                    if isinstance(item, dict) and not is_empty_template(item):
                        if context_source_id and not item.get("source_id"):
                            item = {"source_id": context_source_id, **item}
                        blocks.append((enrich_source_label(item), heading))
                continue
            blocks.append((enrich_source_label(loaded), heading))
        elif isinstance(loaded, list):
            for item in loaded:
                if isinstance(item, dict) and not is_empty_template(item):
                    blocks.append((enrich_source_label(item), heading))
        else:
            blocks.append(({"__non_mapping__": loaded, "__raw__": raw}, heading))
    return blocks

def infer_kind(data: Dict[str, Any], file_path: Path) -> str:
    file_rel = rel(file_path)
    if "schema" in data:
        return "schema"
    record_id = str(data.get("id", ""))
    # CHR- = entrée legacy ; EVENT-<SLUG> = identité canonique source-agnostique
    # (étape 6). On exclut le préfixe source-scopé legacy EVENT-S\d+- (présent
    # dans le registre des chansons), non canonique, laissé en l'état.
    if record_id.startswith("CHR-") or (
        record_id.startswith("EVENT-") and not re.match(r"EVENT-S\d+-", record_id)):
        return "chronology"
    # Gabarits à identifiant-placeholder (ex. l'exemple README
    # JD-CONCERT-YYYYMMDD-NNN) : exclus de l'ingestion comme le gabarit
    # chronologie (bloc `schema: *_template`). Sinon le placeholder est
    # ingéré comme un vrai concert (parasite de concerts.json).
    if re.search(r"(YYYYMMDD|AAAAMMJJ|YYYY-MM-DD)", record_id):
        return "template"
    if record_id.startswith("JD-CONCERT-"):
        return "concert"
    # CONCERT-<SLUG> = identité canonique source-agnostique du registre concerts
    # (étape 7b). Les entrées legacy JD-CONCERT- (joydiv) gardent leur schéma
    # propre et se réconcilient par same_as.
    if record_id.startswith("CONCERT-"):
        return "concert"
    if record_id.startswith("JD-SESSION-"):
        return "session"
    # Étape 9 : identité canonique d'acteur PERSON-<slug>
    # (registers/people/00_canonical_people.md), réconciliant la couche
    # provisoire PERS-* par `same_as`. NB : "PERSON-…".startswith("PERS-") est
    # False (5e caractère 'O', pas '-'), d'où ce test explicite et antérieur.
    if record_id.startswith("PERSON-"):
        return "person"
    if record_id.startswith("PERS-"):
        return "person"
    if record_id.startswith("CONCEPT-"):
        return "concept"
    if record_id.startswith("MYTH-"):
        return "myth"
    if record_id.startswith("MOTIF-"):
        return "motif"
    if record_id.startswith("HIST-"):
        return "quote_batch"
    if "RULES" in record_id or "rules" in data:
        return "rules"
    if "song" in data:
        return "song"
    if data.get("type_unite") == "source" or (re.fullmatch(r"S\d+", record_id) and data.get("source_label")):
        return "source"
    # Parité avec le loader runtime (dynamic-registers.js : `id.startsWith('CIT-')
    # || id.includes('-Q')`). Le préfixe CIT- et l'infixe -CIT- (formes
    # S\d+-CIT-, CIT-S\d+-…) désignent une citation au même titre que -Q. Sans
    # cela, les conteneurs `citations:` éclatés (étape 8a) produisaient des
    # records CIT-* classés `unknown` et omis de quotes.json, alors que la page
    # les affichait — divergence build/loader.
    if "-Q" in record_id or "-CIT-" in record_id or record_id.startswith("CIT-") or "citations_exactes" in file_rel:
        return "quote"
    if record_id.startswith("S") and "-" in record_id:
        return "atom"
    if not record_id and ("README.md" in file_rel or "coverage" in data or "chapters" in data or "source_id" in data or "source_label" in data):
        return "metadata"
    if not record_id and file_rel.startswith("registers/"):
        return "template"
    return "unknown"


# --------------------------------------------------------------------------- #
# Normalisation structurelle du type d'unité `quote` (étape 8b-1, backbone).
# --------------------------------------------------------------------------- #
# Dérive — SANS renommer d'id ni réécrire les fichiers source — les champs
# canoniques du backbone dans l'enregistrement exporté. L'identité reste
# source+ordinal (S\d+-Q, S\d+-CIT-, CIT-, HIST-). L'attribution et le split
# fin paraphrase/concept relèvent de 8b-2 et ne sont PAS touchés ici.
QUOTE_VERBATIM_FIELDS = ("citation", "citation_directe", "citation_originale", "passage", "quote")
QUOTE_TEXT_FALLBACK_FIELDS = (
    "texte", "resume", "usage_livre", "usage_recommande", "traduction_de_travail",
    "traduction_editoriale_fr", "traduction_litterale_fr", "usage", "contexte",
)
QUOTE_PAGE_FIELDS = ("page_pdf", "pages_pdf", "pages", "page_print", "pages_livre", "pagination", "page")
QUOTE_PAGE_PLACEHOLDERS = {"", "a_completer", "a_verifier", "a_reverifier", "inconnue"}
# Repli des libellés de langue vers les codes contrôlés (en/fr/de/it).
QUOTE_LANG_NORMALISATION = {
    "anglais": "en", "anglaise": "en", "english": "en",
    "francais": "fr", "français": "fr", "french": "fr",
    "italien": "it", "italienne": "it", "italian": "it", "italiano": "it",
    "allemand": "de", "allemande": "de", "german": "de", "deutsch": "de",
}

def _quote_first_nonempty(data: Dict[str, Any], fields: Iterable[str]) -> Optional[Any]:
    """1er champ de texte exploitable parmi `fields`.

    Ne retient qu'un **texte** : ignore les booléens (certains records utilisent
    `citation_directe: true|false` comme drapeau, pas comme corps) et les valeurs
    vides ; pour une liste, retient le 1er élément chaîne non vide.
    """
    for key in fields:
        value = data.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, str):
            if value.strip():
                return value
            continue
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    return item
            continue
        if value not in (None, "", [], {}):
            return value
    return None

def _quote_has_real_page(data: Dict[str, Any]) -> bool:
    for key in QUOTE_PAGE_FIELDS:
        value = data.get(key)
        if value not in (None, "", [], {}) and str(value).strip() not in QUOTE_PAGE_PLACEHOLDERS:
            return True
    statut = data.get("statut") or data.get("statut_verification")
    if isinstance(statut, dict):
        for key in ("pagination_pdf", "pagination_papier", "page_pdf"):
            value = statut.get(key)
            if value not in (None, "") and str(value).strip() not in QUOTE_PAGE_PLACEHOLDERS:
                return True
    return False

# --- 8b-2 : dénormalisation de l'attribution (rôles texte ; arête PERSON- = étape 9) ---
QUOTE_ATTR_RAW_FIELDS = ("auteur", "source_auteur")
# Chaîne d'attribution « X (cité·e / rapporté·e / mobilisé·e par|dans Y) » —
# incl. forme parenthétique. X = témoin (locuteur), Y = rapporteur.
_QUOTE_CHAIN_RE = re.compile(
    r"^[(\[]?\s*(?P<x>.+?)\s*[,;]?\s*[(\[]?\s*"
    r"(?:cit[ée]e?s?|rapport[ée]e?s?|mobilis[ée]e?s?|repris[e]?|évoqu[ée]e?s?)\s+"
    r"(?:par|dans|via)\s+"
    r"(?P<y>.+?)\s*[)\].]?\s*$",
    re.IGNORECASE,
)
# Marqueurs de chaîne NON parsables par le parseur ci-dessus (formes mixtes
# « d'après », « selon », « / »…) : à FLAGGER plutôt qu'à deviner ou rabattre
# par défaut sur la narration.
_QUOTE_CHAIN_MARKER_RE = re.compile(
    r"cit[ée]|rapport[ée]|mobilis[ée]|repris|évoqu[ée]|d[’']apr[èe]s|selon|/| via ",
    re.IGNORECASE,
)
# « X dans l'entretien / le documentaire Y » (sans verbe de citation) : X est le
# témoin (locuteur), le reste est le contexte/rapporteur — à dégager du locuteur.
_QUOTE_CONTEXT_RE = re.compile(r"^(?P<x>.+?)\s+dans\s+(?:l['’]|le |la |les )(?P<y>.+)$", re.IGNORECASE)
# Forme participe « X rapportant / citant Y » : rôles INVERSES — Y est le témoin
# (locuteur), X le rapporteur.
_QUOTE_REPORTING_RE = re.compile(
    r"^(?P<reporter>.+?)\s+(?:rapport[ae]nt|citant|évoquant)\s+(?P<x>.+?)\s*$",
    re.IGNORECASE,
)

def _quote_tokens(value: Optional[str]) -> set:
    return set(re.findall(r"[a-zà-ÿ]{4,}", (value or "").lower()))

def _quote_source_author(source_id: Any) -> Optional[str]:
    ensure_source_labels_loaded()
    label = SOURCE_LABELS.get(str(source_id or ""))
    return label["auteur"] if label else None

def _derive_quote_attribution(data: Dict[str, Any]) -> bool:
    """Sépare le champ d'attribution conflé en rôles (valeurs texte) :
    `auteur_source` (qui a consigné), `locuteur` (qui a énoncé), `rapporteur`
    (intermédiaire « cité par »). N'écrit AUCUNE arête `PERSON-` (étape 9).
    Renvoie `has_named_speaker` (témoin nommé distinct), qui pilote le split
    paraphrase/concept. Marque `attribution_a_arbitrer` les conflations ambiguës.
    """
    source_author = _quote_source_author(data.get("source_id"))
    if source_author and not data.get("auteur_source"):
        data["auteur_source"] = source_author
    raw = None
    for field in QUOTE_ATTR_RAW_FIELDS:
        value = data.get(field)
        if isinstance(value, str) and value.strip():
            raw = value.strip()
            break
    if raw and not data.get("auteur_origine"):
        data["auteur_origine"] = raw

    locuteur = None
    rapporteur = None
    named = False
    clean = lambda s: s.strip(" (),; ").strip()

    via = data.get("via")
    if isinstance(via, str) and via.strip():
        rapporteur = clean(via)

    if isinstance(data.get("locuteur"), str) and data["locuteur"].strip():
        locuteur = clean(data["locuteur"]); named = True
    elif isinstance(data.get("auteur_cite"), str) and data["auteur_cite"].strip():
        locuteur = clean(data["auteur_cite"]); named = True
    elif raw:
        match = _QUOTE_CHAIN_RE.match(raw)
        reporting = _QUOTE_REPORTING_RE.match(raw) if not match else None
        if match:
            # « X cité / rapporté par Y » → locuteur = X (témoin), rapporteur = Y.
            locuteur = clean(match.group("x")); named = True
            rapporteur = rapporteur or clean(match.group("y"))
        elif reporting:
            # « X rapportant Y » → locuteur = Y (témoin), rapporteur = X.
            locuteur = clean(reporting.group("x")); named = True
            rapporteur = rapporteur or clean(reporting.group("reporter"))
        elif _QUOTE_CHAIN_MARKER_RE.search(raw):
            # Forme mixte non parsable (« A d'après B », « A / B selon… ») : ne
            # PAS rabattre sur la narration — flagger pour arbitrage manuel.
            locuteur = "anonyme"
            data["attribution_a_arbitrer"] = True
        elif source_author and not (_quote_tokens(raw) - _quote_tokens(source_author)):
            # Narration STRICTE : une fois toute clause « cité/rapporté par »
            # écartée, le raw EST l'auteur de la source seul (aucun jeton-nom
            # distinct ne subsiste) → pas de témoin distinct.
            locuteur = source_author
        else:
            context = _QUOTE_CONTEXT_RE.match(raw)
            if context:
                # « X dans l'entretien Y » : témoin X dégagé, contexte → rapporteur.
                locuteur = clean(context.group("x")); named = True
                rapporteur = rapporteur or clean(context.group("y"))
                data["attribution_a_arbitrer"] = True
            else:
                locuteur = raw; named = True
                if re.search(r"\bet\b|;|&|,| du | de l", raw):
                    data["attribution_a_arbitrer"] = True  # multi-noms / forme ambiguë
    if locuteur is None:
        locuteur = "anonyme"

    if not data.get("locuteur"):
        data["locuteur"] = locuteur
    if rapporteur and not data.get("rapporteur"):
        data["rapporteur"] = rapporteur
    return named

def normalize_quote_record(data: Dict[str, Any]) -> Dict[str, Any]:
    """Matérialise le backbone `quote` (8b-1) + la curation de jugement (8b-2).

    Backbone (8b-1) : `kind`, `texte` (1er champ dispo ; sentinelle
    ``"(non transcrit)"`` pour les fiches-pointeur), `page` (``"inconnue"`` si
    aucun localisateur réel), `source_id` recouvré depuis l'id si absent.

    Curation 8b-2 (valeurs texte, dérivées — pas de réécriture source, pas
    d'arête `PERSON-`) :
    - attribution dénormalisée en rôles `auteur_source` / `locuteur` /
      `rapporteur` (cf. `_derive_quote_attribution`) ;
    - `type` ∈ {``verbatim``, ``paraphrase``, ``concept``} : verbatim si champ
      verbatim ; sinon paraphrase si témoin nommé (énoncé attribué reformulé),
      sinon concept (usage conceptuel) — `concept` est **flaggé**
      `migration_concept_register` (migration différée, NON déplacé ici) ;
    - résidus flaggés : `texte_pointeur` (sentinelles, transcription différée),
      `page == "inconnue"` (sourçage différé).
    """
    if not isinstance(data, dict):
        return data
    data.setdefault("kind", "quote")
    # Récupère le source_id encodé dans l'id (CIT-S65-001 → S65 ; S41-Q007 → S41 ;
    # S37-CIT-001 → S37) quand le champ manque — recouvrement, pas fabrication.
    if not data.get("source_id"):
        match = re.match(r"(?:CIT-)?(S\d+)\b", str(data.get("id", "")))
        if match:
            data["source_id"] = match.group(1)
    verbatim = _quote_first_nonempty(data, QUOTE_VERBATIM_FIELDS)
    if data.get("texte") in (None, "", [], {}):
        texte = verbatim if verbatim is not None else _quote_first_nonempty(data, QUOTE_TEXT_FALLBACK_FIELDS)
        data["texte"] = texte if texte is not None else "(non transcrit)"
    legacy_type = data.get("type")
    if legacy_type not in (None, "", "verbatim", "non_verbatim", "paraphrase", "concept"):
        data.setdefault("type_legacy", legacy_type)
    # Attribution (8b-2) — détermine le témoin nommé, pilote le split de type.
    named_speaker = _derive_quote_attribution(data)
    sentinel = data.get("texte") == "(non transcrit)"
    if verbatim is not None:
        data["type"] = "verbatim"
    elif sentinel:
        data["texte_pointeur"] = True
        data["type"] = "verbatim" if named_speaker else "concept"
    else:
        data["type"] = "paraphrase" if named_speaker else "concept"
    if data["type"] == "concept":
        data["migration_concept_register"] = True
        # Borderline : énoncé analytique de l'auteur de la source (narration) —
        # arbitrage paraphrase (énoncé reformulé de l'auteur) vs concept (usage
        # conceptuel). Les concepts « purs » (note éditoriale, terme, sans
        # locuteur) ne sont PAS flaggés.
        if not sentinel and data.get("locuteur") and data.get("locuteur") == data.get("auteur_source"):
            data["type_a_arbitrer"] = True
    if not _quote_has_real_page(data):
        data["page"] = "inconnue"
    langue = data.get("langue_originale")
    if isinstance(langue, str) and langue.strip().lower() in QUOTE_LANG_NORMALISATION:
        data["langue_originale"] = QUOTE_LANG_NORMALISATION[langue.strip().lower()]
    return data

def validate_record(kind: str, data: Dict[str, Any], file_path: Path) -> List[Diagnostic]:
    file_rel = rel(file_path)
    record_id = str(data.get("id") or data.get("song") or "") or None
    diagnostics: List[Diagnostic] = []
    if "__parse_error__" in data:
        return [Diagnostic("error", file_rel, f"YAML parse error: {data['__parse_error__']}", None)]
    if "__non_mapping__" in data:
        return [Diagnostic("warning", file_rel, "YAML block is not a mapping/object", None)]
    if kind == "unknown":
        diagnostics.append(Diagnostic("warning", file_rel, "Unable to infer documentary kind", record_id))
        return diagnostics
    if kind in {"schema", "source", "concept", "myth", "motif", "quote_batch", "rules", "metadata", "template", "concert", "session"}:
        return diagnostics
    if kind != "song" and not data.get("id"):
        diagnostics.append(Diagnostic("warning", file_rel, "Missing id", record_id))
    for message in validate_against_schema(kind, data):
        diagnostics.append(Diagnostic("warning", file_rel, message, record_id))
    return diagnostics

def parse_repository() -> Tuple[List[ParsedRecord], List[Diagnostic]]:
    ensure_source_labels_loaded()
    records: List[ParsedRecord] = []
    diagnostics: List[Diagnostic] = []
    seen_ids: Dict[str, str] = {}
    for path in iter_markdown_files():
        for data, heading in extract_yaml_blocks(path):
            kind = infer_kind(data, path)
            if kind == "quote":
                normalize_quote_record(data)
            diagnostics.extend(validate_record(kind, data, path))
            if kind == "schema":
                continue
            record_id = str(data.get("id") or data.get("song") or "")
            if not record_id:
                record_id = f"NO_ID::{rel(path)}::{len(records) + 1}"
            if kind not in {"source", "metadata", "template"}:
                if record_id in seen_ids:
                    diagnostics.append(Diagnostic("error", rel(path), f"Duplicate id also found in {seen_ids[record_id]}", record_id))
                else:
                    seen_ids[record_id] = rel(path)
            records.append(ParsedRecord(kind=kind, id=record_id, file=rel(path), heading=heading, data=data))
    return records, diagnostics

def records_by_kind(records: List[ParsedRecord], kind: str) -> List[ParsedRecord]:
    return [record for record in records if record.kind == kind]

def make_json_safe(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): make_json_safe(val) for key, val in value.items()}
    if isinstance(value, list):
        return [make_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [make_json_safe(item) for item in value]
    return value

def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(make_json_safe(payload), ensure_ascii=False, indent=2, sort_keys=False), encoding="utf-8")

def flatten_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return json.dumps(make_json_safe(value), ensure_ascii=False)

def write_csv(path: Path, records: List[ParsedRecord], preferred_fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["kind", "id", "file", "heading"] + preferred_fields
    extra_keys: List[str] = []
    for record in records:
        for key in record.data.keys():
            if key not in preferred_fields and key not in {"id"} and key not in extra_keys:
                extra_keys.append(key)
    fields += extra_keys
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = {"kind": record.kind, "id": record.id, "file": record.file, "heading": record.heading or ""}
            for key in fields:
                if key not in row:
                    row[key] = flatten_value(record.data.get(key))
            writer.writerow(row)

def label_for_source(source_id: str, data: Dict[str, Any]) -> Dict[str, str]:
    ensure_source_labels_loaded()
    source_id = normalize_identifier(source_id)
    if source_id in SOURCE_LABELS:
        return SOURCE_LABELS[source_id]
    return {
        "label": data.get("source_label", source_id),
        "auteur": data.get("auteur", "Inconnu"),
        "titre": data.get("titre", source_id),
        "annee": data.get("source_year", ""),
    }

def build_source_registry(records: List[ParsedRecord]) -> List[Dict[str, Any]]:
    ensure_source_labels_loaded()
    grouped: Dict[str, Dict[str, Any]] = {}
    for record in records:
        data = record.data or {}
        ids: List[str] = []
        if data.get("source_id"):
            ids.append(data["source_id"])
        if isinstance(data.get("sources"), list):
            ids.extend([s for s in data["sources"] if isinstance(s, str) and re.match(r"^S\d+$", s)])
        for raw_source_id in ids:
            source_id = normalize_identifier(raw_source_id)
            label = label_for_source(source_id, data)
            entry = grouped.setdefault(source_id, {
                "source_id": source_id,
                "source_label": label.get("label", source_id),
                "auteur": label.get("auteur", data.get("auteur", "Inconnu")),
                "titre": label.get("titre", data.get("titre", source_id)),
                "annee": label.get("annee", data.get("source_year", "")),
                "records": 0,
                "atoms": 0,
                "quotes": 0,
                "chronology": 0,
                "files": set(),
            })
            entry["records"] += 1
            entry["files"].add(record.file)
            if record.kind == "atom": entry["atoms"] += 1
            if record.kind == "quote": entry["quotes"] += 1
            if record.kind == "chronology": entry["chronology"] += 1
    result = []
    for entry in grouped.values():
        entry["files"] = sorted(entry["files"])
        result.append(entry)
    return sorted(result, key=lambda e: e["source_id"])

def source_ids_from_registry() -> Dict[str, Dict[str, Any]]:
    declared: Dict[str, Dict[str, Any]] = {}
    for entry in load_source_registry_entries():
        normalized = normalize_source_entry(entry)
        if not normalized:
            continue
        source_id, label = normalized
        declared[source_id] = {
            "source_id": source_id,
            "source_label": label.get("label", source_id),
            "auteur": label.get("auteur", "Inconnu"),
            "titre": label.get("titre", source_id),
            "annee": label.get("annee", ""),
            "statut": entry.get("statut", ""),
            "usage": entry.get("usage", ""),
        }
    return declared

def source_ids_from_records(records: List[ParsedRecord]) -> List[str]:
    used = set()
    for record in records:
        data = record.data or {}
        if isinstance(data.get("source_id"), str):
            used.add(normalize_identifier(data["source_id"]))
        if isinstance(data.get("sources"), list):
            for source in data["sources"]:
                if isinstance(source, str) and re.match(r"^S\d+$", source):
                    used.add(normalize_identifier(source))
    return sorted(used)

def weak_source_labels(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    weak: List[Dict[str, Any]] = []
    for source in sources:
        source_id = source.get("source_id", "")
        label = source.get("source_label", "")
        auteur = source.get("auteur", "")
        titre = source.get("titre", "")
        if label == source_id or auteur == "Inconnu" or titre == source_id:
            weak.append({
                "source_id": source_id,
                "source_label": label,
                "auteur": auteur,
                "titre": titre,
            })
    return weak

def build_diagnostics_payload(records: List[ParsedRecord], diagnostics: List[Diagnostic], sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for record in records:
        counts[record.kind] = counts.get(record.kind, 0) + 1

    declared = source_ids_from_registry()
    used_ids = source_ids_from_records(records)
    used_set = set(used_ids)
    declared_set = set(declared.keys())
    exported_set = {source.get("source_id") for source in sources}

    errors = [diag for diag in diagnostics if diag.level == "error"]
    warnings = [diag for diag in diagnostics if diag.level == "warning"]
    declared_but_unused = [declared[source_id] for source_id in sorted(declared_set - used_set)]
    used_but_missing = sorted(used_set - declared_set)
    weak_labels = weak_source_labels(sources)

    status = "ok"
    if errors or used_but_missing:
        status = "error"
    elif warnings or weak_labels:
        status = "warning"

    return {
        "generated_at": resolved_generated_at(),
        "status": status,
        "summary": {
            "records_total": len(records),
            "records_by_kind": counts,
            "diagnostics_total": len(diagnostics),
            "errors": len(errors),
            "warnings": len(warnings),
            "sources_declared_in_registre_json": len(declared_set),
            "sources_used_in_records": len(used_set),
            "sources_exported": len(exported_set),
            "declared_but_unused": len(declared_but_unused),
            "used_but_missing_from_registre_json": len(used_but_missing),
            "weak_source_labels": len(weak_labels),
        },
        "controls": {
            "declared_but_unused": declared_but_unused,
            "used_but_missing_from_registre_json": used_but_missing,
            "weak_source_labels": weak_labels,
            "exported_sources": sources,
        },
        "issues": [asdict(diag) for diag in diagnostics],
    }

def write_diagnostics_markdown(path: Path, payload: Dict[str, Any]) -> None:
    summary = payload.get("summary", {})
    controls = payload.get("controls", {})
    lines = [
        "# Diagnostic du repo documentaire",
        "",
        f"Généré le : `{payload.get('generated_at', '')}`",
        "",
        f"Statut : **{payload.get('status', 'unknown')}**",
        "",
        "## Synthèse",
        "",
        f"- Enregistrements : {summary.get('records_total', 0)}",
        f"- Erreurs : {summary.get('errors', 0)}",
        f"- Avertissements : {summary.get('warnings', 0)}",
        f"- Sources déclarées dans `data/registre.json` : {summary.get('sources_declared_in_registre_json', 0)}",
        f"- Sources utilisées dans les enregistrements : {summary.get('sources_used_in_records', 0)}",
        f"- Sources exportées : {summary.get('sources_exported', 0)}",
        f"- Sources déclarées mais non utilisées : {summary.get('declared_but_unused', 0)}",
        f"- Sources utilisées mais absentes du registre : {summary.get('used_but_missing_from_registre_json', 0)}",
        f"- Libellés faibles : {summary.get('weak_source_labels', 0)}",
        "",
        "## Enregistrements par type",
        "",
    ]
    for kind, count in sorted((summary.get("records_by_kind") or {}).items()):
        lines.append(f"- {kind} : {count}")

    lines += ["", "## Sources utilisées mais absentes du registre", ""]
    missing = controls.get("used_but_missing_from_registre_json") or []
    if missing:
        lines.extend(f"- {source_id}" for source_id in missing)
    else:
        lines.append("Aucune.")

    lines += ["", "## Sources déclarées mais non utilisées", ""]
    unused = controls.get("declared_but_unused") or []
    if unused:
        for source in unused:
            lines.append(f"- {source.get('source_label', source.get('source_id', ''))} — statut : {source.get('statut', '')}")
    else:
        lines.append("Aucune.")

    lines += ["", "## Libellés faibles", ""]
    weak = controls.get("weak_source_labels") or []
    if weak:
        for source in weak:
            lines.append(f"- {source.get('source_id', '')} : {source.get('source_label', '')}")
    else:
        lines.append("Aucun.")

    lines += ["", "## Problèmes YAML / schéma", ""]
    issues = payload.get("issues") or []
    if issues:
        for issue in issues[:100]:
            record = f" [{issue.get('record_id')}]" if issue.get("record_id") else ""
            lines.append(f"- **{issue.get('level', '').upper()}** `{issue.get('file', '')}`{record} : {issue.get('message', '')}")
        if len(issues) > 100:
            lines.append(f"- … {len(issues) - 100} problèmes supplémentaires dans `diagnostics.json`.")
    else:
        lines.append("Aucun.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def build_exports(records: List[ParsedRecord], diagnostics: List[Diagnostic]) -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    atoms = records_by_kind(records, "atom")
    quotes = records_by_kind(records, "quote")
    chronology = records_by_kind(records, "chronology")
    songs = records_by_kind(records, "song")
    people = records_by_kind(records, "person")
    source_records = records_by_kind(records, "source")
    concepts = records_by_kind(records, "concept")
    myths = records_by_kind(records, "myth")
    motifs = records_by_kind(records, "motif")
    quote_batches = records_by_kind(records, "quote_batch")
    rules = records_by_kind(records, "rules")
    metadata = records_by_kind(records, "metadata")
    templates = records_by_kind(records, "template")
    concerts = records_by_kind(records, "concert")
    sessions = records_by_kind(records, "session")
    sources = build_source_registry(records)
    diagnostics_payload = build_diagnostics_payload(records, diagnostics, sources)

    write_json(EXPORT_DIR / "atoms.json", [asdict(r) for r in atoms])
    write_json(EXPORT_DIR / "quotes.json", [asdict(r) for r in quotes])
    write_json(EXPORT_DIR / "chronology.json", [asdict(r) for r in chronology])
    # songs.json is a build artifact (gitignored under exports/generated/), NOT
    # orphan: it is consumed downstream by tools/build_master_docs.py,
    # tools/audit_song_canon.py and tools/enrich_songbook_from_internal_sources.py.
    # The web app (apps/song-register/) does NOT read it — it loads the canonical
    # YAML directly. Do not remove this write without updating those consumers.
    write_json(EXPORT_DIR / "songs.json", [asdict(r) for r in songs])
    write_json(EXPORT_DIR / "people.json", [asdict(r) for r in people])
    write_json(EXPORT_DIR / "source_records.json", [asdict(r) for r in source_records])
    write_json(EXPORT_DIR / "concepts.json", [asdict(r) for r in concepts])
    write_json(EXPORT_DIR / "myths.json", [asdict(r) for r in myths])
    write_json(EXPORT_DIR / "motifs.json", [asdict(r) for r in motifs])
    write_json(EXPORT_DIR / "quote_batches.json", [asdict(r) for r in quote_batches])
    write_json(EXPORT_DIR / "rules.json", [asdict(r) for r in rules])
    write_json(EXPORT_DIR / "metadata.json", [asdict(r) for r in metadata])
    write_json(EXPORT_DIR / "templates.json", [asdict(r) for r in templates])
    write_json(EXPORT_DIR / "concerts.json", [asdict(r) for r in concerts])
    write_json(EXPORT_DIR / "sessions.json", [asdict(r) for r in sessions])
    write_json(EXPORT_DIR / "sources.json", sources)
    write_json(EXPORT_DIR / "all_records.json", [asdict(record) for record in records])
    write_json(EXPORT_DIR / "index_by_id.json", {record.id: asdict(record) for record in records})
    write_json(EXPORT_DIR / "diagnostics.json", diagnostics_payload)
    write_diagnostics_markdown(EXPORT_DIR / "diagnostics.md", diagnostics_payload)

    write_csv(EXPORT_DIR / "atoms.csv", atoms, [
        "source_id", "source_label", "source_short_title", "auteur", "titre", "pages_pdf",
        "type_unite", "concepts", "chapitres", "statut", "fiabilite", "role_argumentatif",
        "niveau_preuve", "stabilite", "importance", "risque_surinterpretation",
        "liens_interchapitres", "liens_citations", "motifs", "concepts_derives",
        "charge_emotionnelle", "nature_discursive"
    ])
    write_csv(EXPORT_DIR / "quotes.csv", quotes, ["source_id", "source_label", "citation_originale", "traduction_editoriale_fr", "page_pdf", "langue_originale", "importance"])
    write_csv(EXPORT_DIR / "chronology.csv", chronology, ["date", "precision_date", "event", "type", "location", "people", "songs", "sources", "certainty"])
    write_csv(EXPORT_DIR / "songs.csv", songs, ["song", "period", "themes", "sources", "chapters", "certainty"])
    write_csv(EXPORT_DIR / "people.csv", people, ["name", "full_name", "role", "sources", "chapters", "certainty"])
    write_csv(EXPORT_DIR / "source_records.csv", source_records, ["source_id", "source_label", "auteur", "titre", "source_year", "nature", "status", "priority"])
    write_csv(EXPORT_DIR / "concepts.csv", concepts, ["id", "nom", "name", "definition", "filiation", "niveau_consensus", "chapitres", "sources"])
    write_csv(EXPORT_DIR / "myths.csv", myths, ["id", "mythe", "name", "niveau_risque", "correction", "chapitres", "sources"])
    write_csv(EXPORT_DIR / "motifs.csv", motifs, ["id", "motif", "name", "definition", "chapitres", "sources"])
    write_csv(EXPORT_DIR / "quote_batches.csv", quote_batches, ["id", "lot", "source_file", "rows_imported", "chapitres", "statut_consolidation"])
    write_csv(EXPORT_DIR / "rules.csv", rules, ["id", "statut_consolidation", "rules"])
    write_csv(EXPORT_DIR / "metadata.csv", metadata, ["source_id", "source_label", "coverage", "chapters", "nature", "status", "priority"])
    write_csv(EXPORT_DIR / "templates.csv", templates, ["id", "name", "role", "sources", "certainty", "date", "event", "type"])
    write_csv(EXPORT_DIR / "concerts.csv", concerts, ["date", "statut", "lieu", "ville", "pays", "ere", "source", "url_detail", "atomes_lies", "notes"])
    write_csv(EXPORT_DIR / "sessions.csv", sessions, ["numero", "label", "date", "studio", "ville", "producteur", "ere", "titres", "premiere_sortie_officielle", "source", "atomes_lies"])
    source_csv_records = [ParsedRecord("source", e["source_id"], "exports/generated/sources.json", None, e) for e in sources]
    write_csv(EXPORT_DIR / "sources.csv", source_csv_records, ["source_id", "source_label", "auteur", "titre", "annee", "records", "atoms", "quotes", "chronology", "files"])
    diagnostic_csv_records = [ParsedRecord("diagnostic", f"D{idx:04d}", "exports/generated/diagnostics.json", None, asdict(diag)) for idx, diag in enumerate(diagnostics, start=1)]
    write_csv(EXPORT_DIR / "diagnostics.csv", diagnostic_csv_records, ["level", "file", "record_id", "message"])

def print_summary(records: List[ParsedRecord], diagnostics: List[Diagnostic]) -> None:
    counts: Dict[str, int] = {}
    for record in records:
        counts[record.kind] = counts.get(record.kind, 0) + 1
    print("Documentary parser summary")
    print("---------------------------")
    for kind in sorted(counts):
        print(f"{kind:12s}: {counts[kind]}")
    errors = [d for d in diagnostics if d.level == "error"]
    warnings = [d for d in diagnostics if d.level == "warning"]
    unknowns = [d for d in diagnostics if d.message == "Unable to infer documentary kind"]
    print(f"errors      : {len(errors)}")
    print(f"warnings    : {len(warnings)}")
    print(f"unknown     : {len(unknowns)}")
    print(f"exports     : {rel(EXPORT_DIR)}")
    if diagnostics:
        ordered = errors + [d for d in diagnostics if d.level != "error"]
        print("\nDiagnostics:")
        for diag in ordered[:50]:
            suffix = f" [{diag.record_id}]" if diag.record_id else ""
            print(f"- {diag.level.upper()} {diag.file}{suffix}: {diag.message}")
        if len(diagnostics) > 50:
            print(f"... {len(diagnostics) - 50} additional diagnostics written to diagnostics.json")

def main() -> int:
    parser = argparse.ArgumentParser(description="Build documentary exports from Markdown/YAML records.")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if errors are found.")
    args = parser.parse_args()
    records, diagnostics = parse_repository()
    build_exports(records, diagnostics)
    print_summary(records, diagnostics)
    if args.strict and any(d.level == "error" for d in diagnostics):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
