# ✏️ CRUD Operations in ChromaDB

## 📌 Overview

CRUD stands for **Create, Read, Update, Delete** — the four basic operations for managing data. This guide covers how to perform each operation in ChromaDB with detailed examples.

---

## 📊 CRUD Operations Summary

| Operation | Method | Description |
|-----------|--------|-------------|
| **Create** | `add()` | Add new documents |
| **Read** | `get()`, `query()` | Retrieve documents |
| **Update** | `update()`, `upsert()` | Modify existing documents |
| **Delete** | `delete()` | Remove documents |

---

## ➕ CREATE: Adding Documents

### Basic Add

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("products")

# Add single document
collection.add(
    documents=["Wireless Bluetooth headphones with noise cancellation"],
    ids=["product_001"]
)

# Add multiple documents
collection.add(
    documents=[
        "Ergonomic mechanical keyboard",
        "Ultra-wide curved monitor",
        "Wireless gaming mouse"
    ],
    ids=["product_002", "product_003", "product_004"]
)
```

### Add with Metadata

```python
collection.add(
    documents=[
        "Premium leather wallet",
        "Stainless steel water bottle",
        "Organic cotton t-shirt"
    ],
    ids=["prod_101", "prod_102", "prod_103"],
    metadatas=[
        {
            "category": "accessories",
            "price": 49.99,
            "in_stock": True,
            "brand": "LuxuryGoods"
        },
        {
            "category": "drinkware",
            "price": 24.99,
            "in_stock": True,
            "brand": "EcoLife"
        },
        {
            "category": "clothing",
            "price": 29.99,
            "in_stock": False,
            "brand": "GreenWear"
        }
    ]
)
```

### Add with Pre-computed Embeddings

```python
from sentence_transformers import SentenceTransformer

# Generate embeddings externally
model = SentenceTransformer('all-MiniLM-L6-v2')
documents = ["Document one", "Document two"]
embeddings = model.encode(documents).tolist()

# Add with embeddings
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=["doc_1", "doc_2"]
)
```

### Add Rules and Constraints

| Rule | Description | Example |
|------|-------------|---------|
| **Unique IDs** | Each ID must be unique | `ids=["unique_1", "unique_2"]` |
| **String IDs** | IDs must be strings | `ids=["123"]` not `ids=[123]` |
| **Matching Lengths** | All lists must be same length | 3 docs = 3 ids = 3 metadatas |
| **No Empty Strings** | Documents can't be empty | `documents=["text"]` not `[""]` |

---

## 📖 READ: Retrieving Documents

### Get by ID

```python
# Get specific documents by ID
results = collection.get(
    ids=["product_001", "product_002"]
)

print(results)
# {
#     'ids': ['product_001', 'product_002'],
#     'documents': ['Wireless Bluetooth headphones...', 'Ergonomic mechanical keyboard'],
#     'metadatas': [{...}, {...}],
#     'embeddings': None  # Not included by default
# }
```

### Get All Documents

```python
# Get all documents in collection
all_docs = collection.get()

# Get with specific fields
all_docs = collection.get(
    include=["documents", "metadatas", "embeddings"]
)
```

### Get with Filters

```python
# Get documents matching metadata criteria
results = collection.get(
    where={"category": "electronics"},
    include=["documents", "metadatas"]
)

# Get with multiple conditions
results = collection.get(
    where={
        "$and": [
            {"category": "electronics"},
            {"price": {"$lt": 100}}
        ]
    }
)
```

### Query (Similarity Search)

```python
# Find similar documents
results = collection.query(
    query_texts=["wireless audio device"],
    n_results=3
)

# Query with filters
results = collection.query(
    query_texts=["wireless audio device"],
    n_results=3,
    where={"in_stock": True}
)
```

### Include Parameter Options

```python
# Control what's returned
results = collection.get(
    ids=["product_001"],
    include=[
        "documents",    # Original text
        "metadatas",    # Associated metadata
        "embeddings"    # Vector embeddings
    ]
)

