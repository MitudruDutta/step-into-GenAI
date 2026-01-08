# 🔧 Fine Tuning

This module covers model fine-tuning techniques for Large Language Models, from understanding quantization fundamentals to practical fine-tuning with modern tools like Unsloth, LoRA, and QLoRA.

---

## 📚 Module Contents

| Document | Description |
|----------|-------------|
| [01-quantization-basics.md](docs/01-quantization-basics.md) | Understanding int8 and NF4 quantization techniques |
| [02-finetuning-with-unsloth.md](docs/02-finetuning-with-unsloth.md) | Practical fine-tuning with LoRA, QLoRA, and Unsloth |

---

## 📓 Notebooks

| Notebook | Description |
|----------|-------------|
| [quantization_basics.ipynb](notebooks/quantization_basics.ipynb) | Hands-on int8 and NF4 quantization implementation |
| [unsloth_finetuning.ipynb](notebooks/unsloth_finetuning.ipynb) | Fine-tuning Llama 3.2 with Unsloth on R1-Distill dataset |

---

## 🎯 Learning Objectives

By the end of this module, you will understand:

1. **Quantization Fundamentals**
   - How int8 quantization maps floats to integers
   - Why NF4 is optimized for neural network weights
   - Trade-offs between compression and precision

2. **Fine-Tuning Approaches**
   - Full fine-tuning vs Parameter-Efficient Fine-Tuning (PEFT)
   - Why full fine-tuning risks catastrophic forgetting

3. **LoRA (Low-Rank Adaptation)**
   - How LoRA adds trainable low-rank matrices to frozen weights
   - Why it's efficient and memory-friendly

4. **QLoRA**
   - Combining 4-bit quantization with LoRA
   - Double quantization and paged optimizers
   - Fine-tuning 65B models on consumer GPUs

5. **Practical Skills**
   - Fine-tune models using Unsloth
   - Export models to GGUF for Ollama deployment

---

## 🔑 Key Concepts

### Quantization

**Quantization** reduces model size and inference cost by converting high-precision weights (float32) to lower-precision formats (int8, 4-bit).

| Precision | Memory for 7B Model | Compression |
|-----------|---------------------|-------------|
| FP32 | ~28 GB | 1x |
| FP16 | ~14 GB | 2x |
| INT8 | ~7 GB | 4x |
| NF4 | ~3.5 GB | 8x |

**NF4 (NormalFloat4)** is a 4-bit quantization method optimized for neural network weights that follow a normal distribution, providing higher precision near zero where most weights lie.

### Fine-Tuning

**Fine-tuning an LLM** is retraining a pre-trained model for a specific task, format, dataset, or tone.

| Approach | Parameters Updated | Memory | Risk |
|----------|-------------------|--------|------|
| Full Fine-Tuning | All (~7B) | Very High | Catastrophic forgetting |
| LoRA | ~0.1% | Low | Minimal |
| QLoRA | ~0.1% (4-bit base) | Very Low | Minimal |

### LoRA

**LoRA** fine-tunes LLMs by adding trainable low-rank matrices (B, A) to frozen model weights:

```
W' = W + BA
```

Instead of updating all parameters, LoRA learns only a small number, making it efficient and memory-friendly.

### QLoRA

**QLoRA** combines 4-bit NF4 quantization with LoRA:
- Base model quantized to 4-bit (frozen)
- LoRA adapters in FP16 (trainable)
- Enables fine-tuning 65B models on a single 48GB GPU

---

## 🛤️ Learning Path

```
┌─────────────────────────────────────────────────────────────────┐
│                    FINE TUNING MODULE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────┐                                          │
│  │ 1. Quantization  │  Understand int8 and NF4                 │
│  │    Basics        │  compression techniques                  │
│  └────────┬─────────┘                                          │
│           │                                                    │
│           ▼                                                    │
│  ┌──────────────────┐                                          │
│  │ 2. Fine-Tuning   │  Learn LoRA, QLoRA, and                  │
│  │    with Unsloth  │  practical training workflow             │
│  └──────────────────┘                                          │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Prerequisites

- Understanding of LLM fundamentals (see Gen AI: Foundation module)
- Basic PyTorch knowledge
- GPU with at least 8GB VRAM (16GB recommended for 7B models)

### Required Packages

```bash
pip install unsloth torch transformers datasets trl peft bitsandbytes
```

---

## 📖 Quick Start

1. **Understand Quantization** → Read [01-quantization-basics.md](docs/01-quantization-basics.md)
2. **Run Quantization Notebook** → Execute [quantization_basics.ipynb](notebooks/quantization_basics.ipynb)
3. **Learn Fine-Tuning** → Read [02-finetuning-with-unsloth.md](docs/02-finetuning-with-unsloth.md)
4. **Fine-Tune a Model** → Follow [unsloth_finetuning.ipynb](notebooks/unsloth_finetuning.ipynb)

---

## 💡 Key Takeaways

- **Fine-tuning** adapts pre-trained models to specific tasks without training from scratch
- **Full fine-tuning** updates all parameters but risks catastrophic forgetting
- **LoRA** adds small trainable matrices, reducing compute by ~99%
- **QLoRA** combines 4-bit quantization with LoRA for consumer GPU training
- **NF4** is information-theoretically optimal for normally distributed weights
- **Unsloth** provides 2x faster training with 50% less memory

---

## 🔗 Related Modules

- [Gen AI: Foundation](../Gen%20AI%3A%20Foundation/) — LLM fundamentals and parameters
- [Agentic AI: Basics](../Agentic%20AI%3A%20Basics/) — Using fine-tuned models in agents
