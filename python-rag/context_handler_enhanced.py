"""
Enhanced Context Handler for OpenRouter RAG with Intelligent Cutoff
Processes student queries with context and generates appropriate prompts
"""
import logging
from typing import Dict, Any, List, Tuple, Optional
import re
from intelligent_cutoff import IntelligentCutoff

logger = logging.getLogger(__name__)

class ContextHandler:
    def __init__(self, openrouter_client):
        self.openrouter_client = openrouter_client
        self.intelligent_cutoff = IntelligentCutoff()
    
    def process_query(self, student_id: int, query: str, student_context: Dict[str, Any], 
                     student_email: Optional[str] = None, student_name: Optional[str] = None) -> Tuple[str, Dict[str, Any], str, str]:
        """
        Process a student query with context and generate response using OpenRouter
        Returns: (message, data, query_type, model_used)
        """
        try:
            # INTELLIGENT CUTOFF: Check if query is off-topic
            is_off_topic, category, relevance_score = self.intelligent_cutoff.is_off_topic(query)
            
            # Check if query is unclear/ambiguous
            is_unclear = self.intelligent_cutoff.is_unclear_query(query, relevance_score)
            
            if is_unclear:
                logger.info(f"Unclear query detected: relevance={relevance_score}% - Using AI clarification")
                
                student_name = student_context.get('student_info', {}).get('name', 'there')
                
                # Build prompt for unclear queries
                unclear_prompt = [
                    {
                        "role": "system",
                        "content": f"""You are a placement preparation assistant. The student said something unclear or vague.
                        
Student's message: "{query}"
Student's name: {student_name}

Your task:
1. Acknowledge their message politely
2. Ask for clarification about what they need help with
3. Suggest placement-related topics they might be interested in

Context:
- Available assessments: {len(student_context.get('available_assessments', []))}
- Completed assessments: {len(student_context.get('completed_assessments', []))}

Guidelines:
- Be helpful and patient
- Ask a clarifying question
- Offer specific placement-related options
- Keep response brief and friendly"""
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
                
                try:
                    # Get AI response for unclear query
                    response = self.openrouter_client.call_with_fallback(unclear_prompt)
                    ai_message = response["choices"][0]["message"]["content"] if response.get("choices") else None
                    
                    if ai_message:
                        clarification_message = ai_message
                        model_used = response.get("model_used", "openrouter")
                    else:
                        # Fallback to template
                        clarification_message = self.intelligent_cutoff.generate_clarification_message(
                            query, student_context
                        )
                        model_used = 'intelligent_cutoff_fallback'
                
                except Exception as e:
                    logger.error(f"AI clarification failed: {e}")
                    # Fallback to template
                    clarification_message = self.intelligent_cutoff.generate_clarification_message(
                        query, student_context
                    )
                    model_used = 'intelligent_cutoff_fallback'
                
                # Get study suggestions
                suggestions = self.intelligent_cutoff.get_study_suggestions(student_context)
                
                return (
                    clarification_message,
                    {
                        'unclear_query': True,
                        'relevance_score': relevance_score,
                        'suggestions': suggestions,
                        'original_query': query
                    },
                    'unclear_redirect',
                    model_used
                )
            
            if is_off_topic:
                logger.warning(f"Off-topic query detected: category={category}, relevance={relevance_score}%")
                
                # ENHANCED: Let AI acknowledge the query and redirect contextually
                student_name = student_context.get('student_info', {}).get('name', 'there')
                
                # Build a special prompt for off-topic queries
                available_count = len(student_context.get('available_assessments', []))
                completed_count = len(student_context.get('completed_assessments', []))
                avg_score = student_context.get('performance_summary', {}).get('average_percentage', 0)
                
                off_topic_prompt = [
                    {
                        "role": "system",
                        "content": f"""You are an academic assistant that helps students only with study-related topics using the retrieved database content.

Student's name: {student_name}
Student's message: "{query}"

If the user's question or message is unrelated to academics or studies, respond politely by briefly acknowledging the topic they mentioned and then gently guiding them back to studies.

Context about student:
- Available assessments: {available_count}
- Completed assessments: {completed_count}
- Average score: {avg_score:.1f}%

Example tone:
- "Hmm, [topic] sound interesting! But let's stay focused on your studies for now."
- "That's a fun topic, but we should concentrate on your learning goals right now."
- "I see you mentioned [keyword], but let's get back to your placement preparation!"

Guidelines:
1. Use the user's keyword naturally in your reply when possible
2. Keep it brief and positive (1-2 sentences)
3. Gently redirect to their studies or assessments
4. Stay motivating and focused on learning
5. Mention specific actions they can take (e.g., "You have {available_count} assessments to try!")

Do not generate or assume answers outside the database content.
Always keep your tone positive, motivating, and focused on learning."""
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
                
                try:
                    # Get AI response for off-topic query
                    response = self.openrouter_client.call_with_fallback(off_topic_prompt)
                    ai_message = response["choices"][0]["message"]["content"] if response.get("choices") else None
                    
                    if ai_message:
                        # Use AI's contextual response
                        redirect_message = ai_message
                        model_used = response.get("model_used", "openrouter")
                    else:
                        # Fallback to template-based redirect
                        redirect_message = self.intelligent_cutoff.generate_redirect_message(
                            query, category, student_context
                        )
                        model_used = 'intelligent_cutoff_fallback'
                
                except Exception as e:
                    logger.error(f"AI redirect failed: {e}")
                    # Fallback to template-based redirect
                    redirect_message = self.intelligent_cutoff.generate_redirect_message(
                        query, category, student_context
                    )
                    model_used = 'intelligent_cutoff_fallback'
                
                # Get study suggestions
                suggestions = self.intelligent_cutoff.get_study_suggestions(student_context)
                
                return (
                    redirect_message,
                    {
                        'off_topic': True,
                        'category': category,
                        'relevance_score': relevance_score,
                        'suggestions': suggestions,
                        'original_query': query
                    },
                    'off_topic',
                    model_used
                )
            
            # Determine query type
            query_type = self._classify_query(query)
            logger.info(f"Query classified as: {query_type} (relevance: {relevance_score}%)")
            
            # Build prompt based on query type and context
            prompt_messages = self._build_prompt(query, student_context, query_type, student_name, student_email)
            
            # Call OpenRouter API with fallback
            response = self.openrouter_client.call_with_fallback(prompt_messages)
            
            # Extract message and data
            message = response["choices"][0]["message"]["content"] if response.get("choices") else "No response generated"
            data = response.get("data", {})
            data['relevance_score'] = relevance_score  # Add relevance score to data
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
        Note: Off-topic queries are already filtered by intelligent_cutoff
        """
        query_lower = query.lower().strip()
        
        # Greeting queries
        greeting_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings", "yo", "sup", "hola"]
        if any(greeting == query_lower or query_lower.startswith(greeting + " ") or query_lower.startswith(greeting + "!") for greeting in greeting_keywords):
            if not any(keyword in query_lower for keyword in ["assessment", "test", "exam", "result", "score", "available", "show", "what", "when", "where", "how"]):
                return "greeting"
        
        # Assessment-related queries
        if any(keyword in query_lower for keyword in ["assessment", "test", "exam", "quiz", "available", "pending", "take test", "start test"]):
            return "assessments"
        
        # Results-related queries
        if any(keyword in query_lower for keyword in ["result", "score", "grade", "performance", "pass", "fail", "mark", "marks", "percentage"]):
            return "results"
        
        # Help/How-to queries  
        if any(keyword in query_lower for keyword in ["how to", "how do", "how can", "guide", "tutorial", "instructions", "steps to"]):
            return "help"
        
        # Name change requests
        if any(keyword in query_lower for keyword in ["change my name", "update my name", "rename me", "my name is", "call me", "change name to", "update name to"]):
            return "name_change"
        
        # Profile/Account queries
        if any(keyword in query_lower for keyword in ["profile", "account", "password", "email", "settings", "update profile"]):
            return "profile"
        
        # General information queries
        if any(keyword in query_lower for keyword in ["what is", "what are", "when is", "when are", "where is", "where are", "who is", "why is", "explain"]):
            return "general"
        
        # Thank you / feedback
        if any(keyword in query_lower for keyword in ["thank", "thanks", "appreciate", "helpful", "good", "great", "awesome"]):
            return "acknowledgment"
        
        # Default to general
        return "general"
    
    def _build_prompt(self, query: str, context: Dict[str, Any], query_type: str, 
                     student_name: Optional[str] = None, student_email: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Build an optimized prompt for OpenRouter models based on query type and context
        """
        # System prompt with student information
        system_prompt = self._build_system_prompt(context, student_name, student_email)
        
        # User prompt based on query type
        user_prompt = self._build_user_prompt(query, context, query_type)
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
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
6. NEVER invent, hallucinate, or make up ANY data (especially assessment names)
7. NEVER add signatures, "Best regards", closing remarks, or sign-offs
8. Be CONCISE: 1-3 sentences unless listing specific data
9. FOCUS ON STUDIES: Always encourage placement preparation and learning

YOUR BEHAVIOR BY QUERY TYPE:
┌─────────────────┬──────────────────────────────────────────────┐
│ Greeting        │ Friendly welcome, ask how to help            │
│ Assessment Q    │ List ONLY from "Available Assessments"       │
│ Results Q       │ Show data from performance sections          │
│ Help/How-to     │ Step-by-step guidance                        │
│ Profile/Account │ Guide to settings/profile features           │
│ Thanks/Feedback │ Brief acknowledgment, offer more help        │
│ General Q       │ Answer from context or say unknown           │
└─────────────────┴──────────────────────────────────────────────┘

STRICT DATA RULES:
- Assessment count: If list shows 1, say 1. If 0, say 0. NEVER guess!
- NO hallucinated names: Don't mention assessments unless they're EXPLICITLY in the list
- Context ONLY: Use provided data, not your training knowledge
"""
        
        return system_prompt
    
    def _build_user_prompt(self, query: str, context: Dict[str, Any], query_type: str) -> str:
        """
        Build user prompt based on query type and context
        """
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
- DO NOT mention assessments unless they are EXPLICITLY listed above
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
        
        # Available assessments
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
        """
        logger.info("ANTI-HALLUCINATION: Starting post-processing")
        
        available_assessments = context.get('available_assessments', [])
        logger.info(f"ANTI-HALLUCINATION: Found {len(available_assessments)} real assessments in database")
        
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
        """
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
        
        # Pattern 4: "i am X" or "i'm X"
        match = re.search(r'^(?:i\s+am|i\'m)\s+(.+?)(?:\s*$|[.!?])', query, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
        
        return None
