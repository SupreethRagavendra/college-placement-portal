"""
Response Cache for RAG System
Caches non-personalized responses to reduce API calls and improve performance
"""
from typing import Optional, Dict, Any
import hashlib
import json
import time
import logging

logger = logging.getLogger(__name__)

class ResponseCache:
    def __init__(self, ttl_seconds=300):
        """
        Initialize response cache
        
        Args:
            ttl_seconds: Time-to-live for cached responses (default: 5 minutes)
        """
        self.cache = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, query: str, student_id: int) -> str:
        """
        Generate cache key from query and student ID
        Uses MD5 hash of normalized query
        """
        # Normalize query (lowercase, trimmed)
        normalized = query.lower().strip()
        hash_input = f"{student_id}:{normalized}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def get(self, query: str, student_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if available and not expired
        
        Returns:
            Cached response dict or None if not found/expired
        """
        key = self._generate_key(query, student_id)
        
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            
            # Check if cache is still valid
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                logger.info(f"Cache HIT for query: '{query[:50]}...' (hit rate: {self.get_hit_rate():.1f}%)")
                return cached_data
            else:
                # Cache expired, remove it
                del self.cache[key]
                logger.debug(f"Cache EXPIRED for query: '{query[:50]}...'")
        
        self.misses += 1
        logger.debug(f"Cache MISS for query: '{query[:50]}...' (hit rate: {self.get_hit_rate():.1f}%)")
        return None
    
    def set(self, query: str, student_id: int, response: Dict[str, Any]):
        """
        Cache a response
        
        Args:
            query: User query
            student_id: Student ID
            response: Response dict to cache
        """
        key = self._generate_key(query, student_id)
        self.cache[key] = (response, time.time())
        logger.debug(f"Cached response for query: '{query[:50]}...' (cache size: {len(self.cache)})")
    
    def should_cache(self, query: str, query_type: str = None) -> bool:
        """
        Determine if a query response should be cached
        Don't cache personalized queries (results, scores, my, etc.)
        
        Args:
            query: User query
            query_type: Optional query type classification
            
        Returns:
            True if response should be cached
        """
        query_lower = query.lower()
        
        # Don't cache personalized queries
        personal_keywords = [
            'my', 'i ', "i'm", 'me', 'mine',
            'result', 'score', 'performance', 
            'profile', 'account',
            'show me', 'give me'
        ]
        
        for keyword in personal_keywords:
            if keyword in query_lower:
                return False
        
        # Don't cache certain query types
        non_cacheable_types = ['results', 'profile', 'assessments', 'name_change']
        if query_type and query_type in non_cacheable_types:
            return False
        
        return True
    
    def clear(self):
        """
        Clear all cached responses
        """
        size = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache cleared ({size} entries removed)")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        """
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': self.get_hit_rate(),
            'ttl_seconds': self.ttl
        }
    
    def get_hit_rate(self) -> float:
        """
        Calculate cache hit rate percentage
        """
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return (self.hits / total) * 100
    
    def cleanup_expired(self):
        """
        Remove all expired entries from cache
        """
        current_time = time.time()
        expired_keys = []
        
        for key, (data, timestamp) in self.cache.items():
            if current_time - timestamp >= self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)

