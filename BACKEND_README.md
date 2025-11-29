# 🚀 Integrated RAG System Backend

## 📋 Overview

A complete backend system for the Integrated RAG (Retrieval-Augmented Generation) system with:
- **FastAPI REST API** for query processing and management
- **gRPC Chatbot Service** for real-time chat functionality
- **Automatic Query Classification** and routing
- **Session Management** and chat history

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   gRPC          │
│   REST API      │    │   Chatbot       │
│   Port: 8000    │    │   Port: 50051   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │  RAG System     │
         │  (Query         │
         │  Classification │
         │  & Processing)  │
         └─────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn grpcio grpcio-tools
```

### 2. Generate gRPC Code
```bash
python -m grpc_tools.protoc --proto_path=proto --python_out=proto --grpc_python_out=proto proto/chatbot.proto
```

### 3. Start Both Servers
```bash
python start_backend.py
```

### 4. Test the System
```bash
# Test REST API
python rest_api_client.py

# Test gRPC Chatbot
python grpc_chatbot_client.py

# Interactive REST chat
python rest_api_client.py interactive

# Interactive gRPC chat
python grpc_chatbot_client.py interactive
```

## 📡 API Endpoints

### FastAPI REST API (Port 8000)

#### Core Endpoints
- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /query` - Process a single query
- `POST /classify` - Classify a query without processing
- `POST /batch-query` - Process multiple queries

#### Session Management
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}` - Get session details
- `DELETE /sessions/{session_id}` - Delete a session

#### Statistics
- `GET /stats` - Get system statistics

### gRPC Chatbot Service (Port 50051)

#### RPC Methods
- `SendMessage` - Send a single message (unary)
- `ChatStream` - Real-time chat streaming (bidirectional)
- `GetChatHistory` - Retrieve chat history

## 🔧 Usage Examples

### REST API Examples

#### Process a Query
```python
import requests

response = requests.post("http://localhost:8000/query", json={
    "query": "What is machine learning?",
    "user_id": "user123",
    "session_id": "session456"
})

result = response.json()
print(f"Response: {result['response']}")
print(f"Strategy: {result['strategy']}")
```

#### Classify a Query
```python
response = requests.post("http://localhost:8000/classify", json={
    "query": "Who is the CEO of OpenAI?"
})

classification = response.json()
print(f"Strategy: {classification['strategy']}")
print(f"Confidence: {classification['confidence']}")
```

### gRPC Examples

#### Send Single Message
```python
import grpc
from proto import chatbot_pb2, chatbot_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = chatbot_pb2_grpc.ChatServiceStub(channel)

request = chatbot_pb2.ChatMessage(
    user_id="user123",
    message="Hello! How are you?",
    session_id="session456"
)

response = stub.SendMessage(request)
print(f"Response: {response.response}")
```

#### Streaming Chat
```python
def message_generator():
    messages = ["Hello!", "What is AI?", "Tell me about OpenAI"]
    for msg in messages:
        yield chatbot_pb2.ChatMessage(
            user_id="user123",
            message=msg,
            session_id="session456"
        )

responses = stub.ChatStream(message_generator())
for response in responses:
    print(f"Bot: {response.response}")
```

## 📊 Query Classification

The system automatically classifies queries into:

- **`general`** - Casual conversation (handled by chatbot)
- **`vector`** - Detailed information requests (document search)
- **`knowledge_graph`** - Relationship queries (entity search)
- **`hybrid`** - Complex queries requiring both approaches

## 🔄 Session Management

### REST API Sessions
- Automatic session creation
- Session-based query history
- User-specific sessions
- Session statistics

### gRPC Sessions
- Real-time session tracking
- Bidirectional streaming
- Chat history persistence
- Session metadata

## 📈 Monitoring

### Health Checks
- `GET /health` - API health status
- `GET /stats` - System statistics

### Statistics Available
- Total sessions
- Total queries processed
- Strategy distribution
- System uptime

## 🛠️ Development

### File Structure
```
├── fastapi_backend.py          # FastAPI server
├── grpc_chatbot_server.py      # gRPC server
├── grpc_chatbot_client.py      # gRPC client example
├── rest_api_client.py          # REST API client example
├── start_backend.py            # Startup script
├── simplified_rag_system.py    # Core RAG system
├── query_classifier.py         # Query classification
└── proto/
    ├── chatbot.proto           # gRPC definitions
    ├── chatbot_pb2.py          # Generated Python code
    └── chatbot_pb2_grpc.py     # Generated gRPC code
```

### Adding New Features

1. **REST Endpoints**: Add to `fastapi_backend.py`
2. **gRPC Methods**: Update `proto/chatbot.proto` and regenerate
3. **RAG Logic**: Modify `simplified_rag_system.py`
4. **Classification**: Update `query_classifier.py`

## 🔒 Production Considerations

### Security
- Add authentication/authorization
- Input validation and sanitization
- Rate limiting
- CORS configuration

### Performance
- Database for session storage (Redis/PostgreSQL)
- Caching for frequent queries
- Load balancing
- Connection pooling

### Monitoring
- Logging and metrics
- Error tracking
- Performance monitoring
- Health checks

## 🎯 Next Steps

1. **Database Integration**: Replace in-memory storage
2. **Authentication**: Add user authentication
3. **Caching**: Implement query result caching
4. **Load Balancing**: Scale horizontally
5. **Monitoring**: Add comprehensive monitoring

## 📚 API Documentation

Once the servers are running:
- **FastAPI Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes on ports
   lsof -ti:8000 | xargs kill -9
   lsof -ti:50051 | xargs kill -9
   ```

2. **gRPC Code Not Generated**
   ```bash
   python -m grpc_tools.protoc --proto_path=proto --python_out=proto --grpc_python_out=proto proto/chatbot.proto
   ```

3. **Missing Dependencies**
   ```bash
   pip install fastapi uvicorn grpcio grpcio-tools
   ```

## 🎉 Success!

Your integrated RAG system backend is now running with:
- ✅ FastAPI REST API on port 8000
- ✅ gRPC Chatbot service on port 50051
- ✅ Automatic query classification
- ✅ Session management
- ✅ Real-time chat capabilities
- ✅ Comprehensive client examples

**Ready for production deployment!** 🚀
