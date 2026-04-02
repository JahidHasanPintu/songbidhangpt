import chromadb
from langchain_chroma import Chroma
from langchain.schema import Document
from app.config import settings
from app.core.embeddings import get_embeddings, embed_texts_debug
from app.utils.logger import get_logger
from typing import List, Tuple
import os

logger = get_logger(__name__)


class VectorStore:
    def __init__(self):
        self.persist_directory = settings.CHROMA_DB_PATH
        self.collection_name = settings.COLLECTION_NAME
        self._store = None
        logger.info(f"VectorStore init — persist_dir='{self.persist_directory}', collection='{self.collection_name}'")

    def _get_store(self) -> Chroma:
        if self._store is None:
            logger.info("Creating Chroma store instance...")
            logger.info(f"  persist_directory : {self.persist_directory}")
            logger.info(f"  collection_name   : {self.collection_name}")
            os.makedirs(self.persist_directory, exist_ok=True)
            try:
                self._store = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=get_embeddings(),
                    persist_directory=self.persist_directory,
                )
                logger.info("  Chroma store created OK")
            except Exception as e:
                logger.error(f"  Chroma store creation FAILED: {type(e).__name__}: {e}")
                raise
        return self._store

    def add_documents(self, documents: List[Document]) -> int:
        logger.info("="*50)
        logger.info(f"add_documents called with {len(documents)} total chunks")

        store = self._get_store()
        batch_size = 25  # reduced batch size to isolate issues
        total = 0

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(documents) + batch_size - 1) // batch_size

            logger.info(f"  Batch {batch_num}/{total_batches} — {len(batch)} chunks")

            # Log first chunk of each batch for inspection
            first = batch[0]
            logger.info(f"    First chunk preview : '{first.page_content[:80].strip()}'")
            logger.info(f"    First chunk metadata: {first.metadata}")
            logger.info(f"    First chunk length  : {len(first.page_content)} chars")

            # Check for any empty or suspiciously short chunks
            empty = [j for j, d in enumerate(batch) if len(d.page_content.strip()) < 10]
            if empty:
                logger.warning(f"    WARNING: {len(empty)} chunk(s) are very short at indices {empty}")

            try:
                # Test raw embedding on first chunk text before sending to Chroma
                logger.info(f"    Testing raw embed on first chunk text...")
                embed_texts_debug([batch[0].page_content[:200]])
                logger.info(f"    Raw embed test passed — proceeding with batch")

                store.add_documents(batch)
                total += len(batch)
                logger.info(f"    Batch {batch_num} added OK — total so far: {total}")

            except Exception as e:
                logger.error(f"    Batch {batch_num} FAILED: {type(e).__name__}: {e}")
                logger.error(f"    Full error: {e}")

                # Try to isolate which chunk caused the failure
                logger.info(f"    Trying chunks one-by-one to isolate bad chunk...")
                for j, doc in enumerate(batch):
                    try:
                        store.add_documents([doc])
                        total += 1
                        logger.info(f"      Chunk {i+j} OK")
                    except Exception as inner_e:
                        logger.error(f"      Chunk {i+j} FAILED: {inner_e}")
                        logger.error(f"      Bad chunk content: '{doc.page_content[:200]}'")
                        logger.error(f"      Bad chunk metadata: {doc.metadata}")

        logger.info(f"add_documents complete — {total}/{len(documents)} chunks stored")
        logger.info("="*50)
        return total

    def similarity_search(
        self, query: str, k: int = None
    ) -> List[Tuple[Document, float]]:
        k = k or settings.TOP_K_RESULTS
        logger.info(f"similarity_search — query='{query[:60]}', k={k}")
        store = self._get_store()
        try:
            results = store.similarity_search_with_relevance_scores(query, k=k)
            logger.info(f"  Search returned {len(results)} results")
            for idx, (doc, score) in enumerate(results):
                logger.info(f"  [{idx}] score={score:.4f} source={doc.metadata.get('source')} page={doc.metadata.get('page')}")
            return results
        except Exception as e:
            logger.error(f"  similarity_search FAILED: {type(e).__name__}: {e}")
            raise

    def get_count(self) -> int:
        try:
            count = self._get_store()._collection.count()
            logger.info(f"get_count — {count} chunks in collection")
            return count
        except Exception as e:
            logger.error(f"get_count FAILED: {e}")
            return 0

    def collection_exists(self) -> bool:
        exists = self.get_count() > 0
        logger.info(f"collection_exists — {exists}")
        return exists

    def reset_collection(self):
        logger.info(f"Resetting collection '{self.collection_name}'...")
        try:
            client = chromadb.PersistentClient(path=self.persist_directory)
            client.delete_collection(self.collection_name)
            logger.info("  Collection deleted OK")
        except Exception as e:
            logger.warning(f"  Could not delete collection (may not exist): {e}")
        self._store = None
        logger.info("  Store instance cleared — will reinitialize on next use")


vector_store = VectorStore()