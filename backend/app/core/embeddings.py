from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

_embeddings = None


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        logger.info("="*50)
        logger.info("Initializing embedding model...")
        logger.info(f"  Model name   : '{settings.EMBEDDING_MODEL}'")
        logger.info(f"  API key set  : {'YES' if settings.GOOGLE_API_KEY else 'NO'}")
        logger.info(f"  API key prefix: '{settings.GOOGLE_API_KEY[:8]}...'")
        try:
            _embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
            )
            logger.info("  Embedding model initialized OK")

            # Test with a single string immediately
            logger.info("  Running test embed on single string...")
            test_result = _embeddings.embed_query("test")
            logger.info(f"  Test embed OK — vector size: {len(test_result)}")
        except Exception as e:
            logger.error(f"  FAILED to initialize embeddings: {type(e).__name__}: {e}")
            raise
        logger.info("="*50)
    else:
        logger.info("Reusing existing embedding instance")
    return _embeddings


def embed_texts_debug(texts: list) -> list:
    """Debug helper — embeds a small list and logs everything."""
    logger.info(f"embed_texts_debug: embedding {len(texts)} text(s)")
    emb = get_embeddings()
    for i, t in enumerate(texts):
        logger.info(f"  [{i}] length={len(t)}, preview='{t[:60].strip()}'")
    try:
        results = emb.embed_documents(texts)
        logger.info(f"  embed_documents returned {len(results)} vectors")
        return results
    except Exception as e:
        logger.error(f"  embed_documents FAILED: {type(e).__name__}: {e}")
        raise