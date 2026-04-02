from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Language(str, Enum):
    BANGLA = "bn"
    ENGLISH = "en"
    AUTO = "auto"


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    language: Language = Language.AUTO
    chat_history: Optional[List[dict]] = []


class SourceDocument(BaseModel):
    content: str
    source: str
    page: Optional[int] = None
    article: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    language_detected: str
    question: str


class IngestRequest(BaseModel):
    force_reingest: bool = False


class IngestResponse(BaseModel):
    status: str
    documents_processed: int
    chunks_created: int
    message: str


class HealthResponse(BaseModel):
    status: str
    version: str
    vector_store_ready: bool
    documents_count: int