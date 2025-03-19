import time
from threading import Lock

class LeakyBucket:
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity
        self.tokens = 0
        self.leak_rate = leak_rate
        self.last_leak = time.time()
        self.lock = Lock()

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            self._leak()
            if self.tokens + tokens <= self.capacity:
                self.tokens += tokens
                return True
            return False

    def _leak(self):
        now = time.time()
        elapsed = now - self.last_leak
        self.tokens = max(0, self.tokens - elapsed * self.leak_rate)
        self.last_leak = now