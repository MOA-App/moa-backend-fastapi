#!/bin/sh
set -e

echo "⏳ Waiting for PostgreSQL..."

until pg_isready \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$POSTGRES_USER"
do
    sleep 2
done

echo "📦 Applying database migrations..."
alembic upgrade head

echo "🚀 Starting API..."

exec "$@"
