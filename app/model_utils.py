import whisper
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

WHISPER_MODEL = None
EMBED_MODEL = None

def get_whisper_model():
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        WHISPER_MODEL = whisper.load_model("base")
    return WHISPER_MODEL

def get_embed_model():
    global EMBED_MODEL
    if EMBED_MODEL is None:
        EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return EMBED_MODEL

def save_faiss_index(index, path):
    faiss.write_index(index, path)

def load_faiss_index(path):
    return faiss.read_index(path)

def save_metadata(metadata, path):
    with open(path, "wb") as f:
        pickle.dump(metadata, f)

def load_metadata(path):
    with open(path, "rb") as f:
        return pickle.load(f) 