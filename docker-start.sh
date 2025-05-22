#!/bin/bash

# RAGdoll Docker Startup Script

echo "🤖 Starting RAGdoll with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating one from example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Please edit .env file and add your OPENAI_API_KEY"
        echo "💡 You can edit it with: nano .env"
        exit 1
    else
        echo "📝 Please create a .env file with your OPENAI_API_KEY:"
        echo "OPENAI_API_KEY=your_openai_api_key_here"
        exit 1
    fi
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Please set your OPENAI_API_KEY in the .env file"
    echo "💡 Edit with: nano .env"
    exit 1
fi

echo "🔧 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 10

echo "🎉 RAGdoll is starting up!"
echo "📡 API will be available at: http://localhost:8000"
echo "📖 Interactive docs at: http://localhost:8000/docs"
echo ""
echo "🐳 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart: docker-compose restart"
echo ""
echo "📊 Check service status:"
docker-compose ps 