from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import IngestRequest, IngestResponse
from app.core.document_processor import document_processor
from app.core.vector_store import vector_store
from app.config import settings
from app.utils.logger import get_logger
import os

router = APIRouter()
logger = get_logger(__name__)
_ingestion_status = {"running": False, "last_result": None}


def _run_ingestion(force: bool = False):
    global _ingestion_status
    _ingestion_status["running"] = True
    try:
        if force:
            vector_store.reset_collection()

        documents = document_processor.process_all_pdfs(settings.PDF_DIR)
        if not documents:
            _ingestion_status["last_result"] = {"status": "warning", "message": "No PDFs found"}
            return

        count = vector_store.add_documents(documents)
        _ingestion_status["last_result"] = {
            "status": "success",
            "chunks_created": count,
        }
        logger.info(f"Ingestion complete: {count} chunks")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        _ingestion_status["last_result"] = {"status": "error", "message": str(e)}
    finally:
        _ingestion_status["running"] = False


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest, background_tasks: BackgroundTasks):
    """Trigger PDF ingestion into the vector store."""
    if _ingestion_status["running"]:
        raise HTTPException(status_code=409, detail="Ingestion already in progress")

    background_tasks.add_task(_run_ingestion, force=request.force_reingest)

    return IngestResponse(
        status="started",
        documents_processed=0,
        chunks_created=0,
        message="Ingestion started in background. Check /health for status.",
    )


@router.get("/documents/list")
async def list_documents():
    """List all PDF files available."""
    pdf_dir = settings.PDF_DIR
    if not os.path.exists(pdf_dir):
        return {"pdfs": [], "total": 0}

    pdfs = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    return {
        "pdfs": pdfs,
        "total": len(pdfs),
        "vector_store_chunks": vector_store.get_count(),
    }