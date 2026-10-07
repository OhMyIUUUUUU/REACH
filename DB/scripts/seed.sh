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

echo "Applying seed data to ${CONTAINER_NAME}..."

for file in seeds/*.sql; do
  if [ -f "$file" ]; then
    echo "Running seed: $file"
    docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" < "$file"
  fi
done

echo "Seed data applied successfully."
