import os
import numpy as np
try:
    from app.model_utils import get_whisper_model, get_embed_model
except ImportError:
    from model_utils import get_whisper_model, get_embed_model

import chromadb

DATA_DIR = "app/data"
INDEX_DIR = "app/index"

# Ensure absolute path for Docker volume mount
INDEX_DIR_ABS = os.path.abspath(INDEX_DIR)
os.makedirs(INDEX_DIR_ABS, exist_ok=True)
print("[DEBUG] ChromaDB index absolute path:", INDEX_DIR_ABS)

def process_all_videos():
    whisper_model = get_whisper_model()
    embed_model = get_embed_model()
    client = chromadb.PersistentClient(path=INDEX_DIR_ABS)
    collection = client.get_or_create_collection("video_segments")

    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".mp4"):
            video_path = os.path.join(DATA_DIR, fname)
            print(f"Transcribing {fname} ...")
            result = whisper_model.transcribe(video_path)
            segments = result['segments']
            texts = []
            metadatas = []
            ids = []
            for i, seg in enumerate(segments):
                text = seg['text'].strip()
                if not text:
                    continue  # skip empty segments
                texts.append(text)
                metadatas.append({
                    "video_id": fname,
                    "start": seg['start'],
                    "end": seg['end']
                })
                ids.append(f"{fname}_{i}")
            if not texts:
                continue
            print("Generating embeddings ...")
            embeddings = embed_model.encode(texts, show_progress_bar=True).tolist()
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
    print("Indexing complete.")

if __name__ == "__main__":
    process_all_videos() 