import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings
from app.utils.logger import get_logger
from typing import List
import re

logger = get_logger(__name__)


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "।", ".", "!", "?", " ", ""],  # Bangla-aware
            length_function=len,
        )

    def extract_text_from_pdf(self, pdf_path: str) -> List[dict]:
        """Extract text page by page from a PDF using PyMuPDF."""
        pages = []
        doc = fitz.open(pdf_path)
        filename = os.path.basename(pdf_path)

        logger.info(f"Extracting text from: {filename} ({len(doc)} pages)")

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            text = self._clean_text(text)
            if text.strip():
                pages.append({
                    "text": text,
                    "page": page_num,
                    "source": filename,
                })

        doc.close()
        logger.info(f"Extracted {len(pages)} pages from {filename}")
        return pages

    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove excessive whitespace but preserve paragraph breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        # Remove page numbers (common patterns)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        return text.strip()

    def _detect_article_reference(self, text: str) -> str:
        """Try to detect article number from chunk text."""
        # Bangla article pattern: ধারা ১, অনুচ্ছেদ ১
        bn_match = re.search(r'(ধারা|অনুচ্ছেদ)\s*(\d+)', text)
        if bn_match:
            return f"{bn_match.group(1)} {bn_match.group(2)}"

        # English article pattern: Article 1, Section 1
        en_match = re.search(r'(Article|Section|Part)\s*(\d+)', text, re.IGNORECASE)
        if en_match:
            return f"{en_match.group(1)} {en_match.group(2)}"

        return ""

    def process_pdf(self, pdf_path: str) -> List[Document]:
        """Process a single PDF into LangChain Documents."""
        pages = self.extract_text_from_pdf(pdf_path)
        documents = []

        for page_data in pages:
            # Create document chunks from each page
            chunks = self.text_splitter.split_text(page_data["text"])

            for chunk in chunks:
                if len(chunk.strip()) < 50:  # Skip tiny chunks
                    continue

                article_ref = self._detect_article_reference(chunk)
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": page_data["source"],
                        "page": page_data["page"],
                        "article": article_ref,
                    },
                )
                documents.append(doc)

        logger.info(f"Created {len(documents)} chunks from {os.path.basename(pdf_path)}")
        return documents

    def process_all_pdfs(self, pdf_dir: str) -> List[Document]:
        """Process all PDFs in a directory."""
        all_documents = []
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]

        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return []

        logger.info(f"Found {len(pdf_files)} PDF(s) to process: {pdf_files}")

        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            docs = self.process_pdf(pdf_path)
            all_documents.extend(docs)

        logger.info(f"Total chunks created: {len(all_documents)}")
        return all_documents


document_processor = DocumentProcessor()