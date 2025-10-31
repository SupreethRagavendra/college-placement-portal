"""
Test Script for RAG System
Tests vector database, embeddings, conversation memory, and caching
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def print_header(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)

def test_health_check():
    """Test health check endpoint"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"[OK] Service Status: {data.get('status')}")
            print(f"[OK] Database: {data.get('database')}")
            print(f"[OK] Primary Model: {data.get('primary_model')}")
            print(f"[OK] Fallback Model: {data.get('fallback_model')}")
            return True
        else:
            print(f"[FAIL] Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_knowledge_base_query():
    """Test RAG with knowledge base retrieval"""
    print_header("TEST 2: Knowledge Base Query (RAG)")
    
    test_queries = [
        {
            "query": "How do I start an assessment?",
            "expected_keywords": ["click", "start", "assessment"],
            "should_retrieve": True
        },
        {
            "query": "What are tips to improve aptitude scores?",
            "expected_keywords": ["practice", "math", "daily"],
            "should_retrieve": True
        },
        {
            "query": "Can I pause an assessment?",
            "expected_keywords": ["cannot", "pause", "one session"],
            "should_retrieve": True
        }
    ]
    
    for idx, test in enumerate(test_queries, 1):
        print(f"\n{idx}. Query: '{test['query']}'")
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json={
                "student_id": 1,
                "message": test["query"],
                "student_name": "Test Student",
                "student_email": "test@example.com"
            }, timeout=30)
            
            if response.ok:
                data = response.json()
                message = data.get('message', '')
                
                print(f"   Query Type: {data.get('query_type')}")
                print(f"   Model Used: {data.get('model_used')}")
                print(f"   From Cache: {data.get('from_cache', False)}")
                
                # Check if expected keywords are in response
                found_keywords = [kw for kw in test['expected_keywords'] if kw.lower() in message.lower()]
                
                if found_keywords:
                    print(f"   [OK] Found keywords: {', '.join(found_keywords)}")
                else:
                    print(f"   [WARN] Missing expected keywords")
                
                print(f"   Response preview: {message[:150]}...")
            else:
                print(f"   [FAIL] Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   [FAIL] Error: {e}")

def test_conversation_memory():
    """Test conversation memory and context"""
    print_header("TEST 3: Conversation Memory")
    
    conversation = [
        "Show available assessments",
        "Tell me more about the first one",  # Should reference previous message
        "What about the second assessment?"  # Should maintain context
    ]
    
    history = []
    
    for idx, query in enumerate(conversation, 1):
        print(f"\n{idx}. User: '{query}'")
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json={
                "student_id": 1,
                "message": query,
                "student_name": "Test Student",
                "conversation_history": history
            }, timeout=30)
            
            if response.ok:
                data = response.json()
                message = data.get('message', '')
                
                # Add to conversation history
                history.append({"role": "user", "content": query})
                history.append({"role": "assistant", "content": message})
                
                print(f"   Bot: {message[:200]}...")
                print(f"   History size: {len(history)} messages")
            else:
                print(f"   [FAIL] Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   [FAIL] Error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_caching():
    """Test response caching"""
    print_header("TEST 4: Response Caching")
    
    query = "What is the passing criteria?"
    
    print("First request (cache miss):")
    start = time.time()
    try:
        response1 = requests.post(f"{BASE_URL}/chat", json={
            "student_id": 1,
            "message": query
        }, timeout=30)
        time1 = time.time() - start
        
        if response1.ok:
            data1 = response1.json()
            print(f"   Response time: {time1:.2f}s")
            print(f"   From cache: {data1.get('from_cache', False)}")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
    
    print("\nSecond request (should be cached):")
    start = time.time()
    try:
        response2 = requests.post(f"{BASE_URL}/chat", json={
            "student_id": 1,
            "message": query
        }, timeout=30)
        time2 = time.time() - start
        
        if response2.ok:
            data2 = response2.json()
            print(f"   Response time: {time2:.2f}s")
            print(f"   From cache: {data2.get('from_cache', False)}")
            
            if data2.get('from_cache') and time2 < time1:
                print(f"   [OK] Cache working! Speed improvement: {((time1-time2)/time1*100):.1f}%")
            else:
                print(f"   [WARN] Cache may not be working as expected")
    except Exception as e:
        print(f"   [FAIL] Error: {e}")

def test_personalized_queries():
    """Test that personalized queries are not cached"""
    print_header("TEST 5: Personalized Queries (No Cache)")
    
    personalized_queries = [
        "Show my results",
        "What is my score?",
        "How am I doing?"
    ]
    
    for query in personalized_queries:
        print(f"\nQuery: '{query}'")
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json={
                "student_id": 1,
                "message": query
            }, timeout=30)
            
            if response.ok:
                data = response.json()
                from_cache = data.get('from_cache', False)
                print(f"   From cache: {from_cache}")
                
                if not from_cache:
                    print(f"   [OK] Correctly not cached (personalized query)")
                else:
                    print(f"   [WARN] Should not be cached!")
            else:
                print(f"   [FAIL] Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   [FAIL] Error: {e}")

def test_query_classification():
    """Test query type classification"""
    print_header("TEST 6: Query Classification")
    
    test_cases = [
        ("Hello", "greeting"),
        ("Show available assessments", "assessments"),
        ("What are my results?", "results"),
        ("How do I take a test?", "help"),
        ("Tips for aptitude", "general")
    ]
    
    for query, expected_type in test_cases:
        print(f"\nQuery: '{query}'")
        print(f"   Expected type: {expected_type}")
        
        try:
            response = requests.post(f"{BASE_URL}/chat", json={
                "student_id": 1,
                "message": query
            }, timeout=30)
            
            if response.ok:
                data = response.json()
                actual_type = data.get('query_type')
                print(f"   Actual type: {actual_type}")
                
                if actual_type == expected_type:
                    print(f"   [OK] Correct classification")
                else:
                    print(f"   [WARN] Classification mismatch")
            else:
                print(f"   [FAIL] Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   [FAIL] Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "RAG SYSTEM TEST SUITE" + "\n" + "="*60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n[WARN] Service is not healthy. Please start the RAG service.")
        print("Run: cd python-rag && python main.py")
        return
    
    time.sleep(1)
    
    # Test 2: Knowledge Base
    test_knowledge_base_query()
    time.sleep(2)
    
    # Test 3: Conversation Memory
    test_conversation_memory()
    time.sleep(2)
    
    # Test 4: Caching
    test_caching()
    time.sleep(2)
    
    # Test 5: Personalized Queries
    test_personalized_queries()
    time.sleep(2)
    
    # Test 6: Query Classification
    test_query_classification()
    
    print_header("TEST SUITE COMPLETE")
    print("Check the results above for any warnings or errors.")
    print("\nNext steps:")
    print("1. Run migrations: php artisan migrate")
    print("2. Initialize vector DB: cd python-rag && python init_vector_db.py")
    print("3. Start RAG service: cd python-rag && python main.py")
    print("4. Test chatbot in browser: http://localhost:8000")

if __name__ == "__main__":
    main()
