# AI Literacy Lab Local Environment

This environment packages the entire AI Literacy Lab toolchain inside Docker so every learner runs the exact same stack. By pinning operating system packages, Python libraries, and the local large language model (LLM) server, we avoid the hidden drift that usually accumulates on personal machines.

## Why it is reproducible

- **Immutable base image.** The Dockerfile starts from `ubuntu:22.04`, a publicly versioned image. Every `apt-get` invocation installs specific packages at the versions published with that release, so the build always begins from a known state.
- **Offline model + deterministic binaries.** The build step compiles `llama.cpp` inside the container and downloads a tiny GGUF model into `/models`. Because this happens during the image build, the same artifacts are baked into every container run.
- **Pinned Python dependencies.** `requirements.txt` lists exact versions (pytest 8.3.1, requests 2.32.3, markdownlint-cli 0.40.0). The build caches the wheel files inside the image, guaranteeing that test scripts execute with the same libraries no matter where the container runs.
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
   docker-compose run --rm verifier pytest sandbox/01_fact_check_challenge -q
   ```

All steps run locally, with no Internet access required after the initial image build. That constraint keeps demonstrations falsifiable: the same prompts yield the same model outputs, and the same regression tests enforce that property over time.
