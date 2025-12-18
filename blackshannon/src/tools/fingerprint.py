import re
import logging
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse, urljoin


class Fingerprint:
    """Advanced fingerprinting for comprehensive target analysis"""
    
    def __init__(self, config, http_client, logger):
        self.config = config
        self.http_client = http_client
        self.logger = logger
        
        # Initialize pattern databases
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize all detection patterns"""
        
        # CMS Signatures
        self.cms_patterns = {
            "wordpress": {
                "patterns": [
                    r"wp-content",
                    r"wp-includes",
                    r"wp-admin",
                    r'<meta name="generator" content="WordPress\s*([\d.]+)?'
                ],
                "paths": ["/wp-login.php", "/wp-admin/"],
                "headers": [],
                "cookies": ["wordpress_"]
            },
            "joomla": {
                "patterns": [
                    r"/components/com_",
                    r"/media/jui/",
                    r'<meta name="generator" content="Joomla!?\s*([\d.]+)?'
                ],
                "paths": ["/administrator/"],
                "headers": [],
                "cookies": []
            },
            "drupal": {
                "patterns": [
                    r"Drupal",
                    r"/sites/default/",
                    r"/sites/all/",
                    r'<meta name="Generator" content="Drupal\s*([\d.]+)?'
                ],
                "paths": ["/user/login"],
                "headers": ["X-Drupal-Cache", "X-Generator: Drupal"],
                "cookies": ["SESS"]
            },
            "magento": {
                "patterns": [
                    r"/skin/frontend/",
                    r"Mage.Cookies",
                    r"varien/js"
                ],
                "paths": ["/admin"],
                "headers": [],
                "cookies": ["frontend"]
            },
            "shopify": {
                "patterns": [
                    r"cdn.shopify.com",
                    r"shopify",
                    r"Shopify.theme"
                ],
                "paths": [],
                "headers": ["X-ShopId"],
                "cookies": ["_shopify"]
            }
        }
        
        # Framework Signatures
        self.framework_patterns = {
            "laravel": {
                "patterns": [r"laravel", r"Laravel"],
                "cookies": ["laravel_session", "XSRF-TOKEN"],
                "headers": ["X-Laravel"]
            },
            "django": {
                "patterns": [r"csrfmiddlewaretoken", r"__admin"],
                "cookies": ["csrftoken", "sessionid"],
                "headers": []
            },
            "flask": {
                "patterns": [r"Werkzeug"],
                "cookies": ["session"],
                "headers": ["Server: Werkzeug"]
            },
            "express": {
                "patterns": [],
                "cookies": ["connect.sid"],
                "headers": ["X-Powered-By: Express"]
            },
            "spring": {
                "patterns": [r"Whitelabel Error Page"],
                "cookies": ["JSESSIONID"],
                "headers": []
            },
            "aspnet": {
                "patterns": [r"__VIEWSTATE", r"__EVENTVALIDATION"],
                "cookies": ["ASP.NET_SessionId"],
                "headers": ["X-AspNet-Version", "X-AspNetMvc-Version"]
            }
        }
        
        # Frontend Framework Signatures
        self.frontend_patterns = {
            "react": [r"react", r"_react", r"data-reactroot"],
            "vue": [r"vue\.js", r"data-v-", r"Vue\."],
            "angular": [r"ng-app", r"ng-controller", r"angular"],
            "jquery": [r"jquery", r"\$\("],
            "bootstrap": [r"bootstrap", r"btn-primary"],
            "tailwind": [r"tailwind"]
        }
        
        # Database Error Patterns (expanded)
        self.db_patterns = {
            "mysql": [
                r"SQL syntax.*MySQL",
                r"Warning.*mysql_",
                r"MySQLSyntaxErrorException",
                r"valid MySQL result",
                r"check the manual that corresponds to your MySQL",
                r"mysql_fetch",
                r"mysql_num_rows"
            ],
            "postgresql": [
                r"PostgreSQL.*ERROR",
                r"Warning.*\Wpg_",
                r"valid PostgreSQL result",
                r"Npgsql\.",
                r"PG::SyntaxError",
                r"org.postgresql.util.PSQLException"
            ],
            "mssql": [
                r"Driver.*SQL Server",
                r"OLE DB.*SQL Server",
                r"(\W|\A)SQL Server.*Driver",
                r"Warning.*mssql_",
                r"Microsoft SQL Native Client error",
                r"ODBC SQL Server Driver",
                r"SQLServer JDBC Driver"
            ],
            "oracle": [
                r"\bORA-[0-9][0-9][0-9][0-9]",
                r"Oracle error",
                r"Oracle.*Driver",
                r"Warning.*\Woci_",
                r"quoted string not properly terminated"
            ],
            "sqlite": [
                r"SQLite/JDBCDriver",
                r"SQLite.Exception",
                r"System.Data.SQLite.SQLiteException",
                r"Warning.*sqlite_",
                r"sqlite3.OperationalError"
            ],
            "mongodb": [
                r"MongoError",
                r"mongodb://",
                r"TypeError: db\.\w+ is not a function"
            ]
        }
        
        # WAF Signatures
        self.waf_patterns = {
            "cloudflare": {
                "headers": ["CF-RAY", "cf-cache-status", "__cfduid"],
                "cookies": ["__cfduid", "__cflb"],
                "patterns": [r"cloudflare", r"cf-ray"]
            },
            "akamai": {
                "headers": ["X-Akamai-", "AkamaiGHost"],
                "cookies": ["ak_bmsc"],
                "patterns": []
            },
            "aws_waf": {
                "headers": ["X-Amzn-", "X-AMZ-"],
                "cookies": [],
                "patterns": [r"Access Denied.*AWS"]
            },
            "modsecurity": {
                "headers": [],
                "cookies": [],
                "patterns": [r"Mod_Security", r"ModSecurity", r"NOYB"]
            },
            "f5": {
                "headers": ["X-WA-Info"],
                "cookies": ["TS", "F5"],
                "patterns": []
            },
            "imperva": {
                "headers": ["X-Iinfo"],
                "cookies": ["incap_ses", "visid_incap"],
                "patterns": []
            }
        }
        
        # Server Software Patterns
        self.server_patterns = {
            "nginx": r"nginx/([\d.]+)",
            "apache": r"Apache/([\d.]+)",
            "iis": r"Microsoft-IIS/([\d.]+)",
            "tomcat": r"Apache-Coyote/([\d.]+)",
            "lighttpd": r"lighttpd/([\d.]+)"
        }
    
    def analyze_target(self, url: str) -> Dict:
        """
        Comprehensive target analysis
        Returns complete fingerprint with all detected technologies
        """
        self.logger.info(f"Starting comprehensive fingerprint for {url}")
        
        result = {
            "url": url,
            "final_url": url,
            "status_code": None,
            "server": {"name": "Unknown", "version": None},
            "backend": {"language": None, "version": None},
            "cms": {"name": None, "version": None, "confidence": "none"},
            "framework": {"backend": [], "frontend": []},
            "database": {"type": "unknown", "confidence": "low", "evidence": []},
            "waf": {"detected": False, "type": None, "confidence": "none"},
            "technologies": [],
            "headers": {},
            "cookies": {},
            "paths_found": [],
            "tech_stack_summary": "Unknown",
            "fingerprint_confidence": "low",
            "timestamp": datetime.now().isoformat(),
            "errors": []
        }
        
        try:
            # Phase 1: Initial request and header analysis
            self.logger.debug("Phase 1: Initial request")
            response = self._make_safe_request(url)
            if not response:
                result["errors"].append("Failed to reach target")
                return result
            
            result["status_code"] = response.status_code
            result["final_url"] = response.url
            headers = dict(response.headers)
            html = response.text
            
            # Phase 2: Header analysis
            self.logger.debug("Phase 2: Analyzing headers")
            header_info = self._analyze_headers(headers)
            result["server"] = header_info["server"]
            result["backend"] = header_info["backend"]
            result["headers"] = header_info["filtered_headers"]
            result["cookies"] = header_info["cookies"]
            
            # Phase 3: WAF detection
            self.logger.debug("Phase 3: WAF detection")
            waf_info = self._detect_waf(headers, html)
            result["waf"] = waf_info
            
            # Phase 4: CMS detection
            self.logger.debug("Phase 4: CMS detection")
            cms_info = self._detect_cms(html, headers, url)
            result["cms"] = cms_info
            
            # Phase 5: Framework detection
            self.logger.debug("Phase 5: Framework detection")
            framework_info = self._detect_frameworks(html, headers, result["cookies"])
            result["framework"] = framework_info
            
            # Phase 6: Database detection
            self.logger.debug("Phase 6: Database detection")
            db_info = self._detect_database(html, headers)
            result["database"] = db_info
            
            # Phase 7: Additional probing
            self.logger.debug("Phase 7: Additional probing")
            probe_info = self._probe_common_paths(url)
            result["paths_found"] = probe_info
            
            # Phase 8: Build technology list and summary
            result["technologies"] = self._build_tech_list(result)
            result["tech_stack_summary"] = self._build_summary(result)
            result["fingerprint_confidence"] = self._calculate_confidence(result)
            
            self.logger.info(f"Fingerprint complete: {result['tech_stack_summary']}")
            
        except Exception as e:
            self.logger.error(f"Fingerprint error: {str(e)}", exc_info=True)
            result["errors"].append(str(e))
        
        return result
    
    def _make_safe_request(self, url: str, timeout: int = 10) -> Optional:
        """Make HTTP request with error handling"""
        try:
            return self.http_client.get(url, timeout=timeout, allow_redirects=True)
        except Exception as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            return None
    
    def _analyze_headers(self, headers: Dict) -> Dict:
        """Extract detailed info from HTTP headers"""
        info = {
            "server": {"name": "Unknown", "version": None},
            "backend": {"language": None, "version": None},
            "filtered_headers": {},
            "cookies": {}
        }
        
        # Server detection
        if "Server" in headers:
            server_str = headers["Server"]
            info["filtered_headers"]["Server"] = server_str
            
            for server_name, pattern in self.server_patterns.items():
                match = re.search(pattern, server_str, re.IGNORECASE)
                if match:
                    info["server"]["name"] = server_name
                    if match.groups():
                        info["server"]["version"] = match.group(1)
                    break
        
        # Backend language detection
        if "X-Powered-By" in headers:
            powered_by = headers["X-Powered-By"]
            info["filtered_headers"]["X-Powered-By"] = powered_by
            
            # PHP detection
            php_match = re.search(r"PHP/([\d.]+)", powered_by, re.IGNORECASE)
            if php_match:
                info["backend"]["language"] = "PHP"
                info["backend"]["version"] = php_match.group(1)
            
            # ASP.NET detection
            if "ASP.NET" in powered_by:
                info["backend"]["language"] = "ASP.NET"
        
        # ASP.NET specific headers
        if "X-AspNet-Version" in headers:
            info["backend"]["language"] = "ASP.NET"
            info["backend"]["version"] = headers["X-AspNet-Version"]
            info["filtered_headers"]["X-AspNet-Version"] = headers["X-AspNet-Version"]
        
        # Express detection
        if "X-Powered-By" in headers and "Express" in headers["X-Powered-By"]:
            info["backend"]["language"] = "Node.js"
            info["backend"]["framework"] = "Express"
        
        # Cookie analysis
        if "Set-Cookie" in headers:
            cookie_str = headers["Set-Cookie"]
            
            # PHP session
            if "PHPSESSID" in cookie_str:
                info["cookies"]["PHPSESSID"] = True
                if not info["backend"]["language"]:
                    info["backend"]["language"] = "PHP"
            
            # ASP.NET session
            if "ASP.NET_SessionId" in cookie_str:
                info["cookies"]["ASP.NET_SessionId"] = True
                if not info["backend"]["language"]:
                    info["backend"]["language"] = "ASP.NET"
            
            # Laravel
            if "laravel_session" in cookie_str:
                info["cookies"]["laravel_session"] = True
            
            # Express/Node
            if "connect.sid" in cookie_str:
                info["cookies"]["connect.sid"] = True
                if not info["backend"]["language"]:
                    info["backend"]["language"] = "Node.js"
            
            # Django
            if "csrftoken" in cookie_str or "sessionid" in cookie_str:
                info["cookies"]["django"] = True
                if not info["backend"]["language"]:
                    info["backend"]["language"] = "Python"
        
        # Additional headers
        for header in ["X-Framework", "X-Generator", "X-Drupal-Cache"]:
            if header in headers:
                info["filtered_headers"][header] = headers[header]
        
        return info
    
    def _detect_waf(self, headers: Dict, html: str) -> Dict:
        """Detect Web Application Firewall"""
        waf_info = {
            "detected": False,
            "type": None,
            "confidence": "none",
            "evidence": []
        }
        
        scores = {waf: 0 for waf in self.waf_patterns.keys()}
        
        for waf_name, signatures in self.waf_patterns.items():
            # Check headers
            for header in signatures["headers"]:
                if any(header.lower() in h.lower() for h in headers.keys()):
                    scores[waf_name] += 2
                    waf_info["evidence"].append(f"Header: {header}")
            
            # Check cookies
            cookie_str = headers.get("Set-Cookie", "")
            for cookie in signatures["cookies"]:
                if cookie in cookie_str:
                    scores[waf_name] += 2
                    waf_info["evidence"].append(f"Cookie: {cookie}")
            
            # Check HTML patterns
            for pattern in signatures["patterns"]:
                if re.search(pattern, html, re.IGNORECASE):
                    scores[waf_name] += 1
                    waf_info["evidence"].append(f"Pattern: {pattern}")
        
        # Determine WAF
        max_score = max(scores.values())
        if max_score > 0:
            waf_info["detected"] = True
            waf_info["type"] = max(scores, key=scores.get)
            waf_info["confidence"] = "high" if max_score >= 3 else "medium" if max_score >= 2 else "low"
        
        return waf_info
    
    def _detect_cms(self, html: str, headers: Dict, base_url: str) -> Dict:
        """Detect Content Management System"""
        cms_info = {
            "name": None,
            "version": None,
            "confidence": "none",
            "evidence": []
        }
        
        scores = {cms: 0 for cms in self.cms_patterns.keys()}
        
        for cms_name, signatures in self.cms_patterns.items():
            # Check HTML patterns
            for pattern in signatures["patterns"]:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    scores[cms_name] += 2
                    cms_info["evidence"].append(f"Pattern: {pattern[:50]}")
                    
                    # Try to extract version
                    if isinstance(matches[0], tuple) and matches[0][0]:
                        cms_info["version"] = matches[0][0]
                    elif isinstance(matches[0], str) and re.search(r'[\d.]+', matches[0]):
                        version_match = re.search(r'([\d.]+)', matches[0])
                        if version_match:
                            cms_info["version"] = version_match.group(1)
            
            # Check headers
            for header_pattern in signatures["headers"]:
                if any(header_pattern.lower() in h.lower() for h in headers.keys()):
                    scores[cms_name] += 1
                    cms_info["evidence"].append(f"Header: {header_pattern}")
            
            # Check cookies
            cookie_str = headers.get("Set-Cookie", "")
            for cookie_pattern in signatures["cookies"]:
                if cookie_pattern in cookie_str:
                    scores[cms_name] += 1
                    cms_info["evidence"].append(f"Cookie: {cookie_pattern}")
        
        # Determine CMS
        max_score = max(scores.values())
        if max_score > 0:
            cms_info["name"] = max(scores, key=scores.get)
            cms_info["confidence"] = "high" if max_score >= 4 else "medium" if max_score >= 2 else "low"
        
        return cms_info
    
    def _detect_frameworks(self, html: str, headers: Dict, cookies: Dict) -> Dict:
        """Detect backend and frontend frameworks"""
        framework_info = {
            "backend": [],
            "frontend": []
        }
        
        # Backend frameworks
        for framework_name, signatures in self.framework_patterns.items():
            score = 0
            
            # Check patterns
            for pattern in signatures["patterns"]:
                if re.search(pattern, html, re.IGNORECASE):
                    score += 1
            
            # Check cookies
            for cookie in signatures["cookies"]:
                if cookie in cookies or cookie in headers.get("Set-Cookie", ""):
                    score += 1
            
            # Check headers
            for header in signatures["headers"]:
                if any(header.lower() in h.lower() for h in headers.keys()):
                    score += 1
            
            if score > 0:
                framework_info["backend"].append({
                    "name": framework_name,
                    "confidence": "high" if score >= 2 else "medium"
                })
        
        # Frontend frameworks
        for frontend_name, patterns in self.frontend_patterns.items():
            for pattern in patterns:
                if re.search(pattern, html, re.IGNORECASE):
                    framework_info["frontend"].append(frontend_name)
                    break
        
        return framework_info
    
    def _detect_database(self, html: str, headers: Dict) -> Dict:
        """Enhanced database detection"""
        db_info = {
            "type": "unknown",
            "confidence": "low",
            "evidence": []
        }
        
        scores = {db: 0 for db in self.db_patterns.keys()}
        
        # Check error patterns in HTML
        for db_type, patterns in self.db_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    scores[db_type] += 1
                    evidence = matches[0] if isinstance(matches[0], str) else str(matches[0])
                    db_info["evidence"].append(f"{db_type}: {evidence[:100]}")
        
        # Determine database
        max_score = max(scores.values())
        if max_score > 0:
            db_info["type"] = max(scores, key=scores.get)
            db_info["confidence"] = "high" if max_score >= 3 else "medium" if max_score >= 2 else "low"
        else:
            # Inference from backend
            db_info["type"] = "inferred"
            db_info["confidence"] = "low"
        
        return db_info
    
    def _probe_common_paths(self, base_url: str) -> List[str]:
        """Probe common paths to gather more information"""
        paths_found = []
        
        common_paths = [
            "/robots.txt",
            "/sitemap.xml",
            "/.well-known/security.txt",
            "/admin",
            "/wp-admin",
            "/administrator",
            "/phpmyadmin"
        ]
        
        parsed = urlparse(base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        for path in common_paths:
            url = urljoin(base, path)
            response = self._make_safe_request(url, timeout=5)
            
            if response and response.status_code == 200:
                paths_found.append(path)
                self.logger.debug(f"Found: {path}")
        
        return paths_found
    
    def _build_tech_list(self, result: Dict) -> List[str]:
        """Build comprehensive technology list"""
        technologies = []
        
        # Server
        if result["server"]["name"] != "Unknown":
            tech = result["server"]["name"]
            if result["server"]["version"]:
                tech += f" {result['server']['version']}"
            technologies.append(tech)
        
        # Backend
        if result["backend"]["language"]:
            tech = result["backend"]["language"]
            if result["backend"]["version"]:
                tech += f" {result['backend']['version']}"
            technologies.append(tech)
        
        # CMS
        if result["cms"]["name"]:
            tech = result["cms"]["name"]
            if result["cms"]["version"]:
                tech += f" {result['cms']['version']}"
            technologies.append(tech)
        
        # Backend Frameworks
        for fw in result["framework"]["backend"]:
            technologies.append(fw["name"])
        
        # Database
        if result["database"]["type"] != "unknown":
            db_tech = f"Database: {result['database']['type']}"
            if result["database"]["confidence"] == "low":
                db_tech += " (inferred)"
            technologies.append(db_tech)
        
        # WAF
        if result["waf"]["detected"]:
            technologies.append(f"WAF: {result['waf']['type']}")
        
        # Frontend (only main ones)
        if result["framework"]["frontend"]:
            frontend_str = "Frontend: " + ", ".join(result["framework"]["frontend"][:3])
            technologies.append(frontend_str)
        
        return technologies
    
    def _build_summary(self, result: Dict) -> str:
        """Build human-readable tech stack summary"""
        parts = []
        
        # Server
        if result["server"]["name"] != "Unknown":
            parts.append(result["server"]["name"])
        
        # Backend
        if result["backend"]["language"]:
            parts.append(result["backend"]["language"])
        
        # CMS/Framework
        if result["cms"]["name"]:
            parts.append(result["cms"]["name"])
        elif result["framework"]["backend"]:
            parts.append(result["framework"]["backend"][0]["name"])
        
        # Database
        if result["database"]["type"] != "unknown":
            parts.append(f"DB:{result['database']['type']}")
        
        # WAF
        if result["waf"]["detected"]:
            parts.append(f"WAF:{result['waf']['type']}")
        
        return " | ".join(parts) if parts else "Unknown Stack"
    
    def _calculate_confidence(self, result: Dict) -> str:
        """Calculate overall fingerprint confidence"""
        score = 0
        
        # Server identified
        if result["server"]["name"] != "Unknown":
            score += 1
        
        # Backend identified
        if result["backend"]["language"]:
            score += 2
        
        # CMS identified
        if result["cms"]["name"] and result["cms"]["confidence"] in ["high", "medium"]:
            score += 2
        
        # Database detected
        if result["database"]["confidence"] in ["high", "medium"]:
            score += 2
        
        # Framework detected
        if result["framework"]["backend"] or result["framework"]["frontend"]:
            score += 1
        
        # Determine confidence level
        if score >= 6:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
