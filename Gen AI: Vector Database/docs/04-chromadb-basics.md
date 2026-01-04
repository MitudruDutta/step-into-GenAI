# 🎨 ChromaDB Basics

## 📌 Overview

ChromaDB is a lightweight, open-source embedding database that makes it easy to build AI applications with semantic search. This guide covers everything you need to get started.

---

## 🚀 Installation

```bash
# Basic installation
pip install chromadb

# With sentence-transformers for custom embeddings
pip install chromadb sentence-transformers
```

---

## 🔧 Client Types

ChromaDB offers two client types for different use cases:

### In-Memory Client

Data exists only in memory and is **lost when the session ends**.

```python
import chromadb

# In-memory client (ephemeral)
client = chromadb.Client()
```

| Pros | Cons |
|------|------|
| Fast | Data not persisted |
| No setup | Lost on restart |
| Great for testing | Not for production |

### Persistent Client

Data is **saved to disk** and persists across sessions.

```python
import chromadb

# Persistent client (data saved to disk)
client = chromadb.PersistentClient(path="./chromadb_data")
```

| Pros | Cons |
|------|------|
| Data persists | Slightly slower |
| Survives restarts | Requires disk space |
| Production-ready | Need to manage storage |

### Choosing a Client

```
Testing/Learning → In-Memory Client
Development → Persistent Client
Production → Persistent Client (or ChromaDB Cloud)
```

---

## 📁 Collections

Collections are the primary organizational unit in ChromaDB — similar to tables in traditional databases.

### Creating a Collection

```python
# Create a new collection
collection = client.create_collection(name="my_documents")

# Create with custom settings
collection = client.create_collection(
    name="my_documents",
    metadata={"hnsw:space": "cosine"}  # Distance metric
)
```

### Getting an Existing Collection

```python
# Get existing collection (raises error if not found)
collection = client.get_collection(name="my_documents")

# Get or create (creates if doesn't exist)
collection = client.get_or_create_collection(name="my_documents")
```

### Listing Collections

```python
# List all collections
collections = client.list_collections()
for col in collections:
    print(f"Collection: {col.name}")
```

### Deleting a Collection

```python
# Delete a collection
client.delete_collection(name="my_documents")
```

### Collection Metadata

```python
# Create with metadata
collection = client.create_collection(
    name="product_reviews",
    metadata={
        "description": "Customer product reviews",
        "created_by": "data_team",
        "hnsw:space": "cosine"  # Distance metric
    }
)

# Access metadata
print(collection.metadata)
```

---

## 📝 Adding Documents

### Basic Addition

ChromaDB can automatically generate embeddings for your documents:

```python
# Add documents with automatic embedding
collection.add(
    documents=[
        "Machine learning is fascinating",
        "I love programming in Python",
        "Data science combines statistics and coding"
    ],
    ids=["doc1", "doc2", "doc3"]
)
```

### Adding with Metadata

Metadata enables powerful filtering during queries:

```python
collection.add(
    documents=[
        "Great product, highly recommend!",
        "Terrible experience, avoid this.",
        "Average quality, nothing special."
    ],
    ids=["review1", "review2", "review3"],
    metadatas=[
        {"rating": 5, "category": "electronics", "verified": True},
        {"rating": 1, "category": "electronics", "verified": False},
        {"rating": 3, "category": "clothing", "verified": True}
    ]
)
```

### Adding Pre-computed Embeddings

If you've already generated embeddings:

```python
import numpy as np

# Your pre-computed embeddings
embeddings = [
    [0.1, 0.2, 0.3, ...],  # 384 dimensions typically
    [0.4, 0.5, 0.6, ...],
    [0.7, 0.8, 0.9, ...]
]

collection.add(
    embeddings=embeddings,
    documents=["Doc 1", "Doc 2", "Doc 3"],
    ids=["id1", "id2", "id3"]
)
```

### Important Rules for Adding

| Rule | Description |
|------|-------------|
| **Unique IDs** | Each document must have a unique ID |
| **Matching Lengths** | documents, ids, metadatas must have same length |
| **ID Format** | IDs must be strings |
| **No Duplicates** | Adding existing ID will fail (use upsert instead) |

---

## 🔍 Querying Documents

### Basic Query

```python
# Query with text (auto-embedded)
results = collection.query(
    query_texts=["What is machine learning?"],
    n_results=3
)

print(results)
```

### Understanding Query Results

```python
results = collection.query(
    query_texts=["search term"],
    n_results=2
)

# Results structure
{
    'ids': [['doc1', 'doc3']],           # Matched document IDs
    'documents': [['text1', 'text3']],    # Document content
    'metadatas': [[{...}, {...}]],        # Associated metadata
    'distances': [[0.23, 0.45]]           # Distance scores (lower = more similar)
}

# Accessing results
for i, doc_id in enumerate(results['ids'][0]):
    print(f"ID: {doc_id}")
    print(f"Document: {results['documents'][0][i]}")
    print(f"Distance: {results['distances'][0][i]}")
    print("---")
```

### Query with Pre-computed Embeddings

```python
# If you have your own query embedding
query_embedding = [0.1, 0.2, 0.3, ...]

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)
```

