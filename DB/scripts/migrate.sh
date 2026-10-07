#!/usr/bin/env bash
set -e

# Load environment variables if .env exists
if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
elif [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

DB_USER="${POSTGRES_USER:-reach_user}"
DB_NAME="${POSTGRES_DB:-reach_db}"
CONTAINER_NAME="reach_postgres"

echo "Applying SQL migrations to ${CONTAINER_NAME}..."

for file in migrations/*.up.sql; do
  if [ -f "$file" ]; then
    echo "Running migration: $file"
    docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" < "$file"
  fi
done

echo "Migrations applied successfully."
