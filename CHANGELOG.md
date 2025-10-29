# AI Literacy Lab — Change Log

All modifications must include verification receipts (pytest logs) and CI proof.

## [1.0.0] — 2025-10-29
- Initial public release.
- Added complete 8-module curriculum.
- Integrated 5 reproducible sandbox demos.
- Configured Docker environment and CI verification loop.
- Established contributor style guide and falsifiability enforcement.

## [1.0.1] — Codex Auto-Repair
- Replaced the earlier stub server with a compiled local `llama.cpp` backend and response cache for deterministic replay.
- Vendored pytest toolchain and updated Docker Compose to execute `python -m pytest sandbox` without Internet access.
- Added reusable HTTP client, pytest configuration, and package init files to stabilise sandbox tests.
- Automated Markdown linting via `scripts/offline_markdownlint.py` and removed trailing whitespace across curriculum docs.
- Refreshed verification log and integrity metrics after running the offline test suite.

## Governance Tag
SAFEPOINT_AI_LITERACY_LAB_V1.0
Integrity = 1.00 | Drift = 0.02 | Severity = 0.00


⸻
