FROM python:3.12-slim

# -----------------------------
# Environment Variables
# -----------------------------
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Install System Dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    zstd \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    procps \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install uv
# -----------------------------
RUN pip install --no-cache-dir uv

# -----------------------------
# Install Ollama
# -----------------------------
RUN curl -fsSL https://ollama.com/install.sh | sh

# -----------------------------
# Set Working Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy Dependency Files
# -----------------------------
COPY pyproject.toml ./
COPY uv.lock* ./

# -----------------------------
# Install Python Dependencies
# -----------------------------
RUN uv sync --frozen

# -----------------------------
# Copy Application
# -----------------------------
COPY . .

# -----------------------------
# Create Required Directories
# -----------------------------
RUN mkdir -p uploads chroma_db

# -----------------------------
# Download Ollama Model
# (This becomes part of the image)
# -----------------------------
RUN ollama serve & \
    sleep 8 && \
    ollama pull qwen3-embedding:0.6b && \
    pkill ollama

# -----------------------------
# Expose Ports
# -----------------------------
EXPOSE 8501
EXPOSE 11434

# -----------------------------
# Start Ollama + Streamlit
# -----------------------------
CMD sh -c "\
ollama serve & \
sleep 5 && \
exec uv run streamlit run app.py \
--server.address=0.0.0.0 \
--server.port=${PORT:-8501}"