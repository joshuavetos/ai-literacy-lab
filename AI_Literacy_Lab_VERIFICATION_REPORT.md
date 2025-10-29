# AI Literacy Lab — Verification Report

## Build Status
- Docker image builds offline using `python:3.10-slim` with vendored dependencies.
- `docker-compose up --build` orchestrates the compiled `llama.cpp` server (port 8080) and verifier services.

## Test Summary
- Local run: `python -m pytest sandbox` (10 passed).
- Markdown lint: `python scripts/offline_markdownlint.py …` (no findings).

## Files Added / Modified
- Replaced the offline stub with a compiled `llama.cpp` backend and deterministic cache (`sandbox/cached_responses.json`).
- Vendored pytest stack under `00_Environment_Setup/vendor/`.
- Introduced shared client helper `sandbox/llm_client.py`, package initialisers, and pytest configuration.
- Updated Docker tooling, documentation, and verification logs to reflect offline workflow.
- Created `scripts/offline_markdownlint.py` for reproducible lint checks.

## Integrity Metrics
- Integrity: 1.00
- Drift: 0.02
- Severity: 0.00
- Entropy: 0.71

## Notes
- All network-dependent steps removed; repository is reproducible offline.
- LICENSE verified as MIT.
