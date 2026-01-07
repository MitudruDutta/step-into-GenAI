# 📊 Functional Evaluation

## 📌 Overview

**Functional Evaluation** tests whether an AI agent produces accurate, correct, and useful outputs. Unlike traditional software where you can assert exact matches, AI systems require semantic evaluation — checking if the meaning is correct even if the exact words differ.

This document covers text-based evaluation metrics, LLM-as-judge approaches, task-based testing, and human evaluation strategies.

---

## 🎯 What is Functional Evaluation?

Functional evaluation answers the question: **"Does the agent give the right answer?"**

| Aspect | Traditional Testing | AI Functional Evaluation |
|--------|--------------------|-----------------------|
| **Comparison** | `assert output == expected` | Semantic similarity scoring |
| **Tolerance** | Exact match required | Meaning match acceptable |
| **Metrics** | Pass/Fail | Similarity scores (0-1) |
| **Judgment** | Deterministic | Probabilistic |

---

## 📏 Text-Based Evaluation Metrics

### 1. Cosine Similarity

Measures the angle between two text embeddings in vector space.

```
┌─────────────────────────────────────────────────────────────────┐
│                    COSINE SIMILARITY                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Expected: "The iPhone 15 is in stock"                          │
│  Actual:   "iPhone 15 is available in inventory"                │
│                                                                  │
│  Step 1: Convert to embeddings                                  │
│  Expected → [0.23, -0.45, 0.67, ...]                            │
│  Actual   → [0.21, -0.43, 0.65, ...]                            │
│                                                                  │
│  Step 2: Calculate cosine similarity                            │
│  Similarity = (A · B) / (||A|| × ||B||)                         │
│                                                                  │
│  Result: 0.94 (94% similar) ✓                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**When to use:** General text similarity, semantic matching

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

expected = "The iPhone 15 is in stock"
actual = "iPhone 15 is available in inventory"

embeddings = model.encode([expected, actual])
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print(f"Similarity: {similarity:.2f}")  # ~0.94
```

### 2. BLEU Score

Measures n-gram overlap between expected and actual outputs. Originally designed for machine translation.

| N-gram | Example |
|--------|---------|
| 1-gram (unigram) | "the", "cat", "sat" |
| 2-gram (bigram) | "the cat", "cat sat" |
| 3-gram (trigram) | "the cat sat" |
| 4-gram | "the cat sat on" |

**When to use:** Translation tasks, structured outputs

```python
from nltk.translate.bleu_score import sentence_bleu

reference = ["the", "cat", "sat", "on", "the", "mat"]
candidate = ["the", "cat", "is", "on", "the", "mat"]

score = sentence_bleu([reference], candidate)
print(f"BLEU Score: {score:.2f}")
```

### 3. ROUGE Score

Measures recall-oriented overlap. Variants include ROUGE-1, ROUGE-2, and ROUGE-L.

| Variant | Measures |
|---------|----------|
| **ROUGE-1** | Unigram overlap |
| **ROUGE-2** | Bigram overlap |
| **ROUGE-L** | Longest common subsequence |

**When to use:** Summarization tasks, long-form content

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
scores = scorer.score(
    "The quick brown fox jumps over the lazy dog",
    "A fast brown fox leaps over a sleepy dog"
)
print(scores)
```

### Metric Comparison

| Metric | Best For | Pros | Cons |
|--------|----------|------|------|
| **Cosine Similarity** | Semantic matching | Captures meaning | Requires embeddings |
| **BLEU** | Translation, structured | Fast, interpretable | Ignores semantics |
| **ROUGE** | Summarization | Recall-focused | Word-level only |

---

## 🤖 LLM-as-Judge Evaluation

Use a powerful LLM to evaluate another LLM's output.

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM-AS-JUDGE PATTERN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │    Agent     │──── Response ────┐                            │
│  │  (Qwen 32B)  │                  │                            │
│  └──────────────┘                  │                            │
│                                    ▼                            │
│                           ┌──────────────┐                      │
│                           │    JUDGE     │                      │
│                           │  (GPT-4 or   │                      │
│                           │   Claude)    │                      │
│                           └──────┬───────┘                      │
│                                  │                               │
│                                  ▼                               │
│                           Score: 8/10                           │
│                           Reasoning: "Accurate but verbose"     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
def llm_judge(question, expected, actual, judge_model):
    prompt = f"""
    Evaluate the following response on a scale of 1-10.
    
    Question: {question}
    Expected Answer: {expected}
    Actual Answer: {actual}
    
    Score the response based on:
    1. Accuracy (does it match the expected answer?)
    2. Completeness (does it cover all key points?)
    3. Clarity (is it easy to understand?)
    
    Return only a JSON object:
    {{"score": <1-10>, "reasoning": "<explanation>"}}
    """
    return judge_model.generate(prompt)
```

**Pros:**
- Captures nuance and context
- Handles paraphrasing well
- Can evaluate complex reasoning

**Cons:**
- Expensive (requires LLM calls)
- Judge can have biases
- Non-deterministic

---

## ✅ Task-Based Evaluation with Agno

Agno provides built-in evaluation tools for testing agents.

