# ⚙️ Model Parameters & Sampling Strategies

## 📌 Overview

When working with Large Language Models, understanding how to control their output is crucial. The model's behavior can be fine-tuned through various parameters that balance creativity and determinism. Mastering these settings allows you to get more relevant, accurate, and appropriate responses for your specific use case.

---

## 🎛️ Key Parameters Explained

### 1. Context Window

The **context window** determines how many tokens (roughly 0.75 words per token) the model can "see" and process at once. Think of it as the model's working memory.

#### What is a Context Window?

```
┌─────────────────────────────────────────────────────────┐
│                    Context Window                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │ [System Prompt] [Conversation History] [New Query] │  │
│  │      1000 tokens   +   2000 tokens   +   500 tokens│  │
│  └───────────────────────────────────────────────────┘  │
│              Total: 3500 tokens used                     │
└─────────────────────────────────────────────────────────┘
```

#### Context Window Sizes by Model

| Model          | Context Window        | Approximate Word Count |
| -------------- | --------------------- | ---------------------- |
| GPT-3.5        | 4,096 tokens          | ~3,000 words           |
| GPT-4          | 8,192 / 32,768 tokens | ~6,000 / ~24,000 words |
| GPT-4 Turbo    | 128,000 tokens        | ~96,000 words          |
| Claude 3       | 200,000 tokens        | ~150,000 words         |
| Gemini 1.5 Pro | 1,000,000 tokens      | ~750,000 words         |

#### Impact on Model Behavior

| Aspect        | Short Context                    | Long Context                            |
| ------------- | -------------------------------- | --------------------------------------- |
| **Memory**    | Forgets earlier conversation     | Maintains coherence over long documents |
| **Coherence** | May lose track of complex topics | Better at multi-turn reasoning          |
| **Cost**      | Lower per request                | Higher per request                      |
| **Speed**     | Faster inference                 | Slower inference                        |

#### Best Practices

- **Prioritize recent context**: Place the most relevant information closer to the query
- **Summarize when needed**: For long conversations, periodically summarize earlier content
- **Use system prompts wisely**: They consume context but provide consistent behavior

---

### 2. Temperature

**Temperature** controls the randomness (creativity) of the model's output. It affects how the model samples from its probability distribution.

#### How Temperature Works

```
Low Temperature (0.1-0.3):
  Token A: 70% → Selected (most likely)
  Token B: 20%
  Token C: 10%

High Temperature (0.8-1.0):
  Token A: 45% → Still likely, but others have better chances
  Token B: 35% → Could be selected
  Token C: 20% → Might be selected
```

#### Temperature Spectrum

```
0.0 ←──────────────────────────────────→ 2.0
│                                         │
│  DETERMINISTIC                CREATIVE  │
│  - Factual tasks              - Stories │
│  - Code generation            - Poetry  │
│  - Data extraction            - Brainstorming │
│  - Consistent outputs         - Varied outputs │
```

#### Recommended Settings by Use Case

| Use Case              | Temperature | Reasoning                         |
| --------------------- | ----------- | --------------------------------- |
| **Code Generation**   | 0.0 - 0.2   | Needs precision and correctness   |
| **Technical Writing** | 0.2 - 0.4   | Factual but slightly varied       |
| **General Chat**      | 0.5 - 0.7   | Balanced creativity and coherence |
| **Creative Writing**  | 0.7 - 0.9   | More varied and interesting       |
| **Brainstorming**     | 0.9 - 1.2   | Maximum creativity, diverse ideas |

#### Visual Example

```python
# Temperature = 0.2 (Deterministic)
Prompt: "The capital of France is"
Output: "Paris" (every time)

# Temperature = 1.0 (Creative)
Prompt: "Write a greeting"
Outputs: "Hello!", "Hey there!", "Greetings!", "Hi friend!" (varies)
```

---

### 3. Top-k Sampling

**Top-k sampling** limits token selection to only the **k most probable tokens**, reducing randomness while maintaining some diversity.

#### How Top-k Works

```
Full Vocabulary (50,000 tokens):
┌────────────────────────────────────────┐
│ cat: 25% │ dog: 15% │ bird: 10% │ ... │
└────────────────────────────────────────┘

Top-k = 3:
┌─────────────────────────────────┐
│ cat: 25% │ dog: 15% │ bird: 10% │  ← Only these 3 considered
└─────────────────────────────────┘
  Remaining 49,997 tokens excluded
```

#### Top-k Value Guide

| k Value     | Behavior                                 | Use Case            |
| ----------- | ---------------------------------------- | ------------------- |
| **k = 1**   | Greedy decoding (always picks top token) | Maximum consistency |
| **k = 10**  | Very focused                             | Technical content   |
| **k = 40**  | Balanced (common default)                | General use         |
| **k = 100** | More diverse                             | Creative tasks      |
| **k = ∞**   | No filtering                             | Full randomness     |

#### Advantages and Limitations

