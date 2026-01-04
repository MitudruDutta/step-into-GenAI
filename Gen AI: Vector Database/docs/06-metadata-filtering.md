# 🔍 Metadata Filtering in ChromaDB

## 📌 Overview

Metadata filtering allows you to **narrow down search results** based on structured data associated with your documents. This combines the power of semantic search with traditional database filtering.

---

## 🎯 Why Metadata Filtering?

Without filtering, semantic search returns the most similar documents regardless of other criteria:

```python
# Without filtering - might return irrelevant results
results = collection.query(
    query_texts=["comfortable shoes"],
    n_results=5
)
# Could return: out-of-stock items, wrong sizes, different categories
```

With filtering, you get relevant AND appropriate results:

```python
# With filtering - precise results
results = collection.query(
    query_texts=["comfortable shoes"],
    n_results=5,
    where={
        "$and": [
            {"category": "footwear"},
            {"in_stock": True},
            {"size": {"$in": [9, 10, 11]}}
        ]
    }
)
# Returns: in-stock shoes in the right sizes
```

---

## 📊 Setting Up Metadata

### Adding Documents with Metadata

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("products")

collection.add(
    documents=[
        "Premium wireless noise-canceling headphones",
        "Budget wired earbuds with microphone",
        "Professional studio monitor headphones",
        "Sports bluetooth earbuds waterproof",
        "Kids volume-limited headphones"
    ],
    ids=["prod_001", "prod_002", "prod_003", "prod_004", "prod_005"],
    metadatas=[
        {"category": "audio", "type": "headphones", "price": 299.99, "wireless": True, "rating": 4.8},
        {"category": "audio", "type": "earbuds", "price": 19.99, "wireless": False, "rating": 4.2},
        {"category": "audio", "type": "headphones", "price": 449.99, "wireless": False, "rating": 4.9},
        {"category": "audio", "type": "earbuds", "price": 79.99, "wireless": True, "rating": 4.5},
        {"category": "audio", "type": "headphones", "price": 29.99, "wireless": True, "rating": 4.3}
    ]
)
```

### Supported Metadata Types

| Type | Example | Notes |
|------|---------|-------|
| **String** | `"electronics"` | Case-sensitive |
| **Integer** | `42` | Whole numbers |
| **Float** | `99.99` | Decimal numbers |
| **Boolean** | `True` / `False` | True or False |

```python
# ✅ Valid metadata
metadata = {
    "category": "electronics",  # string
    "price": 99.99,            # float
    "quantity": 50,            # integer
    "in_stock": True           # boolean
}

# ❌ Invalid metadata (nested objects, lists)
metadata = {
    "tags": ["sale", "new"],   # Lists not supported
    "details": {"color": "red"}  # Nested objects not supported
}
```

---

## 🔧 Basic Filtering

### Exact Match

```python
# Filter by exact value
results = collection.query(
    query_texts=["audio device"],
    n_results=5,
    where={"type": "headphones"}
)
```

### Using the `where` Parameter

The `where` parameter accepts a dictionary with filter conditions:

```python
# Single condition
where={"category": "audio"}

# Implicit equality
where={"price": 29.99}  # Same as {"price": {"$eq": 29.99}}
```

---

## 🔢 Comparison Operators

### Available Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$eq` | Equal to | `{"price": {"$eq": 100}}` |
| `$ne` | Not equal to | `{"status": {"$ne": "discontinued"}}` |
| `$gt` | Greater than | `{"price": {"$gt": 50}}` |
| `$gte` | Greater than or equal | `{"rating": {"$gte": 4.0}}` |
| `$lt` | Less than | `{"price": {"$lt": 100}}` |
| `$lte` | Less than or equal | `{"quantity": {"$lte": 10}}` |
| `$in` | In list | `{"size": {"$in": [8, 9, 10]}}` |
| `$nin` | Not in list | `{"color": {"$nin": ["red", "blue"]}}` |

### Operator Examples

