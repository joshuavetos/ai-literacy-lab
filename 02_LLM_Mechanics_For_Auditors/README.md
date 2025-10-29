# Module 02 — Inside the Black Box: LLM Mechanics for Auditors

### 1. Objective
Explain how model architecture and training objectives create epistemic limits.

### 2. The Illusion (Why)
Prompt any local model for: “List three sources for your last answer.”  
Observe: confident citations, nonexistent papers.

### 3. Mechanism (How)
The network predicts sequences, not facts.  
Loss minimization on token prediction rewards *plausible continuation*, not *verifiable origin*.  
Attention heads amplify associative drift over long contexts.

### 4. Verification Method (Action)
1. Request identical question twice; compare token variance.  
2. Measure entropy of outputs.  
3. Cross-check cited works in an offline index (e.g., provided `ground_truth.json`).  

### 5. Verification Check
1. What is minimized during LLM training?  
2. Why can identical prompts yield divergent answers?  
3. Which experiment would reveal citation hallucination?
