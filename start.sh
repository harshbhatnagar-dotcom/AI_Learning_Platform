#!/bin/sh

ollama serve &

sleep 5

ollama pull qwen3-embedding:0.6b

exec uv run streamlit run app.py \
    --server.address=0.0.0.0 \
    --server.port=8501
