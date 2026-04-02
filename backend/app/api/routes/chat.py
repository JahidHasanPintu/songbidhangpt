from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.core.rag_engine import rag_engine
from app.core.vector_store import vector_store
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint."""
    if not vector_store.collection_exists():
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is not ready. Please run the ingestion pipeline first."
        )

    try:
        response = await rag_engine.query(
            question=request.question,
            language=request.language,
            chat_history=request.chat_history or [],
        )
        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))