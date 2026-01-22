# backend/app/kb_builder.py

import os
import json
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings

BASE = Path(__file__).parent
KB_FILE = BASE / "kb.jsonl"
INDEX_FILE = BASE / "legal_faiss_index"

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load KB
def load_kb(path):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            docs.append(obj)
    return docs

# Build FAISS
def build():
    if not KB_FILE.exists():
        raise FileNotFoundError(f"{KB_FILE} not found.")
    print("Loading KB...")
    docs = load_kb(KB_FILE)
    texts = [d["text"] for d in docs]

    print(f"Loaded {len(texts)} documents. Creating embeddings...")
    embeddings_model = SentenceTransformerEmbeddings(model_name=EMB_MODEL)

    print("Building FAISS vectorstore...")
    vectorstore = FAISS.from_texts(texts=texts, embedding=embeddings_model)
    vectorstore.save_local(str(INDEX_FILE))
    print(f"Built FAISS index and saved to {INDEX_FILE}")


if __name__ == "__main__":
    build()
