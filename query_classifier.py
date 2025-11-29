# #!/usr/bin/env python3
# """
# Query Classification System
# This system uses Gemini to classify queries and determine the best search strategy
# """

# import os
# import json
# from typing import Dict, Any, List
# from datetime import datetime
# import google.generativeai as genai

# # Gemini API key
# GEMINI_API_KEY = "AIzaSyDe1C_D8eLAC8d3ESLqUpZ5OGcAlxR2igs"

# class QueryClassifier:
#     def __init__(self, gemini_api_key):
#         self.gemini_api_key = gemini_api_key
        
#         # Initialize Gemini
#         genai.configure(api_key=gemini_api_key)
#         self.model = genai.GenerativeModel('gemini-1.5-flash')
        
#     def classify_query(self, user_query: str) -> Dict[str, Any]:
#         """
#         Classify the user query to determine the best search strategy
#         """
#         classification_prompt = f"""
#         You are an expert query classifier for a hybrid RAG system that has access to both:
#         1. **Vector Database**: Contains detailed documents about big tech companies, AI initiatives, technologies, and market analysis
#         2. **Knowledge Graph**: Contains structured relationships between entities (companies, people, technologies, products)

#         Analyze the following user query and determine the optimal search strategy:

#         USER QUERY: "{user_query}"

#         CLASSIFICATION CRITERIA:

#         **Use VECTOR DATABASE when:**
#         - Query asks for detailed explanations, descriptions, or comprehensive information
#         - Query seeks specific facts, statistics, or detailed content from documents
#         - Query asks "what is", "how does", "explain", "describe", "tell me about"
#         - Query requests detailed analysis, comparisons, or in-depth information
#         - Query asks for examples, use cases, or detailed explanations
#         - Query seeks information about specific technologies, products, or services
#         - Query asks for market analysis, trends, or detailed reports
#         - Query requests comprehensive information that would be found in documents

#         **Use KNOWLEDGE GRAPH when:**
#         - Query asks about relationships between entities (companies, people, technologies)
#         - Query asks "who is connected to", "what is the relationship between"
#         - Query seeks multi-hop connections or relationship chains
#         - Query asks about investments, partnerships, acquisitions, or business relationships
#         - Query asks "who owns", "who invests in", "who competes with"
#         - Query seeks organizational structure, leadership, or corporate relationships
#         - Query asks about competitive landscape or business connections
#         - Query requests entity-to-entity relationships or network analysis

#         **Use HYBRID SEARCH when:**
#         - Query combines relationship questions with detailed explanations
#         - Query asks for both connections and comprehensive information
#         - Query requires both structured relationships and detailed content
#         - Query seeks both "who/what is connected" AND "detailed explanation"

#         **Query Analysis Guidelines:**
#         1. Identify the primary intent of the query
#         2. Determine if it's asking for relationships/connections or detailed information
#         3. Check if multiple entities are mentioned (suggests relationship analysis)
#         4. Look for relationship keywords: "connected", "invests", "owns", "competes", "partnership"
#         5. Look for detail keywords: "explain", "describe", "what is", "how does", "tell me about"

#         Respond in JSON format with the following structure:
#         {{
#             "search_strategy": "vector" | "knowledge_graph" | "hybrid",
#             "confidence": 0.0-1.0,
#             "reasoning": "detailed explanation of why this strategy was chosen",
#             "query_type": "relationship" | "factual" | "explanatory" | "comparative" | "analytical",
#             "entities_mentioned": ["list", "of", "entities", "mentioned"],
#             "relationship_keywords": ["list", "of", "relationship", "keywords", "found"],
#             "detail_keywords": ["list", "of", "detail", "keywords", "found"],
#             "requires_multi_hop": true/false,
#             "suggested_approach": "specific approach for handling this query type"
#         }}

#         Examples:
        
#         Query: "Who is the CEO of OpenAI?"
#         Strategy: knowledge_graph (seeking relationship between person and company)
        
#         Query: "What is machine learning?"
#         Strategy: vector (seeking detailed explanation)
        
#         Query: "How is Microsoft connected to OpenAI?"
#         Strategy: knowledge_graph (seeking relationship between two companies)
        
#         Query: "Explain Google's AI strategy and how it competes with Microsoft"
#         Strategy: hybrid (both detailed explanation AND relationship analysis)
        
#         Query: "What companies invest in AI startups?"
#         Strategy: knowledge_graph (seeking investment relationships)
        
#         Query: "Tell me about the history of artificial intelligence"
#         Strategy: vector (seeking comprehensive historical information)
#         """

