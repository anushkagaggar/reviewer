from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path


class SimpleRetriever:
    def __init__(self, kb_path: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.documents = []
        self.embeddings = []

        self._load_documents(kb_path)

    def _load_documents(self, kb_path: str):
        kb_dir = Path(kb_path)

        for file in kb_dir.glob("*.txt"):
            text = file.read_text(encoding="utf-8")

            self.documents.append({
                "source": file.name,
                "content": text
            })

        texts = [doc["content"] for doc in self.documents]

        self.embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def retrieve(self, query: str, top_k: int = 3):
        query_emb = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores = np.dot(self.embeddings, query_emb)

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for idx in top_indices:
            results.append({
                "source": self.documents[idx]["source"],
                "content": self.documents[idx]["content"],
                "score": float(scores[idx])
            })

        return results
