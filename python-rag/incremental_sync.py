"""
Incremental Update System
Handles incremental updates to the knowledge base when admin adds/modifies data
"""
import logging
from datetime import datetime
import psycopg2
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IncrementalSync:
    def __init__(self, db_host: str, db_port: str, db_name: str, db_user: str, db_password: str):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.last_sync_timestamp = None
    
    def get_postgres_connection(self):
        """Create and return a PostgreSQL connection"""
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def sync_incremental_changes(self) -> Dict[str, Any]:
        """
        Check for and sync incremental changes since last sync
        """
        logger.info("Starting incremental sync")
        stats = {
            "new_assessments": 0,
            "updated_assessments": 0,
            "deleted_assessments": 0,
            "new_questions": 0,
            "updated_questions": 0,
            "new_categories": 0,
            "start_time": datetime.utcnow().isoformat() + "Z"
        }
        
        try:
            conn = self.get_postgres_connection()
            cursor = conn.cursor()
            
            # Get last sync timestamp
            last_sync = self.last_sync_timestamp or datetime.min
            
            # Sync new assessments
            new_assessments = self._sync_new_assessments(cursor, last_sync)
            stats["new_assessments"] = len(new_assessments)
            
            # Sync updated assessments
            updated_assessments = self._sync_updated_assessments(cursor, last_sync)
            stats["updated_assessments"] = len(updated_assessments)
            
            # Sync new questions
            new_questions = self._sync_new_questions(cursor, last_sync)
            stats["new_questions"] = len(new_questions)
            
            # Sync updated questions
            updated_questions = self._sync_updated_questions(cursor, last_sync)
            stats["updated_questions"] = len(updated_questions)
            
            # Sync new categories
            new_categories = self._sync_new_categories(cursor, last_sync)
            stats["new_categories"] = len(new_categories)
            
            conn.close()
            
            self.last_sync_timestamp = datetime.utcnow()
            stats["end_time"] = self.last_sync_timestamp.isoformat() + "Z"
            stats["success"] = True
            
            logger.info(f"Incremental sync completed: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Incremental sync failed: {e}")
            stats["success"] = False
            stats["error"] = str(e)
            stats["end_time"] = datetime.utcnow().isoformat() + "Z"
            return stats
    
    def _sync_new_assessments(self, cursor, since_timestamp) -> list:
        """Sync newly created assessments"""
        try:
            cursor.execute("""
                SELECT id, name, description, category, created_at
                FROM assessments 
                WHERE is_active = true 
                AND created_at > %s
                ORDER BY created_at DESC
            """, (since_timestamp,))
            
            new_assessments = cursor.fetchall()
            logger.info(f"Found {len(new_assessments)} new assessments")
            return new_assessments
            
        except Exception as e:
            logger.error(f"Failed to sync new assessments: {e}")
            return []
    
    def _sync_updated_assessments(self, cursor, since_timestamp) -> list:
        """Sync updated assessments"""
        try:
            cursor.execute("""
                SELECT id, name, description, category, updated_at
                FROM assessments 
                WHERE is_active = true 
                AND updated_at > %s
                AND created_at <= %s
                ORDER BY updated_at DESC
            """, (since_timestamp, since_timestamp))
            
            updated_assessments = cursor.fetchall()
            logger.info(f"Found {len(updated_assessments)} updated assessments")
            return updated_assessments
            
        except Exception as e:
            logger.error(f"Failed to sync updated assessments: {e}")
            return []
    
    def _sync_new_questions(self, cursor, since_timestamp) -> list:
        """Sync newly created questions"""
        try:
            cursor.execute("""
                SELECT id, question, category, difficulty_level, created_at
                FROM questions 
                WHERE is_active = true 
                AND created_at > %s
                ORDER BY created_at DESC
            """, (since_timestamp,))
            
            new_questions = cursor.fetchall()
            logger.info(f"Found {len(new_questions)} new questions")
            return new_questions
            
        except Exception as e:
            logger.error(f"Failed to sync new questions: {e}")
            return []
    
    def _sync_updated_questions(self, cursor, since_timestamp) -> list:
        """Sync updated questions"""
        try:
            cursor.execute("""
                SELECT id, question, category, difficulty_level, updated_at
                FROM questions 
                WHERE is_active = true 
                AND updated_at > %s
                AND created_at <= %s
                ORDER BY updated_at DESC
            """, (since_timestamp, since_timestamp))
            
            updated_questions = cursor.fetchall()
            logger.info(f"Found {len(updated_questions)} updated questions")
            return updated_questions
            
        except Exception as e:
            logger.error(f"Failed to sync updated questions: {e}")
            return []
    
    def _sync_new_categories(self, cursor, since_timestamp) -> list:
        """Sync newly created categories"""
        try:
            # Get categories from assessments created since last sync
            cursor.execute("""
                SELECT DISTINCT category
                FROM assessments 
                WHERE is_active = true 
                AND created_at > %s
                UNION
                SELECT DISTINCT category
                FROM questions 
                WHERE is_active = true 
                AND created_at > %s
            """, (since_timestamp, since_timestamp))
            
            new_categories = cursor.fetchall()
            logger.info(f"Found {len(new_categories)} new categories")
            return new_categories
            
        except Exception as e:
            logger.error(f"Failed to sync new categories: {e}")
            return []

# Update the KnowledgeSync class to include incremental sync functionality
def update_knowledge_sync_with_incremental():
    """
    This function shows how to extend the KnowledgeSync class with incremental sync
    In practice, this would be integrated directly into the KnowledgeSync class
    """
    pass