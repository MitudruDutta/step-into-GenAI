"""
Knowledge Base Ingestion for RAG-based Hallucination Prevention
================================================================

This module ingests FAQ data into a ChromaDB vector store for use with
Retrieval-Augmented Generation (RAG) to reduce LLM hallucinations.

Why RAG Reduces Hallucinations:
-------------------------------
1. Grounds responses in verified knowledge base
2. Provides citations/sources for answers
3. Limits LLM to domain-specific information
4. Enables fact-checking against retrieved context

Architecture:
-------------
    CSV FAQ Data → Sentence Embeddings → ChromaDB Vector Store
                                              ↓
                            Query → Semantic Search → Context → LLM → Answer

Usage:
    python ingest_data.py
    # Creates ./chroma_storage/ with embedded FAQ data
"""

import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def build_knowledge(
    csv_path: str,
    collection_name: str = 'faq_collection',
    embedding_model: str = 'all-MiniLM-L6-v2',
    persist_directory: Optional[str] = None
) -> chromadb.Collection:
    """
    Ingest CSV FAQ data into a ChromaDB vector store with embeddings.
    
    This function creates a searchable knowledge base that enables
    semantic similarity search for RAG-based question answering.
    
    Args:
        csv_path: Path to CSV file with 'Question' and 'Answer' columns
        collection_name: Name for the ChromaDB collection
        embedding_model: Sentence transformer model for creating embeddings
                        (all-MiniLM-L6-v2 is fast and effective)
        persist_directory: Directory to persist ChromaDB data (for reuse)
    
    Returns:
        chromadb.Collection: Populated vector store collection
        
    CSV Format Expected:
        Question,Answer
        "How do I...", "You can..."
        ...
        
    Example:
        >>> collection = build_knowledge(
        ...     csv_path='airline_faq.csv',
        ...     persist_directory='./chroma_storage',
        ...     collection_name='airline_faqs'
        ... )
        >>> print(f"Ingested {collection.count()} documents")
    """
    logger.info(f"Starting knowledge base ingestion from {csv_path}")
    
    # Initialize the embedding model
    logger.info(f"Loading embedding model: {embedding_model}")
    model = SentenceTransformer(embedding_model)
    
    # Configure ChromaDB client with persistence
    if persist_directory:
        logger.info(f"Using persistent storage: {persist_directory}")
        chroma_client = chromadb.PersistentClient(path=persist_directory)
    else:
        logger.info("Using in-memory storage (data will not persist)")
        chroma_client = chromadb.Client()
    
    # Create or get collection (delete existing to avoid duplicates)
    try:
        chroma_client.delete_collection(name=collection_name)
        logger.info(f"Deleted existing collection: {collection_name}")
    except ValueError:
        pass  # Collection doesn't exist, which is fine
    
    collection = chroma_client.create_collection(
        name=collection_name,
        metadata={"description": "FAQ knowledge base for RAG"}
    )
    logger.info(f"Created collection: {collection_name}")
    
    # Load and validate CSV
    df = pd.read_csv(csv_path)
    required_columns = {'Question', 'Answer'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_columns}")
    
    logger.info(f"Loaded {len(df)} FAQ entries from CSV")
    
    # Generate embeddings for questions
    logger.info("Generating embeddings for questions...")
    questions = df['Question'].tolist()
    embeddings = model.encode(questions, show_progress_bar=True).tolist()
    
    # Prepare metadata (including answers)
    metadatas = [
        {
            'answer': row['Answer'],
            'source': csv_path,
            'index': idx
        }
        for idx, row in df.iterrows()
    ]
    
    # Add to collection
    collection.add(
        embeddings=embeddings,
        documents=questions,
        metadatas=metadatas,
        ids=[f'faq_{i}' for i in range(len(df))]
    )
    
    logger.info(f"✅ Successfully ingested {collection.count()} documents into '{collection_name}'")
    
    return collection


def verify_ingestion(collection: chromadb.Collection, test_query: str = "refund policy"):
    """
    Verify the knowledge base by running a test query.
    
    Args:
        collection: ChromaDB collection to test
        test_query: Sample query to run
    """
    logger.info(f"\nVerifying ingestion with test query: '{test_query}'")
    
    # Load embedding model for query
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([test_query])[0].tolist()
    
    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    print("\n" + "=" * 60)
    print(f"TEST QUERY: '{test_query}'")
    print("=" * 60)
    print("\nTop 3 Retrieved Results:")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\n{i}. Question: {doc}")
        print(f"   Answer: {meta['answer'][:100]}...")


# Main execution
if __name__ == "__main__":
    print("\n" + "🗄️ " * 20)
    print("  KNOWLEDGE BASE INGESTION FOR RAG")
    print("🗄️ " * 20 + "\n")
    
    collection = build_knowledge(
        csv_path='airline_faq.csv',
        persist_directory='./chroma_storage',
        collection_name='airline_faqs'
    )
    
    # Verify with a test query
    verify_ingestion(collection, test_query="cancel flight refund")