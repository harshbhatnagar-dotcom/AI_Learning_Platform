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
# Expose Streamlit Port
# -----------------------------
EXPOSE 8501

# -----------------------------
# Start Streamlit
# -----------------------------
CMD sh -c "uv run streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}"