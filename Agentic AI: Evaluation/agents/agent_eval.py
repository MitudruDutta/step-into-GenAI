from agno.eval.accuracy import AccuracyEval, AccuracyResult

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
            num_iterations=3
        )
        print(f"\nEvaluating: {test['question']}")
        result = evaluation.run(print_results=True)
        
        # Check if score meets minimum threshold
        score = getattr(result, 'score', None) or getattr(evaluation, 'score', 0)
        if score < test["min_score"]:
            print(f"FAILED: Score {score} is below minimum threshold {test['min_score']}")
        else:
            print(f"PASSED: Score {score} meets minimum threshold {test['min_score']}")
    

if __name__ == "__main__":
    test_inventory_agent()
