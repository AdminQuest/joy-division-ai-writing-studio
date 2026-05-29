#!/usr/bin/env python3
"""Validate the song register against schemas/song.schema.json.

Models tools/validate_places.py. Replicates the relevant slice of the runtime
pipeline of apps/lib/dynamic-registers.js:
  1. parse every YAML block under registers/songs/**.md
  2. collect items from `songs:` containers (and standalone song blocks)
  3. classify each record:
       - CANONICAL  (type_unite == "song", canonical_song is True, exclude not
         True) -> validated strictly against the JSON Schema (Draft 2020-12,
         FormatChecker active). These are the 51 cross-repo join records.
       - EXCLUDED   (exclude is True) -> light check only (id present, song
         title present, exclusion_reason present). Not held to the canonical
         contract.
       - MENTION / other -> counted, not strictly validated (heterogeneous
         documentary corpus: live contexts, sessions, source mentions, etc.).
  4. report counts and the list of invalid records with their errors.

`id` (JD-SONG-NNN) and `slug` are the cross-repo join keys with
joy-division-studio-private; the schema enforces their strict patterns.

Usage: python3 tools/validate_songs.py
Exit code 1 if any YAML block fails to parse, any canonical record is invalid,
or any excluded record fails its light check.
"""
import glob
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas" / "song.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

YAML_BLOCK = re.compile(r"```yaml\s*(.*?)\s*```", re.S)


def is_canonical(record: dict) -> bool:
    return (
        record.get("type_unite") == "song"
        and record.get("canonical_song") is True
        and record.get("exclude") is not True
    )


def is_excluded(record: dict) -> bool:
    return record.get("exclude") is True


CANONICAL_HINT = re.compile(r"^\s*-?\s*canonical_song:\s*true\b", re.M)


def collect_song_records():
    """Collect song records and YAML parse errors under registers/songs/.

    Returns (records, parse_errors) where:
      - records is a list of (record_dict, rel_path) for every song-shaped block
        (a `songs:` container or a standalone JD-SONG-* block; document headers
        are skipped);
      - parse_errors is a list of (rel_path, first_line, looks_canonical, message)
        for every YAML block that fails to parse. Parse errors are NOT swallowed
        silently and are NOT downgraded to warnings: ANY block that fails to
        parse makes the whole run fail (see main()). A malformed block — whether
        it looks canonical or is "only" a mention — can never slip past
        validation unnoticed, because an unparseable block is invisible to schema
        validation and could hide an invalid record (e.g. an unquoted colon in a
        title). `looks_canonical` is retained purely to label the report.
    """
    records = []
    parse_errors = []
    for path in sorted(glob.glob(str(ROOT / "registers" / "songs" / "**" / "*.md"), recursive=True)):
        rel = path.replace(str(ROOT) + "/", "")
        for block in YAML_BLOCK.findall(Path(path).read_text(encoding="utf-8")):
            try:
                data = yaml.safe_load(block)
            except yaml.YAMLError as exc:
                first_line = next((ln.strip() for ln in block.splitlines() if ln.strip()), "")
                looks_canonical = bool(CANONICAL_HINT.search(block))
                parse_errors.append((rel, first_line, looks_canonical, str(exc).splitlines()[0]))
                continue
            if not isinstance(data, dict):
                continue
            if isinstance(data.get("songs"), list):
                items = data["songs"]
            elif str(data.get("id", "")).startswith("JD-SONG-"):
                items = [data]
            else:
                # document header / registry metadata block -> skip
                continue
            for item in items:
                if isinstance(item, dict):
                    records.append((item, rel))
    return records, parse_errors


def light_check_excluded(record: dict):
    errors = []
    if not str(record.get("id", "")).startswith("JD-SONG-"):
        errors.append("excluded record without a JD-SONG-* id")
    if not record.get("song"):
        errors.append("excluded record without a `song` title")
    if not record.get("exclusion_reason"):
        errors.append("excluded record without an `exclusion_reason`")
    return errors


def main() -> int:
    records, parse_errors = collect_song_records()

    canonical = [(r, rel) for r, rel in records if is_canonical(r)]
    excluded = [(r, rel) for r, rel in records if is_excluded(r)]
    mentions = [(r, rel) for r, rel in records if not is_canonical(r) and not is_excluded(r)]

    invalid_canonical = []
    for record, rel in canonical:
        errors = sorted(VALIDATOR.iter_errors(record), key=str)
        if errors:
            invalid_canonical.append((record.get("id"), rel, [e.message for e in errors]))

    invalid_excluded = []
    for record, rel in excluded:
        errors = light_check_excluded(record)
        if errors:
            invalid_excluded.append((record.get("id"), rel, errors))

    distinct_ids = {r.get("id") for r, _ in canonical}

    print(f"Song records collected (registers/songs/)   : {len(records)}")
    print(f"  canonical (strict schema)                  : {len(canonical)}")
    print(f"  excluded  (light check)                    : {len(excluded)}")
    print(f"  mentions / other (counted, not validated)  : {len(mentions)}")
    print(f"Distinct canonical ids                        : {len(distinct_ids)}")
    print(f"YAML blocks that failed to parse (all fatal)  : {len(parse_errors)}")
    print(f"Canonical valid against schema                : {len(canonical) - len(invalid_canonical)}/{len(canonical)}")
    print(f"Excluded valid against light check            : {len(excluded) - len(invalid_excluded)}/{len(excluded)}")

    if parse_errors:
        # Never silent, never a warning: every malformed block is fatal. An
        # unparseable block is invisible to schema validation, so a "mention"
        # that fails to parse could just as well be hiding an invalid canonical
        # record. The only safe policy is to fail on any parse error.
        print(f"\nYAML PARSE ERRORS ({len(parse_errors)}) — all fatal:")
        for rel, first_line, looks_canonical, msg in parse_errors:
            hint = " [looks canonical]" if looks_canonical else ""
            print(f"  YAML parse error in {rel}: {msg}{hint}")
            print(f"       first line: {first_line}")

    if invalid_canonical:
        print(f"\nINVALID CANONICAL ({len(invalid_canonical)}):")
        for sid, rel, msgs in invalid_canonical:
            print(f"  {sid}  ({rel})")
            for m in msgs:
                print(f"       - {m}")

    if invalid_excluded:
        print(f"\nINVALID EXCLUDED ({len(invalid_excluded)}):")
        for sid, rel, msgs in invalid_excluded:
            print(f"  {sid}  ({rel})")
            for m in msgs:
                print(f"       - {m}")

    if parse_errors or invalid_canonical or invalid_excluded:
        return 1

    print("\nAll YAML blocks parse; all canonical song records are valid; "
          "excluded records pass the light check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