```python
# Greater than
results = collection.query(
    query_texts=["headphones"],
    n_results=5,
    where={"price": {"$gt": 100}}
)

# Less than or equal
results = collection.query(
    query_texts=["budget audio"],
    n_results=5,
    where={"price": {"$lte": 50}}
)

# In list
results = collection.query(
    query_texts=["wireless audio"],
    n_results=5,
    where={"type": {"$in": ["headphones", "earbuds"]}}
)

# Not in list
results = collection.query(
    query_texts=["audio"],
    n_results=5,
    where={"category": {"$nin": ["accessories", "cables"]}}
)

# Not equal
results = collection.query(
    query_texts=["headphones"],
    n_results=5,
    where={"type": {"$ne": "earbuds"}}
)
```

---

## 🔗 Logical Operators

### AND Operator

All conditions must be true:

```python
# Both conditions must match
results = collection.query(
    query_texts=["wireless audio"],
    n_results=5,
    where={
        "$and": [
            {"wireless": True},
            {"price": {"$lt": 100}}
        ]
    }
)
```

### OR Operator

At least one condition must be true:

```python
# Either condition can match
results = collection.query(
    query_texts=["audio device"],
    n_results=5,
    where={
        "$or": [
            {"type": "headphones"},
            {"type": "earbuds"}
        ]
    }
)
```

### Combining AND and OR

```python
# Complex nested conditions
results = collection.query(
    query_texts=["premium audio"],
    n_results=5,
    where={
        "$and": [
            {"wireless": True},
            {
                "$or": [
                    {"price": {"$lt": 100}},
                    {"rating": {"$gte": 4.5}}
                ]
            }
        ]
    }
)
# Matches: wireless AND (cheap OR highly-rated)
```


---

## 📄 Document Content Filtering

### The `where_document` Parameter

Filter based on the actual document text content:

```python
# Find documents containing specific text
results = collection.query(
    query_texts=["audio"],
    n_results=5,
    where_document={"$contains": "wireless"}
)
```

### Available Document Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$contains` | Document contains text | `{"$contains": "premium"}` |
| `$not_contains` | Document doesn't contain text | `{"$not_contains": "budget"}` |

### Combining Metadata and Document Filters

```python
# Filter by both metadata AND document content
results = collection.query(
    query_texts=["headphones"],
    n_results=5,
    where={"price": {"$lt": 100}},
    where_document={"$contains": "wireless"}
)
# Returns: cheap products with "wireless" in description
```

---

## 📋 The `include` Parameter

Control what data is returned in results:

### Available Include Options

| Option | Description | Default |
|--------|-------------|---------|
| `"documents"` | Original text content | ✅ Included |
| `"metadatas"` | Associated metadata | ✅ Included |
| `"embeddings"` | Vector embeddings | ❌ Not included |
| `"distances"` | Similarity scores | ✅ Included (query only) |

### Usage Examples

```python
# Get only IDs and distances (minimal response)
results = collection.query(
    query_texts=["search term"],
    n_results=5,
    include=[]  # Only returns IDs
)

# Get everything including embeddings
results = collection.query(
    query_texts=["search term"],
    n_results=5,
    include=["documents", "metadatas", "embeddings", "distances"]
)

# For get() operations
docs = collection.get(
    ids=["id1", "id2"],
    include=["documents", "metadatas", "embeddings"]
)
```

---

## 🎯 Practical Examples

### E-commerce Product Search

```python
# User searches for "running shoes" with filters
results = collection.query(
    query_texts=["comfortable running shoes for marathon"],
    n_results=10,
    where={
        "$and": [
            {"category": "footwear"},
            {"subcategory": "running"},
            {"price": {"$lte": 150}},
            {"in_stock": True},
            {"size": {"$in": [9, 9.5, 10]}}
        ]
    }
)
```

### Document Management System

```python
# Search company documents with access control
results = collection.query(
    query_texts=["quarterly financial report"],
    n_results=5,
    where={
        "$and": [
            {"department": {"$in": ["finance", "executive"]}},
            {"classification": {"$ne": "confidential"}},
            {"year": {"$gte": 2023}}
        ]
    }
)
```

