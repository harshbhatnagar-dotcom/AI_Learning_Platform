from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

ollama_url="http://localhost:11434/v1/"
ollama=OpenAI(base_url=ollama_url,api_key="ollama")
ollama_embedding_model="qwen3-embedding:0.6b"

gemini_api_key=os.getenv("GEMINI_API_KEY")

gemini = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
gemini_embedding_model="gemini-embedding-2"


def create_embedding(query):
    query=gemini.embeddings.create(model=gemini_embedding_model,input=[query]).data[0].embedding
    return query



def create_embeddings(chunks):
    emb = gemini.embeddings.create(
        model=gemini_embedding_model,
        input=chunks
    )

    vectors=[e.embedding for e in emb.data]

    return vectors