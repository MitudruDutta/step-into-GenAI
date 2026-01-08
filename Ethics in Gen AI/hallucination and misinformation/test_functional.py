"""
Functional Testing for RAG-Based Airline Chatbot
=================================================

This module contains functional tests to validate that the RAG chatbot
produces accurate, grounded responses for expected airline FAQ queries.

Test Philosophy:
---------------
Functional tests verify the system works correctly under normal conditions.
These tests use questions that SHOULD be answerable from the knowledge base
and validate that responses are semantically similar to expected answers.

Key Metrics:
-----------
- Similarity Score: LLM-based semantic comparison (0-100)
- Pass Threshold: Typically 70-80 for semantic similarity
- Coverage: Percentage of test cases that pass

This differs from adversarial testing (test_adversarial.py) which tests
edge cases, out-of-scope queries, and hallucination resistance.

Usage:
    python test_functional.py
    
    # Or programmatically:
    from test_functional import FunctionalTestSuite
    suite = FunctionalTestSuite()
    results = suite.run_all_tests()
"""

from airline_chatbot import RAGAnswerTool
from similarity_checker import check_similarity
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TestCase:
    """
    Represents a single functional test case.
    
    Attributes:
        id: Unique test identifier
        category: Test category (e.g., "refund", "booking", "baggage")
        question: The query to send to the chatbot
        expected_answer: Ground truth answer for comparison
        pass_threshold: Minimum similarity score to pass (default 70)
    """
    id: str
    category: str
    question: str
    expected_answer: str
    pass_threshold: int = 70


@dataclass
class TestResult:
    """
    Results from running a single test case.
    
    Attributes:
        test_case: The original test case
        generated_answer: What the chatbot produced
        similarity_score: LLM-evaluated similarity (0-100)
        passed: Whether similarity >= threshold
        execution_time_ms: How long the test took
        source_questions: RAG retrieval sources used
    """
    test_case: TestCase
    generated_answer: str
    similarity_score: int
    passed: bool
    execution_time_ms: float = 0
    source_questions: List[str] = field(default_factory=list)


