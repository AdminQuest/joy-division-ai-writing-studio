#!/usr/bin/env python3
"""
Local Songbook editor server.

Runs a local-only HTTP server that can read and write the private lyrics workspace
pointed to by SONGBOOK_LYRICS_ROOT. The app is not designed for public hosting.

Usage:
  export SONGBOOK_LYRICS_ROOT="/path/to/private/songbook_lyrics"
  python3 tools/serve_local_songbook.py

Open:
  http://localhost:8765/apps/local-songbook-editor/
"""

from __future__ import annotations

import json
import mimetypes
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOT = Path(os.environ.get("SONGBOOK_LYRICS_ROOT", ROOT / "local_data" / "songbook_lyrics")).expanduser()
HOST = "127.0.0.1"
PORT = int(os.environ.get("SONGBOOK_EDITOR_PORT", "8765"))


def safe_slug(slug: str) -> str:
    if not slug or "/" in slug or ".." in slug or slug.startswith("."):
        raise ValueError("Invalid slug")
    return slug


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def list_songs():
    items = []
    if PRIVATE_ROOT.exists():
        for folder in sorted(p for p in PRIVATE_ROOT.iterdir() if p.is_dir()):
            notes_path = folder / "editorial_notes.json"
            full_path = folder / "full_lyrics.txt"
            data = read_json(notes_path, {})
            items.append({
                "slug": folder.name,
                "song_id": data.get("song_id", ""),
                "canonical_song": data.get("canonical_song", folder.name),
                "verification_status": data.get("verification_status", ""),
                "has_full_lyrics": full_path.exists() and full_path.read_text(encoding="utf-8", errors="ignore").strip() != "",
                "notes_path": str(notes_path),
                "full_lyrics_path": str(full_path),
            })
    return items


def song_payload(slug: str):
    slug = safe_slug(slug)
    folder = PRIVATE_ROOT / slug
    notes_path = folder / "editorial_notes.json"
    full_path = folder / "full_lyrics.txt"
    notes = read_json(notes_path, {})
    lyrics = full_path.read_text(encoding="utf-8", errors="ignore") if full_path.exists() else ""
    return {
        "slug": slug,
        "private_root": str(PRIVATE_ROOT),
        "full_lyrics": lyrics,
        "notes": notes,
    }


def write_song(slug: str, payload: dict):
    slug = safe_slug(slug)
    folder = PRIVATE_ROOT / slug
    folder.mkdir(parents=True, exist_ok=True)
    notes = payload.get("notes") or {}
    lyrics = payload.get("full_lyrics")
    if lyrics is not None:
        (folder / "full_lyrics.txt").write_text(str(lyrics), encoding="utf-8")
    (folder / "editorial_notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "slug": slug}


def run_sync(skip_build: bool = True):
    cmd = [sys.executable, "tools/songbook_sync.py", "--skip-pull"]
    if skip_build:
        cmd.append("--skip-build")
    cmd.append("--diagnostics")
    env = os.environ.copy()
    env["SONGBOOK_LYRICS_ROOT"] = str(PRIVATE_ROOT)
    proc = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)
    return {"ok": proc.returncode == 0, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/config":
            return self.send_json({"private_root": str(PRIVATE_ROOT), "repo_root": str(ROOT)})
        if parsed.path == "/api/songs":
            return self.send_json({"songs": list_songs()})
        if parsed.path == "/api/song":
            slug = parse_qs(parsed.query).get("slug", [""])[0]
            try:
                return self.send_json(song_payload(slug))
            except Exception as exc:
                return self.send_json({"error": str(exc)}, 400)

        rel = parsed.path.lstrip("/") or "apps/local-songbook-editor/index.html"
        if rel == "apps/local-songbook-editor/":
            rel = "apps/local-songbook-editor/index.html"
        target = (ROOT / rel).resolve()
        if not str(target).startswith(str(ROOT)) or not target.exists() or target.is_dir():
            self.send_response(404)
            self.end_headers()
            return
        mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        raw = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(body)
        except Exception as exc:
            return self.send_json({"error": f"Invalid JSON: {exc}"}, 400)
        if parsed.path == "/api/song":
            slug = parse_qs(parsed.query).get("slug", [""])[0]
            try:
                return self.send_json(write_song(slug, data))
            except Exception as exc:
                return self.send_json({"error": str(exc)}, 400)
        if parsed.path == "/api/sync":
            skip_build = bool(data.get("skip_build", True))
            return self.send_json(run_sync(skip_build=skip_build))
        return self.send_json({"error": "Not found"}, 404)


def main():
    PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"Local Songbook editor")
    print(f"Repo root: {ROOT}")
    print(f"Private lyrics root: {PRIVATE_ROOT}")
    print(f"Open: http://{HOST}:{PORT}/apps/local-songbook-editor/")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
