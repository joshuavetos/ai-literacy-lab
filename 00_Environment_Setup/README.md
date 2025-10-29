# AI Literacy Lab Local Environment

This environment packages the entire AI Literacy Lab toolchain inside Docker so every learner runs the exact same stack. By pinning operating system packages, Python libraries, and the local large language model (LLM) server, we avoid the hidden drift that usually accumulates on personal machines.

## Why it is reproducible

- **Minimal deterministic base image.** The Dockerfile starts from `python:3.10-slim` and contains no network package installs. Everything required to run the demos ships in the repository.
- **Offline inference stub.** Instead of downloading `llama.cpp`, the image copies `local_llm_server.py` and a curated `model_responses.json`. The HTTP server reproduces each sandbox flaw and fix deterministically with zero Internet dependencies.
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
3. Explore the exercises under `/sandbox`. For example, to run the fact check challenge manually:
   ```bash
   docker-compose run --rm verifier python -m pytest sandbox/01_fact_check_challenge
   ```

All steps run locally, with no Internet access required after the initial image build. That constraint keeps demonstrations falsifiable: the same prompts yield the same model outputs, and the same regression tests enforce that property over time.
