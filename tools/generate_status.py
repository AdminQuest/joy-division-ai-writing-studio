#!/usr/bin/env python3
"""Generate STATUS.md — machine-readable snapshot of the repo state.

Designed to be read by Claude / Claude Code at session start to avoid
re-exploring the repo from scratch.

Usage:
    python3 tools/generate_status.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTERS_DIR = ROOT / "registers"
SCHEMAS_DIR = ROOT / "schemas"
META_DIR = ROOT / "_meta"
STATUS_PATH = ROOT / "STATUS.md"

JSON_REGISTERS = {
    "Organisations": {
        "prefix": "ORG-",
        "path": REGISTERS_DIR / "orgs" / "orgs.json",
        "id_field": "org_id",
        "validator": "tools/validate_orgs.py",
    },
    "Images": {
        "prefix": "IMAGE-",
        "path": REGISTERS_DIR / "images" / "images.json",
        "id_field": "image_id",
        "validator": "tools/validate_images.py",
    },
}

YAML_REGISTERS = {
    "Chronologie": {
        "prefix": "EVENT-",
        "pattern": r"^## (EVENT-\S+)",
        "files": [REGISTERS_DIR / "chronology" / "events_canonical.md"],
        "validator": "tools/validate_chronology.py",
    },
    "Concerts": {
        "prefix": "CONCERT-",
        "pattern": r"same_as:\s*(CONCERT-\S+)",
        "files": [REGISTERS_DIR / "concerts" / "00_canonical_concerts.md"],
        "validator": "tools/validate_concerts.py",
    },
    "Acteurs": {
        "prefix": "PERSON-",
        "pattern": r"^## (PERSON-\S+)",
        "files": [REGISTERS_DIR / "people" / "00_canonical_people.md"],
        "validator": "tools/validate_people.py",
    },
    "Lieux": {
        "prefix": "PLACE-",
        "pattern": r"id:\s*(PLACE-\S+)",
        "files": sorted(REGISTERS_DIR.glob("places/*.md")),
        "validator": "tools/validate_places.py",
    },
    "Chansons": {
        "prefix": "JD-SONG-",
        "pattern": r"id:\s*(JD-SONG-\d+)",
        "files": [REGISTERS_DIR / "songs" / "00_canonical_joy_division_songs.md"],
        "validator": "tools/validate_songs.py",
    },
    "Citations": {
        "prefix": "QUOTE-",
        "pattern": None,
        "files": [],
        "validator": "tools/validate_quotes.py",
        "count_from_attribution": REGISTERS_DIR / "relations" / "attribution_edges.json",
    },
}


def git_short_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=ROOT, timeout=10
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def git_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=ROOT, timeout=10
        )
        return result.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def run_validator(validator_path: str) -> tuple[bool, str]:
    full_path = ROOT / validator_path
    if not full_path.exists():
        return False, "fichier absent"
    try:
        result = subprocess.run(
            [sys.executable, str(full_path)],
            capture_output=True, text=True, cwd=ROOT, timeout=60
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if result.returncode == 0:
            error_match = re.search(r"errors\s*:\s*(\d+)", stdout)
            n_errors = error_match.group(1) if error_match else "0"
            return True, f"PASS ({n_errors} erreurs)"
        else:
            first_error = ""
            for line in (stderr or stdout).splitlines():
                if "ERROR" in line:
                    first_error = line.strip()[:120]
                    break
            return False, first_error or f"exit {result.returncode}"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as exc:
        return False, str(exc)[:100]


def load_json_register(cfg: dict) -> dict:
    info = {
        "total": 0, "public": 0, "private": 0,
        "last_verified_min": None, "last_verified_max": None,
    }
    try:
        data = json.loads(cfg["path"].read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return info
        info["total"] = len(data)
        for entry in data:
            gate = entry.get("gate", "public")
            if gate == "public":
                info["public"] += 1
            elif gate == "private":
                info["private"] += 1
            lv = entry.get("last_verified")
            if lv:
                if info["last_verified_min"] is None or lv < info["last_verified_min"]:
                    info["last_verified_min"] = lv
                if info["last_verified_max"] is None or lv > info["last_verified_max"]:
                    info["last_verified_max"] = lv
    except Exception as exc:
        print(f"WARNING: {cfg['path']}: {exc}", file=sys.stderr)
    return info


def count_yaml_register(cfg: dict) -> int:
    if cfg.get("count_from_attribution"):
        try:
            data = json.loads(cfg["count_from_attribution"].read_text(encoding="utf-8"))
            return data.get("stats", {}).get("n_quotes", 0)
        except Exception:
            return 0

    pattern = cfg.get("pattern")
    if not pattern:
        return 0
    regex = re.compile(pattern, re.MULTILINE)
    ids = set()
    for fpath in cfg.get("files", []):
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8")
            for m in regex.finditer(text):
                ids.add(m.group(1))
        except Exception:
            continue
    return len(ids)


def load_schemas() -> list[dict]:
    schemas = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            title = data.get("title", path.name)
            schemas.append({
                "file": path.name,
                "title": title,
            })
        except Exception:
            schemas.append({"file": path.name, "title": path.name})
    return schemas


def load_drift_sentinels() -> dict[str, str]:
    sentinels = {}
    for name, cfg in JSON_REGISTERS.items():
        try:
            data = json.loads(cfg["path"].read_text(encoding="utf-8"))
            if isinstance(data, list) and data:
                ds = data[0].get("drift_sentinel", "?")
                sentinels[name] = ds
        except Exception:
            sentinels[name] = "?"
    return sentinels


def load_known_gaps() -> str:
    gaps_path = META_DIR / "known_gaps.md"
    if gaps_path.exists():
        content = gaps_path.read_text(encoding="utf-8").strip()
        if content:
            return content
    return "Aucune lacune documentee."


def count_hub_registers() -> int:
    hub_path = ROOT / "index.html"
    if not hub_path.exists():
        return 0
    text = hub_path.read_text(encoding="utf-8")
    return len(re.findall(r'class="card-cta"', text))


def generate() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sha = git_short_sha()
    branch = git_branch()

    lines = [
        "# Status — Joy Division AI Writing Studio",
        f"> Genere automatiquement le {now} — ne pas editer manuellement.",
        "",
        "## Registres",
        "",
        "| Registre | Prefixe | Entrees | Public | Prive | Validateur | Dernier verifie |",
        "|----------|---------|---------|--------|-------|------------|-----------------|",
    ]

    validator_results: list[tuple[str, bool, str]] = []

    for name, cfg in JSON_REGISTERS.items():
        info = load_json_register(cfg)
        ok, msg = run_validator(cfg["validator"])
        validator_results.append((cfg["validator"], ok, msg))
        status_icon = "pass" if ok else "FAIL"
        lv = info["last_verified_max"] or "—"
        lines.append(
            f"| {name} | `{cfg['prefix']}` | {info['total']} "
            f"| {info['public']} | {info['private']} "
            f"| {status_icon} | {lv} |"
        )

    for name, cfg in YAML_REGISTERS.items():
        count = count_yaml_register(cfg)
        ok, msg = run_validator(cfg["validator"])
        validator_results.append((cfg["validator"], ok, msg))
        status_icon = "pass" if ok else "FAIL"
        lines.append(
            f"| {name} | `{cfg['prefix']}` | {count} "
            f"| — | — "
            f"| {status_icon} | — |"
        )

    lines.append("")
    lines.append("## Validateurs")
    lines.append("")
    for vpath, ok, msg in validator_results:
        icon = "pass" if ok else "FAIL"
        lines.append(f"- `{vpath}` : {icon} — {msg}")

    lines.append("")
    lines.append("## Schemas")
    lines.append("")
    sentinels = load_drift_sentinels()
    schemas = load_schemas()
    for s in schemas:
        sentinel_note = ""
        for reg_name, ds in sentinels.items():
            if JSON_REGISTERS[reg_name]["prefix"].lower().replace("-", "") in s["file"].lower():
                sentinel_note = f" — drift_sentinel {ds}"
                break
        lines.append(f"- `{s['file']}`{sentinel_note}")

    lines.append("")
    lines.append("## Lacunes connues")
    lines.append("")
    lines.append(load_known_gaps())

    lines.append("")
    lines.append("## Prochaine etape")
    lines.append("")
    lines.append("Step 12 — Cross-registres profond")

    lines.append("")
    lines.append("## Metadata")
    lines.append("")
    lines.append("- Repo : joy-division-ai-writing-studio")
    lines.append(f"- Branche du snapshot : {branch}")
    lines.append(f"- Reference git observee avant generation : {sha}")
    lines.append(f"- Genere par : tools/generate_status.py")
    lines.append(
        "- Statut : snapshot genere avant commit ; le commit contenant ce "
        "fichier peut donc etre posterieur."
    )
    lines.append(
        "- Note : cette reference designe l'etat lu par le generateur, "
        "non le commit final contenant STATUS.md."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    content = generate()
    STATUS_PATH.write_text(content, encoding="utf-8")
    print(f"STATUS.md generated ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