#         try:
#             response = self.model.generate_content(classification_prompt)
            
#             # Parse JSON response
#             response_text = response.text.strip()
            
#             # Clean up the response if it has markdown formatting
#             if "```json" in response_text:
#                 response_text = response_text.split("```json")[1].split("```")[0].strip()
#             elif "```" in response_text:
#                 response_text = response_text.split("```")[1].split("```")[0].strip()
            
#             classification_result = json.loads(response_text)
            
#             # Add metadata
#             classification_result['timestamp'] = datetime.now().isoformat()
#             classification_result['original_query'] = user_query
            
#             return classification_result
            
#         except json.JSONDecodeError as e:
#             print(f"❌ Error parsing JSON response: {e}")
#             print(f"Raw response: {response.text}")
#             return self._fallback_classification(user_query)
#         except Exception as e:
#             print(f"❌ Error in query classification: {e}")
#             return self._fallback_classification(user_query)
    
#     def _fallback_classification(self, user_query: str) -> Dict[str, Any]:
#         """
#         Fallback classification when Gemini fails
#         """
#         query_lower = user_query.lower()
        
#         # Simple keyword-based classification
#         relationship_keywords = [
#             'who is', 'connected to', 'relationship', 'invests', 'owns', 'competes',
#             'partnership', 'acquisition', 'merger', 'ceo', 'founder', 'leads',
#             'collaborates', 'works with', 'partnered', 'funded by', 'backed by'
#         ]
        
#         detail_keywords = [
#             'what is', 'how does', 'explain', 'describe', 'tell me about',
#             'detailed', 'comprehensive', 'analysis', 'history', 'overview',
#             'definition', 'meaning', 'examples', 'use cases'
#         ]
        
#         relationship_score = sum(1 for keyword in relationship_keywords if keyword in query_lower)
#         detail_score = sum(1 for keyword in detail_keywords if keyword in query_lower)
        
#         if relationship_score > detail_score:
#             strategy = "knowledge_graph"
#             query_type = "relationship"
#         elif detail_score > relationship_score:
#             strategy = "vector"
#             query_type = "explanatory"
#         else:
#             strategy = "hybrid"
#             query_type = "mixed"
        
#         return {
#             "search_strategy": strategy,
#             "confidence": 0.7,
#             "reasoning": f"Fallback classification based on keyword analysis. Relationship score: {relationship_score}, Detail score: {detail_score}",
#             "query_type": query_type,
#             "entities_mentioned": [],
#             "relationship_keywords": [kw for kw in relationship_keywords if kw in query_lower],
#             "detail_keywords": [kw for kw in detail_keywords if kw in query_lower],
#             "requires_multi_hop": "relationship" in query_lower or "connected" in query_lower,
#             "suggested_approach": f"Use {strategy} search strategy",
#             "timestamp": datetime.now().isoformat(),
#             "original_query": user_query
#         }
    
#     def get_search_recommendations(self, classification: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Get specific recommendations for the search strategy
#         """
#         strategy = classification.get("search_strategy", "hybrid")
        
#         recommendations = {
#             "vector": {
#                 "description": "Use vector database for semantic similarity search",
#                 "best_for": [
#                     "Detailed explanations and descriptions",
#                     "Comprehensive information retrieval",
#                     "Document-based content search",
#                     "Semantic similarity matching"
#                 ],
#                 "search_params": {
#                     "similarity_threshold": 0.7,
#                     "max_results": 10,
#                     "include_metadata": True
#                 }
#             },
#             "knowledge_graph": {
#                 "description": "Use knowledge graph for relationship and entity analysis",
#                 "best_for": [
#                     "Entity-to-entity relationships",
#                     "Multi-hop relationship traversal",
#                     "Organizational structure analysis",
#                     "Investment and partnership networks"
#                 ],
#                 "search_params": {
#                     "max_hops": 3,
#                     "confidence_threshold": 0.6,
#                     "include_reverse_relationships": True
#                 }
#             },
#             "hybrid": {
#                 "description": "Combine both vector and knowledge graph searches",
#                 "best_for": [
#                     "Comprehensive analysis requiring both detailed content and relationships",
#                     "Complex queries with multiple information needs",
#                     "Multi-faceted questions about entities and their contexts"
#                 ],
#                 "search_params": {
#                     "vector_weight": 0.6,
#                     "graph_weight": 0.4,
#                     "merge_strategy": "complementary"
#                 }
#             }
#         }
        
#         return {
#             "strategy": strategy,
#             "recommendation": recommendations.get(strategy, recommendations["hybrid"]),
#             "confidence": classification.get("confidence", 0.7),
#             "reasoning": classification.get("reasoning", "No specific reasoning provided")
#         }


