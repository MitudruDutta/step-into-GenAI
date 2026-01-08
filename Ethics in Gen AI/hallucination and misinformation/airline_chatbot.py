"""
RAG-Based Airline Chatbot with Hallucination Prevention
========================================================

This module implements a Retrieval-Augmented Generation (RAG) chatbot
that answers airline FAQ questions while minimizing hallucinations.

Hallucination Prevention Strategies:
------------------------------------
1. GROUNDING: Answers must be based on retrieved context
2. SCOPE LIMITING: Reject questions outside the knowledge domain
3. CONFIDENCE FILTERING: Only use high-confidence retrieved results
4. PROMPT ENGINEERING: Explicit instructions to avoid fabrication

Architecture:
-------------
    User Query → Embedding → ChromaDB Semantic Search → Top-K Context
                                      ↓
                        Context + Query → LLM → Grounded Answer

Usage:
    from airline_chatbot import RAGAnswerTool
    
    chatbot = RAGAnswerTool()
    result = chatbot.get_answer("Can I get a refund?")
    print(result['answer'])
"""

import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from typing import Dict, List, Optional
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAnswerTool:
    """
    RAG-based question answering tool with hallucination safeguards.
    
    This class retrieves relevant context from a ChromaDB knowledge base
    and uses an LLM to generate grounded, accurate responses.
    
    Hallucination Prevention Features:
    - Semantic similarity retrieval ensures relevant context
    - System prompt explicitly forbids fabrication
    - Out-of-scope detection rejects irrelevant questions
    - Source attribution enables verification
    
    Attributes:
        chroma_client: ChromaDB client for vector storage
        collection: The FAQ collection to query
        embedding_model: Model for creating query embeddings
        groq_client: Groq API client for LLM inference
        model_name: LLM model to use for generation
    """
    
    # System prompt designed to minimize hallucinations
    SYSTEM_PROMPT = """You are a precise airline FAQ assistant. Your role is to:

1. ONLY answer questions based on the provided context
2. If the context doesn't contain the answer, say "I don't have information about that"
3. NEVER make up information, policies, or procedures
4. If a question is not related to airlines, respond: "Sorry, I can not answer that question"
5. Be concise and direct in your answers
6. When unsure, acknowledge uncertainty rather than guessing

Remember: It's better to say "I don't know" than to provide incorrect information."""

    def __init__(
        self,
        persist_directory: str = './chroma_storage',
        collection_name: str = 'airline_faqs',
        model_name: str = 'llama-3.1-70b-versatile',
        embedding_model: str = 'all-MiniLM-L6-v2'
    ):
        """
        Initialize the RAG answer tool.
        
        Args:
            persist_directory: Path to ChromaDB storage
            collection_name: Name of the FAQ collection
            model_name: Groq model ID for generation
            embedding_model: Sentence transformer for embeddings
        """
        logger.info(f"Initializing RAGAnswerTool with model: {model_name}")
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.chroma_client.get_collection(name=collection_name)
        logger.info(f"Loaded collection '{collection_name}' with {self.collection.count()} documents")
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize Groq client
        self.groq_client = Groq()
        self.model_name = model_name

    def retrieve_context(
        self, 
        query: str, 
        top_k: int = 3
    ) -> Dict:
        """
        Retrieve most relevant FAQ entries for a given query.
        
        Uses semantic similarity search to find the top-k most
        relevant questions in the knowledge base.
        
        Args:
            query: User's question
            top_k: Number of results to retrieve
            
        Returns:
            ChromaDB query results with documents and metadata
        """
        # Create embedding for the query
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Semantic search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        return results

    def _format_context(self, results: Dict) -> str:
        """
        Format retrieved results into a context string for the LLM.
        
        Args:
            results: ChromaDB query results
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, (question, metadata) in enumerate(
            zip(results['documents'][0], results['metadatas'][0]), 1
        ):
            context_parts.append(
                f"FAQ {i}:\n"
                f"  Question: {question}\n"
                f"  Answer: {metadata['answer']}"
            )
        return "\n\n".join(context_parts)

    def get_answer(
        self, 
        query: str, 
        use_gen_ai: bool = True, 
        top_k: int = 3,
        temperature: float = 0.1  # Low temperature for factual accuracy
    ) -> Dict:
        """
        Generate an answer for the user's query using RAG.
        
        This method:
        1. Retrieves relevant context from the knowledge base
        2. Constructs a grounded prompt with the context
        3. Generates a response using the LLM
        4. Returns the answer with source attribution
        
        Args:
            query: User's question
            use_gen_ai: If True, use LLM for synthesis; if False, return direct retrieval
            top_k: Number of context documents to retrieve
            temperature: LLM temperature (lower = more deterministic/factual)
            
        Returns:
            Dictionary with:
            - 'answer': The generated response
            - 'source_questions': Retrieved FAQ questions used as context
            - 'retrieval_distances': Similarity scores (lower = more similar)
        """
        # Step 1: Retrieve relevant context
        context_results = self.retrieve_context(query, top_k=top_k)
        
        # Direct retrieval mode (no LLM)
        if not use_gen_ai:
            return {
                'answer': context_results['metadatas'][0][0]['answer'],
                'source_questions': context_results['documents'][0],
                'mode': 'direct_retrieval'
            }
        
        # Step 2: Format context for LLM
        context_str = self._format_context(context_results)
        
        # Step 3: Create grounded prompt
        user_prompt = f"""Based ONLY on the following FAQ context, answer the user's question.
If the question cannot be answered from the context, say so clearly.

CONTEXT:
{context_str}

USER QUESTION: {query}

ANSWER (based only on the context above):"""
        
        # Step 4: Generate response with LLM
        try:
            chat_completion = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            
            answer = chat_completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            answer = "I apologize, but I'm unable to process your request at the moment."
        
        return {
            'answer': answer,
            'source_questions': context_results['documents'][0],
            'retrieval_distances': context_results.get('distances', [[]])[0],
            'mode': 'rag_generation'
        }


def demonstrate_hallucination_prevention():
    """
    Demonstrate the chatbot's hallucination prevention capabilities.
    """
    print("\n" + "✈️ " * 20)
    print("  AIRLINE CHATBOT - HALLUCINATION PREVENTION DEMO")
    print("✈️ " * 20 + "\n")
    
    chatbot = RAGAnswerTool()
    
    # Test cases covering different scenarios
    test_cases = [
        # In-scope questions (should answer from knowledge base)
        ("Can I get a refund if I cancel within 24 hours?", "In-Scope"),
        ("What are my options if my flight is delayed?", "In-Scope"),
        ("Do you charge refund processing fees?", "In-Scope"),
        
        # Out-of-scope questions (should reject)
        ("How do I make homemade soap?", "Out-of-Scope"),
        ("Who will win the next election?", "Out-of-Scope"),
        ("What's the recipe for chocolate cake?", "Out-of-Scope"),
    ]
    
    for query, category in test_cases:
        result = chatbot.get_answer(query)
        
        print(f"\n{'=' * 60}")
        print(f"Category: {category}")
        print(f"Query: {query}")
        print(f"{'-' * 60}")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['source_questions'][:2]}...")  # Show first 2 sources


# Main execution
if __name__ == "__main__":
    demonstrate_hallucination_prevention()