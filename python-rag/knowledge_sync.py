"""
Knowledge Sync System
Handles synchronization of data from Supabase PostgreSQL to the RAG system
"""
import psycopg2
import logging
from typing import Dict, Any, List
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class KnowledgeSync:
    def __init__(self, db_host: str, db_port: str, db_name: str, db_user: str, db_password: str):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.last_sync = None
        
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
    
    def sync_all(self, force: bool = False) -> Dict[str, Any]:
        """
        Sync all knowledge from database
        """
        logger.info("Starting knowledge sync")
        stats = {
            "assessments_synced": 0,
            "questions_synced": 0,
            "categories_synced": 0,
            "start_time": datetime.utcnow().isoformat() + "Z"
        }
        
        try:
            conn = self.get_postgres_connection()
            cursor = conn.cursor()
            
            # Sync assessments
            assessments_count = self._sync_assessments(cursor)
            stats["assessments_synced"] = assessments_count
            
            # Sync questions
            questions_count = self._sync_questions(cursor)
            stats["questions_synced"] = questions_count
            
            # Sync categories
            categories_count = self._sync_categories(cursor)
            stats["categories_synced"] = categories_count
            
            conn.close()
            
            self.last_sync = datetime.utcnow()
            stats["end_time"] = self.last_sync.isoformat() + "Z"
            stats["success"] = True
            
            logger.info(f"Knowledge sync completed: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Knowledge sync failed: {e}")
            stats["success"] = False
            stats["error"] = str(e)
            stats["end_time"] = datetime.utcnow().isoformat() + "Z"
            return stats
    
    def _sync_assessments(self, cursor) -> int:
        """Sync assessments from database"""
        try:
            cursor.execute("""
                SELECT id, name, description, category, created_at, updated_at
                FROM assessments 
                WHERE is_active = true
                ORDER BY created_at DESC
            """)
            
            assessments = cursor.fetchall()
            logger.info(f"Synced {len(assessments)} assessments")
            return len(assessments)
            
        except Exception as e:
            logger.error(f"Failed to sync assessments: {e}")
            return 0
    
    def _sync_questions(self, cursor) -> int:
        """Sync questions from database"""
        try:
            cursor.execute("""
                SELECT id, question, category_id, difficulty_level, created_at
                FROM questions 
                WHERE is_active = true
                ORDER BY created_at DESC
            """)
            
            questions = cursor.fetchall()
            logger.info(f"Synced {len(questions)} questions")
            return len(questions)
            
        except Exception as e:
            logger.error(f"Failed to sync questions: {e}")
            return 0
    
    def _sync_categories(self, cursor) -> int:
        """Sync categories from database"""
        try:
            cursor.execute("""
                SELECT DISTINCT category
                FROM assessments 
                WHERE is_active = true
                UNION
                SELECT c.name
                FROM categories c
                JOIN questions q ON q.category_id = c.id
                WHERE q.is_active = true
            """)
            
            categories = cursor.fetchall()
            logger.info(f"Synced {len(categories)} categories")
            return len(categories)
            
        except Exception as e:
            logger.error(f"Failed to sync categories: {e}")
            return 0
    
    def get_student_context(self, student_id: int) -> Dict[str, Any]:
        """
        Get comprehensive student context for RAG
        """
        try:
            conn = self.get_postgres_connection()
            cursor = conn.cursor()
            
            context = {}
            
            # Get student info
            cursor.execute("""
                SELECT id, name, email
                FROM users 
                WHERE id = %s
            """, (student_id,))
            
            student_row = cursor.fetchone()
            if student_row:
                context['student_info'] = {
                    'id': student_row[0],
                    'name': student_row[1],
                    'email': student_row[2]
                }
            
            # Get available assessments (exclude already taken by this student and soft-deleted)
            cursor.execute("""
                SELECT a.id, a.name, a.description, a.category, a.total_time, a.duration
                FROM assessments a
                WHERE a.is_active = true
                AND a.deleted_at IS NULL
                AND (a.start_date IS NULL OR a.start_date <= NOW())
                AND (a.end_date IS NULL OR a.end_date >= NOW())
                AND a.id NOT IN (
                    SELECT assessment_id 
                    FROM student_assessments 
                    WHERE student_id = %s
                )
                ORDER BY a.created_at DESC
            """, (student_id,))
            
            assessment_rows = cursor.fetchall()
            context['available_assessments'] = [
                {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'category': row[3],
                    'total_time': row[4] or row[5] or 30
                }
                for row in assessment_rows
            ]
            
            # Get completed assessments
            cursor.execute("""
                SELECT sa.assessment_id, sa.obtained_marks, sa.total_marks, sa.percentage, 
                       sa.pass_status, sa.submit_time, a.name, a.category
                FROM student_assessments sa
                JOIN assessments a ON sa.assessment_id = a.id
                WHERE sa.student_id = %s AND sa.status = 'completed'
                ORDER BY sa.submit_time DESC
            """, (student_id,))
            
            completed_rows = cursor.fetchall()
            context['completed_assessments'] = [
                {
                    'assessment_id': row[0],
                    'title': row[6],
                    'category': row[7],
                    'score': row[1],
                    'total': row[2],
                    'percentage': row[3],
                    'status': row[4],
                    'completed_at': row[5].isoformat() + "Z" if row[5] else None
                }
                for row in completed_rows
            ]
            
            # Get performance summary
            if context['completed_assessments']:
                percentages = [assess['percentage'] for assess in context['completed_assessments']]
                context['performance_summary'] = {
                    'total_completed': len(context['completed_assessments']),
                    'average_percentage': round(sum(percentages) / len(percentages), 1),
                    'highest_score': max(percentages),
                    'lowest_score': min(percentages),
                    'passed_count': len([assess for assess in context['completed_assessments'] if assess['status'] == 'pass']),
                    'failed_count': len([assess for assess in context['completed_assessments'] if assess['status'] == 'fail'])
                }
            else:
                context['performance_summary'] = {
                    'total_completed': 0,
                    'message': 'No assessments completed yet'
                }
            
            conn.close()
            return context
            
        except Exception as e:
            logger.error(f"Failed to get student context: {e}")
            raise