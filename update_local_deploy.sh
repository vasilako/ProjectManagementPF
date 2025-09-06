#!/usr/bin/env bash
set -euo pipefail

# --- Config rápida ---
PROJECT_NAME="myapp-stack-local"     # separa volúmenes/recursos de prod
IMAGE_NAME="pfapp/img"
IMAGE_TAG="dev-$(date +%Y%m%d%H%M%S)" # tag único por ejecución
COMPOSE_FILES="-f docker-compose.yml -f docker-compose.override.yml"  # añade un override si quieres
ENV_LOCAL=".env.local"

# --- Pre-chequeos ---
if [ ! -f "$ENV_LOCAL" ]; then
  echo "❌ Falta $ENV_LOCAL. Créalo antes de continuar." >&2
  exit 1
fi

export COMPOSE_PROJECT_NAME="$PROJECT_NAME"
export IMAGE_TAG="$IMAGE_TAG"

echo "🔨 Build imagen local: $IMAGE_NAME:$IMAGE_TAG"
docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
export IMAGE_TAG="$IMAGE_TAG"

echo "⬆️  Levantar web"
docker compose $COMPOSE_FILES --env-file "$ENV_LOCAL" up -d web

echo "⚙️  Migraciones y collectstatic"
docker compose $COMPOSE_FILES --env-file "$ENV_LOCAL" exec -T web python manage.py migrate --noinput
docker compose $COMPOSE_FILES --env-file "$ENV_LOCAL" exec -T web python manage.py collectstatic --noinput || true

echo "🧹 Limpiar imágenes antiguas de pfapp/img (conservar la actual)"
current=$(docker compose ps -q web | xargs docker inspect --format '{{.Image}}' || true)
for img in $(docker images "$IMAGE_NAME" --format '{{.ID}}'); do
  if [ -n "$current" ] && [ "$img" != "$current" ]; then
    docker rmi -f "$img" || true
  fi
done

echo "📋 Estado:"
docker compose $COMPOSE_FILES --env-file "$ENV_LOCAL" ps

echo
echo "✅ Listo. Prueba en: http://localhost (Caddy) o http://localhost:8000 si expones web directo."
echo "   Recuerda: en .env.local → CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1"
