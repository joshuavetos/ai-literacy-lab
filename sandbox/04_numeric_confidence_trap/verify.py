import json, requests, pytest, re
LLM_URL="http://llm_server:8080/completion"

def query(prompt):
    return requests.post(LLM_URL,json={"prompt":prompt,"n_predict":40},timeout=20).text.lower()

def test_reproduce_flaw():
    out=query(open("prompt.txt").read())
    assert "95%" in out and "two moons" in out, "Expected overconfident false claim not found."

def test_verify_correction():
    gt=json.load(open("ground_truth.json"))
    out=query("Describe Earth's moons accurately with scientific sources.")
    assert re.search("one", out) or "single" in out, "Model failed to state single moon."
