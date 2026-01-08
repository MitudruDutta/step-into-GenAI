# Fine-Tuning with Unsloth

This document covers the complete workflow for fine-tuning Large Language Models using Unsloth, LoRA, and QLoRA techniques.

---

## What is Fine-Tuning?

**Fine-tuning a large language model (LLM) is the process of retraining a pre-trained model (or foundation model) for a specific task, format, dataset, or tone.**

Instead of training from scratch (which requires massive compute), fine-tuning adapts an existing model's knowledge to your specific use case.

### Fine-Tuning Approaches

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Full Fine-Tuning** | Update all model parameters | High adaptability | Requires massive compute, risk of catastrophic forgetting |
| **PEFT (Parameter-Efficient)** | Update only a subset of parameters | Low compute, maintains base knowledge | Slightly less adaptable |

**Full Fine-Tuning** updates all the model's parameters, offering high adaptability but requiring substantial computational resources and posing risks like **catastrophic forgetting**, where the model loses previously learned information.

**Parameter-Efficient Fine-Tuning (PEFT)** techniques like LoRA adjust only a subset of model parameters, significantly reducing computational demands while maintaining performance, making fine-tuning more accessible.

---

## LoRA: Low-Rank Adaptation

**LoRA (Low-Rank Adaptation) fine-tunes LLMs by adding trainable low-rank matrices to frozen model weights, drastically reducing training cost.**

### The Core Idea

Instead of updating all parameters, LoRA learns only a small number of parameters, making it efficient and memory-friendly. Compared to full fine-tuning, LoRA is much more efficient in terms of training time and hardware resource utilization.

### The Mathematics

For a pre-trained weight matrix **W** of dimensions (d × k), LoRA adds:

```
W' = W + ΔW = W + BA
```

Where:
- **W**: Original frozen weights (d × k) — NOT updated during training
- **B**: Low-rank matrix (d × r) — Trainable
- **A**: Low-rank matrix (r × k) — Trainable
- **r**: Rank (typically 8-64, much smaller than d or k)

### Why This Works

| Full Fine-Tuning | LoRA |
|------------------|------|
| Update all ~7B parameters | Update ~0.1% of parameters |
| Requires 28GB+ VRAM | Works with 8GB VRAM |
| Slow training | Fast training |
| Large checkpoint files (~14GB) | Small adapter files (~100MB) |
| Risk of catastrophic forgetting | Preserves base model knowledge |

### Visual Intuition

```
Original Forward Pass:
    Input → [W] → Output

LoRA Forward Pass:
    Input → [W (frozen)] → Output
              ↓
           [B × A] → (added to output)
```

The original weights W remain frozen. Only the small matrices B and A are trained.

---

## QLoRA: Quantized LoRA

**QLoRA combines 4-bit quantization with Low-Rank Adaptation (LoRA) to enable efficient fine-tuning of large language models (LLMs) on consumer-grade GPUs, significantly reducing memory usage without compromising performance.**

### Key Innovations

1. **4-bit NormalFloat (NF4) quantization** — Information-theoretically optimal for normally distributed weights, leading to better accuracy compared to standard 4-bit methods

2. **Double quantization** — Quantizes the quantization constants themselves, further reducing memory footprint

3. **Paged optimizers** — Manages memory spikes during training by offloading optimizer states to CPU when needed

### How QLoRA Works

```
┌─────────────────────────────────────────────────────────┐
│                    QLoRA Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Base Model Weights (W)                                │
│   ├── Quantized to 4-bit NF4                           │
│   └── FROZEN during training                           │
│                                                         │
│   LoRA Adapters (B, A)                                  │
│   ├── Stored in FP16/BF16                              │
│   └── TRAINABLE                                        │
│                                                         │
│   Forward Pass:                                         │
│   output = W_quantized(x) + scale * B(A(x))            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**By freezing the quantized base model and training only the low-rank adapter layers**, QLoRA maintains the original model's knowledge while adapting it to new tasks, achieving performance comparable to full fine-tuning with significantly fewer trainable parameters.

### Memory Comparison

| Model Size | Full Fine-Tuning | LoRA (FP16) | QLoRA (4-bit) |
|------------|------------------|-------------|---------------|
| 3B | ~24 GB | ~12 GB | ~6 GB |
| 7B | ~56 GB | ~28 GB | ~8 GB |
| 13B | ~104 GB | ~52 GB | ~16 GB |
| 65B | ~520 GB | ~260 GB | ~48 GB |

QLoRA makes it feasible to fine-tune models with up to 65 billion parameters on a single 48GB GPU.

---

## Unsloth: Optimized Fine-Tuning

Unsloth is an optimized library that provides:
- **2x faster training** through custom CUDA kernels
- **50% less memory** usage
- **Easy LoRA/QLoRA** integration
- **GGUF export** for Ollama/llama.cpp deployment

---

## Complete Fine-Tuning Workflow

### Step 1: Install Dependencies

```bash
pip install unsloth torch transformers datasets trl peft
```

### Step 2: Load a Quantized Model

```python
from unsloth import FastLanguageModel
import torch

