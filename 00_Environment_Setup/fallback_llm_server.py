"""Deterministic HTTP server that replays cached llama.cpp completions."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict

CACHE_PATH = Path("sandbox/cached_responses.json")
_SEPARATORS = (",", ":")


def load_cache() -> Dict[str, Any]:
    if not CACHE_PATH.exists():
        raise FileNotFoundError(f"Cache file missing: {CACHE_PATH}")
    data = json.loads(CACHE_PATH.read_text())
    return data.get("responses", {})


RESPONSES = load_cache()


def make_cache_key(prompt: str, extra: Dict[str, Any] | None) -> str:
    payload = {"prompt": prompt, "extra": extra or {}}
    return json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=_SEPARATORS
    )


class RequestHandler(BaseHTTPRequestHandler):
    server_version = "CachedLLM/1.0"

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid_json"}, status=400)
            return

        prompt = payload.get("prompt")
        if not isinstance(prompt, str):
            self._send_json({"error": "missing_prompt"}, status=400)
            return

        extra = {k: v for k, v in payload.items() if k != "prompt"}
        key = make_cache_key(prompt, extra)
        content = RESPONSES.get(key)
        if content is None:
            self._send_json({"error": "cache_miss", "key": key}, status=404)
            return

        self._send_json({"content": content, "cached": True})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003 - keep quiet
        return


def run() -> None:
    server = HTTPServer(("0.0.0.0", 8080), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - manual stop
        pass


if __name__ == "__main__":
    run()
