import json
import re
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from llm_client import URLError, run_inference  # noqa: E402

BASE_DIR = Path(__file__).parent


def query(prompt: str) -> str:
    try:
        return run_inference(prompt, extra={"n_predict": 40}).lower()
    except URLError as exc:  # pragma: no cover
        pytest.skip(f"LLM not reachable: {exc}")


def test_reproduce_flaw():
    out = query((BASE_DIR / "prompt.txt").read_text().strip())
    assert "95%" in out and "two moons" in out, "Expected overconfident false claim not found."


def test_verify_correction():
    gt = json.loads((BASE_DIR / "ground_truth.json").read_text())
    out = query("Describe Earth's moons accurately with scientific sources.")
    assert re.search("one", out) or "single" in out, "Model failed to state single moon."
