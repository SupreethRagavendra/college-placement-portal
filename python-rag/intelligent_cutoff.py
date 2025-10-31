"""
Intelligent Cutoff System for RAG Chatbot
Detects irrelevant queries and redirects students to focus on placement preparation
"""
import logging
import re
from typing import Tuple

logger = logging.getLogger(__name__)


class IntelligentCutoff:
    """
    Intelligent cutoff system that calculates relevance scores and detects off-topic queries
    """
    
    def __init__(self):
        # HIGH RELEVANCE keywords (+30 points each)
        self.high_relevance = [
            'assessment', 'test', 'exam', 'quiz', 'result', 'score', 'grade',
            'placement', 'interview', 'job', 'career', 'aptitude', 'technical',
            'coding', 'programming', 'algorithm', 'data structure', 'learning',
            'study', 'practice', 'prepare', 'skill', 'improve', 'performance',
            'training', 'course', 'syllabus', 'topic', 'subject'
        ]
        
        # MEDIUM RELEVANCE keywords (+15 points each)
        self.medium_relevance = [
            'question', 'answer', 'help', 'guide', 'how to', 'what is',
            'explain', 'understand', 'know', 'learn', 'teach', 'tutorial',
            'profile', 'account', 'password', 'email', 'settings', 'dashboard'
        ]
        
        # LOW RELEVANCE keywords (-20 points each)
        self.low_relevance = [
            'game', 'gaming', 'movie', 'film', 'music', 'song', 'sport', 'cricket',
            'football', 'party', 'fun', 'bored', 'boring', 'love', 'dating',
            'girlfriend', 'boyfriend', 'relationship', 'weather', 'food', 'recipe',
            'travel', 'vacation', 'shopping', 'fashion', 'celebrity', 'gossip',
            'meme', 'joke', 'funny', 'netflix', 'youtube', 'tiktok', 'instagram',
            'facebook', 'twitter', 'snapchat', 'anime', 'cartoon',
            # Slang and casual expressions
            'bloody', 'sweet', 'cool', 'awesome', 'nice', 'wow', 'damn',
            'hell', 'shit', 'crap', 'stupid', 'dumb', 'lol', 'lmao', 'omg',
            'wtf', 'bruh', 'bro', 'dude', 'mate', 'yolo', 'swag', 'lit'
        ]
        
        # Minimal off-topic detection - only essential categories
        self.off_topic_keywords = {
            'entertainment': ['game', 'movie', 'netflix', 'youtube', 'tiktok', 'music'],
            'personal': ['girlfriend', 'boyfriend', 'dating', 'love', 'relationship'],
            'sports': ['cricket', 'football', 'match', 'ipl'],
            'random': ['weather', 'food', 'travel', 'shopping']
        }
        
        # Career-related terms that indicate relevance (avoid false positives)
        self.career_terms = [
            'placement', 'career', 'job', 'interview', 'skill', 'learning',
            'study', 'prepare', 'practice', 'training', 'professional', 'work'
        ]
    
    def calculate_relevance_score(self, query: str) -> int:
        """
        Calculate relevance score (0-100) based on placement/study-related keywords
        Higher score = more relevant to placement preparation
        Uses intelligent pattern detection instead of extensive word lists
        """
        query_lower = query.lower().strip()
        
        # HANDLE EMPTY OR WHITESPACE-ONLY QUERIES
        if not query_lower or len(query_lower) == 0:
            logger.warning("Empty query detected")
            return 0  # Empty queries get 0 score
        
        # Check if query is just spaces, special chars, or gibberish
        if all(c in ' \t\n\r.,!?;:()[]{}@#$%^&*+=~`|\\/<>' for c in query_lower):
            logger.warning("Query contains only special characters")
            return 0
        
        # Check if query has meaningful alphabetic content
        alpha_chars = sum(1 for c in query_lower if c.isalpha())
        if len(query_lower) > 3 and alpha_chars < len(query_lower) * 0.3:
            logger.warning("Query has too few alphabetic characters")
            return 0
        
        score = 50  # Start with neutral score
        
        # Count keyword matches
        high_matches = sum(1 for keyword in self.high_relevance if keyword in query_lower)
        medium_matches = sum(1 for keyword in self.medium_relevance if keyword in query_lower)
        low_matches = sum(1 for keyword in self.low_relevance if keyword in query_lower)
        
        # Calculate score
        score += (high_matches * 30)
        score += (medium_matches * 15)
        score -= (low_matches * 20)
        
        # Question marks indicate inquiry (slight boost)
        if '?' in query:
            score += 5
        
        # SMART PATTERN DETECTION (without extensive word lists)
        words = query_lower.split()
        word_count = len(words)
        
        # Detect meaningless patterns
        if word_count > 0:
            # Check for repetitive patterns (aaa, xxx, 111)
            for word in words:
                if len(word) > 2 and len(set(word)) == 1:  # All same character
                    score -= 30
                    logger.info("Repetitive character pattern detected")
                    break
            
            # Check if most words are very short (likely gibberish)
            short_words = sum(1 for word in words if len(word) <= 2)
            if word_count >= 3 and short_words >= word_count * 0.7:
                score -= 25
                logger.info("Too many short words detected")
            
            # Check for random consonant clusters (no vowels)
            vowels = set('aeiou')
            no_vowel_words = sum(1 for word in words if len(word) > 3 and not any(c in vowels for c in word))
            if no_vowel_words > word_count * 0.5:
                score -= 30
                logger.info("Too many words without vowels")
        
        # ENHANCED: Single word/character detection
        if word_count == 1:
            single_word = words[0]
            # Check if it's a single character or very short meaningless word
            if len(single_word) <= 2 and single_word not in ['hi', 'ok', 'no']:
                score -= 30
            # Check if it's just a number or special character
            if single_word.isdigit() or not single_word.isalnum():
                score -= 40
        
        # Very short queries (< 3 words) might be greetings or casual
        if word_count < 3 and high_matches == 0:
            score -= 20  # Increased penalty
        
        # Long queries with no relevant keywords are likely off-topic
        if word_count > 5 and high_matches == 0 and medium_matches == 0:
            score -= 25  # Increased penalty
        
        # INTELLIGENT CONTEXT DETECTION
        # Check if query lacks any meaningful context about placement/study
        has_question_words = any(word in query_lower for word in ['what', 'how', 'when', 'where', 'why', 'which', 'can', 'should', 'could'])
        has_action_words = any(word in query_lower for word in ['show', 'tell', 'explain', 'help', 'need', 'want', 'give', 'find'])
        
        # If no question words, no action words, and no high relevance keywords
        if not has_question_words and not has_action_words and high_matches == 0:
            score -= 20
            logger.info("Query lacks meaningful context")
        
        # Detect vague or dismissive phrases
        dismissive_patterns = ['whatever', 'nevermind', 'forget it', 'leave it', 'who cares', 'doesnt matter']
        if any(pattern in query_lower for pattern in dismissive_patterns):
            score -= 40
            logger.info("Dismissive phrase detected")
        
        # If query is mostly slang/casual words, reduce score significantly
        slang_count = sum(1 for word in words if word in [
            'bloody', 'sweet', 'cool', 'awesome', 'nice', 'wow', 'damn',
            'hell', 'shit', 'crap', 'stupid', 'dumb', 'lol', 'lmao', 'omg',
            'wtf', 'bruh', 'bro', 'dude', 'mate', 'yolo', 'swag', 'lit',
            'sick', 'fire', 'dope', 'rad', 'wicked', 'epic', 'savage'
        ])
        
        if word_count > 0 and (slang_count / word_count) > 0.4:  # More than 40% slang
            score -= 30
        
        # ENHANCED: Detect queries with excessive punctuation or emojis
        special_char_count = sum(1 for c in query if c in '!?.,;:()[]{}@#$%^&*+=~`|\\/<>')
        if len(query) > 0 and (special_char_count / len(query)) > 0.3:
            score -= 25  # Too many special characters
        
        # Cap score between 0 and 100
        score = max(0, min(100, score))
        
        logger.info(f"Relevance score: {score}% (H:{high_matches}, M:{medium_matches}, L:{low_matches}, Words:{word_count})")
        return score
    
    def is_off_topic(self, query: str, relevance_threshold: int = 30) -> Tuple[bool, str, int]:
        """
        Determine if a query is off-topic based on intelligent relevance scoring
        Returns: (is_off_topic, category, relevance_score)
        """
        query_lower = query.lower().strip()
        
        # HANDLE EMPTY QUERIES IMMEDIATELY
        if not query_lower or len(query_lower) == 0:
            logger.warning("Empty query - marking as off-topic")
            return True, "empty_query", 0
        
        # Calculate relevance score using intelligent pattern detection
        relevance_score = self.calculate_relevance_score(query)
        
        # INTELLIGENT CUTOFF: Low relevance score (increased threshold to 30)
        if relevance_score < relevance_threshold:
            logger.warning(f"LOW RELEVANCE ({relevance_score}%) - Triggering intelligent cutoff")
            
            # Categorize the type of irrelevance
            words = query_lower.split()
            word_count = len(words)
            
            if word_count == 0:
                return True, "empty_query", relevance_score
            elif word_count == 1 and len(words[0]) <= 3:
                return True, "too_short", relevance_score
            elif all(not c.isalnum() for c in query_lower.replace(' ', '')):
                return True, "special_chars_only", relevance_score
            elif any(word in query_lower for word in ['whatever', 'nevermind', 'forget']):
                return True, "dismissive", relevance_score
            else:
                return True, "irrelevant", relevance_score
        
        # Quick check for obvious off-topic keywords (minimal list)
        if relevance_score < 50:  # Only check if score is borderline
            for category, keywords in self.off_topic_keywords.items():
                if any(keyword in query_lower for keyword in keywords):
                    # Double-check: avoid false positives with career terms
                    if not any(career_term in query_lower for career_term in self.career_terms):
                        logger.info(f"Off-topic keyword detected: {category}")
                        return True, category, relevance_score
        
        return False, "relevant", relevance_score
    
    def is_unclear_query(self, query: str, relevance_score: int) -> bool:
        """
        Determine if query is unclear/ambiguous (needs AI clarification)
        Returns: True if query is unclear and should be clarified before redirecting
        """
        query_lower = query.lower().strip()
        
        # Unclear if:
        # 1. Relevance score is borderline (30-45%)
        # 2. Very short and vague
        # 3. No clear keywords matched
        
        word_count = len(query.split())
        
        # Borderline relevance (might be unclear intent)
        if 30 <= relevance_score <= 45:
            return True
        
        # Very short and vague queries
        if word_count <= 2 and relevance_score < 60:
            return True
        
        # Check for vague/unclear phrases
        unclear_phrases = [
            'what about', 'tell me about', 'i want to know', 'can you',
            'something', 'anything', 'stuff', 'things', 'random',
            'just curious', 'wondering', 'thinking about'
        ]
        
        if any(phrase in query_lower for phrase in unclear_phrases):
            # Only unclear if not clearly relevant
            if relevance_score < 60:
                return True
        
        return False
    
    def generate_clarification_message(self, query: str, student_context: dict) -> str:
        """
        Generate a clarification message for unclear queries
        Then redirect to studies
        """
        student_name = student_context.get('student_info', {}).get('name', 'there')
        available_count = len(student_context.get('available_assessments', []))
        
        message = f"Hi {student_name}! I understand you're asking about: \"{query}\"\n\n"
        message += "While I'd love to help with that, my main purpose is to assist you with your placement preparation! 📚\n\n"
        message += "Let's focus on what really matters for your career success:\n"
        
        if available_count > 0:
            message += f"• You have {available_count} assessment{'s' if available_count > 1 else ''} ready to take\n"
        
        message += "• Practice makes perfect - let's work on your skills!\n"
        message += "• Your future placement depends on consistent preparation\n\n"
        message += "What would you like to focus on today? 🎯"
        
        return message
    
    def generate_redirect_message(self, query: str, category: str, student_context: dict) -> str:
        """
        Generate a personalized redirect message based on student context
        """
        student_name = student_context.get('student_info', {}).get('name', 'there')
        completed_count = len(student_context.get('completed_assessments', []))
        available_count = len(student_context.get('available_assessments', []))
        performance_summary = student_context.get('performance_summary', {})
        avg_score = performance_summary.get('average_percentage', 0)
        
        # Determine student performance level
        if completed_count == 0:
            level = "beginner"
        elif avg_score < 60:
            level = "needs_improvement"
        elif avg_score < 80:
            level = "good"
        else:
            level = "excellent"
        
        # Generate personalized redirect based on level and category
        messages = {
            "beginner": [
                f"Hey {student_name}! I know you're curious about other things, but let's focus on getting started with your placement prep! 🚀",
                f"You have {available_count} assessments waiting for you. Let's tackle your first one together!",
                "Your future career starts here - let's make it count! 💪"
            ],
            "needs_improvement": [
                f"Hi {student_name}, I understand you have other interests, but your placement prep needs attention right now! 📚",
                f"Your current average is {avg_score:.1f}% - let's work on improving that together!",
                f"You have {available_count} more assessments to practice. Focus is key to success! 🎯"
            ],
            "good": [
                f"Hey {student_name}! You're doing well at {avg_score:.1f}%, but let's keep that momentum going! 💪",
                "Taking a mental break is fine, but remember - consistency is what gets you to excellence!",
                f"Ready to tackle the next challenge? You have {available_count} assessments waiting! 🚀"
            ],
            "excellent": [
                f"Impressive work, {student_name}! You're at {avg_score:.1f}% - that's fantastic! 🌟",
                "But champions stay focused. Let's maintain that excellence!",
                f"Challenge yourself with the remaining {available_count} assessments. Keep pushing! 💪"
            ]
        }
        
        # Category-specific additions (simplified)
        category_messages = {
            "entertainment": "Entertainment is great for breaks, but right now, let's prioritize your career goals!",
            "personal": "Personal matters are important, but your placement preparation will shape your future!",
            "sports": "Sports are fun, but your career game needs attention too!",
            "random": "Let's stay focused on what really matters - your placement preparation!",
            "empty_query": "I noticed you sent an empty message. Let me help you with your placement preparation instead!",
            "too_short": "I need more context to help you effectively. What about your assessments would you like to know?",
            "special_chars_only": "I couldn't understand that. How about we work on your placement preparation?",
            "dismissive": "Don't give up! Your placement preparation is important. Let me help you succeed!",
            "irrelevant": "Let's focus on what matters most - your placement success and career preparation!"
        }
        
        # Build final message
        redirect_parts = messages.get(level, messages["beginner"])
        category_msg = category_messages.get(category, category_messages["irrelevant"])
        
        final_message = f"{redirect_parts[0]} {category_msg}\n\n{redirect_parts[1]}"
        
        if len(redirect_parts) > 2:
            final_message += f"\n\n{redirect_parts[2]}"
        
        return final_message
    
    def get_study_suggestions(self, student_context: dict) -> list:
        """
        Generate study suggestions based on student context
        """
        suggestions = []
        
        available_count = len(student_context.get('available_assessments', []))
        completed_count = len(student_context.get('completed_assessments', []))
        performance_summary = student_context.get('performance_summary', {})
        avg_score = performance_summary.get('average_percentage', 0)
        
        if available_count > 0:
            suggestions.append("📝 Take an available assessment")
        
        if completed_count > 0:
            suggestions.append("📊 Review your past results")
        
        if avg_score < 60 and completed_count > 0:
            suggestions.append("💡 Focus on weak areas")
        
        if completed_count == 0:
            suggestions.append("🚀 Start your first assessment")
        
        suggestions.append("📚 Check study materials")
        suggestions.append("🎯 Set learning goals")
        
        return suggestions[:4]  # Return top 4 suggestions
