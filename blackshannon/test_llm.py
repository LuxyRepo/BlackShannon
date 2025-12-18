# test_llm.py (nella root del progetto)

from src.llm import HybridStrategy, TaskComplexity
from src.core.config_manager import init_config
from src.core.logger import get_logger
from dotenv import load_dotenv
import os

load_dotenv()

# Init
config = init_config()
logger = get_logger()

# Create hybrid strategy
hybrid = HybridStrategy(
    deepseek_key=os.getenv("DEEPSEEK_API_KEY"),
    claude_key=os.getenv("ANTHROPIC_API_KEY")
)

# Test simple task (should use DeepSeek)
messages = [
    hybrid.deepseek.create_message("system", "You are a helpful assistant"),
    hybrid.deepseek.create_message("user", "What is 2+2?")
]

response = hybrid.route(
    messages,
    task_type="simple_classification",
    complexity=TaskComplexity.SIMPLE
)

logger.info(f"Response: {response.content}")
logger.info(f"Provider: {response.provider}")
logger.info(f"Cost: ${response.cost:.4f}")

# Print stats
stats = hybrid.get_stats()
logger.info(f"Stats: {stats}")
