"""
LLM-Based Semantic Similarity Checker
======================================

This module evaluates the semantic similarity between expected and generated
answers using LLM-based comparison. It's used to validate RAG outputs against
ground truth for hallucination detection.

Why LLM-Based Similarity?
-------------------------
Traditional similarity metrics (cosine, Jaccard, BLEU) often fail with:
- Paraphrased answers (same meaning, different words)
- Partial matches (correct but incomplete answers)
- Contextual nuances (technically different but contextually equivalent)

LLM-based evaluation can understand semantic equivalence even when
the surface forms differ significantly.

Use Cases:
---------
1. Validating RAG chatbot outputs against expected answers
2. Detecting hallucinations (low similarity = potential fabrication)
3. Automated testing of Q&A systems
4. Comparing answer quality across different models

Example:
    from similarity_checker import check_similarity, evaluate_answer_quality
    
    score = check_similarity(
        expected="Cancel within 24 hours for a full refund",
        generated="You can get all your money back if you cancel in the first day"
    )
    # Returns ~85 (high similarity despite different wording)
"""

from groq import Groq
from dotenv import load_dotenv
from typing import Dict, Optional
import logging
import re

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_similarity(
    expected: str, 
    generated: str,
    model: str = "llama-3.1-70b-versatile",
    max_retries: int = 2
) -> int:
    """
    Compare expected and generated answers using LLM-based semantic evaluation.
    
    This function uses an LLM to assess how semantically similar two text
    passages are, which is more robust than lexical similarity measures
    for evaluating paraphrases and semantically equivalent responses.
    
    Scoring Guidelines (used by LLM):
    - 90-100: Answers convey identical information
    - 70-89: Same core meaning with minor differences
    - 50-69: Partially overlapping information
    - 30-49: Related but significantly different
    - 0-29: Unrelated or contradictory
    
    Args:
        expected: Reference/ground truth answer
        generated: Generated answer to evaluate
        model: Groq model ID for evaluation
        max_retries: Number of retry attempts on parsing failure
        
    Returns:
        Integer similarity score (0-100), or -1 on error
    """
    client = Groq()
    
    # Enhanced prompt with clearer instructions and examples
    prompt = f"""You are evaluating semantic similarity between two text answers.

EXPECTED ANSWER (Ground Truth):
"{expected}"

GENERATED ANSWER (To Evaluate):
"{generated}"

SCORING CRITERIA:
- 90-100: Nearly identical meaning, all key information present
- 70-89: Same core message, minor differences in detail or phrasing  
- 50-69: Partial overlap, missing or extra significant information
- 30-49: Related topic but substantially different claims
- 0-29: Unrelated, contradictory, or completely wrong information

TASK: Output ONLY a single integer between 0 and 100.
No explanation, no text, just the number.

Score:"""

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert evaluator. Respond with only a number."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent scoring
                max_tokens=10
            )
            
            # Extract numeric score from response
            response_text = response.choices[0].message.content.strip()
            
            # Handle responses that might include extra text
            numbers = re.findall(r'\d+', response_text)
            if numbers:
                score = int(numbers[0])
                # Clamp to valid range
                return max(0, min(100, score))
            else:
                logger.warning(f"No number found in response: {response_text}")
                
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            
    logger.error("All similarity check attempts failed")
    return -1


