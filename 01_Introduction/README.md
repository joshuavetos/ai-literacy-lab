# Module 01 — Introduction: The Fluency Illusion

### 1. Objective
Understand what the *fluency illusion* is and why language confidence ≠ factual accuracy.

### 2. The Illusion (Why)
Run `/sandbox/01_fact_check_challenge/verify.py`.
Observe that a fluent model insists **Sydney** is the capital of Australia.
The sentence sounds correct; the content is wrong.

### 3. Mechanism (How)
LLMs maximize *next-token probability*—a statistical goal divorced from truth.
When training text contains Sydney more often near “capital of Australia,” the model learns correlation, not correction.

### 4. Verification Method (Action)
1. Isolate the claim.
2. Ask: *Could this be falsified?*
3. Check against a trusted static corpus or JSON record.
4. Compare frequency of phrasing vs factual incidence.

### 5. Verification Check
1. What is the definition of the fluency illusion?
2. How does token frequency bias output plausibility?
3. Which dataset verified the false claim?
