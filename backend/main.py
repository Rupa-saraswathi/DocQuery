import os
import pymupdf as fitz
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from dotenv import load_dotenv

load_dotenv()

# New SDK: create a client instead of calling genai.configure()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    all_chunks = []
    all_metadatas = []
    all_ids = []
    chunk_counter = 0

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if not text:
            continue

        page_chunks = chunk_text(text)
        for chunk in page_chunks:
            chunk_counter += 1
            all_chunks.append(chunk)
            all_metadatas.append({
                "document_name": file.filename,
                "page_number": page_number
            })
            all_ids.append(f"{file.filename}_p{page_number}_c{chunk_counter}")

    doc.close()

    if all_chunks:
        collection.add(
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=all_ids
        )

    return {
        "filename": file.filename,
        "total_pages": page_number,
        "total_chunks_stored": len(all_chunks)
    }


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@app.post("/query")
async def query_documents(request: QueryRequest):
    results = collection.query(
        query_texts=[request.question],
        n_results=request.top_k
    )

    retrieved_chunks = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]

    if not retrieved_chunks:
        return {
            "answer": "No documents have been uploaded yet.",
            "sources": []
        }

    context_block = ""
    for chunk, meta in zip(retrieved_chunks, retrieved_metadatas):
        context_block += f"\n[Page {meta['page_number']}]\n{chunk}\n"

    prompt = f"""You are a study assistant. Answer the question using ONLY the context below.
Cite the page number(s) for every claim, like (p. 3).
If the answer is not fully contained in the context, say so clearly instead of guessing.

Context:
{context_block}

Question: {request.question}

Answer:"""

    # New SDK call style
    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    pages_used = sorted(set(m["page_number"] for m in retrieved_metadatas))

    return {
        "answer": response.text,
        "sources": [{"page": p} for p in pages_used]
    }