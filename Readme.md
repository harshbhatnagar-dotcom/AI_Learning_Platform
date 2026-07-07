# 🎓 AI Study Platform

An AI-powered learning assistant that transforms study materials into interactive learning resources. Upload your notes, books, PPTs, or assignments, and let AI generate summaries, explain concepts, create quizzes, flashcards, personalized study plans, and answer questions using Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- 📄 Upload multiple PDF, DOCX, and PPTX files
- 📚 Treat all uploaded documents as a single knowledge base
- 📝 AI-generated summaries
- 💡 Concept explanations
- ❓ Quiz generation
- 🃏 Flashcard generation
- 📅 Personalized study plans
- 💬 Chat with your notes using RAG
- 🔍 Semantic search with ChromaDB
- 🧠 Local embeddings using Ollama

---

## 🏗️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### LLM
- Groq (OpenAI SDK)

### Embeddings
- Ollama
- qwen3-embedding:0.6b

### Vector Database
- ChromaDB

### OCR
- Tesseract OCR

### Document Parsing
- PyMuPDF
- python-docx
- python-pptx

### Chunking
- RecursiveCharacterTextSplitter

---

# 📂 Project Structure

```text
AI-Study-Platform/
│
├── app.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .env
│
├── pages/
│   ├── 1_Upload.py
│   ├── 2_Summary.py
│   ├── 3_Concept_Explainer.py
│   ├── 4_Quiz.py
│   ├── 5_Flashcards.py
│   ├── 6_Study_Plan.py
│   └── 7_Chat.py
│
├── utils/
│   ├── parser.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vectordb.py
│   ├── llm.py
│   └── topic_extractor.py
│
├── uploads/
├── chroma_db/
│
└── static/
```