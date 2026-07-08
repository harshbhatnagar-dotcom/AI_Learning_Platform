FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD [".venv/bin/streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]