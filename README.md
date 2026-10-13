# REACH (Reviewer Evaluation and Assignment for Conference Handling)

REACH is a web-based university research-conference management framework featuring an explainable Natural Language Processing (NLP) reviewer-matching engine. The system automates matching submitted research papers with qualified reviewers by evaluating keyword overlap, TF-IDF cosine similarity, reviewer workload limits, and conflict-of-interest (COI) constraints in a double-blind workflow.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 19 + TypeScript (Vite + Tailwind CSS v4) |
| **Backend** | Python (FastAPI + SQLAlchemy 2.0) |
| **Database** | PostgreSQL 16 (Docker) |
| **NLP & ML** | scikit-learn, NLTK |
| **Auth** | JWT (email/password with native bcrypt) |
| **Deployment** | Docker + Docker Compose |

---

## OS Compatibility & Environment Setup

### 🪟 Windows Users: Use WSL2 (Required)
The project's automation scripts (`./install-deps.sh`, `./start-dev.sh`) and development workflow rely on POSIX/bash environments. Running directly in Windows Command Prompt (cmd) or PowerShell will cause compatibility errors.

1. **Install WSL2** (if not already installed):
   ```powershell
   wsl --install
   ```
2. **Open your WSL2 terminal** (e.g., Ubuntu).
3. **Clone and open the repository inside WSL**:
   ```bash
   git clone https://github.com/OhMyIUUUUUU/REACH.git
   cd REACH
   ```
4. **Docker Desktop for Windows**: Ensure **"Use the WSL 2 based engine"** and your WSL distro integration are enabled in Docker Desktop settings under **Settings > Resources > WSL Integration**.

### 🐧 Linux & 🍎 macOS Users: Native Terminal
- **Do NOT use WSL.**
- Linux and macOS have full native POSIX/bash compatibility. Run all commands directly in your standard terminal. Ensure `docker`, `python3` (3.12+), and `node` (v20+) are installed.

---

## Docker Setup (Database Container)

Docker is used specifically to containerize and manage the **PostgreSQL 16 database** (`reach_postgres`), while the FastAPI Backend and React Frontend run bare-metal on the host for rapid live-reload development.

### Compose Configuration
The root [`docker-compose.yml`](docker-compose.yml) configures:
- **Image**: `postgres:16-alpine`
- **Container Name**: `reach_postgres`
- **Port Mapping**: `5432:5432`
- **Volume**: `reach_pgdata` (persistent database storage across restarts)
- **Automatic Migrations**: Mounts `./DB/migrations` to `/docker-entrypoint-initdb.d:ro` so schemas are automatically executed upon first container startup.
- **Health Check**: Continuous `pg_isready` check to verify database readiness.

### Docker Management Commands
```bash
# Start PostgreSQL database container in the background
docker compose up -d

# Check container health and status
docker ps -f name=reach_postgres

# View live database logs
docker logs -f reach_postgres

# Stop the database container (data remains preserved in volume)
docker compose down

# Stop container and remove volume (full wipe)
docker compose down -v
```

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

### 2. Start Database Container (PostgreSQL)
```bash
docker compose up -d
```
Starts PostgreSQL 16 in a background container on port `5432`, auto-loading migrations from `DB/migrations`.

---

### 3. Start Development Servers (Backend & Frontend)
```bash
./start-dev.sh
```
Runs the Python FastAPI backend on `http://localhost:8080` and the Vite React frontend on `http://localhost:5173` concurrently.
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
