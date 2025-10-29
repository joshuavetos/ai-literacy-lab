# Module 04 — Verification and Cross-Validation Methods

### 1. Objective
Turn AI answers into verifiable claims through reproducible checks.

### 2. The Illusion (Why)
A fluent model references “WHO 2022 Report on Sleep” — nonexistent offline.

### 3. Mechanism (How)
Models lack persistent reference memory; they interpolate plausible sources.

### 4. Verification Method (Action)
1. Parse outputs into atomic claims.
2. Search static corpus for supporting text.
3. Rate evidence: Primary / Secondary / Absent.
4. Record provenance in JSONL.

### 5. Verification Check
1. What distinguishes cross-validation from citation?
2. How is provenance recorded?
3. Why avoid online APIs for verification?
