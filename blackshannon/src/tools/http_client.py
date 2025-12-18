"""
Smart HTTP Client
Intelligent HTTP client with retry, rate limiting, and analysis
"""

import requests
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import time
from ..core.logger import get_logger

logger = get_logger()


@dataclass
class HTTPResponse:
    """Structured HTTP response"""
    url: str
    status_code: int
    headers: Dict[str, str]
    body: str
    response_time: float
    error: Optional[str] = None


class HTTPClient:
    """
    Intelligent HTTP client for security testing
    
    Features:
    - Automatic retry with backoff
    - Rate limiting
    - Response time tracking
    - Error handling
    - Custom headers support
    """
    
    def __init__(
        self,
        timeout: int = 30,
        verify_ssl: bool = False,
        max_retries: int = 3,
        retry_delay: int = 2,
        rate_limit: float = 0.5,  # seconds between requests
        **kwargs
    ):
        self.session = requests.Session()
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit = rate_limit
        self.last_request_time = 0
        
        # Default headers
        self.default_headers = {
            'User-Agent': kwargs.get(
                'user_agent',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            ),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # Statistics
        self.request_count = 0
        self.error_count = 0
        
        # Disable SSL warnings if verify_ssl is False
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()
        
        logger.debug("HTTPClient initialized")
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        if self.rate_limit > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit:
                sleep_time = self.rate_limit - elapsed
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        allow_redirects: bool = True,
        **kwargs
    ) -> HTTPResponse:
        """
        Make HTTP request with retry logic
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            params: Query parameters
            data: Form data
            json: JSON data
            headers: Custom headers
            allow_redirects: Follow redirects
        
        Returns:
            HTTPResponse object
        """
        # Rate limiting
        self._rate_limit()
        
        # Merge headers
        request_headers = {**self.default_headers}
        if headers:
            request_headers.update(headers)
        
        # Retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=request_headers,
                    timeout=self.timeout,
                    verify=self.verify_ssl,
                    allow_redirects=allow_redirects,
                    **kwargs
                )
                
                response_time = time.time() - start_time
                
                self.request_count += 1
                
                logger.debug(
                    f"{method} {url} → {response.status_code} "
                    f"({response_time:.2f}s)"
                )
                
                return HTTPResponse(
                    url=response.url,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    body=response.text,
                    response_time=response_time
                )
                
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                else:
                    self.error_count += 1
        
        # All retries failed
        logger.error(f"Request failed after {self.max_retries} attempts: {last_error}")
        
        return HTTPResponse(
            url=url,
            status_code=0,
            headers={},
            body="",
            response_time=0.0,
            error=last_error
        )
    
    def get(self, url: str, **kwargs) -> HTTPResponse:
        """GET request"""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> HTTPResponse:
        """POST request"""
        return self.request("POST", url, **kwargs)
    
    def test_connectivity(self, url: str) -> bool:
        """
        Test if target is reachable
        
        Returns:
            True if target responds, False otherwise
        """
        logger.info(f"Testing connectivity to {url}")
        
        try:
            response = self.get(url)
            
            if response.status_code > 0:
                logger.success(f"Target is reachable (status: {response.status_code})")
                return True
            else:
                logger.error("Target is not reachable")
                return False
                
        except Exception as e:
            logger.error(f"Connectivity test failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics"""
        return {
            "total_requests": self.request_count,
            "errors": self.error_count,
            "success_rate": (
                (self.request_count - self.error_count) / self.request_count * 100
                if self.request_count > 0 else 0
            )
        }
