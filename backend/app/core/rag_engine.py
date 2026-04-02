from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import Document
from app.core.vector_store import vector_store
from app.core.llm import get_llm
from app.models.schemas import ChatResponse, SourceDocument, Language
from app.utils.logger import get_logger
from typing import List, Tuple
import re

logger = get_logger(__name__)

# ─── Prompts ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_BN = """আপনি SongbidhanGPT — বাংলাদেশের সংবিধান বিষয়ক একজন বিশেষজ্ঞ AI সহকারী।

আপনার কাজ হলো নিচের প্রসঙ্গ (context) ব্যবহার করে প্রশ্নের সঠিক ও বিস্তারিত উত্তর বাংলায় দেওয়া।

নিয়মাবলী:
- শুধুমাত্র প্রদত্ত প্রসঙ্গ থেকে উত্তর দিন
- প্রাসঙ্গিক ধারা বা অনুচ্ছেদের উল্লেখ করুন
- যদি প্রসঙ্গে উত্তর না থাকে, তাহলে সৎভাবে বলুন
- আইনি ভাষা সহজ করে বুঝিয়ে দিন
- উত্তর সংগঠিত ও পরিষ্কার রাখুন

প্রসঙ্গ:
{context}

প্রশ্ন: {question}

উত্তর (বাংলায়):"""

SYSTEM_PROMPT_EN = """You are SongbidhanGPT — an expert AI assistant on the Constitution of Bangladesh.

Your task is to answer questions accurately and thoroughly using the context below.

Rules:
- Answer ONLY from the provided context
- Reference relevant Articles or Sections when applicable
- If the answer is not in the context, honestly say so
- Simplify legal language for clarity
- Keep answers organized and clear

Context:
{context}

Question: {question}

Answer (in English):"""


class RAGEngine:
    def __init__(self):
        self.llm = get_llm()

    def _detect_language(self, text: str) -> str:
        """Detect if text is Bangla or English."""
        # Check for Bangla Unicode range
        bangla_chars = len(re.findall(r'[\u0980-\u09FF]', text))
        total_alpha = len(re.findall(r'[a-zA-Z\u0980-\u09FF]', text))

        if total_alpha == 0:
            return "en"

        bangla_ratio = bangla_chars / total_alpha
        return "bn" if bangla_ratio > 0.3 else "en"

    def _format_context(self, docs: List[Tuple[Document, float]]) -> str:
        """Format retrieved documents into context string."""
        context_parts = []
        for doc, score in docs:
            if score < 0.3:  # Skip very low relevance
                continue
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "")
            article = doc.metadata.get("article", "")

            header = f"[Source: {source}"
            if page:
                header += f", Page {page}"
            if article:
                header += f", {article}"
            header += "]"

            context_parts.append(f"{header}\n{doc.page_content}")

        return "\n\n---\n\n".join(context_parts)

    def _build_sources(self, docs: List[Tuple[Document, float]]) -> List[SourceDocument]:
        """Build source list for response."""
        sources = []
        seen = set()
        for doc, score in docs:
            if score < 0.3:
                continue
            key = (doc.metadata.get("source"), doc.metadata.get("page"))
            if key not in seen:
                seen.add(key)
                sources.append(SourceDocument(
                    content=doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                    source=doc.metadata.get("source", "Unknown"),
                    page=doc.metadata.get("page"),
                    article=doc.metadata.get("article", ""),
                ))
        return sources

    async def query(
        self,
        question: str,
        language: Language = Language.AUTO,
        chat_history: list = [],
    ) -> ChatResponse:
        """Main RAG query pipeline."""
        logger.info(f"Processing query: {question[:80]}...")

        # 1. Detect language
        if language == Language.AUTO:
            detected_lang = self._detect_language(question)
        else:
            detected_lang = language.value

        # 2. Retrieve relevant documents
        docs_with_scores = vector_store.similarity_search(question)

        if not docs_with_scores:
            no_answer = (
                "দুঃখিত, সংবিধানে এই বিষয়ে কোনো তথ্য খুঁজে পাওয়া যায়নি।"
                if detected_lang == "bn"
                else "Sorry, no relevant information was found in the Constitution for this query."
            )
            return ChatResponse(
                answer=no_answer,
                sources=[],
                language_detected=detected_lang,
                question=question,
            )

        # 3. Format context
        context = self._format_context(docs_with_scores)

        # 4. Build prompt
        prompt_template = SYSTEM_PROMPT_BN if detected_lang == "bn" else SYSTEM_PROMPT_EN
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # 5. Build chain
        chain = prompt | self.llm | StrOutputParser()

        # 6. Run chain
        answer = await chain.ainvoke({
            "context": context,
            "question": question,
        })

        # 7. Build sources
        sources = self._build_sources(docs_with_scores)

        logger.info(f"Generated answer in '{detected_lang}' with {len(sources)} sources")

        return ChatResponse(
            answer=answer.strip(),
            sources=sources,
            language_detected=detected_lang,
            question=question,
        )


rag_engine = RAGEngine()