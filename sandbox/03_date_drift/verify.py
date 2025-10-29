import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from llm_client import URLError, post_completion  # noqa: E402

BASE_DIR = Path(__file__).parent


def test_reproduce_flaw():
    prompt=(BASE_DIR/"prompt.txt").read_text().strip()
    try:
        out=post_completion(prompt, extra={"n_predict":30})
    except URLError as exc:  # pragma: no cover
        pytest.skip(f"LLM not reachable: {exc}")
    assert "1971" in out, "Expected wrong year missing."

def test_verify_correction():
    gt=json.loads((BASE_DIR/"ground_truth.json").read_text())
    corr=f"{gt['event']} occurred in what year? Answer numerically."
    try:
        out=post_completion(corr, extra={"n_predict":20})
    except URLError as exc:  # pragma: no cover
        pytest.skip(f"LLM not reachable: {exc}")
    assert str(gt["year"]) in out, "Correct year not returned."
