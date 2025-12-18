"""
DeepSeek API Client
Uses OpenAI-compatible API
"""

from typing import List
from openai import OpenAI
from .base_llm import BaseLLM, LLMMessage, LLMResponse
from ..core.logger import get_logger

logger = get_logger()


class DeepSeekClient(BaseLLM):
    """DeepSeek LLM client using OpenAI SDK"""
    
    # DeepSeek pricing (as of Dec 2024)
    COST_PER_1M_INPUT = 0.14   # $0.14 per 1M input tokens
    COST_PER_1M_OUTPUT = 0.28  # $0.28 per 1M output tokens
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs):
        super().__init__(api_key, model, **kwargs)
        
        # DeepSeek uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        logger.debug(f"DeepSeek client initialized with model: {model}")
    
    def generate(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate response from DeepSeek"""
        try:
            # Convert messages to OpenAI format
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            # Override defaults with kwargs
            temperature = kwargs.get('temperature', self.temperature)
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            
            logger.debug(f"Calling DeepSeek API with {len(messages)} messages")
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            # Extract response
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            # Calculate tokens and cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            cost = self.calculate_cost(input_tokens, output_tokens)
            
            logger.info(
                f"DeepSeek response: {total_tokens} tokens, ${cost:.4f}"
            )
            
            return LLMResponse(
                content=content,
                model=self.model,
                provider="deepseek",
                tokens_used=total_tokens,
                cost=cost,
                finish_reason=finish_reason
            )
            
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate DeepSeek cost"""
        input_cost = (input_tokens / 1_000_000) * self.COST_PER_1M_INPUT
        output_cost = (output_tokens / 1_000_000) * self.COST_PER_1M_OUTPUT
        return input_cost + output_cost
