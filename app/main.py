from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from fastapi.responses import JSONResponse

try:
    from app.model_utils import get_embed_model
except ImportError:
    from model_utils import get_embed_model

import chromadb

INDEX_DIR = "app/index"

app = FastAPI(title="Video Query Relevance System")

embed_model = get_embed_model()
client = chromadb.PersistentClient(path=INDEX_DIR)
collection = client.get_or_create_collection("video_segments")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 1

@app.post("/search")
def search(req: QueryRequest):
    query_emb = embed_model.encode([req.query]).tolist()
    results = collection.query(
        query_embeddings=query_emb,
        n_results=req.top_k,
        include=["metadatas", "documents"]
    )
    if not results["ids"] or not results["ids"][0]:
        raise HTTPException(status_code=404, detail="No results found.")
    output = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        video_id = meta["video_id"]
        start = meta["start"]
        end = meta["end"]
        # Construct a direct video link (assuming videos are served from /videos/{video_id})
        video_url = f"/videos/{video_id}?t={int(start)}"
        output.append({
            "video_id": video_id,
            "start": start,
            "end": end,
            "text": results["documents"][0][i],
            "video_url": video_url
        })
    return {"results": output}

class EmbeddingRequest(BaseModel):
    query: str

@app.post("/embedding")
def get_embedding(req: EmbeddingRequest):
    embedding = embed_model.encode([req.query]).tolist()[0]
    return {"embedding": embedding}

@app.get("/segments")
def get_all_segments():
    # Query all segments in the collection
    results = collection.get(include=["embeddings", "metadatas", "documents", "ids"])
    segments = []
    for i in range(len(results["ids"])):
        meta = results["metadatas"][i]
        segments.append({
            "id": results["ids"][i],
            "video_id": meta.get("video_id"),
            "start": meta.get("start"),
            "end": meta.get("end"),
            "text": results["documents"][i],
            "embedding": results["embeddings"][i],
        })
    return JSONResponse(content={"segments": segments}) 