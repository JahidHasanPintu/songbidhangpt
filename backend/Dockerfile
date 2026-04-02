# ------------------------------
# Debug Dockerfile for backend
# ------------------------------
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libsqlite3-dev \
    libnss3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install requirements with verbose logging
# This will print all compilation steps and errors
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Copy the rest of your app
COPY . .

# Create required directories
RUN mkdir -p data/pdfs data/chroma_db

# Expose port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]