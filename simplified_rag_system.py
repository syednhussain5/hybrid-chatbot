#!/usr/bin/env python3
"""
Simplified Integrated RAG System
Avoids heavy model downloads for initial testing
"""

import os
import json
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import google.generativeai as genai
from query_classifier import QueryClassifier

# Configuration
from config import GEMINI_API_KEY

class SimplifiedRAGSystem:
    """Simplified RAG system for testing"""
    
    def __init__(self):
        self.classifier = QueryClassifier(GEMINI_API_KEY)
        
        # Initialize Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    
    def handle_general_query(self, query: str) -> str:
        """Handle general conversation queries"""
        try:
            prompt = f"""
            You are a friendly AI assistant. Respond to this user query in a conversational, helpful way.
            
            User query: "{query}"
            
            Keep your response:
            - Friendly and conversational
            - Helpful and informative
            - Appropriate for casual conversation
            - Not too long (2-3 sentences max)
            
            Response:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in general query: {e}")
            return "I'm here to help! How can I assist you today? 😊"
    
    def handle_vector_query(self, query: str) -> str:
        """Handle vector search queries (simplified)"""
        try:
            # For now, use Gemini to simulate vector search results
            prompt = f"""
            You are an AI assistant with access to a knowledge base about big tech companies and AI technologies.
            
            User Query: "{query}"
            
            Instructions:
            1. Provide a detailed, informative answer about the topic
            2. Focus on factual information about big tech companies, AI technologies, and market trends
            3. Be specific and comprehensive
            4. If you don't have specific information, mention that this would typically come from document search
            
            Response:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in vector query: {e}")
            return "I encountered an error while searching for information. Please try again."
    
    def handle_kg_query(self, query: str) -> str:
        """Handle knowledge graph queries (simplified)"""
        try:
            # For now, use Gemini to simulate KG search results
            prompt = f"""
            You are an AI assistant with access to a knowledge graph about big tech companies, people, and their relationships.
            
            User Query: "{query}"
            
            Instructions:
            1. Focus on relationships between entities (companies, people, technologies)
            2. Provide specific information about who leads what, who owns what, partnerships, investments
            3. Be specific about the connections and relationships
            4. If you don't have specific information, mention that this would typically come from knowledge graph search
            
            Response:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in KG query: {e}")
            return "I encountered an error while searching the knowledge graph. Please try again."
    
    def handle_hybrid_query(self, query: str) -> str:
        """Handle hybrid queries (simplified)"""
        try:
            # For now, use Gemini to simulate hybrid search results
            prompt = f"""
            You are an AI assistant with access to both document content and knowledge graph information about big tech companies and AI technologies.
            
            User Query: "{query}"
            
            Instructions:
            1. Provide a comprehensive answer combining both factual information and relationship details
            2. Show how entities are connected and what the documents say about them
            3. Be thorough but organized in your response
            4. Focus on both the technical details and the business relationships
            
            Response:
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in hybrid query: {e}")
            return "I encountered an error while processing your query. Please try again."
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Main function to process any query"""
        print(f"\n🤖 Processing query: '{query}'")
        print("="*60)
        
        # Classify the query
        classification = self.classifier.classify_query(query)
        strategy = classification['search_strategy']
        confidence = classification['confidence']
        method = classification.get('method', 'unknown')
        
        print(f"🎯 Classification: {strategy} (confidence: {confidence:.2f}, method: {method})")
        
        # Route to appropriate handler
        if strategy == 'general':
            response = self.handle_general_query(query)
        elif strategy == 'vector':
            response = self.handle_vector_query(query)
        elif strategy == 'knowledge_graph':
            response = self.handle_kg_query(query)
        elif strategy == 'hybrid':
            response = self.handle_hybrid_query(query)
        else:
            response = "I'm not sure how to handle this query. Please try rephrasing it."
        
        result = {
            "query": query,
            "strategy": strategy,
            "confidence": confidence,
            "method": method,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n💬 Response:")
        print(f"{response}")
        print("="*60)
        
        return result

def main():
    """Main function for testing"""
    if len(sys.argv) < 2:
        print("Usage: python simplified_rag_system.py 'your query here'")
        print("Examples:")
        print("  python simplified_rag_system.py 'hi'")
        print("  python simplified_rag_system.py 'Who is the CEO of OpenAI?'")
        print("  python simplified_rag_system.py 'What is machine learning?'")
        sys.exit(1)
    
    query = sys.argv[1]
    
    # Initialize system
    rag_system = SimplifiedRAGSystem()
    
    try:
        # Process the query
        result = rag_system.process_query(query)
        
        # Save result
        with open(f"query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n✅ Result saved to query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