# Configuration
max_seq_length = 2048  # Context length (affects memory)
dtype = None           # Auto-detect: float16 for T4/V100, bfloat16 for Ampere+
load_in_4bit = True    # Enable QLoRA with NF4 quantization

# Load model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,  # 4-bit NF4 quantization
)
```

**Parameter Explanation:**
- `model_name`: HuggingFace model ID or Unsloth optimized version
- `max_seq_length`: Maximum tokens the model can process (higher = more memory)
- `dtype`: Compute precision (None for auto-detection)
- `load_in_4bit`: Enables NF4 quantization for QLoRA

### Step 3: Add LoRA Adapters

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank - higher captures more but uses more memory
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention layers
        "gate_proj", "up_proj", "down_proj",      # MLP layers
    ],
    lora_alpha=16,                    # Scaling factor
    lora_dropout=0,                   # Dropout (0 = faster with Unsloth)
    bias="none",                      # Don't train bias terms
    use_gradient_checkpointing="unsloth",  # Memory optimization
    random_state=3407,                # Reproducibility
)
```

**LoRA Parameters Explained:**

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `r` | Rank of low-rank matrices. Higher = more capacity but more memory | 8, 16, 32, 64 |
| `target_modules` | Which layers to add adapters to | Attention + MLP projections |
| `lora_alpha` | Scaling factor. Effective scale = alpha/r | Usually same as r |
| `lora_dropout` | Regularization dropout | 0 (Unsloth optimized) |
| `bias` | Whether to train bias terms | "none" for efficiency |
| `use_gradient_checkpointing` | Trade compute for memory | "unsloth" for best |

### Step 4: Prepare the Dataset

```python
from datasets import load_dataset

# Load a dataset (example: R1-Distill for reasoning capabilities)
dataset = load_dataset(
    "ServiceNow-AI/R1-Distill-SFT",
    "v0",
    split="train"
)

print(dataset[:5])  # Inspect the data
```

### Step 5: Create Prompt Template

The prompt template defines how inputs and outputs are formatted for training:

```python
# Template for instruction-following with reasoning
r1_prompt = """You are a reflective assistant engaging in thorough, iterative reasoning, mimicking human thought processes.

<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{}"""

def formatting_prompts_func(examples):
    """Format dataset examples into training prompts."""
    inputs = examples["prompt"]
    outputs = examples["response"]
    
    # Combine input and output with the template
    texts = [
        r1_prompt.format(inp, out) 
        for inp, out in zip(inputs, outputs)
    ]
    
    return {"text": texts}

# Apply formatting to dataset
dataset = dataset.map(formatting_prompts_func, batched=True)
```

### Step 6: Configure the Trainer

```python
from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from unsloth import is_bfloat16_supported

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",        # Column containing formatted text
    max_seq_length=2048,
    data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
    dataset_num_proc=2,               # Parallel data processing
    packing=False,                    # Don't pack multiple samples
    
    args=TrainingArguments(
        # Batch settings
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,  # Effective batch = 2 × 4 = 8
        
        # Training duration
        warmup_steps=5,
        max_steps=60,                   # Or use num_train_epochs=1
        
        # Optimization
        learning_rate=2e-4,             # Typical for LoRA
        optim="adamw_8bit",             # Memory-efficient optimizer
        weight_decay=0.01,
        lr_scheduler_type="linear",
        
        # Precision
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        
        # Logging
        logging_steps=1,
        output_dir="outputs",
        seed=3407,
    ),
)
```

**Training Arguments Explained:**

