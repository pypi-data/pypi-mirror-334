import json
from typing import List, Dict
import re
from request_sentinal.processor import URLProcessor
from request_sentinal.algorithms.token_bucket import TokenBucket


def load_urls(file_path: str) -> List[str]:
    """
    Load URLs from a text file.
    """
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def load_config(file_path: str) -> Dict:
    """
    Load configuration from a JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)

import pickle

def unpickle_file(file_path):
    try:
        with open(file_path, "rb") as file:
            data = pickle.load(file)
            print("Successfully unpickled the file!")
            return data
    except Exception as e:
        print(f"Error unpickling file: {e}")

def retry_failed():
    # Parse error log
    failed_urls = []
    with open("error.log", "r") as file:
        for line in file:
            match = re.search(r"URL (https://[^\s]+)", line)
            if match:
                failed_urls.append(match.group(1))

    # Retry failed URLs
    rate_limiter = TokenBucket(capacity=10, refill_rate=1)
    processor = URLProcessor(rate_limiter)
    results = processor.process_urls(failed_urls)

    # Save retry results
    with open("retry_results.pkl", "wb") as file:
        pickle.dump(results, file)