| Pros                             | Cons                                          |
| -------------------------------- | --------------------------------------------- |
| ✅ Prevents very unlikely tokens | ❌ Fixed k may exclude good options           |
| ✅ Maintains some diversity      | ❌ Doesn't adapt to probability distributions |
| ✅ Simple to understand          | ❌ May cut off at arbitrary points            |

---

### 4. Top-p (Nucleus) Sampling

**Top-p sampling** (also called nucleus sampling) selects from the smallest set of tokens whose cumulative probability exceeds the threshold **p**.

#### How Top-p Works

```
Token Probabilities:
  cat:   35%  │ Cumulative: 35%  ✓ (< 0.9)
  dog:   25%  │ Cumulative: 60%  ✓ (< 0.9)
  bird:  15%  │ Cumulative: 75%  ✓ (< 0.9)
  fish:  10%  │ Cumulative: 85%  ✓ (< 0.9)
  rat:    5%  │ Cumulative: 90%  ✓ (= 0.9)
  ─────────────────────────────────
  ant:    3%  │ Cumulative: 93%  ✗ (> 0.9) EXCLUDED
  ...remaining tokens excluded...

With top-p = 0.9, only {cat, dog, bird, fish, rat} are considered
```

#### Top-p Value Guide

| p Value      | Behavior                  | Use Case              |
| ------------ | ------------------------- | --------------------- |
| **p = 0.1**  | Very restrictive          | Highly focused output |
| **p = 0.5**  | Moderately restrictive    | Technical tasks       |
| **p = 0.9**  | Standard (common default) | General use           |
| **p = 0.95** | Slightly more diverse     | Creative tasks        |
| **p = 1.0**  | No filtering              | Full vocabulary       |

#### Top-p vs Top-k Comparison

| Feature                        | Top-k                          | Top-p                                 |
| ------------------------------ | ------------------------------ | ------------------------------------- |
| **Adaptability**               | Fixed number of tokens         | Adapts to probability distribution    |
| **When distribution is sharp** | May include unlikely tokens    | Naturally restricts to few tokens     |
| **When distribution is flat**  | May exclude reasonable options | Includes more tokens                  |
| **Recommended for**            | Consistent filtering           | Dynamic, distribution-aware filtering |

---

## 🔧 Combining Parameters

In practice, these parameters are often used together. Here are some effective combinations:

### Configuration Presets

```python
# Precise/Factual (Documentation, Code)
config_precise = {
    "temperature": 0.1,
    "top_p": 0.9,
    "top_k": 40
}

# Balanced (General Chat, Q&A)
config_balanced = {
    "temperature": 0.5,
    "top_p": 0.9,
    "top_k": 50
}

# Creative (Stories, Brainstorming)
config_creative = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 100
}
```

### Parameter Interaction Matrix

| Temperature | Top-p       | Top-k      | Result                      |
| ----------- | ----------- | ---------- | --------------------------- |
| Low (0.2)   | Low (0.5)   | Low (10)   | Very deterministic          |
| Low (0.2)   | High (0.95) | High (100) | Slightly varied but focused |
| High (0.9)  | Low (0.5)   | Low (10)   | Random among top choices    |
| High (0.9)  | High (0.95) | High (100) | Maximum creativity          |

---

## 🎯 Practical Tips

### Do's ✅

1. **Start with defaults**: Most APIs have sensible defaults (temp ~0.7, top-p ~0.9)
2. **Adjust one parameter at a time**: Helps understand the impact of each
3. **Test with representative prompts**: Ensure settings work for your use case
4. **Document your settings**: Makes reproduction and debugging easier

### Don'ts ❌

1. **Don't use temperature = 0 for everything**: Some tasks benefit from variation
2. **Don't set both top-k and top-p to very restrictive values**: May over-constrain
3. **Don't ignore context window limits**: Will cause truncation and lost information

---

## 📊 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│              PARAMETER QUICK REFERENCE                   │
├─────────────────────────────────────────────────────────┤
│ TEMPERATURE                                              │
│   0.0-0.3: Factual, Code, Data extraction               │
│   0.4-0.6: Balanced, General purpose                    │
│   0.7-1.0: Creative, Brainstorming                      │
├─────────────────────────────────────────────────────────┤
│ TOP-P (Nucleus Sampling)                                │
│   0.1-0.5: Very focused                                 │
│   0.9: Standard default                                 │
│   0.95-1.0: More diverse                                │
├─────────────────────────────────────────────────────────┤
│ TOP-K                                                   │
│   1-10: Highly restricted                               │
│   40-50: Standard default                               │
│   100+: More diverse                                    │
├─────────────────────────────────────────────────────────┤
│ CONTEXT WINDOW                                          │
│   Manage carefully - prioritize recent/relevant info    │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Takeaways

1. **Context Window** = Model's memory capacity; manage it wisely
2. **Temperature** = Creativity dial; lower for facts, higher for creativity
3. **Top-k** = Fixed limit on token choices; simple but rigid
4. **Top-p** = Dynamic limit based on probability mass; more adaptive
5. **Combine parameters** thoughtfully for optimal results

---

_Previous: [How LLMs Work](./01-how-llms-work.md) | Next: [Vector Databases & RAG](./03-vector-databases-rag.md)_
