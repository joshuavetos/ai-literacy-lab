#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${LLAMA_MODEL_PATH:-/models/ggml-model-q4_0.bin}"
LLAMA_SERVER="/opt/llama/build/bin/llama-server"
PLACEHOLDER_TOKEN="AI_LITERACY_LAB_PLACEHOLDER"

if [[ ! -f "${MODEL_PATH}" ]]; then
  echo "Model file not found at ${MODEL_PATH}" >&2
  echo "Falling back to cached deterministic server." >&2
  exec python /app/fallback_llm_server.py
fi

if head -c ${#PLACEHOLDER_TOKEN} "${MODEL_PATH}" 2>/dev/null | grep -q "${PLACEHOLDER_TOKEN}"; then
  echo "Placeholder model detected; launching deterministic cache server." >&2
  exec python /app/fallback_llm_server.py
fi

exec "${LLAMA_SERVER}" \
  --model "${MODEL_PATH}" \
  --host 0.0.0.0 \
  --port 8080 \
  --threads "${LLAMA_THREADS:-4}" \
  --n-predict 256