def evaluate_answer_quality(
    expected: str,
    generated: str,
    model: str = "llama-3.1-70b-versatile"
) -> Dict:
    """
    Perform comprehensive quality evaluation of a generated answer.
    
    This function provides a detailed breakdown of answer quality across
    multiple dimensions, useful for understanding WHY an answer is good or bad.
    
    Args:
        expected: Reference/ground truth answer
        generated: Generated answer to evaluate
        model: Groq model ID for evaluation
        
    Returns:
        Dictionary containing:
        - overall_score: Main similarity score (0-100)
        - factual_accuracy: Does it contain correct facts?
        - completeness: Does it cover all key points?
        - relevance: Is it on-topic?
        - hallucination_risk: Likelihood of fabricated content
        - analysis: Brief explanation of scores
    """
    client = Groq()
    
    prompt = f"""Evaluate this generated answer against the expected answer.

EXPECTED: "{expected}"
GENERATED: "{generated}"

Provide evaluation in this exact JSON format:
{{
    "overall_score": <0-100>,
    "factual_accuracy": <0-100>,
    "completeness": <0-100>,
    "relevance": <0-100>,
    "hallucination_risk": "<LOW|MEDIUM|HIGH>",
    "analysis": "<brief 1-2 sentence explanation>"
}}

Respond with ONLY the JSON, no other text."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an answer quality evaluator. Respond only with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON from response
        import json
        
        # Handle potential markdown code blocks
        if "```" in response_text:
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
        
        result = json.loads(response_text)
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        return {
            "overall_score": check_similarity(expected, generated),
            "error": "Detailed evaluation failed, using basic similarity"
        }
    except Exception as e:
        logger.error(f"Quality evaluation failed: {e}")
        return {"error": str(e), "overall_score": -1}


def batch_evaluate(
    test_cases: list,
    model: str = "llama-3.1-70b-versatile"
) -> Dict:
    """
    Evaluate multiple expected/generated answer pairs.
    
    Useful for running automated test suites to assess overall
    RAG system quality.
    
    Args:
        test_cases: List of dicts with 'expected' and 'generated' keys
        model: Groq model ID for evaluation
        
    Returns:
        Dictionary with individual scores and aggregate statistics
    """
    scores = []
    results = []
    
    for i, case in enumerate(test_cases):
        score = check_similarity(
            expected=case['expected'],
            generated=case['generated'],
            model=model
        )
        scores.append(score)
        results.append({
            'case_id': i + 1,
            'expected': case['expected'][:50] + '...',
            'generated': case['generated'][:50] + '...',
            'score': score
        })
    
    # Calculate statistics (exclude failed evaluations)
    valid_scores = [s for s in scores if s >= 0]
    
    return {
        'results': results,
        'statistics': {
            'total_cases': len(test_cases),
            'successful_evaluations': len(valid_scores),
            'average_score': sum(valid_scores) / len(valid_scores) if valid_scores else 0,
            'min_score': min(valid_scores) if valid_scores else 0,
            'max_score': max(valid_scores) if valid_scores else 0,
            'passing_rate': len([s for s in valid_scores if s >= 70]) / len(valid_scores) if valid_scores else 0
        }
    }


def demonstrate_similarity_checking():
    """
    Demonstrate similarity checking with various example pairs.
    """
    print("\n" + "🔍 " * 20)
    print("  SEMANTIC SIMILARITY CHECKER DEMO")
    print("🔍 " * 20 + "\n")
    
    test_pairs = [
        # High similarity (paraphrase)
        {
            "expected": "Passengers can check in online 24 hours before flight departure.",
            "generated": "Online check-in opens 24 hours prior to your scheduled flight.",
            "description": "Paraphrased (should be ~90+)"
        },
        # Medium similarity (partial)
        {
            "expected": "Refunds are processed within 7-10 business days to your original payment method.",
            "generated": "You'll receive your refund in about a week.",
            "description": "Partial info (should be ~60-70)"
        },
        # Low similarity (unrelated)
        {
            "expected": "You can bring one carry-on bag and one personal item.",
            "generated": "Our in-flight meals include vegetarian options.",
            "description": "Unrelated (should be ~10-20)"
        },
        # Hallucination detection
        {
            "expected": "Name changes are not permitted after booking.",
            "generated": "You can change the name on your ticket for a $50 fee up to 24 hours before departure.",
            "description": "Contradictory/Hallucinated (should be ~10-30)"
        }
    ]
    
    print("Testing similarity evaluation...\n")
    
    for pair in test_pairs:
        score = check_similarity(pair["expected"], pair["generated"])
        
        print(f"📋 {pair['description']}")
        print(f"   Expected:  {pair['expected'][:60]}...")
        print(f"   Generated: {pair['generated'][:60]}...")
        print(f"   Score:     {score}/100")
        print()


# Main execution
if __name__ == "__main__":
    demonstrate_similarity_checking()