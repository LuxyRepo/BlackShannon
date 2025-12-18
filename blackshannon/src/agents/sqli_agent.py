"""
SQL Injection Agent
Specialized agent for SQL injection testing
"""

from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from datetime import datetime
from .base_agent import BaseAgent, Finding
from ..llm import TaskComplexity
from ..core.logger import get_logger

logger = get_logger()


class SQLiAgent(BaseAgent):
    """
    SQL Injection Testing Agent
    
    Follows Shannon methodology:
    - Phase 1: Already done by fingerprinting
    - Phase 2: Analyze potential SQLi targets (this agent)
    - Phase 3: Exploit confirmed targets
    - Phase 4: Report findings
    """
    
    # Common parameters that often have SQLi
    COMMON_SQLI_PARAMS = [
        'id', 'user', 'username', 'email', 'search', 'q', 'query',
        'page', 'product', 'category', 'item', 'order', 'sort',
        'filter', 'name', 'pid', 'uid', 'cid'
    ]
    
    # Common endpoints to test
    COMMON_SQLI_ENDPOINTS = [
        '/search', '/api/search', '/rest/search',
        '/products', '/api/products', '/rest/products',
        '/users', '/api/users', '/rest/users',
        '/items', '/api/items', '/rest/items',
        '/admin', '/login', '/api/login',
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # SQLi-specific state
        self.discovered_databases = []
        self.extracted_tables = []
        
        # Load system prompt
        self.system_prompt = self.prompts.load_system_prompt(
            'sqli_exploit',
            variables={
                'TARGET_URL': self.target_url,
                'TARGET_DOMAIN': urlparse(self.target_url).netloc,
                'TEST_DATE': datetime.now().strftime('%Y-%m-%d'),
                'TARGET_DETAILS': 'Black-box testing without source code access'
            }
        )
        
        logger.info("SQLi Agent ready")
    
    def run(self) -> List[Finding]:
        """
        Main execution: Analyze + Exploit
        
        Returns:
            List of findings
        """
        logger.phase("SQL INJECTION TESTING")
        
        # Step 1: Analyze for potential SQLi targets
        logger.info("Step 1: Analyzing for SQL injection targets...")
        analysis = self.analyze()
        
        potential_targets = analysis.get('targets', [])
        logger.info(f"Found {len(potential_targets)} potential SQLi targets")
        
        # Step 2: Exploit each target
        logger.info("Step 2: Attempting exploitation...")
        for i, target in enumerate(potential_targets, 1):
            logger.info(f"Testing target {i}/{len(potential_targets)}: {target['endpoint']}")
            
            finding = self.exploit(target)
            
            if finding and finding.status == "EXPLOITED":
                logger.success(f"✓ Exploited: {target['endpoint']}")
            elif finding and finding.status == "POTENTIAL":
                logger.warning(f"⚠ Potential: {target['endpoint']}")
            else:
                logger.info(f"✗ Not exploitable: {target['endpoint']}")
        
        # Step 3: Summary
        stats = self.get_stats()
        logger.info(
            f"SQLi testing complete: "
            f"{stats['exploited']} exploited, "
            f"{stats['potential']} potential, "
            f"{stats['false_positives']} false positives"
        )
        
        return self.findings
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze phase: Identify potential SQLi targets
        
        Returns:
            Dictionary with potential targets
        """
        targets = []
        
        # Strategy 1: Test common endpoints
        logger.info("Testing common SQLi endpoints...")
        for endpoint in self.COMMON_SQLI_ENDPOINTS:
            url = urljoin(self.target_url, endpoint)
            
            # Test with common parameters
            for param in self.COMMON_SQLI_PARAMS[:3]:  # Test top 3 params
                target = {
                    'endpoint': f"{url}?{param}=",
                    'url': url,
                    'parameter': param,
                    'method': 'GET'
                }
                
                # Quick test for existence
                response = self.http.get(url, params={param: 'test'})
                
                if response.status_code not in [404, 500]:
                    targets.append(target)
                    logger.debug(f"Added target: {url}?{param}=")
                
                self.tests_run += 1
        
        # Strategy 2: Test root with common params
        logger.info("Testing root endpoint with common parameters...")
        for param in self.COMMON_SQLI_PARAMS[:5]:
            target = {
                'endpoint': f"{self.target_url}?{param}=",
                'url': self.target_url,
                'parameter': param,
                'method': 'GET'
            }
            
            response = self.http.get(self.target_url, params={param: 'test'})
            
            if response.status_code == 200 and len(response.body) > 100:
                targets.append(target)
                logger.debug(f"Added target: {self.target_url}?{param}=")
            
            self.tests_run += 1
        
        logger.info(f"Analysis complete: {len(targets)} targets identified")
        
        return {
            'targets': targets,
            'total_tested': self.tests_run
        }
    
    def exploit(self, target: Dict[str, Any]) -> Optional[Finding]:
        """
        Exploit phase: Attempt to exploit specific target
        
        Args:
            target: Target dict with endpoint, parameter, etc.
        
        Returns:
            Finding if vulnerability found, None otherwise
        """
        endpoint = target['endpoint']
        url = target['url']
        param = target['parameter']
        
        logger.debug(f"Exploiting: {endpoint}")
        
        # Track this endpoint
        self.tested_endpoints.append(endpoint)
        
        # Build context for LLM
        context = self._build_exploit_context(target)
        
        # Load task prompt
        task_prompt = self.prompts.load_task_prompt(
            'sqli_test_endpoint',
            variables={
                'ENDPOINT_URL': url,
                'PARAMETER_NAME': param,
                'HTTP_METHOD': target.get('method', 'GET'),
                'FINGERPRINT_CONTEXT': context
            }
        )
        
        # Call LLM to perform exploitation
        logger.debug("Calling LLM for exploitation strategy...")
        
        try:
            llm_response = self._call_llm(
                system_prompt=self.system_prompt,
                user_prompt=task_prompt,
                task_type="exploitation_planning",
                complexity=TaskComplexity.COMPLEX
            )
            
            # Parse LLM response for results
            evidence = self._parse_exploitation_response(llm_response, target)
            
            # Classify finding
            status = self._classify_finding(endpoint, evidence)
            
            # If not a false positive, create finding
            if status != "FALSE_POSITIVE":
                finding_id = f"SQLI-{len(self.findings) + 1:03d}"
                
                self.add_finding(
                    finding_id=finding_id,
                    finding_type="SQL Injection",
                    severity=evidence.get('severity', 'HIGH'),
                    status=status,
                    endpoint=endpoint,
                    description=evidence.get('description', 'SQL Injection vulnerability'),
                    evidence=evidence,
                    remediation="Use parameterized queries; implement input validation; apply least privilege principle for database access"
                )
                
                return self.findings[-1]
            
            return None
            
        except Exception as e:
            logger.error(f"Exploitation error for {endpoint}: {e}")
            return None
    
    def _build_exploit_context(self, target: Dict[str, Any]) -> str:
        """
        Build context for exploitation
        
        Args:
            target: Target information
        
        Returns:
            Context string for LLM
        """
        # Perform basic fingerprinting
        url = target['url']
        param = target['parameter']
        
        # Test basic response
        response = self.http.get(url, params={param: 'test'})
        
        context_parts = [
            "## Fingerprinting Context",
            "",
            f"**Endpoint Response:**",
            f"- Status Code: {response.status_code}",
            f"- Response Time: {response.response_time:.2f}s",
            f"- Content Length: {len(response.body)} bytes",
            "",
        ]
        
        # Check for tech indicators
        server = response.headers.get('Server', 'Unknown')
        powered_by = response.headers.get('X-Powered-By', 'Unknown')
        
        context_parts.extend([
            f"**Technology Stack (inferred):**",
            f"- Server: {server}",
            f"- Framework: {powered_by}",
            "",
        ])
        
        # Test for error
        error_response = self.http.get(url, params={param: "test'"})
        
        if 'sql' in error_response.body.lower() or 'syntax' in error_response.body.lower():
            context_parts.append("**⚠️ INITIAL INDICATOR:** SQL error detected in response with single quote")
        
        return "\n".join(context_parts)
    
    def _parse_exploitation_response(
        self,
        llm_response: str,
        target: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse LLM exploitation response into structured evidence
        
        Args:
            llm_response: Response from LLM
            target: Target that was tested
        
        Returns:
            Evidence dictionary
        """
        evidence = {
            'endpoint': target['endpoint'],
            'parameter': target['parameter'],
            'llm_analysis': llm_response,
            'confirmed': False,
            'data_extracted': False,
        }
        
        # Parse response for indicators
        response_lower = llm_response.lower()
        
        # Check if LLM reported exploitation
        if 'exploited' in response_lower or 'extracted' in response_lower:
            evidence['confirmed'] = True
            
            # Check for data extraction proof
            if any(keyword in response_lower for keyword in [
                'table names:', 'extracted data:', 'database version:',
                'user records:', 'columns:', 'rows:'
            ]):
                evidence['data_extracted'] = True
        
        # Check for blockers
        if 'blocked' in response_lower or 'waf' in response_lower:
            evidence['blocker'] = True
            
            # Determine blocker type
            if 'waf' in response_lower or 'filter' in response_lower or 'forbidden' in response_lower:
                evidence['blocker_type'] = 'security_control'
            else:
                evidence['blocker_type'] = 'external_factor'
        
        # Extract severity if mentioned
        if 'critical' in response_lower:
            evidence['severity'] = 'CRITICAL'
        elif 'high' in response_lower:
            evidence['severity'] = 'HIGH'
        else:
            evidence['severity'] = 'MEDIUM'
        
        # Extract description
        lines = llm_response.split('\n')
        for line in lines:
            if 'summary' in line.lower() or 'description' in line.lower():
                evidence['description'] = line.strip()
                break
        
        if 'description' not in evidence:
            evidence['description'] = 'SQL Injection vulnerability detected'
        
        return evidence