class FunctionalTestSuite:
    """
    Comprehensive functional test suite for the airline FAQ chatbot.
    
    This suite validates that the RAG system produces accurate answers
    for questions that should be answerable from the knowledge base.
    
    Test Categories:
    - Refund policies (24-hour rule, general refunds)
    - Flight changes and modifications
    - Booking procedures
    - General FAQ queries
    """
    
    def __init__(self, pass_threshold: int = 70):
        """
        Initialize the test suite.
        
        Args:
            pass_threshold: Default minimum score to pass tests
        """
        self.chatbot = RAGAnswerTool()
        self.pass_threshold = pass_threshold
        self.test_cases = self._load_test_cases()
        
    def _load_test_cases(self) -> List[TestCase]:
        """
        Load all functional test cases.
        
        In a production system, these might come from a JSON/YAML file.
        """
        return [
            # ===== REFUND POLICY TESTS =====
            TestCase(
                id="REFUND-001",
                category="Refund - 24 Hour Rule",
                question="I booked my flight 3 hours ago, if I cancel right now, will I get a refund?",
                expected_answer="Yes, you are eligible for a refund since you booked your flight within the 24 hour window."
            ),
            TestCase(
                id="REFUND-002",
                category="Refund - Outside Window",
                question="I booked my flight 5 days ago, if I cancel right now, will I get a refund?",
                expected_answer="No, you will not be eligible for a refund since you booked your flight 5 days ago, which is beyond the 24-hour window. However, you may retain the ticket value for future travel, subject to certain conditions."
            ),
            TestCase(
                id="REFUND-003",
                category="Refund - Processing Time",
                question="How long does it take to receive my refund?",
                expected_answer="Refunds are typically processed within 7-10 business days to your original payment method."
            ),
            
            # ===== FLIGHT CHANGE TESTS =====
            TestCase(
                id="CHANGE-001",
                category="Flight Changes - Fees",
                question="Do I have to pay a fee to change my flight?",
                expected_answer="Change or cancellation fees may apply based on the type of ticket purchased. Review the fare rules associated with your ticket to understand applicable fees."
            ),
            TestCase(
                id="CHANGE-002",
                category="Flight Changes - Process",
                question="How can I modify my existing booking?",
                expected_answer="You can modify your booking online through our website, mobile app, or by contacting customer service."
            ),
            
            # ===== CHECK-IN TESTS =====
            TestCase(
                id="CHECKIN-001",
                category="Check-In - Online",
                question="When can I check in for my flight online?",
                expected_answer="Online check-in is available 24 hours before your scheduled departure time."
            ),
        ]
    
    def run_test(self, test_case: TestCase) -> TestResult:
        """
        Execute a single test case.
        
        Args:
            test_case: The test to run
            
        Returns:
            TestResult with all execution details
        """
        import time
        start_time = time.time()
        
        # Get chatbot response
        response = self.chatbot.get_answer(test_case.question)
        generated_answer = response['answer']
        
        # Evaluate similarity
        similarity_score = check_similarity(
            expected=test_case.expected_answer,
            generated=generated_answer
        )
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return TestResult(
            test_case=test_case,
            generated_answer=generated_answer,
            similarity_score=similarity_score,
            passed=similarity_score >= test_case.pass_threshold,
            execution_time_ms=execution_time,
            source_questions=response.get('source_questions', [])
        )
    
    def run_all_tests(self, verbose: bool = True) -> Dict:
        """
        Execute all test cases in the suite.
        
        Args:
            verbose: If True, print results as tests complete
            
        Returns:
            Dictionary with all results and aggregate statistics
        """
        print("\n" + "=" * 70)
        print("  FUNCTIONAL TEST SUITE - AIRLINE FAQ CHATBOT")
        print("=" * 70)
        print(f"  Running {len(self.test_cases)} test cases...")
        print(f"  Pass threshold: {self.pass_threshold}%")
        print("=" * 70 + "\n")
        
        results: List[TestResult] = []
        
        for test_case in self.test_cases:
            result = self.run_test(test_case)
            results.append(result)
            
            if verbose:
                status = "✅ PASSED" if result.passed else "❌ FAILED"
                print(f"[{test_case.id}] {test_case.category}")
                print(f"   Status: {status} (Score: {result.similarity_score}/100)")
                
                if not result.passed:
                    print(f"   Expected: {test_case.expected_answer[:80]}...")
                    print(f"   Got:      {result.generated_answer[:80]}...")
                print()
        
        # Calculate aggregate statistics
        passed_tests = [r for r in results if r.passed]
        failed_tests = [r for r in results if not r.passed]
        scores = [r.similarity_score for r in results if r.similarity_score >= 0]
        
        summary = {
            'total_tests': len(self.test_cases),
            'passed': len(passed_tests),
            'failed': len(failed_tests),
            'pass_rate': len(passed_tests) / len(self.test_cases) * 100 if self.test_cases else 0,
            'average_score': sum(scores) / len(scores) if scores else 0,
            'min_score': min(scores) if scores else 0,
            'max_score': max(scores) if scores else 0,
            'total_execution_time_ms': sum(r.execution_time_ms for r in results),
            'timestamp': datetime.now().isoformat()
        }
        
        # Print summary
        print("\n" + "=" * 70)
        print("  TEST SUMMARY")
        print("=" * 70)
        print(f"  Total:  {summary['total_tests']}")
        print(f"  Passed: {summary['passed']} ✅")
        print(f"  Failed: {summary['failed']} ❌")
        print(f"  Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"  Average Score: {summary['average_score']:.1f}/100")
        print(f"  Score Range: {summary['min_score']} - {summary['max_score']}")
        print("=" * 70 + "\n")
        
        return {
            'results': results,
            'summary': summary,
            'failed_tests': [
                {
                    'id': r.test_case.id,
                    'question': r.test_case.question,
                    'expected': r.test_case.expected_answer,
                    'generated': r.generated_answer,
                    'score': r.similarity_score
                }
                for r in failed_tests
            ]
        }
    
    def run_category(self, category: str, verbose: bool = True) -> Dict:
        """
        Run tests only for a specific category.
        
        Args:
            category: Category name to filter by (partial match)
            verbose: If True, print results
            
        Returns:
            Test results for the category
        """
        filtered_cases = [
            tc for tc in self.test_cases 
            if category.lower() in tc.category.lower()
        ]
        
        original_cases = self.test_cases
        self.test_cases = filtered_cases
        results = self.run_all_tests(verbose=verbose)
        self.test_cases = original_cases
        
        return results


def test_functional():
    """
    Legacy function for backward compatibility.
    Runs the functional test suite with default settings.
    """
    suite = FunctionalTestSuite()
    suite.run_all_tests()


# Main execution
if __name__ == "__main__":
    test_functional()