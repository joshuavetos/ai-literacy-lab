# AI Literacy Lab Local Environment

This environment packages the entire AI Literacy Lab toolchain inside Docker so every learner runs the exact same stack. By pinning operating system packages, Python libraries, and the local large language model (LLM) server, we avoid the hidden drift that usually accumulates on personal machines.

## Why it is reproducible

- **Deterministic base image.** The Dockerfile starts from `python:3.10-slim` and vendors the Python dependencies used by the verifier.
- **Compiled llama.cpp backend.** During the image build we compile `llama.cpp` with the HTTP server target under `/opt/llama`. At runtime the container launches `llama-server` against `models/ggml-model-q4_0.bin` on port 8080.
- **Deterministic cache replay.** The first time a sandbox prompt is issued the response is stored in `sandbox/cached_responses.json`. Subsequent runs replay the cached text, guaranteeing identical results across machines and CI. When no model is provided, the startup script detects the placeholder and serves the cached responses directly.
- **Vendored test runner.** `pytest` and its transitive dependencies live under `00_Environment_Setup/vendor`. The image sets `PYTHONPATH` accordingly, so `python -m pytest sandbox` works without `pip`.
- **Single command orchestration.** `docker-compose.yml` launches two services—an LLM server and a verifier—on the same virtual network. Since Docker orchestrates the lifecycle, port bindings, and startup order, each run of `docker-compose up` reproduces the identical topology.
- **Automated verification pipeline.** The GitHub Actions workflow runs the same Docker Compose commands on every push or pull request. CI serves as a watchdog that immediately flags any configuration drift.

## How to use it

1. Build and start the services:
   ```bash
   cd 00_Environment_Setup
   docker-compose up --build
   ```
2. After the containers start, open another terminal and run the verification suite from the mounted sandbox directory:
   ```bash
   cd 00_Environment_Setup
   docker-compose up verifier
   ```
   or, if you are already inside the `docker-compose up` session, wait for the verifier container to finish.
3. To supply your own model, replace `models/ggml-model-q4_0.bin` with a llama.cpp-compatible checkpoint. The startup script automatically switches from the cached replay server to real-time inference when a valid model is present. If the placeholder file is still in place, `verify_local_llm.py` will surface an explicit failure so you know a real checkpoint is required.
4. Explore the exercises under `/sandbox`. For example, to run the fact check challenge manually:
   ```bash
   docker-compose run --rm verifier python -m pytest sandbox/01_fact_check_challenge
   ```

All steps run locally, with no Internet access required after the initial image build. That constraint keeps demonstrations falsifiable: the same prompts yield the same model outputs, and the same regression tests enforce that property over time.
