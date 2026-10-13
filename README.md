# REACH (Reviewer Evaluation and Assignment for Conference Handling)

REACH is a web-based university research-conference management framework with an explainable Natural Language Processing (NLP) reviewer-matching engine. The system automates matching submitted research papers with qualified reviewers by evaluating keyword overlap, TF-IDF cosine similarity, reviewer workload limits, and conflict-of-interest (COI) constraints in a double-blind workflow.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 19 + TypeScript (Vite + Tailwind CSS v4) |
| **Backend** | Python (FastAPI + SQLAlchemy 2.0) |
| **Database** | PostgreSQL 16 |
| **NLP & ML** | scikit-learn, NLTK |
| **Auth** | JWT (email/password with native bcrypt) |
| **Deployment** | Docker + Docker Compose |

---

## Directory Architecture

- [Frontend/](Frontend) - React 19 + TypeScript + Vite + Tailwind CSS v4
- [Backend/](Backend) - Python FastAPI REST API (`app/main.py`), PostgreSQL ORM, JWT authentication, and Scikit-Learn/NLTK reviewer matching engine
- [DB/](DB) - PostgreSQL schemas (`schema.sql`), SQL migrations, seeds, and Docker configurations
- [Docs/](Docs) - System specifications, architecture design docs, and thesis reference materials

---

## Quickstart

### 1. Install Dependencies
```bash
./install-deps.sh
```
*Installs npm packages for Frontend and sets up the Python virtual environment with all required packages for Backend.*

---

### 2. Run with Docker Compose (Full Stack)
```bash
docker compose up -d
```
Starts PostgreSQL and the Python FastAPI backend in connected containers.

---

### 3. Run Development Servers (Bare Metal)
```bash
# 1. Start Database
cd DB && docker compose up -d && cd ..

# 2. Start Backend & Frontend concurrently
./start-dev.sh
```
- **Backend API**: `http://localhost:8080` (Interactive Swagger: `/docs`)
- **Frontend App**: `http://localhost:5173`
- **PostgreSQL**: `localhost:5432`

---

## Core API Endpoints

### Health & Metadata
- `GET /` - Root service index
- `GET /api/health` - Health check status, UTC timestamp, and uptime
- `GET /api/info` - Service metadata and environment

### Authentication
- `POST /api/auth/register` - Register a new user (email, username, password) and receive JWT
- `POST /api/auth/login` - Authenticate with email & password and receive JWT
- `GET /api/auth/me` - Retrieve current authenticated user profile (Protected Bearer token)

### NLP Reviewer Matching
- `POST /api/nlp/match` - Match conference papers to reviewer profiles with TF-IDF, keywords, workload capacity, and conflict-of-interest detection
- `POST /api/nlp/similarity` - Pairwise TF-IDF cosine similarity
- `POST /api/nlp/tokenize` - Text tokenization and stopword removal
