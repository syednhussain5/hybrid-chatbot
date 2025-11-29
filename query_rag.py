import argparse
import os
import json
from pathlib import Path
import numpy as np
import pdfplumber

from langchain_core.documents.base import Document
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.embeddings import Embeddings

from StatisticalChunker import StatisticalChunker


# ---------------------- CONFIG ----------------------
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_HOST, TOP_K, MAX_DOCS_FOR_CONTEXT, TARGET_DIM


# ---------------------- BASE EMBEDDING MODEL ----------------------
base_embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")  # 768-dim


# ---------------------- CUSTOM EMBEDDING CLASS ----------------------
class ProjectedFastEmbedEmbeddings(Embeddings):
    """Wrapper to project 768-d FastEmbed vectors to target dimension for Pinecone."""

    def __init__(self, model_name="BAAI/bge-base-en-v1.5", target_dim=1024):
        self.model = FastEmbedEmbeddings(model_name=model_name)
        self.target_dim = target_dim
        # Load or create projection matrix
        projection_file = Path("projection_matrix.pkl")
        if projection_file.exists():
            import pickle
            with open(projection_file, 'rb') as f:
                self.projection_matrix = pickle.load(f)
        else:
            self.projection_matrix = np.random.randn(768, target_dim).astype(np.float32)
            import pickle
            with open(projection_file, 'wb') as f:
                pickle.dump(self.projection_matrix, f)

    def _project(self, vec):
        return np.dot(vec, self.projection_matrix).tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        base_vecs = self.model.embed_documents(texts)
        return [self._project(v) for v in base_vecs]

    def embed_query(self, text: str) -> list[float]:
        base_vec = self.model.embed_query(text)
        return self._project(base_vec)


# Instantiate once
embedding_obj = ProjectedFastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5", target_dim=TARGET_DIM)


# ---------------------- STATISTICAL CHUNKER ----------------------
class FastEmbedDenseEncoder:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def __call__(self, docs):
        return [self.embedding_model.embed_query(doc) for doc in docs]


encoder = FastEmbedDenseEncoder(embedding_obj)
chunker = StatisticalChunker(encoder=encoder, min_split_tokens=100, max_split_tokens=300, overlap_tokens=50)


# ---------------------- UTILITIES ----------------------
def read_pdf_files(directory: str):
    documents = []
    for pdf_file in Path(directory).glob("*.pdf"):
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            documents.append(Document(page_content=text, metadata={"filename": pdf_file.stem, "file_type": "pdf"}))
    return documents


def read_markdown_files(directory: str):
    documents = []
    for md_file in Path(directory).glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                text = f.read()
            if text.strip():
                documents.append(Document(page_content=text, metadata={"filename": md_file.stem, "file_type": "markdown"}))
        except Exception as e:
            print(f"[WARNING] Could not read {md_file}: {e}")
    return documents


def read_documents(directory: str):
    """Read both PDF and Markdown files from the given directory."""
    pdf_docs = read_pdf_files(directory)
    md_docs = read_markdown_files(directory)
    all_docs = pdf_docs + md_docs
    print(f"[INFO] Found {len(pdf_docs)} PDF files and {len(md_docs)} Markdown files.")
    return all_docs


def create_pinecone_index():
    """Create Pinecone index if it doesn't exist."""
    # Initialize Pinecone client
    api_key = PINECONE_API_KEY or os.environ.get("PINECONE_API_KEY", "")
    if not api_key:
        # Try to extract API key from environment or use a default
        print("[WARNING] PINECONE_API_KEY not set. Please set it in config.py or environment variable.")
        print("[INFO] Attempting to connect with host-based configuration...")
        # For serverless, we might not need an API key if using host
        try:
            pc = Pinecone(api_key="")  # Empty key might work for some setups
        except:
            print("[ERROR] Pinecone requires an API key. Please set PINECONE_API_KEY in config.py")
            return None
    else:
        pc = Pinecone(api_key=api_key)
    
    # Check if index exists
    try:
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        
        if PINECONE_INDEX_NAME in existing_indexes:
            print(f"[INFO] Index '{PINECONE_INDEX_NAME}' already exists.")
            return pc
        
        # Create index if it doesn't exist
        print(f"[INFO] Creating Pinecone index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=TARGET_DIM,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"  # Free plan supports us-east-1
            )
        )
        print(f"[INFO] Pinecone index '{PINECONE_INDEX_NAME}' created successfully.")
    except Exception as e:
        print(f"[INFO] Index may already exist or connection issue: {e}")
        # Try to get the index anyway
        try:
            index = pc.Index(PINECONE_INDEX_NAME)
            print(f"[INFO] Successfully connected to existing index '{PINECONE_INDEX_NAME}'")
        except Exception as e2:
            print(f"[ERROR] Could not connect to index: {e2}")
            return None
    
    return pc


