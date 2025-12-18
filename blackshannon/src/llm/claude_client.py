"""
Claude API Client (Anthropic)
"""

from typing import List
from anthropic import Anthropic
from .base_llm import BaseLLM, LLMMessage, LLMResponse
from ..core.logger import get_logger

logger = get_logger()


class ClaudeClient(BaseLLM):
    """Claude (Anthropic) LLM client"""
    
    # Claude Sonnet 4 pricing (as of Dec 2024)
    COST_PER_1M_INPUT = 3.00   # $3 per 1M input tokens
    COST_PER_1M_OUTPUT = 15.00  # $15 per 1M output tokens
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "claude-sonnet-4-20250514",
        **kwargs
    ):
        super().__init__(api_key, model, **kwargs)
        
        self.client = Anthropic(api_key=api_key)
        
        logger.debug(f"Claude client initialized with model: {model}")
    
    def generate(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate response from Claude"""
        try:
            # Claude separates system message from conversation
            system_message = None
            conversation_messages = []
            
            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    conversation_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Override defaults with kwargs
            temperature = kwargs.get('temperature', self.temperature)
            max_tokens = kwargs.get('max_tokens', self.max_tokens)
            
            logger.debug(f"Calling Claude API with {len(messages)} messages")
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                system=system_message,
                messages=conversation_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            # Extract response
            content = response.content[0].text
            finish_reason = response.stop_reason
            
            # Calculate tokens and cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            cost = self.calculate_cost(input_tokens, output_tokens)
            
            logger.info(
                f"Claude response: {total_tokens} tokens, ${cost:.4f}"
            )
            
            return LLMResponse(
                content=content,
                model=self.model,
                provider="claude",
                tokens_used=total_tokens,
                cost=cost,
                finish_reason=finish_reason
            )
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate Claude cost"""
        input_cost = (input_tokens / 1_000_000) * self.COST_PER_1M_INPUT
        output_cost = (output_tokens / 1_000_000) * self.COST_PER_1M_OUTPUT
        return input_cost + output_cost
