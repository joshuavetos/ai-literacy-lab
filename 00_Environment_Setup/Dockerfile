FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        build-essential \
        git \
        curl \
        python3 \
        python3-pip \
        wget \
        cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Download and build llama.cpp minimal model
RUN git clone https://github.com/ggerganov/llama.cpp.git \
    && cd llama.cpp \
    && make

# Add a tiny GGUF test model (toy 1B quantized or dummy)
RUN mkdir -p /models \
    && wget -q https://huggingface.co/ggml-org/tinyllama-1b/resolve/main/tinyllama-1b.gguf \
        -O /models/tinyllama.gguf \
    || echo "Placeholder model - add offline copy here"

EXPOSE 8080
CMD ["bash", "-c", "cd llama.cpp && ./server -m /models/tinyllama.gguf --port 8080"]
