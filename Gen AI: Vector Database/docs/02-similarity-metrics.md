# 📐 Similarity Metrics

## 📌 Overview

When comparing vectors in a vector database, the choice of **distance/similarity metric** significantly impacts search accuracy and relevance. This guide covers the most common metrics, their mathematical foundations, and when to use each.

---

## 🎯 Why Metrics Matter

Different metrics measure "closeness" in different ways:

```
Vector A: [1, 0]
Vector B: [2, 0]
Vector C: [0, 1]

Euclidean: A is closer to B (same direction, different magnitude)
Cosine:    A is identical to B (same direction), C is completely different
```

Choosing the wrong metric can lead to poor search results!

---

## 📏 Euclidean Distance (L2)

### Definition

Euclidean distance measures the **straight-line distance** between two points in vector space — like measuring with a ruler.

### Formula

```
Distance = √[(x₁-y₁)² + (x₂-y₂)² + ... + (xₙ-yₙ)²]
```

### Visual Representation

```
        y
        │
    B ● │ (3, 4)
        │   ╲
        │     ╲  distance = 5
        │       ╲
    A ● │─────────● (3, 0)
        │ (0, 0)
        └──────────── x
        
Distance = √[(3-0)² + (4-0)²] = √[9 + 16] = √25 = 5
```

### Characteristics

| Property | Description |
|----------|-------------|
| **Range** | 0 to ∞ (0 = identical) |
| **Magnitude Sensitive** | Yes — longer vectors are "farther" |
| **Scale Dependent** | Yes — affected by feature scaling |
| **Interpretation** | Physical distance in space |

### Python Implementation

```python
import numpy as np

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Example
vec_a = np.array([1, 2, 3])
vec_b = np.array([4, 5, 6])

distance = euclidean_distance(vec_a, vec_b)
print(f"Euclidean Distance: {distance}")  # 5.196
```

### When to Use Euclidean Distance

| ✅ Good For | ❌ Not Ideal For |
|------------|-----------------|
| Image embeddings | Text embeddings |
| Dense, normalized vectors | Sparse vectors |
| When magnitude matters | When only direction matters |
| Spatial/geographic data | High-dimensional sparse data |
| Clustering algorithms | Document similarity |

---

## 🧭 Cosine Similarity & Distance

### Definition

Cosine similarity measures the **angle** between two vectors, ignoring their magnitude. It focuses purely on **direction/orientation**.

### Formula

```
Similarity = (A · B) / (||A|| × ||B||)

Where:
- A · B = dot product of vectors
- ||A|| = magnitude (length) of vector A
- ||B|| = magnitude (length) of vector B

Distance = 1 - Similarity
```

### Visual Representation

```
        y
        │     B (1, 2)
        │    ╱
        │   ╱  θ = angle between vectors
        │  ╱
        │ ╱ θ
        │╱______ A (2, 1)
        └──────────── x

Cosine Similarity = cos(θ)
- θ = 0°  → similarity = 1 (identical direction)
- θ = 90° → similarity = 0 (perpendicular)
- θ = 180° → similarity = -1 (opposite direction)
```

### Characteristics

| Property | Description |
|----------|-------------|
| **Similarity Range** | -1 to 1 (1 = identical direction) |
| **Distance Range** | 0 to 2 (0 = identical direction) |
| **Magnitude Sensitive** | No — scale invariant |
| **Interpretation** | Directional similarity |

### Python Implementation

```python
import numpy as np

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    return dot_product / (magnitude_a * magnitude_b)

def cosine_distance(a, b):
    return 1 - cosine_similarity(a, b)

# Example
vec_a = np.array([1, 2, 3])
vec_b = np.array([2, 4, 6])  # Same direction, different magnitude

similarity = cosine_similarity(vec_a, vec_b)
print(f"Cosine Similarity: {similarity}")  # 1.0 (identical direction!)

distance = cosine_distance(vec_a, vec_b)
print(f"Cosine Distance: {distance}")  # 0.0
```

### When to Use Cosine Similarity

| ✅ Good For | ❌ Not Ideal For |
|------------|-----------------|
| Text embeddings | When magnitude matters |
| Document similarity | Spatial data |
| NLP applications | Image pixel comparisons |
| High-dimensional data | Low-dimensional data |
| Sparse vectors | Dense normalized vectors |


---

## 🔢 Dot Product (Inner Product)

### Definition

The dot product measures similarity by multiplying corresponding elements and summing them. Unlike cosine similarity, it **is affected by magnitude**.

### Formula

```
Dot Product = A · B = (a₁×b₁) + (a₂×b₂) + ... + (aₙ×bₙ)
```

### Characteristics

| Property | Description |
|----------|-------------|
| **Range** | -∞ to +∞ |
| **Magnitude Sensitive** | Yes |
| **Interpretation** | Combined direction and magnitude similarity |

