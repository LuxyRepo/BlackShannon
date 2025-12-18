"""
Base Agent
Abstract class for all agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from ..llm import HybridStrategy, LLMMessage, TaskComplexity
from ..llm.prompt_manager import PromptManager
from ..tools.http_client import HTTPClient
from ..core.logger import get_logger

logger = get_logger()


@dataclass
class Finding:
    """Represents a security finding"""
    id: str
    type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str    # EXPLOITED, POTENTIAL, FALSE_POSITIVE
    endpoint: str
    description: str
    evidence: Dict[str, Any]
    remediation: Optional[str] = None


class BaseAgent(ABC):
    """
    Base class for all security testing agents
    
    Each agent is specialized in one attack type (SQLi, XSS, etc.)
    and follows Shannon's methodology
    """
    
    def __init__(
        self,
        target_url: str,
        llm_strategy: HybridStrategy,
        http_client: HTTPClient,
        prompt_manager: PromptManager,
        config: Dict[str, Any]
    ):
        self.target_url = target_url
        self.llm = llm_strategy
        self.http = http_client
        self.prompts = prompt_manager
        self.config = config
        
        # Agent state
        self.findings: List[Finding] = []
        self.tested_endpoints: List[str] = []
        
        # Statistics
        self.tests_run = 0
        self.vulnerabilities_found = 0
        
        # Agent metadata
        self.agent_type = self.__class__.__name__.replace('Agent', '')
        self.agent_name = f"{self.agent_type} Agent"
        
        logger.info(f"{self.agent_name} initialized for {target_url}")
    
    @abstractmethod
    def run(self) -> List[Finding]:
        """
        Main execution method
        Must be implemented by each agent
        
        Returns:
            List of findings (vulnerabilities discovered)
        """
        pass
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """
        Analysis phase (Shannon Phase 2)
        Identify potential vulnerabilities
        
        Returns:
            Analysis results with potential targets
        """
        pass
    
    @abstractmethod
    def exploit(self, target: Dict[str, Any]) -> Optional[Finding]:
        """
        Exploitation phase (Shannon Phase 3)
        Attempt to exploit a specific target
        
        Args:
            target: Target to exploit (endpoint, parameter, etc.)
        
        Returns:
            Finding if exploited, None if not
        """
        pass
    
    def _call_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        task_type: Optional[str] = None,
        complexity: Optional[TaskComplexity] = None,
        **kwargs
    ) -> str:
        """
        Helper to call LLM with prompts
        
        Args:
            system_prompt: System prompt text
            user_prompt: User prompt text
            task_type: Type of task for routing
            complexity: Task complexity
        
        Returns:
            LLM response content
        """
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]
        
        response = self.llm.route(
            messages=messages,
            task_type=task_type,
            complexity=complexity,
            **kwargs
        )
        
        return response.content
    
    def _classify_finding(
        self,
        endpoint: str,
        evidence: Dict[str, Any]
    ) -> str:
        """
        Classify finding as EXPLOITED, POTENTIAL, or FALSE_POSITIVE
        
        Args:
            endpoint: Tested endpoint
            evidence: Evidence collected
        
        Returns:
            Classification status
        """
        # Check if we have concrete data extraction
        if evidence.get('data_extracted'):
            return "EXPLOITED"
        
        # Check if confirmed but blocked
        if evidence.get('confirmed') and evidence.get('blocker'):
            # Determine if blocker is security control or external factor
            blocker_type = evidence.get('blocker_type', 'unknown')
            if blocker_type == 'security_control':
                return "FALSE_POSITIVE"
            else:
                return "POTENTIAL"
        
        # Default to false positive
        return "FALSE_POSITIVE"
    
    def add_finding(
        self,
        finding_id: str,
        finding_type: str,
        severity: str,
        status: str,
        endpoint: str,
        description: str,
        evidence: Dict[str, Any],
        remediation: Optional[str] = None
    ):
        """Add a finding to the results"""
        finding = Finding(
            id=finding_id,
            type=finding_type,
            severity=severity,
            status=status,
            endpoint=endpoint,
            description=description,
            evidence=evidence,
            remediation=remediation
        )
        
        self.findings.append(finding)
        self.vulnerabilities_found += 1
        
        logger.success(
            f"Finding added: {finding_id} - {status} "
            f"({severity} severity)"
        )
    
    def get_findings_by_status(self, status: str) -> List[Finding]:
        """Get findings filtered by status"""
        return [f for f in self.findings if f.status == status]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "agent": self.agent_name,
            "tests_run": self.tests_run,
            "endpoints_tested": len(self.tested_endpoints),
            "vulnerabilities_found": self.vulnerabilities_found,
            "exploited": len(self.get_findings_by_status("EXPLOITED")),
            "potential": len(self.get_findings_by_status("POTENTIAL")),
            "false_positives": len(self.get_findings_by_status("FALSE_POSITIVE")),
        }
