"""
BlackShannon Configuration Manager
Loads and validates configuration
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv
import os


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str = "config/default_config.yaml"):
        # Load environment variables
        load_dotenv()
        
        # Load YAML config
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(self.config_path, 'r') as f:
            self.config: Dict[str, Any] = yaml.safe_load(f)
        
        # Load API keys from env
        self._load_api_keys()
        
        # Validate configuration
        self._validate()
    
    def _load_api_keys(self):
        """Load API keys from environment"""
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.claude_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.deepseek_key and not self.claude_key:
            raise ValueError(
                "At least one API key required: DEEPSEEK_API_KEY or ANTHROPIC_API_KEY"
            )
    
    def _validate(self):
        """Validate configuration"""
        # Check LLM strategy
        strategy = self.get("llm.strategy")
        valid_strategies = ["deepseek", "claude", "hybrid"]
        if strategy not in valid_strategies:
            raise ValueError(f"Invalid LLM strategy: {strategy}")
        
        # Validate strategy matches available keys
        if strategy == "deepseek" and not self.deepseek_key:
            raise ValueError("DeepSeek strategy requires DEEPSEEK_API_KEY")
        if strategy == "claude" and not self.claude_key:
            raise ValueError("Claude strategy requires ANTHROPIC_API_KEY")
        if strategy == "hybrid" and (not self.deepseek_key or not self.claude_key):
            raise ValueError("Hybrid strategy requires both API keys")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value using dot notation
        Example: config.get("llm.strategy")
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set config value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_llm_config(self, provider: str) -> Dict[str, Any]:
        """Get LLM-specific configuration"""
        return self.get(f"llm.{provider}", {})
    
    def get_workspace_dir(self) -> Path:
        """Get workspace directory"""
        workspace = Path(self.get("output.workspace_dir", "./workspace"))
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace


# Global config instance
_config: Optional[ConfigManager] = None

def get_config() -> ConfigManager:
    """Get or create config instance"""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config


def init_config(config_path: str = "config/default_config.yaml"):
    """Initialize config with custom path"""
    global _config
    _config = ConfigManager(config_path)
    return _config
