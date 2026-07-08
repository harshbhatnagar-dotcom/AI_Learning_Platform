FROM python:3.12-slim

# -----------------------------
# Environment Variables
# -----------------------------
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Install System Dependencies
# -----------------------------
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install uv
# -----------------------------
RUN pip install --no-cache-dir uv

# -----------------------------
# Working Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy dependency files
# -----------------------------
COPY pyproject.toml ./
COPY uv.lock* ./

# -----------------------------
# Install dependencies into the
# system Python (NOT a .venv)
# -----------------------------
RUN uv sync --frozen --no-dev --system

# -----------------------------
# Copy application
# -----------------------------
COPY . .

# -----------------------------
# Create directories
# -----------------------------
RUN mkdir -p chroma_db uploads

# -----------------------------
# Expose Streamlit port
# -----------------------------
EXPOSE 8501

# -----------------------------
# Start Streamlit
# -----------------------------
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
