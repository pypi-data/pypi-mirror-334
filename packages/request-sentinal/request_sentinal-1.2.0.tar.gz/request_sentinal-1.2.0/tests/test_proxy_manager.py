from request_sentinal.proxy_manager import ProxyManager

def test_proxy_manager():
    proxies = ["http://proxy1.com", "http://proxy2.com"]
    manager = ProxyManager(proxies)
    assert manager.get_proxy() in proxies