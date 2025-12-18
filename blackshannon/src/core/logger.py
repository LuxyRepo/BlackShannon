"""
BlackShannon Logger
Beautiful CLI logging with Rich
"""

import logging
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "phase": "bold magenta",
})

console = Console(theme=custom_theme)


class BlackShannonLogger:
    """Enhanced logger with Rich formatting"""
    
    def __init__(self, log_dir: str = "./workspace/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"blackshannon_{timestamp}.log"
        
        # Setup logger
        self.logger = logging.getLogger("blackshannon")
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler (Rich)
        console_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
        console_handler.setLevel(logging.INFO)
        
        # File handler (detailed)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, msg: str):
        """Info message"""
        self.logger.info(msg)
    
    def success(self, msg: str):
        """Success message (green)"""
        console.print(f"[success]✓ {msg}[/success]")
        self.logger.info(f"SUCCESS: {msg}")
    
    def warning(self, msg: str):
        """Warning message"""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """Error message"""
        self.logger.error(msg)
    
    def phase(self, msg: str):
        """Phase header"""
        console.print(f"\n[phase]{'='*60}[/phase]")
        console.print(f"[phase]{msg}[/phase]")
        console.print(f"[phase]{'='*60}[/phase]\n")
        self.logger.info(f"PHASE: {msg}")
    
    def debug(self, msg: str):
        """Debug message"""
        self.logger.debug(msg)


# Global logger instance
logger = None

def get_logger() -> BlackShannonLogger:
    """Get or create logger instance"""
    global logger
    if logger is None:
        logger = BlackShannonLogger()
    return logger
