"""
Test script for Intelligent Cutoff System
Tests relevance scoring and off-topic detection
"""
from intelligent_cutoff import IntelligentCutoff

def test_cutoff():
    cutoff = IntelligentCutoff()
    
    print("=" * 60)
    print("INTELLIGENT CUTOFF SYSTEM - TEST SUITE")
    print("=" * 60)
    print()
    
    # Test cases: (query, expected_result)
    test_cases = [
        # OFF-TOPIC queries (should trigger cutoff)
        ("What's the best game to play?", True, "entertainment"),
        ("Have you seen the latest movie?", True, "entertainment"),
        ("Which Netflix series should I watch?", True, "entertainment"),
        ("How do I get a girlfriend?", True, "personal"),
        ("Who won the cricket match?", True, "sports"),
        ("What's the weather like?", True, "random"),
        ("I'm bored, tell me a joke", True, "casual_chat"),
        ("Let's talk about music", True, "entertainment"),
        ("I want to play PUBG", True, "entertainment"),
        
        # EMPTY/GIBBERISH queries (should trigger cutoff)
        ("", True, "empty_query"),
        ("   ", True, "empty_query"),
        ("a", True, "single_word"),
        ("x", True, "single_word"),
        ("!!!", True, "special_chars_only"),
        ("...", True, "special_chars_only"),
        ("lol", True, "single_word"),
        ("wtf", True, "single_word"),
        ("bruh", True, "single_word"),
        
        # NONSENSICAL queries (should trigger cutoff)
        ("bloody sweet", True, "low_relevance"),
        ("random stuff", True, "low_relevance"),
        ("whatever man", True, "low_relevance"),
        ("idk bro", True, "low_relevance"),
        ("just because", True, "low_relevance"),
        ("hi hello bye", True, "low_relevance"),
        ("ok ok ok", True, "low_relevance"),
        ("asdfghjkl", True, "low_relevance"),
        ("aaaaaaa", True, "low_relevance"),
        ("123456", True, "single_word"),
        
        # SLANG/CASUAL queries (should trigger cutoff)
        ("cool awesome nice", True, "low_relevance"),
        ("damn bro that's lit", True, "low_relevance"),
        ("yolo swag epic", True, "low_relevance"),
        
        # RELEVANT queries (should NOT trigger cutoff)
        ("Show me available assessments", False, "relevant"),
        ("What's my test score?", False, "relevant"),
        ("How do I prepare for placement?", False, "relevant"),
        ("Help me improve my coding skills", False, "relevant"),
        ("How do I take a test?", False, "relevant"),
        ("What is the passing score?", False, "relevant"),
        ("Can you explain algorithms?", False, "relevant"),
        ("I want to practice programming", False, "relevant"),
        ("Show my results", False, "relevant"),
        ("How to improve my performance?", False, "relevant"),
    ]
    
    passed = 0
    failed = 0
    
    for query, expected_off_topic, expected_category in test_cases:
        is_off_topic, category, relevance_score = cutoff.is_off_topic(query)
        
        # Check if result matches expectation
        if is_off_topic == expected_off_topic:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"{status} | Score: {relevance_score:3d}% | Off-topic: {is_off_topic:5} | {query[:50]}")
    
    print()
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 60)
    print()
    
    # Test redirect messages
    print("=" * 60)
    print("TESTING REDIRECT MESSAGES")
    print("=" * 60)
    print()
    
    # Mock student context
    student_contexts = [
        {
            "name": "Beginner",
            "student_info": {"name": "John"},
            "completed_assessments": [],
            "available_assessments": [{"title": "Test 1"}, {"title": "Test 2"}],
            "performance_summary": {"average_percentage": 0}
        },
        {
            "name": "Needs Improvement",
            "student_info": {"name": "Sarah"},
            "completed_assessments": [1, 2, 3],
            "available_assessments": [{"title": "Test 4"}],
            "performance_summary": {"average_percentage": 45}
        },
        {
            "name": "Good Performer",
            "student_info": {"name": "Mike"},
            "completed_assessments": [1, 2, 3, 4],
            "available_assessments": [{"title": "Test 5"}],
            "performance_summary": {"average_percentage": 72}
        },
        {
            "name": "Excellent Performer",
            "student_info": {"name": "Emma"},
            "completed_assessments": [1, 2, 3, 4, 5],
            "available_assessments": [{"title": "Test 6"}],
            "performance_summary": {"average_percentage": 88}
        }
    ]
    
    for context in student_contexts:
        print(f"\n{context['name']} ({context['performance_summary']['average_percentage']}%):")
        print("-" * 60)
        message = cutoff.generate_redirect_message(
            "What's the best game?",
            "entertainment",
            context
        )
        print(message)
        print()
    
    # Test study suggestions
    print("=" * 60)
    print("TESTING STUDY SUGGESTIONS")
    print("=" * 60)
    print()
    
    for context in student_contexts:
        suggestions = cutoff.get_study_suggestions(context)
        print(f"{context['name']}:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
        print()

if __name__ == "__main__":
    test_cutoff()
