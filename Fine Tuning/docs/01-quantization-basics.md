# Quantization Basics

Quantization is a model compression technique that converts high-precision weights (e.g., float32) to lower-precision formats like int8 or 4-bit representations, enabling faster and more efficient deployment on resource-constrained devices.

---

## Why Quantization Matters

Large Language Models have billions of parameters stored as 32-bit or 16-bit floating-point numbers. A 7B parameter model in FP32 requires ~28GB of memory just for weights—more than most consumer GPUs can handle.

| Precision | Bits per Parameter | Memory for 7B Model | Relative Size |
|-----------|-------------------|---------------------|---------------|
| FP32 | 32 | ~28 GB | 1x |
| FP16/BF16 | 16 | ~14 GB | 0.5x |
| INT8 | 8 | ~7 GB | 0.25x |
| NF4 | 4 | ~3.5 GB | 0.125x |

**Key Benefits:**
- Run larger models on consumer hardware
- Faster inference (reduced memory bandwidth)
- Lower deployment and cloud costs
- Enable fine-tuning on limited VRAM (via QLoRA)

---

## INT8 Quantization

INT8 quantization maps continuous floating-point values to discrete 8-bit integers in the range [-128, 127].

### The Mathematical Foundation

The quantization process involves two key operations:

**Quantization (float → int8):**
```
q = round((x - zero_point) / scale)
q = clip(q, -128, 127)
```

**Dequantization (int8 → float):**
```
x̂ = scale × (q - zero_point)
```

Where:
- **Scale**: The step size between adjacent quantized values
- **Zero Point**: Offset for asymmetric quantization (0 for symmetric)
- **x**: Original float value
- **q**: Quantized integer value
- **x̂**: Reconstructed (dequantized) value

### Calculating Scale

For symmetric quantization around zero:

```
scale = (max_value - min_value) / (qmax - qmin)
scale = (1.0 - (-1.0)) / (127 - (-128))
scale = 2.0 / 255 ≈ 0.00784
```

### Step-by-Step Implementation

```python
import numpy as np

# Step 1: Simulate original float values (e.g., model weights)
# Neural network weights typically range from -1 to 1
x = np.linspace(-1.0, 1.0, 100)
print(f"Original values (first 10): {x[:10]}")
# Output: [-1.0, -0.98, -0.96, -0.94, -0.92, ...]
```

```python
# Step 2: Define quantization parameters
min_x = -1.0   # Minimum value in our range
max_x = 1.0    # Maximum value in our range
qmin = -128    # Minimum int8 value
qmax = 127     # Maximum int8 value

# Step 3: Calculate scale (step size between quantized levels)
scale = (max_x - min_x) / (qmax - qmin)
print(f"Scale: {scale}")  # ≈ 0.00784

# For symmetric quantization, zero_point = 0
zero_point = 0
```

```python
# Step 4: Quantize - convert floats to int8
# Formula: q = round((x - zero_point) / scale)
q = np.round((x - zero_point) / scale).astype(int)

# Clip to valid int8 range to handle edge cases
q = np.clip(q, qmin, qmax)
print(f"Quantized values (first 10): {q[:10]}")
# Output: [-128, -125, -122, -120, -117, ...]
```

```python
# Step 5: Dequantize - convert back to floats
# Formula: x̂ = scale × (q - zero_point)
x_hat = scale * (q - zero_point)
print(f"Dequantized values (first 10): {x_hat[:10]}")
# Output: [-1.004, -0.980, -0.957, -0.941, ...]
```

### Understanding Quantization Error

The dequantized values won't exactly match the originals due to the discrete nature of quantization:

| Original (x) | Quantized (q) | Dequantized (x̂) | Error |
|--------------|---------------|------------------|-------|
| -1.000 | -128 | -1.004 | 0.004 |
| -0.980 | -125 | -0.980 | 0.000 |
| 0.000 | 0 | 0.000 | 0.000 |
| 0.980 | 125 | 0.980 | 0.000 |
| 1.000 | 127 | 0.996 | 0.004 |

**Maximum quantization error** is bounded by `scale / 2 ≈ 0.004`.

### Visualizing Quantization

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(x, x, label='Original Float (x)', linestyle='--', color='gray')
plt.scatter(x, x_hat, label='Dequantized (x̂)', color='red', s=15)
plt.title('Linear Quantization (int8) with Dequantization')
plt.xlabel('Original Float Value')
plt.ylabel('Dequantized Value')
plt.grid(True)
plt.legend()
plt.show()
```

The plot shows how dequantized values closely follow the original values, with small step-like deviations due to the discrete quantization levels.

---

## NF4 (NormalFloat4) Quantization

**NF4 is a 4-bit quantization method optimized for neural network weights that typically follow a normal (Gaussian) distribution.** It maps values into 16 non-uniform bins centered around zero, providing higher precision near zero where most weights lie.

### Why NF4 is Different

Standard uniform quantization spaces levels evenly across the range. But neural network weights cluster around zero following a bell curve. NF4 exploits this by:

1. Placing more quantization levels near zero (where weights are dense)
2. Spacing levels according to quantiles of the normal distribution
3. Minimizing expected quantization error for normally distributed data

### The 16 NF4 Representative Values

```python
# 4 bits = 2^4 = 16 possible values
# These values are placed at quantiles of the normal distribution
nf4_values = np.array([
    -1.0, -0.75, -0.5, -0.35, -0.2, -0.1, -0.05, -0.01,
     0.01,  0.05,  0.1,  0.2,  0.35,  0.5,  0.75,  1.0
])
```

**Notice:** Values are denser near zero (-0.01, 0.01, -0.05, 0.05, etc.) where most neural network weights reside.

### NF4 Quantization Implementation

```python
import numpy as np