# For queries, also available:
results = collection.query(
    query_texts=["search"],
    n_results=5,
    include=[
        "documents",
        "metadatas",
        "embeddings",
        "distances"     # Similarity scores
    ]
)
```

---

## 🔄 UPDATE: Modifying Documents

### Update Existing Documents

The `update()` method modifies existing documents. **Only provided fields are updated.**

```python
# Update document text
collection.update(
    ids=["product_001"],
    documents=["Updated: Premium wireless headphones with ANC"]
)

# Update metadata only
collection.update(
    ids=["product_001"],
    metadatas=[{"price": 79.99, "on_sale": True}]
)

# Update both document and metadata
collection.update(
    ids=["product_001"],
    documents=["New description here"],
    metadatas=[{"price": 69.99}]
)
```

### Update Multiple Documents

```python
collection.update(
    ids=["prod_101", "prod_102", "prod_103"],
    metadatas=[
        {"price": 44.99},  # Updated price
        {"price": 22.99},
        {"in_stock": True}  # Now in stock
    ]
)
```

### Upsert: Update or Insert

`upsert()` updates if the ID exists, or inserts if it doesn't.

```python
# This will update if exists, insert if not
collection.upsert(
    documents=[
        "Existing product - updated",
        "Brand new product"
    ],
    ids=["product_001", "product_999"],  # 001 exists, 999 is new
    metadatas=[
        {"updated": True},
        {"new": True}
    ]
)
```

### Update vs Upsert

| Method | ID Exists | ID Doesn't Exist |
|--------|-----------|------------------|
| `update()` | Updates document | **Error** |
| `upsert()` | Updates document | Inserts new document |

```python
# ❌ update() fails if ID doesn't exist
collection.update(ids=["nonexistent"], documents=["text"])
# Error!

# ✅ upsert() handles both cases
collection.upsert(ids=["nonexistent"], documents=["text"])
# Creates new document
```


---

## 🗑️ DELETE: Removing Documents

### Delete by ID

```python
# Delete single document
collection.delete(ids=["product_001"])

# Delete multiple documents
collection.delete(ids=["product_002", "product_003", "product_004"])
```

### Delete by Filter

```python
# Delete all documents matching criteria
collection.delete(
    where={"category": "discontinued"}
)

# Delete with multiple conditions
collection.delete(
    where={
        "$and": [
            {"in_stock": False},
            {"price": {"$lt": 10}}
        ]
    }
)
```

### Delete by Document Content

```python
# Delete documents containing specific text
collection.delete(
    where_document={"$contains": "deprecated"}
)
```

### Delete Entire Collection

```python
# Delete the entire collection
client.delete_collection(name="products")

# Verify deletion
collections = client.list_collections()
print(collections)  # "products" no longer listed
```

### Delete Cautions

| ⚠️ Warning | Description |
|-----------|-------------|
| **Irreversible** | Deleted data cannot be recovered |
| **No Confirmation** | Deletion happens immediately |
| **Cascade** | Deleting collection removes all documents |

---

## 🔄 Complete CRUD Example

```python
import chromadb

# Setup
client = chromadb.PersistentClient(path="./crud_example")
collection = client.get_or_create_collection("inventory")

# ============ CREATE ============
print("=== CREATE ===")
collection.add(
    documents=[
        "Red running shoes, size 10",
        "Blue denim jeans, size 32",
        "Black leather jacket, size M"
    ],
    ids=["item_001", "item_002", "item_003"],
    metadatas=[
        {"category": "footwear", "price": 89.99, "color": "red"},
        {"category": "pants", "price": 59.99, "color": "blue"},
        {"category": "outerwear", "price": 199.99, "color": "black"}
    ]
)
print(f"Created {collection.count()} items")

# ============ READ ============
print("\n=== READ ===")

# Get by ID
item = collection.get(ids=["item_001"])
print(f"Item 001: {item['documents'][0]}")

# Query by similarity
results = collection.query(
    query_texts=["athletic footwear"],
    n_results=1
)
print(f"Similar to 'athletic footwear': {results['documents'][0]}")

# Get with filter
expensive = collection.get(
    where={"price": {"$gt": 100}}
)
print(f"Expensive items: {expensive['documents']}")

# ============ UPDATE ============
print("\n=== UPDATE ===")

# Update price
collection.update(
    ids=["item_001"],
    metadatas=[{"price": 79.99, "on_sale": True}]
)

