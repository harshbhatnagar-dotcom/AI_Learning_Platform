from chromadb import PersistentClient
from utils.embedding import create_embedding,create_embeddings

collection_name="study_details"
chroma=PersistentClient("Study")

collection=chroma.get_or_create_collection(collection_name)

def store_to_vectordb(chunks,filename):
    

    vectors=create_embeddings(chunks)
    metadatas = [
        {
            "source": filename
        }
        for _ in chunks
    ]

    ids=[f"{filename}_{i}" for i in range(len(chunks))]
    collection.add(ids=ids,embeddings=vectors,documents=chunks,metadatas=metadatas) 
    print(f"Added {len(chunks)} chunks from {filename} file to db")

def search(question,RETRIEVAL_K=10):
    query=create_embedding(question)
    results=collection.query(query_embeddings=[query],n_results=RETRIEVAL_K)
    chunks=[]
    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": document,
            "metadata": metadata,
            "distance": distance
        })

    return chunks

def clear_db():
    """
    Delete all stored study material.
    """

    global collection

    try:
        chroma.delete_collection(collection_name)
    except Exception:
        pass

    collection = chroma.get_or_create_collection(
        name=collection_name
    )
