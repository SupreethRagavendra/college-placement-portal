"""
Context Handler for OpenRouter RAG
Processes student queries with context and generates appropriate prompts
"""
import logging
from typing import Dict, Any, List, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class ContextHandler:
    def __init__(self, openrouter_client, vector_store=None):
        self.openrouter_client = openrouter_client
        self.vector_store = vector_store  # Add vector store for RAG
    
    def process_query(self, student_id: int, query: str, student_context: Dict[str, Any], 
                     student_email: Optional[str] = None, student_name: Optional[str] = None,
                     conversation_history: List[Dict] = None) -> Tuple[str, Dict[str, Any], str, str]:
        """
        Process a student query with context and generate response using OpenRouter with RAG
        Returns: (message, data, query_type, model_used)
        """
        try:
            # 1. Classify query type
            query_type = self._classify_query(query)
            logger.info(f"Query classified as: {query_type}")
            
            # 2. Search vector database for relevant knowledge (RAG component)
            retrieved_docs = []
            if self.vector_store:
                try:
                    search_results = self.vector_store.search(query, n_results=3)
                    retrieved_docs = search_results['documents'][0] if search_results['documents'] else []
                    if retrieved_docs:
                        logger.info(f"Retrieved {len(retrieved_docs)} relevant documents from knowledge base")
                except Exception as e:
                    logger.warning(f"Vector search failed: {e}")
            
            # 3. Build enhanced prompt with retrieved knowledge + conversation history
            prompt_messages = self._build_enhanced_prompt(
                query, student_context, query_type, 
                student_name, student_email,
                retrieved_docs, conversation_history or []
            )
            
            # 4. Call OpenRouter API with fallback
            response = self.openrouter_client.call_with_fallback(prompt_messages)
            
            # 5. Extract message and data
            message = response["choices"][0]["message"]["content"] if response.get("choices") else "No response generated"
            data = response.get("data", {})
            model_used = response.get("model_used", "unknown")
            
            # CRITICAL: Post-process ONLY for assessment queries to prevent hallucination
            if query_type == "assessments":
                logger.info(f"POST-PROCESSING [assessments]: Removing hallucinated data. Original: {len(message)} chars")
                message = self._remove_hallucinated_assessments(message, student_context)
                logger.info(f"POST-PROCESSING [assessments]: Clean message: {len(message)} chars")
            else:
                logger.info(f"QUERY TYPE [{query_type}]: No post-processing needed. Message: {len(message)} chars")
            
            return message, data, query_type, model_used
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    def _classify_query(self, query: str) -> str:
        """
        Classify the type of query based on keywords
        """
        query_lower = query.lower().strip()
        
        # OFF-TOPIC / IRRELEVANT queries (check FIRST to redirect students)
        off_topic_keywords = {
            'entertainment': ['game', 'gaming', 'video game', 'pubg', 'fortnite', 'minecraft', 'valorant', 'cod', 'gta', 'fifa', 'movie', 'film', 'netflix', 'series', 'tv show', 'youtube', 'tiktok', 'instagram', 'facebook', 'social media', 'twitter', 'music', 'song', 'spotify'],
            'personal': ['love', 'girlfriend', 'boyfriend', 'dating', 'relationship', 'crush', 'romance', 'marriage', 'wedding'],
            'sports': ['cricket', 'football', 'soccer', 'basketball', 'ipl', 'world cup', 'match', 'player', 'team sport'],
            'random': ['weather', 'food', 'recipe', 'cooking', 'travel', 'vacation', 'holiday', 'party', 'shopping', 'fashion', 'celebrity', 'gossip']
        }
        
        for category, keywords in off_topic_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                # Avoid false positives with placement/career terms
                if not any(career_term in query_lower for career_term in ["placement", "career", "job", "interview", "skill", "learning", "study"]):
                    return "off_topic"
        
        # Greeting queries (should be checked SECOND)
        greeting_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings", "yo", "sup", "hola"]
        # Check if it's JUST a greeting (short message, no other keywords)
        if any(greeting == query_lower or query_lower.startswith(greeting + " ") or query_lower.startswith(greeting + "!") for greeting in greeting_keywords):
            # Only classify as greeting if it doesn't contain data request keywords
            if not any(keyword in query_lower for keyword in ["assessment", "test", "exam", "result", "score", "available", "show", "what", "when", "where", "how"]):
                return "greeting"
        
        # Assessment-related queries (must be before "what" check)
        if any(keyword in query_lower for keyword in ["assessment", "test", "exam", "quiz", "available", "pending", "take test", "start test"]):
            return "assessments"
        
        # Results-related queries
        if any(keyword in query_lower for keyword in ["result", "score", "grade", "performance", "pass", "fail", "mark", "marks", "percentage"]):
            return "results"
        
        # Help/How-to queries  
        if any(keyword in query_lower for keyword in ["how to", "how do", "how can", "guide", "tutorial", "instructions", "steps to"]):
            return "help"
        
        # Name change requests (check before general profile)
        if any(keyword in query_lower for keyword in ["change my name", "update my name", "rename me", "my name is", "call me", "change name to", "update name to"]):
            return "name_change"
        
        # Profile/Account queries
        if any(keyword in query_lower for keyword in ["profile", "account", "password", "email", "settings", "update profile"]):
            return "profile"
        
        # General information queries (what/when/where/who/why)
        if any(keyword in query_lower for keyword in ["what is", "what are", "when is", "when are", "where is", "where are", "who is", "why is", "explain"]):
            return "general"
        
        # Thank you / feedback
        if any(keyword in query_lower for keyword in ["thank", "thanks", "appreciate", "helpful", "good", "great", "awesome"]):
            return "acknowledgment"
        
        # Default to general for anything else
        return "general"
    
    def _build_prompt(self, query: str, context: Dict[str, Any], query_type: str, 
                     student_name: Optional[str] = None, student_email: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Build an optimized prompt for OpenRouter models based on query type and context
        (Legacy method - use _build_enhanced_prompt for RAG)
        """
        # System prompt with student information
        system_prompt = self._build_system_prompt(context, student_name, student_email)
        
        # User prompt based on query type
        user_prompt = self._build_user_prompt(query, context, query_type)
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def _build_enhanced_prompt(self, query: str, context: Dict[str, Any], query_type: str, 
                               student_name: Optional[str], student_email: Optional[str],
                               retrieved_docs: List[str], conversation_history: List[Dict]) -> List[Dict[str, str]]:
        """
        Build enhanced prompt with RAG-retrieved knowledge and conversation history
        """
        # Build base system prompt
        system_prompt = self._build_system_prompt(context, student_name, student_email)
        
        # Add retrieved knowledge to system prompt (RAG component)
        if retrieved_docs:
            knowledge_section = "\n\n" + "="*60 + "\n"
            knowledge_section += "RELEVANT KNOWLEDGE BASE (Use this to answer questions):\n"
            knowledge_section += "="*60 + "\n"
            for idx, doc in enumerate(retrieved_docs, 1):
                # Truncate very long documents
                doc_preview = doc[:500] if len(doc) > 500 else doc
                knowledge_section += f"\n[Document {idx}]:\n{doc_preview}\n"
            knowledge_section += "="*60 + "\n"
            system_prompt += knowledge_section
            logger.info(f"Added {len(retrieved_docs)} knowledge documents to prompt")
        
        # Build user prompt
        user_prompt = self._build_user_prompt(query, context, query_type)
        
        # Construct messages with conversation history
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add last 5 conversation turns (10 messages max) for context
        if conversation_history:
            # Ensure history is properly formatted
            valid_history = [msg for msg in conversation_history 
                           if isinstance(msg, dict) and 'role' in msg and 'content' in msg]
            if valid_history:
                messages.extend(valid_history[-10:])
                logger.info(f"Added {len(valid_history[-10:])} conversation history messages")
        
        # Add current query
        messages.append({"role": "user", "content": user_prompt})
        
        return messages
    
    def _build_system_prompt(self, context: Dict[str, Any], student_name: Optional[str] = None, student_email: Optional[str] = None) -> str:
        """
        Build system prompt with student information and portal context
        """
        student_info = context.get('student_info', {})
        student_name = student_name or student_info.get('name', 'Student')
        student_email = student_email or student_info.get('email', 'Not provided')
        
        system_prompt = f"""You are a friendly and intelligent PLACEMENT TRAINING assistant for the College Placement Training Portal.

Student: {student_name}

CRITICAL RULES - NEVER VIOLATE:
1. GREETINGS: Respond warmly in 1-2 sentences, ask how to help. NO data dumping!
2. ASSESSMENTS: Show ONLY what's in "Available Assessments" list - count them carefully
3. RESULTS: Use ONLY "Completed Assessments" and "Performance Summary" data
4. HELP: Give clear, step-by-step guidance from portal knowledge
5. GENERAL: Answer from context; if not available, say so and suggest where to look
6. OFF-TOPIC: Politely redirect to studies/placement prep like a caring teacher would
7. NEVER invent, hallucinate, or make up ANY data (especially assessment names)
8. NEVER add signatures, "Best regards", closing remarks, or sign-offs
9. Be CONCISE: 1-3 sentences unless listing specific data

YOUR BEHAVIOR BY QUERY TYPE:
┌─────────────────┬──────────────────────────────────────────────┐
│ Greeting        │ Friendly welcome, ask how to help            │
│ Assessment Q    │ List ONLY from "Available Assessments"       │
│ Results Q       │ Show data from performance sections          │
│ Help/How-to     │ Step-by-step guidance                        │
│ Profile/Account │ Guide to settings/profile features           │
│ Thanks/Feedback │ Brief acknowledgment, offer more help        │
│ General Q       │ Answer from context or say unknown           │
│ OFF-TOPIC       │ Politely redirect to placement preparation   │
└─────────────────┴──────────────────────────────────────────────┘

STRICT DATA RULES:
- Assessment count: If list shows 1, say 1. If 0, say 0. NEVER guess!
- NO hallucinated names: Don't mention "Logical Reasoning" or "Programming Fundamentals" unless they're EXPLICITLY in the list
- Context ONLY: Use provided data, not your training knowledge
"""
        
        return system_prompt
    
    def _build_user_prompt(self, query: str, context: Dict[str, Any], query_type: str) -> str:
        """
        Build user prompt based on query type and context
        """
        # OFF-TOPIC: Redirect to studies like a caring teacher
        if query_type == "off_topic":
            student_info = context.get('student_info', {})
            student_name = student_info.get('name', 'there')
            return f"""Student asked an OFF-TOPIC question: {query}

This is NOT related to placement training, studies, or career preparation.

Your Role (as a caring teacher/mentor):
- Acknowledge their question briefly WITHOUT answering it
- Gently remind them to focus on placement preparation
- Redirect them to use the portal for assessments/learning
- Be kind but firm - like a teacher who wants them to succeed
- Encourage them to prioritize their career goals
- Suggest they can discuss such topics in their free time

Example responses:
"I understand you're interested in that, {student_name}, but let's focus on what matters for your placement! 📚 Have you checked the available assessments? Your future career is more important right now."

"Hey {student_name}, I get it - we all have interests outside studies! But right now, let's prioritize your placement preparation. What can I help you with regarding assessments or learning?"

Keep it: Professional, caring, motivating, redirecting to studies."""
        
        # NAME CHANGE: Extract new name and prepare update
        if query_type == "name_change":
            new_name = self._extract_new_name(query)
            if new_name:
                return f"""SPECIAL REQUEST: Student wants to change their name to "{new_name}".

Query: {query}
New Name Requested: {new_name}

Instructions:
1. Confirm the name change warmly
2. Tell them it's being updated
3. Include in response: {{"action": "update_name", "new_name": "{new_name}"}}

Example: "Perfect! I've updated your name to {new_name} ✓. Your profile has been updated successfully!" """
            else:
                return f"""Student wants to change their name but didn't specify it clearly.

Query: {query}

Instructions:
Ask them to provide their new name clearly.

Example: "I'd be happy to update your name! Please tell me your new name. For example: 'My name is John' or 'Change my name to Sarah'." """
        
        # GREETING: Special handling for greetings - keep it simple and friendly
        if query_type == "greeting":
            student_info = context.get('student_info', {})
            student_name = student_info.get('name', 'there')
            return f"""Student said: {query}

This is a greeting. Respond warmly and briefly.

Instructions:
- Greet the student by name: {student_name}
- Keep it friendly and welcoming (1-2 sentences)
- Ask how you can help them today
- DO NOT list assessments or any data unless they ask
- DO NOT include signatures or closing remarks
- Just be friendly and conversational

Example: "Hi {student_name}! 👋 Welcome back to the College Placement Training Portal. How can I assist you today?" """
        
        # Format context data for the prompt
        context_info = self._format_context_for_prompt(context)
        
        # Base prompt with context
        base_prompt = f"""Student Question: {query}

STRICT CONTEXT - USE ONLY THIS DATA:
{context_info}

CRITICAL INSTRUCTION:
Count the assessments in "Available Assessments" section above.
- If you see 1 assessment listed, mention ONLY that 1
- If you see 0 or "None available", say there are NO assessments
- DO NOT mention assessments like "Logical Reasoning" or "Programming Fundamentals" unless they are EXPLICITLY listed above
- DO NOT add extra assessments from your knowledge
- DO NOT include signatures

Answer in 1-2 sentences based ONLY on the data above.
"""
        
        # Add query-type specific instructions
        if query_type == "assessments":
            base_prompt += """
Focus: Show ONLY the assessments listed in "Available Assessments" section.
- If list is empty or shows "None available", say so
- Do NOT make up assessment names
- Be specific about what's actually available
"""
        elif query_type == "results":
            base_prompt += """
Focus: Answer about the student's test results and performance.
- Use data from "Completed Assessments" and "Performance Summary" sections
- If no results yet, say so and suggest taking an assessment
- Be encouraging and specific about their progress
"""
        elif query_type == "help":
            base_prompt += """
Focus: Provide clear, step-by-step guidance.
- Explain how to use portal features
- Give practical instructions
- Be helpful and educational
- Keep it concise and actionable
"""
        elif query_type == "profile":
            base_prompt += """
Focus: Help with account and profile-related questions.
- Explain how to update profile settings
- Guide on password changes or email updates
- Direct to appropriate pages
- Be clear and security-conscious
"""
        elif query_type == "acknowledgment":
            base_prompt += """
Focus: Respond to positive feedback warmly.
- Acknowledge their thanks
- Offer continued assistance
- Keep it brief and friendly
- NO data dumping
"""
        elif query_type == "general":
            base_prompt += """
Focus: Answer the question using available context.
- Provide accurate information from the context
- If not in context, say you don't have that information
- Suggest where they might find it (dashboard, settings, etc.)
- Be helpful and concise
"""
        
        return base_prompt
    
    def _format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format context data for inclusion in the prompt
        """
        formatted_context = []
        
        # Student information
        if 'student_info' in context:
            student_info = context['student_info']
            formatted_context.append(f"Student ID: {student_info.get('id', 'N/A')}")
            formatted_context.append(f"Student Name: {student_info.get('name', 'N/A')}")
            formatted_context.append(f"Student Email: {student_info.get('email', 'N/A')}")
        
        # Available assessments (only show what student hasn't taken)
        if 'available_assessments' in context and context['available_assessments']:
            formatted_context.append("\nAvailable Assessments (Not Yet Taken):")
            for i, assessment in enumerate(context['available_assessments'], 1):
                formatted_context.append(f"  {i}. {assessment.get('title', 'N/A')} ({assessment.get('category', 'General')}) - {assessment.get('total_time', 30)} minutes")
        elif 'available_assessments' in context:
            formatted_context.append("\nAvailable Assessments: None available (all completed or none active)")
        
        # Completed assessments summary
        if 'completed_assessments' in context and context['completed_assessments']:
            completed_count = len(context['completed_assessments'])
            formatted_context.append(f"\nCompleted Assessments: {completed_count}")
            
            # Performance summary
            if 'performance_summary' in context:
                perf = context['performance_summary']
                if perf.get('total_completed', 0) > 0:
                    formatted_context.append(f"Performance Summary:")
                    formatted_context.append(f"  - Average Score: {perf.get('average_percentage', 0)}%")
                    formatted_context.append(f"  - Highest Score: {perf.get('highest_score', 0)}%")
                    formatted_context.append(f"  - Passed: {perf.get('passed_count', 0)} | Failed: {perf.get('failed_count', 0)}")
        elif 'completed_assessments' in context:
            formatted_context.append("\nCompleted Assessments: None")
        
        return "\n".join(formatted_context) if formatted_context else "No specific context available"
    
    def _remove_hallucinated_assessments(self, message: str, context: Dict[str, Any]) -> str:
        """
        Post-process response to remove any assessment names that aren't in the actual available list
        This is a safety net against AI hallucination
        """
        logger.info("ANTI-HALLUCINATION: Starting post-processing")
        
        # Get the actual available assessments
        available_assessments = context.get('available_assessments', [])
        logger.info(f"ANTI-HALLUCINATION: Found {len(available_assessments)} real assessments in database")
        
        # Fix: Safely get assessment names, handle None values
        actual_assessment_names = [(a.get('title') or a.get('name') or '').lower() for a in available_assessments if a.get('title') or a.get('name')]
        
        # Common hallucinated assessment names to remove
        hallucinated_names = [
            'logical reasoning',
            'programming fundamentals',
            'aptitude assessment',
            'technical assessment',
            'verbal reasoning',
            'data structures',
            'algorithms'
        ]
        
        # If we have assessments, build a clean response
        if available_assessments:
            clean_message = f"You have {len(available_assessments)} assessment"
            clean_message += "s" if len(available_assessments) > 1 else ""
            clean_message += " available:\n\n"
            
            for assessment in available_assessments:
                name = assessment.get('title', 'Unknown')
                category = assessment.get('category', 'General')
                duration = assessment.get('total_time', 30)
                clean_message += f"📝 **{name}** ({category})\n"
                clean_message += f"   • Duration: {duration} minutes\n\n"
            
            clean_message += "Ready to start? Click 'View Assessments' to begin!"
            logger.info(f"ANTI-HALLUCINATION: Built clean response with {len(available_assessments)} real assessments")
            return clean_message
        else:
            logger.info("ANTI-HALLUCINATION: No assessments available, returning empty message")
            return "You have no assessments available at the moment. All assessments have been completed or none are currently active."
    
    def _extract_new_name(self, query: str) -> Optional[str]:
        """
        Extract the new name from name change queries
        Examples:
        - "Change my name to John Smith" -> "John Smith"
        - "My name is Sarah Johnson" -> "Sarah Johnson"
        - "Call me Alex" -> "Alex"
        - "Update my name to Mike Davis" -> "Mike Davis"
        """
        import re
        
        query = query.strip()
        
        # Pattern 1: "change my name to X" or "update my name to X"
        match = re.search(r'(?:change|update)\s+(?:my\s+)?name\s+to\s+(.+?)(?:\s*$|[.!?])', query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
        
        # Pattern 2: "my name is X"
        match = re.search(r'my\s+name\s+is\s+(.+?)(?:\s*$|[.!?])', query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
        
        # Pattern 3: "call me X" or "rename me to X"
        match = re.search(r'(?:call|rename)\s+me(?:\s+to)?\s+(.+?)(?:\s*$|[.!?])', query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
        
        # Pattern 4: "i am X" or "i'm X" (at start of sentence)
        match = re.search(r'^(?:i\s+am|i\'m)\s+(.+?)(?:\s*$|[.!?])', query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
        
        return None