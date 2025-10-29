# Module 05 — Hallucination Detection and Correction

### 1. Objective
Identify and repair common hallucination types: fabrication, conflation, extrapolation.

### 2. The Illusion (Why)
Prompt: “Summarize Jane Austen’s ‘Wuthering Heights.’”
Output merges Austen with Bronte.

### 3. Mechanism (How)
Semantic proximity collapses author boundaries.
Model merges clusters with overlapping features.

### 4. Verification Method (Action)
1. Create minimal prompt pairs causing conflation.
2. Compare named entities to reference JSON.
3. Rewrite prompt using disambiguation cues.
4. Re-run and log corrected entities.

### 5. Verification Check
1. Name two hallucination categories.
2. Which disambiguation prompt repaired the conflation?
3. Why are entity tests falsifiable?
