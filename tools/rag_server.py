#!/usr/bin/env python3
"""
Joy Division AI Writing Studio — Local web server v0.3

Usage
-----
From repository root:

    python tools/build_registers.py
    python tools/build_master_docs.py
    python tools/rag_server.py

Then open:

    http://127.0.0.1:8765

Routes
------
/                       unified portal
/prompt                 prompt interface
/rag                    documentary RAG interface
/masters                full-web master documents interface
/apps/prompt-studio/    prompt interface
/apps/rag-studio/       documentary RAG interface
/apps/master-docs/      master documents interface
/api/status             RAG corpus status
/api/search             RAG search endpoint
/api/master-docs        list generated master documents
/api/master-doc         read one generated master document
/api/master-doc-raw     read one generated master document as raw Markdown

This server is local-only by default.
It uses Python standard library only and wraps the existing lexical RAG engine.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
APPS_ROOT = REPO_ROOT / "apps"
TOOLS_ROOT = REPO_ROOT / "tools"
CHAPTERS_ROOT = REPO_ROOT / "chapters"

sys.path.insert(0, str(TOOLS_ROOT))

try:
    from rag_search import concise_record, load_records, score_records
except Exception as exc:  # pragma: no cover
    print(f"Unable to import rag_search.py: {exc}", file=sys.stderr)
    raise SystemExit(2) from exc


CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".svg": "image/svg+xml",
}


def chapter_dir_name(chapter: str) -> str | None:
    """Return a safe chapter directory name from a query value."""
    value = str(chapter or "").strip()
    if not re.fullmatch(r"\d{1,2}", value):
        return None
    number = int(value)
    if number < 1 or number > 99:
        return None
    return str(number).zfill(2)


def extract_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


class RAGRequestHandler(BaseHTTPRequestHandler):
    server_version = "JoyDivisionStudio/0.3"

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, body: bytes, content_type: str, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path):
        if not path.exists() or not path.is_file():
            self.send_error(404, "File not found")
            return
        content = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_under_root(self, request_path: str, root: Path):
        requested = request_path.lstrip("/")
        safe_path = (REPO_ROOT / requested).resolve()

        if request_path.endswith("/"):
            safe_path = safe_path / "index.html"

        root_resolved = root.resolve()
        if not str(safe_path).startswith(str(root_resolved)):
            self.send_error(403, "Forbidden")
            return

        self._send_file(safe_path)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/search":
            self.handle_search(parsed)
            return

        if parsed.path == "/api/status":
            self.handle_status()
            return

        if parsed.path == "/api/master-docs":
            self.handle_master_docs_list()
            return

        if parsed.path == "/api/master-doc":
            self.handle_master_doc(parsed, raw=False)
            return

        if parsed.path == "/api/master-doc-raw":
            self.handle_master_doc(parsed, raw=True)
            return

        if parsed.path in {"/", "/index.html"}:
            self._send_file(REPO_ROOT / "index.html")
            return

        if parsed.path in {"/prompt", "/prompt/"}:
            self._send_file(APPS_ROOT / "prompt-studio" / "index.html")
            return

        if parsed.path in {"/rag", "/rag/"}:
            self._send_file(APPS_ROOT / "rag-studio" / "index.html")
            return

        if parsed.path in {"/masters", "/masters/"}:
            self._send_file(APPS_ROOT / "master-docs" / "index.html")
            return

        if parsed.path.startswith("/apps/"):
            self._serve_under_root(parsed.path, APPS_ROOT)
            return

        self.send_error(404, "Not found")

    def handle_status(self):
        try:
            records = load_records()
            counts = {}
            for record in records:
                kind = record.get("kind", "unknown")
                counts[kind] = counts.get(kind, 0) + 1
            self._send_json({
                "ok": True,
                "records": len(records),
                "counts": counts,
                "exports_path": "exports/generated/all_records.json",
            })
        except SystemExit:
            self._send_json({
                "ok": False,
                "error": "Exports missing. Run: python tools/build_registers.py",
            }, status=500)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=500)

    def handle_master_docs_list(self):
        documents = []
        if CHAPTERS_ROOT.exists():
            for path in sorted(CHAPTERS_ROOT.glob("[0-9][0-9]/document_maitre.md")):
                chapter = path.parent.name
                markdown = path.read_text(encoding="utf-8")
                documents.append({
                    "chapter": int(chapter),
                    "chapter_padded": chapter,
                    "title": extract_title(markdown, f"Chapitre {int(chapter)}"),
                    "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                })
        self._send_json({"ok": True, "documents": documents})

    def handle_master_doc(self, parsed, raw: bool):
        params = parse_qs(parsed.query)
        chapter_value = (params.get("chapter") or [""])[0]
        chapter_dir = chapter_dir_name(chapter_value)
        if not chapter_dir:
            self._send_json({"ok": False, "error": "Invalid or missing chapter"}, status=400)
            return

        path = (CHAPTERS_ROOT / chapter_dir / "document_maitre.md").resolve()
        if not str(path).startswith(str(CHAPTERS_ROOT.resolve())):
            self.send_error(403, "Forbidden")
            return
        if not path.exists():
            self._send_json({
                "ok": False,
                "error": "Master document not found. Run: python tools/build_master_docs.py",
                "chapter": int(chapter_dir),
            }, status=404)
            return

        markdown = path.read_text(encoding="utf-8")
        if raw:
            self._send_bytes(markdown.encode("utf-8"), "text/markdown; charset=utf-8")
            return

        self._send_json({
            "ok": True,
            "chapter": int(chapter_dir),
            "chapter_padded": chapter_dir,
            "title": extract_title(markdown, f"Chapitre {int(chapter_dir)}"),
            "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "content": markdown,
        })

    def handle_search(self, parsed):
        params = parse_qs(parsed.query)
        query = (params.get("q") or [""])[0].strip()
        kind = (params.get("kind") or [""])[0].strip() or None
        top_raw = (params.get("top") or ["10"])[0]

        try:
            top = max(1, min(int(top_raw), 50))
        except ValueError:
            top = 10

        if not query:
            self._send_json({"ok": False, "error": "Missing query"}, status=400)
            return

        if kind and kind not in {"atom", "quote", "chronology", "song", "person", "unknown"}:
            self._send_json({"ok": False, "error": f"Invalid kind: {kind}"}, status=400)
            return

        try:
            records = load_records()
            scored = score_records(records, query, kind)
            payload = {
                "ok": True,
                "query": query,
                "kind": kind,
                "top": top,
                "total_matches": len(scored),
                "results": [
                    {
                        "score": round(score, 3),
                        "record": concise_record(record),
                    }
                    for score, record in scored[:top]
                ],
            }
            self._send_json(payload)
        except SystemExit:
            self._send_json({
                "ok": False,
                "error": "Exports missing. Run: python tools/build_registers.py",
            }, status=500)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=500)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local Joy Division AI Writing Studio web interface.")
    parser.add_argument("--host", default="127.0.0.1", help="Host, default 127.0.0.1")
    parser.add_argument("--port", type=int, default=8765, help="Port, default 8765")
    args = parser.parse_args()

    if not APPS_ROOT.exists():
        print("Missing apps/ directory", file=sys.stderr)
        return 2

    server = ThreadingHTTPServer((args.host, args.port), RAGRequestHandler)
    print(f"Joy Division AI Writing Studio running at http://{args.host}:{args.port}")
    print("Routes: / · /prompt · /rag · /masters · /apps/prompt-studio/ · /apps/rag-studio/ · /apps/master-docs/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