# Verify update
updated = collection.get(ids=["item_001"])
print(f"Updated metadata: {updated['metadatas'][0]}")

# Upsert new item
collection.upsert(
    documents=["White cotton t-shirt, size L"],
    ids=["item_004"],
    metadatas=[{"category": "tops", "price": 24.99, "color": "white"}]
)
print(f"After upsert: {collection.count()} items")

# ============ DELETE ============
print("\n=== DELETE ===")

# Delete by ID
collection.delete(ids=["item_002"])
print(f"After delete: {collection.count()} items")

# Delete by filter
collection.delete(where={"price": {"$lt": 30}})
print(f"After filter delete: {collection.count()} items")

# Final state
print("\n=== FINAL STATE ===")
all_items = collection.get()
for i, doc in enumerate(all_items['documents']):
    print(f"- {all_items['ids'][i]}: {doc}")
```

---

## 📋 Method Reference

### add()

```python
collection.add(
    ids: List[str],                    # Required: Unique identifiers
    documents: List[str] = None,       # Optional: Text content
    embeddings: List[List[float]] = None,  # Optional: Pre-computed vectors
    metadatas: List[Dict] = None       # Optional: Associated metadata
)
```

### get()

```python
collection.get(
    ids: List[str] = None,             # Optional: Specific IDs to retrieve
    where: Dict = None,                # Optional: Metadata filter
    where_document: Dict = None,       # Optional: Document content filter
    include: List[str] = ["documents", "metadatas"]  # What to return
)
```

### query()

```python
collection.query(
    query_texts: List[str] = None,     # Text queries (auto-embedded)
    query_embeddings: List[List[float]] = None,  # Pre-computed query vectors
    n_results: int = 10,               # Number of results per query
    where: Dict = None,                # Metadata filter
    where_document: Dict = None,       # Document content filter
    include: List[str] = ["documents", "metadatas", "distances"]
)
```

### update()

```python
collection.update(
    ids: List[str],                    # Required: IDs to update
    documents: List[str] = None,       # Optional: New text content
    embeddings: List[List[float]] = None,  # Optional: New vectors
    metadatas: List[Dict] = None       # Optional: New metadata
)
```

### upsert()

```python
collection.upsert(
    ids: List[str],                    # Required: IDs to upsert
    documents: List[str] = None,       # Optional: Text content
    embeddings: List[List[float]] = None,  # Optional: Vectors
    metadatas: List[Dict] = None       # Optional: Metadata
)
```

### delete()

```python
collection.delete(
    ids: List[str] = None,             # Optional: Specific IDs to delete
    where: Dict = None,                # Optional: Delete by metadata filter
    where_document: Dict = None        # Optional: Delete by content filter
)
```

---

## 💡 Best Practices

### 1. Use Upsert for Idempotent Operations

```python
# ✅ Safe to run multiple times
collection.upsert(
    documents=["Latest version of document"],
    ids=["doc_123"]
)
```

### 2. Batch Operations for Performance

```python
# ✅ Add many documents at once
collection.add(
    documents=large_document_list,  # 1000 documents
    ids=large_id_list
)

# ❌ Avoid adding one at a time in a loop
for doc, id in zip(documents, ids):
    collection.add(documents=[doc], ids=[id])  # Slow!
```

### 3. Verify Before Delete

```python
# Check what will be deleted
to_delete = collection.get(where={"status": "archived"})
print(f"Will delete {len(to_delete['ids'])} documents")

# Then delete
collection.delete(where={"status": "archived"})
```

### 4. Use Transactions for Related Operations

```python
# Group related operations
try:
    collection.delete(ids=["old_version"])
    collection.add(
        documents=["New version"],
        ids=["new_version"]
    )
except Exception as e:
    print(f"Operation failed: {e}")
```

---

## 📚 Related Topics

- [What is a Vector Database?](./01-what-is-vector-database.md)
- [Similarity Metrics](./02-similarity-metrics.md)
- [Popular Vector Databases](./03-popular-vector-databases.md)
- [ChromaDB Basics](./04-chromadb-basics.md)
- [Metadata Filtering](./06-metadata-filtering.md)

---

_Last Updated: January 2026_
