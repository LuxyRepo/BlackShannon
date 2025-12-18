"""
Markdown Report Generator
Generates professional Markdown reports
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from ..agents.base_agent import Finding


class MarkdownReporter:
    """Generate Markdown reports"""
    
    def __init__(self, output_dir: str = "./workspace/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, results: Dict[str, Any]) -> Path:
        """
        Generate complete Markdown report
        
        Args:
            results: Results from orchestrator
        
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"scan_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            # Header
            f.write(self._generate_header(results))
            
            # Executive Summary
            f.write(self._generate_executive_summary(results))
            
            # Exploited Vulnerabilities
            exploited = results['findings']['exploited']
            if exploited:
                f.write(self._generate_exploited_section(exploited))
            
            # Potential Vulnerabilities
            potential = results['findings']['potential']
            if potential:
                f.write(self._generate_potential_section(potential))
            
            # Recommendations
            f.write(self._generate_recommendations())
            
            # Appendix
            f.write(self._generate_appendix(results))
        
        return report_path
    
    def _generate_header(self, results: Dict[str, Any]) -> str:
        """Generate report header"""
        return f"""# BlackShannon Security Assessment Report

**Target:** {results['target_url']}  
**Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tool:** BlackShannon v1.0  
**Methodology:** Shannon-Inspired Black-Box Testing

---

"""
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate executive summary"""
        risk_level = "🔴 CRITICAL" if results['exploited'] > 0 else "🟢 LOW"
        
        return f"""## Executive Summary

**Overall Risk Level:** {risk_level}

### Key Findings

- **Total Vulnerabilities:** {results['total_findings']}
  - **Exploited (Verified):** {results['exploited']}
  - **Potential (Manual Review):** {results['potential']}

### Assessment Overview

This report documents a systematic black-box security assessment performed using BlackShannon,
an AI-powered security scanner following Shannon's proof-based methodology.

---

"""
    
    def _generate_exploited_section(self, findings: List[Finding]) -> str:
        """Generate exploited vulnerabilities section"""
        section = """## Verified Vulnerabilities (EXPLOITED)

These vulnerabilities have been successfully exploited with concrete proof of impact.

"""
        
        for finding in findings:
            section += f"""### {finding.id}: {finding.type}

**Severity:** {finding.severity}  
**Location:** `{finding.endpoint}`  
**Status:** ✅ EXPLOITED

**Description:**
{finding.description}

**Evidence:**
```
{self._format_evidence(finding.evidence)}
```

**Remediation:**
{finding.remediation or 'See general recommendations below.'}

---

"""
        
        return section
    
    def _generate_potential_section(self, findings: List[Finding]) -> str:
        """Generate potential vulnerabilities section"""
        section = """## Potential Vulnerabilities (Require Manual Review)

These findings show suspicious indicators but require manual verification.

"""
        
        for finding in findings:
            section += f"""### {finding.id}: {finding.type}

**Location:** `{finding.endpoint}`  
**Status:** ⚠️ POTENTIAL

**Description:**
{finding.description}

**Next Steps:**
- Manual verification required
- Review with security expert
- Test in controlled environment

---

"""
        
        return section
    
    def _generate_recommendations(self) -> str:
        """Generate remediation recommendations"""
        return """## Remediation Recommendations

### Immediate Actions (Critical)

1. **Input Validation**
   - Implement whitelist-based validation for all user inputs
   - Reject special characters unless explicitly required
   - Validate data types and formats

2. **Parameterized Queries**
   - Use prepared statements for all database queries
   - Never concatenate user input into SQL queries
   - Apply principle of least privilege for database access

3. **Output Encoding**
   - HTML encode all user-controlled data before display
   - Use context-aware encoding (HTML, JavaScript, URL, etc.)
   - Implement Content Security Policy (CSP)

### Long-term Improvements

1. **Security Training**
   - Train developers on secure coding practices
   - Conduct regular security awareness sessions
   - Implement secure SDLC

2. **Defense in Depth**
   - Deploy Web Application Firewall (WAF)
   - Implement intrusion detection/prevention
   - Enable comprehensive logging and monitoring
   - Regular penetration testing

3. **Compliance & Standards**
   - Follow OWASP Top 10 guidelines
   - Implement security headers
   - Regular security audits
   - Bug bounty program

---

"""
    
    def _generate_appendix(self, results: Dict[str, Any]) -> str:
        """Generate appendix with technical details"""
        llm_stats = results.get('llm_stats', {})
        http_stats = results.get('http_stats', {})
        
        return f"""## Appendix

### Technical Details

**LLM Usage:**
- Total Cost: ${llm_stats.get('total_cost', 0):.2f}
- DeepSeek Calls: {llm_stats.get('deepseek_calls', 0)}
- Claude Calls: {llm_stats.get('claude_calls', 0)}

**HTTP Statistics:**
- Total Requests: {http_stats.get('total_requests', 0)}
- Errors: {http_stats.get('errors', 0)}
- Success Rate: {http_stats.get('success_rate', 0):.1f}%

### Methodology

BlackShannon follows a systematic 4-phase approach inspired by Shannon:

1. **Reconnaissance:** Target fingerprinting and endpoint discovery
2. **Analysis:** Identify potential vulnerabilities using AI reasoning
3. **Exploitation:** Proof-based validation with actual exploitation attempts
4. **Reporting:** Professional documentation with reproducible PoCs

### Tools Used

- LLM: DeepSeek + Claude (Hybrid Strategy)
- HTTP Client: Custom smart client with retry logic
- Browser: Playwright (for JavaScript-heavy apps)

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Tool:** BlackShannon v1.0
"""
    
    def _format_evidence(self, evidence: Dict[str, Any]) -> str:
        """Format evidence dictionary for display"""
        lines = []
        for key, value in evidence.items():
            if key == 'llm_analysis':
                continue  # Skip long LLM output
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
