# 🎯 BlackShannon

**AI-Powered Penetration Testing Framework**

BlackShannon is an ethical security testing tool that combines Large Language Models (DeepSeek + Claude) with traditional penetration testing techniques to automate vulnerability discovery and exploitation. Inspired by Shannon's information theory, it uses intelligent reasoning to analyze targets and craft precision exploits.

---

## ⚠️ LEGAL DISCLAIMER

**READ THIS BEFORE USING**

BlackShannon is designed for **authorized security testing only**.

### ✅ You MUST:
- Only test systems you **own** or have **explicit written authorization** to test
- Comply with all applicable laws and regulations
- Use responsibly and ethically
- Respect rate limits and target resources

### ❌ You MUST NOT:
- Test unauthorized systems
- Use for illegal activities
- Cause damage, disruption, or data loss
- Violate terms of service

**The developers assume NO responsibility for misuse. You are solely responsible for your actions.**

---

## 📋 Table of Contents

1. [Project Status](#project-status)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [How It Works](#how-it-works)
8. [Development Guide](#development-guide)
9. [What's Implemented](#whats-implemented)
10. [What's Missing](#whats-missing)
11. [Roadmap](#roadmap)
12. [Troubleshooting](#troubleshooting)
13. [Contributing](#contributing)

---

## 🚀 Project Status

**Version:** 0.1 (Proof of Concept)  
**Status:** ✅ Core functionality complete, ready for testing  
**Last Updated:** December 2024

### Current State:
- ✅ **Core System**: Config, Logger, Orchestrator - COMPLETE
- ✅ **LLM Integration**: DeepSeek + Claude with hybrid routing - COMPLETE
- ✅ **Fingerprinting**: Advanced tech stack detection - COMPLETE
- ✅ **SQL Injection Agent**: Detection + Exploitation - COMPLETE
- ✅ **Reporting**: Markdown reports with evidence - COMPLETE
- ✅ **CLI Interface**: Rich UI with progress tracking - COMPLETE

### What Works Now:
- Full fingerprinting (server, CMS, framework, database, WAF detection)
- SQL injection testing with LLM-powered exploitation
- Hybrid LLM strategy (DeepSeek for detection, Claude for complex reasoning)
- Comprehensive reporting with proof-of-concept evidence

### What's Next:
- Additional vulnerability agents (XSS, LFI, Auth Bypass)
- Unit tests and integration tests
- Enhanced error handling and retry logic
- Multi-threading for faster scans

---

## 🎯 Features

### 🔍 Intelligent Fingerprinting
- **Server Detection**: nginx, Apache, IIS identification with versions
- **CMS Detection**: WordPress, Joomla, Drupal, Magento, Shopify
- **Framework Detection**: Laravel, Django, Flask, Express, Spring, ASP.NET
- **Database Inference**: MySQL, PostgreSQL, MSSQL, Oracle, SQLite, MongoDB
- **WAF Detection**: Cloudflare, Akamai, AWS WAF, ModSecurity, Imperva, F5
- **Frontend Detection**: React, Vue, Angular, jQuery, Bootstrap, Tailwind

### 🤖 AI-Powered Testing
- **Hybrid LLM Strategy**: Routes tasks to optimal model
  - DeepSeek (deepseek-chat): Fast detection and simple tasks
  - Claude Sonnet 4: Complex reasoning and exploitation
- **Context-Aware**: Uses fingerprint data to craft database-specific payloads
- **Iterative Learning**: Adapts based on target responses

### 🎯 SQL Injection Testing
- **Two-Stage Approach**:
  1. **Detection** (DeepSeek): Fast identification of vulnerable parameters
  2. **Exploitation** (Claude): Deep reasoning for data extraction
- **Database-Specific Payloads**: Automatically adapts to MySQL, PostgreSQL, MSSQL
- **Classification System**: EXPLOITED / POTENTIAL / FALSE_POSITIVE
- **Evidence Collection**: Saves exact payloads and responses

### 📊 Comprehensive Reporting
- **Markdown Reports**: Human-readable with technical details
- **Executive Summary**: High-level findings
- **Detailed Evidence**: Every request/response logged
- **Remediation Advice**: Actionable fix recommendations
- **Structured Logs**: JSON-formatted for parsing

---

## 🏗️ Architecture

### Directory Structure

```
blackshannon/
│
├── README.md                         # This file
├── DISCLAIMER.md                     # Legal disclaimer
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
│
├── config/
│   └── default_config.yaml           # Configuration settings
│
├── prompts/                          # LLM prompt templates
│   ├── system/
│   │   └── sqli_exploit.txt          # SQLi system prompt
│   ├── shared/
│   │   ├── _target_info.txt          # Target context template
│   │   ├── _rules.txt                # Testing rules
│   │   ├── _classification.txt       # Finding classification
│   │   └── _tool_usage.txt           # Tool usage instructions
│   └── tasks/
│       └── sqli_test_endpoint.txt    # Task-specific prompts
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/                         # Core system components
│   │   ├── __init__.py
│   │   ├── config_manager.py         # YAML config loader
│   │   ├── logger.py                 # Logging system
│   │   └── orchestrator.py           # Main workflow coordinator
│   │
│   ├── llm/                          # LLM integration layer
│   │   ├── __init__.py
│   │   ├── base_llm.py               # Abstract base class
│   │   ├── deepseek_client.py        # DeepSeek API client
│   │   ├── claude_client.py          # Claude API client
│   │   ├── hybrid_strategy.py        # Model routing logic
│   │   └── prompt_manager.py         # Prompt template manager
│   │
│   ├── agents/                       # Vulnerability testing agents
│   │   ├── __init__.py
│   │   ├── base_agent.py             # Abstract agent class
│   │   └── sqli_agent.py             # SQL Injection agent
│   │
│   ├── tools/                        # Utility tools
│   │   ├── __init__.py
│   │   ├── http_client.py            # Smart HTTP client
│   │   └── fingerprint.py            # Target fingerprinting
│   │
│   └── reporting/                    # Report generation
│       ├── __init__.py
│       └── markdown_reporter.py      # Markdown report generator
│
├── workspace/                        # Output directory (gitignored)
│   ├── logs/                         # Execution logs
│   ├── reports/                      # Generated reports
│   └── evidence/                     # Evidence files
│
└── cli.py                            # Command-line interface
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI (cli.py)                        │
│                    Entry Point + UI                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestrator                              │
│              Workflow Coordination                          │
└─┬───────────────┬──────────────┬────────────────┬──────────┘
  │               │              │                │
  │               │              │                │
  ▼               ▼              ▼                ▼
┌─────────┐  ┌──────────┐  ┌─────────┐     ┌──────────┐
│ Config  │  │  Logger  │  │Fingerpr.│     │ Reporter │
│ Manager │  │          │  │         │     │          │
└─────────┘  └──────────┘  └────┬────┘     └──────────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │HTTP Client  │
                          │             │
                          └─────────────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │   Agents    │
                          │  (SQLi...)  │
                          └──────┬──────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │ LLM Layer   │
                          │ (Hybrid)    │
                          └──────┬──────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
              ┌──────────┐            ┌──────────┐
              │ DeepSeek │            │  Claude  │
              │ (detect) │            │ (exploit)│
              └──────────┘            └──────────┘
```

### Data Flow

```
1. User → CLI (--target URL)
2. CLI → Orchestrator.execute(target)
3. Orchestrator → Fingerprint.analyze_target(URL)
4. Fingerprint → HTTP Client → Target
5. Fingerprint → Returns: {server, cms, db, waf, ...}
6. Orchestrator → SQLi Agent.execute(URL, fingerprint_context)
7. SQLi Agent → Stage 1: Detection
   ├─ Prompt Manager → Loads prompts + substitutes {{placeholders}}
   ├─ Hybrid Strategy → Routes to DeepSeek (simple task)
   ├─ DeepSeek → Analyzes parameters
   └─ Returns: [vulnerable_params]
8. SQLi Agent → Stage 2: Exploitation (per vulnerable param)
   ├─ Hybrid Strategy → Routes to Claude (complex reasoning)
   ├─ Claude → Generates DB-specific payloads
   ├─ HTTP Client → Sends payloads to target
   ├─ Claude → Analyzes responses
   └─ Returns: {exploited: true, data: [...]}
9. Orchestrator → Reporter.generate_report(findings)
10. Reporter → Saves to workspace/reports/
11. CLI → Displays summary to user
```

---

## 🛠️ Installation

### Prerequisites

- **Python**: 3.8 or higher
- **API Keys**: 
  - DeepSeek API key ([Get it here](https://platform.deepseek.com))
  - Anthropic Claude API key ([Get it here](https://console.anthropic.com))

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/blackshannon.git
cd blackshannon
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `requests` - HTTP client
- `pyyaml` - Config file parsing
- `anthropic` - Claude API
- `openai` - DeepSeek API (uses OpenAI-compatible endpoint)
- `python-dotenv` - Environment variables
- `rich` - Terminal UI

### Step 3: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit with your API keys
nano .env
```

Add your API keys:
```
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
```

### Step 4: Create Workspace Directories

```bash
mkdir -p workspace/logs workspace/reports workspace/evidence
```

### Step 5: Verify Installation

```bash
python cli.py --help
```

You should see the help message with available options.

---

## ⚙️ Configuration

### Main Config File: `config/default_config.yaml`

```yaml
# LLM Configuration
llm:
  deepseek:
    model: "deepseek-chat"
    base_url: "https://api.deepseek.com"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30
  
  claude:
    model: "claude-sonnet-4-20250514"
    temperature: 0.7
    max_tokens: 4000
    timeout: 60
  
  hybrid_strategy:
    simple_task_threshold: 0.3
    complex_task_threshold: 0.7

# HTTP Client Configuration
http:
  timeout: 30
  max_retries: 3
  retry_delay: 1
  user_agents:
    - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    - "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Logging Configuration
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "workspace/logs/blackshannon_{timestamp}.log"

# Workspace Paths
workspace:
  logs: "workspace/logs"
  reports: "workspace/reports"
  evidence: "workspace/evidence"
```

### Environment Variables (`.env`)

```
# Required
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx

# Optional overrides
LOG_LEVEL=DEBUG
HTTP_TIMEOUT=60
```

---

## 🚀 Usage

### Basic Scan

```bash
python cli.py --target https://example.com
```

### Verbose Mode (Debug Logging)

```bash
python cli.py --target https://example.com --verbose
```

### Custom Config File

```bash
python cli.py --target https://example.com --config custom_config.yaml
```

### Example Output

```
╭─────────────────────────────────────╮
│        BLACKSHANNON v0.1            │
│    Ethical Security Testing Tool    │
╰─────────────────────────────────────╯

⚠️  WARNING: Only test authorized systems!
Press Enter to confirm you have authorization...

[*] Target: https://example.com
[*] Starting orchestrator...
[*] Fingerprinting target...
[+] Server: nginx/1.18.0
[+] Backend: PHP 7.4
[+] Database: mysql (confidence: high)
[+] CMS: WordPress 5.8
[+] WAF: Not detected
[+] Tech Stack: nginx | PHP 7.4 | WordPress 5.8 | DB:mysql
[*] Starting SQLi testing...
[*] Testing parameter: id
[+] Vulnerable parameter found: id
[*] Exploiting with Claude...
[+] Database type: MySQL 5.7.32
[+] Database user: webuser@localhost
[+] Tables found: users, posts, comments
[+] EXPLOITED: Successfully extracted data
[*] Generating report...
[+] Report saved: workspace/reports/scan_report_20241218_143022.md
[+] Scan complete! Found 1 vulnerability.
```

---

## 🔬 How It Works

### Phase 1: Fingerprinting

The system analyzes the target to understand its technology stack:

1. **HTTP Analysis**: Examines headers, cookies, response codes
2. **Pattern Matching**: Searches HTML for CMS/framework signatures
3. **Error Detection**: Triggers errors to identify database types
4. **Path Probing**: Checks common admin/config paths
5. **WAF Detection**: Identifies web application firewalls

**Output**: Complete tech profile used to inform exploitation

### Phase 2: Vulnerability Testing (SQL Injection)

**Stage 1 - Detection (DeepSeek):**
```
Task: Find vulnerable parameters
Model: DeepSeek (fast, cost-effective)
Process:
  1. Test common parameters (?id=, ?page=, ?search=)
  2. Send basic detection payloads ('")
  3. Analyze responses for SQL errors
  4. Return list of potentially vulnerable parameters
```

**Stage 2 - Exploitation (Claude):**
```
Task: Extract data from vulnerable parameter
Model: Claude Sonnet 4 (complex reasoning)
Process:
  1. Receive: parameter, fingerprint context, detection evidence
  2. Reason about database type and structure
  3. Generate database-specific payloads:
     - Determine column count (UNION-based)
     - Extract version, user, database name
     - Enumerate tables (information_schema)
     - Extract data (target tables)
  4. Adapt based on responses
  5. Return: Exploitation status + extracted data
```

### Phase 3: Classification

Each finding is classified:

- **EXPLOITED**: Successfully extracted data (HIGH severity)
- **POTENTIAL**: Vulnerability exists but blocked (MEDIUM severity)
- **FALSE_POSITIVE**: Not actually exploitable (INFO)

### Phase 4: Reporting

Generates comprehensive Markdown report:

```markdown
# Security Assessment Report

## Executive Summary
Found 1 HIGH severity vulnerability

## Findings

### [HIGH] SQL Injection in 'id' parameter
**URL**: https://example.com/page.php?id=1
**Parameter**: id
**Status**: EXPLOITED

**Evidence**:
Database: MySQL 5.7.32
User: webuser@localhost
Tables: users, posts, comments

**Proof of Concept**:
GET /page.php?id=1' UNION SELECT 1,2,version()-- -

**Remediation**:
1. Use parameterized queries
2. Implement input validation
3. Apply principle of least privilege
```

---

## 👨‍💻 Development Guide

### For Future Claude Sessions or Developers

This section explains how to extend BlackShannon.

### Adding a New Vulnerability Agent

**Example: XSS Agent**

1. **Create Agent File**: `src/agents/xss_agent.py`

```python
from .base_agent import BaseAgent

class XSSAgent(BaseAgent):
    def __init__(self, config, http_client, llm_strategy, prompt_manager, logger):
        super().__init__(config, http_client, llm_strategy, prompt_manager, logger)
        self.agent_name = "XSS"
    
    def execute(self, target_url, context=None):
        """
        Implement XSS testing logic
        1. Detection phase (DeepSeek)
        2. Exploitation phase (Claude)
        3. Return findings
        """
        # Your implementation here
        pass
```

2. **Create Prompts**: 
   - `prompts/system/xss_exploit.txt`
   - `prompts/tasks/xss_test_endpoint.txt`

3. **Update Orchestrator**: Add XSS agent to workflow

```python
# In orchestrator.py
from ..agents import XSSAgent

xss_agent = XSSAgent(...)
xss_findings = xss_agent.execute(target_url, fingerprint)
```

4. **Test**: Create `test_xss_agent.py`

### Extending Fingerprint

**Add new CMS detection:**

In `src/tools/fingerprint.py`:

```python
self.cms_patterns = {
    # ... existing patterns
    "prestashop": {
        "patterns": [r"/themes/", r"prestashop"],
        "paths": ["/admin-dev"],
        "headers": [],
        "cookies": ["PrestaShop-"]
    }
}
```

### Modifying LLM Behavior

**Change routing logic:**

In `src/llm/hybrid_strategy.py`:

```python
def select_model(self, task_type, complexity):
    if task_type == "xss_detection":
        return self.deepseek_client  # Fast detection
    elif complexity > 0.8:
        return self.claude_client  # Very complex
    # ... your logic
```

### Prompt Engineering

Prompts use **placeholder substitution**:

**Template** (`prompts/shared/_target_info.txt`):
```
TARGET: {{url}}
SERVER: {{server}}
DATABASE: {{database_type}}
```

**Usage** (in agent):
```python
context = {
    "url": target_url,
    "server": fingerprint["server"]["name"],
    "database_type": fingerprint["database"]["type"]
}
prompt = self.prompt_manager.get_prompt("shared/_target_info.txt", context)
```

---

## ✅ What's Implemented

### Core System (100%)
- ✅ `config_manager.py` - YAML configuration loading
- ✅ `logger.py` - Structured logging with rotation
- ✅ `orchestrator.py` - Workflow coordination
- ✅ All `__init__.py` files with proper exports

### LLM Layer (100%)
- ✅ `base_llm.py` - Abstract interface
- ✅ `deepseek_client.py` - DeepSeek API integration
- ✅ `claude_client.py` - Claude API integration
- ✅ `hybrid_strategy.py` - Intelligent model routing
- ✅ `prompt_manager.py` - Template management with placeholders

### Prompt System (100%)
- ✅ System prompts (SQLi)
- ✅ Shared prompts (target info, rules, classification)
- ✅ Task prompts (endpoint testing)

### Tools (100%)
- ✅ `http_client.py` - HTTP client with retry/timeout
- ✅ `fingerprint.py` - Comprehensive fingerprinting:
  - Server detection (nginx, Apache, IIS)
  - CMS detection (WordPress, Joomla, Drupal, Magento, Shopify)
  - Framework detection (Laravel, Django, Flask, Express, Spring, ASP.NET)
  - Frontend detection (React, Vue, Angular, jQuery, Bootstrap)
  - Database inference (MySQL, PostgreSQL, MSSQL, Oracle, SQLite, MongoDB)
  - WAF detection (Cloudflare, Akamai, AWS WAF, ModSecurity, Imperva, F5)

### Agents (Partial)
- ✅ `base_agent.py` - Abstract agent class
- ✅ `sqli_agent.py` - SQL Injection testing (2-stage: detection + exploitation)
- ❌ XSS Agent - Not implemented
- ❌ LFI Agent - Not implemented
- ❌ Auth Bypass Agent - Not implemented

### Reporting (100%)
- ✅ `markdown_reporter.py` - Markdown report generation
- ✅ Executive summary
- ✅ Detailed findings with evidence
- ✅ Remediation recommendations

### CLI (100%)
- ✅ `cli.py` - Command-line interface with Rich UI
- ✅ Argument parsing (--target, --verbose, --config)
- ✅ Progress indicators
- ✅ Authorization confirmation prompt

### Configuration Files (100%)
- ✅ `default_config.yaml` - All settings
- ✅ `.env.example` - Environment template
- ✅ `.gitignore` - Proper exclusions
- ✅ `requirements.txt` - All dependencies

---

## ❌ What's Missing

### Critical (Should implement before production)
- ❌ **Legal Protection**
  - Create `DISCLAIMER.md` (template provided above)
  - Add scope validation (confirm authorization)
  - Add domain whitelist/blacklist
  
- ❌ **Error Handling**
  - Comprehensive try-catch in all agents
  - Graceful degradation when LLM fails
  - Retry logic for transient failures
  
- ❌ **Security**
  - Sensitive data redaction in logs
  - API key validation at startup
  - Rate limiting per target

### Important (Quality & Reliability)
- ❌ **Testing**
  - Unit tests (`tests/` directory)
  - Integration tests (end-to-end)
  - Mock LLM responses for testing
  
- ❌ **Documentation**
  - Docstrings for all methods
  - Type hints throughout
  - API documentation
  - Video tutorials
  
- ❌ **Monitoring**
  - Token usage tracking
  - Cost estimation
  - Success rate metrics

### Nice to Have (Future Features)
- ❌ **Additional Agents**
  - XSS detection and exploitation
  - Local File Inclusion (LFI)
  - Remote Code Execution (RCE)
  - Authentication bypass
  - API fuzzing
  
- ❌ **Advanced SQLi**
  - Blind SQL injection (time-based, boolean-based)
  - Second-order SQLi
  - Advanced WAF bypass
  
- ❌ **Reporting**
  - HTML reports
  - PDF export
  - JSON export (for SIEM integration)
  - Burp Suite integration
  
- ❌ **Performance**
  - Multi-threading
  - Async HTTP requests
  - Result caching
  - Progress persistence (resume scans)
  
- ❌ **UI/UX**
  - Web dashboard
  - Real-time progress tracking
  - Historical scan comparison
  
- ❌ **Collaboration**
  - Multi-user support
  - Shared workspaces
  - Team reporting

---

## 🗺️ Roadmap

### Version 0.2 (Next Release)
- [ ] Complete error handling
- [ ] Add unit tests (80% coverage)
- [ ] Create DISCLAIMER.md
- [ ] Add scope validation
- [ ] Token usage tracking

### Version 0.3
- [ ] XSS Agent implementation
- [ ] LFI Agent implementation
- [ ] HTML report generation
- [ ] Multi-threading support

### Version 0.4
- [ ] Blind SQLi support
- [ ] WAF bypass techniques
- [ ] API fuzzing agent
- [ ] Web dashboard (optional)

### Version 1.0 (Production Ready)
- [ ] Comprehensive test suite
- [ ] Full documentation
- [ ] Security audit
- [ ] Performance optimization
- [ ] Plugin system

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

**Error**: `ImportError: cannot import name 'HTTPClient'`

**Solution**: Check class names match in files and `__init__.py`:
```bash
# Verify class name in file
grep "class HTTP" src/tools/http_client.py

# Verify import in __init__.py
cat src/tools/__init__.py
```

#### 2. API Key Errors

**Error**: `AuthenticationError: Invalid API key`

**Solution**: 
```bash
# Check .env file exists
ls -la .env

# Verify keys are set
cat .env | grep API_KEY

# Test key validity
python -c "from src.core.config_manager import ConfigManager; c=ConfigManager(); print(c.get('llm.deepseek.api_key'))"
```

#### 3. Fingerprint Fails

**Error**: Target analysis returns empty results

**Solution**:
- Check target is reachable: `curl -I https://target.com`
- Verify user-agent isn't blocked
- Check timeout settings in config
- Run with `--verbose` for debug logs

#### 4. LLM Timeout

**Error**: Request timeout after 30s

**Solution**: Increase timeout in `config/default_config.yaml`:
```yaml
llm:
  claude:
    timeout: 120  # Increase from 60
```

#### 5. Rate Limiting

**Error**: `RateLimitError: Too many requests`

**Solution**: Add delays between requests:
```yaml
http:
  request_delay: 2  # seconds between requests
```

### Debug Mode

Run with verbose logging:
```bash
# Maximum verbosity
LOG_LEVEL=DEBUG python cli.py --target https://example.com --verbose

# Check logs
tail -f workspace/logs/blackshannon_*.log
```

### Getting Help

1. Check logs in `workspace/logs/`
2. Review error messages carefully
3. Search issues on GitHub
4. Ask on discussions forum

---

## 🤝 Contributing

### Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/xss-agent`)
3. **Implement** your changes
4. **Test** thoroughly (add unit tests)
5. **Document** your code (docstrings + README)
6. **Commit** with clear messages
7. **Push** and create Pull Request

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public methods
- Keep functions under 50 lines
- Add logging for important operations

### Testing

Before submitting:
```bash
# Run tests
python -m pytest tests/

# Check style
flake8 src/
black src/ --check

# Type check
mypy src/
```

---

## 📚 References

### Documentation
- [DeepSeek API Docs](https://api-docs.deepseek.com)
- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Inspiration
- Shannon's Information Theory
- OWASP ZAP
- Burp Suite
- SQLMap

### Papers & Articles
- "Language Models for Web Security Testing" (2024)
- "AI-Assisted Penetration Testing" (2023)
- "Automated Vulnerability Discovery with LLMs" (2024)

---

## 📄 License

[Specify your license here - e.g., MIT, GPL-3.0]

---

## 👥 Authors

- **Your Name** - Initial work

---

## 🙏 Acknowledgments

- Anthropic for Claude API
- DeepSeek for their powerful language model
- OWASP community for security research
- All contributors and testers

---

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/blackshannon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/blackshannon/discussions)
- **Email**: your.email@example.com

---

**Remember: Use responsibly. Happy (ethical) hacking! 🎯**


-------------------------------------------------------------



# 🔧 BlackShannon - Development Guide

**Technical Reference for Developers and AI Assistants**

This document provides detailed technical information for continuing development on BlackShannon. If you're a developer (human or AI) picking up this project, read this first.

---

## 🎯 Quick Context

**What is BlackShannon?**
AI-powered penetration testing tool that uses LLMs (DeepSeek + Claude) to automate vulnerability discovery. Currently focuses on SQL injection with comprehensive fingerprinting.

**Current State:** PoC complete, core functionality working, ready for testing and expansion.

**Your Mission (if continuing development):**
1. Understand what exists
2. Know what's missing
3. Implement next priority features
4. Maintain code quality

---

## 📦 What's Already Built - Component Reference

### 1. Core System (`src/core/`)

#### `config_manager.py`
**Purpose:** Load and manage configuration from YAML + environment variables

**Key Methods:**
- `__init__()` - Loads `config/default_config.yaml`, merges with env vars
- `get(key_path, default=None)` - Retrieve config value (e.g., `"llm.deepseek.model"`)
- `get_api_key(service)` - Get API key from environment

**Important:**
- Uses `python-dotenv` for `.env` loading
- Validates API keys on initialization
- Supports nested key access with dot notation

**Example Usage:**
```python
config = ConfigManager()
model = config.get("llm.deepseek.model")  # "deepseek-chat"
api_key = config.get_api_key("deepseek")  # from DEEPSEEK_API_KEY
```

---

#### `logger.py`
**Purpose:** Structured logging with file + console output

**Key Functions:**
- `setup_logger(config)` - Initialize logger instance
- Logs to: `workspace/logs/blackshannon_{timestamp}.log`
- Console output: INFO and above
- File output: DEBUG and above (if verbose)

**Log Levels:**
- `DEBUG` - Detailed diagnostic info
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages (with stack traces)

**Usage:**
```python
logger = setup_logger(config)
logger.info("Starting scan")
logger.debug("Detailed debug info")
logger.error("Error occurred", exc_info=True)
```

---

#### `orchestrator.py`
**Purpose:** Main workflow coordinator - ties everything together

**Key Methods:**
- `__init__(config)` - Initialize all components
- `execute(target_url)` - Main entry point, runs full workflow

**Workflow:**
```
1. Initialize components (fingerprint, agents, reporter)
2. Run fingerprint analysis
3. Execute agents (SQLi, etc.)
4. Collect findings
5. Generate report
6. Return summary
```

**Important:**
- Handles global error catching
- Manages component lifecycle
- Passes context between components

---

### 2. LLM Layer (`src/llm/`)

#### `base_llm.py`
**Purpose:** Abstract base class for LLM clients

**Key Methods:**
- `chat(messages, temperature, max_tokens)` - Abstract, implemented by subclasses
- `count_tokens(text)` - Abstract, estimate token count
- `_retry_with_backoff(func, *args, **kwargs)` - Retry logic with exponential backoff

**Important:**
- All LLM clients inherit from this
- Provides consistent interface
- Handles retries automatically

---

#### `deepseek_client.py`
**Purpose:** DeepSeek API integration (uses OpenAI-compatible endpoint)

**Configuration:**
```yaml
llm:
  deepseek:
    model: "deepseek-chat"
    base_url: "https://api.deepseek.com"
    temperature: 0.7
    max_tokens: 2000
```

**Key Methods:**
- `chat(messages, **kwargs)` - Send request to DeepSeek
- Uses `openai` library with custom base URL

**Usage:**
```python
client = DeepSeekClient(config)
response = client.chat([
    {"role": "system", "content": "You are a security tester"},
    {"role": "user", "content": "Analyze this: ..."}
])
```

**Rate Limits:** Check DeepSeek documentation (typically generous for chat model)

---

#### `claude_client.py`
**Purpose:** Claude API integration (Anthropic)

**Configuration:**
```yaml
llm:
  claude:
    model: "claude-sonnet-4-20250514"
    temperature: 0.7
    max_tokens: 4000
```

**Key Methods:**
- `chat(messages, **kwargs)` - Send request to Claude
- Converts OpenAI-style messages to Anthropic format

**Important:**
- Handles system message extraction (Anthropic requires separate `system` parameter)
- More expensive than DeepSeek but better reasoning

**Token Limits:**
- Input: 200K tokens
- Output: 8K tokens (configured to 4K for cost)

---

#### `hybrid_strategy.py`
**Purpose:** Intelligent routing between DeepSeek and Claude

**Logic:**
```python
def select_model(self, task_type, complexity):
    if task_type == "detection":
        return self.deepseek_client  # Fast, cheap
    elif complexity > 0.7:
        return self.claude_client    # Complex reasoning
    else:
        return self.deepseek_client  # Default
```

**Task Types:**
- `"detection"` - Finding vulnerabilities → DeepSeek
- `"exploitation"` - Complex reasoning for data extraction → Claude
- `"analysis"` - Medium complexity → Based on complexity score

**Complexity Score (0-1):**
- 0.0-0.3: Simple (parameter checking)
- 0.4-0.6: Medium (basic SQL injection)
- 0.7-1.0: Complex (blind SQLi, multi-step exploitation)

---

#### `prompt_manager.py`
**Purpose:** Load and manage prompt templates with placeholder substitution

**Key Methods:**
- `get_prompt(prompt_name, context=None)` - Load prompt file, substitute placeholders
- `_load_prompt(path)` - Read prompt file from disk
- `_substitute_placeholders(prompt, context)` - Replace `{{key}}` with values

**Placeholder System:**
```
Template: "Target URL: {{url}}, Database: {{database_type}}"
Context: {"url": "https://example.com", "database_type": "mysql"}
Result: "Target URL: https://example.com, Database: mysql"
```

**Prompt File Structure:**
```
prompts/
├── system/           # System prompts (role definition)
│   └── sqli_exploit.txt
├── shared/           # Reusable components
│   ├── _target_info.txt
│   ├── _rules.txt
│   └── _classification.txt
└── tasks/            # Task-specific prompts
    └── sqli_test_endpoint.txt
```

---

### 3. Tools (`src/tools/`)

#### `http_client.py`
**Purpose:** Smart HTTP client with retry and timeout

**Key Methods:**
- `get(url, **kwargs)` - GET request
- `post(url, data, **kwargs)` - POST request
- `_make_request(method, url, **kwargs)` - Internal, handles retries

**Features:**
- Automatic retries (3 attempts by default)
- Exponential backoff
- User-Agent rotation
- Timeout handling
- Session management (cookies persist)

**Configuration:**
```yaml
http:
  timeout: 30
  max_retries: 3
  retry_delay: 1
  user_agents: [...]
```

---

#### `fingerprint.py`
**Purpose:** Comprehensive target technology detection

**Key Method:**
- `analyze_target(url)` - Returns complete tech stack dict

**Detection Capabilities:**

1. **Server Detection**
   - nginx, Apache, IIS, Tomcat, Lighttpd
   - Version extraction from headers

2. **CMS Detection**
   - WordPress, Joomla, Drupal, Magento, Shopify
   - Version detection from meta tags and patterns

3. **Framework Detection**
   - Backend: Laravel, Django, Flask, Express, Spring, ASP.NET
   - Frontend: React, Vue, Angular, jQuery, Bootstrap, Tailwind

4. **Database Detection**
   - Error-based: MySQL, PostgreSQL, MSSQL, Oracle, SQLite, MongoDB
   - Inference from backend language (PHP → MySQL)

5. **WAF Detection**
   - Cloudflare, Akamai, AWS WAF, ModSecurity, Imperva, F5

**Return Structure:**
```python
{
    "url": "https://example.com",
    "server": {"name": "nginx", "version": "1.18.0"},
    "backend": {"language": "PHP", "version": "7.4"},
    "cms": {"name": "WordPress", "version": "5.8", "confidence": "high"},
    "framework": {
        "backend": [{"name": "laravel", "confidence": "medium"}],
        "frontend": ["react", "bootstrap"]
    },
    "database": {"type": "mysql", "confidence": "high", "evidence": [...]},
    "waf": {"detected": true, "type": "cloudflare", "confidence": "high"},
    "technologies": ["nginx 1.18.0", "PHP 7.4", "WordPress 5.8", "DB:mysql"],
    "tech_stack_summary": "nginx | PHP 7.4 | WordPress 5.8 | DB:mysql",
    "fingerprint_confidence": "high"
}
```

**Algorithm:**

1. **Initial Request:** GET to target URL
2. **Header Analysis:** Extract Server, X-Powered-By, cookies
3. **Body Analysis:** Regex patterns for CMS/frameworks
4. **Error Triggering:** Send malformed requests to trigger DB errors
5. **Path Probing:** Check `/robots.txt`, `/wp-admin`, etc.
6. **Scoring:** Each detection increments score, highest wins
7. **Confidence:** Based on number of matching signals

---

### 4. Agents (`src/agents/`)

#### `base_agent.py`
**Purpose:** Abstract base class for all vulnerability agents

**Key Methods:**
- `execute(target_url, context)` - Abstract, implemented by subclasses
- Must return: `{"findings": [...], "status": "complete"}`

**Provided to Subclasses:**
- `self.config` - Configuration
- `self.http_client` - For making requests
- `self.llm_strategy` - For routing LLM calls
- `self.prompt_manager` - For loading prompts
- `self.logger` - For logging

---

#### `sqli_agent.py`
**Purpose:** SQL Injection detection and exploitation

**Two-Stage Workflow:**

**Stage 1: Detection (DeepSeek)**
```python
def _detection_stage(self, url):
    # 1. Identify testable parameters
    params = self._find_parameters(url)
    
    # 2. Test each parameter with basic payloads
    for param in params:
        payload = "' OR '1'='1"
        response = self._test_parameter(url, param, payload)
        
        # 3. Ask DeepSeek to analyze response
        llm_response = self.llm_strategy.select_model("detection").chat([
            {"role": "system", "content": sqli_detection_prompt},
            {"role": "user", "content": f"Response: {response}"}
        ])
        
        if "vulnerable" in llm_response:
            vulnerable_params.append(param)
    
    return vulnerable_params
```

**Stage 2: Exploitation (Claude)**
```python
def _exploitation_stage(self, url, param, fingerprint):
    # 1. Build context with fingerprint
    context = {
        "url": url,
        "parameter": param,
        "database_type": fingerprint["database"]["type"]
    }
    
    # 2. Load exploitation prompt
    system_prompt = self.prompt_manager.get_prompt("system/sqli_exploit.txt", context)
    
    # 3. Iterative exploitation with Claude
    conversation = [{"role": "system", "content": system_prompt}]
    
    for iteration in range(max_iterations):
        # Ask Claude for next payload
        response = self.llm_strategy.select_model("exploitation").chat(conversation)
        
        # Extract payload from response
        payload = self._extract_payload(response)
        
        # Execute payload
        result = self.http_client.get(f"{url}?{param}={payload}")
        
        # Feed result back to Claude
        conversation.append({"role": "assistant", "content": response})
        conversation.append({"role": "user", "content": f"Response: {result.text}"})
        
        # Check if exploitation complete
        if "extracted" in response.lower():
            break
    
    return findings
```

**Classification Logic:**
- **EXPLOITED**: Data successfully extracted (tables, users, etc.)
- **POTENTIAL**: Vulnerability confirmed but extraction blocked (WAF, permissions)
- **FALSE_POSITIVE**: Initially flagged but not actually exploitable

**Important:**
- Uses database-specific payloads (MySQL syntax ≠ PostgreSQL syntax)
- Adapts based on responses
- Logs every request/response for evidence

---

### 5. Reporting (`src/reporting/`)

#### `markdown_reporter.py`
**Purpose:** Generate comprehensive Markdown reports

**Key Methods:**
- `generate_report(findings, fingerprint, metadata)` - Create full report
- `_generate_executive_summary(findings)` - High-level overview
- `_generate_findings_section(findings)` - Detailed vulnerabilities
- `_generate_remediation(findings)` - Fix recommendations

**Report Structure:**
```markdown
# Security Assessment Report

## Executive Summary
- Scan date
- Target URL
- Findings count by severity
- Overall risk score

## Target Information
- Fingerprint results
- Tech stack
- Detected protections (WAF)

## Findings
### [SEVERITY] Vulnerability Title
- URL
- Parameter
- Status (EXPLOITED/POTENTIAL/FALSE_POSITIVE)
- Evidence (exact payloads + responses)
- Proof of Concept
- Impact
- Remediation

## Appendix
- Methodology
- Tools used
- Scan duration
```

**Output Location:** `workspace/reports/scan_report_{timestamp}.md`

---

### 6. CLI (`cli.py`)

**Purpose:** Command-line interface with Rich UI

**Arguments:**
- `--target URL` - Target URL to scan (required)
- `--verbose` - Enable debug logging (optional)
- `--config PATH` - Custom config file (optional, default: `config/default_config.yaml`)

**Features:**
- Rich progress bars and status messages
- Authorization confirmation prompt (legal protection)
- Colored output (success=green, error=red, info=blue)
- Graceful error handling

**Flow:**
```python
1. Parse arguments
2. Display banner
3. Prompt for authorization confirmation
4. Initialize ConfigManager
5. Setup Logger
6. Initialize Orchestrator
7. Run orchestrator.execute(target)
8. Display summary
9. Show report path
```

---

## 🔧 Common Development Tasks

### Task 1: Add New Agent (e.g., XSS)

**Steps:**

1. **Create agent file:** `src/agents/xss_agent.py`

```python
from .base_agent import BaseAgent

class XSSAgent(BaseAgent):
    def __init__(self, config, http_client, llm_strategy, prompt_manager, logger):
        super().__init__(config, http_client, llm_strategy, prompt_manager, logger)
        self.agent_name = "XSS"
    
    def execute(self, target_url, context=None):
        self.logger.info(f"Starting XSS testing on {target_url}")
        findings = []
        
        # Detection stage
        vulnerable_params = self._detection_stage(target_url)
        
        # Exploitation stage
        for param in vulnerable_params:
            finding = self._exploitation_stage(target_url, param, context)
            if finding:
                findings.append(finding)
        
        return {"findings": findings, "status": "complete"}
    
    def _detection_stage(self, url):
        # TODO: Implement XSS detection
        pass
    
    def _exploitation_stage(self, url, param, context):
        # TODO: Implement XSS exploitation
        pass
```

2. **Create prompts:**
   - `prompts/system/xss_exploit.txt`
   - `prompts/tasks/xss_test_endpoint.txt`

3. **Update `__init__.py`:**
```python
from .xss_agent import XSSAgent
__all__ = [..., 'XSSAgent']
```

4. **Update orchestrator:**
```python
from ..agents import SQLiAgent, XSSAgent

# In execute method
xss_agent = XSSAgent(self.config, http_client, llm_strategy, prompt_manager, self.logger)
xss_findings = xss_agent.execute(target_url, fingerprint)
all_findings.extend(xss_findings["findings"])
```

5. **Test:**
```bash
python cli.py --target https://xss-game.appspot.com --verbose
```

---

### Task 2: Improve Fingerprint Detection

**Example: Add Symfony framework detection**

In `src/tools/fingerprint.py`:

```python
# In _init_patterns method
self.framework_patterns = {
    # ... existing frameworks
    "symfony": {
        "patterns": [r"symfony", r"_profiler", r"_wdt"],
        "cookies": ["PHPSESSID"],  # Symfony uses PHP
        "headers": ["X-Debug-Token", "X-Debug-Token-Link"]
    }
}
```

Test:
```python
fp = Fingerprint(config, http_client, logger)
result = fp.analyze_target("https://symfony-demo.com")
print(result["framework"]["backend"])  # Should include Symfony
```

---

### Task 3: Add New Prompt

**Example: Blind SQLi prompt**

1. Create `prompts/system/blind_sqli_exploit.txt`:
```
You are an expert penetration tester specializing in blind SQL injection.

TARGET INFORMATION:
{{target_info}}

TASK:
Extract data from database using blind SQL injection techniques:
- Boolean-based blind SQLi
- Time-based blind SQLi
- Binary search for data extraction

OUTPUT FORMAT:
{
  "method": "boolean-based" | "time-based",
  "payload": "SQL injection payload",
  "extracted_data": "data extracted so far",
  "confidence": 0-100,
  "next_steps": "what to try next"
}
```

2. Use in agent:
```python
blind_prompt = self.prompt_manager.get_prompt(
    "system/blind_sqli_exploit.txt",
    context={"target_info": fingerprint}
)
```

---

### Task 4: Add Unit Test

**Example: Test HTTP Client**

Create `tests/test_http_client.py`:

```python
import pytest
from src.tools.http_client import HTTPClient
from src.core.config_manager import ConfigManager
from src.core.logger import setup_logger

@pytest.fixture
def http_client():
    config = ConfigManager()
    logger = setup_logger(config)
    return HTTPClient(config, logger)

def test_get_request(http_client):
    response = http_client.get("https://httpbin.org/get")
    assert response.status_code == 200
    assert "httpbin.org" in response.text

def test_retry_on_failure(http_client):
    # Test with invalid URL
    with pytest.raises(Exception):
        http_client.get("https://invalid-url-xyz123.com", max_retries=2)

def test_timeout(http_client):
    # Test with very short timeout
    with pytest.raises(Exception):
        http_client.get("https://httpbin.org/delay/10", timeout=1)
```

Run tests:
```bash
pytest tests/ -v
```

---

## 🎨 Code Style & Standards

### Naming Conventions
- **Classes**: PascalCase (`HTTPClient`, `SQLiAgent`)
- **Functions/Methods**: snake_case (`analyze_target`, `get_prompt`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `API_BASE_URL`)
- **Private methods**: Prefix with underscore (`_detect_database`)

### Docstrings
```python
def analyze_target(self, url: str) -> Dict:
    """
    Perform comprehensive fingerprinting on target URL.
    
    Args:
        url (str): Target URL to analyze
    
    Returns:
        Dict: Complete fingerprint results including:
            - server: Server software and version
            - cms: Content Management System info
            - database: Database type and confidence
            - waf: Web Application Firewall detection
            - technologies: List of detected technologies
    
    Raises:
        RequestException: If target is unreachable
        ValueError: If URL is invalid
    
    Example:
        >>> fp = Fingerprint(config, http_client, logger)
        >>> result = fp.analyze_target("https://example.com")
        >>> print(result["server"]["name"])
        'nginx'
    """
```

### Type Hints
```python
from typing import Dict, List, Optional, Tuple

def select_model(self, task_type: str, complexity: float) -> BaseLLM:
    """Select appropriate LLM based on task"""
    pass

def execute(self, target_url: str, context: Optional[Dict] = None) -> Dict:
    """Execute agent testing"""
    pass
```

### Error Handling
```python
try:
    response = self.http_client.get(url)
    data = self._parse_response(response)
except RequestException as e:
    self.logger.error(f"Request failed: {e}", exc_info=True)
    return {"error": str(e), "status": "failed"}
except ValueError as e:
    self.logger.error(f"Parse error: {e}")
    return {"error": "Invalid response format"}
except Exception as e:
    self.logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

### Logging Best Practices
```python
# Use appropriate levels
self.logger.debug("Detailed diagnostic info")    # Development only
self.logger.info("Normal operation messages")     # User-facing
self.logger.warning("Unexpected but handled")     # Potential issues
self.logger.error("Error occurred", exc_info=True) # Failures

# Include context
self.logger.info(f"Testing parameter {param} on {url}")
self.logger.error(f"Failed to connect to {url}: {error}")

# Don't log sensitive data
self.logger.info("Login successful")  # Good
self.logger.info(f"Password: {password}")  # BAD!
```

---

## 🧪 Testing Strategy

### Unit Tests
Test individual components in isolation:
- Config Manager
- HTTP Client
- Prompt Manager
- Fingerprint (with mock HTTP responses)

### Integration Tests
Test component interactions:
- Orchestrator → Agent → LLM
- Agent → HTTP Client → Target
- Reporter → File System

### End-to-End Tests
Full workflow on test targets:
- DVWA (Damn Vulnerable Web Application)
- testphp.vulnweb.com
- Local test servers

### Mock Strategies

**Mock LLM Responses:**
```python
class MockLLM:
    def chat(self, messages):
        # Return predefined response
        return "Vulnerable parameter detected: id"

# In test
agent = SQLiAgent(config, http_client, mock_llm, prompt_manager, logger)
```

**Mock HTTP Responses:**
```python
@pytest.fixture
def mock_response():
    response = Mock()
    response.status_code = 200
    response.text = "<html>MySQL error: syntax</html>"
    return response
```

---

## 📝 TODO List by Priority

### P0 - Critical (Do First)
- [ ] Add `DISCLAIMER.md` file
- [ ] Implement scope validation (whitelist/blacklist)
- [ ] Add API key validation at startup
- [ ] Improve error handling in all agents
- [ ] Add sensitive data redaction in logs

### P1 - Important (Do Soon)
- [ ] Write unit tests (80% coverage minimum)
- [ ] Add docstrings to all public methods
- [ ] Implement rate limiting per target
- [ ] Add token usage tracking
- [ ] Create integration tests

### P2 - Nice to Have (Future)
- [ ] Implement XSS Agent
- [ ] Implement LFI Agent
- [ ] Add HTML report format
- [ ] Implement blind SQLi techniques
- [ ] Add multi-threading support

### P3 - Future Enhancements
- [ ] Web dashboard
- [ ] Plugin system
- [ ] API fuzzing agent
- [ ] Burp Suite integration
- [ ] Historical scan comparison

---

## 🚨 Known Issues & Limitations

### Current Limitations

1. **Single-threaded**: All requests are sequential (slow for large scans)
2. **No WAF Bypass**: Basic detection only, no bypass techniques implemented
3. **Limited SQLi Techniques**: No blind SQLi, second-order, or advanced methods
4. **No State Persistence**: Can't resume interrupted scans
5. **API Cost**: Claude calls can be expensive for large scans

### Known Bugs

1. **Fingerprint timeout**: Very slow targets may timeout during fingerprint
2. **Large responses**: HTML >1MB may cause memory issues
3. **Redirect loops**: Infinite redirects not properly handled

### Workarounds

**Issue**: Slow targets  
**Workaround**: Increase timeout in config: `http.timeout: 60`

**Issue**: High API costs  
**Workaround**: Use DeepSeek for more tasks, reduce Claude usage

**Issue**: Rate limiting  
**Workaround**: Add delays: `http.request_delay: 2`

---

## 📚 Resources for Continued Development

### SQL Injection
- [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLMap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)
- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

### LLM for Security
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [DeepSeek API Documentation](https://api-docs.deepseek.com)
- "AI-Assisted Penetration Testing" research papers

### Web Security
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Burp Suite Academy](https://portswigger.net/web-security)
- [HackerOne Disclosed Reports](https://hackerone.com/hacktivity)

---

## 🤝 When Asking Claude for Help

**Provide This Context:**
```
I'm working on BlackShannon, an AI-powered penetration testing tool.

Current status: [describe what you're working on]
Issue: [describe the problem]
What I've tried: [list attempts]

Relevant files:
- src/agents/sqli_agent.py
- prompts/system/sqli_exploit.txt

Code snippet:
[paste relevant code]

Error message:
[paste error if applicable]
```

**Good Questions:**
- "How should I implement blind SQLi in the SQLi agent?"
- "What's the best way to detect XSS vulnerabilities using LLMs?"
- "How can I improve the fingerprint detection for framework X?"

**Bad Questions:**
- "Fix my code" (too vague)
- "Why doesn't it work?" (no context)
- "Make it better" (no specific goal)

---

## ✅ Final Checklist Before Deploying

- [ ] README.md is up to date
- [ ] DISCLAIMER.md exists and is prominent
- [ ] All API keys are in `.env` (not committed)
- [ ] Dependencies in `requirements.txt` are correct
- [ ] Unit tests pass (`pytest tests/`)
- [ ] Integration test successful on test target
- [ ] Logs don't contain sensitive data
- [ ] Error handling is comprehensive
- [ ] Code follows style guide
- [ ] Docstrings are complete
- [ ] Scope validation is implemented
- [ ] Rate limiting is configured

---

**Good luck with development! Remember: Test responsibly, document thoroughly, and always prioritize ethical security testing.** 🎯