| Argument | Description |
|----------|-------------|
| `per_device_train_batch_size` | Samples processed per GPU per step |
| `gradient_accumulation_steps` | Steps before weight update (effective batch = batch × accumulation) |
| `learning_rate` | 2e-4 is typical for LoRA fine-tuning |
| `optim="adamw_8bit"` | 8-bit Adam optimizer saves memory |
| `max_steps` | Total training steps (alternative: `num_train_epochs`) |
| `fp16/bf16` | Mixed precision training for speed |

### Step 7: Train the Model

```python
# Start training
trainer_stats = trainer.train()

# View training statistics
print(f"Training time: {trainer_stats.metrics['train_runtime']:.2f}s")
print(f"Final loss: {trainer_stats.metrics['train_loss']:.4f}")
```

### Step 8: Test the Fine-Tuned Model

```python
from unsloth.chat_templates import get_chat_template

# Apply chat template to tokenizer
tokenizer = get_chat_template(
    tokenizer,
    chat_template="llama-3.1",
)

# Switch model to inference mode
FastLanguageModel.for_inference(model)

# Prepare input
messages = [
    {"role": "system", "content": "You are a reflective assistant..."},
    {"role": "user", "content": "What is 2+2? Think step by step."},
]

inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
).to("cuda")

# Generate response
outputs = model.generate(
    input_ids=inputs,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
)

# Decode and print
response = tokenizer.batch_decode(outputs)
print(response[0])
```

---

## Saving and Exporting Models

### Save LoRA Adapters Only

```python
# Save just the adapter weights (~100MB instead of ~6GB)
model.save_pretrained("my-finetuned-model")
tokenizer.save_pretrained("my-finetuned-model")
```

### Export to GGUF Format

GGUF is the format used by llama.cpp and Ollama for efficient CPU/GPU inference:

```python
# Export as GGUF for Ollama/llama.cpp
model.save_pretrained_gguf("my-model-gguf", tokenizer)
```

### Deploy with Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# Create model from GGUF (use the generated Modelfile)
ollama create my-model -f Modelfile

# Run inference
ollama run my-model "What is machine learning?"
```

---

## Best Practices

### Hyperparameter Guidelines

| Parameter | Recommendation |
|-----------|----------------|
| LoRA rank (r) | Start with 16, increase if underfitting |
| Learning rate | 1e-4 to 3e-4 for LoRA |
| Batch size | As large as memory allows |
| Epochs | 1-3 for most tasks |
| lora_alpha | Usually equal to r |

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Out of Memory (OOM) | Reduce batch size, enable gradient checkpointing, use 4-bit |
| Slow training | Use Unsloth optimizations, increase batch size |
| Poor output quality | Increase rank (r), more training data, lower learning rate |
| Overfitting | Reduce epochs, add dropout, use more diverse data |
| Catastrophic forgetting | Use LoRA instead of full fine-tuning |

---

## Key Takeaways

1. **Fine-tuning an LLM** is retraining a pre-trained model for a specific task, format, dataset, or tone

2. **Full Fine-Tuning** updates all parameters but requires massive compute and risks catastrophic forgetting

3. **LoRA (Low-Rank Adaptation)** fine-tunes LLMs by adding trainable low-rank matrices to frozen model weights, drastically reducing training cost

4. **QLoRA** combines 4-bit quantization with LoRA to enable efficient fine-tuning on consumer-grade GPUs, significantly reducing memory usage without compromising performance

5. **The 4-bit NormalFloat (NF4) quantization technique** is central to QLoRA, offering an information-theoretically optimal approach for normally distributed weights

6. **QLoRA innovations** like double quantization and paged optimizers further reduce memory footprint, making it feasible to fine-tune models with up to 65 billion parameters on a single 48GB GPU

7. **By freezing the quantized base model and training only the low-rank adapter layers**, QLoRA maintains the original model's knowledge while adapting it to new tasks

---

## Resources

- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [LoRA Paper](https://arxiv.org/abs/2106.09685) — "LoRA: Low-Rank Adaptation of Large Language Models"
- [QLoRA Paper](https://arxiv.org/abs/2305.14314) — "QLoRA: Efficient Finetuning of Quantized LLMs"
- [Ollama](https://ollama.com/) — Local LLM deployment
- [bitsandbytes](https://github.com/TimDettmers/bitsandbytes) — Quantization library
