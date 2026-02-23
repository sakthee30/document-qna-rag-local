from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

from app.utils import load_pdf, chunk_text
from app.rag import VectorStore, generate_answer

app = FastAPI(title="Document QnA RAG API")

#vector store 
vector_store = VectorStore(dimension=384)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load and chunk
    text = load_pdf(file_path)
    chunks = chunk_text(text)

    # Add to vector store
    vector_store.add(chunks)

    return {
        "message": "PDF uploaded and processed successfully.",
        "total_chunks": len(chunks)
    }


@app.post("/ask")
async def ask_question(question: str):
    if not vector_store.text_chunks:
        raise HTTPException(status_code=400, detail="No document uploaded yet.")

    results = vector_store.search(question)
    answer = generate_answer(results, question)

    return {
        "question": question,
        "answer": answer
    }