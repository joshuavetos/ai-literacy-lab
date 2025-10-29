import json, re, requests, pytest
LLM_URL = "http://llm_server:8080/completion"

def query(prompt): 
    r = requests.post(LLM_URL, json={"prompt": prompt, "n_predict":80}, timeout=20)
    return r.text.lower()

def test_reproduce_flaw():
    out = query(open("prompt.txt").read())
    assert "jane austen" in out, "Expected author conflation not reproduced."

def test_verify_correction():
    gt = json.load(open("ground_truth.json"))
    fixed = f"Who actually wrote {gt['work']}?"
    out = query(fixed)
    assert re.search(gt["author"].lower(), out), "Correct author not found."
