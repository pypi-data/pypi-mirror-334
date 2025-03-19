import requests
from urllib.parse import urlparse
from typing import Dict, Optional

class RobotsChecker:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def fetch_robots_txt(self, base_url: str) -> Optional[str]:
        parsed_url = urlparse(base_url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        try:
            response = requests.get(robots_url, headers={"User-Agent": self.user_agent})
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            return None

    def is_allowed(self, url: str, robots_txt: Optional[str]) -> bool:
        if not robots_txt:
            return True
        # Implement parsing logic for Disallow and Crawl-Delay
        # (This is a simplified version; you can use a library like `reppy` for full compliance)
        return True