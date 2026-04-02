from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings
from app.utils.logger import get_logger
import importlib.metadata

logger = get_logger(__name__)

_embeddings = None


def _get_package_version(package: str) -> tuple:
    try:
        version_str = importlib.metadata.version(package)
        parts = version_str.split(".")
        return tuple(int(x) for x in parts[:2])
    except Exception:
        return (0, 0)


def _resolve_model_name(model: str) -> str:
    """
    langchain-google-genai < 4.0.0  → needs 'models/text-embedding-004'
    langchain-google-genai >= 4.0.0 → needs 'gemini-embedding-001'
    """
    major, _ = _get_package_version("langchain-google-genai")
    logger.info(f"  langchain-google-genai major version: {major}")

    if major >= 4:
        resolved = "gemini-embedding-001"
        logger.info(f"  v4+ detected → overriding model to '{resolved}'")
    else:
        # Ensure models/ prefix for older versions
        if not model.startswith("models/"):
            resolved = f"models/{model}"
        else:
            resolved = model
        logger.info(f"  v3 detected → using model '{resolved}'")

    return resolved


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        logger.info("=" * 50)
        logger.info("Initializing embedding model...")
        logger.info(f"  Model in config  : '{settings.EMBEDDING_MODEL}'")
        logger.info(f"  API key set      : {'YES' if settings.GOOGLE_API_KEY else 'NO'}")
        logger.info(f"  API key prefix   : '{settings.GOOGLE_API_KEY[:8]}...'")

        resolved_model = _resolve_model_name(settings.EMBEDDING_MODEL)
        logger.info(f"  Resolved model   : '{resolved_model}'")

        try:
            _embeddings = GoogleGenerativeAIEmbeddings(
                model=resolved_model,
                google_api_key=settings.GOOGLE_API_KEY,
            )
            logger.info("  Instance created OK — running test embed...")
            test_result = _embeddings.embed_query("test")
            logger.info(f"  Test embed OK — vector dimensions: {len(test_result)}")
        except Exception as e:
            logger.error(f"  FAILED: {type(e).__name__}: {e}")
            _embeddings = None
            raise

        logger.info("=" * 50)
    else:
        logger.info("Reusing existing embedding instance")

    return _embeddings