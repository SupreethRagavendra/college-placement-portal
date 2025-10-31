"""
Test AI Contextual Redirect for Irrelevant Queries
Shows how the system acknowledges keywords and redirects to studies
"""
from intelligent_cutoff import IntelligentCutoff

def test_redirect_messages():
    cutoff = IntelligentCutoff()
    
    print("=" * 70)
    print("AI CONTEXTUAL REDIRECT - Expected Behavior")
    print("=" * 70)
    print()
    
    # Mock student context
    student_context = {
        'student_info': {'name': 'Rahul'},
        'available_assessments': [{'title': 'Python Test'}, {'title': 'Java Test'}, {'title': 'Aptitude Test'}],
        'completed_assessments': [{'title': 'SQL Test'}],
        'performance_summary': {'average_percentage': 65.0}
    }
    
    print("Student Context:")
    print(f"  Name: {student_context['student_info']['name']}")
    print(f"  Available Assessments: {len(student_context['available_assessments'])}")
    print(f"  Completed: {len(student_context['completed_assessments'])}")
    print(f"  Average Score: {student_context['performance_summary']['average_percentage']}%")
    print()
    print("=" * 70)
    print()
    
    # Test cases showing expected AI behavior
    test_cases = [
        {
            'query': 'fool',
            'expected_style': 'Acknowledge "fool" and redirect to studies',
            'ai_example': 'Hello Rahul, it seems like you entered a term unrelated to your placement training. How can I assist you with your studies today?'
        },
        {
            'query': 'I want to play games',
            'expected_style': 'Acknowledge "games" and redirect',
            'ai_example': 'Hmm, games sound interesting! But let\'s stay focused on your studies for now. You have 3 assessments waiting!'
        },
        {
            'query': 'what about movies?',
            'expected_style': 'Acknowledge "movies" and redirect',
            'ai_example': 'Movies are fun, but we should concentrate on your learning goals right now. How about tackling one of your 3 available assessments?'
        },
        {
            'query': 'cricket match',
            'expected_style': 'Acknowledge "cricket" and redirect',
            'ai_example': 'I see you mentioned cricket, but let\'s get back to your placement preparation! Your current average is 65% - let\'s improve it!'
        },
        {
            'query': '',
            'expected_style': 'Handle empty message',
            'ai_example': 'I noticed you sent an empty message. Let me help you with your placement preparation instead!'
        },
        {
            'query': 'whatever',
            'expected_style': 'Acknowledge dismissive tone and motivate',
            'ai_example': 'Don\'t give up! Your placement preparation is important. You have 3 assessments ready - let\'s tackle one together!'
        }
    ]
    
    print("EXPECTED AI BEHAVIOR:")
    print("-" * 70)
    print()
    
    for i, test in enumerate(test_cases, 1):
        query = test['query']
        is_off_topic, category, score = cutoff.is_off_topic(query if query else " ")
        
        print(f"{i}. Student says: \"{query}\"")
        print(f"   Detection: {'OFF-TOPIC' if is_off_topic else 'RELEVANT'} (score: {score}%, category: {category})")
        print(f"   Expected Style: {test['expected_style']}")
        print(f"   AI Example: \"{test['ai_example']}\"")
        print()
    
    print("=" * 70)
    print("SYSTEM BEHAVIOR:")
    print("=" * 70)
    print()
    print("1. When AI API is available:")
    print("   ✓ AI reads the student's exact message")
    print("   ✓ AI uses the keyword/topic naturally in response")
    print("   ✓ AI gently redirects to studies with positive tone")
    print("   ✓ AI mentions specific actions (e.g., '3 assessments available')")
    print()
    print("2. When AI API fails (rate limit, error):")
    print("   ✓ System automatically falls back to template messages")
    print("   ✓ Still provides personalized redirect based on context")
    print("   ✓ Includes study suggestions")
    print()
    print("3. Template fallback example:")
    fallback_msg = cutoff.generate_redirect_message('games', 'entertainment', student_context)
    print(f"   {fallback_msg[:150]}...")
    print()
    print("=" * 70)

if __name__ == "__main__":
    test_redirect_messages()
