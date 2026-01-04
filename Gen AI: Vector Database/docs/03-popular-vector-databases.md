# 🗄️ Popular Vector Databases

## 📌 Overview

The vector database landscape has grown rapidly with the rise of AI applications. This guide covers the most popular options, their strengths, and when to use each.

---

## 🏆 Vector Database Comparison

### Quick Comparison Table

| Database | Type | Best For | Pricing |
|----------|------|----------|---------|
| **ChromaDB** | Open-source | Prototyping, local dev | Free |
| **Pinecone** | Managed cloud | Production, scalability | Pay-per-use |
| **Milvus** | Open-source | Enterprise, large scale | Free (self-hosted) |
| **Qdrant** | Open-source | Real-time, filtering | Free (self-hosted) |
| **Weaviate** | Open-source | Multi-modal, GraphQL | Free (self-hosted) |
| **pgvector** | PostgreSQL extension | Existing Postgres users | Free |
| **FAISS** | Library | Research, custom solutions | Free |

---

## 🎨 ChromaDB

### Overview

ChromaDB is a lightweight, open-source embedding database designed for **simplicity and ease of use**. It's the go-to choice for prototyping and learning.

### Key Features

| Feature | Description |
|---------|-------------|
| **Simplicity** | Minimal setup, intuitive API |
| **Embedding Functions** | Built-in support for popular models |
| **Persistence** | In-memory or disk storage |
| **Metadata Filtering** | Rich query capabilities |
| **Python-First** | Native Python experience |

### Installation

```bash
pip install chromadb
```

### Quick Example

```python
import chromadb

# Create client
client = chromadb.Client()

# Create collection
collection = client.create_collection("my_collection")

# Add documents
collection.add(
    documents=["Hello world", "Goodbye world"],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["Hi there"],
    n_results=1
)
```

### When to Use ChromaDB

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Learning/prototyping | Need massive scale |
| Local development | Require managed service |
| Small to medium datasets | Need advanced clustering |
| Quick experimentation | Enterprise compliance needs |

### Pros & Cons

| Pros | Cons |
|------|------|
| Very easy to start | Limited scalability |
| Great documentation | Fewer enterprise features |
| Active community | Single-node only |
| No infrastructure needed | Less mature than alternatives |

---

## 🌲 Pinecone

### Overview

Pinecone is a **fully managed vector database** designed for production AI applications. It handles infrastructure, scaling, and maintenance automatically.

### Key Features

| Feature | Description |
|---------|-------------|
| **Fully Managed** | No infrastructure to manage |
| **Scalability** | Handles billions of vectors |
| **Low Latency** | Optimized for real-time queries |
| **Hybrid Search** | Combine vector + keyword search |
| **Namespaces** | Logical partitioning of data |

### Installation

```bash
pip install pinecone-client
```

### Quick Example

```python
from pinecone import Pinecone

# Initialize
pc = Pinecone(api_key="your-api-key")

# Create index
pc.create_index(
    name="my-index",
    dimension=384,
    metric="cosine"
)

# Connect to index
index = pc.Index("my-index")

# Upsert vectors
index.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"genre": "comedy"}},
        {"id": "vec2", "values": [0.3, 0.4, ...], "metadata": {"genre": "drama"}}
    ]
)

# Query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    include_metadata=True
)
```

### When to Use Pinecone

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Production applications | Budget constraints |
| Need managed service | Data sovereignty requirements |
| Require high availability | Simple prototyping |
| Scale is important | Learning/experimentation |

### Pricing Model

| Tier | Description |
|------|-------------|
| **Starter** | Free tier with limits |
| **Standard** | Pay-per-use |
| **Enterprise** | Custom pricing |

---

## 🐋 Milvus

### Overview

Milvus is an **open-source, highly scalable** vector database designed for enterprise-grade AI applications. It can handle billions of vectors with high performance.

### Key Features

| Feature | Description |
|---------|-------------|
| **Scalability** | Distributed architecture |
| **Multiple Indexes** | HNSW, IVF, DiskANN, etc. |
| **GPU Support** | Hardware acceleration |
| **Hybrid Search** | Vector + scalar filtering |
| **Cloud Option** | Zilliz Cloud (managed) |

### Installation

```bash
# Using Docker
docker-compose up -d

# Python client
pip install pymilvus
```

### Quick Example

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# Connect
connections.connect("default", host="localhost", port="19530")

# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
]
schema = CollectionSchema(fields, "My collection")

# Create collection
collection = Collection("my_collection", schema)

# Insert data
collection.insert([[1, 2], [[0.1, 0.2, ...], [0.3, 0.4, ...]]])

# Create index
collection.create_index("embedding", {"index_type": "HNSW", "metric_type": "COSINE"})

# Search
collection.load()
results = collection.search(
    data=[[0.1, 0.2, ...]],
    anns_field="embedding",
    limit=5
)
```

### When to Use Milvus

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Enterprise scale needed | Simple use cases |
| Billions of vectors | Quick prototyping |
| Need GPU acceleration | Limited infrastructure |
| Self-hosting preferred | Want managed service |


---

## 🔷 Qdrant

### Overview

Qdrant is a **high-performance, open-source** vector database with excellent filtering capabilities and a modern API.

### Key Features

| Feature | Description |
|---------|-------------|
| **Rich Filtering** | Advanced metadata filtering |
| **Payload Storage** | Store any JSON with vectors |
| **Quantization** | Memory-efficient storage |
| **Distributed** | Horizontal scaling |
| **REST & gRPC** | Multiple API options |

### Installation

```bash
# Docker
docker run -p 6333:6333 qdrant/qdrant

