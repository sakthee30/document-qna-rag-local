import faiss
import numpy as np
import requests 
from app.embeddings import get_embeddings

class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.text_chunks = []

    def add(self, chunks):
        embeddings = get_embeddings(chunks)
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(chunks)

    def search(self, query, top_k=3):
        query_embedding = get_embeddings([query])
        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        results = [self.text_chunks[i] for i in indices[0]]
        return results


def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]