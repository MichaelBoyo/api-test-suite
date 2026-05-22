def test_contract_integrations_list(client1, spec_validator):
    resp = client1.get("/integrations")
    assert resp.status_code == 200
    spec_validator.validate_response("/integrations", "get", 200, resp.json())

def test_contract_create_integration(client1, spec_validator):
    payload = {"name": "contract_int", "type": "test"}
    resp = client1.post("/integrations", json=payload)
    assert resp.status_code == 200
    spec_validator.validate_response("/integrations", "post", 200, resp.json())

def test_contract_get_integration(client1, spec_validator):
    integration = client1.post("/integrations", json={"name": "contract_get", "type": "test"}).json()
    resp = client1.get(f"/integrations/{integration['id']}")
    spec_validator.validate_response("/integrations/{id}", "get", 200, resp.json())
