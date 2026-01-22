# backend/retriever.py
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

BASE = os.path.dirname(__file__)
PICKLE_FILE = os.path.join(BASE, "legal_faiss_index.pkl")

class Retriever:
    def __init__(self):
        if not os.path.exists(PICKLE_FILE):
            raise FileNotFoundError("legal_faiss_index.pkl not found. Run kb_builder.py first.")
        with open(PICKLE_FILE, "rb") as f:
            payload = pickle.load(f)
        self.index = payload["index"]
        self.docs = payload["docs"]
        self.emb_model = payload["emb_model"]
        self.dim = payload["embeddings_dim"]
        # load embedding model for queries
        self.model = SentenceTransformer(self.emb_model)

    def get_relevant_documents(self, query: str, k: int = 4):
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(q_emb, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.docs):
                doc = self.docs[idx].copy()
                # convert distance to simple score
                doc['score'] = float(1.0 / (1.0 + float(dist)))
                results.append(doc)
        return results
