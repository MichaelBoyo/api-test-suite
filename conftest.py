import os
import pytest
import requests
from utils.api_client import ApiClient
from utils.openapi_validator import OpenAPIValidator

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL", "http://localhost:8080/api/v1")

@pytest.fixture(scope="session")
def openapi_spec():
    url = "http://localhost:8080/swagger.json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    import json
    with open("openapi_spec.json", "r") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def spec_validator(openapi_spec):
    return OpenAPIValidator(openapi_spec)

@pytest.fixture
def client1(base_url):
    return ApiClient(
        base_url=base_url,
        username=os.getenv("TEST_USER1", "test1"),
        password=os.getenv("TEST_PASS1", "test123")
    )

@pytest.fixture
def client2(base_url):
    return ApiClient(
        base_url=base_url,
        username=os.getenv("TEST_USER2", "test2"),
        password=os.getenv("TEST_PASS2", "test456")
    )
