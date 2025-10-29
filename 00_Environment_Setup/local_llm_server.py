"""Deterministic offline stub that emulates a minimal llama.cpp server."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Dict, List

PORT = 8080
RESPONSES_PATH = Path("model_responses.json")


def load_responses() -> List[Dict[str, str]]:
    data = json.loads(RESPONSES_PATH.read_text())
    # Normalize keys for case-insensitive matching
    for item in data:
        item["match"] = item["match"].lower()
    data.sort(key=lambda item: len(item["match"]), reverse=True)
    return data


RESPONSES = load_responses()
DEFAULT_RESPONSE = (
    "This offline stub cannot answer the prompt. "
    "Provide a sandbox prompt defined in model_responses.json."
)


def find_response(prompt: str) -> str:
    prompt_lower = prompt.lower()
    for item in RESPONSES:
        if item["match"] in prompt_lower:
            return item["response"]
    return DEFAULT_RESPONSE


class CompletionHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/completion":
            self.send_error(404, "Endpoint not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON body")
            return

        prompt = payload.get("prompt", "")
        response_text = find_response(prompt)

        body_bytes = response_text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        """Silence default HTTP server logging for deterministic output."""
        return


def run_server() -> None:
    server = HTTPServer(("0.0.0.0", PORT), CompletionHandler)
    print(f"Offline LLM stub listening on http://0.0.0.0:{PORT}/completion", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
