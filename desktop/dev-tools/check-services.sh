#!/bin/bash
echo "🔍 Checking AI Services Status..."

services=(
    "n8n:5678"
    "open-webui:8080"
    "ollama:11434"
    "qdrant:6333"
    "kong:8000"
    "flowise:3001"
    "searxng:8081"
    "appflowy:8082"
    "affine:3010"
    "gitlab:8083"
    "langfuse:3002"
)

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)

    if curl -s "http://$service" > /dev/null 2>&1; then
        echo "✅ $name ($service) - Running"
    else
        echo "❌ $name ($service) - Not responding"
    fi
done
