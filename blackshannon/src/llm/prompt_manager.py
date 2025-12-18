"""
Prompt Manager
Loads and manages prompt templates (Shannon-style)
"""

from pathlib import Path
from typing import Dict, Optional
from ..core.logger import get_logger

logger = get_logger()


class PromptManager:
    """
    Manages prompt templates from files
    Supports Shannon-style @include() directives
    """
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {prompts_dir}")
        
        self.cache: Dict[str, str] = {}
        logger.debug(f"PromptManager initialized with dir: {prompts_dir}")
    
    def load(self, prompt_path: str, variables: Optional[Dict] = None) -> str:
        """
        Load prompt from file with variable substitution
        
        Args:
            prompt_path: Path relative to prompts_dir (e.g., "system/sqli_exploit.txt")
            variables: Dict of variables to substitute (e.g., {"TARGET_URL": "..."})
        
        Returns:
            Processed prompt text
        """
        full_path = self.prompts_dir / prompt_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")
        
        # Check cache
        cache_key = str(full_path)
        if cache_key not in self.cache:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.cache[cache_key] = content
        
        prompt = self.cache[cache_key]
        
        # Process @include() directives
        prompt = self._process_includes(prompt)
        
        # Substitute variables
        if variables:
            prompt = self._substitute_variables(prompt, variables)
        
        return prompt
    
    def _process_includes(self, content: str) -> str:
        """
        Process @include() directives (Shannon-style)
        Example: @include(shared/_target_info.txt)
        """
        import re
        
        # Find all @include() directives
        pattern = r'@include\(([^)]+)\)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            include_path = match.group(1).strip()
            
            # Load included file
            try:
                included_content = self.load(include_path)
                content = content.replace(match.group(0), included_content)
            except FileNotFoundError:
                logger.warning(f"Include not found: {include_path}")
                content = content.replace(match.group(0), f"[INCLUDE NOT FOUND: {include_path}]")
        
        return content
    
    def _substitute_variables(self, content: str, variables: Dict) -> str:
        """
        Substitute variables in format {{VARIABLE_NAME}}
        Example: {{TARGET_URL}} → https://example.com
        """
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        
        return content
    
    def load_system_prompt(self, agent_type: str, variables: Optional[Dict] = None) -> str:
        """
        Load system prompt for specific agent type
        
        Args:
            agent_type: Type of agent (e.g., "sqli_exploit", "xss_analysis")
            variables: Variables to substitute
        """
        prompt_path = f"system/{agent_type}.txt"
        return self.load(prompt_path, variables)
    
    def load_task_prompt(self, task_name: str, variables: Optional[Dict] = None) -> str:
        """
        Load task-specific prompt
        
        Args:
            task_name: Task name (e.g., "sqli_confirmation", "sqli_enumeration")
            variables: Variables to substitute
        """
        prompt_path = f"tasks/{task_name}.txt"
        return self.load(prompt_path, variables)
    
    def build_full_prompt(
        self,
        system_file: str,
        task_file: str,
        context: Optional[str] = None,
        variables: Optional[Dict] = None
    ) -> tuple[str, str]:
        """
        Build complete prompt (system + task + context)
        
        Returns:
            (system_prompt, user_prompt)
        """
        # Load system prompt
        system_prompt = self.load(f"system/{system_file}", variables)
        
        # Load task prompt
        task_prompt = self.load(f"tasks/{task_file}", variables)
        
        # Build user prompt
        user_prompt = task_prompt
        if context:
            user_prompt = f"{context}\n\n{task_prompt}"
        
        return system_prompt, user_prompt
