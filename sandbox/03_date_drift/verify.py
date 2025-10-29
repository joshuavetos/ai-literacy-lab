import json, requests, pytest
LLM_URL="http://llm_server:8080/completion"

def test_reproduce_flaw():
    prompt=open("prompt.txt").read().strip()
    r=requests.post(LLM_URL,json={"prompt":prompt,"n_predict":30},timeout=20)
    out=r.text
    assert "1971" in out, "Expected wrong year missing."

def test_verify_correction():
    gt=json.load(open("ground_truth.json"))
    corr=f"{gt['event']} occurred in what year? Answer numerically."
    r=requests.post(LLM_URL,json={"prompt":corr,"n_predict":20},timeout=20)
    assert str(gt["year"]) in r.text, "Correct year not returned."
