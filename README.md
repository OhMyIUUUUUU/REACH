# REACH

Fullstack monorepo with React TypeScript frontend, Go backend, Python NLP / Machine Learning microservice, and PostgreSQL database layer.

## Architecture

- [Frontend/](file:///home/ohmyiu/Documents/REACH/Frontend) - React 19 + TypeScript + Vite + Tailwind CSS v4
- [Backend/](file:///home/ohmyiu/Documents/REACH/Backend) - Go 1.27 HTTP REST API (`reach/backend`)
- [Nlp-service/](file:///home/ohmyiu/Documents/REACH/Nlp-service) - Python FastAPI + Machine Learning / NLP service
- [DB/](file:///home/ohmyiu/Documents/REACH/DB) - PostgreSQL Docker orchestration, schema migrations, and seeds
- [Docs/](file:///home/ohmyiu/Documents/REACH/Docs) - System specifications and design documents

---

## Quickstart

### 1. Install All Dependencies
```bash
./install-deps.sh
```
*Installs npm packages for Frontend, Go modules for Backend, and creates the Python virtual environment with NLP packages for Nlp-service.*

---

### 2. Run Full Stack (Frontend + Backend)
```bash
./start-dev.sh
```
*Runs Go backend on `:8080` and React dev server on `:5173` concurrently. Press `Ctrl+C` to stop both.*

*(Optional: Run `./start-dev.sh --with-nlp` to include the Python NLP service)*

---

### Individual Services

### 1. Database (PostgreSQL)
```bash
cd DB
docker compose up -d
./scripts/migrate.sh
```
Runs PostgreSQL 16 on port `5432`.

### 2. Backend (Go)
```bash
cd Backend
go run main.go
```
The API server starts on `http://localhost:8080`.
- Health check: `http://localhost:8080/api/health`
- Info: `http://localhost:8080/api/info`

### 3. Frontend (React + TypeScript)
```bash
cd Frontend
npm run dev
```
The Vite development server starts on `http://localhost:5173`.

### 4. NLP & Machine Learning Service (Python)
```bash
cd Nlp-service
source .venv/bin/activate
uvicorn app.main:app --port 5000 --reload
```
The NLP service starts on `http://localhost:5000`.
- Swagger Docs: `http://localhost:5000/docs`
- Health check: `http://localhost:5000/api/nlp/health`
