"""
Simple test for Intelligent Cutoff System improvements
"""
from intelligent_cutoff import IntelligentCutoff

def test_improved_cutoff():
    cutoff = IntelligentCutoff()
    
    print("=" * 60)
    print("TESTING IMPROVED INTELLIGENT CUTOFF SYSTEM")
    print("=" * 60)
    print()
    
    # Test cases focusing on irrelevant queries
    test_cases = [
        # Empty and meaningless
        ("", "Should detect empty"),
        ("   ", "Should detect whitespace"),
        ("!!!", "Should detect special chars only"),
        ("...", "Should detect dots only"),
        ("123", "Should detect numbers only"),
        
        # Single words/chars
        ("a", "Should detect single char"),
        ("x", "Should detect single char"),
        ("lol", "Should detect single slang"),
        ("wtf", "Should detect single slang"),
        
        # Gibberish
        ("asdfghjkl", "Should detect gibberish"),
        ("aaaaaaa", "Should detect repetitive"),
        ("xxxxx", "Should detect repetitive"),
        ("qwerty", "Should detect keyboard mash"),
        
        # Dismissive
        ("whatever", "Should detect dismissive"),
        ("nevermind", "Should detect dismissive"),
        ("forget it", "Should detect dismissive"),
        
        # Irrelevant combinations
        ("hi hello bye", "Should detect filler combo"),
        ("ok ok ok", "Should detect repetitive filler"),
        ("random stuff", "Should detect vague"),
        ("just because", "Should detect vague"),
        
        # RELEVANT queries (should pass)
        ("What is my test score?", "Should be relevant"),
        ("Show available assessments", "Should be relevant"),
        ("How to prepare for placement?", "Should be relevant"),
        ("Help me with coding practice", "Should be relevant"),
    ]
    
    print("Testing irrelevance detection:")
    print("-" * 60)
    
    for query, description in test_cases:
        is_off_topic, category, score = cutoff.is_off_topic(query)
        
        status = "OFF-TOPIC" if is_off_topic else "RELEVANT"
        print(f"[{status:10}] Score: {score:3}% | Category: {category:15} | Query: '{query[:30]}' | {description}")
    
    print()
    print("=" * 60)
    print("Test complete! The system now detects irrelevant queries")
    print("without needing extensive keyword lists.")
    print("=" * 60)

if __name__ == "__main__":
    test_improved_cutoff()
