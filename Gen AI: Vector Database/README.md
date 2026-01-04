# Gen AI: Vector Databases

## 📖 Overview

This module covers **Vector Databases**, a fundamental component for building modern Generative AI applications. Vector databases enable semantic search capabilities by storing and retrieving data based on meaning rather than exact keyword matches—making them essential for RAG (Retrieval-Augmented Generation) systems, recommendation engines, and intelligent search applications.

---

## 💾 What is a Vector Database?

A **Vector Database** is a specialized storage system designed to store, index, and query **high-dimensional vectors (embeddings)**. Unlike traditional databases that search based on exact matches or predefined indexes, vector databases perform **similarity searches** to find the most semantically related data.

### How It Works

1. **Text → Embedding**: Raw text (or other data) is converted into numerical vectors using embedding models
2. **Storage**: These vectors are stored in the database with associated metadata
3. **Query**: When you search, your query is also converted to a vector
4. **Similarity Search**: The database finds vectors closest to your query vector
5. **Retrieval**: Returns the most semantically similar results

### Why Vector Databases Matter for GenAI

| Traditional Database       | Vector Database                                                |
| -------------------------- | -------------------------------------------------------------- |
| Exact keyword matching     | Semantic similarity matching                                   |
| "apple" only finds "apple" | "apple" can find "iPhone", "fruit", "orchard" based on context |
| SQL queries                | Vector similarity queries                                      |
| Structured data            | Unstructured text, images, audio                               |

### Popular Vector Databases

| Database     | Type                          | Best For                                         |
| ------------ | ----------------------------- | ------------------------------------------------ |
| **ChromaDB** | Open-source, lightweight      | Local development, prototyping, small-scale apps |
| **Pinecone** | Managed (cloud)               | Production applications, scalability             |
| **Milvus**   | Open-source, scalable         | Large-scale enterprise deployments               |
| **Qdrant**   | Open-source, high-performance | Real-time applications, filtering                |
| **Weaviate** | Open-source                   | Multi-modal data (text, images)                  |

---

## 📐 Similarity Metrics

When comparing vectors, the choice of **distance metric** significantly impacts search accuracy. The two most common metrics are:

### 1. Euclidean Distance (L2)

**Definition**: Measures the straight-line distance between two points in vector space.

```
Distance = √[(x₁-y₁)² + (x₂-y₂)² + ... + (xₙ-yₙ)²]
```

| Aspect          | Description                                   |
| --------------- | --------------------------------------------- |
| **Sensitivity** | Sensitive to vector **magnitude** (length)    |
| **Best For**    | Dense embeddings where absolute values matter |
| **Use Cases**   | Image similarity, spatial data                |

### 2. Cosine Distance

**Definition**: Measures the **angle** between two vectors, ignoring their magnitude.

```
Similarity = (A · B) / (||A|| × ||B||)
Distance = 1 - Similarity
```

| Aspect          | Description                                           |
| --------------- | ----------------------------------------------------- |
| **Sensitivity** | Focuses on **direction/orientation**, scale-invariant |
| **Best For**    | Sparse or high-dimensional data                       |
| **Use Cases**   | Text similarity, document search, NLP applications    |

### Quick Comparison

| Metric    | Magnitude Sensitive | Best For                     |
| --------- | ------------------- | ---------------------------- |
| Euclidean | ✅ Yes              | Dense embeddings, images     |
| Cosine    | ❌ No               | Text, documents, sparse data |

---

## 🗂️ Module Structure

```
Gen AI: Vector Database/
├── README.md                    # This file
├── docs/                        # Detailed documentation
│   ├── README.md                     # Documentation index
│   ├── 01-what-is-vector-database.md # Vector DB fundamentals
│   ├── 02-similarity-metrics.md      # Distance metrics explained
│   ├── 03-popular-vector-databases.md # DB comparison guide
│   ├── 04-chromadb-basics.md         # ChromaDB getting started
│   ├── 05-crud-operations.md         # Create, Read, Update, Delete
│   └── 06-metadata-filtering.md      # Advanced filtering
└── notebooks/
    ├── 1_chromadb_basics.ipynb       # Getting started with ChromaDB
    ├── 2_add_update_delete.ipynb     # CRUD operations
    ├── 3_metadata_filtering.ipynb    # Advanced querying
    └── chromadb_data/                # Persistent storage
```

---

## 📓 Notebooks

### 1. ChromaDB Basics (`1_chromadb_basics.ipynb`)

**Learn the fundamentals of ChromaDB**

**Topics Covered:**

- Installing and importing ChromaDB
- Creating in-memory vs. persistent clients
- Creating and managing collections
- Adding documents with automatic embedding generation
- Performing basic similarity queries
- Using custom embedding functions (SentenceTransformers)

**Key Concepts:**

```python
# In-memory client (data lost when session ends)
client = chromadb.Client()

# Persistent client (data saved to disk)
client = chromadb.PersistentClient(path="./chromadb_data")

# Create a collection
collection = client.create_collection(name="my_collection")

# Add documents (embeddings generated automatically)
collection.add(
    documents=["Document 1", "Document 2"],
    ids=["id1", "id2"]
)

# Query for similar documents
results = collection.query(
    query_texts=["Search query"],
    n_results=2
)
```

