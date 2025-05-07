#!/bin/bash

echo "🚀 Starting VibeStack setup..."

# Determine whether 'docker compose' or 'docker-compose' is available
if command -v docker compose &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Neither 'docker compose' nor 'docker-compose' is installed."
    echo "Please install Docker with Compose support."
    exit 1
fi

echo "🔧 Using: $COMPOSE_CMD"

# Start the services
$COMPOSE_CMD up --build -d

echo "✅ Done. Services are running."
echo "To view logs: $COMPOSE_CMD logs -f"
