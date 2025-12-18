"""
Base LLM Interface
Abstract class for all LLM providers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LLMMessage:
    """Represents a message in conversation"""
    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    model: str
    provider: str
    tokens_used: int
    cost: float
    finish_reason: str


class BaseLLM(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        self.api_key = api_key
        self.model = model
        self.temperature = kwargs.get('temperature', 0.3)
        self.max_tokens = kwargs.get('max_tokens', 4000)
        self.provider_name = self.__class__.__name__.replace('Client', '').lower()
    
    @abstractmethod
    def generate(
        self, 
        messages: List[LLMMessage],
        **kwargs
    ) -> LLMResponse:
        """
        Generate response from LLM
        Must be implemented by each provider
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on tokens
        Must be implemented by each provider
        """
        pass
    
    def create_message(self, role: str, content: str) -> LLMMessage:
        """Helper to create message"""
        return LLMMessage(role=role, content=content)
    
    def format_conversation(
        self,
        system_prompt: str,
        user_prompt: str,
        context: Optional[str] = None
    ) -> List[LLMMessage]:
        """Format a typical conversation"""
        messages = [
            self.create_message("system", system_prompt)
        ]
        
        if context:
            messages.append(self.create_message("user", context))
        
        messages.append(self.create_message("user", user_prompt))
        
        return messages
