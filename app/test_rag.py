from app.utils import load_pdf, chunk_text
from app.rag import VectorStore, generate_answer

#Load PDF
text = load_pdf("data/sample.pdf")

#Chunk text
chunks = chunk_text(text)

print(f"Total chunks created: {len(chunks)}")

#vector store
vector_store = VectorStore(dimension=384)  # MiniLM embedding size

#Add chunks to vector DB
vector_store.add(chunks)

print("Embeddings stored successfully.")

#Test search
query = "What is this document about?"
results = vector_store.search(query)

print("\nTop Retrieved Chunks:\n")
for i, chunk in enumerate(results):
    print(f"Result {i+1}:\n{chunk}\n")

answer = generate_answer(results, query)

print("Final Answer:\n")
print(answer)