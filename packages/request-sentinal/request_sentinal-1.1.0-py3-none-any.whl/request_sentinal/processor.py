import time
import requests
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from .algorithms.token_bucket import TokenBucket
from .proxy_manager import ProxyManager
from .robots_checker import RobotsChecker
from .exceptions import RateLimitExceeded, RobotsDisallowed, MaxRetriesExceeded, ProxyError
from .logger import logger

class URLProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.rate_limiters = {}  # Domain-specific rate limiters
        self.global_limiter = TokenBucket(
            capacity=config["rate_limit"]["global_capacity"],
            refill_rate=config["rate_limit"]["global_refill_rate"]
        )
        self.proxy_manager = ProxyManager(config.get("proxies", []))
        self.robots_checker = RobotsChecker(config.get("user_agent", "MyScraper/1.0"))

    def _get_rate_limiter(self, domain: str):
        if domain not in self.rate_limiters:
            self.rate_limiters[domain] = TokenBucket(
                capacity=self.config["rate_limit"]["domain_capacity"],
                refill_rate=self.config["rate_limit"]["domain_refill_rate"]
            )
        return self.rate_limiters[domain]

    def process_url(self, url: str, headers: Optional[Dict] = None, error_callback: Optional[Callable] = None) -> \
    Optional[Dict]:
        domain = urlparse(url).netloc
        rate_limiter = self._get_rate_limiter(domain)
        robots_txt = self.robots_checker.fetch_robots_txt(url)

        if not self.robots_checker.is_allowed(url, robots_txt):
            logger.log("WARNING", f"URL disallowed by robots.txt", {"url": url})
            if error_callback:
                error_callback(url, RobotsDisallowed(f"URL {url} disallowed by robots.txt"))
            return None

        for attempt in range(self.config["retry"]["max_retries"]):
            try:
                # Check global and domain-specific rate limits
                if not self.global_limiter.consume() or not rate_limiter.consume():
                    raise RateLimitExceeded(f"Rate limit exceeded for {url}")

                # Get a proxy
                proxy = self.proxy_manager.get_proxy()
                if not proxy:
                    logger.log("WARNING", "No proxies available, falling back to direct connection")
                    response = requests.get(url, headers=headers)
                else:
                    response = requests.get(
                        url,
                        headers=headers,
                        proxies={"http": proxy, "https": proxy}
                    )

                response.raise_for_status()

                # Log successful request
                logger.log("INFO", f"Successfully processed URL", {"url": url, "status_code": response.status_code})
                return {
                    "url": url,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "content": response.content
                }

            except requests.exceptions.RequestException as e:
                logger.log("ERROR", f"Attempt {attempt + 1} failed for URL", {"url": url, "error": str(e)})
                if error_callback:
                    error_callback(url, e)

                # Adjust rate limits if the server responds with 429
                if isinstance(e, requests.exceptions.HTTPError) and hasattr(e, "response") and e.response is not None:
                    if e.response.status_code == 429:  # Too Many Requests
                        self._adjust_rate_limits(e.response, domain)

                # Rotate to the next proxy if the current one fails
                if proxy:
                    logger.log("INFO", f"Rotating to the next proxy", {"current_proxy": proxy})
                    self.proxy_manager.get_proxy()  # Rotate to the next proxy

                time.sleep(
                    min(self.config["retry"]["initial_delay"] * (2 ** attempt), self.config["retry"]["max_delay"]))
            except (RateLimitExceeded, ProxyError) as e:
                logger.log("ERROR", str(e), {"url": url})
                if error_callback:
                    error_callback(url, e)
                time.sleep(
                    min(self.config["retry"]["initial_delay"] * (2 ** attempt), self.config["retry"]["max_delay"]))

        logger.log("ERROR", f"Max retries exceeded for URL", {"url": url})
        if error_callback:
            error_callback(url, MaxRetriesExceeded(f"Max retries exceeded for {url}"))
        return None

    def process_urls(self, urls: List[str], headers: Optional[Dict] = None, error_callback: Optional[Callable] = None) -> List[Optional[Dict]]:
        results = [None] * len(urls)
        with ThreadPoolExecutor(max_workers=self.config["concurrency"]["max_workers"]) as executor:
            future_to_index = {executor.submit(self.process_url, url, headers, error_callback): i for i, url in enumerate(urls)}
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                results[index] = future.result()
        return results