"""
FastAPI entry point.
POST /chat — routes query to show or explain mode.
POST /upload — accepts a PDF, processes it, rebuilds the embedding index.
"""

import json
import shutil
import tempfile
import time
from pathlib import Path
from typing import List, Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from retriever.search import retrieve, reset_index
from llm.inference import explain, explain_stream
from utils.preprocessing import extract_and_clean
from utils.chunking import build_chunks, save_chunks
from retriever.index import build_index

app = FastAPI(title="Offline Textbook Chatbot")

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    mode: str
    answer: str


def route_query(query: str) -> str:
    keywords = ["show", "display", "what is written", "give me the text"]
    if any(kw in query.lower() for kw in keywords):
        return "retrieval_only"
    return "explain"


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix
    chapter_name = Path(file.filename).stem

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    pages = extract_and_clean(tmp_path)
    new_chunks = build_chunks(pages, chapter=chapter_name)

    data_path = Path(__file__).parent.parent / "data" / "textbook.json"
    existing = []
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            existing = json.load(f)

    max_id = max((c["id"] for c in existing), default=0)
    for i, chunk in enumerate(new_chunks):
        chunk["id"] = max_id + i + 1

    save_chunks(existing + new_chunks)
    build_index()
    reset_index()

    Path(tmp_path).unlink(missing_ok=True)

    return {"chapter": chapter_name, "chunks": len(new_chunks)}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    query = request.query.strip()
    mode = route_query(query)
    chunks = retrieve(query, top_k=3)

    if not chunks:
        return ChatResponse(mode=mode, answer="No relevant content found in the textbook.")

    if mode == "retrieval_only":
        answer = chunks[0]["content"]
    else:
        context = ' '.join(chunks[0]['content'].split()[:200])
        answer = explain(context, query, request.history)

    return ChatResponse(mode=mode, answer=answer)


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    query = request.query.strip()

    t0 = time.time()
    chunks = retrieve(query, top_k=2)
    print(f"Retrieval: {time.time() - t0:.3f}s", flush=True)

    if not chunks:
        def empty():
            yield "No relevant content found in the textbook."
        return StreamingResponse(empty(), media_type="text/plain")

    context = ' '.join(' '.join(c['content'].split()[:75]) for c in chunks)

    t1 = time.time()
    def timed_stream():
        first_token = True
        for token in explain_stream(context, query):
            if first_token:
                print(f"Time to first token: {time.time() - t1:.3f}s", flush=True)
                first_token = False
            yield token

    return StreamingResponse(timed_stream(), media_type="text/plain")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = FRONTEND_DIR / full_path
    if file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
