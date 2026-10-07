# REACH Database Layer

Database architecture, schema migrations, and local PostgreSQL container orchestration for the REACH platform.

## Directory Structure

```
DB/
├── docker-compose.yml       # Local PostgreSQL 16 container definition
├── migrations/              # Versioned schema migrations (up / down)
│   ├── 000001_init_schema.up.sql
│   └── 000001_init_schema.down.sql
├── seeds/                   # Development seed records and initial fixtures
│   └── 01_seed_users.sql
├── schemas/                 # Reference SQL schema definition
│   └── schema.sql
├── scripts/                 # Migration and database management scripts
│   ├── migrate.sh           # Apply migrations to running container
│   └── seed.sh              # Apply seeds to running container
├── .env.example             # Database connection environment template
├── .gitignore               # Ignores persistent data directories & backups
└── README.md
```

## Quickstart

### 1. Configure Environment
```bash
cp .env.example .env
```

### 2. Start PostgreSQL Container
```bash
docker compose up -d
```
*Starts PostgreSQL 16 on port `5432` (or the port defined in `.env`).*

### 3. Run Migrations & Seeds
```bash
./scripts/migrate.sh
./scripts/seed.sh
```

### 4. Stop Container
```bash
docker compose down
```
*(To erase local database volume: `docker compose down -v`)*

---

## Connection Strings

- **Go (`Backend/`)**:
  ```
  postgres://reach_user:reach_password@localhost:5432/reach_db?sslmode=disable
  ```
- **Python (`Nlp-service/`)**:
  ```
  postgresql://reach_user:reach_password@localhost:5432/reach_db
  ```
- **psql CLI**:
  ```bash
  docker exec -it reach_postgres psql -U reach_user -d reach_db
  ```