def upload_chunks_to_pinecone(pc, docs):
    """Upload document chunks to Pinecone."""
    index = pc.Index(PINECONE_INDEX_NAME)
    
    point_id = 0
    vectors_to_upload = []
    
    print(f"[INFO] Processing {len(docs)} documents...")
    
    for doc in docs:
        chunks = chunker([doc.page_content])[0]
        for chunk in chunks:
            text = " ".join(chunk.splits)
            vector = embedding_obj.embed_query(text)
            
            # Prepare metadata
            metadata = {
                "page_content": text,
                "filename": doc.metadata.get("filename", "unknown"),
                "file_type": doc.metadata.get("file_type", "unknown")
            }
            
            vectors_to_upload.append({
                "id": str(point_id),
                "values": vector,
                "metadata": metadata
            })
            point_id += 1
            
            # Upload in batches
            if len(vectors_to_upload) >= 100:
                index.upsert(vectors=vectors_to_upload)
                print(f"[INFO] Uploaded {point_id} chunks...")
                vectors_to_upload = []
    
    # Upload remaining vectors
    if vectors_to_upload:
        index.upsert(vectors=vectors_to_upload)
    
    print(f"[INFO] Upload completed. Total chunks uploaded: {point_id}")


# ---------------------- QUERY & RETRIEVAL ----------------------
def reciprocal_rank_fusion(results: list[list], k=60):
    """
    Fixed version: converts Document objects to dict before JSON serialization
    """
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            # Convert Document to a serializable dict
            doc_dict = {
                "page_content": doc.page_content,
                "metadata": doc.metadata
            }
            doc_str = json.dumps(doc_dict, sort_keys=True)
            fused_scores[doc_str] = fused_scores.get(doc_str, 0) + 1 / (rank + k)
    
    reranked = [
        (json.loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Convert back to Document objects
    result_docs = []
    for doc_dict, score in reranked[:MAX_DOCS_FOR_CONTEXT]:
        result_docs.append(Document(
            page_content=doc_dict["page_content"],
            metadata=doc_dict["metadata"]
        ))
    
    return result_docs


def generate_similar_queries(query_text: str) -> list[str]:
    """Use Gemini to generate semantically similar queries."""
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "AIzaSyBEUcJ_B7DgULX8BtCjbAti3xm4PEl0TCo"

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt = f"Generate 3 semantically similar search queries for: '{query_text}' without changing the meaning."

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        lines = [l.strip("*-123. ") for l in content.split("\n") if l.strip()]
        queries = [query_text] + [q for q in lines if len(q) > 5]
        return queries
    except Exception as e:
        print(f"[ERROR] Gemini generation failed: {e}")
        return [query_text]


def rrf_retriever(query: str):
    """Retrieve documents using Reciprocal Rank Fusion with Pinecone."""
    queries = generate_similar_queries(query)
    print(f"[INFO] Generated similar queries: {queries}\n")

    # Initialize Pinecone
    api_key = PINECONE_API_KEY or os.environ.get("PINECONE_API_KEY", "")
    if not api_key:
        print("[ERROR] PINECONE_API_KEY is required for querying. Please set it in config.py")
        return []
    
    pc = Pinecone(api_key=api_key)
    
    # Create Pinecone vector store
    try:
        vectorstore = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            embedding=embedding_obj,
            pinecone_api_key=api_key,
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

        all_results = []
        for q in queries:
            try:
                retrieved = retriever.invoke(q)
                all_results.append(retrieved)
            except Exception as e:
                print(f"[WARNING] Error retrieving for query '{q}': {e}")

        if not all_results:
            print("[WARNING] No results retrieved from any query.")
            return []

        final_results = reciprocal_rank_fusion(all_results)

        print(f"\n[INFO] Top {TOP_K} Retrieved Chunks:\n")
        for idx, document in enumerate(final_results[:TOP_K]):
            print(f"🔹 Document {idx + 1}: {document.metadata.get('filename', 'N/A')}")
            print(f"   {document.page_content[:150]}...\n")
        return final_results
    except Exception as e:
        print(f"[ERROR] Failed to query Pinecone: {e}")
        return []


# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF & Markdown Chunking & Pinecone Upload + Retrieval")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("create", help="Create the Pinecone index")

    upload_parser = subparsers.add_parser("upload", help="Upload PDFs and Markdown files to Pinecone")
    upload_parser.add_argument("--dir", required=True, help="Directory containing PDF and/or Markdown files")

    query_parser = subparsers.add_parser("query", help="Query the vector DB")
    query_parser.add_argument("--text", required=True, help="User query text")

    args = parser.parse_args()

    if args.command == "create":
        create_pinecone_index()
    elif args.command == "upload":
        pc = create_pinecone_index()
        documents = read_documents(args.dir)
        upload_chunks_to_pinecone(pc, documents)
    elif args.command == "query":
        rrf_retriever(args.text)
    else:
        parser.print_help()
