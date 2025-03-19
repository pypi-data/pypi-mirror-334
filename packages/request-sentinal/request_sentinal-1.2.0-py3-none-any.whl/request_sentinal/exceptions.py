class RateLimitExceeded(Exception):
    """Raised when the rate limit is exceeded."""
    pass

class RobotsDisallowed(Exception):
    """Raised when a URL is disallowed by robots.txt."""
    pass

class MaxRetriesExceeded(Exception):
    """Raised when the maximum number of retries is exceeded."""
    pass

class ProxyError(Exception):
    """Raised when there is an issue with the proxy."""
    pass