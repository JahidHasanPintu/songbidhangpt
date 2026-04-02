# 🇧🇩 SongbidhanGPT

> Open-source RAG-powered AI for the Constitution of Bangladesh — answers in Bangla & English

## Tech Stack
- **LLM**: Google Gemini 1.5 Flash (free tier)
- **Embeddings**: Google text-embedding-004 (free)
- **Vector DB**: ChromaDB (local, persistent)
- **Backend**: FastAPI + LangChain
- **Frontend**: Next.js 14 + Tailwind CSS

## Quick Start

### 1. Get Free API Key
Go to [Google AI Studio](https://aistudio.google.com/) → Create API Key (free, 1500 req/day)

### 2. Setup Backend
```bash
cd backend
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

pip install -r requirements.txt

# Add your PDF(s) to backend/data/pdfs/
# Then index them:
python scripts/ingest.py
```

### 3. Start Backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Docker (Production on VPS)
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API key
# Copy your PDFs to backend/data/pdfs/

docker-compose up -d

# Index PDFs inside container
docker exec songbidhangpt-backend python scripts/ingest.py
```

## Adding More PDFs
Simply drop new PDF files into `backend/data/pdfs/` and run:
```bash
python scripts/ingest.py --force
# or via API:
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{"force_reingest": false}'
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Ask a question |
| POST | `/api/v1/ingest` | Trigger PDF ingestion |
| GET  | `/api/v1/documents/list` | List PDFs & chunk count |
| GET  | `/health` | Health check |

## License
MIT — Open Source