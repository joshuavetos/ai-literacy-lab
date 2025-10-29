#!/usr/bin/env python3
"""Verify that the local llama.cpp Docker service is healthy."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import requests

IMAGE_NAME = "ai-literacy-lab/llama"
CONTAINER_NAME = "ai-literacy-llm-verification"
DOCKERFILE_DIR = Path(__file__).resolve().parent / "00_Environment_Setup"
LLM_URL = "http://127.0.0.1:8080/completion"
POLL_TIMEOUT_SECONDS = 90
POLL_INTERVAL_SECONDS = 5
PLACEHOLDER_VALUES = {"{{cached}}", "DEMO_RESPONSE"}


def run_command(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a subprocess command returning the completed process."""

    result = subprocess.run(command, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            "Command failed: {}\nSTDOUT:{}\nSTDERR:{}".format(
                " ".join(command),
                f"\n{result.stdout}" if result.stdout else " <empty>",
                f"\n{result.stderr}" if result.stderr else " <empty>",
            )
        )
    return result


def docker_image_exists(name: str) -> bool:
    result = run_command(["docker", "images", "-q", name], check=False)
    return bool(result.stdout.strip())


def ensure_docker_image() -> None:
    if docker_image_exists(IMAGE_NAME):
        return
    build_command = [
        "docker",
        "build",
        "-t",
        IMAGE_NAME,
        "-f",
        str(DOCKERFILE_DIR / "Dockerfile"),
        str(DOCKERFILE_DIR),
    ]
    run_command(build_command)


def stop_container(name: str) -> None:
    run_command(["docker", "rm", "-f", name], check=False)


def start_container(name: str) -> None:
    stop_container(name)
    run_command(
        [
            "docker",
            "run",
            "-d",
            "--rm",
            "--name",
            name,
            "-p",
            "8080:8080",
            IMAGE_NAME,
        ]
    )


def poll_server(prompt: str) -> Optional[requests.Response]:
    deadline = time.time() + POLL_TIMEOUT_SECONDS
    payload = {"prompt": prompt, "n_predict": 64}
    headers = {"Content-Type": "application/json"}

    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            break

        try:
            response = requests.post(
                LLM_URL,
                data=json.dumps(payload),
                headers=headers,
                timeout=remaining,
            )
            if response.status_code == 200:
                return response
        except requests.RequestException:
            pass

        sleep_duration = min(POLL_INTERVAL_SECONDS, max(deadline - time.time(), 0))
        if sleep_duration:
            time.sleep(sleep_duration)
    return None


def validate_response(response: requests.Response) -> bool:
    try:
        data = response.json()
    except ValueError:
        return False

    if not isinstance(data, dict):
        return False
    if data.get("cached") is True:
        return False
    content = data.get("content")
    if not isinstance(content, str):
        return False
    content_stripped = content.strip()
    if not content_stripped:
        return False
    if content_stripped in PLACEHOLDER_VALUES:
        return False
    return True


def main() -> int:
    try:
        ensure_docker_image()
    except Exception as exc:  # pragma: no cover - runtime failure handling
        print("❌ Server unreachable or invalid response.")
        print(f"Failed to build Docker image: {exc}")
        return 1

    try:
        start_container(CONTAINER_NAME)
    except Exception as exc:  # pragma: no cover
        print("❌ Server unreachable or invalid response.")
        print(f"Failed to start container: {exc}")
        return 1

    try:
        response = poll_server("Explain why audits improve AI systems.")
        if response and validate_response(response):
            print("✅ LLM server running and generating completions.")
            return 0
        print("❌ Server unreachable or invalid response.")
        if response is not None:
            print(f"Status code: {response.status_code}")
            try:
                payload = response.json()
            except ValueError:
                print(f"Body: {response.text}")
            else:
                if payload.get("cached") is True:
                    print(
                        "Detected fallback cached responses. "
                        "Place a llama.cpp checkpoint at "
                        "00_Environment_Setup/models/ggml-model-q4_0.bin."
                    )
                else:
                    print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    finally:
        stop_container(CONTAINER_NAME)


if __name__ == "__main__":
    sys.exit(main())
