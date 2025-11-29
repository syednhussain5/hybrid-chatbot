#!/usr/bin/env python3
"""
FastAPI Backend for Integrated RAG System
Provides REST endpoints for query processing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime
import uuid

from simplified_rag_system import SimplifiedRAGSystem

# Initialize FastAPI app
app = FastAPI(
    title="Integrated RAG System API",
    description="Backend API for query classification and response generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = SimplifiedRAGSystem()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

class QueryResponse(BaseModel):
    query: str
    strategy: str
    confidence: float
    method: str
    response: str
    timestamp: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ClassificationRequest(BaseModel):
    query: str

class ClassificationResponse(BaseModel):
    query: str
    strategy: str
    confidence: float
    method: str
    reasoning: str
    query_type: str
    entities_mentioned: List[str]
    requires_multi_hop: bool
    suggested_approach: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# In-memory storage for sessions (in production, use Redis or database)
sessions = {}

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Integrated RAG System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a query and return the response
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process the query
        result = rag_system.process_query(request.query)
        
        # Store in session
        if session_id not in sessions:
            sessions[session_id] = {
                "user_id": request.user_id,
                "queries": [],
                "created_at": datetime.now().isoformat()
            }
        
        sessions[session_id]["queries"].append({
            "query": request.query,
            "response": result["response"],
            "strategy": result["strategy"],
            "timestamp": result["timestamp"]
        })
        
        return QueryResponse(
            query=result["query"],
            strategy=result["strategy"],
            confidence=result["confidence"],
            method=result["method"],
            response=result["response"],
            timestamp=result["timestamp"],
            session_id=session_id,
            user_id=request.user_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/classify", response_model=ClassificationResponse)
async def classify_query(request: ClassificationRequest):
    """
    Classify a query without processing it
    """
    try:
        classification = rag_system.classifier.classify_query(request.query)
        
        return ClassificationResponse(
            query=request.query,
            strategy=classification["search_strategy"],
            confidence=classification["confidence"],
            method=classification.get("method", "unknown"),
            reasoning=classification["reasoning"],
            query_type=classification["query_type"],
            entities_mentioned=classification.get("entities_mentioned", []),
            requires_multi_hop=classification.get("requires_multi_hop", False),
            suggested_approach=classification["suggested_approach"],
            timestamp=classification["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying query: {str(e)}")

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get session information and chat history
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]

@app.get("/sessions")
async def list_sessions():
    """
    List all active sessions
    """
    return {
        "sessions": list(sessions.keys()),
        "total_sessions": len(sessions)
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del sessions[session_id]
    return {"message": "Session deleted successfully"}

@app.post("/batch-query")
async def batch_process_queries(requests: List[QueryRequest], background_tasks: BackgroundTasks):
    """
    Process multiple queries in batch
    """
    try:
        results = []
        
        for request in requests:
            session_id = request.session_id or str(uuid.uuid4())
            result = rag_system.process_query(request.query)
            
            # Store in session
            if session_id not in sessions:
                sessions[session_id] = {
                    "user_id": request.user_id,
                    "queries": [],
                    "created_at": datetime.now().isoformat()
                }
            
            sessions[session_id]["queries"].append({
                "query": request.query,
                "response": result["response"],
                "strategy": result["strategy"],
                "timestamp": result["timestamp"]
            })
            
            results.append(QueryResponse(
                query=result["query"],
                strategy=result["strategy"],
                confidence=result["confidence"],
                method=result["method"],
                response=result["response"],
                timestamp=result["timestamp"],
                session_id=session_id,
                user_id=request.user_id
            ))
        
        return {"results": results, "total_processed": len(results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch queries: {str(e)}")

@app.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    total_queries = sum(len(session["queries"]) for session in sessions.values())
    
    strategy_counts = {}
    for session in sessions.values():
        for query in session["queries"]:
            strategy = query["strategy"]
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
    
    return {
        "total_sessions": len(sessions),
        "total_queries": total_queries,
        "strategy_distribution": strategy_counts,
        "uptime": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