### Support Ticket System

```python
# Find similar resolved tickets
results = collection.query(
    query_texts=["login authentication error"],
    n_results=5,
    where={
        "$and": [
            {"status": "resolved"},
            {"category": "authentication"},
            {"resolution_time_hours": {"$lt": 24}}
        ]
    },
    where_document={"$contains": "solution"}
)
```

### Content Recommendation

```python
# Recommend articles based on user preferences
results = collection.query(
    query_texts=["machine learning tutorials"],
    n_results=10,
    where={
        "$and": [
            {"content_type": "article"},
            {"difficulty": {"$in": ["beginner", "intermediate"]}},
            {"language": "english"},
            {
                "$or": [
                    {"topic": "machine learning"},
                    {"topic": "data science"}
                ]
            }
        ]
    }
)
```

---

## ⚠️ Common Mistakes

### 1. Using Unsupported Types

```python
# ❌ Wrong: Lists in metadata
collection.add(
    documents=["doc"],
    ids=["id1"],
    metadatas=[{"tags": ["sale", "new"]}]  # Lists not supported!
)

# ✅ Correct: Use separate fields or comma-separated string
collection.add(
    documents=["doc"],
    ids=["id1"],
    metadatas=[{
        "tag_sale": True,
        "tag_new": True,
        # OR
        "tags_str": "sale,new"
    }]
)
```

### 2. Case Sensitivity

```python
# ❌ Won't match if stored as "Electronics"
where={"category": "electronics"}

# ✅ Ensure consistent casing when storing
# Or normalize before storing
metadata["category"] = category.lower()
```

### 3. Missing Metadata Fields

```python
# ❌ Filter fails silently if field doesn't exist
where={"nonexistent_field": "value"}

# ✅ Ensure all documents have the fields you filter on
# Or use $or to handle missing fields
```

### 4. Incorrect Operator Syntax

```python
# ❌ Wrong: Operator outside dict
where={"price": $gt: 100}

# ✅ Correct: Operator inside nested dict
where={"price": {"$gt": 100}}
```

---

## 💡 Best Practices

### 1. Design Metadata Schema Upfront

```python
# Define a consistent schema
METADATA_SCHEMA = {
    "category": str,      # Required
    "price": float,       # Required
    "in_stock": bool,     # Required
    "rating": float,      # Optional
    "brand": str          # Optional
}
```

### 2. Index Frequently Filtered Fields

```python
# Add metadata that you'll filter on frequently
collection.add(
    documents=[doc],
    ids=[id],
    metadatas=[{
        "category": "electronics",  # Frequently filtered
        "created_date": "2024-01-15",  # For date range queries
        "author_id": "user_123"  # For user-specific queries
    }]
)
```

### 3. Use Appropriate Data Types

```python
# ✅ Use numbers for numeric comparisons
{"price": 99.99}  # Can use $gt, $lt

# ❌ Don't store numbers as strings
{"price": "99.99"}  # String comparison won't work as expected
```

### 4. Combine Semantic Search with Filters

```python
# Let semantic search find relevant content
# Let filters ensure business rules
results = collection.query(
    query_texts=["user's natural language query"],  # Semantic
    n_results=10,
    where={  # Business rules
        "published": True,
        "region": user_region,
        "language": user_language
    }
)
```

---

## 📊 Filter Performance Tips

| Tip | Description |
|-----|-------------|
| **Filter Early** | Apply filters to reduce search space |
| **Avoid Complex Nesting** | Deep nesting can slow queries |
| **Use $in for Multiple Values** | More efficient than multiple $or |
| **Limit Results** | Use appropriate `n_results` |

---

## 📚 Related Topics

- [What is a Vector Database?](./01-what-is-vector-database.md)
- [Similarity Metrics](./02-similarity-metrics.md)
- [Popular Vector Databases](./03-popular-vector-databases.md)
- [ChromaDB Basics](./04-chromadb-basics.md)
- [CRUD Operations](./05-crud-operations.md)

---

_Last Updated: January 2026_