# def test_classifier():
#     """Test the query classifier with various query types"""
#     print("="*70)
#     print("🧠 Query Classification System Test")
#     print("="*70)
    
#     classifier = QueryClassifier(GEMINI_API_KEY)
    
#     test_queries = [
#         "Who is the CEO of OpenAI?",
#         "What is machine learning and how does it work?",
#         "How is Microsoft connected to OpenAI?",
#         "Explain Google's AI strategy and how it competes with Microsoft",
#         "What companies invest in AI startups?",
#         "Tell me about the history of artificial intelligence",
#         "Who owns ChatGPT and what are its main features?",
#         "What is the relationship between Amazon and Anthropic?",
#         "Describe the competitive landscape in AI technology",
#         "Who founded Google and what is their current AI focus?",
#         "What are the main differences between OpenAI and Anthropic?",
#         "How does Google's Gemini compare to OpenAI's ChatGPT?"
#     ]
    
#     print(f"Testing {len(test_queries)} different query types...\n")
    
#     for i, query in enumerate(test_queries, 1):
#         print(f"{'='*60}")
#         print(f"Test {i}/{len(test_queries)}")
#         print(f"{'='*60}")
#         print(f"Query: {query}")
        
#         try:
#             # Classify the query
#             classification = classifier.classify_query(query)
            
#             print(f"\n🎯 Classification Results:")
#             print(f"   Strategy: {classification['search_strategy']}")
#             print(f"   Confidence: {classification['confidence']:.2f}")
#             print(f"   Query Type: {classification['query_type']}")
#             print(f"   Reasoning: {classification['reasoning']}")
            
#             if classification.get('entities_mentioned'):
#                 print(f"   Entities: {', '.join(classification['entities_mentioned'])}")
            
#             if classification.get('relationship_keywords'):
#                 print(f"   Relationship Keywords: {', '.join(classification['relationship_keywords'])}")
            
#             if classification.get('detail_keywords'):
#                 print(f"   Detail Keywords: {', '.join(classification['detail_keywords'])}")
            
#             print(f"   Multi-hop Required: {classification.get('requires_multi_hop', False)}")
            
#             # Get recommendations
#             recommendations = classifier.get_search_recommendations(classification)
#             print(f"\n💡 Recommendations:")
#             print(f"   {recommendations['recommendation']['description']}")
#             print(f"   Best for: {', '.join(recommendations['recommendation']['best_for'][:3])}")
            
#             # Save classification result
#             filename = f"classification_{i}_{query.replace('?', '').replace(' ', '_')[:20]}.json"
#             with open(filename, 'w', encoding='utf-8') as f:
#                 json.dump(classification, f, indent=2, ensure_ascii=False)
#             print(f"\n💾 Classification saved to: {filename}")
            
#         except Exception as e:
#             print(f"\n❌ Error classifying query: {e}")
        
#         print()
    
#     print("✅ Classification test complete!")


# def classify_single_query(query: str):
#     """Classify a single query interactively"""
#     print("="*70)
#     print("🧠 Single Query Classification")
#     print("="*70)
    
#     classifier = QueryClassifier(GEMINI_API_KEY)
    
#     print(f"Query: {query}")
#     print("\n🤖 Analyzing query...")
    
#     try:
#         classification = classifier.classify_query(query)
        
#         print(f"\n🎯 Classification Results:")
#         print(f"   Strategy: {classification['search_strategy']}")
#         print(f"   Confidence: {classification['confidence']:.2f}")
#         print(f"   Query Type: {classification['query_type']}")
#         print(f"   Reasoning: {classification['reasoning']}")
        
#         if classification.get('entities_mentioned'):
#             print(f"   Entities: {', '.join(classification['entities_mentioned'])}")
        
#         if classification.get('relationship_keywords'):
#             print(f"   Relationship Keywords: {', '.join(classification['relationship_keywords'])}")
        
#         if classification.get('detail_keywords'):
#             print(f"   Detail Keywords: {', '.join(classification['detail_keywords'])}")
        
#         print(f"   Multi-hop Required: {classification.get('requires_multi_hop', False)}")
        
#         # Get recommendations
#         recommendations = classifier.get_search_recommendations(classification)
#         print(f"\n💡 Recommendations:")
#         print(f"   {recommendations['recommendation']['description']}")
#         print(f"   Best for: {', '.join(recommendations['recommendation']['best_for'])}")
        
#         return classification
        
