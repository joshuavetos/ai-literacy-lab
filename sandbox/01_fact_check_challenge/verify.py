import json
import re
from pathlib import Path

import pytest
import requests

LLM_URL = "http://llm_server:8080/completion"

def query_llm(prompt: str) -> str:
    """Send prompt to local LLM server and return text output."""
    try:
        response = requests.post(
            LLM_URL,
            json={"prompt": prompt, "n_predict": 50},
            timeout=15,
        )
        response.raise_for_status()
        return response.text.strip().lower()
    except Exception as exc:  # pragma: no cover - gracefully handle network issues in CI
        pytest.skip(f"LLM not reachable: {exc}")

def load_ground_truth() -> dict:
    ground_truth_path = Path("ground_truth.json")
    with ground_truth_path.open() as handle:
        return json.load(handle)

def test_reproduce_flaw():
    prompt = Path("prompt.txt").read_text().strip()
    output = query_llm(prompt)
    expected = Path("expected_flaw.txt").read_text().strip().lower()
    assert expected in output, (
        f"Expected flaw '{expected}' not found in output: {output[:100]}"
    )

def test_verify_correction():
    """Check corrected prompt produces right answer."""
    ground_truth = load_ground_truth()
    corrected_prompt = (
        f"{ground_truth['question']} Answer only with the factual capital city."
    )
    output = query_llm(corrected_prompt)
    assert re.search(ground_truth["answer"].lower(), output), (
        f"Correct answer not found. Got: {output[:100]}"
    )
