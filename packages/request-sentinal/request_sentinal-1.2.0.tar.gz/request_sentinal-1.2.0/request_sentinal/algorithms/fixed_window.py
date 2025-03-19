import time
from threading import Lock

class FixedWindow:
    def __init__(self, capacity: int, window_size: float):
        self.capacity = capacity
        self.window_size = window_size
        self.tokens = 0
        self.window_start = time.time()
        self.lock = Lock()

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            if now - self.window_start > self.window_size:
                self.tokens = 0
                self.window_start = now
            if self.tokens + tokens <= self.capacity:
                self.tokens += tokens
                return True
            return False