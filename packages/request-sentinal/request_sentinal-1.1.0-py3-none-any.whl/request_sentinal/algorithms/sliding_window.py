import time
from collections import deque
from threading import Lock

class SlidingWindow:
    def __init__(self, capacity: int, window_size: float):
        self.capacity = capacity
        self.window_size = window_size
        self.requests = deque()
        self.lock = Lock()

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            while self.requests and self.requests[0] <= now - self.window_size:
                self.requests.popleft()
            if len(self.requests) + tokens <= self.capacity:
                self.requests.extend([now] * tokens)
                return True
            return False