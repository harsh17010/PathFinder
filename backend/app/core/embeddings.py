from sentence_transformers import SentenceTransformer
from app.core.config import settings
from typing import List

class EmbeddingService:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def load(self):
        if self.model is None:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def encode(self, text: str) -> List[float]:
        if not self.model:
            self.load()
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        if not self.model:
            self.load()
        return self.model.encode(texts).tolist()
