"""Utility for interacting with the local llama.cpp server with deterministic caching."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict
from urllib.error import URLError
from urllib.request import Request, urlopen

LLM_URL = os.getenv("LLM_URL", "http://127.0.0.1:8080/completion")
CACHE_PATH = Path(__file__).with_name("cached_responses.json")
_CACHE: Dict[str, Any] | None = None

_SEPARATORS = (",", ":")


def _load_cache() -> Dict[str, Any]:
    global _CACHE
    if _CACHE is None:
        if CACHE_PATH.exists():
            try:
                _CACHE = json.loads(CACHE_PATH.read_text())
            except json.JSONDecodeError:
                _CACHE = {}
        else:
            _CACHE = {}
        _CACHE.setdefault("responses", {})
    return _CACHE


def _save_cache(cache: Dict[str, Any]) -> None:
    contents = json.dumps(cache, indent=2, sort_keys=True, ensure_ascii=False)
    CACHE_PATH.write_text(f"{contents}\n")


def _cache_key(prompt: str, extra: Dict[str, Any] | None) -> str:
    payload = {"prompt": prompt, "extra": extra or {}}
    return json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=_SEPARATORS
    )


def _extract_content(payload: Any) -> str:
    if isinstance(payload, dict):
        if "content" in payload and isinstance(payload["content"], str):
            return payload["content"]
        if "response" in payload and isinstance(payload["response"], str):
            return payload["response"]
        if "choices" in payload and isinstance(payload["choices"], list):
            for choice in payload["choices"]:
                if isinstance(choice, dict):
                    text = choice.get("text")
                    if isinstance(text, str):
                        return text
    if isinstance(payload, str):
        return payload
    raise ValueError("LLM response missing textual content")


def run_inference(prompt: str, *, timeout: int = 30, extra: Dict[str, Any] | None = None) -> str:
    """Send prompt to local LLM server, caching the first response."""

    cache = _load_cache()
    key = _cache_key(prompt, extra)
    cached = cache["responses"].get(key)
    if isinstance(cached, str):
        return cached

    payload: Dict[str, Any] = {"prompt": prompt, "n_predict": 256}
    if extra:
        payload.update(extra)

    data = json.dumps(payload).encode("utf-8")
    request = Request(LLM_URL, data=data, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")

    parsed: Any
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = raw

    content = _extract_content(parsed)
    cache["responses"][key] = content
    _save_cache(cache)
    return content


__all__ = ["run_inference", "LLM_URL", "URLError"]
