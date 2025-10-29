FROM python:3.10-slim

WORKDIR /app

# Add vendored Python dependencies (pytest + support libs)
COPY vendor ./vendor

ENV PYTHONPATH=/app/vendor:${PYTHONPATH}

# Install build prerequisites for llama.cpp
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake git wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Build llama.cpp with the HTTP server target
RUN git clone --depth 1 https://github.com/ggerganov/llama.cpp.git /opt/llama && \
    cmake -B /opt/llama/build -S /opt/llama -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF && \
    cmake --build /opt/llama/build --target llama-server --config Release

# Copy deterministic demo model assets
COPY models /models

# Copy fallback server for deterministic replays
COPY fallback_llm_server.py ./fallback_llm_server.py

# Script that launches the server when the container starts
COPY start_llama.sh /usr/local/bin/start_llama.sh
RUN chmod +x /usr/local/bin/start_llama.sh

EXPOSE 8080

CMD ["/usr/local/bin/start_llama.sh"]
