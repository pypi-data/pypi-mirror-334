from request_sentinal.robots_checker import RobotsChecker

def test_robots_checker():
    checker = RobotsChecker("MyScraper/1.0")
    assert checker.is_allowed("http://example.com", None) == True