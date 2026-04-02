from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_embeddings():
    """Returns Google Generative AI embedding model."""
    logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
    )