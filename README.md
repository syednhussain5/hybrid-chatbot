# hybrid-chatbot-using-vectordb-and-knowledge-graph

**HybridRAG-Chatbot** - is an end-to-end intelligent chatbot system built with FastAPI backend and React frontend that uses Google Gemini from Langchain framework for natural language understanding, combining Pinecone vector database for semantic document search and Neo4j knowledge graph for entity relationship queries with automatic query routing and hybrid search capabilities.

## 🎯 Features

- **Multi-Strategy Query Routing**: Automatically classifies queries and routes them to the appropriate search strategy
- **Vector Search**: Semantic search using Pinecone vector database
- **Knowledge Graph**: Entity relationship queries using Neo4j
- **Hybrid Search**: Combines both vector and knowledge graph results
- **Statistical Chunking**: Intelligent document chunking for optimal retrieval
- **Modern UI**: Beautiful dark-themed React frontend with real-time chat

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI   │────▶│   RAG       │
│   Frontend  │     │   Backend   │     │   System    │
│  Port:3000  │     │  Port:8000  │     │             │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                 │
                        ┌────────────────────────┼────────────────────────┐
                        │                        │                        │
                  ┌─────▼─────┐          ┌─────▼─────┐          ┌─────▼─────┐
                  │  Pinecone │          │   Neo4j   │          │  Gemini   │
                  │  Vector   │          │Knowledge  │          │    API    │
                  │  Database │          │   Graph   │          │           │
                  └───────────┘          └───────────┘          └───────────┘
```

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- Neo4j Database (running locally or remote)
- Pinecone account and API key
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/deepkx/hybrid-chatbot-vector-knowledge-graph-.git
cd hybrid-chatbot-vector-knowledge-graph-
```

### 2. Setup Backend

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp config.example.py config.py
# Edit config.py with your API keys and credentials
```

### 3. Setup Frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Initialize Databases

```bash
# Create Pinecone index
python3 query_rag.py create

# Upload documents
python3 query_rag.py upload --dir Documents/
python3 query_rag.py upload --dir big_tech_docs/
```

### 5. Start the System

```bash
# Start backend
python3 fastapi_backend.py

# In another terminal, start frontend
cd frontend
npm start
```

Visit http://localhost:3000 to use the chatbot!

## 📁 Project Structure

```
.
├── frontend/              # React frontend application
├── Documents/             # PDF documents for vector search
├── big_tech_docs/         # Markdown documents about tech companies
├── proto/                 # gRPC protocol definitions
├── config.py              # Configuration (not in git)
├── config.example.py      # Configuration template
├── fastapi_backend.py     # FastAPI REST API server
├── simplified_rag_system.py # Core RAG system
├── query_classifier.py    # Query classification engine
├── query_rag.py          # Vector search and document upload
├── StatisticalChunker.py # Document chunking algorithm
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration

Copy `config.example.py` to `config.py` and fill in:

- **Pinecone**: API key, index name, and host
- **Neo4j**: URI, username, and password
- **Gemini**: API key for query classification and generation

## 📚 API Endpoints

- `GET /health` - Health check
- `POST /query` - Process a query
- `POST /classify` - Classify a query without processing
- `GET /sessions` - List all sessions
- `GET /sessions/{session_id}` - Get session details
- `GET /stats` - System statistics

See http://localhost:8000/docs for interactive API documentation.

## 🎨 Query Strategies

The system automatically routes queries to:

1. **General**: Conversational queries (greetings, casual chat)
2. **Vector**: Detailed explanations and document-based queries
3. **Knowledge Graph**: Relationship and entity queries
4. **Hybrid**: Complex queries requiring both approaches

