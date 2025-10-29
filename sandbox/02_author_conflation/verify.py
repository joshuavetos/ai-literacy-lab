import json
import re
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from llm_client import URLError, post_completion  # noqa: E402

BASE_DIR = Path(__file__).parent


def query(prompt: str) -> str:
    try:
        return post_completion(prompt, extra={"n_predict": 80}).lower()
    except URLError as exc:  # pragma: no cover - skip when stub unavailable
        pytest.skip(f"LLM not reachable: {exc}")

def test_reproduce_flaw():
    out = query((BASE_DIR / "prompt.txt").read_text())
    assert "jane austen" in out, "Expected author conflation not reproduced."

def test_verify_correction():
    gt = json.loads((BASE_DIR / "ground_truth.json").read_text())
    fixed = f"Who actually wrote {gt['work']}?"
    out = query(fixed)
    assert re.search(gt["author"].lower(), out), "Correct author not found."
