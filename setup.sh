#!/bin/bash

# Exit on error
set -e

echo "Creating project structure..."

# Backend structure
mkdir -p backend/app/api/routes
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/utils
mkdir -p backend/data/pdfs
mkdir -p backend/data/chroma_db
mkdir -p backend/scripts
mkdir -p backend/tests

# Frontend structure
mkdir -p frontend/src/app
mkdir -p frontend/src/components
mkdir -p frontend/src/lib
mkdir -p frontend/public

# Nginx & GitHub
mkdir -p nginx
mkdir -p .github/workflows

# Create backend files
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/config.py

touch backend/app/api/__init__.py
touch backend/app/api/routes/__init__.py
touch backend/app/api/routes/chat.py
touch backend/app/api/routes/documents.py

touch backend/app/core/__init__.py
touch backend/app/core/rag_engine.py
touch backend/app/core/embeddings.py
touch backend/app/core/vector_store.py
touch backend/app/core/llm.py
touch backend/app/core/document_processor.py

touch backend/app/models/__init__.py
touch backend/app/models/schemas.py

touch backend/app/utils/__init__.py
touch backend/app/utils/logger.py

touch backend/scripts/ingest.py
touch backend/tests/test_rag.py

touch backend/.env.example
touch backend/requirements.txt
touch backend/Dockerfile

# Create frontend files
touch frontend/src/app/layout.tsx
touch frontend/src/app/page.tsx
touch frontend/src/app/globals.css

touch frontend/src/components/ChatWindow.tsx
touch frontend/src/components/MessageBubble.tsx
touch frontend/src/components/SourceCard.tsx
touch frontend/src/components/LanguageToggle.tsx

touch frontend/src/lib/api.ts

touch frontend/package.json
touch frontend/tailwind.config.ts
touch frontend/Dockerfile

# Root files
touch docker-compose.yml
touch nginx/nginx.conf
touch .github/workflows/ci.yml
touch .gitignore
touch README.md

echo "Project structure created successfully!"