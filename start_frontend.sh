#!/bin/bash

# RAG Chatbot Frontend Startup Script

echo "🚀 Starting RAG Chatbot Frontend..."
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Please make sure you're in the correct directory."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        exit 1
    fi
    echo "✅ Dependencies installed successfully!"
fi

# Check if backend is running
echo "🔍 Checking backend connection..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on port 8000"
else
    echo "⚠️  Backend is not running on port 8000"
    echo "   Please start the backend first:"
    echo "   python start_backend.py"
    echo ""
    echo "   The frontend will still start but won't be able to connect to the backend."
fi

# Start the React development server
echo "🚀 Starting React development server..."
echo "   Frontend will be available at: http://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo ""

npm start
