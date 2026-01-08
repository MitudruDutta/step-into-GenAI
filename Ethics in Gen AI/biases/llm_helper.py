"""
LLM Helper Module for Bias Detection in AI
==========================================

This module provides utilities for generating text completions using LLMs
to study and demonstrate bias patterns in language models.

Bias in LLMs can manifest as:
- Gender bias (e.g., "A doctor is..." completing with male pronouns)
- Racial bias (stereotypical associations)
- Age bias (assumptions about capabilities)
- Socioeconomic bias (wealth/class stereotypes)

Usage:
    from llm_helper import generate
    completion = generate("A doctor is")
"""

import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def generate(
    prompt: str,
    model: str = "llama-3.1-8b-instant",
    max_tokens: int = 50,
    temperature: float = 0.7
) -> str:
    """
    Generate text completion for bias analysis.
    
    This function is designed to study how LLMs complete sentences,
    which can reveal underlying biases in the training data.
    
    Args:
        prompt: The sentence starter to complete (e.g., "A nurse is")
        model: The LLM model to use for generation
        max_tokens: Maximum tokens in the completion
        temperature: Sampling temperature (higher = more random)
    
    Returns:
        The generated completion text
        
    Example:
        >>> generate("A software engineer typically")
        "works long hours and enjoys solving complex problems..."
        
    Note:
        The completions may reveal biases present in the model's
        training data. This is intentional for educational purposes.
    """
    try:
        client = Groq()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Complete the following sentence naturally and concisely."
                },
                {
                    "role": "user",
                    "content": f"Complete this sentence: {prompt}"
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"[Error generating completion: {str(e)}]"


def analyze_bias_patterns(prompts: list[str], num_samples: int = 3) -> dict:
    """
    Analyze bias patterns by generating multiple completions for each prompt.
    
    Args:
        prompts: List of sentence starters to analyze
        num_samples: Number of completions per prompt
        
    Returns:
        Dictionary mapping prompts to their completions
    """
    results = {}
    for prompt in prompts:
        completions = []
        for _ in range(num_samples):
            completion = generate(prompt, temperature=0.9)
            completions.append(completion)
        results[prompt] = completions
    return results