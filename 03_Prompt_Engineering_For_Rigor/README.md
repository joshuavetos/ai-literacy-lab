# Module 03 — Prompt Engineering for Epistemic Rigor

### 1. Objective
Design prompts that reduce hallucination by enforcing structure and uncertainty disclosure.

### 2. The Illusion (Why)
Naïve prompt: “Explain quantum entanglement.”
Model output: poetic, wrong, unfalsifiable metaphors.

### 3. Mechanism (How)
Broad prompts trigger generative sprawl.
Structured prompts constrain probability space and signal desired verification (e.g., “cite or flag unknown”).

### 4. Verification Method (Action)
1. Compare baseline vs structured prompt outputs.
2. Log hallucination frequency across 10 runs.
3. Compute reduction % in unsupported claims.

### 5. Verification Check
1. Define a falsifiable prompt.
2. What structure encourages source citation?
3. How would you measure hallucination rate?
