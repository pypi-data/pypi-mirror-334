from typing import List, Optional
import random

class ProxyManager:
    def __init__(self, proxies: List[str]):
        self.proxies = proxies
        self.current_proxy = None

    def get_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        self.current_proxy = random.choice(self.proxies)
        return self.current_proxy