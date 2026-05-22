import pytest
import time
import concurrent.futures
import os
from utils.api_client import ApiClient

@pytest.mark.load
def test_load_1000_requests_per_minute():
    base_url = os.getenv("API_BASE_URL", "http://localhost:8080/api/v1")
    username = os.getenv("TEST_USER1", "test1")
    password = os.getenv("TEST_PASS1", "test123")
    client = ApiClient(base_url, username, password)

    def make_request():
        return client.get("/integrations").status_code

    total_requests = 1000
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_request) for _ in range(total_requests)]
        done, _ = concurrent.futures.wait(futures, timeout=65)
        elapsed = time.time() - start
        completed = len(done)
        success = sum(1 for f in done if not f.exception() and f.result() < 300)
    assert completed >= total_requests * 0.95
    assert success > total_requests * 0.99
    assert elapsed <= 70
