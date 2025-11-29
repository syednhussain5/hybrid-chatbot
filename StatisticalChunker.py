# statistical_chunker.py
import numpy as np
from typing import List
from dataclasses import dataclass

# --- Encoder stub ---
class DenseEncoder:
    score_threshold: float = 0.5
    def __call__(self, docs: List[str]):
        return [np.random.rand(1024) for _ in docs]
    async def acall(self, docs: List[str]):
        return [np.random.rand(1024) for _ in docs]

# --- Splitter stubs ---
class BaseSplitter:
    def split(self, text):
        return text.split(".")
class RegexSplitter(BaseSplitter):
    pass

# --- Chunk dataclass ---
@dataclass
class Chunk:
    splits: List[str]
    is_triggered: bool
    triggered_score: float
    token_count: int

# --- Logger stub ---
class logger:
    @staticmethod
    def info(msg): print(f"[INFO] {msg}")
    @staticmethod
    def debug(msg): print(f"[DEBUG] {msg}")
    @staticmethod
    def warning(msg): print(f"[WARNING] {msg}")
    @staticmethod
    def error(msg): print(f"[ERROR] {msg}")

# --- Utility functions ---
def tiktoken_length(text: str) -> int:
    return len(text.split())

def time_it(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

def async_retry_with_timeout(*args, **kwargs):
    def decorator(func): return func
    return decorator

# --- Chunker class ---
class StatisticalChunker:
    def __init__(self, encoder: DenseEncoder, splitter=RegexSplitter(), min_split_tokens=100, max_split_tokens=300, overlap_tokens=50):
        self.encoder = encoder
        self.splitter = splitter
        self.min_split_tokens = min_split_tokens
        self.max_split_tokens = max_split_tokens
        self.overlap_tokens = overlap_tokens

    @time_it
    def _split(self, doc: str) -> List[str]:
        return [s.strip() for s in self.splitter.split(doc) if s.strip()]

    @time_it
    def __call__(self, docs: List[str]) -> List[List[Chunk]]:
        all_chunks = []
        for doc in docs:
            splits = self._split(doc)
            chunks = []
            current = []
            token_count = 0
            overlap_buffer = []
            overlap_token_count = 0
            
            for s in splits:
                t = tiktoken_length(s)
                
                # Check if we need to create a chunk
                if token_count + t > self.max_split_tokens and token_count >= self.min_split_tokens:
                    # Create chunk with current content
                    chunks.append(Chunk(current.copy(), is_triggered=False, triggered_score=None, token_count=token_count))
                    
                    # Prepare overlap buffer
                    overlap_buffer = []
                    overlap_token_count = 0
                    
                    # Add content to overlap buffer (last few splits)
                    for split in reversed(current):
                        split_tokens = tiktoken_length(split)
                        if overlap_token_count + split_tokens <= self.overlap_tokens:
                            overlap_buffer.insert(0, split)
                            overlap_token_count += split_tokens
                        else:
                            break
                    
                    # Start new chunk with overlap
                    current = overlap_buffer.copy()
                    token_count = overlap_token_count
                
                current.append(s)
                token_count += t
            
            # Add final chunk if there's content
            if current:
                chunks.append(Chunk(current, is_triggered=False, triggered_score=None, token_count=token_count))
            
            all_chunks.append(chunks)
        return all_chunks
