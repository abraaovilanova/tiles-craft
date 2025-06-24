#!/bin/bash
set -e

echo "📦 Aguardando o banco de dados ficar disponível..."

# Espera o PostgreSQL estar pronto (usa pg_isready)
until pg_isready -h db -p 5432 -U postgres; do
  sleep 2
done

echo "✅ Banco de dados disponível! Aplicando migrações Alembic..."
alembic upgrade head

echo "🚀 Iniciando servidor FastAPI com Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload