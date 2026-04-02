import chromadb
from langchain_chroma import Chroma
from langchain.schema import Document
from app.config import settings
from app.core.embeddings import get_embeddings
from app.utils.logger import get_logger
from typing import List, Tuple
import os

logger = get_logger(__name__)


class VectorStore:
    def __init__(self):
        self.persist_directory = settings.CHROMA_DB_PATH
        self.collection_name = settings.COLLECTION_NAME
        self._store = None

    def _get_store(self) -> Chroma:
        if self._store is None:
            os.makedirs(self.persist_directory, exist_ok=True)
            self._store = Chroma(
                collection_name=self.collection_name,
                embedding_function=get_embeddings(),
                persist_directory=self.persist_directory,
            )
        return self._store

    def add_documents(self, documents: List[Document]) -> int:
        store = self._get_store()
        # Add in batches to avoid API rate limits
        batch_size = 50
        total = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            store.add_documents(batch)
            total += len(batch)
            logger.info(f"Embedded batch {i // batch_size + 1}: {total}/{len(documents)} chunks")
        return total

    def similarity_search(
        self, query: str, k: int = None
    ) -> List[Tuple[Document, float]]:
        k = k or settings.TOP_K_RESULTS
        store = self._get_store()
        results = store.similarity_search_with_relevance_scores(query, k=k)
        return results

    def get_count(self) -> int:
        try:
            return self._get_store()._collection.count()
        except Exception:
            return 0

    def collection_exists(self) -> bool:
        return self.get_count() > 0

    def reset_collection(self):
        client = chromadb.PersistentClient(path=self.persist_directory)
        try:
            client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception:
            pass
        self._store = None


vector_store = VectorStore()