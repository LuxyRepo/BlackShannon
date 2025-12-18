# test_agent.py
from src.agents.sqli_agent import SQLiAgent
from src.core.config_manager import ConfigManager

config = ConfigManager()
agent = SQLiAgent(config)

# Usa un target di test tipo DVWA o http://testphp.vulnweb.com
findings = agent.execute("http://testphp.vulnweb.com/artists.php?artist=1")
print("Findings:", findings)
