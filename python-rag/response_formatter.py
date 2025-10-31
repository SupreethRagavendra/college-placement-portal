"""
Response Formatter for OpenRouter Models
Formats API responses into structured JSON for the frontend
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ResponseFormatter:
    def __init__(self):
        pass
    
    def format_response(self, message: str, data: Dict[str, Any], query_type: str, 
                       student_id: int, model_used: Optional[str] = None) -> Dict[str, Any]:
        """
        Format the response from OpenRouter into a structured JSON response
        """
        try:
            # Check for special action requests (like name updates)
            special_action = self._extract_special_action(message, query_type)
            
            # Log name change detection
            if query_type == "name_change":
                logger.info(f"🔍 NAME CHANGE PROCESSING - Student {student_id}")
                logger.info(f"   Query Type: {query_type}")
                logger.info(f"   Message: {message[:200]}...")  # First 200 chars
                logger.info(f"   Special Action Extracted: {special_action}")
            
            # Parse any data tables or structured information from the message
            parsed_data = self._parse_message_for_data(message, data)
            
            # Generate follow-up questions based on query_type
            follow_up_questions = self._generate_follow_up_questions(query_type)
            
            # Generate actions based on context
            actions = self._generate_actions(query_type, data)
            
            # Determine RAG status from model
            rag_status = self._get_rag_status(model_used)
            
            # Create the response structure
            response = {
                "success": True,
                "message": message,
                "data": parsed_data,
                "actions": actions,
                "follow_up_questions": follow_up_questions,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "query_type": query_type,
                "model_used": "Campus AI",  # Hide technical model names - user-friendly
                "rag_status": rag_status,
                "service_info": {
                    "indicator": self._get_status_emoji(rag_status),
                    "text": self._get_status_text(rag_status)
                }
            }
            
            # Add special action if detected
            if special_action:
                response["special_action"] = special_action
                logger.info(f"✅ SPECIAL ACTION ADDED TO RESPONSE: {special_action}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            # Return a basic response if formatting fails
            return {
                "success": True,
                "message": message,
                "data": data,
                "actions": [],
                "follow_up_questions": [],
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "query_type": query_type,
                "model_used": "Campus AI"  # Hide technical model names
            }
    
    def _parse_message_for_data(self, message: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the message for any structured data like tables or lists
        """
        parsed_data = data.copy() if data else {}
        
        # Add any assessments data if available
        if 'assessments' in parsed_data:
            parsed_data['assessments'] = self._format_assessments_data(parsed_data['assessments'])
        
        # Add any results data if available
        if 'results' in parsed_data:
            parsed_data['results'] = self._format_results_data(parsed_data['results'])
        
        return parsed_data
    
    def _format_assessments_data(self, assessments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format assessments data for better presentation
        """
        formatted = []
        for assessment in assessments:
            formatted_assessment = {
                "id": assessment.get("id"),
                "title": assessment.get("title") or assessment.get("name"),
                "description": assessment.get("description"),
                "category": assessment.get("category", "General"),
                "duration": f"{assessment.get('total_time', assessment.get('duration', 30))} minutes",
                "questions_count": assessment.get("questions_count", "N/A")
            }
            formatted.append(formatted_assessment)
        return formatted
    
    def _format_results_data(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format results data for better presentation
        """
        formatted = []
        for result in results:
            formatted_result = {
                "assessment_id": result.get("assessment_id"),
                "title": result.get("title") or result.get("assessment_name"),
                "score": result.get("score"),
                "total": result.get("total"),
                "percentage": result.get("percentage"),
                "status": result.get("status", "N/A"),
                "completed_at": result.get("completed_at")
            }
            formatted.append(formatted_result)
        return formatted
    
    def _generate_follow_up_questions(self, query_type: str) -> List[str]:
        """
        Generate relevant follow-up questions based on the query type
        """
        follow_ups = {
            "assessments": [
                "How do I start taking an assessment?",
                "What is the passing criteria for assessments?",
                "Can I review my previous attempts?"
            ],
            "results": [
                "How can I improve my scores?",
                "Which assessments should I focus on?",
                "Are there any study materials available?"
            ],
            "help": [
                "How do I navigate the portal?",
                "Where can I find my assessment history?",
                "How do I contact support if I need help?"
            ],
            "general": [
                "What assessments are available right now?",
                "How do I view my performance statistics?",
                "Where can I find study resources?"
            ]
        }
        
        return follow_ups.get(query_type, [
            "What else would you like to know?",
            "Do you need help with anything else?",
            "Is there anything specific you'd like assistance with?"
        ])
    
    def _generate_actions(self, query_type: str, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate relevant actions based on the query type and data
        """
        actions = []
        
        if query_type == "assessments":
            # Add action to view assessments
            actions.append({
                "label": "View Available Assessments",
                "url": "/student/assessments"
            })
            
            # If there are completed assessments, add action to view results
            if data.get('completed_assessments'):
                actions.append({
                    "label": "View My Results",
                    "url": "/student/results"
                })
        
        elif query_type == "results":
            # Add action to view detailed results
            actions.append({
                "label": "View Detailed Results",
                "url": "/student/results"
            })
            
            # Add action to take new assessments
            actions.append({
                "label": "Take New Assessment",
                "url": "/student/assessments"
            })
        
        elif query_type == "help":
            # Add general navigation actions
            actions.extend([
                {
                    "label": "Go to Dashboard",
                    "url": "/student/dashboard"
                },
                {
                    "label": "View Profile",
                    "url": "/student/profile"
                }
            ])
        
        # Always add a general help action
        actions.append({
            "label": "Need More Help?",
            "url": "/student/support"
        })
        
        return actions
    
    def _get_rag_status(self, model_used: Optional[str]) -> str:
        """Determine RAG status from model used - Returns user-friendly name"""
        if not model_used or model_used == 'unknown':
            return 'offline'
        elif 'qwen' in model_used.lower():
            return 'Campus AI'  # Hide technical model name - user-friendly
        elif 'deepseek' in model_used.lower():
            return 'Campus AI'  # Hide technical model name - user-friendly
        elif model_used == 'fallback':
            return 'Campus AI'  # Hide technical model name
        else:
            return 'operational'
    
    def _get_status_emoji(self, status: str) -> str:
        """Get emoji indicator for status"""
        emojis = {
            'qwen/qwen-2.5-72b-instruct:free': '🟢',
            'deepseek/deepseek-v3.1:free': '🟡',
            'fallback': '🟠',
            'offline': '🔴',
            'operational': '🟢',
            'degraded': '🟡',
            'error': '🔴'
        }
        return emojis.get(status, '⚪')
    
    def _get_status_text(self, status: str) -> str:
        """Get text description for status"""
        texts = {
            'qwen/qwen-2.5-72b-instruct:free': 'RAG Active (Primary)',
            'deepseek/deepseek-v3.1:free': 'RAG Active (Fallback)',
            'fallback': 'Database Only',
            'offline': 'Offline Mode',
            'operational': 'RAG Active',
            'degraded': 'Limited Mode',
            'error': 'Error Mode'
        }
        return texts.get(status, 'Unknown')
    
    def _extract_special_action(self, message: str, query_type: str) -> Optional[Dict[str, Any]]:
        """
        Extract special actions from AI responses (like name updates)
        Returns action dictionary if found, None otherwise
        """
        import re
        import json
        
        # Check for name change action
        if query_type == "name_change":
            # Try to extract JSON action from message
            json_match = re.search(r'\{[^}]*"action"\s*:\s*"update_name"[^}]*\}', message)
            if json_match:
                try:
                    action_data = json.loads(json_match.group(0))
                    return {
                        "type": "update_name",
                        "new_name": action_data.get("new_name", ""),
                        "requires_db_update": True
                    }
                except json.JSONDecodeError:
                    pass
            
            # Fallback: try to extract "to [Name]" pattern - support all name formats
            # Matches: "Supreeth Ragavendra S", "John Smith", "Alex", etc.
            name_match = re.search(r'updated your name to ([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*(?:\s+[A-Z])?)', message)
            if name_match:
                return {
                    "type": "update_name",
                    "new_name": name_match.group(1).strip(),
                    "requires_db_update": True
                }
            
            # Additional fallback: try to extract name from "I've updated" pattern
            name_match2 = re.search(r"I['\']ve updated your name to ([^.!✓]+)", message)
            if name_match2:
                return {
                    "type": "update_name",
                    "new_name": name_match2.group(1).strip(),
                    "requires_db_update": True
                }
        
        return None