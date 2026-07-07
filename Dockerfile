FROM python:3.12-slim

# Prevent Python from buffering stdout
ENV PYTHONUNBUFFERED=1

# Install system packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy dependency files first (better Docker layer caching)
COPY pyproject.toml .
COPY uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application
COPY . .

# Create required folders
RUN mkdir -p uploads chroma_db

# Download embedding model
RUN ollama serve & \
    sleep 10 && \
    ollama pull qwen3-embedding:0.6b

EXPOSE 8501
EXPOSE 11434

# Start Ollama and Streamlit
CMD sh -c "\
ollama serve & \
sleep 5 && \
uv run streamlit run app.py --server.address=0.0.0.0 --server.port=8501"