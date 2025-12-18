"""
Hybrid LLM Strategy
Intelligent routing between DeepSeek and Claude
"""

from typing import List, Optional
from enum import Enum
from .base_llm import BaseLLM, LLMMessage, LLMResponse
from .deepseek_client import DeepSeekClient
from .claude_client import ClaudeClient
from ..core.logger import get_logger

logger = get_logger()


class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"      # Pattern matching, basic analysis
    MEDIUM = "medium"      # Moderate reasoning
    COMPLEX = "complex"    # Deep reasoning, strategy


class HybridStrategy:
    """
    Intelligent routing between DeepSeek (cheap) and Claude (smart)
    
    Strategy:
    - Simple tasks → DeepSeek (faster, cheaper)
    - Complex tasks → Claude (better reasoning)
    - Large context → Claude (200k tokens)
    """
    
    # Task type mappings
    DEEPSEEK_TASKS = {
        "fingerprinting",
        "error_analysis",
        "pattern_matching",
        "payload_generation",
        "response_comparison",
        "simple_classification",
    }
    
    CLAUDE_TASKS = {
        "vulnerability_analysis",
        "exploitation_planning",
        "false_positive_filtering",
        "report_generation",
        "complex_bypass_logic",
        "multi_step_reasoning",
    }
    
    CONTEXT_THRESHOLD = 30000  # Switch to Claude if > 30k tokens
    
    def __init__(
        self,
        deepseek_key: Optional[str] = None,
        claude_key: Optional[str] = None,
        **kwargs
    ):
        self.deepseek: Optional[DeepSeekClient] = None
        self.claude: Optional[ClaudeClient] = None
        
        # Initialize available clients
        if deepseek_key:
            self.deepseek = DeepSeekClient(
                api_key=deepseek_key,
                **kwargs.get('deepseek', {})
            )
            logger.info("Hybrid: DeepSeek client ready")
        
        if claude_key:
            self.claude = ClaudeClient(
                api_key=claude_key,
                **kwargs.get('claude', {})
            )
            logger.info("Hybrid: Claude client ready")
        
        if not self.deepseek and not self.claude:
            raise ValueError("At least one LLM client required")
        
        # Track costs
        self.total_cost = 0.0
        self.deepseek_calls = 0
        self.claude_calls = 0
    
    def route(
        self,
        messages: List[LLMMessage],
        task_type: Optional[str] = None,
        complexity: Optional[TaskComplexity] = None,
        force_provider: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Route request to appropriate LLM
        
        Args:
            messages: Conversation messages
            task_type: Type of task (e.g., "fingerprinting", "exploitation_planning")
            complexity: Task complexity level
            force_provider: Force specific provider ("deepseek" or "claude")
        """
        
        # Force specific provider if requested
        if force_provider:
            provider = self._get_provider(force_provider)
            if provider:
                return self._call_provider(provider, messages, force_provider, **kwargs)
        
        # Estimate context size (rough)
        context_size = sum(len(msg.content) for msg in messages)
        
        # Decision logic
        selected_provider = self._decide_provider(
            task_type=task_type,
            complexity=complexity,
            context_size=context_size
        )
        
        logger.info(f"Routing to: {selected_provider} (task={task_type}, context={context_size})")
        
        # Get provider and call
        provider = self._get_provider(selected_provider)
        if not provider:
            # Fallback to available provider
            provider = self.claude or self.deepseek
            selected_provider = "claude" if self.claude else "deepseek"
            logger.warning(f"Fallback to {selected_provider}")
        
        return self._call_provider(provider, messages, selected_provider, **kwargs)
    
    def _decide_provider(
        self,
        task_type: Optional[str],
        complexity: Optional[TaskComplexity],
        context_size: int
    ) -> str:
        """Decide which provider to use"""
        
        # Rule 1: Large context always goes to Claude
        if context_size > self.CONTEXT_THRESHOLD:
            if self.claude:
                return "claude"
        
        # Rule 2: Explicit complexity
        if complexity:
            if complexity == TaskComplexity.SIMPLE and self.deepseek:
                return "deepseek"
            elif complexity == TaskComplexity.COMPLEX and self.claude:
                return "claude"
        
        # Rule 3: Task type mapping
        if task_type:
            if task_type in self.CLAUDE_TASKS and self.claude:
                return "claude"
            elif task_type in self.DEEPSEEK_TASKS and self.deepseek:
                return "deepseek"
        
        # Rule 4: Default to cheapest available
        if self.deepseek:
            return "deepseek"
        return "claude"
    
    def _get_provider(self, name: str) -> Optional[BaseLLM]:
        """Get provider by name"""
        if name == "deepseek":
            return self.deepseek
        elif name == "claude":
            return self.claude
        return None
    
    def _call_provider(
        self,
        provider: BaseLLM,
        messages: List[LLMMessage],
        provider_name: str,
        **kwargs
    ) -> LLMResponse:
        """Call provider and track stats"""
        
        response = provider.generate(messages, **kwargs)
        
        # Track stats
        self.total_cost += response.cost
        if provider_name == "deepseek":
            self.deepseek_calls += 1
        else:
            self.claude_calls += 1
        
        return response
    
    def get_stats(self) -> dict:
        """Get usage statistics"""
        return {
            "total_cost": self.total_cost,
            "deepseek_calls": self.deepseek_calls,
            "claude_calls": self.claude_calls,
            "cost_per_call": (
                self.total_cost / (self.deepseek_calls + self.claude_calls)
                if (self.deepseek_calls + self.claude_calls) > 0
                else 0
            )
        }
