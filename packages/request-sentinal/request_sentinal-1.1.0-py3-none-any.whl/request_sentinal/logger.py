import logging
from typing import Dict, Any

class Logger:
    def __init__(self, log_file: str = "error.log", log_level: str = "INFO"):
        self.logger = logging.getLogger("rate_limiter")
        self.logger.setLevel(log_level)

        # File handler for logging to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Stream handler for logging to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)

    def log(self, level: str, message: str, metadata: Dict[str, Any] = None):
        if metadata:
            message = f"{message} | Metadata: {metadata}"
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)

# Singleton logger instance
logger = Logger()