#     except Exception as e:
#         print(f"\n❌ Error classifying query: {e}")
#         return None


# if __name__ == "__main__":
#     import sys
    
#     if len(sys.argv) > 1:
#         # Single query classification
#         query = " ".join(sys.argv[1:])
#         classify_single_query(query)
#     else:
#         # Run full test suite
#         test_classifier()




































#!/usr/bin/env python3
"""
Query Classification System
This system uses Gemini to classify queries and determine the best search strategy,
including a 'general' category for conversational or casual prompts.
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime
import google.generativeai as genai

# Gemini API key
from config import GEMINI_API_KEY

class QueryClassifier:
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def classify_query(self, user_query: str) -> Dict[str, Any]:
        """
        Classify the user query to determine the best search strategy or conversation type.
        """
        classification_prompt = f"""
        You are a query router for a hybrid RAG system. Your job is to determine which system should handle the user's query.

        USER QUERY: "{user_query}"

        ROUTING DECISION:

        **ROUTE TO VECTOR DATABASE if:**
        - Query asks "what is", "how does", "explain", "describe", "tell me about"
        - Query seeks detailed explanations, definitions, or comprehensive information
        - Query asks for examples, use cases, or detailed descriptions
        - Query requests analysis, comparisons, or in-depth information
        - Examples: "What is machine learning?", "Explain Google's AI strategy", "Tell me about the history of AI"

        **ROUTE TO KNOWLEDGE GRAPH if:**
        - Query asks "who is", "who owns", "who leads", "who founded"
        - Query asks about relationships: "connected to", "invests in", "partners with", "competes with"
        - Query seeks entity-to-entity relationships or organizational structure
        - Query asks about investments, partnerships, acquisitions, or business relationships
        - Examples: "Who is the CEO of OpenAI?", "How is Microsoft connected to OpenAI?", "Who owns Anthropic?"

        **ROUTE TO HYBRID SEARCH if:**
        - Query combines both relationship questions AND detailed explanations
        - Query asks for both "who/what is connected" AND "detailed explanation"
        - Examples: "Explain how Google collaborates with OpenAI in AI research", "Who founded Google and what is their current AI focus?"

        **ROUTE TO GENERAL CONVERSATION if:**
        - Query is purely conversational, greeting, or casual
        - Query does NOT request any factual, technical, or analytical information
        - Examples: "hi", "hello", "good morning", "how are you", "can you help me?", "thanks", "bye"

        IMPORTANT: Be precise. If a query asks for ANY factual information, do NOT classify it as "general".

        Respond in JSON format:
        {{
            "search_strategy": "vector" | "knowledge_graph" | "hybrid" | "general",
            "confidence": 0.0-1.0,
            "reasoning": "Clear explanation of why this routing decision was made",
            "query_type": "relationship" | "factual" | "explanatory" | "comparative" | "analytical" | "general_conversation",
            "entities_mentioned": ["list of specific entities mentioned"],
            "requires_multi_hop": true/false,
            "suggested_approach": "Specific approach for handling this query type"
        }}
        """

        try:
            response = self.model.generate_content(classification_prompt)
            response_text = response.text.strip()

            # Clean JSON formatting
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            classification_result = json.loads(response_text)

            classification_result['timestamp'] = datetime.now().isoformat()
            classification_result['original_query'] = user_query
            classification_result['method'] = 'gemini'
            return classification_result

        except json.JSONDecodeError as e:
            print(f"⚠️ Gemini returned invalid JSON, using fallback. Error: {e}")
            print(f"Raw response: {response_text[:200]}...")
            fallback_result = self._fallback_classification(user_query)
            fallback_result['method'] = 'fallback_json_error'
            return fallback_result
        except Exception as e:
            print(f"⚠️ Gemini API error, using fallback. Error: {e}")
            fallback_result = self._fallback_classification(user_query)
            fallback_result['method'] = 'fallback_api_error'
            return fallback_result
    
    def _fallback_classification(self, user_query: str) -> Dict[str, Any]:
        """
        Fallback classification when Gemini fails or JSON parsing fails.
        """
        query_lower = user_query.lower()

        # Define keyword lists
        relationship_keywords = [
            'who is', 'connected to', 'relationship', 'invests', 'owns', 'competes',
            'partnership', 'acquisition', 'merger', 'ceo', 'founder', 'leads',
            'collaborates', 'works with', 'partnered', 'funded by', 'backed by'
        ]
        
        detail_keywords = [
            'what is', 'how does', 'explain', 'describe', 'tell me about',
            'analysis', 'history', 'overview', 'definition', 'examples', 'use cases'
        ]

        general_keywords = [
            'hi', 'hello', 'hey', 'good morning', 'good evening', 'good night',
            'how are you', 'how r u', 'what’s up', 'whats up', 'wht doingg',
            'can you help me', 'could you help me', 'hiya', 'yo', 'sup',
            'nice to meet you', 'thank you', 'thanks', 'howdy', 'morning', 'evening'
        ]

        # Compute keyword scores
        relationship_score = sum(1 for kw in relationship_keywords if kw in query_lower)
        detail_score = sum(1 for kw in detail_keywords if kw in query_lower)
        general_score = sum(1 for kw in general_keywords if kw in query_lower)

        # Determine classification
        if general_score > max(relationship_score, detail_score):
            strategy = "general"
            query_type = "general_conversation"
        elif relationship_score > detail_score:
            strategy = "knowledge_graph"
            query_type = "relationship"
        elif detail_score > relationship_score:
            strategy = "vector"
            query_type = "explanatory"
        else:
            strategy = "hybrid"
            query_type = "mixed"

        return {
            "search_strategy": strategy,
            "confidence": 0.9 if strategy == "general" else 0.7,
            "reasoning": f"Fallback classification using keyword scores. Relationship: {relationship_score}, Detail: {detail_score}, General: {general_score}",
            "query_type": query_type,
            "entities_mentioned": [],
            "relationship_keywords": [kw for kw in relationship_keywords if kw in query_lower],
            "detail_keywords": [kw for kw in detail_keywords if kw in query_lower],
            "general_keywords": [kw for kw in general_keywords if kw in query_lower],
            "requires_multi_hop": "relationship" in query_lower or "connected" in query_lower,
            "suggested_approach": f"Use {strategy} strategy",
            "timestamp": datetime.now().isoformat(),
            "original_query": user_query,
            "method": "fallback_keyword_analysis"
        }

    def get_search_recommendations(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggests a search or response approach based on classification.
        """
        strategy = classification.get("search_strategy", "hybrid")
        
        recommendations = {
            "vector": {
                "description": "Use vector database for semantic similarity search.",
                "best_for": [
                    "Detailed explanations",
                    "Comprehensive document retrieval",
                    "In-depth factual queries"
                ]
            },
            "knowledge_graph": {
                "description": "Use knowledge graph for entity relationships.",
                "best_for": [
                    "Entity connections",
                    "Partnerships and investments",
                    "Corporate structures"
                ]
            },
            "hybrid": {
                "description": "Combine vector and knowledge graph results.",
                "best_for": [
                    "Mixed relationship + detailed info queries",
                    "Complex multi-entity questions",
                    "Comprehensive context analysis"
                ]
            },
            "general": {
                "description": "Handle as a friendly conversational prompt.",
                "best_for": [
                    "Greetings",
                    "Small talk",
                    "User assistance or polite interactions"
                ]
            }
        }
        
        return {
            "strategy": strategy,
            "recommendation": recommendations.get(strategy, recommendations["hybrid"]),
            "confidence": classification.get("confidence", 0.7),
            "reasoning": classification.get("reasoning", "Default reasoning")
        }

