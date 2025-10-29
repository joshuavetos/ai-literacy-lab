FROM python:3.10-slim

WORKDIR /app

# Add vendored Python dependencies (pytest + support libs)
COPY vendor ./vendor

ENV PYTHONPATH=/app/vendor:${PYTHONPATH}

# Copy the lightweight deterministic LLM stub
COPY local_llm_server.py ./
COPY model_responses.json ./

EXPOSE 8080

CMD ["python", "local_llm_server.py"]
