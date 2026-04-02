from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import chat, documents
from app.core.vector_store import vector_store
from app.models.schemas import HealthResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG-powered Bangladesh Constitution Q&A in Bangla & English",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    count = vector_store.get_count()
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        vector_store_ready=count > 0,
        documents_count=count,
    )


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }