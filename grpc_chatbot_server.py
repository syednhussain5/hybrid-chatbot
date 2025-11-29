#!/usr/bin/env python3
"""
gRPC Server for Chatbot Functionality
Handles real-time chat using gRPC
"""

import grpc
from concurrent import futures
import time
import json
from datetime import datetime
from typing import Dict, Any, Iterator
import uuid

# Import generated gRPC code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))

import chatbot_pb2
import chatbot_pb2_grpc

from simplified_rag_system import SimplifiedRAGSystem

class ChatbotServicer(chatbot_pb2_grpc.ChatServiceServicer):
    """gRPC servicer for chatbot functionality"""
    
    def __init__(self):
        self.rag_system = SimplifiedRAGSystem()
        self.chat_sessions = {}  # In production, use Redis or database
    
    def SendMessage(self, request: chatbot_pb2.ChatMessage, context) -> chatbot_pb2.ChatResponse:
        """Handle single message (unary RPC)"""
        try:
            # Process the message
            result = self.rag_system.process_query(request.message)
            
            # Store in session
            session_id = request.session_id or str(uuid.uuid4())
            if session_id not in self.chat_sessions:
                self.chat_sessions[session_id] = {
                    "user_id": request.user_id,
                    "messages": [],
                    "created_at": datetime.now().isoformat()
                }
            
            # Add to session history
            self.chat_sessions[session_id]["messages"].append({
                "user_message": request.message,
                "bot_response": result["response"],
                "strategy": result["strategy"],
                "timestamp": datetime.now().isoformat()
            })
            
            # Create response
            response = chatbot_pb2.ChatResponse(
                response=result["response"],
                session_id=session_id,
                timestamp=int(time.time()),
                classification=result["strategy"],
                confidence=result["confidence"],
                metadata={
                    "method": result.get("method", "unknown"),
                    "query_type": result.get("query_type", "unknown"),
                    "timestamp": result["timestamp"]
                }
            )
            
            return response
            
        except Exception as e:
            # Return error response
            return chatbot_pb2.ChatResponse(
                response=f"I encountered an error: {str(e)}",
                session_id=request.session_id or str(uuid.uuid4()),
                timestamp=int(time.time()),
                classification="error",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def ChatStream(self, request_iterator: Iterator[chatbot_pb2.ChatMessage], context) -> Iterator[chatbot_pb2.ChatResponse]:
        """Handle streaming chat (bidirectional streaming RPC)"""
        try:
            for request in request_iterator:
                # Process each message
                result = self.rag_system.process_query(request.message)
                
                # Store in session
                session_id = request.session_id or str(uuid.uuid4())
                if session_id not in self.chat_sessions:
                    self.chat_sessions[session_id] = {
                        "user_id": request.user_id,
                        "messages": [],
                        "created_at": datetime.now().isoformat()
                    }
                
                # Add to session history
                self.chat_sessions[session_id]["messages"].append({
                    "user_message": request.message,
                    "bot_response": result["response"],
                    "strategy": result["strategy"],
                    "timestamp": datetime.now().isoformat()
                })
                
                # Create and yield response
                response = chatbot_pb2.ChatResponse(
                    response=result["response"],
                    session_id=session_id,
                    timestamp=int(time.time()),
                    classification=result["strategy"],
                    confidence=result["confidence"],
                    metadata={
                        "method": result.get("method", "unknown"),
                        "query_type": result.get("query_type", "unknown"),
                        "timestamp": result["timestamp"]
                    }
                )
                
                yield response
                
        except Exception as e:
            # Yield error response
            yield chatbot_pb2.ChatResponse(
                response=f"I encountered an error: {str(e)}",
                session_id=str(uuid.uuid4()),
                timestamp=int(time.time()),
                classification="error",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def GetChatHistory(self, request: chatbot_pb2.ChatHistoryRequest, context) -> chatbot_pb2.ChatHistoryResponse:
        """Get chat history for a session"""
        try:
            session_id = request.session_id
            
            if session_id not in self.chat_sessions:
                return chatbot_pb2.ChatHistoryResponse(
                    messages=[],
                    responses=[],
                    total_count=0
                )
            
            session = self.chat_sessions[session_id]
            messages = session["messages"]
            
            # Limit results if requested
            if request.limit > 0:
                messages = messages[-request.limit:]
            
            # Convert to protobuf messages
            pb_messages = []
            pb_responses = []
            
            for msg in messages:
                # Create ChatMessage
                pb_message = chatbot_pb2.ChatMessage(
                    user_id=request.user_id,
                    message=msg["user_message"],
                    session_id=session_id,
                    timestamp=int(time.time()),
                    metadata={"timestamp": msg["timestamp"]}
                )
                pb_messages.append(pb_message)
                
                # Create ChatResponse
                pb_response = chatbot_pb2.ChatResponse(
                    response=msg["bot_response"],
                    session_id=session_id,
                    timestamp=int(time.time()),
                    classification=msg["strategy"],
                    confidence=0.9,  # Default confidence
                    metadata={"timestamp": msg["timestamp"]}
                )
                pb_responses.append(pb_response)
            
            return chatbot_pb2.ChatHistoryResponse(
                messages=pb_messages,
                responses=pb_responses,
                total_count=len(session["messages"])
            )
            
        except Exception as e:
            return chatbot_pb2.ChatHistoryResponse(
                messages=[],
                responses=[],
                total_count=0
            )

def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatbot_pb2_grpc.add_ChatServiceServicer_to_server(ChatbotServicer(), server)
    
    # Listen on port 50051
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    print(f"🚀 gRPC Chatbot Server starting on {listen_addr}")
    server.start()
    
    try:
        while True:
            time.sleep(86400)  # Sleep for 24 hours
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gRPC server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
