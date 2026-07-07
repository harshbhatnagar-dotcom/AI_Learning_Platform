from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

ollama_url="http://localhost:11434/v1/"
ollama=OpenAI(base_url=ollama_url,api_key="ollama")
embedding_model="qwen3-embedding:0.6b"


def create_embedding(query):
    query=ollama.embeddings.create(model=embedding_model,input=[query]).data[0].embedding
    return query



def create_embeddings(chunks):
    emb = ollama.embeddings.create(
        model=embedding_model,
        input=chunks
    )

    vectors=[e.embedding for e in emb.data]

    return vectors