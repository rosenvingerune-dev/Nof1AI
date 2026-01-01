#!/bin/bash
echo "Starting Alpha Arena Bot... 🚀"
cd "$(dirname "$0")/.."
echo "Stopping existing bot..."
docker compose down
echo "Rebuilding and starting..."
docker compose up -d --build
echo "Bot started! Access at http://$(curl -s ifconfig.me):8081"
echo "To view logs: ./scripts/view_logs.sh"
