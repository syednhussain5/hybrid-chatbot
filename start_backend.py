#!/usr/bin/env python3
"""
Startup script for the integrated RAG system
Runs both FastAPI and gRPC servers
"""

import subprocess
import time
import signal
import sys
import os
from threading import Thread

def run_fastapi_server():
    """Run FastAPI server"""
    print("🚀 Starting FastAPI server on port 8000...")
    try:
        subprocess.run([
            sys.executable, "fastapi_backend.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI server error: {e}")
    except KeyboardInterrupt:
        print("🛑 FastAPI server stopped")

def run_grpc_server():
    """Run gRPC server"""
    print("🚀 Starting gRPC server on port 50051...")
    try:
        subprocess.run([
            sys.executable, "grpc_chatbot_server.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ gRPC server error: {e}")
    except KeyboardInterrupt:
        print("🛑 gRPC server stopped")

def main():
    """Main function to start both servers"""
    print("🎯 Starting Integrated RAG System Backend")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        "fastapi_backend.py",
        "grpc_chatbot_server.py",
        "simplified_rag_system.py",
        "query_classifier.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            sys.exit(1)
    
    # Check if proto files exist
    proto_files = [
        "proto/chatbot_pb2.py",
        "proto/chatbot_pb2_grpc.py"
    ]
    
    for file in proto_files:
        if not os.path.exists(file):
            print(f"❌ Generated proto file not found: {file}")
            print("Run: python -m grpc_tools.protoc --proto_path=proto --python_out=proto --grpc_python_out=proto proto/chatbot.proto")
            sys.exit(1)
    
    print("✅ All required files found")
    
    # Start servers in separate threads
    fastapi_thread = Thread(target=run_fastapi_server, daemon=True)
    grpc_thread = Thread(target=run_grpc_server, daemon=True)
    
    try:
        # Start both servers
        fastapi_thread.start()
        time.sleep(2)  # Give FastAPI time to start
        
        grpc_thread.start()
        time.sleep(2)  # Give gRPC time to start
        
        print("\n🎉 Both servers are running!")
        print("📡 FastAPI: http://localhost:8000")
        print("📡 gRPC: localhost:50051")
        print("📚 FastAPI Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop both servers")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()