# Define NF4 representative values (16 levels for 4 bits)
nf4_values = np.array([
    -1.0, -0.75, -0.5, -0.35, -0.2, -0.1, -0.05, -0.01,
     0.01,  0.05,  0.1,  0.2,  0.35,  0.5,  0.75,  1.0
])

# Original float values to quantize
x = np.linspace(-1.0, 1.0, 100)

def quantize_to_nf4(x_vals, nf4_vals):
    """
    Map each float value to its nearest NF4 representative.
    
    Args:
        x_vals: Array of original float values
        nf4_vals: Array of 16 NF4 representative values
    
    Returns:
        indices: Which NF4 bin each value maps to (0-15)
        quantized: The actual NF4 values after quantization
    """
    # For each x value, find the NF4 value with minimum distance
    # x_vals[:, None] creates column vector for broadcasting
    # nf4_vals[None, :] creates row vector
    # Result: distance matrix of shape (len(x_vals), 16)
    distances = np.abs(x_vals[:, None] - nf4_vals[None, :])
    
    # Find index of minimum distance for each x value
    indices = distances.argmin(axis=1)
    
    # Get the actual NF4 values
    quantized = nf4_vals[indices]
    
    return indices, quantized

# Perform quantization
indices, x_quantized = quantize_to_nf4(x, nf4_values)

print(f"Original: {x[:5]}")
print(f"Quantized: {x_quantized[:5]}")
print(f"Indices: {indices[:5]}")
```

### Visualizing NF4 Quantization

```python
plt.figure(figsize=(10, 5))
plt.plot(x, x, label='Original Float (x)', linestyle='--', color='gray')
plt.scatter(x, x_quantized, label='NF4 Quantized', color='blue', s=15)

# Mark the 16 NF4 levels
for nf4_val in nf4_values:
    plt.axhline(y=nf4_val, color='green', alpha=0.3, linestyle=':')

plt.title('NF4 Quantization (4-bit, Normal Distribution Optimized)')
plt.xlabel('Original Float Value')
plt.ylabel('Quantized Value')
plt.grid(True)
plt.legend()
plt.show()
```

The staircase pattern shows how continuous values snap to the nearest of 16 discrete NF4 levels.

---

## INT8 vs NF4 Comparison

| Aspect | INT8 | NF4 |
|--------|------|-----|
| **Bits per weight** | 8 | 4 |
| **Quantization levels** | 256 | 16 |
| **Level distribution** | Uniform | Normal-optimized |
| **Memory savings** | 4x vs FP32 | 8x vs FP32 |
| **Precision** | Higher | Lower |
| **Best for** | Inference | QLoRA training |
| **Typical error** | ~0.4% | ~2-3% |

### When to Use Each

| Scenario | Recommendation |
|----------|----------------|
| Production inference | INT8 (good balance) |
| Fine-tuning with limited VRAM | NF4 + QLoRA |
| Maximum quality needed | FP16/BF16 |
| Edge deployment | INT8 or NF4 |
| Research/experimentation | FP16 |

---

## Quantization in Practice

### Using bitsandbytes Library

NF4 is supported by Hugging Face's **bitsandbytes** library, enabling seamless integration into PyTorch pipelines:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

# Configure 4-bit NF4 quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,              # Enable 4-bit loading
    bnb_4bit_quant_type="nf4",      # Use NF4 (not uniform int4)
    bnb_4bit_compute_dtype=torch.float16,  # Compute in FP16
    bnb_4bit_use_double_quant=True, # Double quantization for more savings
)

# Load model with quantization
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
)
```

### Using Unsloth (Optimized)

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length=2048,
    dtype=None,          # Auto-detect best dtype
    load_in_4bit=True,   # NF4 quantization
)
```

---

## Key Takeaways

1. **Quantization** reduces model size and inference cost by converting high-precision weights to lower-precision formats like int8 or 4-bit representations

2. **INT8 quantization** provides 4x compression with minimal quality loss using uniform quantization levels

3. **NF4 (NormalFloat4)** is a 4-bit quantization method optimized for neural network weights that typically follow a normal distribution. It maps values into 16 non-uniform bins centered around zero, providing higher precision near zero where most weights lie

4. **NF4 is widely used** in large language model compression strategies like QLoRA, allowing models to be fine-tuned and deployed with significantly reduced memory and compute requirements without substantial accuracy loss

5. **NF4 is supported** by libraries such as Hugging Face's bitsandbytes, enabling seamless integration into PyTorch pipelines for 4-bit quantized model loading and inference

---

## Next Steps

→ [Fine-Tuning with Unsloth](02-finetuning-with-unsloth.md) — Apply quantization to practical fine-tuning with LoRA and QLoRA