# Python client
pip install qdrant-client
```

### Quick Example

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect
client = QdrantClient("localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="my_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Insert points
client.upsert(
    collection_name="my_collection",
    points=[
        PointStruct(id=1, vector=[0.1, 0.2, ...], payload={"city": "London"}),
        PointStruct(id=2, vector=[0.3, 0.4, ...], payload={"city": "Paris"})
    ]
)

# Search with filter
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, ...],
    query_filter={"must": [{"key": "city", "match": {"value": "London"}}]},
    limit=5
)
```

### When to Use Qdrant

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Need advanced filtering | Simplest possible setup |
| Real-time applications | Already using another DB |
| Self-hosting preferred | Need managed service |
| Modern API desired | Legacy system integration |

---

## 🌐 Weaviate

### Overview

Weaviate is an **open-source vector database** with built-in vectorization modules and GraphQL API. It excels at multi-modal data.

### Key Features

| Feature | Description |
|---------|-------------|
| **Built-in Vectorization** | Automatic embedding generation |
| **GraphQL API** | Flexible querying |
| **Multi-Modal** | Text, images, and more |
| **Modules** | Extensible architecture |
| **Hybrid Search** | BM25 + vector search |

### Installation

```bash
# Docker
docker-compose up -d

# Python client
pip install weaviate-client
```

### Quick Example

```python
import weaviate

# Connect
client = weaviate.Client("http://localhost:8080")

# Create schema
class_obj = {
    "class": "Article",
    "vectorizer": "text2vec-transformers",
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "content", "dataType": ["text"]}
    ]
}
client.schema.create_class(class_obj)

# Add data (auto-vectorized)
client.data_object.create(
    {"title": "AI News", "content": "Latest developments..."},
    "Article"
)

# Query with GraphQL
result = client.query.get("Article", ["title", "content"]) \
    .with_near_text({"concepts": ["artificial intelligence"]}) \
    .with_limit(5) \
    .do()
```

### When to Use Weaviate

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Multi-modal data | Simple text-only use case |
| Want auto-vectorization | Need fine-grained control |
| GraphQL preferred | REST API preferred |
| Module ecosystem needed | Minimal dependencies wanted |

---

## 🐘 pgvector

### Overview

pgvector is a **PostgreSQL extension** that adds vector similarity search to your existing Postgres database.

### Key Features

| Feature | Description |
|---------|-------------|
| **PostgreSQL Native** | Use existing Postgres skills |
| **ACID Compliant** | Full transaction support |
| **SQL Interface** | Familiar query language |
| **Hybrid Queries** | Combine with regular SQL |
| **No New Infrastructure** | Add to existing Postgres |

### Installation

```sql
-- In PostgreSQL
CREATE EXTENSION vector;
```

```bash
# Python
pip install pgvector psycopg2
```

### Quick Example

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect("postgresql://localhost/mydb")
register_vector(conn)

# Create table
cur = conn.cursor()
cur.execute("""
    CREATE TABLE items (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)
    )
""")

# Insert
cur.execute(
    "INSERT INTO items (content, embedding) VALUES (%s, %s)",
    ("Hello world", [0.1, 0.2, ...])
)

# Query (cosine similarity)
cur.execute("""
    SELECT content, 1 - (embedding <=> %s) AS similarity
    FROM items
    ORDER BY embedding <=> %s
    LIMIT 5
""", ([0.1, 0.2, ...], [0.1, 0.2, ...]))
```

### When to Use pgvector

| ✅ Use When | ❌ Avoid When |
|------------|--------------|
| Already using PostgreSQL | Need specialized features |
| Want SQL interface | Billions of vectors |
| ACID compliance needed | Maximum performance critical |
| Hybrid queries important | Dedicated vector DB preferred |

---

## 📊 Detailed Comparison

### Performance & Scale

| Database | Max Vectors | Query Latency | Throughput |
|----------|-------------|---------------|------------|
| ChromaDB | Millions | ~10-50ms | Medium |
| Pinecone | Billions | ~10-20ms | High |
| Milvus | Billions | ~5-20ms | Very High |
| Qdrant | Billions | ~5-15ms | High |
| Weaviate | Billions | ~10-30ms | High |
| pgvector | Millions | ~20-100ms | Medium |

### Feature Matrix

| Feature | ChromaDB | Pinecone | Milvus | Qdrant | Weaviate | pgvector |
|---------|----------|----------|--------|--------|----------|----------|
| Open Source | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Managed Cloud | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Filtering | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hybrid Search | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GPU Support | ❌ | N/A | ✅ | ❌ | ❌ | ❌ |
| Multi-Modal | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 🎯 Choosing the Right Database

### Decision Guide

```
Start
  │
  ▼
Learning/Prototyping?
  │
  ├─ YES → ChromaDB
  │
  └─ NO
      │
      ▼
    Need managed service?
      │
      ├─ YES → Pinecone
      │
      └─ NO
          │
          ▼
        Already using PostgreSQL?
          │
          ├─ YES → pgvector
          │
          └─ NO
              │
              ▼
            Need multi-modal?
              │
              ├─ YES → Weaviate
              │
              └─ NO
                  │
                  ▼
                Enterprise scale?
                  │
                  ├─ YES → Milvus
                  │
                  └─ NO → Qdrant
```

---

## 📚 Related Topics

- [What is a Vector Database?](./01-what-is-vector-database.md)
- [Similarity Metrics](./02-similarity-metrics.md)
- [ChromaDB Basics](./04-chromadb-basics.md)
- [CRUD Operations](./05-crud-operations.md)
- [Metadata Filtering](./06-metadata-filtering.md)

---

_Last Updated: January 2026_