**Custom Embedding Functions:**

```python
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L12-v2"
)

collection = client.create_collection(
    name="custom_embeddings",
    embedding_function=ef
)
```

---

### 2. Add, Update, Delete (`2_add_update_delete.ipynb`)

**Master CRUD operations in ChromaDB**

**Topics Covered:**

- Creating collections with metadata
- Adding documents with custom metadata
- Retrieving documents by ID
- Updating existing documents and metadata
- Deleting specific records
- Deleting entire collections

**Key Operations:**

```python
# Create collection with metadata
collection = client.create_collection(
    name="reviews",
    metadata={
        "description": "Product reviews",
        "created": "2024-01-01"
    }
)

# Add documents with metadata
collection.add(
    documents=["Great product!", "Poor quality"],
    ids=["r1", "r2"],
    metadatas=[
        {"category": "electronics", "rating": 5},
        {"category": "electronics", "rating": 1}
    ]
)

# Get specific documents
collection.get(ids=["r1", "r2"])

# Update a document
collection.update(
    documents=["Updated review text"],
    ids=["r1"],
    metadatas=[{"category": "electronics", "rating": 4}]
)

# Delete documents
collection.delete(ids=["r1", "r2"])

# Delete entire collection
client.delete_collection(name="reviews")
```

---

### 3. Metadata Filtering (`3_metadata_filtering.ipynb`)

**Advanced querying with filters**

**Topics Covered:**

- Filtering queries by metadata fields
- Using comparison operators (`$in`, `$gt`, `$lt`, etc.)
- Full-text search with `where_document`
- Controlling output with the `include` parameter

**Metadata Filtering:**

```python
# Filter by exact metadata match
collection.query(
    query_texts=["search term"],
    n_results=2,
    where={"category": "electronics"}
)

# Filter using operators
collection.query(
    query_texts=["search term"],
    n_results=2,
    where={"rating": {"$in": [4, 5]}}  # Rating is 4 OR 5
)
```

**Available Operators:**

| Operator | Description           | Example                                |
| -------- | --------------------- | -------------------------------------- |
| `$eq`    | Equal to              | `{"rating": {"$eq": 5}}`               |
| `$ne`    | Not equal to          | `{"category": {"$ne": "services"}}`    |
| `$gt`    | Greater than          | `{"rating": {"$gt": 3}}`               |
| `$gte`   | Greater than or equal | `{"rating": {"$gte": 4}}`              |
| `$lt`    | Less than             | `{"rating": {"$lt": 3}}`               |
| `$lte`   | Less than or equal    | `{"rating": {"$lte": 2}}`              |
| `$in`    | In list               | `{"rating": {"$in": [1, 2, 3]}}`       |
| `$nin`   | Not in list           | `{"category": {"$nin": ["services"]}}` |

**Full-Text Search:**

```python
# Search within document content
collection.query(
    query_texts=["search term"],
    n_results=2,
    where_document={"$contains": "keyword"}
)
```

**Include Parameter:**

```python
# Control what's returned in results
collection.query(
    query_texts=["search term"],
    n_results=2,
    include=["documents", "metadatas", "embeddings", "distances"]
)
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install chromadb sentence-transformers
```

### Quick Start

```python
import chromadb

# Initialize client
client = chromadb.Client()

# Create collection
collection = client.create_collection("my_first_collection")

# Add some documents
collection.add(
    documents=[
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with many layers.",
        "Python is popular for data science and AI."
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Query for similar documents
results = collection.query(
    query_texts=["What is AI?"],
    n_results=2
)

print(results["documents"])
```

---

## 💡 Best Practices

1. **Use Persistent Storage** for production applications
2. **Choose Appropriate Embedding Models** based on your use case
3. **Add Meaningful Metadata** to enable powerful filtering
4. **Use Batching** when adding large amounts of data
5. **Select the Right Distance Metric** (Cosine for text, Euclidean for images)

---

## 🔗 Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Embedding Models Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)

---

## 📚 Detailed Documentation

For in-depth coverage of each topic, see the [docs folder](./docs/):

| Topic | Description |
|-------|-------------|
| [What is a Vector Database?](./docs/01-what-is-vector-database.md) | Fundamentals, embeddings, and semantic search |
| [Similarity Metrics](./docs/02-similarity-metrics.md) | Euclidean, Cosine, and Dot product explained |
| [Popular Vector Databases](./docs/03-popular-vector-databases.md) | Comparison of ChromaDB, Pinecone, Milvus, and more |
| [ChromaDB Basics](./docs/04-chromadb-basics.md) | Getting started guide with examples |
| [CRUD Operations](./docs/05-crud-operations.md) | Complete data management guide |
| [Metadata Filtering](./docs/06-metadata-filtering.md) | Advanced querying techniques |

---

## ⏭️ Next Steps

After completing this module, you'll be ready to:

- Build RAG (Retrieval-Augmented Generation) applications
- Implement semantic search in your projects
- Create intelligent document retrieval systems
- Integrate vector databases with LLMs for context-aware responses
