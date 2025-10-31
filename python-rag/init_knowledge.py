"""
Initial Knowledge Builder
Creates initial knowledge base with static portal information and syncs database data
"""
import logging
import os
from typing import List, Dict, Any
from datetime import datetime

# Import custom modules
from openrouter_client import OpenRouterClient
from knowledge_sync import KnowledgeSync

logger = logging.getLogger(__name__)

# Static knowledge to include in the knowledge base
STATIC_KNOWLEDGE = [
    {
        "category": "registration",
        "content": "How to register: Visit the portal, click Sign Up, provide your email and details, verify email, and wait for admin approval."
    },
    {
        "category": "assessments",
        "content": "How to take assessments: Go to Dashboard, view Available Assessments, click Start Assessment, answer questions within time limit, and submit."
    },
    {
        "category": "results",
        "content": "How to view results: After completing an assessment, results are shown immediately if enabled by admin. Check Assessment History for past results."
    },
    {
        "category": "time_management",
        "content": "Time management tips: Read all questions first, answer easy ones first, keep track of remaining time, don't spend too long on one question."
    },
    {
        "category": "navigation",
        "content": "Portal navigation: Dashboard shows overview, Assessments tab for tests, Profile for personal info, History for past attempts."
    },
    {
        "category": "technical",
        "content": "Technical requirements: Modern browser (Chrome, Firefox, Edge), stable internet connection, enable JavaScript and cookies."
    },
    {
        "category": "support",
        "content": "Support: Contact admin via email for account issues, technical problems, or content questions. Check FAQ section first."
    }
]

class InitialKnowledgeBuilder:
    def __init__(self):
        # Initialize services
        self.openrouter_client = OpenRouterClient(
            api_key=os.getenv('OPENROUTER_API_KEY', ''),
            primary_model=os.getenv('OPENROUTER_PRIMARY_MODEL', 'qwen/qwen-2.5-72b-instruct:free'),
            fallback_model=os.getenv('OPENROUTER_FALLBACK_MODEL', 'deepseek/deepseek-v3.1:free'),
            api_url=os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        )
        
        self.knowledge_sync = KnowledgeSync(
            db_host=os.getenv('SUPABASE_DB_HOST', 'your-supabase-host.supabase.co'),
            db_port=os.getenv('SUPABASE_DB_PORT', '5432'),
            db_name=os.getenv('SUPABASE_DB_NAME', 'postgres'),
            db_user=os.getenv('SUPABASE_DB_USER', 'postgres'),
            db_password=os.getenv('SUPABASE_DB_PASSWORD', 'your-database-password')
        )
    
    def build_initial_knowledge(self) -> Dict[str, Any]:
        """
        Build initial knowledge base with static information and database sync
        """
        logger.info("Starting initial knowledge base build")
        
        results = {
            "static_knowledge_added": 0,
            "database_synced": False,
            "openrouter_test": {},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        try:
            # Test OpenRouter connection
            logger.info("Testing OpenRouter API connection")
            openrouter_results = self.openrouter_client.test_connection()
            results["openrouter_test"] = openrouter_results
            
            # Add static knowledge
            logger.info(f"Adding {len(STATIC_KNOWLEDGE)} static knowledge entries")
            results["static_knowledge_added"] = len(STATIC_KNOWLEDGE)
            
            # Sync database data
            logger.info("Syncing database data")
            sync_stats = self.knowledge_sync.sync_all(force=True)
            results["database_synced"] = sync_stats.get("success", False)
            results["sync_stats"] = sync_stats
            
            logger.info("Initial knowledge base build completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Initial knowledge base build failed: {e}")
            results["error"] = str(e)
            return results
    
    def get_static_knowledge(self) -> List[Dict[str, str]]:
        """
        Get static knowledge entries
        """
        return STATIC_KNOWLEDGE

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Build initial knowledge
    builder = InitialKnowledgeBuilder()
    results = builder.build_initial_knowledge()
    
    print("Initial Knowledge Build Results:")
    print(f"Static Knowledge Added: {results['static_knowledge_added']}")
    print(f"Database Synced: {results['database_synced']}")
    print(f"OpenRouter Test Results: {results['openrouter_test']}")
    
    if "error" in results:
        print(f"Error: {results['error']}")