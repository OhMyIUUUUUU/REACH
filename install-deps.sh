#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "===================================================="
echo "       Installing REACH Project Dependencies        "
echo "===================================================="

# 1. Frontend Dependencies (React + TypeScript + Vite + Tailwind)
echo ""
echo "1. Installing Frontend dependencies (npm)..."
if [ -d "$ROOT_DIR/Frontend" ]; then
  (
    cd "$ROOT_DIR/Frontend"
    npm install
  )
  echo "Frontend dependencies installed."
else
  echo "Warning: Frontend directory not found."
fi

# 2. Backend Dependencies (Go Modules)
echo ""
echo "2. Installing Backend dependencies (Go modules)..."
if [ -d "$ROOT_DIR/Backend" ]; then
  (
    cd "$ROOT_DIR/Backend"
    go mod download
    go mod tidy
  )
  echo "Backend dependencies installed."
else
  echo "Warning: Backend directory not found."
fi

# 3. NLP & Machine Learning Dependencies (Python)
echo ""
echo "3. Installing NLP Service dependencies (Python venv & pip)..."
if [ -d "$ROOT_DIR/Nlp-service" ]; then
  (
    cd "$ROOT_DIR/Nlp-service"
    if [ ! -d ".venv" ]; then
      echo "Creating Python virtual environment (.venv)..."
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
    echo "Downloading spaCy English language model (en_core_web_sm)..."
    python -m spacy download en_core_web_sm || true
  )
  echo "NLP Service dependencies installed."
else
  echo "Warning: Nlp-service directory not found."
fi

echo ""
echo "===================================================="
echo "All dependencies installed successfully!"
echo "Run ./start-dev.sh to start the development servers."
echo "===================================================="
