from utils.data_generators import random_integration_name

def test_create_integration(client1):
    payload = {"name": random_integration_name(), "type": "rest"}
    resp = client1.post("/integrations", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["name"] == payload["name"]

def test_create_integration_missing_fields(client1):
    resp = client1.post("/integrations", json={"name": "only"})
    assert resp.status_code == 400

def test_get_integration(client1):
    name = random_integration_name()
    create_resp = client1.post("/integrations", json={"name": name, "type": "api"})
    integration_id = create_resp.json()["id"]
    resp = client1.get(f"/integrations/{integration_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == integration_id

def test_get_nonexistent_integration(client1):
    resp = client1.get("/integrations/nonexistent")
    assert resp.status_code == 404

def test_update_integration(client1):
    create_resp = client1.post("/integrations", json={"name": "old", "type": "test"})
    integration_id = create_resp.json()["id"]
    resp = client1.put("/integrations", json={"id": integration_id, "name": "updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "updated"

def test_delete_integration(client1):
    create_resp = client1.post("/integrations", json={"name": "to_delete", "type": "test"})
    integration_id = create_resp.json()["id"]
    resp = client1.delete(f"/integrations/{integration_id}")
    assert resp.status_code == 200
    get_resp = client1.get(f"/integrations/{integration_id}")
    assert get_resp.status_code == 404
