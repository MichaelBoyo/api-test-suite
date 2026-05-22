import requests
from requests.auth import HTTPBasicAuth

class ApiClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, **kwargs)
        return response

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, json=None):
        return self._request("POST", path, json=json)

    def put(self, path, json=None):
        return self._request("PUT", path, json=json)

    def patch(self, path, json=None):
        return self._request("PATCH", path, json=json)

    def delete(self, path):
        return self._request("DELETE", path)
