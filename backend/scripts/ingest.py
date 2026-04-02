#!/usr/bin/env python3
"""
Run this script to index your PDFs into the vector store.
Usage: python scripts/ingest.py [--force]
"""
import sys
import os
import argparse

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.config import settings
from app.core.document_processor import document_processor
from app.core.vector_store import vector_store
from app.utils.logger import get_logger

logger = get_logger("ingest")


def main():
    parser = argparse.ArgumentParser(description="Ingest PDFs into SongbidhanGPT")
    parser.add_argument("--force", action="store_true", help="Force re-ingestion (clears existing data)")
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("SongbidhanGPT — PDF Ingestion Pipeline")
    logger.info("=" * 50)

    if not os.path.exists(settings.PDF_DIR):
        os.makedirs(settings.PDF_DIR)
        logger.warning(f"Created PDF directory: {settings.PDF_DIR}")
        logger.warning("Please add your PDF files and run again.")
        return

    if args.force:
        logger.info("Force mode: resetting vector store...")
        vector_store.reset_collection()

    if vector_store.collection_exists() and not args.force:
        logger.info(f"Vector store already has {vector_store.get_count()} chunks.")
        logger.info("Use --force to re-ingest. Exiting.")
        return

    documents = document_processor.process_all_pdfs(settings.PDF_DIR)

    if not documents:
        logger.error("No documents were processed. Check your PDF directory.")
        return

    logger.info(f"Adding {len(documents)} chunks to vector store...")
    count = vector_store.add_documents(documents)

    logger.info("=" * 50)
    logger.info(f"✅ Ingestion complete!")
    logger.info(f"   Chunks stored: {count}")
    logger.info(f"   Total in DB  : {vector_store.get_count()}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()