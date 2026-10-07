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

  if [ -n "$NLP_PID" ] && kill -0 "$NLP_PID" 2>/dev/null; then
    echo "Stopping NLP Service (PID: $NLP_PID)..."
    kill -TERM "$NLP_PID" 2>/dev/null || true
  fi

  sleep 0.5 2>/dev/null || true
  echo "All services stopped cleanly."
  exit 0
}

trap cleanup INT TERM EXIT

# 1. Start Go Backend
echo "Starting Go Backend on http://localhost:8080..."
(
  cd "$ROOT_DIR/Backend"
  go run main.go
) &
BACKEND_PID=$!

# 2. Optional: Start NLP Service if --with-nlp or --all is passed
if [[ "$*" == *"--with-nlp"* ]] || [[ "$*" == *"--all"* ]]; then
  if [ -d "$ROOT_DIR/Nlp-service/.venv" ]; then
    echo "Starting NLP Service on http://localhost:5000..."
    (
      cd "$ROOT_DIR/Nlp-service"
      source .venv/bin/activate
      uvicorn app.main:app --port 5000 --reload
    ) &
    NLP_PID=$!
  else
    echo "Warning: Nlp-service/.venv not found. Skipping NLP service."
  fi
fi

# 3. Start React + TypeScript Frontend
echo "Starting Frontend Vite Server on http://localhost:5173..."
(
  cd "$ROOT_DIR/Frontend"
  npm run dev
) &
FRONTEND_PID=$!

echo "----------------------------------------------------"
echo "Backend:  http://localhost:8080"
echo "Frontend: http://localhost:5173"
if [ -n "$NLP_PID" ]; then
  echo "NLP API:  http://localhost:5000 (Docs: /docs)"
fi
echo "Press Ctrl+C to stop all services."
echo "----------------------------------------------------"

wait
