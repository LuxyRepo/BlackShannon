"""
Main Orchestrator
Coordinates all agents and phases
"""

from typing import List, Dict, Any
from pathlib import Path
from ..agents import SQLiAgent
from ..llm import HybridStrategy
from ..llm.prompt_manager import PromptManager
from ..tools.http_client import HTTPClient
from .config_manager import ConfigManager
from .logger import get_logger

logger = get_logger()


class Orchestrator:
    """
    Main orchestrator for BlackShannon
    
    Coordinates:
    - Configuration loading
    - LLM initialization
    - Agent lifecycle
    - Phase execution
    - Results aggregation
    """
    
    def __init__(self, target_url: str, config: ConfigManager):
        self.target_url = target_url
        self.config = config
        
        # Initialize components
        self._init_llm()
        self._init_http_client()
        self._init_prompt_manager()
        
        # Agent registry
        self.agents = []
        
        # Results
        self.all_findings = []
        
        logger.info(f"Orchestrator initialized for {target_url}")
    
    def _init_llm(self):
        """Initialize LLM strategy"""
        strategy = self.config.get('llm.strategy', 'hybrid')
        
        logger.info(f"Initializing LLM strategy: {strategy}")
        
        if strategy == 'hybrid':
            self.llm = HybridStrategy(
                deepseek_key=self.config.deepseek_key,
                claude_key=self.config.claude_key,
                deepseek=self.config.get_llm_config('deepseek'),
                claude=self.config.get_llm_config('claude')
            )
        elif strategy == 'deepseek':
            from ..llm import DeepSeekClient
            self.llm = DeepSeekClient(
                api_key=self.config.deepseek_key,
                **self.config.get_llm_config('deepseek')
            )
        elif strategy == 'claude':
            from ..llm import ClaudeClient
            self.llm = ClaudeClient(
                api_key=self.config.claude_key,
                **self.config.get_llm_config('claude')
            )
        else:
            raise ValueError(f"Invalid LLM strategy: {strategy}")
        
        logger.success("LLM initialized")
    
    def _init_http_client(self):
        """Initialize HTTP client"""
        http_config = self.config.get('http', {})
        
        self.http_client = HTTPClient(
            timeout=self.config.get('target.timeout', 30),
            verify_ssl=self.config.get('target.verify_ssl', False),
            user_agent=http_config.get('user_agent', 'Mozilla/5.0'),
            max_retries=http_config.get('retry_count', 3),
            retry_delay=http_config.get('retry_delay', 2),
            rate_limit=0.5  # 0.5 seconds between requests
        )
        
        logger.success("HTTP client initialized")
    
    def _init_prompt_manager(self):
        """Initialize prompt manager"""
        self.prompt_manager = PromptManager(prompts_dir="prompts")
        logger.success("Prompt manager initialized")
    
    def run(self) -> Dict[str, Any]:
        """
        Main execution flow
        
        Returns:
            Results dictionary with all findings
        """
        logger.phase("BLACKSHANNON SCAN START")
        logger.info(f"Target: {self.target_url}")
        
        # Step 0: Connectivity test
        if not self._test_connectivity():
            logger.error("Target unreachable. Aborting scan.")
            return {'error': 'Target unreachable'}
        
        # Step 1: Initialize agents based on config
        self._initialize_agents()
        
        # Step 2: Run all agents
        self._run_agents()
        
        # Step 3: Aggregate results
        results = self._aggregate_results()
        
        # Step 4: Show summary
        self._show_summary(results)
        
        return results
    
    def _test_connectivity(self) -> bool:
        """Test target connectivity"""
        logger.info("Testing target connectivity...")
        return self.http_client.test_connectivity(self.target_url)
    
    def _initialize_agents(self):
        """Initialize agents based on configuration"""
        logger.info("Initializing agents...")
        
        # Check which attacks are enabled
        attacks = self.config.get('attacks', {})
        
        # SQLi Agent
        if attacks.get('sqli', {}).get('enabled', True):
            sqli_agent = SQLiAgent(
                target_url=self.target_url,
                llm_strategy=self.llm,
                http_client=self.http_client,
                prompt_manager=self.prompt_manager,
                config=attacks.get('sqli', {})
            )
            self.agents.append(sqli_agent)
            logger.info("✓ SQLi Agent added")
        
        # Future agents will be added here
        # if attacks.get('xss', {}).get('enabled', False):
        #     xss_agent = XSSAgent(...)
        #     self.agents.append(xss_agent)
        
        logger.success(f"{len(self.agents)} agent(s) initialized")
    
    def _run_agents(self):
        """Run all enabled agents"""
        logger.phase("RUNNING SECURITY TESTS")
        
        for i, agent in enumerate(self.agents, 1):
            logger.info(f"Running agent {i}/{len(self.agents)}: {agent.agent_name}")
            
            try:
                findings = agent.run()
                self.all_findings.extend(findings)
                
                stats = agent.get_stats()
                logger.info(
                    f"{agent.agent_name} complete: "
                    f"{stats['tests_run']} tests, "
                    f"{stats['vulnerabilities_found']} findings"
                )
                
            except Exception as e:
                logger.error(f"{agent.agent_name} failed: {e}")
    
    def _aggregate_results(self) -> Dict[str, Any]:
        """Aggregate results from all agents"""
        # Separate findings by status
        exploited = [f for f in self.all_findings if f.status == "EXPLOITED"]
        potential = [f for f in self.all_findings if f.status == "POTENTIAL"]
        
        # Calculate LLM costs
        llm_stats = {}
        if isinstance(self.llm, HybridStrategy):
            llm_stats = self.llm.get_stats()
        
        results = {
            'target_url': self.target_url,
            'total_findings': len(self.all_findings),
            'exploited': len(exploited),
            'potential': len(potential),
            'findings': {
                'exploited': exploited,
                'potential': potential
            },
            'llm_stats': llm_stats,
            'http_stats': self.http_client.get_stats()
        }
        
        return results
    
    def _show_summary(self, results: Dict[str, Any]):
        """Show scan summary"""
        logger.phase("SCAN COMPLETE")
        
        logger.info(f"Total Findings: {results['total_findings']}")
        logger.info(f"  └─ Exploited: {results['exploited']}")
        logger.info(f"  └─ Potential: {results['potential']}")
        
        # LLM stats
        llm_stats = results.get('llm_stats', {})
        if llm_stats:
            logger.info(f"LLM Usage:")
            logger.info(f"  └─ Total Cost: ${llm_stats.get('total_cost', 0):.2f}")
            logger.info(f"  └─ DeepSeek Calls: {llm_stats.get('deepseek_calls', 0)}")
            logger.info(f"  └─ Claude Calls: {llm_stats.get('claude_calls', 0)}")
        
        # HTTP stats
        http_stats = results.get('http_stats', {})
        logger.info(f"HTTP Requests: {http_stats.get('total_requests', 0)}")
        
        # Show critical findings
        exploited = results['findings']['exploited']
        if exploited:
            logger.warning("\n⚠️  CRITICAL VULNERABILITIES FOUND:")
            for finding in exploited:
                logger.error(f"  • {finding.id}: {finding.type} at {finding.endpoint}")