### Multiple Queries at Once

```python
# Batch queries
results = collection.query(
    query_texts=[
        "First search query",
        "Second search query",
        "Third search query"
    ],
    n_results=3
)

# results['ids'] will have 3 lists, one per query
```


---

## 🎯 Custom Embedding Functions

By default, ChromaDB uses a built-in embedding model. You can customize this for better results.

### Using Sentence Transformers

```python
from chromadb.utils import embedding_functions

# Create embedding function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Use with collection
collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=sentence_transformer_ef
)
```

### Popular Embedding Models

| Model | Dimensions | Speed | Quality |
|-------|------------|-------|---------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good |
| `all-MiniLM-L12-v2` | 384 | Medium | Better |
| `all-mpnet-base-v2` | 768 | Slower | Best |
| `paraphrase-MiniLM-L6-v2` | 384 | Fast | Good for paraphrases |

### Using OpenAI Embeddings

```python
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-api-key",
    model_name="text-embedding-ada-002"
)

collection = client.create_collection(
    name="openai_embeddings",
    embedding_function=openai_ef
)
```

### Using Hugging Face Models

```python
from chromadb.utils import embedding_functions

huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="your-api-key",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Custom Embedding Function

```python
from chromadb import EmbeddingFunction, Documents, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Your custom embedding logic
        embeddings = []
        for doc in input:
            # Generate embedding for each document
            embedding = your_model.encode(doc)
            embeddings.append(embedding.tolist())
        return embeddings

# Use custom function
collection = client.create_collection(
    name="custom",
    embedding_function=MyEmbeddingFunction()
)
```

---

## 📊 Collection Information

### Get Collection Count

```python
# Number of documents in collection
count = collection.count()
print(f"Documents in collection: {count}")
```

### Peek at Collection

```python
# Preview first 10 documents
preview = collection.peek(limit=10)
print(preview)
```

### Get All Documents

```python
# Retrieve all documents (use with caution for large collections)
all_docs = collection.get()

# Get specific fields
all_docs = collection.get(
    include=["documents", "metadatas", "embeddings"]
)
```

---

## 💾 Persistence Example

### Complete Workflow

```python
import chromadb

# === Session 1: Create and populate ===
client = chromadb.PersistentClient(path="./my_vectordb")

collection = client.get_or_create_collection("knowledge_base")

collection.add(
    documents=[
        "Python is a programming language",
        "Machine learning uses algorithms",
        "Data science analyzes data"
    ],
    ids=["py1", "ml1", "ds1"]
)

print(f"Added {collection.count()} documents")
# Session ends, data is saved

# === Session 2: Load and query ===
client = chromadb.PersistentClient(path="./my_vectordb")

collection = client.get_collection("knowledge_base")

print(f"Loaded {collection.count()} documents")

results = collection.query(
    query_texts=["What is Python?"],
    n_results=2
)
print(results['documents'])
```

---

## ⚠️ Common Errors and Solutions

### Duplicate ID Error

```python
# ❌ Error: ID already exists
collection.add(documents=["New doc"], ids=["existing_id"])

# ✅ Solution: Use upsert instead
collection.upsert(documents=["New doc"], ids=["existing_id"])
```

### Collection Not Found

```python
# ❌ Error: Collection doesn't exist
collection = client.get_collection("nonexistent")

# ✅ Solution: Use get_or_create
collection = client.get_or_create_collection("my_collection")
```

### Mismatched Lengths

```python
# ❌ Error: Lists have different lengths
collection.add(
    documents=["doc1", "doc2"],
    ids=["id1"]  # Only 1 ID for 2 documents!
)

# ✅ Solution: Ensure matching lengths
collection.add(
    documents=["doc1", "doc2"],
    ids=["id1", "id2"]
)
```

---

## 🎯 Best Practices

### 1. Use Meaningful IDs

```python
# ❌ Bad: Generic IDs
ids = ["1", "2", "3"]

# ✅ Good: Descriptive IDs
ids = ["product_review_123", "article_456", "faq_789"]
```

### 2. Add Rich Metadata

```python
# ✅ Good: Comprehensive metadata for filtering
collection.add(
    documents=["Great laptop for coding"],
    ids=["review_001"],
    metadatas=[{
        "product_id": "laptop_123",
        "rating": 5,
        "category": "electronics",
        "date": "2024-01-15",
        "verified_purchase": True
    }]
)
```

### 3. Choose Appropriate Embedding Model

```python
# For general text: all-MiniLM-L6-v2 (fast, good quality)
# For better quality: all-mpnet-base-v2 (slower, better)
# For production: Consider OpenAI or domain-specific models
```

### 4. Use Persistent Client for Important Data

```python
# Always use persistent client for data you want to keep
client = chromadb.PersistentClient(path="./production_db")
```

---

## 📚 Related Topics

- [What is a Vector Database?](./01-what-is-vector-database.md)
- [Similarity Metrics](./02-similarity-metrics.md)
- [Popular Vector Databases](./03-popular-vector-databases.md)
- [CRUD Operations](./05-crud-operations.md)
- [Metadata Filtering](./06-metadata-filtering.md)

---

_Last Updated: January 2026_