### Python Implementation

```python
import numpy as np

def dot_product(a, b):
    return np.dot(a, b)

vec_a = np.array([1, 2, 3])
vec_b = np.array([4, 5, 6])

result = dot_product(vec_a, vec_b)
print(f"Dot Product: {result}")  # 32
```

### When to Use Dot Product

| ✅ Good For | ❌ Not Ideal For |
|------------|-----------------|
| Normalized embeddings | Non-normalized vectors |
| When vectors are pre-normalized | When scale varies |
| Maximum inner product search | General similarity |

---

## 📊 Metric Comparison

### Side-by-Side Comparison

| Metric | Magnitude Sensitive | Range | Best For |
|--------|-------------------|-------|----------|
| **Euclidean** | ✅ Yes | 0 to ∞ | Images, spatial data |
| **Cosine** | ❌ No | -1 to 1 | Text, documents |
| **Dot Product** | ✅ Yes | -∞ to +∞ | Normalized vectors |

### Practical Example

```python
import numpy as np

# Two text embeddings (simplified)
doc1 = np.array([0.8, 0.2, 0.1])  # About "cats"
doc2 = np.array([1.6, 0.4, 0.2])  # Also about "cats" (same direction, 2x magnitude)
doc3 = np.array([0.1, 0.9, 0.3])  # About "dogs" (different direction)

# Euclidean Distance
print("Euclidean Distances:")
print(f"  doc1 vs doc2: {np.linalg.norm(doc1 - doc2):.3f}")  # 0.917 (seems far!)
print(f"  doc1 vs doc3: {np.linalg.norm(doc1 - doc3):.3f}")  # 0.922 (similar distance)

# Cosine Similarity
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\nCosine Similarities:")
print(f"  doc1 vs doc2: {cosine_sim(doc1, doc2):.3f}")  # 1.000 (identical!)
print(f"  doc1 vs doc3: {cosine_sim(doc1, doc3):.3f}")  # 0.507 (different)
```

**Key Insight**: For text, cosine correctly identifies doc1 and doc2 as identical in meaning, while Euclidean is misled by the magnitude difference.

---

## 🛠️ Using Metrics in ChromaDB

### Setting Distance Metric

```python
import chromadb

client = chromadb.Client()

# Cosine distance (default for text)
collection_cosine = client.create_collection(
    name="text_collection",
    metadata={"hnsw:space": "cosine"}
)

# Euclidean distance (L2)
collection_euclidean = client.create_collection(
    name="image_collection",
    metadata={"hnsw:space": "l2"}
)

# Inner product (dot product)
collection_ip = client.create_collection(
    name="normalized_collection",
    metadata={"hnsw:space": "ip"}
)
```

### Available Metrics in ChromaDB

| Metric Name | ChromaDB Setting | Description |
|-------------|------------------|-------------|
| Cosine | `"cosine"` | Default, best for text |
| Euclidean (L2) | `"l2"` | Straight-line distance |
| Inner Product | `"ip"` | Dot product |

---

## 💡 Choosing the Right Metric

### Decision Flowchart

```
Start
  │
  ▼
Is your data text/documents?
  │
  ├─ YES → Use Cosine
  │
  └─ NO
      │
      ▼
    Are vectors normalized?
      │
      ├─ YES → Dot Product or Cosine
      │
      └─ NO
          │
          ▼
        Does magnitude matter?
          │
          ├─ YES → Euclidean
          │
          └─ NO → Cosine
```

### Quick Reference

| Data Type | Recommended Metric |
|-----------|-------------------|
| Text embeddings | Cosine |
| Document search | Cosine |
| Image embeddings | Euclidean or Cosine |
| Audio embeddings | Cosine |
| Normalized vectors | Dot Product |
| Geographic/spatial | Euclidean |
| Recommendation systems | Cosine |

---

## ⚠️ Common Pitfalls

### 1. Using Euclidean for Text
```python
# ❌ Wrong: Euclidean for text embeddings
# Magnitude differences can dominate semantic differences
```

### 2. Forgetting to Normalize for Dot Product
```python
# ❌ Wrong: Using dot product without normalization
# Results will be skewed by vector lengths

# ✅ Correct: Normalize first
normalized_vec = vec / np.linalg.norm(vec)
```

### 3. Mixing Metrics
```python
# ❌ Wrong: Storing with one metric, querying with another
# Always use consistent metrics throughout your pipeline
```

---

## 📚 Related Topics

- [What is a Vector Database?](./01-what-is-vector-database.md)
- [Popular Vector Databases](./03-popular-vector-databases.md)
- [ChromaDB Basics](./04-chromadb-basics.md)
- [CRUD Operations](./05-crud-operations.md)
- [Metadata Filtering](./06-metadata-filtering.md)

---

_Last Updated: January 2026_
