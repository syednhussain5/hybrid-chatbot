#!/bin/bash

# Complete RAG Chatbot System Startup Script

echo "🚀 Starting Complete RAG Chatbot System"
echo "======================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "start_backend.py" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check Python installation
if ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python first."
    exit 1
fi

# Check Node.js installation
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check npm installation
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_info "All prerequisites are installed"

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python -m venv venv
fi

print_info "Activating Python virtual environment..."
source venv/bin/activate

print_info "Installing Python dependencies..."
pip install -q fastapi uvicorn grpcio grpcio-tools google-generativeai sentence-transformers qdrant-client neo4j pdfplumber

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    print_info "Installing frontend dependencies..."
    cd frontend
    npm install --silent
    cd ..
fi

# Generate gRPC code if needed
if [ ! -f "proto/chatbot_pb2.py" ]; then
    print_info "Generating gRPC code..."
    python -m grpc_tools.protoc --proto_path=proto --python_out=proto --grpc_python_out=proto proto/chatbot.proto
fi

# Function to start backend
start_backend() {
    print_info "Starting backend servers..."
    python start_backend.py &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    
    # Wait for backend to start
    sleep 5
    
    # Check if backend is running
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend is running on port 8000"
        print_status "gRPC server is running on port 50051"
    else
        print_warning "Backend may not be fully started yet"
    fi
}

# Function to start frontend
start_frontend() {
    print_info "Starting frontend..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid
    cd ..
    
    sleep 3
    print_status "Frontend is starting on port 3000"
}

# Function to cleanup on exit
cleanup() {
    print_info "Shutting down servers..."
    
    if [ -f "backend.pid" ]; then
        BACKEND_PID=$(cat backend.pid)
        kill $BACKEND_PID 2>/dev/null
        rm backend.pid
    fi
    
    if [ -f "frontend.pid" ]; then
        FRONTEND_PID=$(cat frontend.pid)
        kill $FRONTEND_PID 2>/dev/null
        rm frontend.pid
    fi
    
    # Kill any remaining processes
    pkill -f "fastapi_backend.py" 2>/dev/null
    pkill -f "grpc_chatbot_server.py" 2>/dev/null
    pkill -f "npm start" 2>/dev/null
    
    print_status "Cleanup complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the system
print_info "Starting complete RAG Chatbot system..."

# Start backend
start_backend

# Start frontend
start_frontend

# Display system information
echo ""
echo "🎉 RAG Chatbot System is now running!"
echo "====================================="
echo ""
print_status "Frontend: http://localhost:3000"
print_status "Backend API: http://localhost:8000"
print_status "API Documentation: http://localhost:8000/docs"
print_status "gRPC Server: localhost:50051"
echo ""
print_info "Press Ctrl+C to stop all servers"
echo ""

# Wait for user to stop
while true; do
    sleep 1
done
