# REACH Backend Service

Python FastAPI REST backend service for the REACH platform, featuring PostgreSQL ORM, JWT Authentication, and Scikit-Learn/NLTK Reviewer Matching.

## Tech Stack
- **Framework**: Python 3.12+ (tested with Python 3.14) & FastAPI
- **ASGI Server**: Uvicorn
- **Database ORM**: SQLAlchemy 2.0 with PostgreSQL (`psycopg`)
- **Authentication**: JWT (email/password) with native `bcrypt`
- **NLP & Matching**: Scikit-Learn (TF-IDF & Cosine Similarity) + NLTK
- **Testing**: Pytest & HTTPX

---

## Getting Started

### 1. Setup Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Ensure PostgreSQL is running (e.g., via `cd ../DB && docker compose up -d`) or rely on the configured `DATABASE_URL`.

### 3. Run Development Server
```bash
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
The server will start on port `8080`:
- Interactive Swagger UI: `http://localhost:8080/docs`
- ReDoc API reference: `http://localhost:8080/redoc`

### 4. Run Test Suite
```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/
```

---

## API Endpoints Overview

### Health & Metadata
- `GET /` - Root service index
- `GET /api/health` - Service health status, UTC timestamp, and uptime
- `GET /api/info` - Service metadata and environment

### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register a new user (email, username, password) and receive JWT
- `POST /api/auth/login` - Authenticate with email & password and receive JWT
- `GET /api/auth/me` - Retrieve current authenticated user profile (Protected Bearer JWT)

### NLP & Reviewer Matching (`/api/nlp`)
- `POST /api/nlp/match` - Match conference papers with reviewer expertise profiles using TF-IDF, keywords, workload capacity, and conflict-of-interest detection
- `POST /api/nlp/similarity` - Compute pairwise TF-IDF cosine similarity across text candidates
- `POST /api/nlp/tokenize` - Tokenize text with stopword filtering