def test_classifier():
    """Test the query classifier with conversational queries"""
    print("="*70)
    print("💬 Query Classification System Test (Including 'general')")
    print("="*70)
    
    classifier = QueryClassifier(GEMINI_API_KEY)
    
    test_queries = [
        "hi",
        "hello",
        "hey there",
        "good morning",
        "good evening",
        "how are you",
        "how r u",
        "what’s up",
        "wht doingg",
        "can you help me",
        "could you help me please",
        "yo",
        "hiya",
        "i need help"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"🧠 Test {i}/{len(test_queries)} — Query: {query}")
        print(f"{'='*60}")
        
        classification = classifier.classify_query(query)
        strategy = classification.get("search_strategy")
        print(f"\n🎯 Strategy: {strategy}")
        print(f"   Confidence: {classification['confidence']:.2f}")
        print(f"   Type: {classification['query_type']}")
        print(f"   Reason: {classification['reasoning']}")
        
        if strategy == "general":
            print("🤖 Response: Hey there! How can I help you today? 😊")
        else:
            print(f"⚙️  Suggested handling: {classification['suggested_approach']}")
        
        recommendations = classifier.get_search_recommendations(classification)
        print(f"\n💡 Recommendation: {recommendations['recommendation']['description']}")
        print(f"   Best for: {', '.join(recommendations['recommendation']['best_for'])}")

    print("\n✅ All test queries classified successfully!")

if __name__ == "__main__":
    test_classifier()
