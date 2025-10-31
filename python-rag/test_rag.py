"""
Test Script for OpenRouter RAG Service
Includes tests for OpenRouter API connection and RAG functionality
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import custom modules
from openrouter_client import OpenRouterClient
from knowledge_sync import KnowledgeSync

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openrouter_connection():
    """Test OpenRouter API connection with both models"""
    logger.info("Testing OpenRouter API connection...")
    
    try:
        # Initialize OpenRouter client
        client = OpenRouterClient(
            api_key=os.getenv('OPENROUTER_API_KEY', ''),
            primary_model=os.getenv('OPENROUTER_PRIMARY_MODEL', 'qwen/qwen-2.5-72b-instruct:free'),
            fallback_model=os.getenv('OPENROUTER_FALLBACK_MODEL', 'deepseek/deepseek-v3.1:free'),
            api_url=os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        )
        
        test_message = "Hello, this is a test message"
        
        # Test primary model
        logger.info(f"Testing primary model: {client.primary_model}")
        try:
            response1 = client.call_api([
                {"role": "user", "content": test_message}
            ], model=client.primary_model, max_tokens=50)
            logger.info(f"Primary model response: {response1['choices'][0]['message']['content'] if response1.get('choices') else 'No response'}")
            logger.info("Primary model test: PASSED")
        except Exception as e:
            logger.error(f"Primary model test failed: {e}")
            return False
        
        # Test fallback model
        logger.info(f"Testing fallback model: {client.fallback_model}")
        try:
            response2 = client.call_api([
                {"role": "user", "content": test_message}
            ], model=client.fallback_model, max_tokens=50)
            logger.info(f"Fallback model response: {response2['choices'][0]['message']['content'] if response2.get('choices') else 'No response'}")
            logger.info("Fallback model test: PASSED")
        except Exception as e:
            logger.error(f"Fallback model test failed: {e}")
            return False
            
        # Test fallback mechanism
        logger.info("Testing fallback mechanism...")
        try:
            # This should work with fallback if primary fails
            response3 = client.call_with_fallback([
                {"role": "user", "content": "What is 2+2?"}
            ])
            logger.info(f"Fallback mechanism response: {response3['choices'][0]['message']['content'] if response3.get('choices') else 'No response'}")
            logger.info("Fallback mechanism test: PASSED")
        except Exception as e:
            logger.error(f"Fallback mechanism test failed: {e}")
            return False
            
        logger.info("All OpenRouter connection tests PASSED")
        return True
        
    except Exception as e:
        logger.error(f"OpenRouter connection test failed: {e}")
        return False

def test_database_connection():
    """Test database connection for knowledge sync"""
    logger.info("Testing database connection...")
    
    try:
        # Initialize knowledge sync
        knowledge_sync = KnowledgeSync(
            db_host=os.getenv('SUPABASE_DB_HOST', 'your-supabase-host.supabase.co'),
            db_port=os.getenv('SUPABASE_DB_PORT', '5432'),
            db_name=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            db_user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            db_password=os.getenv('SUPABASE_DB_PASSWORD', 'your-database-password')
        )
        
        # Test connection
        conn = knowledge_sync.get_postgres_connection()
        conn.close()
        logger.info("Database connection test: PASSED")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def test_knowledge_sync():
    """Test knowledge sync functionality"""
    logger.info("Testing knowledge sync...")
    
    try:
        # Initialize knowledge sync
        knowledge_sync = KnowledgeSync(
            db_host=os.getenv('SUPABASE_DB_HOST', 'your-supabase-host.supabase.co'),
            db_port=os.getenv('SUPABASE_DB_PORT', '5432'),
            db_name=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            db_user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            db_password=os.getenv('SUPABASE_DB_PASSWORD', 'your-database-password')
        )
        
        # Test sync
        stats = knowledge_sync.sync_all(force=True)
        if stats.get("success"):
            logger.info(f"Knowledge sync test: PASSED - {stats}")
            return True
        else:
            logger.error(f"Knowledge sync test failed: {stats.get('error', 'Unknown error')}")
            return False
        
    except Exception as e:
        logger.error(f"Knowledge sync test failed: {e}")
        return False

def test_student_context():
    """Test student context retrieval"""
    logger.info("Testing student context retrieval...")
    
    try:
        # Initialize knowledge sync
        knowledge_sync = KnowledgeSync(
            db_host=os.getenv('SUPABASE_DB_HOST', 'your-supabase-host.supabase.co'),
            db_port=os.getenv('SUPABASE_DB_PORT', '5432'),
            db_name=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            db_user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            db_password=os.getenv('SUPABASE_DB_PASSWORD', 'your-database-password')
        )
        
        # Test with a sample student ID (you might need to adjust this)
        student_context = knowledge_sync.get_student_context(1)
        logger.info(f"Student context retrieval test: PASSED - Retrieved context for student")
        logger.info(f"Available assessments: {len(student_context.get('available_assessments', []))}")
        logger.info(f"Completed assessments: {len(student_context.get('completed_assessments', []))}")
        return True
        
    except Exception as e:
        logger.error(f"Student context retrieval test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("Starting RAG service tests...")
    
    tests = [
        ("OpenRouter Connection", test_openrouter_connection),
        ("Database Connection", test_database_connection),
        ("Knowledge Sync", test_knowledge_sync),
        ("Student Context", test_student_context)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if not result:
                logger.error(f"Test '{test_name}' FAILED")
            else:
                logger.info(f"Test '{test_name}' PASSED")
        except Exception as e:
            logger.error(f"Test '{test_name}' ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info("="*50)
    logger.info(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All tests PASSED! RAG service is ready.")
        return True
    else:
        logger.error(f"Some tests FAILED. Please check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)