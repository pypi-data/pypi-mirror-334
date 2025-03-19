## **Request Sentinal Package Documentation**

### **Overview**
The `request_sentinal` package is a Python library designed to handle rate limiting dynamically for web scraping and API requests. It supports multiple rate-limiting algorithms, concurrent processing, proxy rotation, and respect for `robots.txt` rules. The package is designed to be robust, efficient, and easy to use.

---

### **Installation**

#### **Using pip**
You can install the package directly from PyPI (if published) or from a local source.

```bash
pip install request_sentinal
```

#### **From Source**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/request-sentinal.git
   cd request-sentinal
   ```
2. Install the package:
   ```bash
   pip install .
   ```

---

### **Configuration**

The package uses a JSON configuration file (`config.json`) to define rate limits, retry logic, concurrency, and other settings.

#### **Example `config.json`**
```json
{
  "rate_limit": {
    "global_capacity": 100,
    "global_refill_rate": 10,
    "domain_capacity": 10,
    "domain_refill_rate": 1
  },
  "retry": {
    "max_retries": 5,
    "initial_delay": 1,
    "max_delay": 10
  },
  "concurrency": {
    "max_workers": 10
  },
  "proxies": [
    "http://proxy1.com:80",
    "http://proxy2.com:80"
  ],
  "user_agent": "MyScraper/1.0",
  "logging": {
    "log_file": "error.log",
    "log_level": "INFO",
    "log_dir": "/path/to/logs"  # Optional: Custom log directory
  }
}
```

#### **Configuration Fields**
- **`rate_limit`**:
  - `global_capacity`: Maximum number of requests allowed globally.
  - `global_refill_rate`: Rate at which global tokens are refilled (tokens per second).
  - `domain_capacity`: Maximum number of requests allowed per domain.
  - `domain_refill_rate`: Rate at which domain tokens are refilled (tokens per second).

- **`retry`**:
  - `max_retries`: Maximum number of retries for failed requests.
  - `initial_delay`: Initial delay (in seconds) for retries.
  - `max_delay`: Maximum delay (in seconds) for retries.

- **`concurrency`**:
  - `max_workers`: Maximum number of concurrent threads.

- **`proxies`**: List of proxy servers to use for requests.

- **`user_agent`**: User-Agent string to use for requests.

- **`logging`**:
  - `log_file`: Name of the log file.
  - `log_level`: Logging level (e.g., `INFO`, `ERROR`).
  - `log_dir`: Directory to store log files (default: `~/request_sentinal_logs`).

---

### **Usage**

#### **1. Import the Package**
```python
from request_sentinal.processor import URLProcessor
from request_sentinal.utils import load_urls, load_config
```

#### **2. Load URLs and Configuration**
```python
# Load URLs from a text file
urls = load_urls("urls.txt")

# Load configuration from a JSON file
config = load_config("config.json")
```

#### **3. Process URLs**
```python
# Initialize the URLProcessor
processor = URLProcessor(config)

# Process URLs
results = processor.process_urls(urls, headers=config.get("headers"))
```

#### **4. Save Results**
```python
import pickle

# Save results to a pickle file
with open("results.pkl", "wb") as file:
    pickle.dump(results, file)
```

#### **5. Access Logs**
Logs are saved to the directory specified in the `log_dir` field of the configuration. By default, logs are stored in `~/request_sentinal_logs/error.log`.

---

### **Advanced Features**

#### **Dynamic Rate Limiting**
The package dynamically adjusts rate limits based on server responses (e.g., `Retry-After` headers). This is handled automatically.

#### **Proxy Rotation**
If a proxy fails, the package rotates to the next available proxy. If no proxies are available, it falls back to making requests without a proxy.

#### **Respect `robots.txt`**
The package checks `robots.txt` before making requests and respects `Disallow` and `Crawl-Delay` rules.

#### **Custom Error Handling**
You can define a custom error callback function to handle errors.

```python
def error_callback(url, error):
    print(f"Error processing {url}: {error}")

# Process URLs with custom error handling
results = processor.process_urls(urls, headers=config.get("headers"), error_callback=error_callback)
```

---

### **Example Script**

#### **`main.py`**
```python
from request_sentinal.processor import URLProcessor
from request_sentinal.utils import load_urls, load_config
import pickle

# Define error callback
def error_callback(url, error):
    print(f"Error processing {url}: {error}")

# Load URLs and configuration
urls = load_urls("urls.txt")
config = load_config("config.json")

# Initialize the URLProcessor
processor = URLProcessor(config)

# Process URLs
results = processor.process_urls(urls, headers=config.get("headers"), error_callback=error_callback)

# Save results
with open("results.pkl", "wb") as file:
    pickle.dump(results, file)

# Access logs
log_file = config.get("logging", {}).get("log_dir", os.path.join(os.path.expanduser("~"), "request_sentinal_logs"))
log_file_path = os.path.join(log_file, "error.log")
print(f"Log file can be found at: {log_file_path}")
```

---

### **Logging**

#### **Log Levels**
- `DEBUG`: Detailed information for debugging.
- `INFO`: General information about the process.
- `WARNING`: Indicates potential issues.
- `ERROR`: Indicates errors that need attention.
- `CRITICAL`: Indicates critical errors that may stop the process.

#### **Log Format**
Logs are formatted as:
```
<timestamp> - <log_level> - <message> | Metadata: <metadata>
```

Example:
```
2025-03-13 15:18:50,722 - ERROR - Attempt 1 failed for URL | Metadata: {'url': 'https://books.toscrape.com/', 'error': 'ProxyError: Unable to connect to proxy'}
```

---

### **Testing**

#### **Run Tests**
The package includes unit tests for all major components. Run the tests using `pytest`:

```bash
pytest tests/
```

---

### **Contributing**
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

### **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### **Support**
For issues or questions, please open an issue on the [GitHub repository](https://github.com/yourusername/request-sentinal).

---

This documentation follows **PEP 8** guidelines and provides a clear, structured guide for users to install, configure, and use the `request_sentinal` package. Let me know if you need further assistance!