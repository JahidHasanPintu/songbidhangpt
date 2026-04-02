from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_llm():
    """Returns Gemini LLM instance."""
    logger.info(f"Loading LLM: {settings.GEMINI_MODEL}")
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.TEMPERATURE,
        max_output_tokens=settings.MAX_TOKENS,
        convert_system_message_to_human=True,
    )