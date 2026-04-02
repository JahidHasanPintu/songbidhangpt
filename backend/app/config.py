from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SongbidhanGPT"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API Keys
    GOOGLE_API_KEY: str

    # RAG
    CHROMA_DB_PATH: str = "./data/chroma_db"
    PDF_DIR: str = "./data/pdfs"
    COLLECTION_NAME: str = "songbidhan_docs"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5

    # LLM
    GEMINI_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.1

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()