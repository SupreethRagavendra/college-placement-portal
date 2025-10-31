"""
OpenRouter API Client with Model Fallback
Handles API calls to OpenRouter with automatic fallback between models
"""
import requests
import json
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self, api_key: str, primary_model: str, fallback_model: str, api_url: str = "https://openrouter.ai/api/v1/chat/completions"):
        self.api_key = api_key
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "College Placement Portal"
        })
        
    def call_api(self, messages: List[Dict[str, str]], model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Call OpenRouter API with proper headers and error handling
        """
        if model is None:
            model = self.primary_model
            
        payload = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000),
            "top_p": kwargs.get("top_p", 0.9)
        }
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in ["temperature", "max_tokens", "top_p"] and key in ["frequency_penalty", "presence_penalty", "stop"]:
                payload[key] = value
        
        try:
            logger.info(f"Calling OpenRouter API with model: {model}")
            start_time = time.time()
            
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=kwargs.get("timeout", 30)
            )
            
            response_time = time.time() - start_time
            logger.info(f"API call completed in {response_time:.2f} seconds")
            
            response.raise_for_status()
            result = response.json()
            
            # Add metadata
            if "usage" in result:
                result["metadata"] = {
                    "model_used": model,
                    "response_time": f"{response_time:.2f}s",
                    "tokens_used": result["usage"].get("total_tokens", 0)
                }
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout calling OpenRouter API with model {model}")
            raise Exception(f"API call timed out after {kwargs.get('timeout', 30)} seconds")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error calling OpenRouter API with model {model}: {str(e)}")
            raise Exception(f"API request failed: {str(e)}")
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error from OpenRouter API: {str(e)}")
            raise Exception(f"Failed to parse API response: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error calling OpenRouter API with model {model}: {str(e)}")
            raise e
    
    def call_with_fallback(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Call OpenRouter API with automatic fallback to secondary model
        """
        # Try primary model first
        try:
            result = self.call_api(messages, model=self.primary_model, **kwargs)
            result["model_used"] = self.primary_model
            return result
        except Exception as primary_error:
            logger.warning(f"Primary model {self.primary_model} failed: {str(primary_error)}")
            
            # Try fallback model
            try:
                logger.info(f"Trying fallback model {self.fallback_model}")
                result = self.call_api(messages, model=self.fallback_model, **kwargs)
                result["model_used"] = self.fallback_model
                result["fallback_used"] = True
                return result
            except Exception as fallback_error:
                logger.error(f"Fallback model {self.fallback_model} also failed: {str(fallback_error)}")
                raise Exception(f"Both primary and fallback models failed. Primary: {str(primary_error)}. Fallback: {str(fallback_error)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test OpenRouter API connection with both models
        """
        test_message = "Hello, this is a test message"
        
        results = {}
        
        # Test primary model
        try:
            logger.info(f"Testing primary model: {self.primary_model}")
            response1 = self.call_api([
                {"role": "user", "content": test_message}
            ], model=self.primary_model, max_tokens=50)
            results["primary_model"] = {
                "success": True,
                "model": self.primary_model,
                "response": response1["choices"][0]["message"]["content"] if response1.get("choices") else "No response",
                "usage": response1.get("usage", {})
            }
        except Exception as e:
            results["primary_model"] = {
                "success": False,
                "model": self.primary_model,
                "error": str(e)
            }
        
        # Test fallback model
        try:
            logger.info(f"Testing fallback model: {self.fallback_model}")
            response2 = self.call_api([
                {"role": "user", "content": test_message}
            ], model=self.fallback_model, max_tokens=50)
            results["fallback_model"] = {
                "success": True,
                "model": self.fallback_model,
                "response": response2["choices"][0]["message"]["content"] if response2.get("choices") else "No response",
                "usage": response2.get("usage", {})
            }
        except Exception as e:
            results["fallback_model"] = {
                "success": False,
                "model": self.fallback_model,
                "error": str(e)
            }
        
        return results