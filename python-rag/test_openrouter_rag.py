"""
Comprehensive Test Suite for OpenRouter RAG System
Tests RAG functionality, status indicators, and database integration
"""
import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Back, Style

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
RAG_SERVICE_URL = "http://localhost:8001"
STUDENT_ID = 1  # Test student ID

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Back.CYAN}{Fore.BLACK} {text} {Style.RESET_ALL}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_status(emoji, text):
    """Print status with emoji"""
    print(f"{emoji} {text}")

def test_health_check():
    """Test 1: Health Check"""
    print_header("Test 1: Health Check")
    
    try:
        response = requests.get(f"{RAG_SERVICE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("RAG service is healthy")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Database: {data.get('database')}")
            print_info(f"Primary Model: {data.get('primary_model')}")
            print_info(f"Fallback Model: {data.get('fallback_model')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to RAG service. Is it running?")
        print_info("Start it with: python main.py")
        return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_root_endpoint():
    """Test 2: Root Endpoint"""
    print_header("Test 2: Root Endpoint")
    
    try:
        response = requests.get(f"{RAG_SERVICE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Root endpoint accessible")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Provider: {data.get('provider')}")
            return True
        else:
            print_error(f"Root endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint error: {e}")
        return False

def test_chat_query(query, expected_type=None):
    """Test chat query and return response"""
    print_info(f"Query: \"{query}\"")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{RAG_SERVICE_URL}/chat",
            json={
                "student_id": STUDENT_ID,
                "message": query,
                "student_name": "Test Student",
                "student_email": "test@student.com"
            },
            timeout=30
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Check RAG status
            rag_status = data.get('rag_status', 'unknown')
            model_used = data.get('model_used', 'unknown')
            query_type = data.get('query_type', 'unknown')
            
            # Display status with emoji
            service_info = data.get('service_info', {})
            status_emoji = service_info.get('indicator', '⚪')
            status_text = service_info.get('text', 'Unknown')
            
            print_status(status_emoji, f"Status: {status_text}")
            print_info(f"Model: {model_used}")
            print_info(f"Query Type: {query_type}")
            print_info(f"Response Time: {elapsed_time:.2f}s")
            
            # Print response message (truncated)
            message = data.get('message', '')
            if len(message) > 150:
                print_info(f"Response: {message[:150]}...")
            else:
                print_info(f"Response: {message}")
            
            # Print actions if available
            actions = data.get('actions', [])
            if actions:
                print_info(f"Actions: {len(actions)} available")
            
            # Verify expected type if provided
            if expected_type and query_type != expected_type:
                print_error(f"Expected query type '{expected_type}' but got '{query_type}'")
                return False
            
            print_success("Query successful")
            return True
        else:
            print_error(f"Query failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Query error: {e}")
        return False

def test_assessment_queries():
    """Test 3: Assessment Queries"""
    print_header("Test 3: Assessment Queries")
    
    queries = [
        ("What assessments are available?", "assessments"),
        ("Show me all tests", "assessments"),
        ("Are there any exams I can take?", "assessments"),
    ]
    
    results = []
    for query, expected_type in queries:
        result = test_chat_query(query, expected_type)
        results.append(result)
        time.sleep(1)  # Small delay between requests
    
    return all(results)

def test_result_queries():
    """Test 4: Result Queries"""
    print_header("Test 4: Result Queries")
    
    queries = [
        ("Show my results", "results"),
        ("What's my score?", "results"),
        ("How did I perform?", "results"),
    ]
    
    results = []
    for query, expected_type in queries:
        result = test_chat_query(query, expected_type)
        results.append(result)
        time.sleep(1)
    
    return all(results)

def test_help_queries():
    """Test 5: Help Queries"""
    print_header("Test 5: Help Queries")
    
    queries = [
        ("How do I take a test?", "help"),
        ("Guide me through the portal", "help"),
        ("I need help", "help"),
    ]
    
    results = []
    for query, expected_type in queries:
        result = test_chat_query(query, expected_type)
        results.append(result)
        time.sleep(1)
    
    return all(results)

def test_general_queries():
    """Test 6: General Queries"""
    print_header("Test 6: General Queries")
    
    queries = [
        "Hello",
        "What is this portal?",
        "Tell me about placement training",
    ]
    
    results = []
    for query in queries:
        result = test_chat_query(query)
        results.append(result)
        time.sleep(1)
    
    return all(results)

def test_rag_status_indicators():
    """Test 7: RAG Status Indicators"""
    print_header("Test 7: RAG Status Indicators")
    
    print_info("Testing various queries to verify status indicators...")
    
    test_queries = [
        "Show available assessments",  # Should trigger RAG
        "My results",  # Should trigger RAG
    ]
    
    for query in test_queries:
        print(f"\n{Fore.YELLOW}Testing: {query}{Style.RESET_ALL}")
        test_chat_query(query)
        time.sleep(1)
    
    print_success("Status indicator test complete")
    return True

def test_models_endpoint():
    """Test 8: Models Endpoint"""
    print_header("Test 8: Models Configuration")
    
    try:
        response = requests.get(f"{RAG_SERVICE_URL}/models", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Models endpoint accessible")
            print_info(f"Primary: {data.get('primary_model')}")
            print_info(f"Fallback: {data.get('fallback_model')}")
            print_info(f"API URL: {data.get('api_url')}")
            return True
        else:
            print_error(f"Models endpoint failed")
            return False
    except Exception as e:
        print_error(f"Models endpoint error: {e}")
        return False

def run_all_tests():
    """Run all tests and display summary"""
    print(f"\n{Back.MAGENTA}{Fore.WHITE} OpenRouter RAG Test Suite {Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing RAG service at: {RAG_SERVICE_URL}{Style.RESET_ALL}\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Models Configuration", test_models_endpoint),
        ("Assessment Queries", test_assessment_queries),
        ("Result Queries", test_result_queries),
        ("Help Queries", test_help_queries),
        ("General Queries", test_general_queries),
        ("RAG Status Indicators", test_rag_status_indicators),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)  # Small delay between tests
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    if passed == total:
        print(f"{Fore.GREEN}All tests passed! ({passed}/{total}){Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Tests passed: {passed}/{total}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    # Display RAG status legend
    print_header("RAG Status Indicators")
    print_status("🟢", "RAG Active (Primary Model - Qwen 2.5 72B)")
    print_status("🟡", "RAG Active (Fallback Model - DeepSeek V3.1)")
    print_status("🟠", "Database Only (No AI)")
    print_status("🔴", "Offline Mode (Static Responses)")
    print()

if __name__ == "__main__":
    run_all_tests()

