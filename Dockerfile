# Dockerfile
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependencias del sistema (psycopg2, pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
  && rm -rf /var/lib/apt/lists/*

LABEL org.opencontainers.image.source="https://github.com/vasilako/ProjectManagementPF"

WORKDIR /app

# Requisitos
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copiar proyecto
COPY . .

# Exponer puerto interno (usado por reverse proxy)
EXPOSE 8000

# Comando de servidor (Gunicorn WSGI)
CMD gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120