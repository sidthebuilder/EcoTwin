#!/bin/bash
# EcoTwin Deployment Helper

echo "🌿 EcoTwin: Orchestrating the Digital Twin Stack..."

# Check dependencies
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

# Build and Start
echo "🚀 Building containers [Production Mode]..."
docker-compose up --build -d

echo "✅ Stack is up!"
echo "📡 Backend API: http://localhost:8000/docs"
echo "🌐 Frontend Dashboard: http://localhost:3000"
echo ""
echo "Use 'docker-compose logs -f' to watch the heart beat."
