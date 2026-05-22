import pytest
from utils.api_client import ApiClient

def test_no_auth_fails(base_url):
    client = ApiClient(base_url, "", "")
    resp = client.get("/integrations")
    assert resp.status_code == 401

def test_invalid_auth_fails(base_url):
    client = ApiClient(base_url, "wrong", "wrong")
    resp = client.get("/integrations")
    assert resp.status_code == 401

def test_valid_auth_succeeds(client1):
    resp = client1.get("/integrations")
    assert resp.status_code == 200
