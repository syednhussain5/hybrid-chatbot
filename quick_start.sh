#!/bin/bash

# Quick RAG Chatbot Startup Script

echo "🚀 Quick Start - RAG Chatbot System"
echo "=================================="

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "fastapi_backend.py" 2>/dev/null
pkill -f "grpc_chatbot_server.py" 2>/dev/null
pkill -f "npm start" 2>/dev/null

# Start backend (FastAPI only for now)
echo "🔧 Starting FastAPI backend..."
python fastapi_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "🎨 Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 System is running!"
echo "==================="
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

# Wait for user to stop
wait
