#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "===================================================="
echo "          Starting REACH Development Stack         "
echo "===================================================="

BACKEND_PID=""
FRONTEND_PID=""
NLP_PID=""

cleanup() {
  echo ""
  echo "Stopping all REACH services..."
  
  if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo "Stopping Frontend (PID: $FRONTEND_PID)..."
    kill -TERM "$FRONTEND_PID" 2>/dev/null || true
  fi

  if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "Stopping Backend (PID: $BACKEND_PID)..."
    kill -TERM "$BACKEND_PID" 2>/dev/null || true
  fi

  sleep 0.5 2>/dev/null || true
  echo "All services stopped cleanly."
  exit 0
}

trap cleanup INT TERM EXIT

# 1. Start Python FastAPI Backend (with integrated NLP engine)
echo "Starting Python FastAPI Backend on http://localhost:8080..."
(
  cd "$ROOT_DIR/Backend"
  if [ -d ".venv" ]; then
    source .venv/bin/activate
  fi
  python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
) &
BACKEND_PID=$!

# 2. Start React + TypeScript Frontend
echo "Starting Frontend Vite Server on http://localhost:5173..."
(
  cd "$ROOT_DIR/Frontend"
  npm run dev
) &
FRONTEND_PID=$!

echo "----------------------------------------------------"
echo "Backend (REST + NLP): http://localhost:8080 (Docs: /docs)"
echo "Frontend App:        http://localhost:5173"
echo "Press Ctrl+C to stop all services."
echo "----------------------------------------------------"

wait
