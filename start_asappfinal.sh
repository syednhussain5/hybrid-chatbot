#!/bin/bash
# AsappFinal Project Startup Script

echo "🚀 Starting AsappFinal Project..."
echo "=================================="

# Navigate to project directory
cd "/Users/deepek/AsappFinal"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Start backend
echo "🔧 Starting FastAPI backend..."
python3 fastapi_backend.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "🎨 Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ AsappFinal is now running!"
echo "=================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
