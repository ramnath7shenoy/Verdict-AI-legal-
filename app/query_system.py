# app/query_system.py
import faiss
import numpy as np

class DocumentQuerySystem:
    def __init__(self):
        # This should load FAISS and related vector index
        self.index = faiss.IndexFlatL2(768)
        self.documents = []

    def get_similar_documents(self, query_text: str, k: int = 5):
        # Dummy logic (replace with real embedding logic)
        query_vector = self._get_vector(query_text)
        _, indices = self.index.search(np.array([query_vector]), k)
        return [self.documents[i] for i in indices[0] if i < len(self.documents)]

    def format_similar_documents_context(self, docs):
        return "\n---\n".join(docs)

    def _get_vector(self, text: str):
        return np.random.rand(768).astype('float32')
