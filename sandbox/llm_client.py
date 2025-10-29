"""Lightweight HTTP client for the offline LLM stub."""

from __future__ import annotations

import json
import os
from typing import Any, Dict
from urllib.error import URLError
from urllib.request import Request, urlopen

LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/completion")


def post_completion(prompt: str, *, timeout: int = 15, extra: Dict[str, Any] | None = None) -> str:
    payload = {"prompt": prompt}
    if extra:
        payload.update(extra)
    data = json.dumps(payload).encode("utf-8")
    request = Request(LLM_URL, data=data, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


__all__ = ["post_completion", "LLM_URL", "URLError"]
