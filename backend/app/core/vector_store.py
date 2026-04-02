import chromadb
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings
from app.core.embeddings import get_embeddings
from app.utils.logger import get_logger
from typing import List, Tuple
import os


logger = get_logger(__name__)


class VectorStore:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.persist_directory = settings.CHROMA_DB_PATH
        self.collection_name = settings.COLLECTION_NAME
        self._store = None

    def _get_store(self) -> Chroma:
        if self._store is None:
            os.makedirs(self.persist_directory, exist_ok=True)
            self._store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        return self._store

    def add_documents(self, documents: List[Document]) -> int:
        """Add documents to the vector store."""
        store = self._get_store()
        store.add_documents(documents)
        logger.info(f"Added {len(documents)} chunks to vector store")
        return len(documents)

    def similarity_search(self, query: str, k: int = None) -> List[Tuple[Document, float]]:
        """Search for similar documents."""
        k = k or settings.TOP_K_RESULTS
        store = self._get_store()
        # Use query task type for search
        results = store.similarity_search_with_relevance_scores(
            query, k=k,
            embedding=GoogleGenerativeAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                task_type="retrieval_query",
            )
        )
        return results

    def get_count(self) -> int:
        """Get total number of stored chunks."""
        try:
            store = self._get_store()
            return store._collection.count()
        except Exception:
            return 0

    def collection_exists(self) -> bool:
        """Check if the collection has documents."""
        return self.get_count() > 0

    def reset_collection(self):
        """Delete and recreate collection."""
        client = chromadb.PersistentClient(path=self.persist_directory)
        try:
            client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception:
            pass
        self._store = None


# Singleton instance
vector_store = VectorStore()