### AccuracyEval Example

```python
from agno.eval.accuracy import AccuracyEval

from inventory_agent import inventory_agent

def test_inventory_agent():
    test_cases = [
        {
            "question": "What is the stock status of iPhone 15?",
            "expected_answer": "The iPhone 15 is In Stock with 2 available items.",
            "min_score": 8
        },
        {
            "question": "Is AirPods Pro available?",
            "expected_answer": "The AirPods Pro are currently Out of Stock",
            "min_score": 8
        },
        {
            "question": "How many MacBook Air M3 units are in stock?",
            "expected_answer": "5",
            "min_score": 8
        },
        {
            "question": "Do you have Samsung Galaxy S23?",
            "expected_answer": "The product is not available in our inventory.",
            "min_score": 8
        },
        {
            "question": "Can you tell me the recipe of Vada pav?",
            "expected_answer": "Sorry, I can't assist with that.",
            "min_score": 8
        }   
    ]

    for test in test_cases:
        evaluation = AccuracyEval(
            agent=inventory_agent,
            input=test["question"],
            expected_output=test["expected_answer"],
            num_iterations=3  # Run multiple times for consistency
        )
        print(f"\nEvaluating: {test['question']}")
        evaluation.run(print_results=True)
```

### Test Case Design

| Test Type | Purpose | Example |
|-----------|---------|---------|
| **Happy Path** | Normal expected behavior | "What's iPhone 15 stock?" |
| **Edge Case** | Boundary conditions | "Product not in inventory" |
| **Out of Scope** | Rejection of irrelevant queries | "Recipe for Vada pav?" |
| **Adversarial** | Attempts to break the agent | Jailbreak attempts |

---

## 👥 Human Evaluation

Automated metrics don't catch everything. Human evaluation remains essential.

### When to Use Human Evaluation

| Scenario | Why Human Evaluation? |
|----------|----------------------|
| **Subjective quality** | "Is this response helpful?" |
| **Tone and style** | "Is this professional enough?" |
| **Complex reasoning** | "Is the logic sound?" |
| **Edge cases** | Unusual inputs that metrics miss |

### Human Evaluation Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                 HUMAN EVALUATION RUBRIC                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ACCURACY (1-5)                                                 │
│  1 = Completely wrong                                           │
│  3 = Partially correct                                          │
│  5 = Fully accurate                                             │
│                                                                  │
│  HELPFULNESS (1-5)                                              │
│  1 = Not helpful at all                                         │
│  3 = Somewhat helpful                                           │
│  5 = Very helpful                                               │
│                                                                  │
│  SAFETY (1-5)                                                   │
│  1 = Harmful/dangerous                                          │
│  3 = Neutral                                                    │
│  5 = Safe and appropriate                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Combining Automated and Human Evaluation

```
┌─────────────────────────────────────────────────────────────────┐
│              EVALUATION PIPELINE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Stage 1: AUTOMATED (High Volume)                               │
│  ├── Cosine similarity                                          │
│  ├── BLEU/ROUGE scores                                          │
│  └── Task completion rate                                       │
│           │                                                      │
│           ▼ Flag low scores                                     │
│                                                                  │
│  Stage 2: LLM-AS-JUDGE (Medium Volume)                          │
│  ├── Semantic evaluation                                        │
│  ├── Reasoning quality                                          │
│  └── Coherence check                                            │
│           │                                                      │
│           ▼ Flag edge cases                                     │
│                                                                  │
│  Stage 3: HUMAN REVIEW (Low Volume)                             │
│  ├── Subjective quality                                         │
│  ├── Safety concerns                                            │
│  └── Final approval                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Evaluation Frameworks

### Agno (Built-in)

```python
from agno.eval.accuracy import AccuracyEval
from agno.eval.performance import PerformanceEval

# Accuracy evaluation
AccuracyEval(agent=my_agent, input="...", expected_output="...")

# Performance evaluation
PerformanceEval(func=agent_call, num_iterations=10)
```

### LangSmith

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

results = evaluate(
    lambda inputs: my_agent.run(inputs["question"]),
    data="my-dataset",
    evaluators=["qa", "cot_qa"],
)
```

### Custom Evaluation

```python
def evaluate_agent(agent, test_cases):
    results = []
    for test in test_cases:
        response = agent.run(test["input"])
        score = calculate_similarity(response, test["expected"])
        results.append({
            "input": test["input"],
            "expected": test["expected"],
            "actual": response,
            "score": score,
            "passed": score >= test["min_score"]
        })
    return results
```

---

## 🎯 Key Takeaways

1. **Semantic evaluation** — Use cosine similarity for meaning-based comparison
2. **Multiple metrics** — Combine BLEU, ROUGE, and cosine for comprehensive evaluation
3. **LLM-as-judge** — Powerful but expensive; use for complex evaluations
4. **Test case variety** — Include happy path, edge cases, and adversarial tests
5. **Human evaluation** — Essential for subjective quality and safety
6. **Iterative testing** — Run multiple iterations to account for variability

---

## 📖 Next Steps

→ [02-safety-evaluation.md](02-safety-evaluation.md) — Learn about security testing and guardrails
