"""
Test script for Unclear Query Clarification Feature
Tests AI clarification for ambiguous/unclear queries before redirecting to studies
"""
from intelligent_cutoff import IntelligentCutoff

def test_unclear_queries():
    cutoff = IntelligentCutoff()
    
    print("=" * 70)
    print("UNCLEAR QUERY CLARIFICATION - TEST SUITE")
    print("=" * 70)
    print()
    
    # Test cases: (query, expected_unclear, description)
    test_cases = [
        # UNCLEAR queries (should trigger clarification)
        ("what about", True, "Very vague - no context"),
        ("tell me something", True, "Ambiguous request"),
        ("can you help", True, "Unclear what help is needed"),
        ("just curious", True, "No specific topic"),
        ("random stuff", True, "Vague and unclear"),
        ("things", True, "Too vague"),
        ("i want to know", True, "Incomplete thought"),
        ("wondering about", True, "No clear subject"),
        ("hi", True, "Too short, unclear intent"),
        ("ok", True, "Too short, unclear intent"),
        
        # CLEAR queries (should NOT trigger clarification)
        ("show me assessments", False, "Clear request"),
        ("what is my score", False, "Specific question"),
        ("how to prepare for interview", False, "Clear intent"),
        ("help me with coding", False, "Specific help request"),
        ("what is the passing score", False, "Specific question"),
        ("i want to take a test", False, "Clear action"),
        ("show my results", False, "Specific request"),
        ("how do i improve", False, "Clear goal"),
        
        # BORDERLINE queries (30-45% relevance - should clarify)
        ("tell me about programming", True, "Borderline relevance"),
        ("what about tests", True, "Borderline, vague"),
        ("can you explain", True, "Incomplete, borderline"),
    ]
    
    passed = 0
    failed = 0
    
    print("Testing Unclear Query Detection:")
    print("-" * 70)
    
    for query, expected_unclear, description in test_cases:
        relevance_score = cutoff.calculate_relevance_score(query)
        is_unclear = cutoff.is_unclear_query(query, relevance_score)
        
        # Check if result matches expectation
        if is_unclear == expected_unclear:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | Score: {relevance_score:3d}% | Unclear: {str(is_unclear):5} | {description}")
        print(f"       Query: \"{query}\"")
        print()
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    print()
    
    # Test clarification messages
    print("=" * 70)
    print("TESTING CLARIFICATION MESSAGES")
    print("=" * 70)
    print()
    
    # Mock student contexts
    student_contexts = [
        {
            "name": "Beginner",
            "student_info": {"name": "John"},
            "completed_assessments": [],
            "available_assessments": [
                {"title": "Python Basics"},
                {"title": "Aptitude Test"}
            ],
            "performance_summary": {"average_percentage": 0}
        },
        {
            "name": "Active Student",
            "student_info": {"name": "Sarah"},
            "completed_assessments": [1, 2],
            "available_assessments": [
                {"title": "Advanced Java"}
            ],
            "performance_summary": {"average_percentage": 65}
        }
    ]
    
    unclear_queries = [
        "what about",
        "tell me something",
        "just curious",
        "random stuff"
    ]
    
    for context in student_contexts:
        print(f"\n{context['name']} Context:")
        print("-" * 70)
        
        for query in unclear_queries[:2]:  # Test 2 queries per context
            message = cutoff.generate_clarification_message(query, context)
            print(f"\nQuery: \"{query}\"")
            print(f"Response:\n{message}")
            print()
    
    # Test the full flow
    print("=" * 70)
    print("TESTING FULL FLOW (Unclear → Clarify → Redirect)")
    print("=" * 70)
    print()
    
    test_query = "tell me something"
    context = student_contexts[0]
    
    print(f"Query: \"{test_query}\"")
    print()
    
    # Step 1: Calculate relevance
    relevance_score = cutoff.calculate_relevance_score(test_query)
    print(f"Step 1 - Relevance Score: {relevance_score}%")
    
    # Step 2: Check if unclear
    is_unclear = cutoff.is_unclear_query(test_query, relevance_score)
    print(f"Step 2 - Is Unclear: {is_unclear}")
    
    # Step 3: Generate clarification
    if is_unclear:
        clarification = cutoff.generate_clarification_message(test_query, context)
        print(f"Step 3 - Clarification Message:")
        print(clarification)
        
        suggestions = cutoff.get_study_suggestions(context)
        print(f"\nStep 4 - Study Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    
    print()
    print("=" * 70)
    print("EXPECTED BEHAVIOR:")
    print("=" * 70)
    print("""
1. Unclear queries (vague, ambiguous) are detected
2. System acknowledges what student asked
3. Politely explains focus should be on placement prep
4. Redirects to studies with actionable suggestions
5. Maintains friendly, helpful tone
    """)

if __name__ == "__main__":
    test_unclear_queries()
